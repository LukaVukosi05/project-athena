"""Server-authoritative self-guided practice endpoints for the lesson schedule."""
from uuid import UUID,uuid4
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_optional_user
from app.practice.catalog import PRACTICE_BANKS,PRACTICE_BY_ID
from app.curriculum.repository import curriculum_repository
from app.db.database import get_db
from app.db.models.progress import PracticeSession
from app.db.models.user import User
from app.practice.schemas import AssessmentSubmission,PracticeAnswerRequest,PracticeBankResponse,PracticePublicQuestion,PracticeState
from app.practice.service import blank_response,check_answer,mastery_summary,public_status
from app.curriculum.grade8.assessment import MASTERY_BANK,MISCONCEPTION_REPAIRS,REASSESSMENT_BANK,REPAIR_RULES

router=APIRouter()
def bank_or_404(lesson_id):
    bank=PRACTICE_BANKS.get(lesson_id)
    if bank is None:raise HTTPException(404,"Practice bank not found")
    return bank
def session_or_404(lesson_id,session_id,db,user=None):
    try:UUID(session_id)
    except ValueError as error:raise HTTPException(404,"Practice session not found") from error
    result=db.get(PracticeSession,session_id)
    if result is None or result.lesson_id!=lesson_id:raise HTTPException(404,"Practice session not found")
    if result.user_id is not None and (user is None or result.user_id != user.id):raise HTTPException(404,"Practice session not found")
    return result
def question_or_404(lesson_id,question_id):
    question=PRACTICE_BY_ID.get(question_id)
    if question is None or question.lesson_id!=lesson_id:raise HTTPException(404,"Practice question not found")
    return question
def save_response(session,question_id,response,db):
    updated=dict(session.responses or {});updated[question_id]=response;session.responses=updated;db.add(session);db.commit()

@router.get("/{lesson_id}",response_model=PracticeBankResponse)
def get_practice_bank(lesson_id:str):
    bank=bank_or_404(lesson_id);found=curriculum_repository.get_lesson(lesson_id);title=found[2].title if found else "Self-guided practice"
    return PracticeBankResponse(lesson_id=lesson_id,title="Self-guided practice",supporting_text=f"{title}: solve, submit, then compare your method.",mastery_threshold=.8,questions=[PracticePublicQuestion(**q.model_dump(include={"id","question_number","difficulty","cognitive_level","marks","type","prompt","options"})) for q in bank])
@router.post("/{lesson_id}/sessions")
def start_practice(lesson_id:str,user:User|None=Depends(get_optional_user),db:Session=Depends(get_db)):
    bank_or_404(lesson_id);session=PracticeSession(id=str(uuid4()),user_id=user.id if user else None,lesson_id=lesson_id,responses={});db.add(session);db.commit();return {"session_id":session.id,"states":{}}
@router.get("/{lesson_id}/sessions/{session_id}")
def restore_practice(lesson_id:str,session_id:str,user:User|None=Depends(get_optional_user),db:Session=Depends(get_db)):
    session=session_or_404(lesson_id,session_id,db,user);return {"session_id":session.id,"states":{qid:public_status(value,PRACTICE_BY_ID[qid]) for qid,value in session.responses.items() if qid in PRACTICE_BY_ID}}
@router.post("/{lesson_id}/sessions/{session_id}/questions/{question_id}/submit")
def submit_answer(lesson_id:str,session_id:str,question_id:str,payload:PracticeAnswerRequest,user:User|None=Depends(get_optional_user),db:Session=Depends(get_db)):
    session,question=session_or_404(lesson_id,session_id,db,user),question_or_404(lesson_id,question_id);response=dict((session.responses or {}).get(question_id,blank_response()));response["state"]=PracticeState.CHECKING;response["answer"]=payload.answer;response["attempts"]=int(response.get("attempts",0))+1;correct=check_answer(question_id,payload.answer);response["correct"]=correct
    if correct:response["first_attempt_correct"]=response["attempts"]==1;response["state"]=PracticeState.CORRECT;feedback=question.correct_feedback
    else:response["state"]=PracticeState.INCORRECT_FIRST_ATTEMPT if response["attempts"]==1 else PracticeState.INCORRECT_RETRY;feedback="Not quite yet."
    save_response(session,question_id,response,db);return {**public_status(response,question),"feedback":feedback}
@router.post("/{lesson_id}/sessions/{session_id}/questions/{question_id}/hint")
def request_hint(lesson_id:str,session_id:str,question_id:str,hint_index:int|None=None,user:User|None=Depends(get_optional_user),db:Session=Depends(get_db)):
    session,question=session_or_404(lesson_id,session_id,db,user),question_or_404(lesson_id,question_id);response=dict((session.responses or {}).get(question_id,blank_response()));index=int(response.get("hints_used",0)) if hint_index is None else hint_index
    if index < 0 or index >= len(question.hints):raise HTTPException(409,"No further hints are available")
    response["hints_used"]=max(int(response.get("hints_used",0)),index+1)
    if response["hints_used"]>=len(question.hints) and not response.get("correct"):response["state"]=PracticeState.SOLUTION_AVAILABLE
    save_response(session,question_id,response,db);return {**public_status(response,question),"hint":question.hints[index],"hint_index":index,"hint_count":len(question.hints),"hints_remaining":len(question.hints)-index-1,"hint_complete":index==len(question.hints)-1}
