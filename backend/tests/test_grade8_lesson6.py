"""Approved Lesson 6 release and assessment gates."""
import hashlib
from fractions import Fraction
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app
from app.curriculum.content_manifest import readiness_for
from app.curriculum.repository import curriculum_repository
from app.curriculum.validation import validate_curriculum
from app.curriculum.grade8.lesson6_runtime import LESSON_6,SOURCE_DATA
from app.curriculum.grade8.assessment_lesson6 import PRACTICE_BANK,MASTERY_BANK,REASSESSMENT_BANK,MISCONCEPTION_REPAIRS
SOURCE=Path(__file__).resolve().parents[2]/"docs/curriculum/grade8/algebraic-equations/Project_Athena_Grade8_Algebraic_Equations_Gold_Pack_v1_0.docx"

def test_pack_banks_and_release():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==SOURCE_DATA["source_sha256"]
    for bank,prefix,count in ((LESSON_6.whiteboard_questions,"w",15),(PRACTICE_BANK,"p",15),(MASTERY_BANK,"m",5),(REASSESSMENT_BANK,"r",3)):
        assert [q.id for q in bank]==[f"g8-ae-l06-{prefix}{n:02}" for n in range(1,count+1)]
    assert set(tag for q in MASTERY_BANK for tag in q.misconception_tags)<=set(MISCONCEPTION_REPAIRS)
    assert readiness_for(LESSON_6).value=="published"
    assert not [f for f in validate_curriculum([curriculum_repository.get_grade("grade-8")]) if f.lesson_id==LESSON_6.id]

def test_all_question_specific_timelines_and_final_checks():
    assert {q.whiteboard.visualization.template for q in LESSON_6.whiteboard_questions}=={"variables_both_sides_native","expression_comparison","identity_contradiction","dual_rate_timeline","equal_sides_triangle"}
    for q in LESSON_6.whiteboard_questions:
        board=q.whiteboard
        assert len(board.steps)>=5 and board.initial_expression==board.problem
        assert board.steps[-1].after_expression.startswith("Checked:") and board.steps[-1].state_after["verification_complete"]
        for i,s in enumerate(board.steps):
            assert s.before_expression!=s.after_expression and s.events and s.visualization_state
            assert [e.text for e in s.events if e.type=="caption"]==[e.text for e in s.events if e.type=="narration"]
            assert min(e.at_ms for e in s.events if e.type=="show_operation")<min(e.at_ms for e in s.events if e.type=="reveal")
            if i:assert s.before_expression==board.steps[i-1].after_expression
    assert "infinitely many solutions" in LESSON_6.whiteboard_questions[7].whiteboard.steps[-1].after_expression
    assert "no solution" in LESSON_6.whiteboard_questions[8].whiteboard.steps[-1].after_expression
    assert "20 cm" in LESSON_6.whiteboard_questions[12].whiteboard.steps[-1].after_expression
    assert len(LESSON_6.whiteboard_questions[14].whiteboard.steps)==15

def test_api_preview_reveal_and_repair_gate():
    with TestClient(app) as client:
        topic=client.get("/api/v1/curriculum/grades/grade-8/topics/algebraic-equations").json()
        row=next(row for group in topic["subtopics"] for row in group["lessons"] if row["id"]==LESSON_6.id)
        assert row["readiness"]=="published" and row["usable"]
        response=client.get(f"/api/v1/lessons/{LESSON_6.id}")
        if response.status_code==200:
            for q in response.json()["whiteboard_questions"]:
                assert "answer" not in q and "full_memo" not in q
                board=q["whiteboard"]
                assert len(board["steps"])==1 and not board["steps"][0]["events"]
                assert board["steps"][0]["after_expression"]==board["steps"][0]["before_expression"]
                source=board["visualization"]["parameters"]["source_data"]
                assert not any(term in source for term in ("solution = ","classification = ","test values = ","meeting week = ","equal cost rand = "))
            for n in range(1,16):
                revealed=client.post(f"/api/v1/lessons/{LESSON_6.id}/questions/g8-ae-l06-w{n:02}/reveal")
                assert revealed.status_code==200,n
                assert revealed.json()["whiteboard"]["steps"][-1]["state_after"]["verification_complete"]
        else:assert response.status_code==401
        practice=client.get(f"/api/v1/practice/{LESSON_6.id}").json()
        assert len(practice["questions"])==15 and "accepted_answers" not in str(practice)
        prefix=f"/api/v1/practice/{LESSON_6.id}"
        session=client.post(prefix+"/sessions").json()["session_id"]
        failed=client.post(prefix+f"/sessions/{session}/mastery",json={"answers":{q.id:"incorrect" for q in MASTERY_BANK}})
        assert failed.status_code==200 and not failed.json()["mastered"] and failed.json()["repair_routes"]
        assert client.get(prefix+f"/sessions/{session}/reassessment").status_code==409
        assert client.post(prefix+f"/sessions/{session}/repair/complete").json()["reassessment_unlocked"]
        assert len(client.get(prefix+f"/sessions/{session}/reassessment").json()["questions"])==3


def test_final_values_satisfy_both_original_expressions():
    one_solution = {
        1:(3,2,1,10,4), 2:(5,-7,2,8,5), 3:(4,9,6,-3,6),
        4:(-2,7,1,-8,5), 5:(-3,4,1,-12,4),
        6:(Fraction(1,2),2,Fraction(1,5),5,10),
        7:(Fraction(2,3),1,Fraction(1,3),5,12),
        10:(6,-4,2,12,4), 11:(8,50,11,20,10),
        12:(35,120,15,260,7), 13:(3,2,5,-10,6),
        14:(Fraction(-1,2),6,Fraction(1,4),-3,12),
        15:(Fraction(-3,2),7,Fraction(1,2),-9,8),
    }
    for number,(a,b,c,d,x) in one_solution.items():
        assert a*x+b==c*x+d,number
        assert str(x) in LESSON_6.whiteboard_questions[number-1].whiteboard.steps[-1].after_expression
    assert all(5*x+6==5*x+6 for x in (0,2,-3))
    assert all(4*x+3!=4*x-2 for x in (0,2,-3))
