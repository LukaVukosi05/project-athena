"""Topic 4 source, arithmetic, diagrams and preview gates."""
import json
import math
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from app.curriculum.grade11 import GRADE_11
from app.curriculum.grade11.assessment_euclidean import BANKS
from app.curriculum.validation import validate_curriculum
from app.practice.catalog import PRACTICE_BANKS

DATA = Path(__file__).resolve().parents[1] / "app/curriculum/grade11/generated"


def test_eight_lessons_and_independent_circle_calculations():
    assert validate_curriculum([GRADE_11]) == []
    topic = GRADE_11.topics[3]
    assert topic.id == "euclidean-geometry"
    assert topic.paper == "Paper 2"
    assert len(topic.subtopics[0].lessons) == 8
    for n, lesson in enumerate(topic.subtopics[0].lessons, 1):
        assert lesson.status.value == "teacher_review_required"
        assert len(lesson.whiteboard_questions) == len(PRACTICE_BANKS[lesson.id]) == 15
        assert tuple(map(len, BANKS[n][:3])) == (15, 5, 3)
        data = json.loads((DATA / f"euclidean_{n:02}.json").read_text())
        assert len({q["problem"] for q in data["worked"]}) == 15
        for item in data["worked"]:
            assert len(item["actions"]) == 5
            assert item["answer"] in item["check"]
            v = item["visual"]["values"]
            if n == 1:
                assert v["radius"] ** 2 == v["half"] ** 2 + v["distance"] ** 2
                assert item["answer"] == f'{2*v["half"]} cm'
            elif n == 5:
                assert v["external"] ** 2 == v["radius"] ** 2 + v["tangent"] ** 2
                assert item["answer"] == f'PA = PB = {v["tangent"]} cm'
            elif n in (2, 7):
                expected = v["central"] / 2 if n == 2 else 180 - v["central"] / 2
                assert item["answer"] == f'{expected:g}°'
            elif n == 3:
                assert item["answer"] == f'{v["inscribed"]}°'
            elif n == 4:
                assert item["answer"] == f'{180-v["given"]}°'
            elif n == 6:
                assert item["answer"] == f'{v["given"]}°'
            elif n == 8:
                assert item["answer"].startswith(f'{180-v["given"]}°;')
        for section in ("practice", "mastery", "reassessment"):
            for item in data[section]:
                assert len(set(item["options"])) == 4
                assert item["options"][item["answer_index"]] in item["memo"]


def test_public_previews_are_gated_and_reveals_have_all_five_steps(monkeypatch):
    monkeypatch.setattr("app.api.v1.lessons.enforce_lesson_access", lambda *args: None)
    with TestClient(app) as client:
        for n in range(1, 9):
            response = client.get(f"/api/v1/lessons/g11-euc-{n:02}")
            assert response.status_code == 200, response.text
            payload = response.json()
            assert payload["paper"] == "Paper 2"
            for question in payload["whiteboard_questions"]:
                assert question["solution_gated"] and question["total_step_count"] == 5
                assert len(question["whiteboard"]["steps"]) == 1
                assert "answer" not in question and "full_memo" not in question
                scene = json.loads(question["whiteboard"]["visualization"]["parameters"]["scene_json"])
                assert not any(key in scene for key in ("actions", "answer", "check"))
                assert "half" not in scene["visual"]["values"]
                assert "tangent" not in scene["visual"]["values"]
            qid = payload["whiteboard_questions"][0]["id"]
            reveal = client.post(f"/api/v1/lessons/g11-euc-{n:02}/questions/{qid}/reveal")
            assert reveal.status_code == 200
            assert len(reveal.json()["whiteboard"]["steps"]) == 5
