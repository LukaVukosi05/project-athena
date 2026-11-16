"""Renewal, logout, CSRF and real OIDC validation with an offline provider transport."""

import time
from urllib.parse import parse_qs, urlsplit
import httpx
import pytest
from authlib.integrations.starlette_client import OAuth
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
from app.core.config import get_settings
from app.db.database import Base, get_db
from app.db.models import AuthSession, ExternalIdentity, User
from app.main import app
from app.api.v1 import social_auth


@pytest.fixture
def client():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)

    def database():
        with Session(engine) as db:
            yield db

    original = dict(app.dependency_overrides)
    app.dependency_overrides[get_db] = database
    try:
        with TestClient(app) as client:
            yield client, engine
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(original)
        Base.metadata.drop_all(engine)
        engine.dispose()


def account(client, remember=False):
    payload = {
        "first_name": "Test",
        "email": "auth@example.com",
        "password": "strong-password",
        "grade": "grade-8",
    }
    assert client.post("/api/v1/auth/signup", json=payload).status_code == 201
    return client.post(
        "/api/v1/auth/login",
        json={
            "email": payload["email"],
            "password": payload["password"],
            "remember_me": remember,
        },
    )


def test_session_renewal_and_revoke(client):
    client, engine = client
    login = account(client, True)
    cookie = login.headers["set-cookie"]
    assert (
        "HttpOnly" in cookie
        and "Max-Age=2592000" in cookie
        and "SameSite=lax" in cookie
    )
    with Session(engine) as db:
        row = db.scalar(select(AuthSession))
        assert len(row.token_hash) == 64 and row.token_hash not in cookie
    assert (
        client.post("/api/v1/auth/refresh").json()["user"]["email"]
        == "auth@example.com"
    )
    # Renewal remains safe across concurrent tabs: the browser secret is stable until logout/expiry.
    assert client.post("/api/v1/auth/refresh").status_code == 200
    old_cookie = client.cookies.get("athena_session")
    assert client.post("/api/v1/auth/logout").status_code == 200
    client.cookies.set("athena_session", old_cookie, path="/api/v1/auth")
    assert client.post("/api/v1/auth/refresh").status_code == 401


def test_session_cookie_and_cross_site_csrf(client):
    client, _ = client
    response = account(client)
    assert "Max-Age" not in response.headers["set-cookie"]
    assert (
        client.post(
            "/api/v1/auth/refresh", headers={"Origin": "https://attacker.invalid"}
        ).status_code
        == 403
    )
    assert (
        client.post(
            "/api/v1/auth/logout", headers={"Sec-Fetch-Site": "cross-site"}
        ).status_code
        == 403
    )
    assert client.post("/api/v1/auth/refresh").status_code == 200


