"""Two-step lesson release, question-specific progression, and assessment gates."""
import hashlib
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from app.curriculum.content_manifest import readiness_for
from app.curriculum.repository import curriculum_repository
from app.curriculum.validation import validate_curriculum
from app.curriculum.grade8.lesson5_runtime import LESSON_5, SOURCE_DATA
from app.curriculum.grade8.assessment_lesson5 import PRACTICE_BANK, MASTERY_BANK, REASSESSMENT_BANK

SOURCE=Path(__file__).resolve().parents[2]/"docs/curriculum/grade8/algebraic-equations/Project_Athena_Grade8_Algebraic_Equations_Gold_Pack_v1_0.docx"


def test_approved_pack_and_all_question_banks():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==SOURCE_DATA["source_sha256"]
    assert [q.id for q in LESSON_5.whiteboard_questions]==[f"g8-ae-l05-w{n:02}" for n in range(1,16)]
    assert [q.id for q in PRACTICE_BANK]==[f"g8-ae-l05-p{n:02}" for n in range(1,16)]
    assert len(MASTERY_BANK)==5 and len(REASSESSMENT_BANK)==3
    assert readiness_for(LESSON_5).value=="published"
    assert not [f for f in validate_curriculum([curriculum_repository.get_grade("grade-8")]) if f.lesson_id==LESSON_5.id]


def test_each_timeline_reverses_two_operations_and_checks_original():
    families={"two_step_balance_native","operation_machine","two_step_number_line","two_step_fraction_scale","two_step_context"}
    assert {q.whiteboard.visualization.template for q in LESSON_5.whiteboard_questions}==families
    for q in LESSON_5.whiteboard_questions:
        board=q.whiteboard
        assert len(board.steps)>=5,(q.id,len(board.steps))
        assert board.initial_expression==q.whiteboard.problem
        assert "Checked:" in board.steps[-1].after_expression
        assert board.steps[-1].state_after["verification_complete"]
        assert any("both" in step.working_expression.lower() for step in board.steps[:-1]),q.id
        for index,step in enumerate(board.steps):
            assert step.before_expression!=step.after_expression,q.id
            assert step.events and step.visualization_state
            assert [e.text for e in step.events if e.type=="caption"]==[e.text for e in step.events if e.type=="narration"]
            assert min(e.at_ms for e in step.events if e.type=="show_operation") < min(e.at_ms for e in step.events if e.type=="reveal")
            if index:assert step.before_expression==board.steps[index-1].after_expression
    assert "divide the constant" in LESSON_5.whiteboard_questions[8].whiteboard.steps[0].narration
    assert "a ≠ 0" in LESSON_5.whiteboard_questions[14].whiteboard.steps[-1].after_expression


def test_public_preview_contains_no_answer_and_reveal_is_question_specific():
    with TestClient(app) as client:
        preview=client.get(f"/api/v1/lessons/{LESSON_5.id}")
        if preview.status_code==200:
            body=preview.json()
            assert len(body["whiteboard_questions"])==15
            for q in body["whiteboard_questions"]:
                assert "answer" not in q and "full_memo" not in q
                board=q["whiteboard"]
                assert len(board["steps"])==1 and not board["steps"][0]["events"]
                assert board["steps"][0]["before_expression"]==board["steps"][0]["after_expression"]
                data=board["visualization"]["parameters"]["source_data"]
                assert "solution = " not in data and "reverse operations = " not in data
            assert len(next(block for block in body["blocks"] if block["type"]=="whiteboard")["steps"])==1
            for n in (1,9,15):
                response=client.post(f"/api/v1/lessons/{LESSON_5.id}/questions/g8-ae-l05-w{n:02}/reveal")
                assert response.status_code==200 and response.json()["whiteboard"]["steps"][-1]["state_after"]["verification_complete"]
        else:assert preview.status_code==401
        practice=client.get(f"/api/v1/practice/{LESSON_5.id}").json()
        assert len(practice["questions"])==15 and "accepted_answers" not in str(practice)


def test_failed_mastery_requires_repair_before_parallel_reassessment():
    with TestClient(app) as client:
        prefix=f"/api/v1/practice/{LESSON_5.id}"
        session=client.post(prefix+"/sessions").json()["session_id"]
        failure=client.post(prefix+f"/sessions/{session}/mastery",
                            json={"answers":{q.id:"incorrect" for q in MASTERY_BANK}})
        assert failure.status_code==200 and not failure.json()["mastered"] and failure.json()["repair_routes"]
        assert client.get(prefix+f"/sessions/{session}/reassessment").status_code==409
        assert client.post(prefix+f"/sessions/{session}/repair/complete").json()["reassessment_unlocked"]
        assert len(client.get(prefix+f"/sessions/{session}/reassessment").json()["questions"])==3
