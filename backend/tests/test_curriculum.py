from fastapi.testclient import TestClient

from app.curriculum.grade12 import GRADE_12
from app.curriculum.repository import curriculum_repository
from app.main import app
from app.visualization.registry import validate_visualization


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


def test_active_catalogue_contains_controlled_grade_12_rollout():
    assert [grade.id for grade in curriculum_repository.list_grades()] == ["grade-8", "grade-9", "grade-10", "grade-11", "grade-12"]
    assert GRADE_12.grade == 12
    assert [topic.id for topic in GRADE_12.topics] == ["sequences-series", "functions-graphs", "finance-growth-decay", "differential-calculus", "algebra-equations-inequalities", "statistics-regression", "analytical-geometry"]
    assert [topic.product_order for topic in GRADE_12.topics] == [1, 2, 3, 4, 5, 8, 9]
    assert len({topic.id for topic in GRADE_12.topics}) == 7
    topic = GRADE_12.topics[0]
    lessons = topic.subtopics[0].lessons
    assert len(lessons) == 18
    assert [lesson.order for lesson in lessons] == list(range(1, 19))
    assert [lesson.title for lesson in lessons] == EXPECTED_TITLES
    assert len({lesson.id for lesson in lessons}) == 18


def test_every_scheduled_lesson_has_a_complete_whiteboard_bank():
    lessons = GRADE_12.topics[0].subtopics[0].lessons
    assert all(len(lesson.whiteboard_questions) == 12 for lesson in lessons)
    assert lessons[0].objective == "Classify arithmetic, geometric and quadratic patterns using evidence, not appearance."
    assert lessons[0].mastery_threshold == .8


def test_functions_graphs_schedule_has_three_complete_vertical_slices():
    topic = GRADE_12.topics[1]
    assert topic.id == "functions-graphs"
    assert topic.title == "Functions and Graphs"
    assert topic.product_order == 2
    assert topic.paper == "Paper 1"
    assert topic.term == 1
    assert topic.status.value == "teacher_review_required"
    assert len(topic.subtopics) == 1
    lessons = topic.subtopics[0].lessons
    assert len(lessons) == 18
    assert [lesson.order for lesson in lessons] == list(range(1, 19))
    assert [lesson.id for lesson in lessons] == [f"g12-functions-{number:02}" for number in range(1, 19)]
    assert all(lesson.status.value == "teacher_review_required" for lesson in lessons[:3])
    assert all(lesson.blocks and len(lesson.whiteboard_questions) == 3 for lesson in lessons[:3])
    assert all(lesson.mastery_threshold == .8 for lesson in lessons[:3])
    assert all(lesson.status.value == "coming_soon" for lesson in lessons[3:])
    assert all(not lesson.blocks for lesson in lessons[3:])


def test_catalogue_and_lesson_apis_return_controlled_rollout():
    with TestClient(app) as client:
        grades = client.get("/api/v1/curriculum/grades")
        grade = client.get("/api/v1/curriculum/grades/grade-12")
        topic = client.get("/api/v1/curriculum/grades/grade-12/topics/sequences-series")
        functions = client.get("/api/v1/curriculum/grades/grade-12/topics/functions-graphs")
        finance = client.get("/api/v1/curriculum/grades/grade-12/topics/finance-growth-decay")
        finance_lesson = client.get("/api/v1/lessons/g12-finance-01")
        calculus = client.get("/api/v1/curriculum/grades/grade-12/topics/differential-calculus")
        calculus_lesson = client.get("/api/v1/lessons/g12-calculus-01")
        calculus_alias = client.get("/api/v1/lessons/g12-calculus-average-rate")
        algebra = client.get("/api/v1/curriculum/grades/grade-12/topics/algebra-equations-inequalities")
        algebra_lesson = client.get("/api/v1/lessons/g12-algebra-01")
        function_lesson = client.get("/api/v1/lessons/g12-functions-01")
        coming_soon = client.get("/api/v1/lessons/g12-functions-04")
        lesson = client.get("/api/v1/lessons/g12-sequences-series-01")
        legacy = [client.get(path).status_code for path in (
            "/api/v1/lessons/g12-readiness-linear-equations",
            "/api/v1/lessons/g12-p2-trigonometry-exam",
            "/api/v1/curriculum/grades/grade-10",
        )]
    assert [item["id"] for item in grades.json()] == ["grade-8", "grade-9", "grade-10", "grade-11", "grade-12"]
    assert [item["id"] for item in grade.json()["topics"]] == ["sequences-series", "functions-graphs", "finance-growth-decay", "differential-calculus", "algebra-equations-inequalities", "statistics-regression", "analytical-geometry"]
    summaries = topic.json()["subtopics"][0]["lessons"]
    assert len(summaries) == 18
    assert lesson.status_code == 200 and lesson.json()["title"] == EXPECTED_TITLES[0]
    assert functions.status_code == 200
    assert len(functions.json()["subtopics"]) == 1
    assert len(functions.json()["subtopics"][0]["lessons"]) == 18
    assert function_lesson.status_code == 200
    assert function_lesson.json()["topic_title"] == "Functions and Graphs"
    assert function_lesson.json()["lesson_count"] == 18
    assert coming_soon.status_code == 409
    assert finance.status_code == 200 and len(finance.json()["subtopics"][0]["lessons"]) == 16
    assert finance_lesson.status_code == 200 and finance_lesson.json()["topic_title"] == "Finance, Growth and Decay"
    assert calculus.status_code == 200 and len(calculus.json()["subtopics"][0]["lessons"]) == 24
    assert calculus_lesson.status_code == 200 and calculus_lesson.json()["topic_title"] == "Differential Calculus"
    assert calculus_alias.status_code == 200 and calculus_alias.json()["id"] == "g12-calculus-01"
    assert algebra.status_code == 200 and len(algebra.json()["subtopics"][0]["lessons"]) == 18
    assert algebra_lesson.status_code == 200 and algebra_lesson.json()["topic_title"] == "Algebra, Equations and Inequalities"
    assert legacy == [404, 404, 200]


def test_frontend_has_no_competing_curriculum_catalogue():
    root = __import__("pathlib").Path(__file__).parents[2] / "frontend"
    assert not (root / "js/data/curriculum-data.js").exists()
    pages = "\n".join(path.read_text(encoding="utf-8") for path in root.glob("*.html"))
    assert "curriculum-data.js" not in pages
    topic_source = (root / "js/pages/topic.js").read_text(encoding="utf-8")
    assert "CurriculumAPI" not in topic_source
    assert "legacyTopic" not in topic_source
    assert "g12-calculus" not in topic_source


def test_complete_function_lessons_have_valid_exact_graphs():
    lessons = GRADE_12.topics[1].subtopics[0].lessons[:3]
    for lesson in lessons:
        for question in lesson.whiteboard_questions:
            validate_visualization(question.whiteboard)
            spec = question.whiteboard.graph_spec
            assert spec and spec["data"][0]["x"] and spec["data"][0]["y"]
            assert len(spec["data"][0]["x"]) == len(spec["data"][0]["y"])
            assert question.whiteboard.steps[-1].operation.type == "verify_result"


def test_sequences_topic_content_remains_first_and_complete():
    topic = GRADE_12.topics[0]
    assert topic.id == "sequences-series" and topic.product_order == 1
    assert [lesson.title for lesson in topic.subtopics[0].lessons] == EXPECTED_TITLES
    assert all(len(lesson.whiteboard_questions) == 12 for lesson in topic.subtopics[0].lessons)
