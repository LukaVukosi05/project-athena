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
from app.curriculum.grade8 import assessment_lesson2, assessment_lesson3, assessment_lesson4, assessment_lesson5, assessment_lesson6, assessment_lesson7, assessment_lesson8, assessment_lesson9, assessment_lesson10
from app.curriculum.grade8 import assessment_expressions

ASSESSMENT_BANKS={
    "g8-algebraic-expressions-01":(assessment_expressions.MASTERY_BANK, assessment_expressions.REASSESSMENT_BANK,
                                    assessment_expressions.MISCONCEPTION_REPAIRS, assessment_expressions.REPAIR_RULES),
    "g8-algebraic-equations-01":(MASTERY_BANK,REASSESSMENT_BANK,MISCONCEPTION_REPAIRS,REPAIR_RULES),
    "g8-algebraic-equations-02":(assessment_lesson2.MASTERY_BANK,assessment_lesson2.REASSESSMENT_BANK,
                                  assessment_lesson2.MISCONCEPTION_REPAIRS,assessment_lesson2.REPAIR_RULES),
    "g8-algebraic-equations-03":(assessment_lesson3.MASTERY_BANK,assessment_lesson3.REASSESSMENT_BANK,
                                  assessment_lesson3.MISCONCEPTION_REPAIRS,assessment_lesson3.REPAIR_RULES),
    "g8-algebraic-equations-04":(assessment_lesson4.MASTERY_BANK,assessment_lesson4.REASSESSMENT_BANK,
                                  assessment_lesson4.MISCONCEPTION_REPAIRS,assessment_lesson4.REPAIR_RULES),
    "g8-algebraic-equations-05":(assessment_lesson5.MASTERY_BANK,assessment_lesson5.REASSESSMENT_BANK,
                                  assessment_lesson5.MISCONCEPTION_REPAIRS,assessment_lesson5.REPAIR_RULES),
    "g8-algebraic-equations-06":(assessment_lesson6.MASTERY_BANK,assessment_lesson6.REASSESSMENT_BANK,
                                  assessment_lesson6.MISCONCEPTION_REPAIRS,assessment_lesson6.REPAIR_RULES),
    "g8-algebraic-equations-07":(assessment_lesson7.MASTERY_BANK,assessment_lesson7.REASSESSMENT_BANK,
                                  assessment_lesson7.MISCONCEPTION_REPAIRS,assessment_lesson7.REPAIR_RULES),
    "g8-algebraic-equations-08":(assessment_lesson8.MASTERY_BANK,assessment_lesson8.REASSESSMENT_BANK,
                                  assessment_lesson8.MISCONCEPTION_REPAIRS,assessment_lesson8.REPAIR_RULES),
    "g8-algebraic-equations-09":(assessment_lesson9.MASTERY_BANK,assessment_lesson9.REASSESSMENT_BANK,
                                  assessment_lesson9.MISCONCEPTION_REPAIRS,assessment_lesson9.REPAIR_RULES),
    "g8-algebraic-equations-10":(assessment_lesson10.MASTERY_BANK,assessment_lesson10.REASSESSMENT_BANK,
                                  assessment_lesson10.MISCONCEPTION_REPAIRS,assessment_lesson10.REPAIR_RULES),
}

def assessment_or_404(lesson_id):
    result=ASSESSMENT_BANKS.get(lesson_id)
    if result is None:raise HTTPException(404,"Mastery bank not found")
    return result

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
        # This item explicitly tests the fixed fee model AND verification.
        # Its pack's short answer is a memo, not sufficient submission evidence.
        accepted=([*getattr(item,"accepted_answers",[])]
                  if item.id in {"g8-ae-l10-m05", "g8-ae-l10-r03"}
                  else [item.answer,*getattr(item,"accepted_answers",[])])
        passed=any(_normalise_assessment(answers[item.id]).rstrip(".")==_normalise_assessment(option).rstrip(".") for option in accepted)
        correct+=int(passed)
        if not passed:tags.extend(item.misconception_tags)
        reviewed.append({"id":item.id,"correct":passed,"answer":item.answer,"solution":item.solution,"verification":item.verification})
    return correct,reviewed,list(dict.fromkeys(tags))


@router.get("/{lesson_id}/mastery")
def get_mastery(lesson_id:str):
    mastery,_,_,_=assessment_or_404(lesson_id)
    return {"lesson_id":lesson_id,"mastery_threshold":.8,"questions":[item.public() for item in mastery]}


