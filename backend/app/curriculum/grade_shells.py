"""Honest grade selectors for curricula whose master packs are unavailable."""

from app.curriculum.schemas import ContentStatus, GradeCurriculum


SOURCE_BLOCKED_GRADES: tuple[GradeCurriculum, ...] = ()
