"""FastAPI application entrypoint for the Athena API."""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text

from app.api.v1.auth import router as auth_router
from app.api.v1.curriculum import router as curriculum_router
from app.api.v1.lessons import router as lessons_router
from app.api.v1.practice import router as practice_router
from app.core.config import get_settings
from app.db.database import Base, engine
from app.db.models import PracticeSession, User  # noqa: F401 - registers models before table creation
from app.curriculum.content_manifest import readiness_for
from app.curriculum.repository import curriculum_repository

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Fail fast when the configured database cannot be reached."""
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    if settings.environment == "development":
        Base.metadata.create_all(bind=engine)
    diagnostics = curriculum_repository.diagnostics()
    lessons = [
        lesson
        for grade in curriculum_repository.list_grades()
        for topic in grade.topics
        for subtopic in topic.subtopics
        for lesson in subtopic.lessons
    ]
    published = sum(readiness_for(lesson).value == "published" for lesson in lessons)
    roadmap = sum(readiness_for(lesson).value in {"roadmap", "specified", "anchored"} for lesson in lessons)
    print(
        "Curriculum loaded: "
        f"{diagnostics['grades']} grades, {diagnostics['topics']} topics, "
        f"{diagnostics['expected_lessons']} expected lessons, "
        f"{published} published lessons, {roadmap} roadmap lessons"
    )
    if diagnostics["empty_grades"]:
        print(
            "Curriculum source error: grades without topics: "
            + ", ".join(diagnostics["empty_grades"])
        )
    yield


app = FastAPI(
    title="Project Athena API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)
app.add_middleware(GZipMiddleware, minimum_size=1_000, compresslevel=5)
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(curriculum_router, prefix="/api/v1/curriculum", tags=["curriculum"])
app.include_router(lessons_router, prefix="/api/v1/lessons", tags=["lessons"])
app.include_router(practice_router, prefix="/api/v1/practice", tags=["practice"])


@app.middleware("http")
async def disable_development_asset_cache(request, call_next):
    """Prevent stale prototype assets from hiding curriculum changes locally."""
    response = await call_next(request)
    # HTML must always be revalidated: its versioned script URLs are the
    # handoff between the current curriculum API and the matching UI code.
    path = request.url.path
    if path == "/" or path.endswith(".html") or (settings.environment == "development" and path.endswith((".js", ".css"))):
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    """Lightweight health check, including a startup-time DB check."""
    return {"status": "ok", "environment": settings.environment}


# Keep the prototype usable from one local server while API routes are built.
# This mount is deliberately last so explicit routes such as /health and
# future /api/v1/* endpoints always take precedence.
FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
