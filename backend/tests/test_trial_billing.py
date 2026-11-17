from datetime import datetime, timedelta, timezone
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
from app.main import app
from app.core.config import get_settings, Settings
from app.core.security import create_access_token
from app.db.database import Base, get_db
from app.db.models import User, TrialSubscription, BillingNotification
from app.billing import service
from app.billing.plan import TERMS_VERSION


@pytest.fixture
def billing(monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "billing_test_mode", True)
    monkeypatch.setattr(settings, "environment", "development")
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    with Session(engine) as db:
        for n in (1, 2):
            db.add(
                User(
                    id=n,
                    first_name="Test",
                    email=f"trial{n}@example.invalid",
                    hashed_password="test-only",
                    grade="grade-11",
                    curriculum_mode="CAPS",
                )
            )
        db.commit()

    def database():
        with Session(engine) as db:
            yield db

    app.dependency_overrides[get_db] = database
    clock = [datetime(2026, 11, 17, 12, 30, tzinfo=timezone.utc)]
    monkeypatch.setattr(service, "now", lambda: clock[0])
    with TestClient(app) as client:
        client.headers["Authorization"] = "Bearer " + create_access_token(1)
        yield client, engine, clock
    app.dependency_overrides.clear()
    engine.dispose()


def authorise(client, **changes):
    return client.post(
        "/api/v1/payments/test/authorise",
        json={
            "consent": True,
            "adult_payer": True,
            "terms_version": TERMS_VERSION,
            **changes,
        },
    )


def test_clock_starts_only_on_success_and_full_fourteen_days_precede_charge(billing):
    client, engine, clock = billing
    assert client.get("/api/v1/payments/status").json()["status"] == "not_started"
    assert authorise(client, outcome="declined").status_code == 402
    assert client.get("/api/v1/payments/status").json()["status"] == "not_started"
    first = authorise(client).json()
    start = datetime.fromisoformat(first["authorised_at"])
    end = datetime.fromisoformat(first["trial_ends_at"])
    assert end - start == timedelta(days=14)
    assert first["real_money_charged"] is False
    clock[0] = end - timedelta(microseconds=1)
    assert client.post("/api/v1/payments/test/first-charge").status_code == 409
    assert authorise(client).json()["trial_ends_at"] == first["trial_ends_at"]
    clock[0] = end
    paid = client.post("/api/v1/payments/test/first-charge").json()
    assert paid["amount_cents"] == 14900 and paid["status"] == "active_test"
    assert datetime.fromisoformat(paid["first_charge_at"]) >= end
    assert (
        client.post("/api/v1/payments/test/first-charge").json()["first_charge_at"]
        == paid["first_charge_at"]
    )
    with Session(engine) as db:
        assert db.get(User, 1).is_premium is False  # no permanent entitlement mutation
        row = db.get(TrialSubscription, 1)
        assert row.method_reference.startswith("test_")
        notices = db.scalars(select(BillingNotification)).all()
        assert len(notices) == 2
        reminder = next(n for n in notices if n.kind == "trial_reminder")
        assert service.utc(reminder.due_at) == end - timedelta(days=7)


def test_cancellation_and_account_isolation(billing):
    client, _, _ = billing
    first = authorise(client).json()
    client.headers["Authorization"] = "Bearer " + create_access_token(2)
    assert client.get("/api/v1/payments/status").json()["status"] == "not_started"
    assert client.post("/api/v1/payments/cancel").status_code == 404
    client.headers["Authorization"] = "Bearer " + create_access_token(1)
    canceled = client.post("/api/v1/payments/cancel").json()
    assert canceled["status"] == "canceled" and canceled["has_test_access"]
    client.post("/api/v1/payments/test/advance")
    assert client.post("/api/v1/payments/test/first-charge").status_code == 409
    assert not client.get("/api/v1/payments/status").json()["has_test_access"]
    assert authorise(client).json()["trial_ends_at"] == first["trial_ends_at"]


def test_consent_csrf_no_card_fields_and_production_gate(billing, monkeypatch):
    client, _, _ = billing
    assert authorise(client, consent=False).status_code == 422
    assert authorise(client, adult_payer=False).status_code == 422
    assert authorise(client, terms_version="old").status_code == 409
    assert authorise(client, card_number="not-a-card").status_code == 422
    assert (
        client.post(
            "/api/v1/payments/test/authorise",
            headers={"Origin": "https://untrusted.invalid"},
            json={"consent": True, "adult_payer": True, "terms_version": TERMS_VERSION},
        ).status_code
        == 403
    )
    monkeypatch.setattr(get_settings(), "environment", "production")
    for route in ("test/authorise", "test/advance", "test/first-charge", "cancel"):
        assert client.post("/api/v1/payments/" + route, json={}).status_code == 503
    with pytest.raises(ValueError, match="only available in development"):
        Settings(
            _env_file=None,
            jwt_secret="test",
            environment="production",
            billing_test_mode=True,
        )


def test_offer_and_test_clock(billing):
    client, _, _ = billing
    offer = client.get("/api/v1/payments/plan").json()
    assert offer["interactive_lessons"] == 399 and offer["topics"] == 58
    assert (
        offer["practice_questions"] == 5688 and offer["live_payments_enabled"] is False
    )
    first = authorise(client).json()
    moved = client.post("/api/v1/payments/test/advance").json()
    assert (
        moved["status"] == "trial_ended"
        and moved["test_clock_at"] == first["trial_ends_at"]
    )
    assert (
        client.post("/api/v1/payments/test/first-charge").json()["status"]
        == "active_test"
    )
    client.headers.pop("Authorization")
    assert client.get("/api/v1/payments/status").status_code == 401


def test_signin_membership_decision_uses_server_access_state(billing):
    client, engine, _ = billing
    assert client.get("/api/v1/payments/status").json()["has_access"] is False
    authorise(client)
    assert client.get("/api/v1/payments/status").json()["has_access"] is True
    client.post("/api/v1/payments/cancel")
    assert client.get("/api/v1/payments/status").json()["has_access"] is True
    client.post("/api/v1/payments/test/advance")
    assert client.get("/api/v1/payments/status").json()["has_access"] is False
    client.headers["Authorization"] = "Bearer " + create_access_token(2)
    with Session(engine) as db:
        db.get(User, 2).is_premium = True
        db.commit()
    assert client.get("/api/v1/payments/status").json()["has_access"] is True


def test_old_and_unsafe_auth_destinations_fall_back_to_agreed_landing():
    from app.auth.sessions import safe_next

    for value in (
        None,
        "/dashboard.html",
        "/dashboard.html?grade=grade-9",
        "//other.example",
        "https://other.example",
    ):
        assert safe_next(value) == "/index.html"
    assert safe_next("/lesson.html?lesson=g11-es-01") == "/lesson.html?lesson=g11-es-01"


def test_preview_access_does_not_become_production_membership(billing, monkeypatch):
    client, _, _ = billing
    authorise(client)
    assert client.get("/api/v1/payments/status").json()["has_access"] is True
    monkeypatch.setattr(get_settings(), "environment", "production")
    assert client.get("/api/v1/payments/status").json()["has_access"] is False