@router.get("/{lesson_id}/sessions/{session_id}/questions/{question_id}/solution")
def get_solution(lesson_id:str,session_id:str,question_id:str,user:User|None=Depends(get_optional_user),db:Session=Depends(get_db)):
    session,question=session_or_404(lesson_id,session_id,db,user),question_or_404(lesson_id,question_id);response=dict((session.responses or {}).get(question_id,blank_response()));status=public_status(response,question)
    if not status["solution_available"]:raise HTTPException(403,"Worked solution is not available yet")
    response["solution_viewed"]=True;response["state"]=PracticeState.COMPLETE if response.get("correct") else PracticeState.SOLUTION_VIEWED;save_response(session,question_id,response,db);return {**public_status(response,question),"worked_solution":[item.model_dump() for item in question.worked_solution],"verification":question.verification}
@router.get("/{lesson_id}/sessions/{session_id}/summary")
def get_summary(lesson_id:str,session_id:str,user:User|None=Depends(get_optional_user),db:Session=Depends(get_db)):
    return mastery_summary(session_or_404(lesson_id,session_id,db,user).responses or {},bank_or_404(lesson_id),.8)


def _normalise_assessment(value: str) -> str:
    return "".join(str(value).casefold().replace("−", "-").replace("–", "-").split())


def _score_assessment(bank, answers: dict[str, str]) -> tuple[int, list, list[str]]:
    expected={item.id for item in bank}
    if set(answers) != expected:raise HTTPException(422,f"Answers must contain exactly: {', '.join(sorted(expected))}")
    reviewed=[];tags=[];correct=0
    for item in bank:
        passed=_normalise_assessment(answers[item.id])==_normalise_assessment(item.answer)
        correct+=int(passed)
        if not passed:tags.extend(item.misconception_tags)
        reviewed.append({"id":item.id,"correct":passed,"answer":item.answer,"solution":item.solution,"verification":item.verification})
    return correct,reviewed,list(dict.fromkeys(tags))


@router.get("/{lesson_id}/mastery")
def get_mastery(lesson_id:str):
    if lesson_id!="g8-algebraic-equations-01":raise HTTPException(404,"Mastery bank not found")
    return {"lesson_id":lesson_id,"mastery_threshold":.8,"questions":[item.public() for item in MASTERY_BANK]}


@router.post("/{lesson_id}/sessions/{session_id}/mastery")
def submit_mastery(lesson_id:str,session_id:str,payload:AssessmentSubmission,user:User|None=Depends(get_optional_user),db:Session=Depends(get_db)):
    if lesson_id!="g8-algebraic-equations-01":raise HTTPException(404,"Mastery bank not found")
    session=session_or_404(lesson_id,session_id,db,user);correct,reviewed,tags=_score_assessment(MASTERY_BANK,payload.answers);mastered=correct>=4
    updated=dict(session.responses or {});updated["__mastery__"]={"correct":correct,"mastered":mastered,"tags":tags};session.responses=updated;db.add(session);db.commit()
    return {"questions_correct":correct,"total_questions":5,"score":correct*20,"mastered":mastered,"readiness_decision":"ready" if mastered else "targeted_repair_required","diagnosis":tags,"worked_review":reviewed,"repair_routes":[] if mastered else [{"tag":tag,**MISCONCEPTION_REPAIRS[tag]} for tag in tags if tag in MISCONCEPTION_REPAIRS]}


@router.get("/{lesson_id}/sessions/{session_id}/repair")
def get_repair(lesson_id:str,session_id:str,user:User|None=Depends(get_optional_user),db:Session=Depends(get_db)):
    session=session_or_404(lesson_id,session_id,db,user);mastery=(session.responses or {}).get("__mastery__")
    if not mastery or mastery.get("mastered"):raise HTTPException(409,"Targeted repair is not required")
    tags=mastery.get("tags",[])
    return {"diagnosis":tags,"routes":[{"tag":tag,**MISCONCEPTION_REPAIRS[tag]} for tag in tags if tag in MISCONCEPTION_REPAIRS],"source_rules":REPAIR_RULES}


@router.post("/{lesson_id}/sessions/{session_id}/repair/complete")
def complete_repair(lesson_id:str,session_id:str,user:User|None=Depends(get_optional_user),db:Session=Depends(get_db)):
    session=session_or_404(lesson_id,session_id,db,user);mastery=(session.responses or {}).get("__mastery__")
    if not mastery or mastery.get("mastered"):raise HTTPException(409,"Targeted repair is not required")
    updated=dict(session.responses or {});updated["__repair__"]={"complete":True,"tags":mastery.get("tags",[])};session.responses=updated;db.add(session);db.commit();return {"repair_complete":True,"reassessment_unlocked":True}


@router.get("/{lesson_id}/sessions/{session_id}/reassessment")
def get_reassessment(lesson_id:str,session_id:str,user:User|None=Depends(get_optional_user),db:Session=Depends(get_db)):
    session=session_or_404(lesson_id,session_id,db,user)
    if not (session.responses or {}).get("__repair__",{}).get("complete"):raise HTTPException(409,"Complete targeted repair first")
    return {"lesson_id":lesson_id,"questions":[item.public() for item in REASSESSMENT_BANK]}


@router.post("/{lesson_id}/sessions/{session_id}/reassessment")
def submit_reassessment(lesson_id:str,session_id:str,payload:AssessmentSubmission,user:User|None=Depends(get_optional_user),db:Session=Depends(get_db)):
    session=session_or_404(lesson_id,session_id,db,user)
    if not (session.responses or {}).get("__repair__",{}).get("complete"):raise HTTPException(409,"Complete targeted repair first")
    correct,reviewed,tags=_score_assessment(REASSESSMENT_BANK,payload.answers);ready=correct/3>=.8
    updated=dict(session.responses or {});updated["__reassessment__"]={"correct":correct,"ready":ready,"tags":tags};session.responses=updated;db.add(session);db.commit()
    return {"questions_correct":correct,"total_questions":3,"score":round(correct/3*100),"ready":ready,"readiness_decision":"ready" if ready else "more_repair_required","diagnosis":tags,"worked_review":reviewed}
