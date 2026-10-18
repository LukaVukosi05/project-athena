"""Lesson content endpoint with server-side entitlement enforcement."""

from fastapi import APIRouter, Depends, HTTPException

from app.core.security import get_optional_user
from app.curriculum.repository import curriculum_repository as repository
from app.db.models.user import User
from app.lessons.access import enforce_lesson_access

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
    payload = lesson.model_dump()
    # Private assessment banks live outside the Lesson model. Worked-example
    # answers and memos are also omitted from the initial learner payload.
    for question in payload.get("whiteboard_questions", []):
        question.pop("answer", None)
        question.pop("full_memo", None)
        question.pop("expected_evidence", None)
        if grade.id == "grade-8":
            question["solution_gated"] = True
            question["whiteboard"]["steps"] = question["whiteboard"]["steps"][:1]
            question["whiteboard"]["semantic_objects"] = [
                item for item in question["whiteboard"]["semantic_objects"]
                if item["id"] in {"problem", "stage-01"}
            ]
    payload["assessment_contract"] = {
        key: value for key, value in payload.get("assessment_contract", {}).items()
        if key in {"worked_example_count", "practice_count", "mastery_question_count", "parallel_reassessment_count", "answer_hidden_before_submission", "progression_threshold"}
    }
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
    return {"grade_id": grade.id, "topic_id": topic.id,
            "topic_title": topic.title, "paper": topic.paper,
            "paper_number": topic.paper_number, "subtopic_id": subtopic.id,
            "subtopic_title": subtopic.title,
            "lesson_count": len(subtopic.lessons), **payload}


@router.post("/{lesson_id}/questions/{question_id}/reveal")
def reveal_worked_example(lesson_id: str, question_id: str, user: User | None = Depends(get_optional_user)) -> dict:
    grade, _, _, lesson = _lesson_context(lesson_id)
    if grade.id != "grade-8" or lesson.id != "g8-algebraic-equations-01":
        raise HTTPException(status_code=404, detail="Worked example not found")
    enforce_lesson_access(lesson, user)
    question = next((item for item in lesson.whiteboard_questions if item.id == question_id), None)
    if question is None:
        raise HTTPException(status_code=404, detail="Worked example not found")
    # This explicit learner action is the solution gate. It returns only the
    # requested worked example and never exposes assessment answer keys.
    return question.model_dump()
