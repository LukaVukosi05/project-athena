# Athena backend

Working FastAPI backend serving the frontend and `/api/v1/auth`, `/curriculum`,
`/lessons` and `/practice`. Start from the [root README](../README.md).

Run `python -m uvicorn app.main:app --reload` from this directory after installing
`requirements-dev.txt` and configuring `.env`. `ATHENA_JWT_SECRET` is required.
`ATHENA_DATABASE_URL` defaults to local SQLite. Development startup creates tables;
production migration and deployment work must be assessed separately.

Lesson access is enforced in `app/lessons/access.py`. For local content QA only,
`ATHENA_UNLOCK_ALL_LESSONS=true` allows lesson rendering without premium accounts.
Production configuration rejects that override. Never use it to validate access
control; the access tests explicitly turn it off.

Routes delegate payload construction to `app/lessons/` and bank/scoring/session
work to `app/practice/`. `app/api/v1/practice.py` composes topic diagnostics,
question sessions and assessments in the established route order. Its historical
`ASSESSMENT_BANKS` and `_score_assessment` imports remain available for callers.

Register Grade 8–11 lessons once in `app/practice/banks/gradeN.py`; the public
practice and private assessment catalogues are projections of that registration.
Grade 12 retains its existing practice-only catalogue. Existing curriculum and
frontend asset paths stay stable.

See [development guide](../docs/development.md) for tests and behavior parity.
