"""Source, complete teaching states, release, and answer-gate checks."""
import hashlib
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from app.curriculum.repository import curriculum_repository
from app.curriculum.content_manifest import readiness_for
from app.curriculum.validation import validate_curriculum
from app.curriculum.grade8.lesson4_runtime import LESSON_4, SOURCE_DATA
from app.curriculum.grade8.assessment_lesson4 import PRACTICE_BANK, MASTERY_BANK, REASSESSMENT_BANK

SOURCE=Path(__file__).resolve().parents[2]/"docs/curriculum/grade8/algebraic-equations/Project_Athena_Grade8_Algebraic_Equations_Gold_Pack_v1_0.docx"


def test_approved_source_and_four_complete_question_banks():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==SOURCE_DATA["source_sha256"]
    assert [q.id for q in LESSON_4.whiteboard_questions]==[f"g8-ae-l04-w{n:02}" for n in range(1,16)]
    assert [q.id for q in PRACTICE_BANK]==[f"g8-ae-l04-p{n:02}" for n in range(1,16)]
    assert len(MASTERY_BANK)==5 and len(REASSESSMENT_BANK)==3
    assert readiness_for(LESSON_4).value=="published"
    assert not [f for f in validate_curriculum([curriculum_repository.get_grade("grade-8")]) if f.lesson_id==LESSON_4.id]


def test_each_question_teaches_and_finishes_with_original_check():
    families={"equal_groups","fraction_scale","multiplicative_balance","multiplicative_context"}
    assert {q.whiteboard.visualization.template for q in LESSON_4.whiteboard_questions}==families
    for q in LESSON_4.whiteboard_questions:
        board=q.whiteboard
        assert len(board.steps)>=3
        assert board.steps[0].before_expression==q.full_memo[0].split(":")[-1].strip() or board.problem==board.steps[0].before_expression
        for i,step in enumerate(board.steps):
            assert step.before_expression!=step.after_expression
            assert step.events and step.visualization_state
            assert [e.text for e in step.events if e.type=="caption"]==[e.text for e in step.events if e.type=="narration"]
            assert min(e.at_ms for e in step.events if e.type=="show_operation") < min(e.at_ms for e in step.events if e.type=="reveal")
            if i:assert step.before_expression==board.steps[i-1].after_expression
        assert "Checked:" in board.steps[-1].after_expression
        assert board.steps[-1].state_after["verification_complete"]


def test_lesson_and_practice_hide_answers_until_explicit_reveal():
    with TestClient(app) as client:
        preview=client.get(f"/api/v1/lessons/{LESSON_4.id}")
        if preview.status_code==200:
            body=preview.json()
            assert len(body["whiteboard_questions"])==15
            assert all("answer" not in q and "full_memo" not in q for q in body["whiteboard_questions"])
            for q in body["whiteboard_questions"]:
                board=q["whiteboard"]
                assert len(board["steps"])==1 and not board["steps"][0]["events"]
                assert board["steps"][0]["before_expression"]==board["steps"][0]["after_expression"]
                assert "solution = " not in board["visualization"]["parameters"]["source_data"]
            assert len(next(block for block in body["blocks"] if block["type"]=="whiteboard")["steps"])==1
            revealed=client.post(f"/api/v1/lessons/{LESSON_4.id}/questions/g8-ae-l04-w15/reveal")
            assert revealed.status_code==200 and revealed.json()["whiteboard"]["steps"][-1]["state_after"]["verification_complete"]
        else:assert preview.status_code==401
        practice=client.get(f"/api/v1/practice/{LESSON_4.id}").json()
        assert len(practice["questions"])==15 and "accepted_answers" not in str(practice)
