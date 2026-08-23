"""Inspect Athena's configured database without exposing password hashes."""

import argparse
import json

from sqlalchemy import inspect, select

from app.db.database import SessionLocal, engine
from app.db.models.user import User


def schema_report() -> dict:
    inspector = inspect(engine)
    return {table: {
        "columns": [{"name": column["name"], "type": str(column["type"]),
                     "nullable": column["nullable"]} for column in inspector.get_columns(table)],
        "indexes": inspector.get_indexes(table),
        "foreign_keys": inspector.get_foreign_keys(table),
    } for table in inspector.get_table_names()}


def user_report() -> list[dict]:
    with SessionLocal() as db:
        users = db.scalars(select(User).order_by(User.id)).all()
        return [{"id": user.id, "first_name": user.first_name, "email": user.email,
                 "grade": user.grade, "curriculum_mode": user.curriculum_mode,
                 "role": user.role, "is_premium": user.is_premium,
                 "created_at": user.created_at.isoformat() if user.created_at else None}
                for user in users]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schema-only", action="store_true")
    parser.add_argument("--users-only", action="store_true")
    args = parser.parse_args()
    report = {}
    if not args.users_only:
        report["schema"] = schema_report()
    if not args.schema_only:
        report["users"] = user_report()
    print(json.dumps(report, indent=2, default=str))


if __name__ == "__main__":
    main()
