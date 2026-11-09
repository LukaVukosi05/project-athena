"""Topic 3 trigonometric arithmetic and public lesson gates."""
import json
import math
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from app.curriculum.grade11 import GRADE_11
from app.curriculum.grade11.assessment_trigonometry import BANKS
from app.curriculum.validation import validate_curriculum
from app.practice.catalog import PRACTICE_BANKS

DATA=Path(__file__).resolve().parents[1]/"app/curriculum/grade11/generated"

def exact(text):
    """Evaluate only this bank's small exact-value grammar."""
    text=text.replace("√3",str(math.sqrt(3))).replace("√2",str(math.sqrt(2)))
    assert set(text)<set("0123456789.-/")
    numerator,*rest=text.split("/")
    return float(numerator)/float(rest[0]) if rest else float(numerator)

def test_seven_lessons_have_full_banks_and_consistent_exact_angles():
    assert validate_curriculum([GRADE_11])==[]
    topic=GRADE_11.topics[2]
    assert topic.id=="trigonometry-reduction-and-equations"
    assert topic.paper=="Paper 2"
    assert len(topic.subtopics[0].lessons)==7
    count=0
    for n,lesson in enumerate(topic.subtopics[0].lessons,1):
        assert lesson.status.value=="teacher_review_required"
        assert len(lesson.whiteboard_questions)==len(PRACTICE_BANKS[lesson.id])==15
        assert tuple(map(len,BANKS[n][:3]))==(15,5,3)
        assert len({q.whiteboard.problem for q in lesson.whiteboard_questions})==15
        data=json.loads((DATA/f"trigonometry_{n:02}.json").read_text())
        for item in data["worked"]:
            assert len(item["actions"])==5
            assert item["answer"] in item["check"]
        for section in ("practice","mastery","reassessment"):
            for item in data[section]:
                assert len(set(item["options"]))==4
                assert item["options"][item["answer_index"]] in item["memo"]
        count+=len(data["worked"])+len(data["practice"])+len(data["mastery"])+len(data["reassessment"])
    assert count==266

def test_reductions_and_interval_solutions_match_independent_trigonometry():
    for n in range(1,8):
        data=json.loads((DATA/f"trigonometry_{n:02}.json").read_text())
        for scene in data["worked"]:
            v=scene["visual"]["values"]
            if v["mode"]=="reduction":
                fn=getattr(math,v["function"])
                actual=fn(math.radians(v["theta"]))
                assert math.isclose(actual,exact(scene["answer"]),abs_tol=1e-9),scene["id"]
            if v["mode"]=="interval":
                fn=getattr(math,v["function"])
                selected=[int(a[:-1]) for a in scene["answer"].split(", ")]
                expected=[a for a in range(v["upper"]) if math.isclose(
                    fn(math.radians(a)),exact(v["target"]),abs_tol=1e-9)]
                assert selected==expected,scene["id"]

def test_all_public_previews_hide_answers_and_reveal_full_steps(monkeypatch):
    monkeypatch.setattr("app.api.v1.lessons.enforce_lesson_access",lambda *a:None)
    with TestClient(app) as client:
        catalogue=client.get("/api/v1/curriculum/grades/grade-11")
        assert catalogue.status_code==200
        assert catalogue.json()["topics"][2]["id"]=="trigonometry-reduction-and-equations"
        for n in range(1,8):
            response=client.get(f"/api/v1/lessons/g11-tr-{n:02}")
            assert response.status_code==200
            payload=response.json()
            assert payload["paper"]=="Paper 2"
            for q in payload["whiteboard_questions"]:
                assert q["solution_gated"] and q["total_step_count"]==5
                assert len(q["whiteboard"]["steps"])==1
                assert "answer" not in q and "full_memo" not in q
                scene=json.loads(q["whiteboard"]["visualization"]["parameters"]["scene_json"])
                assert "actions" not in scene and "answer" not in scene and "check" not in scene
                assert "excluded" not in scene["visual"]["values"]
            first=payload["whiteboard_questions"][0]["id"]
            reveal=client.post(f"/api/v1/lessons/g11-tr-{n:02}/questions/{first}/reveal")
            assert reveal.status_code==200
            assert len(reveal.json()["whiteboard"]["steps"])==5
