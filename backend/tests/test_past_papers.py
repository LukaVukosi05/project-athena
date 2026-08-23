from fastapi.testclient import TestClient

from app.curriculum.repository import curriculum_repository
from app.main import app
from app.past_papers.catalog import PAPERS, QUESTION_GROUPS_2024
from app.whiteboard.validation import validate_whiteboard


def test_supplied_paper_2_catalogue_files_exist():
    assert sorted(PAPERS) == [2016, 2017, 2019, 2020, 2021, 2022, 2023, 2024]
    assert all(paper.path.is_file() for paper in PAPERS.values())


def test_2024_question_map_covers_all_150_marks():
    assert sum(group["marks"] for group in QUESTION_GROUPS_2024.values()) == 150
    assert set(QUESTION_GROUPS_2024) == {
        "statistics", "analytical-geometry", "trigonometry", "euclidean-geometry"
    }


def test_each_paper_2_module_uses_native_exam_course_not_embedded_paper():
    for topic_id in QUESTION_GROUPS_2024:
        topic = curriculum_repository.get_topic("grade-12", topic_id)
        lessons = [lesson for subtopic in topic.subtopics for lesson in subtopic.lessons]
        exam = next(lesson for lesson in lessons if lesson.difficulty == "exam")
        assert all(block.type != "past_paper_question" for block in exam.blocks)
        quiz = next(
            block for block in exam.blocks
            if block.type != "whiteboard"
            and block.data.get("assessment_mode") == "scored_multiple_choice"
        )
        assert len(quiz.data["questions"]) == 10


def test_each_paper_2_module_has_progressive_practice_mastery_and_exam_lessons():
    for topic_id in QUESTION_GROUPS_2024:
        topic = curriculum_repository.get_topic("grade-12", topic_id)
        lessons = [lesson for subtopic in topic.subtopics for lesson in subtopic.lessons]
        assert len(lessons) == 4
        assert {lesson.difficulty for lesson in lessons} == {
            "foundation", "standard", "challenge", "exam"
        }
        assert all(lesson.access_level == "free" for lesson in lessons)
        assert all(len(lesson.whiteboard_questions) == 12 for lesson in lessons)
        assert all(
            lesson.whiteboard_questions[0].whiteboard.problem
            != lesson.whiteboard_questions[1].whiteboard.problem
            for lesson in lessons
        )
        for lesson in [item for item in lessons if item.difficulty in {"foundation", "standard"}]:
            practice = next(block for block in lesson.blocks if block.type != "whiteboard" and block.data.get("assessment_mode") == "paper_multiple_choice")
            quiz = next(block for block in lesson.blocks if block.type != "whiteboard" and block.data.get("assessment_mode") == "scored_multiple_choice")
            assert len(practice.data["questions"]) == 6
            assert len(quiz.data["questions"]) == 3
            assert all(
                question["options"]
                and question["explanation"]
                and len(question["solution_steps"]) >= 5
                for question in practice.data["questions"]
            )

        mastery = next(item for item in lessons if item.difficulty == "challenge")
        quiz = next(
            block for block in mastery.blocks
            if block.type != "whiteboard" and block.data.get("assessment_mode") == "scored_multiple_choice"
        )
        assert len(quiz.data["questions"]) == 8
        assert quiz.data["pass_mark"] == 0.75

        for lesson in lessons:
            boards = [block for block in lesson.blocks if block.type == "whiteboard"]
            assert len(boards) == 1
            whiteboard = boards[0]
            expected_steps = 3 if lesson.id == "g12-p2-trigonometry-exam" else 4
            assert len(whiteboard.steps) == expected_steps
            assert all(step.working_expression for step in whiteboard.steps)
            validate_whiteboard(whiteboard)


def test_whiteboard_frontend_renders_working_then_result_with_persistent_history():
    source = (PAPERS[2024].path.parents[1] / "frontend" / "js" / "whiteboard" / "animation-registry.js").read_text(encoding="utf-8")
    state = (PAPERS[2024].path.parents[1] / "frontend" / "js" / "whiteboard" / "stateful-whiteboard.js").read_text(encoding="utf-8")
    assert "working_expression" in source
    assert "renderMathHistory" in source
    assert "math-fraction" in source
    assert "previous.working_expression" in state
    assert "renderGraphSpec" in source


def test_past_paper_api_lists_and_serves_allowlisted_pdfs():
    with TestClient(app) as client:
        listing = client.get("/api/v1/past-papers")
        paper = client.get("/api/v1/past-papers/2024/paper-2")
        missing = client.get("/api/v1/past-papers/2018/paper-2")
    assert listing.status_code == 200
    assert len(listing.json()) == 8
    assert paper.status_code == 200
    assert paper.headers["content-type"] == "application/pdf"
    assert missing.status_code == 404


def test_development_frontend_assets_are_not_cached():
    with TestClient(app) as client:
        dashboard = client.get("/dashboard.html")
        script = client.get("/js/pages/dashboard.js")
    assert "no-store" in dashboard.headers["cache-control"]
    assert "no-store" in script.headers["cache-control"]
    assert "Paper 2 lessons" in script.text
