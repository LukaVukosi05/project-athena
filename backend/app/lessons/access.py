"""Server-side lesson entitlement policy."""

from fastapi import HTTPException, status

from app.curriculum.schemas import AccessLevel, Lesson
from app.core.config import get_settings
from app.db.models.user import User


def enforce_lesson_access(lesson: Lesson, user: User | None) -> None:
    settings = get_settings()
    if settings.environment.casefold() == "development" and settings.unlock_all_lessons:
        return
    if lesson.access_level == AccessLevel.FREE:
        return
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Authentication is required for this lesson.")
    if not user.is_premium:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="An active subscription is required for this lesson.")
