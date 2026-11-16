"""Account registration, login, and authenticated profile endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    get_current_user,
    hash_password,
    verify_password,
)
from app.db.database import get_db
from app.db.models.user import User
from app.schemas.auth import (
    LoginRequest,
    SignUpRequest,
    TokenResponse,
    UpdateMeRequest,
    UserResponse,
)

from app.auth.sessions import (
    start_browser_session,
    browser_user,
    end_browser_session,
    require_same_origin,
)

router = APIRouter()


def _normalise_email(email: str) -> str:
    return email.strip().lower()


def _token_response(user: User) -> TokenResponse:
    return TokenResponse(access_token=create_access_token(user.id), user=user)


@router.post(
    "/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED
)
def signup(
    payload: SignUpRequest,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
) -> TokenResponse:
    require_same_origin(request)
    email = _normalise_email(str(payload.email))
    if db.scalar(select(User.id).where(User.email == email)) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already registered."
        )

    user = User(
        first_name=payload.first_name.strip(),
        email=email,
        hashed_password=hash_password(payload.password),
        grade=payload.grade,
        curriculum_mode=payload.curriculum_mode,
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already registered."
        )
    db.refresh(user)
    start_browser_session(user, response, db, request=request)
    return _token_response(user)


@router.post("/login", response_model=TokenResponse)
def login(
    payload: LoginRequest,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
) -> TokenResponse:
    require_same_origin(request)
    user = db.scalar(
        select(User).where(User.email == _normalise_email(str(payload.email)))
    )
    if user is None or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    start_browser_session(user, response, db, payload.remember_me, request)
    return _token_response(user)


@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)) -> User:
    return current_user


@router.patch("/me", response_model=UserResponse)
def update_me(
    payload: UpdateMeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(current_user, field, value.strip() if field == "first_name" else value)
    db.commit()
    db.refresh(current_user)
    return current_user


@router.post("/refresh", response_model=TokenResponse)
def refresh(request: Request, response: Response, db: Session = Depends(get_db)):
    require_same_origin(request)
    response.headers["Cache-Control"] = "no-store"
    return _token_response(browser_user(request, db))


@router.post("/logout")
def logout(request: Request, response: Response, db: Session = Depends(get_db)):
    require_same_origin(request)
    end_browser_session(request, response, db)
    return {"signed_out": True}
