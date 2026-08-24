"""Lesson content endpoint with server-side entitlement enforcement."""

from fastapi import APIRouter, Depends, HTTPException

from app.core.security import get_optional_user
from app.curriculum.repository import curriculum_repository as repository
from app.db.models.user import User
from app.lessons.access import enforce_lesson_access

router = APIRouter()


@router.get("/{lesson_id}")
def get_lesson(lesson_id: str, user: User | None = Depends(get_optional_user)) -> dict:
    result = repository.get_lesson(lesson_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    topic, subtopic, lesson = result
    enforce_lesson_access(lesson, user)
    payload = lesson.model_dump()
    if lesson.id == "g12-sequences-series-01":
        # The practice API is authoritative. Legacy embedded questions and
        # answer keys must never be delivered with the lesson document.
        payload["blocks"] = [
            ({**block, "title": "Self-guided practice",
              "content": "Solve, submit, then compare your method.",
              "data": {"practice_bank_id": lesson.id}}
             if block.get("type") == "practice" else block)
            for block in payload["blocks"] if block.get("type") != "checkpoint"
        ]
    return {"grade_id": "grade-12", "topic_id": topic.id,
            "subtopic_id": subtopic.id, **payload}
