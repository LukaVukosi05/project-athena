"""Synthetic CRUD lab in backend/athena-lab.db only. Never uses the application's configured database."""

import argparse
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
DATABASE = ROOT / "backend/athena-lab.db"
EMAIL = "athena-database-lab@example.invalid"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "action", choices=["demo", "inspect", "cleanup"], default="demo", nargs="?"
    )
    args = parser.parse_args()
    # Override before importing app settings: the lab must never use real accounts.
    os.environ["ATHENA_DATABASE_URL"] = "sqlite:///" + DATABASE.as_posix()
    os.environ["ATHENA_JWT_SECRET"] = "synthetic-lab-only"
    os.environ["ATHENA_ENVIRONMENT"] = "development"
    os.environ["ATHENA_COOKIE_SECURE"] = "false"
    sys.path.insert(0, str(ROOT / "backend"))
    subprocess.run(
        [sys.executable, str(ROOT / "tools/migrate_database.py")],
        check=True,
        env=os.environ,
    )
    from sqlalchemy import delete, select, func
    from sqlalchemy.orm import Session
    from app.db.database import engine
    from app.db.models import User, PracticeSession, AuthSession, ExternalIdentity
    from app.core.security import hash_password

    print(f"Lab file: {DATABASE}")
    with Session(engine) as db:
        user = db.scalar(select(User).where(User.email == EMAIL))
        if args.action == "inspect":
            print(
                {
                    "synthetic_user": (
                        None
                        if user is None
                        else {"id": user.id, "email": user.email, "grade": user.grade}
                    ),
                    "practice_rows": db.scalar(
                        select(func.count()).select_from(PracticeSession)
                    ),
                }
            )
            return
        if user:
            for model in (PracticeSession, AuthSession, ExternalIdentity):
                db.execute(delete(model).where(model.user_id == user.id))
            db.delete(user)
            db.commit()
        if args.action == "cleanup":
            print(
                "Deleted the lab account and its related rows; the database file remains for inspection."
            )
            return
        user = User(
            first_name="Database lab",
            email=EMAIL,
            hashed_password=hash_password("lab-password-only"),
            grade="grade-8",
            curriculum_mode="CAPS",
        )
        db.add(user)
        db.commit()
        user_id = user.id
        db.add(
            PracticeSession(
                id="00000000-0000-4000-8000-000000000001",
                user_id=user_id,
                lesson_id="g8-algebraic-equations-01",
                responses={"lab-question": {"correct": False}},
            )
        )
        db.commit()
        print("CREATE committed: synthetic user + practice row.")
    with Session(engine) as db:
        user = db.get(User, user_id)
        assert user.email == EMAIL
        user.grade = "grade-9"
        db.commit()
        print("RETRIEVE from a new session and UPDATE committed: grade-9.")
    with Session(engine) as db:
        assert db.get(User, user_id).grade == "grade-9"
        db.execute(delete(PracticeSession).where(PracticeSession.user_id == user_id))
        db.commit()
        assert (
            db.scalar(
                select(func.count())
                .select_from(PracticeSession)
                .where(PracticeSession.user_id == user_id)
            )
            == 0
        )
        print(
            "DELETE committed: practice row removed. User kept so you can inspect persistence."
        )
    print("Run: python tools/database_lab.py inspect (or cleanup)")


if __name__ == "__main__":
    main()
