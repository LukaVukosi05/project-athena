import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.curriculum.grade12.lessons.sequences_practice import LESSON_ONE_PRACTICE
from app.db.database import Base, get_db
from app.main import app
from app.practice.schemas import SOURCE_DOCUMENT
from app.practice.service import check_answer, mastery_summary


@pytest.fixture
def practice_client():
    engine=create_engine("sqlite://",connect_args={"check_same_thread":False},poolclass=StaticPool)
    Base.metadata.create_all(engine)
    def test_db():
        with Session(engine) as session: yield session
    app.dependency_overrides[get_db]=test_db
    with TestClient(app) as client: yield client
    app.dependency_overrides.clear();Base.metadata.drop_all(engine)


def test_lesson_one_bank_is_valid_and_authorised():
    assert len(LESSON_ONE_PRACTICE)==12
    assert len({question.id for question in LESSON_ONE_PRACTICE})==12
    assert [question.question_number for question in LESSON_ONE_PRACTICE]==list(range(1,13))
    assert all(question.source==SOURCE_DOCUMENT for question in LESSON_ONE_PRACTICE)
    assert all(2<=len(question.hints)<=3 for question in LESSON_ONE_PRACTICE)
    assert all(question.worked_solution and all(step.why!=step.explanation for step in question.worked_solution) for question in LESSON_ONE_PRACTICE)
    assert sum(question.type=="classification" for question in LESSON_ONE_PRACTICE)==3
    assert {"missing_term","numeric","multiple_choice","error_analysis"}.issubset({question.type for question in LESSON_ONE_PRACTICE})


def test_numeric_and_classification_normalisation():
    assert check_answer("g12-seq-l01-p02","10.0")
    assert check_answer("g12-seq-l01-p04"," Geometric sequence ")
    assert not check_answer("g12-seq-l01-p04","arithmetic")


def test_public_bank_hides_answers_hints_and_solutions(practice_client):
    response=practice_client.get("/api/v1/practice/g12-sequences-series-01")
    assert response.status_code==200 and len(response.json()["questions"])==12
    serialized=response.text.lower()
    assert "accepted_answers" not in serialized and "worked_solution" not in serialized and "hints" not in serialized
    lesson=practice_client.get("/api/v1/lessons/g12-sequences-series-01").json()
    assert any(block.get("data",{}).get("practice_bank_id")=="g12-sequences-series-01" for block in lesson["blocks"])
    practice_blocks=[block for block in lesson["blocks"] if block.get("type")=="practice"]
    assert practice_blocks==[{"type":"practice","title":"Self-guided practice","content":"Solve, submit, then compare your method.","data":{"practice_bank_id":"g12-sequences-series-01"}}]
    assert not any(block.get("type")=="checkpoint" for block in lesson["blocks"])


def test_attempt_retry_hint_solution_and_persistence(practice_client):
    started=practice_client.post("/api/v1/practice/g12-sequences-series-01/sessions").json();session_id=started["session_id"];base=f"/api/v1/practice/g12-sequences-series-01/sessions/{session_id}/questions/g12-seq-l01-p01"
    first=practice_client.post(base+"/submit",json={"answer":"geometric"}).json()
    assert first["state"]=="incorrect_first_attempt" and not first["solution_available"] and first["feedback"]=="Not quite yet."
    assert practice_client.get(base+"/solution").status_code==403
    hint=practice_client.post(base+"/hint").json();assert hint["hints_used"]==1 and "hint" in hint
    retry=practice_client.post(base+"/submit",json={"answer":"arithmetic"}).json()
    assert retry["correct"] and retry["attempts"]==2 and not retry["first_attempt_correct"] and retry["solution_available"]
    solution=practice_client.get(base+"/solution").json()
    assert solution["solution_viewed"] and solution["next_enabled"] and len(solution["worked_solution"])>=4
    restored=practice_client.get(f"/api/v1/practice/g12-sequences-series-01/sessions/{session_id}").json()
    assert restored["states"]["g12-seq-l01-p01"]["attempts"]==2


def test_progressive_final_hint_unlocks_solution(practice_client):
    sid=practice_client.post("/api/v1/practice/g12-sequences-series-01/sessions").json()["session_id"]
    base=f"/api/v1/practice/g12-sequences-series-01/sessions/{sid}/questions/g12-seq-l01-p02"
    results=[practice_client.post(base+"/hint").json() for _ in range(3)]
    assert [item["hints_used"] for item in results]==[1,2,3]
    assert results[-1]["solution_available"]


def test_mastery_is_server_calculated_at_eighty_percent():
    ten={q.id:{"correct":index<10,"first_attempt_correct":index<8,"hints_used":1 if index==8 else 0,"attempts":1,"solution_viewed":False} for index,q in enumerate(LESSON_ONE_PRACTICE)}
    nine={qid:{**value,"correct":index<9} for index,(qid,value) in enumerate(ten.items())}
    assert mastery_summary(ten,LESSON_ONE_PRACTICE)["mastered"]
    assert not mastery_summary(nine,LESSON_ONE_PRACTICE)["mastered"]
