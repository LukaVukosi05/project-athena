# Database and release plan

## Start now: isolated local SQLite

SQLite is suitable for a single-machine local test workflow and needs no extra
server. It is not a promise of unlimited throughput: it has one writer at a time.
See [SQLite's deployment guidance](https://www.sqlite.org/whentouse.html).
For a shared beta and deployment, plan PostgreSQL, keeping SQLAlchemy and Alembic
as the database boundary. Benchmark realistic practice writes and session reads
before choosing capacity; don't buy infrastructure before there is usage.

Run from the repository root:

```powershell
python tools/database_lab.py demo
python tools/database_lab.py inspect
python tools/database_lab.py cleanup
```

These commands use **only `backend/athena-lab.db`**, regardless of the application's
normal database environment. Demo commits a synthetic `.invalid` account and a
practice row, reloads them through a new database session, updates the grade,
then deletes the practice row and confirms deletion. The account stays for
inspection until cleanup. Cleanup deletes that synthetic account and its related
rows; it does not delete the database file or unrelated accounts.

Inspect the file with a SQLite viewer (for example a SQLite extension in VS Code)
and run `SELECT id, email, grade FROM users;` or
`SELECT id, user_id, lesson_id FROM practice_sessions;`. Inspect schema with
`SELECT name FROM sqlite_master WHERE type = 'table';`.
Never paste real password hashes/session hashes into screenshots or support chats.
Do not manually change premium flags or delete real learner rows as a test.

## What is stored today

| Data | Storage / current boundary |
| --- | --- |
| Account profile and password hash | `users`; existing signup/login/profile APIs |
| Provider identity | `external_identities`; unique `(provider, subject)` mapped to a user |
| Renewable browser session | `auth_sessions`; SHA-256 hash of a random secret, user ID and expiry |
| Practice responses, mastery and reassessment | `practice_sessions`; existing server-authoritative practice API |
| Legacy page completion / quiz cache | Browser state; not fully synchronised across devices yet |
| Guardian/learner relationships, subscriptions and billing | Still separate product/database work; not implemented by this patch |

JWT access credentials are short-lived and compatible with current endpoints.
The renewable cookie is HttpOnly and the raw secret is not stored in SQL. Logout
revokes the browser session. Access JWTs already issued can remain valid until
their default 30-minute expiry; immediate per-access-token revocation is future
work. Expired session-row cleanup also needs an operational job before deployment.

## Migrations and existing databases

`0001_existing_core` records the existing users/practice schema;
`0002_auth_sessions` adds session and provider tables. Fresh test databases run
`python tools/migrate_database.py`. For an existing SQLite database:

1. Stop the app and independently back up the database.
2. Set the correct `ATHENA_DATABASE_URL` and test the process on a copy first.
3. Run `python tools/migrate_database.py --adopt-existing`.
4. The tool checks known tables, columns, basic types/nullability, keys and
   identity/email uniqueness, makes an SQLite backup with an integrity check,
   records the recognised baseline and upgrades. Unknown/partial schemas fail.
5. Inspect rows and restore the backup in a separate test directory to verify
   recovery. The user's previous measurement database has not been inspected or
   adopted here; do not assume it has the expected schema.

Automatic table creation in development remains for compatibility. If it created
all four tables before Alembic was initialised, adoption validates them and stamps
the matching revision. Production must run migrations explicitly before starting
the app. Existing PostgreSQL adoption requires a reviewed schema comparison and
verified `pg_dump`/restore; the SQLite auto-adoption flag does not apply there.
Destructive downgrades are deliberately blocked; use an explicit restore plan.

## Next stages and exit criteria

| Stage | Work | Evidence before moving on |
| --- | --- | --- |
| This local patch | Session renewal, sign-in design, provider adapters, schema versions and CRUD lab | Unit/integration checks, local navigation/expiry/logout test, patch applies cleanly |
| Provider staging | Separate Google/Apple credentials, HTTPS, correct callback and cookies | Real consent, cancellation, repeat sign-in, Apple relay and iOS/Safari checks |
| Shared beta database | PostgreSQL staging; migrations, connection pooling, indexes, backups and least-privilege service account | Migration/CRUD/ownership tests on PostgreSQL, backup restore, concurrent practice load test |
| Account completeness | Password recovery, verified email, authenticated provider linking, account deletion/export and guardian relationships | Abuse/rate limits, consent/retention decisions, cross-device progress and deletion tests |
| Launch gate | Security review, production session/revocation policy, monitoring and incident/restore runbooks | No unresolved account/authorisation blocker; no production secrets or learner data in Git |

PostgreSQL transactions support atomic updates/deletes; see the
[PostgreSQL transaction tutorial](https://www.postgresql.org/docs/current/tutorial-transactions.html).
Avoid exposing generic table-editing/SQL endpoints to the frontend. Add specific
ownership-checked application APIs as each feature needs them. Account deletion
must include session/identity/practice retention rules; the lab cleanup is not a
finished customer account-deletion feature. Parent/guardian consent, children's
data handling and account recovery are release work, not solved by social login.

## Protecting the work

Keep each new feature on a branch from verified main. Keep source, tests, migration
and the decision/testing notes together in one reviewable change. Save the branch
and a dated patch; do not merge an untested feature directly into main. Use separate
local, staging and production databases/credentials and never copy real learner
data into a public issue or patch. Confirm Git status, migration state, tests,
secrets exclusion and database backups at each release. Deploy code and its schema
migration as a coordinated release, with a tested restore/rollback decision.

The refactor checkpoint `442e8a4` remains the application rollback point for this
feature. No production database or main-branch change is part of the downloadable
patch handoff.
