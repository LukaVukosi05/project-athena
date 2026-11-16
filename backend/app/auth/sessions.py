"""HttpOnly browser renewal with a server-side, hashed and revocable secret."""

from datetime import datetime, timedelta, timezone
from hashlib import sha256
from secrets import token_urlsafe
from urllib.parse import urlsplit
from fastapi import HTTPException, Request, Response
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.db.models.auth_session import AuthSession
from app.db.models.user import User

COOKIE = "athena_session"


def require_same_origin(request: Request) -> None:
    origin = request.headers.get("origin")
    expected = get_settings().public_base_url.rstrip("/")
    if origin and origin.rstrip("/") != expected:
        raise HTTPException(403, "This account action must start from Athena.")
    if request.headers.get("sec-fetch-site") == "cross-site":
        raise HTTPException(403, "This account action must start from Athena.")


def safe_next(value: str | None) -> str:
    if (
        not value
        or not value.startswith("/")
        or value.startswith("//")
        or "\\" in value
        or any(ord(c) < 32 for c in value)
    ):
        return "/dashboard.html"
    parsed = urlsplit(value)
    return value if not parsed.scheme and not parsed.netloc else "/dashboard.html"


def token_hash(value: str) -> str:
    return sha256(value.encode()).hexdigest()


def start_browser_session(
    user: User,
    response: Response,
    db: Session,
    remember: bool = False,
    request: Request | None = None,
) -> None:
    settings = get_settings()
    if request:
        old = request.cookies.get(COOKIE)
        row = db.get(AuthSession, token_hash(old)) if old else None
        if row:
            db.delete(row)
    secret = token_urlsafe(48)
    lifetime = (
        timedelta(days=settings.remember_days)
        if remember
        else timedelta(hours=settings.browser_session_hours)
    )
    db.add(
        AuthSession(
            token_hash=token_hash(secret),
            user_id=user.id,
            expires_at=datetime.now(timezone.utc) + lifetime,
        )
    )
    db.commit()
    response.set_cookie(
        COOKIE,
        secret,
        httponly=True,
        secure=settings.cookie_secure,
        samesite="lax",
        path="/api/v1/auth",
        max_age=int(lifetime.total_seconds()) if remember else None,
    )
    response.headers["Cache-Control"] = "no-store"


def browser_user(request: Request, db: Session) -> User:
    secret = request.cookies.get(COOKIE)
    row = db.get(AuthSession, token_hash(secret)) if secret else None
    if row is None or row.expires_at.replace(tzinfo=timezone.utc) <= datetime.now(
        timezone.utc
    ):
        raise HTTPException(401, "Please sign in to continue.")
    user = db.get(User, row.user_id)
    if user is None:
        raise HTTPException(401, "Please sign in to continue.")
    return user


def end_browser_session(request: Request, response: Response, db: Session) -> None:
    secret = request.cookies.get(COOKIE)
    row = db.get(AuthSession, token_hash(secret)) if secret else None
    if row:
        db.delete(row)
        db.commit()
    response.delete_cookie(
        COOKIE,
        path="/api/v1/auth",
        secure=get_settings().cookie_secure,
        httponly=True,
        samesite="lax",
    )
    response.headers["Cache-Control"] = "no-store"
