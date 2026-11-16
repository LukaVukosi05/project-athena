"""Lesson content endpoint with server-side entitlement enforcement."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.core.security import get_optional_user
from app.curriculum.repository import curriculum_repository as repository
from app.db.models.user import User
from app.lessons.access import enforce_lesson_access
from app.lessons.payload import lesson_payload

router = APIRouter()


def _lesson_context(lesson_id: str):
    result = repository.get_lesson_context(lesson_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return result


@router.get("/{lesson_id}")
def get_lesson(lesson_id: str, user: User | None = Depends(get_optional_user)) -> dict:
    result = _lesson_context(lesson_id)
    grade, topic, subtopic, lesson = result
    if lesson.status.value == "coming_soon":
        raise HTTPException(status_code=409, detail="This lesson is coming soon")
    enforce_lesson_access(lesson, user)
    return lesson_payload(grade, topic, subtopic, lesson)


@router.post("/{lesson_id}/questions/{question_id}/reveal")
def reveal_worked_example(
    lesson_id: str, question_id: str, user: User | None = Depends(get_optional_user)
) -> dict:
    grade, _, _, lesson = _lesson_context(lesson_id)
    if grade.id not in {"grade-8", "grade-9", "grade-10", "grade-11"}:
        raise HTTPException(status_code=404, detail="Worked example not found")
    enforce_lesson_access(lesson, user)
    if lesson.id in {"g8-algebraic-equations-10", "g8-algebraic-expressions-10"}:
        raise HTTPException(
            status_code=409,
            detail="Submit your first-error diagnosis before viewing the worked repair",
        )
    question = next(
        (item for item in lesson.whiteboard_questions if item.id == question_id), None
    )
    if question is None:
        raise HTTPException(status_code=404, detail="Worked example not found")
    # This explicit learner action is the solution gate. It returns only the
    # requested worked example and never exposes assessment answer keys.
    return question.model_dump()


class DiagnosticAttempt(BaseModel):
    first_error_and_repair: str = Field(min_length=3, max_length=500)


@router.post("/{lesson_id}/questions/{question_id}/diagnose")
def diagnose_worked_example(
    lesson_id: str,
    question_id: str,
    attempt: DiagnosticAttempt,
    user: User | None = Depends(get_optional_user),
) -> dict:
    grade, _, _, lesson = _lesson_context(lesson_id)
    if grade.id != "grade-8" or lesson.id not in {
        "g8-algebraic-equations-10",
        "g8-algebraic-expressions-10",
    }:
        raise HTTPException(status_code=404, detail="Diagnostic case not found")
    enforce_lesson_access(lesson, user)
    if not attempt.first_error_and_repair.strip():
        raise HTTPException(
            status_code=422, detail="Describe the first error and your repair"
        )
    question = next(
        (item for item in lesson.whiteboard_questions if item.id == question_id), None
    )
    if question is None:
        raise HTTPException(status_code=404, detail="Diagnostic case not found")
    # Submission precedes the authored explanation; this is an attempt gate,
    # not automated grading of mathematical prose.
    return question.model_dump()
