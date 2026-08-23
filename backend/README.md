# Backend — not yet implemented (Phase 1 = frontend only)

This directory is a scaffold, not working code. Per the brief's
Phase 1 ("Build: Web frontend, Authentication, Grade selection,
Curriculum database... No advanced AI yet") and the engineering
principle in section 65 ("never integrate an unfamiliar tool
directly — experiment, proof of concept, benchmark, wrapper,
tests, then production integration"), the backend is built
AFTER the frontend UX is validated, not alongside it.

Every file below contains only:
- a module docstring explaining what will live there
- the intended imports / responsibilities
- placeholder function or class signatures with `# TODO` bodies

Nothing here runs yet. When Phase 1 → Phase 2 begins:
1. `pip install -r requirements.txt`
2. Fill in `core/config.py` and `db/database.py` first (everything
   else depends on them)
3. Build `api/v1/auth.py` + `db/models/user.py` next, since the
   frontend's `state.js` mock needs a real session to replace it
4. Only then move to curriculum, lessons, quizzes, and finally AI

Stack (per brief section 64 and the product's open-source-first
philosophy): Python 3.12, FastAPI, PostgreSQL (via SQLAlchemy),
Supabase-style auth, open-source AI models with premium APIs as
a fallback.

## Current backend foundation

The backend now has a safe, independently testable application
foundation. It does not yet replace any frontend behaviour.

1. Create and activate a Python 3.12 virtual environment.
2. Run `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` and replace
   `ATHENA_JWT_SECRET` with a long random value.
4. Run `uvicorn app.main:app --reload` from this directory.
5. Open `http://127.0.0.1:8000/health`; it should return an
   `ok` status. Interactive API documentation is at `/docs`.

The default local database is SQLite so this layer can be validated
without infrastructure. Set `ATHENA_DATABASE_URL` to a PostgreSQL
connection URL before deploying. The next increment will add the
User model and real authentication endpoints.
