from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from app.curriculum.grade12.lessons.linear_equations import LINEAR_EQUATIONS
from app.curriculum.schemas import AccessLevel
from app.lessons.access import enforce_lesson_access


@pytest.fixture(autouse=True)
def production_entitlement_mode():
    from app.core.config import get_settings
    settings = get_settings()
    original = settings.unlock_all_lessons
    settings.unlock_all_lessons = False
    yield
    settings.unlock_all_lessons = original


def test_free_lesson_is_public():
    enforce_lesson_access(LINEAR_EQUATIONS, None)


def test_premium_lesson_requires_auth_and_entitlement():
    premium = LINEAR_EQUATIONS.model_copy(update={"access_level": AccessLevel.PREMIUM})
    with pytest.raises(HTTPException) as unauthenticated:
        enforce_lesson_access(premium, None)
    assert unauthenticated.value.status_code == 401
    with pytest.raises(HTTPException) as unsubscribed:
        enforce_lesson_access(premium, SimpleNamespace(is_premium=False))
    assert unsubscribed.value.status_code == 403
    enforce_lesson_access(premium, SimpleNamespace(is_premium=True))
