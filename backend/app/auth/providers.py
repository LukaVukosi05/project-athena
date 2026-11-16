"""Provider configuration and OIDC clients; secrets never reach the browser."""

from datetime import datetime, timedelta, timezone
from urllib.parse import urlsplit
from authlib.integrations.starlette_client import OAuth
from jose import jwt
from app.core.config import get_settings


def available_providers() -> dict[str, bool]:
    settings = get_settings()
    base = urlsplit(settings.public_base_url)
    return {
        "google": bool(settings.google_client_id and settings.google_client_secret),
        "apple": bool(
            settings.apple_client_id
            and settings.apple_team_id
            and settings.apple_key_id
            and settings.apple_private_key
            and settings.cookie_secure
            and base.scheme == "https"
            and base.hostname not in {"localhost", "127.0.0.1"}
        ),
    }


def oauth_client(provider: str):
    settings = get_settings()
    oauth = OAuth()
    if provider == "google":
        return oauth.register(
            "google",
            client_id=settings.google_client_id,
            client_secret=settings.google_client_secret,
            server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
            client_kwargs={
                "scope": "openid email profile",
                "code_challenge_method": "S256",
            },
        )
    now = datetime.now(timezone.utc)
    secret = jwt.encode(
        {
            "iss": settings.apple_team_id,
            "iat": now,
            "exp": now + timedelta(minutes=5),
            "aud": "https://appleid.apple.com",
            "sub": settings.apple_client_id,
        },
        settings.apple_private_key.replace("\\n", "\n"),
        algorithm="ES256",
        headers={"kid": settings.apple_key_id},
    )
    return oauth.register(
        "apple",
        client_id=settings.apple_client_id,
        client_secret=secret,
        server_metadata_url="https://appleid.apple.com/.well-known/openid-configuration",
        client_kwargs={
            "scope": "openid email name",
            "token_endpoint_auth_method": "client_secret_post",
        },
    )
