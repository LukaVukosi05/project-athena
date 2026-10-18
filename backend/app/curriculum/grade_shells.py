"""Honest grade selectors for curricula whose master packs are unavailable."""

from app.curriculum.schemas import ContentStatus, GradeCurriculum


SOURCE_BLOCKED_GRADES = tuple(
    GradeCurriculum(id=f"grade-{grade}", grade=grade, status=ContentStatus.COMING_SOON, topics=[])
    for grade in range(9, 12)
)
