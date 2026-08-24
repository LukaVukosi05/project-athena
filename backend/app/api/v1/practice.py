"""Server-authoritative Lesson 1 self-guided practice endpoints."""
from uuid import UUID, uuid4
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_optional_user
from app.curriculum.grade12.lessons.sequences_practice import LESSON_ID, LESSON_ONE_PRACTICE, PRACTICE_BY_ID
from app.db.database import get_db
from app.db.models.progress import PracticeSession
from app.db.models.user import User
from app.practice.schemas import PracticeAnswerRequest, PracticeBankResponse, PracticePublicQuestion, PracticeState
from app.practice.service import blank_response, check_answer, mastery_summary, public_status

router=APIRouter()

def session_or_404(session_id:str,db:Session)->PracticeSession:
    try: UUID(session_id)
    except ValueError as error: raise HTTPException(404,"Practice session not found") from error
    result=db.get(PracticeSession,session_id)
    if result is None or result.lesson_id!=LESSON_ID: raise HTTPException(404,"Practice session not found")
    return result

def question_or_404(question_id:str):
    question=PRACTICE_BY_ID.get(question_id)
    if question is None: raise HTTPException(404,"Practice question not found")
    return question

def save_response(session,question_id,response,db):
    updated=dict(session.responses or {});updated[question_id]=response;session.responses=updated;db.add(session);db.commit()

@router.get(f"/{LESSON_ID}",response_model=PracticeBankResponse)
def get_practice_bank():
    return PracticeBankResponse(lesson_id=LESSON_ID,title="Self-guided practice",supporting_text="Solve, submit, then compare your method.",mastery_threshold=.8,questions=[PracticePublicQuestion(**q.model_dump(include={"id","question_number","difficulty","cognitive_level","marks","type","prompt","options"})) for q in LESSON_ONE_PRACTICE])

@router.post(f"/{LESSON_ID}/sessions")
def start_practice(user:User|None=Depends(get_optional_user),db:Session=Depends(get_db)):
    session=PracticeSession(id=str(uuid4()),user_id=user.id if user else None,lesson_id=LESSON_ID,responses={});db.add(session);db.commit();return {"session_id":session.id,"states":{}}

@router.get(f"/{LESSON_ID}/sessions/{{session_id}}")
def restore_practice(session_id:str,db:Session=Depends(get_db)):
    session=session_or_404(session_id,db);return {"session_id":session.id,"states":{qid:public_status(value,PRACTICE_BY_ID[qid]) for qid,value in session.responses.items() if qid in PRACTICE_BY_ID}}

@router.post(f"/{LESSON_ID}/sessions/{{session_id}}/questions/{{question_id}}/submit")
def submit_answer(session_id:str,question_id:str,payload:PracticeAnswerRequest,db:Session=Depends(get_db)):
    session,question=session_or_404(session_id,db),question_or_404(question_id);response=dict((session.responses or {}).get(question_id,blank_response()));response["state"]=PracticeState.CHECKING;response["answer"]=payload.answer;response["attempts"]=int(response.get("attempts",0))+1;correct=check_answer(question_id,payload.answer);response["correct"]=correct
    if correct: response["first_attempt_correct"]=response["attempts"]==1;response["state"]=PracticeState.CORRECT;feedback=question.correct_feedback
    else: response["state"]=PracticeState.INCORRECT_FIRST_ATTEMPT if response["attempts"]==1 else PracticeState.INCORRECT_RETRY;feedback="Not quite yet."
    save_response(session,question_id,response,db);return {**public_status(response,question),"feedback":feedback}

@router.post(f"/{LESSON_ID}/sessions/{{session_id}}/questions/{{question_id}}/hint")
def request_hint(session_id:str,question_id:str,db:Session=Depends(get_db)):
    session,question=session_or_404(session_id,db),question_or_404(question_id);response=dict((session.responses or {}).get(question_id,blank_response()));index=min(int(response.get("hints_used",0)),len(question.hints)-1);response["hints_used"]=index+1
    if response["hints_used"]>=len(question.hints) and not response.get("correct"): response["state"]=PracticeState.SOLUTION_AVAILABLE
    save_response(session,question_id,response,db);return {**public_status(response,question),"hint":question.hints[index]}

@router.get(f"/{LESSON_ID}/sessions/{{session_id}}/questions/{{question_id}}/solution")
def get_solution(session_id:str,question_id:str,db:Session=Depends(get_db)):
    session,question=session_or_404(session_id,db),question_or_404(question_id);response=dict((session.responses or {}).get(question_id,blank_response()));status=public_status(response,question)
    if not status["solution_available"]: raise HTTPException(403,"Worked solution is not available yet")
    response["solution_viewed"]=True;response["state"]=PracticeState.COMPLETE if response.get("correct") else PracticeState.SOLUTION_VIEWED;save_response(session,question_id,response,db)
    return {**public_status(response,question),"worked_solution":[item.model_dump() for item in question.worked_solution],"verification":question.verification}

@router.get(f"/{LESSON_ID}/sessions/{{session_id}}/summary")
def get_summary(session_id:str,db:Session=Depends(get_db)):
    return mastery_summary(session_or_404(session_id,db).responses or {},LESSON_ONE_PRACTICE,.8)
