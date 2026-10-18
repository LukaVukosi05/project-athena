"""Lazy, read-only curriculum navigation endpoints."""

from fastapi import APIRouter, HTTPException

from app.curriculum.repository import curriculum_repository as repository
from app.curriculum.content_manifest import is_usable, manifest_for, readiness_for
from app.practice.catalog import PRACTICE_BANKS

router = APIRouter()


def not_found(resource: str) -> HTTPException:
    return HTTPException(status_code=404, detail=f"{resource} not found")


def authored_count(lesson, field: str) -> int:
    """Return runtime count when converted, otherwise the source-declared count."""
    if field == "worked_example_count" and lesson.whiteboard_questions:
        return len(lesson.whiteboard_questions)
    if field == "practice_count" and lesson.id in PRACTICE_BANKS:
        return len(PRACTICE_BANKS[lesson.id])
    return int(lesson.assessment_contract.get(field, 0))


@router.get("/grades")
def list_grades() -> list[dict]:
    rows = []
    for grade in repository.list_grades():
        lessons = [lesson for topic in grade.topics for item in topic.subtopics for lesson in item.lessons]
        rows.append({
            "id": grade.id,
            "grade": grade.grade,
            "title": f"Grade {grade.grade} Mathematics",
            "curriculum": "CAPS",
            "subject": grade.subject,
            "status": grade.status,
            "topic_count": len(grade.topics),
            "expected_lesson_count": len(lessons),
            "interactive_lesson_count": sum(is_usable(lesson) for lesson in lessons),
            "published_interactive_lesson_count": sum(
                readiness_for(lesson).value == "published" for lesson in lessons
            ),
            "availability": "available" if grade.topics else "source_blocked",
        })
    return rows


@router.get("/manifest")
def get_manifest() -> dict:
    return manifest_for(repository.list_grades())


@router.get("/grades/{grade_id}")
def get_grade(grade_id: str) -> dict:
    grade = repository.get_grade(grade_id)
    if grade is None:
        raise not_found("Grade")
    return {"id": grade.id, "grade": grade.grade, "subject": grade.subject,
            "title": f"Grade {grade.grade} Mathematics", "curriculum": "CAPS",
            "status": grade.status,
            "topics": [{**topic.model_dump(exclude={"subtopics"}),
                        "subtopic_count": len(topic.subtopics),
                        "lesson_count": sum(len(item.lessons) for item in topic.subtopics),
                        "interactive_lesson_count": sum(is_usable(lesson) for item in topic.subtopics for lesson in item.lessons),
                        "published_interactive_lesson_count": sum(readiness_for(lesson).value == "published" for item in topic.subtopics for lesson in item.lessons),
                        "verified_lesson_count": sum(readiness_for(lesson).value == "verified" for item in topic.subtopics for lesson in item.lessons),
                        "completed_lesson_count": sum(is_usable(lesson) for item in topic.subtopics for lesson in item.lessons),
                        "availability": "available" if any(is_usable(lesson) for item in topic.subtopics for lesson in item.lessons) else "roadmap"}
                       for topic in grade.topics]}


@router.get("/grades/{grade_id}/topics/{topic_id}")
def get_topic(grade_id: str, topic_id: str) -> dict:
    topic = repository.get_topic(grade_id, topic_id)
    if topic is None:
        raise not_found("Topic")
    return {**topic.model_dump(exclude={"subtopics"}),
            "subtopics": [{**item.model_dump(exclude={"lessons"}),
                           "lessons": [{**lesson.model_dump(exclude={"blocks", "whiteboard_questions", "assessment_contract"}),
                                        "readiness": readiness_for(lesson),
                                        "usable": is_usable(lesson),
                                        "worked_example_count": authored_count(lesson, "worked_example_count"),
                                        "practice_count": authored_count(lesson, "practice_count")}
                                       for lesson in item.lessons]}
                          for item in topic.subtopics]}


@router.get("/grades/{grade_id}/topics/{topic_id}/subtopics/{subtopic_id}")
def get_subtopic(grade_id: str, topic_id: str, subtopic_id: str) -> dict:
    subtopic = repository.get_subtopic(grade_id, topic_id, subtopic_id)
    if subtopic is None:
        raise not_found("Subtopic")
    return {**subtopic.model_dump(exclude={"lessons"}),
            "lessons": [lesson.model_dump(exclude={"blocks", "whiteboard_questions", "assessment_contract"}) for lesson in subtopic.lessons]}
