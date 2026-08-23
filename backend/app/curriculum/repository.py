"""Repository boundary for source-controlled curriculum data."""

from app.curriculum.grade12 import GRADE_12
from app.curriculum.schemas import GradeCurriculum, Lesson, Subtopic, Topic


class CurriculumRepository:
    def __init__(self, grades: tuple[GradeCurriculum, ...] = (GRADE_12,)):
        self._grades = {grade.id: grade for grade in grades}

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
        for grade in self._grades.values():
            for topic in grade.topics:
                for subtopic in topic.subtopics:
                    for lesson in subtopic.lessons:
                        if lesson.id == lesson_id:
                            return topic, subtopic, lesson
        return None


curriculum_repository = CurriculumRepository()
