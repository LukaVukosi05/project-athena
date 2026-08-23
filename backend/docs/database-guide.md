# Database guide

Project Athena currently uses the database configured by
`ATHENA_DATABASE_URL`. Local development uses `backend/athena.db`, a SQLite
database. PostgreSQL can be selected by changing the connection URL.

## Safe built-in inspection

From `backend/`, run:

```powershell
.\.venv\Scripts\python.exe -m app.cli.db_inspect
```

Use `--schema-only` to show tables, columns, indexes and foreign keys, or
`--users-only` to list safe account fields. The tool deliberately never prints
password hashes.

## Graphical viewing

Open `backend/athena.db` with DB Browser for SQLite or SQLiteStudio. Stop the
development server before performing manual writes. Do not edit
`hashed_password`; use the signup/login APIs so passwords remain scrypt-hashed.

The current persisted schema contains `users`. Curriculum structure is
source-controlled and validated with Pydantic; progress, attempts and mastery
models are the next database migration rather than pretending placeholder
tables are complete.