@router.post("/{lesson_id}/sessions/{session_id}/mastery")
def submit_mastery(lesson_id:str,session_id:str,payload:AssessmentSubmission,user:User|None=Depends(get_optional_user),db:Session=Depends(get_db)):
    mastery,_,repairs,_=assessment_or_404(lesson_id)
    session=session_or_404(lesson_id,session_id,db,user);correct,reviewed,tags=_score_assessment(mastery,payload.answers)
    context_verified=next((row["correct"] for row in reviewed if row["id"] == "g8-ae-l10-m05"),True)
    earned_marks = sum((question.marks or 0) for question, row in zip(mastery, reviewed) if row['correct'])
    mastered=(earned_marks >= 16 if lesson_id == 'g8-algebraic-expressions-01' else correct>=4) and context_verified
    decision=("ready" if mastered else "repeat_diagnostic_required" if lesson_id == "g8-algebraic-equations-10" and correct<=2 else "targeted_repair_required")
    updated=dict(session.responses or {});updated["__mastery__"]={"correct":correct,"mastered":mastered,"tags":tags,"decision":decision,"context_verified":context_verified};session.responses=updated;db.add(session);db.commit()
    score=(earned_marks * 5 if lesson_id == 'g8-algebraic-expressions-01' else correct*20)
    return {"questions_correct":correct,"total_questions":5,"score":score,"mastered":mastered,"readiness_decision":decision,"context_verified":context_verified,"diagnosis":tags,"worked_review":reviewed,"repair_routes":[] if mastered else [{"tag":tag,**repairs[tag]} for tag in tags if tag in repairs]}


@router.get("/{lesson_id}/sessions/{session_id}/repair")
def get_repair(lesson_id:str,session_id:str,user:User|None=Depends(get_optional_user),db:Session=Depends(get_db)):
    _,_,repairs,rules=assessment_or_404(lesson_id)
    session=session_or_404(lesson_id,session_id,db,user);mastery=(session.responses or {}).get("__mastery__")
    if not mastery or mastery.get("mastered"):raise HTTPException(409,"Targeted repair is not required")
    tags=mastery.get("tags",[])
    return {"diagnosis":tags,"routes":[{"tag":tag,**repairs[tag]} for tag in tags if tag in repairs],"source_rules":rules}


@router.post("/{lesson_id}/sessions/{session_id}/repair/complete")
def complete_repair(lesson_id:str,session_id:str,user:User|None=Depends(get_optional_user),db:Session=Depends(get_db)):
    session=session_or_404(lesson_id,session_id,db,user);mastery=(session.responses or {}).get("__mastery__")
    if not mastery or mastery.get("mastered"):raise HTTPException(409,"Targeted repair is not required")
    if lesson_id == "g8-algebraic-equations-10" and mastery.get("decision") == "repeat_diagnostic_required":
        raise HTTPException(409,"Review prerequisites and use a fresh diagnostic form")
    updated=dict(session.responses or {});updated["__repair__"]={"complete":True,"tags":mastery.get("tags",[])};session.responses=updated;db.add(session);db.commit();return {"repair_complete":True,"reassessment_unlocked":True}


@router.get("/{lesson_id}/sessions/{session_id}/reassessment")
def get_reassessment(lesson_id:str,session_id:str,user:User|None=Depends(get_optional_user),db:Session=Depends(get_db)):
    _,reassessment,_,_=assessment_or_404(lesson_id)
    session=session_or_404(lesson_id,session_id,db,user)
    if not (session.responses or {}).get("__repair__",{}).get("complete"):raise HTTPException(409,"Complete targeted repair first")
    return {"lesson_id":lesson_id,"questions":[item.public() for item in reassessment]}


@router.post("/{lesson_id}/sessions/{session_id}/reassessment")
def submit_reassessment(lesson_id:str,session_id:str,payload:AssessmentSubmission,user:User|None=Depends(get_optional_user),db:Session=Depends(get_db)):
    _,reassessment,_,_=assessment_or_404(lesson_id)
    session=session_or_404(lesson_id,session_id,db,user)
    if not (session.responses or {}).get("__repair__",{}).get("complete"):raise HTTPException(409,"Complete targeted repair first")
    correct,reviewed,tags=_score_assessment(reassessment,payload.answers)
    mastery=(session.responses or {}).get("__mastery__",{})
    if lesson_id == "g8-algebraic-equations-10":
        essential={"distribution-error":"g8-ae-l10-r02","classification-error":"g8-ae-l10-r01","context-model-error":"g8-ae-l10-r03","fraction-structure-error":"g8-ae-l10-r03","inverse-direction":"g8-ae-l10-r01"}
        failed_ids={row["id"] for row in reviewed if not row["correct"]}
        repeated=any(essential.get(tag) in failed_ids for tag in mastery.get("tags",[]))
        ready=correct==3 and not repeated and mastery.get("correct",0)>=4 and (mastery.get("context_verified",False) or "g8-ae-l10-r03" not in failed_ids)
    else: ready=correct/3>=.8
    updated=dict(session.responses or {});updated["__reassessment__"]={"correct":correct,"ready":ready,"tags":tags};session.responses=updated;db.add(session);db.commit()
    return {"questions_correct":correct,"total_questions":3,"score":round(correct/3*100),"ready":ready,"readiness_decision":"ready" if ready else "more_repair_required","diagnosis":tags,"worked_review":reviewed}
