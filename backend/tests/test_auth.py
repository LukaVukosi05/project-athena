import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.db.database import Base, get_db
from app.main import app


@pytest.fixture
def auth_client():
    test_engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(test_engine)

    def test_db():
        with Session(test_engine) as session:
            yield session

    app.dependency_overrides[get_db] = test_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(test_engine)


def test_signup_login_profile_and_grade_are_database_backed(auth_client):
    signup = auth_client.post("/api/v1/auth/signup", json={
        "first_name": "Lerato", "email": "Lerato@Example.com",
        "password": "strong-password", "grade": "grade-12",
        "curriculum_mode": "CAPS",
    })
    assert signup.status_code == 201
    assert signup.json()["user"]["grade"] == "grade-12"
    assert signup.json()["user"]["email"] == "lerato@example.com"

    login = auth_client.post("/api/v1/auth/login", json={
        "email": "lerato@example.com", "password": "strong-password"
    })
    assert login.status_code == 200
    headers = {"Authorization": f"Bearer {login.json()['access_token']}"}
    profile = auth_client.get("/api/v1/auth/me", headers=headers)
    assert profile.status_code == 200
    assert profile.json()["grade"] == "grade-12"

    updated = auth_client.patch("/api/v1/auth/me", headers=headers, json={"grade": "grade-11"})
    assert updated.status_code == 200
    assert updated.json()["grade"] == "grade-11"
    login_again = auth_client.post("/api/v1/auth/login", json={
        "email": "lerato@example.com", "password": "strong-password"
    })
    assert login_again.json()["user"]["grade"] == "grade-11"


def test_login_rejects_wrong_password_and_duplicate_email(auth_client):
    payload = {"first_name": "Anele", "email": "anele@example.com",
               "password": "correct-password", "grade": "grade-10",
               "curriculum_mode": "IEB"}
    assert auth_client.post("/api/v1/auth/signup", json=payload).status_code == 201
    assert auth_client.post("/api/v1/auth/signup", json=payload).status_code == 409
    wrong = auth_client.post("/api/v1/auth/login", json={
        "email": payload["email"], "password": "wrong-password"
    })
    assert wrong.status_code == 401
