"""Password hashing, JWT issuing, and current-user dependencies."""

from datetime import datetime, timedelta, timezone
import base64
import hashlib
import hmac
import os

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.database import get_db
from app.db.models.user import User

bearer_scheme = HTTPBearer(auto_error=False)
SCRYPT_N = 2**14
SCRYPT_R = 8
SCRYPT_P = 1
SCRYPT_DKLEN = 64


def hash_password(plain_password: str) -> str:
    """Create a salted scrypt hash without retaining the plaintext password."""
    salt = os.urandom(16)
    digest = hashlib.scrypt(
        plain_password.encode("utf-8"),
        salt=salt,
        n=SCRYPT_N,
        r=SCRYPT_R,
        p=SCRYPT_P,
        dklen=SCRYPT_DKLEN,
    )
    encode = lambda value: base64.urlsafe_b64encode(value).decode("ascii")
    return "$".join(["scrypt", str(SCRYPT_N), str(SCRYPT_R), str(SCRYPT_P), encode(salt), encode(digest)])


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        algorithm, n, r, p, salt, expected = hashed_password.split("$")
        if algorithm != "scrypt":
            return False
        decode = lambda value: base64.urlsafe_b64decode(value.encode("ascii"))
        actual = hashlib.scrypt(
            plain_password.encode("utf-8"),
            salt=decode(salt),
            n=int(n),
            r=int(r),
            p=int(p),
            dklen=len(decode(expected)),
        )
        return hmac.compare_digest(actual, decode(expected))
    except (ValueError, TypeError, UnicodeError):
        return False


def create_access_token(user_id: int) -> str:
    settings = get_settings()
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    return jwt.encode(
        {"sub": str(user_id), "exp": expires_at},
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication is required.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if credentials is None:
        raise unauthorized

    settings = get_settings()
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
        user_id = int(payload["sub"])
    except (JWTError, KeyError, TypeError, ValueError):
        raise unauthorized

    user = db.get(User, user_id)
    if user is None:
        raise unauthorized
    return user


def get_optional_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User | None:
    """Resolve a bearer token when supplied, while allowing public resources."""
    if credentials is None:
        return None
    return get_current_user(credentials=credentials, db=db)
