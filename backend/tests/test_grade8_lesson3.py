"""Check additive-inverse source fidelity, staging, access, and repair routes."""
import hashlib
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from app.curriculum.repository import curriculum_repository
from app.curriculum.content_manifest import readiness_for
from app.curriculum.validation import validate_curriculum
from app.curriculum.grade8.lesson3_runtime import LESSON_3, SOURCE_DATA
from app.curriculum.grade8.assessment_lesson3 import PRACTICE_BANK, MASTERY_BANK, REASSESSMENT_BANK

SOURCE = Path(__file__).resolve().parents[2] / "docs/curriculum/grade8/algebraic-equations/Project_Athena_Grade8_Algebraic_Equations_Gold_Pack_v1_0.docx"


def test_source_registration_and_all_real_banks():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_DATA["source_sha256"]
    assert [q.id for q in LESSON_3.whiteboard_questions] == [f"g8-ae-l03-w{n:02}" for n in range(1,16)]
    assert [q.id for q in PRACTICE_BANK] == [f"g8-ae-l03-p{n:02}" for n in range(1,16)]
    assert len(MASTERY_BANK)==5 and len(REASSESSMENT_BANK)==3
    assert readiness_for(LESSON_3).value=="published"
    assert not [x for x in validate_curriculum([curriculum_repository.get_grade("grade-8")]) if x.lesson_id == LESSON_3.id]


def test_every_step_has_operation_before_result_and_true_original_check():
    for question in LESSON_3.whiteboard_questions:
        board=question.whiteboard
        assert board.visualization.template in {"additive_balance","additive_number_line","additive_context"}
        assert len(board.steps)>=4
        assert board.problem not in {question.answer,board.steps[-1].after_expression}
        for index,step in enumerate(board.steps):
            assert step.before_expression != step.after_expression
            assert step.events
            assert [e.text for e in step.events if e.type=="caption"] == [e.text for e in step.events if e.type=="narration"]
            operation=min(e.at_ms for e in step.events if e.type=="show_operation")
            result=min(e.at_ms for e in step.events if e.type=="reveal")
            assert operation < result
            if index: assert step.before_expression == board.steps[index-1].after_expression
        assert "Checked:" in board.steps[-1].after_expression
        assert board.steps[-1].state_after["verification_complete"]


def test_public_answer_gate_and_practice():
    with TestClient(app) as client:
        topic=client.get("/api/v1/curriculum/grades/grade-8/topics/algebraic-equations").json()
        row=next(row for subtopic in topic["subtopics"] for row in subtopic["lessons"] if row["id"]==LESSON_3.id)
        assert row["status"]=="published" and row["usable"]
        preview=client.get(f"/api/v1/lessons/{LESSON_3.id}")
        if preview.status_code==200:
            question=preview.json()["whiteboard_questions"][0]
            assert "answer" not in question and "full_memo" not in question
            assert question["whiteboard"]["steps"][0]["events"]==[]
            assert question["whiteboard"]["steps"][0]["before_expression"]==question["whiteboard"]["steps"][0]["after_expression"]
            assert "solution = " not in question["whiteboard"]["visualization"]["parameters"]["source_data"]
            revealed=client.post(f"/api/v1/lessons/{LESSON_3.id}/questions/g8-ae-l03-w10/reveal")
            assert revealed.status_code==200 and revealed.json()["whiteboard"]["steps"][-1]["state_after"]["verification_complete"]
        else:
            assert preview.status_code==401
        practice=client.get(f"/api/v1/practice/{LESSON_3.id}").json()
        assert len(practice["questions"])==15 and "accepted_answers" not in str(practice)
        assert len(client.get(f"/api/v1/practice/{LESSON_3.id}/mastery").json()["questions"])==5


def test_wrong_mastery_routes_to_parallel_retry():
    with TestClient(app) as client:
        prefix=f"/api/v1/practice/{LESSON_3.id}"
        session=client.post(prefix+"/sessions").json()["session_id"]
        result=client.post(prefix+f"/sessions/{session}/mastery",json={"answers":{q.id:"incorrect" for q in MASTERY_BANK}})
        assert result.status_code==200 and not result.json()["mastered"] and result.json()["repair_routes"]
        assert client.get(prefix+f"/sessions/{session}/reassessment").status_code==409
        assert client.post(prefix+f"/sessions/{session}/repair/complete").json()["reassessment_unlocked"]
        assert len(client.get(prefix+f"/sessions/{session}/reassessment").json()["questions"])==3
