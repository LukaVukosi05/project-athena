"""Topic 2 authored preview, arithmetic, and assessment gates."""
import json
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app
from app.curriculum.grade11 import GRADE_11
from app.curriculum.grade11.assessment_equations import BANKS
from app.curriculum.validation import validate_curriculum
from app.practice.catalog import PRACTICE_BANKS
from app.visualization.registry import validate_visualization

DATA = Path(__file__).resolve().parents[1]/"app/curriculum/grade11/generated"

def test_topic2_has_complete_banks_valid_steps_and_private_answers():
    assert validate_curriculum([GRADE_11]) == []
    topic=GRADE_11.topics[1]
    assert topic.id=="equations-and-inequalities"
    lessons=topic.subtopics[0].lessons
    assert len(lessons)==7
    for n,lesson in enumerate(lessons,1):
        worked=lesson.whiteboard_questions
        assert len(worked)==15
        assert len(PRACTICE_BANKS[lesson.id])==15
        assert tuple(map(len,BANKS[n][:3]))==(15,5,3)
        assert len({q.whiteboard.problem for q in worked})==15
        assert all(len(q.whiteboard.steps)==5 for q in worked)
        assert all(q.whiteboard.steps[-1].operation.action=="verify_solution" for q in worked)
        for q in worked:
            validate_visualization(q.whiteboard)
        for section in ("practice","mastery","reassessment"):
            data=json.loads((DATA/f"equations_inequalities_{n:02}.json").read_text())
            for item in data[section]:
                assert len(set(item["options"]))==4
                assert 0<=item["answer_index"]<4
                assert item["options"][item["answer_index"]] in item["memo"]

def test_topic2_public_preview_does_not_expose_solution(monkeypatch):
    monkeypatch.setattr("app.api.v1.lessons.enforce_lesson_access",lambda *a:None)
    with TestClient(app) as client:
        catalogue=client.get("/api/v1/curriculum/grades/grade-11")
        assert catalogue.status_code==200
        assert catalogue.json()["topics"][1]["id"]=="equations-and-inequalities"
        for n in range(1,8):
            response=client.get(f"/api/v1/lessons/g11-ei-{n:02}")
            assert response.status_code==200
            for q in response.json()["whiteboard_questions"]:
                assert q["solution_gated"] and q["total_step_count"]==5
                assert len(q["whiteboard"]["steps"])==1
                assert "answer" not in q and "full_memo" not in q
                scene=json.loads(q["whiteboard"]["visualization"]["parameters"]["scene_json"])
                assert "actions" not in scene and "answer" not in scene and "check" not in scene
                assert "r" not in scene["visual"]["values"] and "s" not in scene["visual"]["values"]
            first=response.json()["whiteboard_questions"][0]["id"]
            reveal=client.post(f"/api/v1/lessons/g11-ei-{n:02}/questions/{first}/reveal")
            assert reveal.status_code==200
            assert len(reveal.json()["whiteboard"]["steps"])==5
