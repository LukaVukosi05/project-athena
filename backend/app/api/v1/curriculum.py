"""Lazy, read-only curriculum navigation endpoints."""

from fastapi import APIRouter, HTTPException

from app.curriculum.repository import curriculum_repository as repository

router = APIRouter()


def not_found(resource: str) -> HTTPException:
    return HTTPException(status_code=404, detail=f"{resource} not found")


@router.get("/grades")
def list_grades() -> list[dict]:
    return [{"id": grade.id, "grade": grade.grade, "subject": grade.subject,
             "status": grade.status, "topic_count": len(grade.topics)}
            for grade in repository.list_grades()]


@router.get("/grades/{grade_id}")
def get_grade(grade_id: str) -> dict:
    grade = repository.get_grade(grade_id)
    if grade is None:
        raise not_found("Grade")
    return {"id": grade.id, "grade": grade.grade, "subject": grade.subject,
            "status": grade.status,
            "topics": [{**topic.model_dump(exclude={"subtopics"}),
                        "subtopic_count": len(topic.subtopics)} for topic in grade.topics]}


@router.get("/grades/{grade_id}/topics/{topic_id}")
def get_topic(grade_id: str, topic_id: str) -> dict:
    topic = repository.get_topic(grade_id, topic_id)
    if topic is None:
        raise not_found("Topic")
    return {**topic.model_dump(exclude={"subtopics"}),
            "subtopics": [{**item.model_dump(exclude={"lessons"}),
                           "lessons": [lesson.model_dump(exclude={"blocks"})
                                       for lesson in item.lessons]}
                          for item in topic.subtopics]}


@router.get("/grades/{grade_id}/topics/{topic_id}/subtopics/{subtopic_id}")
def get_subtopic(grade_id: str, topic_id: str, subtopic_id: str) -> dict:
    subtopic = repository.get_subtopic(grade_id, topic_id, subtopic_id)
    if subtopic is None:
        raise not_found("Subtopic")
    return {**subtopic.model_dump(exclude={"lessons"}),
            "lessons": [lesson.model_dump(exclude={"blocks"}) for lesson in subtopic.lessons]}