@pytest.fixture
def offline_provider(monkeypatch):
    private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    pem = private.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    )
    numbers = private.public_key().public_numbers()
    from jose.utils import base64url_encode

    encode = lambda n: base64url_encode(
        n.to_bytes((n.bit_length() + 7) // 8, "big")
    ).decode()
    jwk = {
        "kty": "RSA",
        "kid": "test",
        "use": "sig",
        "alg": "RS256",
        "n": encode(numbers.n),
        "e": encode(numbers.e),
    }
    context = {"nonce": None, "change": {}}
    metadata = {
        "issuer": "https://provider.test",
        "authorization_endpoint": "https://provider.test/authorize",
        "token_endpoint": "https://provider.test/token",
        "jwks_uri": "https://provider.test/keys",
        "id_token_signing_alg_values_supported": ["RS256"],
    }

    def transport(request):
        if request.url.path == "/discovery":
            return httpx.Response(200, json=metadata)
        if request.url.path == "/keys":
            return httpx.Response(200, json={"keys": [jwk]})
        if request.url.path == "/token":
            claims = {
                "iss": "https://provider.test",
                "sub": "stable-subject",
                "aud": "test-client",
                "iat": int(time.time()),
                "exp": int(time.time()) + 300,
                "nonce": context["nonce"],
                "email": "social@example.com",
                "email_verified": True,
                "given_name": "Lerato",
            }
            claims.update(context["change"])
            signed = jwt.encode(claims, pem, algorithm="RS256", headers={"kid": "test"})
            if context.get("corrupt"):
                signed = signed.rsplit(".", 1)[0] + "." + "A" * 342
            return httpx.Response(
                200,
                json={
                    "access_token": "unused-provider-token",
                    "token_type": "Bearer",
                    "id_token": signed,
                },
            )
        raise AssertionError(request.url)

    oauth = OAuth()
    real_client = oauth.register(
        "google",
        client_id="test-client",
        client_secret="test-secret",
        server_metadata_url="https://provider.test/discovery",
        client_kwargs={
            "scope": "openid email profile",
            "transport": httpx.MockTransport(transport),
        },
    )
    monkeypatch.setattr(
        social_auth, "available_providers", lambda: {"google": True, "apple": True}
    )
    monkeypatch.setattr(social_auth, "oauth_client", lambda provider: real_client)
    return context


def start_and_callback(client, context, provider="google", state_override=None):
    response = client.get(
        f"/api/v1/auth/oauth/{provider}/start?next=/lesson.html?lesson=g8-algebraic-equations-01",
        follow_redirects=False,
    )
    assert response.status_code == 302
    params = parse_qs(urlsplit(response.headers["location"]).query)
    context["nonce"] = params["nonce"][0]
    state = state_override or params["state"][0]
    if provider == "apple":
        return client.post(
            f"/api/v1/auth/oauth/{provider}/callback",
            data={"state": state, "code": "one-use-test-code"},
            follow_redirects=False,
        )
    return client.get(
        f"/api/v1/auth/oauth/{provider}/callback",
        params={"state": state, "code": "one-use-test-code"},
        follow_redirects=False,
    )


@pytest.mark.parametrize("provider", ["google", "apple"])
def test_social_onboarding_and_returning_user(client, offline_provider, provider):
    client, engine = client
    result = start_and_callback(client, offline_provider, provider)
    assert result.headers["location"] == "/oauth-onboarding.html"
    pending = client.get("/api/v1/auth/oauth/pending").json()
    payload = {"first_name": "Lerato", "grade": "grade-11", "curriculum_mode": "CAPS"}
    assert client.post("/api/v1/auth/oauth/complete", json=payload).status_code == 403
    completed = client.post(
        "/api/v1/auth/oauth/complete",
        json=payload,
        headers={"X-CSRF-Token": pending["csrf"]},
    )
    assert completed.status_code == 200, completed.text
    assert completed.json()["user"]["grade"] == "grade-11"
    assert (
        client.post(
            "/api/v1/auth/oauth/complete",
            json=payload,
            headers={"X-CSRF-Token": pending["csrf"]},
        ).status_code
        == 401
    )
    with Session(engine) as db:
        identity = db.scalar(select(ExternalIdentity))
        assert identity.provider == provider and identity.subject == "stable-subject"
    returned = start_and_callback(client, offline_provider, provider)
    assert "/login.html?oauth=success" in returned.headers["location"]
    assert client.post("/api/v1/auth/refresh").status_code == 200


@pytest.mark.parametrize(
    "change",
    [
        {"iss": "https://attacker.invalid"},
        {"aud": "wrong-client"},
        {"nonce": "wrong-nonce"},
        {"exp": 1},
        {"email_verified": False},
    ],
)
def test_real_oidc_rejects_invalid_claims(client, offline_provider, change):
    client, engine = client
    offline_provider["change"] = change
    result = start_and_callback(client, offline_provider)
    assert result.headers["location"] == "/login.html?oauth_error=verification"
    with Session(engine) as db:
        assert db.scalar(select(User)) is None


def test_oidc_state_signature_and_account_collision(client, offline_provider):
    client, engine = client
    assert (
        "verification"
        in start_and_callback(
            client, offline_provider, state_override="forged"
        ).headers["location"]
    )
    offline_provider["corrupt"] = True
    assert (
        "verification"
        in start_and_callback(client, offline_provider).headers["location"]
    )
    offline_provider["corrupt"] = False
    account(client)
    offline_provider["change"] = {"email": "auth@example.com"}
    assert (
        "existing_account"
        in start_and_callback(client, offline_provider).headers["location"]
    )
    with Session(engine) as db:
        assert db.scalar(select(ExternalIdentity)) is None


def test_unconfigured_providers_are_explicit(client):
    client, _ = client
    assert client.get("/api/v1/auth/providers").json() == {
        "google": False,
        "apple": False,
    }
    assert client.get("/api/v1/auth/oauth/google/start").status_code == 503
