from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from app.curriculum.grade12.lessons.sequences_series import LESSON_ONE
from app.curriculum.schemas import AccessLevel
from app.lessons.access import enforce_lesson_access
from app.core.config import Settings, get_settings


@pytest.fixture(autouse=True)
def production_entitlement_mode():
    from app.core.config import get_settings
    settings = get_settings()
    original = settings.unlock_all_lessons
    settings.unlock_all_lessons = False
    yield
    settings.unlock_all_lessons = original


def test_free_lesson_is_public():
    enforce_lesson_access(LESSON_ONE, None)


def test_premium_lesson_requires_auth_and_entitlement():
    premium = LESSON_ONE.model_copy(update={"access_level": AccessLevel.PREMIUM})
    with pytest.raises(HTTPException) as unauthenticated:
        enforce_lesson_access(premium, None)
    assert unauthenticated.value.status_code == 401
    with pytest.raises(HTTPException) as unsubscribed:
        enforce_lesson_access(premium, SimpleNamespace(is_premium=False))
    assert unsubscribed.value.status_code == 403
    enforce_lesson_access(premium, SimpleNamespace(is_premium=True))


def test_development_override_opens_premium_without_changing_progress():
    settings = get_settings()
    original_environment, original_override = settings.environment, settings.unlock_all_lessons
    premium = LESSON_ONE.model_copy(update={"access_level": AccessLevel.PREMIUM})
    try:
        settings.environment = "development"
        settings.unlock_all_lessons = True
        enforce_lesson_access(premium, None)
        assert premium.access_level == AccessLevel.PREMIUM
        assert premium.mastery_threshold == .8
    finally:
        settings.environment, settings.unlock_all_lessons = original_environment, original_override


def test_override_is_ignored_outside_development():
    settings = get_settings()
    original_environment, original_override = settings.environment, settings.unlock_all_lessons
    premium = LESSON_ONE.model_copy(update={"access_level": AccessLevel.PREMIUM})
    try:
        settings.environment = "production"
        settings.unlock_all_lessons = True
        with pytest.raises(HTTPException) as blocked:
            enforce_lesson_access(premium, None)
        assert blocked.value.status_code == 401
    finally:
        settings.environment, settings.unlock_all_lessons = original_environment, original_override


def test_production_configuration_rejects_unlock_flag():
    with pytest.raises(ValueError, match="cannot be enabled in production"):
        Settings(environment="production", unlock_all_lessons=True,
                 jwt_secret="test-secret", database_url="sqlite://")
