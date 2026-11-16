"""Fresh schema and backed-up adoption of the previous SQLite schema."""

import os
from pathlib import Path
import sqlite3
import subprocess
import sys
from sqlalchemy import create_engine
from app.db.database import Base
from app.db.models import User, PracticeSession

ROOT = Path(__file__).resolve().parents[2]


def migrate(path, *arguments):
    environment = dict(
        os.environ,
        ATHENA_DATABASE_URL="sqlite:///" + path.as_posix(),
        ATHENA_JWT_SECRET="migration-test-only",
        ATHENA_ENVIRONMENT="development",
    )
    return subprocess.run(
        [sys.executable, str(ROOT / "tools/migrate_database.py"), *arguments],
        env=environment,
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def test_new_database_and_safe_existing_database_adoption(tmp_path):
    fresh = tmp_path / "fresh.db"
    result = migrate(fresh)
    assert result.returncode == 0, result.stderr
    with sqlite3.connect(fresh) as db:
        assert (
            db.execute("SELECT version_num FROM alembic_version").fetchone()[0]
            == "0002_auth_sessions"
        )
        assert {
            "users",
            "practice_sessions",
            "auth_sessions",
            "external_identities",
        } <= {
            row[0]
            for row in db.execute("SELECT name FROM sqlite_master WHERE type='table'")
        }
    old = tmp_path / "old.db"
    engine = create_engine("sqlite:///" + old.as_posix())
    Base.metadata.create_all(engine, tables=[User.__table__, PracticeSession.__table__])
    with sqlite3.connect(old) as db:
        db.execute(
            "INSERT INTO users (first_name,email,hashed_password,grade,curriculum_mode,role,is_premium) VALUES (?,?,?,?,?,?,?)",
            (
                "Existing learner",
                "existing@example.com",
                "unchanged-hash",
                "grade-11",
                "CAPS",
                "learner",
                0,
            ),
        )
    denied = migrate(old)
    assert denied.returncode != 0 and "--adopt-existing" in denied.stderr
    result = migrate(old, "--adopt-existing")
    assert result.returncode == 0, result.stderr
    backup = list((tmp_path / "backups").glob("*.db"))
    assert len(backup) == 1
    for file in [old, backup[0]]:
        with sqlite3.connect(file) as db:
            assert db.execute("SELECT email,hashed_password FROM users").fetchone() == (
                "existing@example.com",
                "unchanged-hash",
            )
    assert migrate(old).returncode == 0
    engine.dispose()
