"""Read-only practice navigation; question data stays in existing endpoints."""

from fastapi import APIRouter, HTTPException
from app.curriculum.repository import curriculum_repository
from app.practice.catalog import PRACTICE_BANKS

router = APIRouter()


@router.get("/catalogue/grades/{grade_id}")
def practice_catalogue(grade_id: str) -> dict:
    grade = curriculum_repository.get_grade(grade_id)
    if grade is None:
        raise HTTPException(404, "Grade not found")
    topics = []
    for topic in grade.topics:
        lessons = []
        for subtopic in topic.subtopics:
            for lesson in subtopic.lessons:
                bank = PRACTICE_BANKS.get(lesson.id, [])
                lessons.append({
                    "id": lesson.id, "title": lesson.title, "order": lesson.order,
                    "question_count": len(bank),
                    "choice_count": sum(bool(q.options) for q in bank),
                })
        topics.append({"id": topic.id, "title": topic.title,
                       "order": topic.product_order, "paper": topic.paper,
                       "lessons": lessons})
    return {"id": grade.id, "grade": grade.grade, "topics": topics}
