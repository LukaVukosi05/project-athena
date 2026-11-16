"""HTTP ownership and persistence checks for the extracted session store."""

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.core.security import get_optional_user
from app.db.database import Base, get_db
from app.db.models.user import User
from app.main import app


def test_authenticated_practice_session_cannot_be_restored_by_another_user():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    owner = User(id=101, is_premium=True)
    other = User(id=102, is_premium=True)

    def test_db():
        with Session(engine) as session:
            yield session

    original = dict(app.dependency_overrides)
    app.dependency_overrides[get_db] = test_db
    app.dependency_overrides[get_optional_user] = lambda: owner
    try:
        with TestClient(app) as client:
            root = "/api/v1/practice/g8-algebraic-equations-01"
            started = client.post(root + "/sessions")
            assert started.status_code == 200
            url = root + "/sessions/" + started.json()["session_id"]
            question = client.get(root).json()["questions"][0]["id"]
            hint = client.post(url + "/questions/" + question + "/hint")
            assert hint.status_code == 200
            restored = client.get(url)
            assert restored.status_code == 200
            assert restored.json()["states"][question]["hints_used"] == 1

            app.dependency_overrides[get_optional_user] = lambda: other
            assert client.get(url).status_code == 404
            assert (
                client.post(url + "/questions/" + question + "/hint").status_code == 404
            )
            app.dependency_overrides[get_optional_user] = lambda: None
            assert client.get(url).status_code == 404
            app.dependency_overrides[get_optional_user] = lambda: owner
            assert client.get(root + "/sessions/not-a-uuid").status_code == 404
            wrong_lesson = url.replace(
                "g8-algebraic-equations-01", "g8-algebraic-equations-02"
            )
            assert client.get(wrong_lesson).status_code == 404
            assert client.get(url).json()["states"][question]["hints_used"] == 1
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(original)
        Base.metadata.drop_all(engine)
        engine.dispose()
