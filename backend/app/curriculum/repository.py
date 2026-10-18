"""Repository boundary for source-controlled curriculum data."""

import json
from pathlib import Path

from app.curriculum.grade12 import GRADE_12
from app.curriculum.grade8 import GRADE_8
from app.curriculum.grade_shells import SOURCE_BLOCKED_GRADES
from app.curriculum.schemas import GradeCurriculum, Lesson, Subtopic, Topic

LESSON_ID_ALIASES = {
    "g12-calculus-average-rate": "g12-calculus-01",
    "g12-calculus-secant-to-tangent": "g12-calculus-04",
}


class CurriculumRepository:
    def __init__(self, grades: tuple[GradeCurriculum, ...] = (GRADE_8, *SOURCE_BLOCKED_GRADES, GRADE_12)):
        self._grades = {grade.id: grade for grade in grades}
        generated_path = Path(__file__).with_name("generated") / "catalogue.json"
        if not generated_path.exists():
            raise RuntimeError(
                "Generated curriculum catalogue is missing. Run "
                "scripts/build_curriculum_catalogue.py before starting Athena."
            )
        self.generated_catalogue = json.loads(generated_path.read_text(encoding="utf-8"))
        generated_ids = [item["grade_id"] for item in self.generated_catalogue["grades"]]
        if generated_ids != list(self._grades):
            raise RuntimeError(
                f"Generated curriculum grades disagree with the runtime registry: {generated_ids}"
            )

    def list_grades(self) -> list[GradeCurriculum]:
        return list(self._grades.values())

    def get_grade(self, grade_id: str) -> GradeCurriculum | None:
        return self._grades.get(grade_id)

    def get_topic(self, grade_id: str, topic_id: str) -> Topic | None:
        grade = self.get_grade(grade_id)
        return next((item for item in grade.topics if item.id == topic_id), None) if grade else None

    def get_subtopic(self, grade_id: str, topic_id: str, subtopic_id: str) -> Subtopic | None:
        topic = self.get_topic(grade_id, topic_id)
        return next((item for item in topic.subtopics if item.id == subtopic_id), None) if topic else None

    def get_lesson(self, lesson_id: str) -> tuple[Topic, Subtopic, Lesson] | None:
        context = self.get_lesson_context(lesson_id)
        return context[1:] if context else None

    def get_lesson_context(self, lesson_id: str) -> tuple[GradeCurriculum, Topic, Subtopic, Lesson] | None:
        lesson_id = LESSON_ID_ALIASES.get(lesson_id, lesson_id)
        for grade in self._grades.values():
            for topic in grade.topics:
                for subtopic in topic.subtopics:
                    for lesson in subtopic.lessons:
                        if lesson.id == lesson_id:
                            return grade, topic, subtopic, lesson
        return None

    def diagnostics(self) -> dict[str, int | list[str]]:
        grades = self.list_grades()
        topics = [topic for grade in grades for topic in grade.topics]
        lessons = [lesson for topic in topics for subtopic in topic.subtopics for lesson in subtopic.lessons]
        return {
            "grades": len(grades),
            "topics": len(topics),
            "expected_lessons": len(lessons),
            "empty_grades": [grade.id for grade in grades if not grade.topics],
        }


curriculum_repository = CurriculumRepository()
