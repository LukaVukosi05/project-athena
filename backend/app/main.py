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

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Fail fast when the configured database cannot be reached."""
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    if settings.environment == "development":
        Base.metadata.create_all(bind=engine)
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
    if settings.environment == "development" and request.url.path.endswith((".html", ".js", ".css")):
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
