from fastapi.testclient import TestClient

from app.curriculum.grade12 import GRADE_12
from app.curriculum.repository import curriculum_repository
from app.main import app


EXPECTED_TITLES = [
    "Recognising sequence structure", "Arithmetic sequences and the nth term",
    "Solving arithmetic sequence problems", "Arithmetic sequences in context",
    "Geometric sequences and the nth term", "Geometric parameters and applications",
    "Quadratic number patterns", "Sigma notation", "Deriving the arithmetic-series formula",
    "Arithmetic-series applications", "Deriving the finite geometric-series formula",
    "Finite geometric-series applications", "Infinite geometric series and convergence",
    "Infinite-series applications", "Mixed sequence and series decisions",
    "Algebraic and integrated exam problems", "Error clinic and proof of understanding",
    "Paper 1 mastery assessment",
]


def test_active_catalogue_is_only_grade_12_sequences_and_series():
    assert [grade.id for grade in curriculum_repository.list_grades()] == ["grade-12"]
    assert GRADE_12.grade == 12
    assert [topic.id for topic in GRADE_12.topics] == ["sequences-series"]
    topic = GRADE_12.topics[0]
    lessons = topic.subtopics[0].lessons
    assert len(lessons) == 18
    assert [lesson.order for lesson in lessons] == list(range(1, 19))
    assert [lesson.title for lesson in lessons] == EXPECTED_TITLES
    assert len({lesson.id for lesson in lessons}) == 18


def test_only_lesson_one_has_an_initial_whiteboard_bank():
    lessons = GRADE_12.topics[0].subtopics[0].lessons
    assert len(lessons[0].whiteboard_questions) == 12
    assert all(not lesson.whiteboard_questions for lesson in lessons[1:])
    assert lessons[0].objective == "Classify arithmetic, geometric and quadratic patterns using evidence, not appearance."
    assert lessons[0].mastery_threshold == .8


def test_catalogue_and_lesson_apis_return_only_approved_content():
    with TestClient(app) as client:
        grades = client.get("/api/v1/curriculum/grades")
        grade = client.get("/api/v1/curriculum/grades/grade-12")
        topic = client.get("/api/v1/curriculum/grades/grade-12/topics/sequences-series")
        lesson = client.get("/api/v1/lessons/g12-sequences-series-01")
        legacy = [client.get(path).status_code for path in (
            "/api/v1/lessons/g12-readiness-linear-equations",
            "/api/v1/lessons/g12-calculus-average-rate",
            "/api/v1/lessons/g12-p2-trigonometry-exam",
            "/api/v1/curriculum/grades/grade-10",
        )]
    assert grades.json() == [{"id":"grade-12","grade":12,"subject":"Mathematics","status":"draft","topic_count":1}]
    assert [item["id"] for item in grade.json()["topics"]] == ["sequences-series"]
    summaries = topic.json()["subtopics"][0]["lessons"]
    assert len(summaries) == 18
    assert lesson.status_code == 200 and lesson.json()["title"] == EXPECTED_TITLES[0]
    assert legacy == [404, 404, 404, 404]


def test_frontend_has_no_competing_curriculum_catalogue():
    root = __import__("pathlib").Path(__file__).parents[2] / "frontend"
    assert not (root / "js/data/curriculum-data.js").exists()
    pages = "\n".join(path.read_text(encoding="utf-8") for path in root.glob("*.html"))
    assert "curriculum-data.js" not in pages
    topic_source = (root / "js/pages/topic.js").read_text(encoding="utf-8")
    assert "CurriculumAPI" not in topic_source
    assert "legacyTopic" not in topic_source
    assert "g12-calculus" not in topic_source
