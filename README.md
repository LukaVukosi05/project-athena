# Project Athena

South African Grade 8–12 mathematics learning application with structured lessons,
question-specific whiteboards, self-guided practice and mastery/reassessment flows.
Curriculum files include material awaiting review; a registered lesson is not a
claim of teacher approval or launch readiness.

## Run locally

Use Python 3.12 and Node.js with the built-in test runner. The backend serves both
the API and the plain HTML/CSS/JavaScript frontend; there is no frontend build.

```bash
python -m venv .venv
# Activate .venv using your shell's activation command.
python -m pip install -r backend/requirements-dev.txt
cd backend
# Copy .env.example to .env and set ATHENA_JWT_SECRET to a random secret.
python -m uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/ for the app, `/health` for health and `/docs` for API
reference. A standalone static server cannot provide the curriculum or auth API.
The default development database is SQLite. Keep local databases and `.env` files
out of Git; use a separate database for tests.

## Code ownership

| Location | Responsibility |
| --- | --- |
| `backend/app/api/v1/` | HTTP validation, authentication dependencies and routing |
| `backend/app/lessons/` | Entitlement and public lesson/whiteboard payload policies |
| `backend/app/practice/banks/` | Grade 8–11 practice and assessment registrations, grouped by grade |
| `backend/app/practice/` | Bank projections, answer scoring, session persistence and practice state |
| `backend/app/curriculum/` | Authored curriculum, lesson schemas, catalogue and readiness rules |
| `backend/app/db/`, `core/` | ORM models, database, settings and security |
| `frontend/js/engine/` | Shared browser state, navigation and HTML escaping; legacy engines |
| `frontend/js/pages/` | Page controllers |
| `frontend/js/lessons/`, `whiteboard/`, `visualization/`, `math/` | Lesson components and native rendering |
| `docs/curriculum/` | Curriculum sources and review evidence |
| `tools/`, `scripts/` | Authoring, validation and catalogue utilities; not runtime imports |
| `backend/tests/`, `frontend/tests/` | Regression checks |

See [development and file-management guide](docs/development.md) for extension
rules, safe test commands and the behavior comparison tool.

## Current limits

The mounted APIs are auth, curriculum, lessons and practice. Payment, quiz-router
and AI-tutor scaffolds do not establish working billing or a live AI tutor. Client
localStorage is not authoritative for purchased entitlement. Teacher review,
production deployment, privacy and commercial readiness remain separate work.
