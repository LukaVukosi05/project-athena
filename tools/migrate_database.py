"""Upgrade a new database, or validate/backup/adopt an existing local SQLite schema."""

import argparse
from datetime import datetime, timezone
import os
from pathlib import Path
import sqlite3
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))


def main():
    from alembic import command
    from alembic.config import Config
    from sqlalchemy import inspect
    from app.db.database import Base, engine
    from app.db import models  # noqa: F401

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--adopt-existing",
        action="store_true",
        help="Validate and snapshot an existing SQLite database before recording its baseline",
    )
    args = parser.parse_args()
    inspector = inspect(engine)
    names = set(inspector.get_table_names())
    config = Config(str(ROOT / "backend/alembic.ini"))
    if names and "alembic_version" not in names:
        if not args.adopt_existing or engine.dialect.name != "sqlite":
            raise SystemExit(
                "Existing unversioned database: stop the app, back it up and use --adopt-existing for SQLite. PostgreSQL requires a reviewed baseline adoption."
            )
        expected = {"users", "practice_sessions"}
        auth = {"auth_sessions", "external_identities"}
        billing = {"trial_subscriptions", "billing_notifications"}
        if (
            not expected <= names
            or names - expected - auth - billing
            or (names & auth and not auth <= names)
            or (names & billing and not (billing | auth) <= names)
        ):
            raise SystemExit("Unrecognised/partial schema. No adoption performed.")
        for name in names:
            wanted = Base.metadata.tables[name]
            actual = {column["name"]: column for column in inspector.get_columns(name)}
            if set(actual) != set(wanted.columns.keys()):
                raise SystemExit(f"Column mismatch in {name}. No adoption performed.")
            for column in wanted.columns:
                found = actual[column.name]
                if (
                    found["type"]._type_affinity != column.type._type_affinity
                    or found["nullable"] != column.nullable
                ):
                    raise SystemExit(
                        f"Type/nullability mismatch in {name}.{column.name}."
                    )
                if getattr(column.type, "length", None) != getattr(
                    found["type"], "length", None
                ):
                    raise SystemExit(f"Column length mismatch in {name}.{column.name}.")
            if set(inspector.get_pk_constraint(name)["constrained_columns"]) != set(
                column.name for column in wanted.primary_key.columns
            ):
                raise SystemExit(f"Primary key mismatch in {name}.")
            actual_fk = {
                (
                    tuple(fk["constrained_columns"]),
                    fk["referred_table"],
                    tuple(fk["referred_columns"]),
                )
                for fk in inspector.get_foreign_keys(name)
            }
            expected_fk = {
                ((fk.parent.name,), fk.column.table.name, (fk.column.name,))
                for fk in wanted.foreign_keys
            }
            if actual_fk != expected_fk:
                raise SystemExit(f"Foreign key mismatch in {name}.")
            unique = {
                tuple(item["column_names"])
                for item in inspector.get_indexes(name)
                if item.get("unique")
            }
            unique |= {
                tuple(item["column_names"])
                for item in inspector.get_unique_constraints(name)
            }
            if name == "users" and ("email",) not in unique:
                raise SystemExit("Missing unique user email constraint.")
            if name == "external_identities" and ("provider", "subject") not in unique:
                raise SystemExit("Missing provider subject uniqueness.")
        source = Path(engine.url.database).resolve()
        if not source.is_file():
            raise SystemExit("Adoption requires a local SQLite file.")
        backup = (
            source.parent
            / "backups"
            / (
                source.stem
                + "-"
                + datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S-%f")
                + ".db"
            )
        )
        backup.parent.mkdir(exist_ok=True)
        with sqlite3.connect(source) as original, sqlite3.connect(
            backup
        ) as destination:
            original.backup(destination)
            assert destination.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
        print(f"Validated SQLite backup: {backup}")
        command.stamp(
            config,
            (
                "0003_trial_subscriptions"
                if billing <= names
                else "0002_auth_sessions" if auth <= names else "0001_existing_core"
            ),
        )
    command.upgrade(config, "head")
    print("Database schema is at the latest revision. No learner records were deleted.")


if __name__ == "__main__":
    main()
