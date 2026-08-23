"""Sourced 2024 DBE NSC Paper 2 practice lessons.

The exact questions remain in their original supplied PDF pages. Solutions are
not authored until the corresponding DBE memorandum is available for checking.
"""

from app.curriculum.schemas import AccessLevel, ContentStatus, Lesson, LessonBlock


def paper_lesson(lesson_id: str, order: int, title: str, topic: str,
                 questions: str, pages: str, marks: int, focus: str) -> Lesson:
    first_page = pages.split("–")[0]
    return Lesson(id=lesson_id, order=order, title=title,
        objective=f"Attempt DBE NSC 2024 {topic} questions under examination conditions and identify skills requiring revision.",
        why_it_matters=f"These are exact questions from the supplied November 2024 Mathematics Paper 2 and contribute {marks} marks in that paper.",
        intuition="Past-paper practice is most useful after learning the underlying concepts: plan first, show every calculation or reason, then review errors by subtopic.",
        prerequisites=[focus], estimated_minutes=max(25, round(marks * 1.2)),
        difficulty="exam", access_level=AccessLevel.FREE,
        status=ContentStatus.TEACHER_REVIEW_REQUIRED, mastery_threshold=0.7,
        blocks=[
            LessonBlock(type="concept", title="Before you begin", content=f"This lesson covers Question {questions}, worth {marks} marks. Work on paper and show all calculations, diagrams and reasons. Use two-decimal-place rounding only where necessary."),
            LessonBlock(type="past_paper_question", title=f"Exact 2024 DBE questions {questions}",
                content="Read and answer the questions in the original paper below. The source page is preserved so diagrams, notation and mark allocations remain exact.",
                data={"source": "DBE NSC Mathematics Paper 2, November 2024, English",
                      "year": 2024, "question_numbers": questions, "pages": pages,
                      "marks": marks, "source_url": f"/api/v1/past-papers/2024/paper-2#page={first_page}",
                      "memorandum_status": "required", "exact_source": True}),
            LessonBlock(type="checkpoint", title="Self-check before submitting", content="Have you answered every sub-question, shown calculations, included units where relevant, and supplied geometry reasons where requested?"),
            LessonBlock(type="practice", title="Error diagnosis", content="After marking with the official memorandum, record each lost mark as a knowledge error, method error, calculator error, notation error, omitted reason or time-management error.",
                data={"questions": [{"difficulty": "Exam reflection", "question": "Which sub-question cost you the most marks, and which named subtopic must you revise?", "answer": "Learner reflection—verify against the official memorandum."}]}),
            LessonBlock(type="summary", title="Source and review status", content="Exact paper wording and diagrams are supplied from the local DBE paper. An official memorandum was not present in the Paper 2 folder, so solutions and step marks are intentionally withheld pending memorandum validation."),
        ])


STATISTICS_2024 = paper_lesson("g12-p2-2024-statistics", 1,
    "2024 Paper 2: Statistics Questions 1–2", "Statistics", "1–2", "3–4", 20,
    "Regression, correlation, ogives, quartiles and box plots")
ANALYTICAL_GEOMETRY_2024 = paper_lesson("g12-p2-2024-analytical-geometry", 1,
    "2024 Paper 2: Analytical Geometry Questions 3–4", "Analytical Geometry", "3–4", "5–6", 39,
    "Straight lines, distance, ratios, circles and tangents")
TRIGONOMETRY_2024 = paper_lesson("g12-p2-2024-trigonometry", 1,
    "2024 Paper 2: Trigonometry Questions 5–8", "Trigonometry", "5–8", "7–10", 50,
    "Compound angles, identities, equations, graphs and 3D applications")
EUCLIDEAN_GEOMETRY_2024 = paper_lesson("g12-p2-2024-euclidean-geometry", 1,
    "2024 Paper 2: Euclidean Geometry Questions 9–11", "Euclidean Geometry", "9–11", "11–13", 41,
    "Circle theorems, proportionality, similarity and proof riders")
