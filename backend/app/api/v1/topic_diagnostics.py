"""Grade 8 topic diagnostics and revision checks."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.curriculum.repository import curriculum_repository
from app.curriculum.grade8.functions_topic_diagnostic import (
    public_items as topic3_items,
    score as topic3_score,
)
from app.practice.assessment_catalog import ASSESSMENT_BANKS
from app.practice.assessment_scoring import _score_assessment

router = APIRouter()


@router.get("/topics/grade-8/functions-relationships/diagnostic")
def get_functions_topic_diagnostic():
    return {
        "topic_id": "functions-relationships",
        "questions": topic3_items(),
        "note": "This short check recommends where to revise; it does not replace lesson mastery.",
    }


class TopicDiagnosticSubmission(BaseModel):
    answers: dict[str, str] = Field(min_length=18, max_length=18)


@router.post("/topics/grade-8/functions-relationships/diagnostic")
def submit_functions_topic_diagnostic(payload: TopicDiagnosticSubmission):
    try:
        return topic3_score(payload.answers)
    except ValueError as error:
        raise HTTPException(422, str(error)) from error


class Grade8TopicCheckSubmission(BaseModel):
    answers: dict[str, str]


def _grade8_topic_check(topic_id: str):
    topic = curriculum_repository.get_topic("grade-8", topic_id)
    if topic is None:
        raise HTTPException(404, "Grade 8 topic not found")
    lessons = [lesson for subtopic in topic.subtopics for lesson in subtopic.lessons]
    if not lessons or any(lesson.id not in ASSESSMENT_BANKS for lesson in lessons):
        raise HTTPException(409, "A topic check is not available for every lesson")
    # These are existing, reviewed lesson items. This is a revision check, not a
    # fresh parallel reassessment or a replacement for each lesson's mastery.
    return [(lesson, list(ASSESSMENT_BANKS[lesson.id][0][:2])) for lesson in lessons]


@router.get("/topics/grade-8/{topic_id}/diagnostic")
def get_grade8_topic_check(topic_id: str):
    groups = _grade8_topic_check(topic_id)
    return {
        "topic_id": topic_id,
        "questions": [item.public() for _, bank in groups for item in bank],
        "note": "Revision check using existing lesson questions. Complete each lesson mastery assessment separately.",
    }


@router.post("/topics/grade-8/{topic_id}/diagnostic")
def submit_grade8_topic_check(topic_id: str, payload: Grade8TopicCheckSubmission):
    groups = _grade8_topic_check(topic_id)
    expected = {item.id for _, bank in groups for item in bank}
    if set(payload.answers) != expected:
        raise HTTPException(
            422, "Submit exactly one answer for every question in this topic check"
        )
    if any(
        not isinstance(value, str) or not 0 < len(value.strip()) <= 1000
        for value in payload.answers.values()
    ):
        raise HTTPException(422, "Every answer must contain 1 to 1000 characters")
    areas = []
    review = []
    for lesson, bank in groups:
        correct, rows, _ = _score_assessment(
            bank, {item.id: payload.answers[item.id] for item in bank}
        )
        areas.append(
            {
                "lesson_id": lesson.id,
                "title": lesson.title,
                "correct": correct,
                "total": len(bank),
                "needs_review": correct < len(bank),
            }
        )
        review.extend(
            {
                "id": row["id"],
                "lesson_id": lesson.id,
                "correct": row["correct"],
                "answer": row["answer"],
                "explanation": " ".join(row["solution"]),
            }
            for row in rows
        )
    return {
        "score": sum(area["correct"] for area in areas),
        "total": len(expected),
        "areas": areas,
        "recommended_lesson_id": next(
            (area["lesson_id"] for area in areas if area["needs_review"]), None
        ),
        "review": review,
        "note": "This check directs revision; it does not certify topic mastery. Complete each lesson mastery and any required repair and reassessment.",
    }
