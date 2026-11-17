"""Google/Apple OIDC, explicit onboarding and subject-based account identity."""

from secrets import compare_digest, token_urlsafe
import time
from typing import Literal
from urllib.parse import urlencode
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field, EmailStr, TypeAdapter, ValidationError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from authlib.integrations.base_client.errors import OAuthError
from joserfc.errors import JoseError
from httpx import HTTPError
from app.auth.providers import available_providers, oauth_client
from app.auth.sessions import safe_next, start_browser_session, require_same_origin
from app.core.config import get_settings
from app.core.security import hash_password, create_access_token
from app.db.database import get_db
from app.db.models.auth_session import ExternalIdentity
from app.db.models.user import User
from app.schemas.auth import GradeId, CurriculumMode, TokenResponse

router = APIRouter()
Provider = Literal["google", "apple"]


@router.get("/providers")
def providers():
    return available_providers()


@router.get("/oauth/{provider}/start")
async def start(
    provider: Provider,
    request: Request,
    next: str = "/index.html",
    remember: bool = False,
):
    if not available_providers()[provider]:
        raise HTTPException(
            503, "This sign-in option is not configured yet. Please use email."
        )
    request.session.clear()
    request.session["destination"] = safe_next(next)
    request.session["remember"] = remember
    callback = (
        get_settings().public_base_url.rstrip("/")
        + f"/api/v1/auth/oauth/{provider}/callback"
    )
    options = {"response_mode": "form_post"} if provider == "apple" else {}
    return await oauth_client(provider).authorize_redirect(request, callback, **options)


@router.api_route("/oauth/{provider}/callback", methods=["GET", "POST"])
async def callback(provider: Provider, request: Request, db: Session = Depends(get_db)):
    if not available_providers()[provider]:
        raise HTTPException(503, "This sign-in option is not configured yet.")
    destination = safe_next(request.session.get("destination"))
    remember = bool(request.session.get("remember"))
    try:
        # Authlib checks browser-bound state and verifies ID token signature,
        # issuer, audience, expiry and nonce using provider discovery/JWKS.
        token = await oauth_client(provider).authorize_access_token(request)
        profile = token.get("userinfo") or {}
        if (
            not token.get("id_token")
            or not profile.get("sub")
            or profile.get("email_verified") not in (True, "true")
        ):
            raise ValueError("Verified provider identity is required")
    except (OAuthError, JoseError, HTTPError, ValueError, KeyError):
        request.session.clear()
        return RedirectResponse("/login.html?oauth_error=verification", status_code=303)
    identity = db.scalar(
        select(ExternalIdentity).where(
            ExternalIdentity.provider == provider,
            ExternalIdentity.subject == profile["sub"],
        )
    )
    if identity:
        user = db.get(User, identity.user_id)
        if user is None:
            raise HTTPException(401, "This account is no longer available.")
        request.session.clear()
        response = RedirectResponse(
            "/login.html?" + urlencode({"oauth": "success", "next": destination}),
            status_code=303,
        )
        start_browser_session(user, response, db, remember, request)
        return response
    try:
        email = (
            str(TypeAdapter(EmailStr).validate_python(profile.get("email", "")))
            .strip()
            .lower()
        )
        if len(str(profile["sub"])) > 255:
            raise ValueError("Provider subject is too long")
    except (ValidationError, ValueError):
        request.session.clear()
        return RedirectResponse("/login.html?oauth_error=verification", status_code=303)
    if not email or db.scalar(select(User.id).where(User.email == email)) is not None:
        # A verified provider email must not take over an unverified local account.
        request.session.clear()
        return RedirectResponse(
            "/login.html?oauth_error=existing_account", status_code=303
        )
    request.session.clear()
    request.session["pending"] = {
        "provider": provider,
        "subject": str(profile["sub"]),
        "email": email,
        "first_name": str(profile.get("given_name") or "")[:100],
        "expires": int(time.time()) + 600,
        "csrf": token_urlsafe(32),
        "destination": destination,
        "remember": remember,
    }
    return RedirectResponse("/oauth-onboarding.html", status_code=303)


def pending_identity(request: Request):
    pending = request.session.get("pending")
    if not pending or pending.get("expires", 0) < time.time():
        raise HTTPException(401, "This sign-in expired. Please start again.")
    return pending


@router.get("/oauth/pending")
def pending(request: Request, response: Response):
    data = pending_identity(request)
    response.headers["Cache-Control"] = "no-store"
    return {key: data[key] for key in ("email", "first_name", "provider", "csrf")}


class CompleteProfile(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    grade: GradeId
    curriculum_mode: CurriculumMode = "CAPS"


@router.post("/oauth/complete", response_model=TokenResponse)
def complete(
    payload: CompleteProfile,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    require_same_origin(request)
    data = pending_identity(request)
    if not compare_digest(data["csrf"], request.headers.get("x-csrf-token", "")):
        raise HTTPException(403, "Please restart sign-in.")
    if not payload.first_name.strip():
        raise HTTPException(422, "Enter a first name.")
    user = User(
        first_name=payload.first_name.strip(),
        email=data["email"],
        hashed_password=hash_password(token_urlsafe(64)),
        grade=payload.grade,
        curriculum_mode=payload.curriculum_mode,
    )
    try:
        db.add(user)
        db.flush()
        db.add(
            ExternalIdentity(
                provider=data["provider"], subject=data["subject"], user_id=user.id
            )
        )
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "An account already exists. Return to sign in.")
    destination, remember = data["destination"], data["remember"]
    request.session.clear()
    start_browser_session(user, response, db, remember, request)
    # Destination is obtained before clearing the signed pending session.
    response.headers["X-Athena-Next"] = safe_next(destination)
    return TokenResponse(access_token=create_access_token(user.id), user=user)
