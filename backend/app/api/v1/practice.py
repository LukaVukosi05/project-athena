"""Server-authoritative self-guided practice endpoints for the lesson schedule."""
from uuid import UUID,uuid4
from pydantic import BaseModel,Field
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
from app.curriculum.grade8 import assessment_functions_lesson1, assessment_functions_lesson2, assessment_functions_lesson3
from app.curriculum.grade8 import assessment_functions_lesson4, assessment_functions_lesson5, assessment_functions_lesson6
from app.curriculum.grade8.functions_topic_diagnostic import public_items as topic3_items, score as topic3_score
from app.curriculum.grade8 import assessment_patterns, assessment_patterns_34, assessment_patterns_56, assessment_whole_numbers, assessment_integers, assessment_integers_advanced, assessment_integers_reasoning, assessment_fractions, assessment_fractions_operations, assessment_fractions_56, assessment_fractions_78, assessment_decimals, assessment_decimals_operations, assessment_decimals_powers, assessment_exponents
from app.curriculum.grade8 import assessment_straight_lines, assessment_shapes, assessment_pythagoras
from app.curriculum.grade8 import assessment_straight_lines_chain
from app.curriculum.grade9 import assessment_whole_numbers as grade9_whole
from app.curriculum.grade10.assessment import ALGEBRA_BANKS as GRADE10_ALGEBRA_BANKS, EEI_BANKS as GRADE10_EEI_BANKS, TRIG_BANKS as GRADE10_TRIG_BANKS, EUC_BANKS as GRADE10_EUC_BANKS, AG_BANKS as GRADE10_AG_BANKS, FN_BANKS as GRADE10_FN_BANKS, STAT_BANKS as GRADE10_STAT_BANKS, PROB_BANKS as GRADE10_PROB_BANKS
from app.curriculum.grade8 import assessment_graphs_lesson1, assessment_graphs_lesson2, assessment_graphs_lesson3, assessment_graphs_lesson4, assessment_graphs_lesson5, assessment_graphs_lesson6
from app.curriculum.grade8 import assessment_expressions, assessment_expressions_lesson2, assessment_expressions_lesson3, assessment_expressions_lesson4, assessment_expressions_lesson5, assessment_expressions_lesson6, assessment_expressions_lesson7, assessment_expressions_lesson8, assessment_expressions_lesson9, assessment_expressions_lesson10

ASSESSMENT_BANKS={
    **{f"g10-fn-{number:02}":GRADE10_FN_BANKS[number][1:] for number in range(1,8)},
    **{f"g10-stat-{number:02}":GRADE10_STAT_BANKS[number][1:] for number in range(1,7)},
    **{f"g10-prob-{number:02}":GRADE10_PROB_BANKS[number][1:] for number in range(1,6)},
    **{f"g10-ag-{number:02}":GRADE10_AG_BANKS[number][1:] for number in range(1,7)},
    **{f"g10-euc-{number:02}":GRADE10_EUC_BANKS[number][1:] for number in range(1,7)},
    **{f"g10-trig-{number:02}":GRADE10_TRIG_BANKS[number][1:] for number in range(1,8)},
    **{f"g10-eei-{number:02}":GRADE10_EEI_BANKS[number][1:] for number in range(1,10)},
    **{f"g10-algebra-{number:02}":GRADE10_ALGEBRA_BANKS[number][1:] for number in range(1,7)},
    "g9-whole-numbers-01": (grade9_whole.MASTERY_1,grade9_whole.REASSESSMENT_1,grade9_whole.REPAIRS_1,grade9_whole.RULES_1),
    "g9-whole-numbers-02": (grade9_whole.MASTERY_2,grade9_whole.REASSESSMENT_2,grade9_whole.REPAIRS_2,grade9_whole.RULES_2),
    **{f"g9-whole-numbers-{number:02}":grade9_whole.EXTENDED_BANKS[number][1:] for number in range(3,9)},
    **{f"g9-integers-{number:02}":grade9_whole.INTEGER_BANKS[number][1:] for number in range(1,6)},
    **{f"g9-exponents-{number:02}":grade9_whole.EXPONENT_BANKS[number][1:] for number in range(1,7)},
    **{f"g9-patterns-{number:02}":grade9_whole.PATTERN_BANKS[number][1:] for number in range(1,6)},
    **{f"g9-functions-{number:02}":grade9_whole.FUNCTION_BANKS[number][1:] for number in range(1,6)},
    **{f"g9-expressions-{number:02}":grade9_whole.EXPRESSION_BANKS[number][1:] for number in range(1,10)},
    **{f"g9-equations-{number:02}":grade9_whole.EQUATION_BANKS[number][1:] for number in range(1,7)},
    **{f"g9-graphs-{number:02}":grade9_whole.GRAPH_BANKS[number][1:] for number in range(1,8)},
    **{f"g9-straight-lines-{number:02}":grade9_whole.LINE_BANKS[number][1:] for number in range(1,6)},
    **{f"g9-shapes-{number:02}":grade9_whole.SHAPE_BANKS[number][1:] for number in range(1,9)},
    **{f"g9-area-{number:02}":grade9_whole.AREA_BANKS[number][1:] for number in range(1,6)},
    **{f"g9-data-{number:02}":grade9_whole.DATA_BANKS[number][1:] for number in range(1,9)},
    **{f"g9-prob-{number:02}":grade9_whole.PROB_BANKS[number][1:] for number in range(1,6)},
    **{f"g9-solid-{number:02}":grade9_whole.SOLID_BANKS[number][1:] for number in range(1,5)},
    **{f"g9-tg-{number:02}":grade9_whole.TRANSFORM_BANKS[number][1:] for number in range(1,8)},
    **{f"g9-sv-{number:02}":grade9_whole.SURFACE_BANKS[number][1:] for number in range(1,7)},
    **{f"g8-pythagoras-{n:02}": assessment_pythagoras.banks(n)[1:] for n in range(1,6)},
    **{f"g8-shapes-{n:02}": assessment_shapes.banks(n)[1:] for n in range(1,6)},
    **{f"g8-straight-lines-{n:02}": assessment_straight_lines.banks(n)[1:] for n in (1,2)},
    **{f"g8-straight-lines-{n:02}": assessment_straight_lines_chain.banks(n)[1:] for n in (3,4,5)},
    **{f"g8-patterns-{n:02}": assessment_patterns_34.banks(n)[1:] for n in (3,4)},
    **{f"g8-patterns-{n:02}": assessment_patterns_56.banks(n)[1:] for n in (5,6)},
    **{f"g8-whole-numbers-{n:02}": assessment_whole_numbers.banks(n)[1:] for n in (1,2)},
    **{f"g8-integers-{n:02}": assessment_integers.banks(n)[1:] for n in (1,2)},
    **{f"g8-integers-{n:02}": assessment_integers_advanced.banks(n)[1:] for n in (3,4)},
    **{f"g8-integers-{n:02}": assessment_integers_reasoning.banks(n)[1:] for n in (5,6)},
    **{f"g8-common-fractions-{n:02}": assessment_fractions.banks(n)[1:] for n in (1,2)},
    **{f"g8-common-fractions-{n:02}": assessment_fractions_operations.banks(n)[1:] for n in (3,4)},
    **{f"g8-common-fractions-{n:02}": assessment_fractions_56.banks(n)[1:] for n in (5,6)},
    **{f"g8-common-fractions-{n:02}": assessment_fractions_78.banks(n)[1:] for n in (7,8)},
    **{f"g8-decimal-fractions-{n:02}": assessment_decimals.banks(n)[1:] for n in (1,2)},
    **{f"g8-decimal-fractions-{n:02}": assessment_decimals_operations.banks(n)[1:] for n in (3,4)},
    **{f"g8-decimal-fractions-{n:02}": assessment_decimals_powers.banks(n)[1:] for n in (5,6)},
    **{f"g8-exponents-{n:02}": assessment_exponents.banks(n)[1:] for n in (1,2,3,4,5,6)},
    **{f"g8-patterns-{n:02}": (bank[1],bank[2],bank[3],{"pattern-rule-from-too-few-terms":"Retry a new pattern with changed starting values."})
       for n,bank in ((1,assessment_patterns.banks(1)),(2,assessment_patterns.banks(2)))},
    **{f"g8-graphs-{n:02}":(bank.MASTERY_BANK,bank.REASSESSMENT_BANK,bank.MISCONCEPTION_REPAIRS,bank.REPAIR_RULES) for n,bank in ((3,assessment_graphs_lesson3),(4,assessment_graphs_lesson4),(5,assessment_graphs_lesson5),(6,assessment_graphs_lesson6))},
    **{f"g8-functions-relationships-{n:02}":(bank.MASTERY_BANK,bank.REASSESSMENT_BANK,bank.MISCONCEPTION_REPAIRS,bank.REPAIR_RULES) for n,bank in ((5,assessment_functions_lesson5),(6,assessment_functions_lesson6))},
    "g8-functions-relationships-04":(assessment_functions_lesson4.MASTERY_BANK, assessment_functions_lesson4.REASSESSMENT_BANK,
                                     assessment_functions_lesson4.MISCONCEPTION_REPAIRS, assessment_functions_lesson4.REPAIR_RULES),
    "g8-graphs-01":(assessment_graphs_lesson1.MASTERY_BANK, assessment_graphs_lesson1.REASSESSMENT_BANK,
                    assessment_graphs_lesson1.MISCONCEPTION_REPAIRS, assessment_graphs_lesson1.REPAIR_RULES),
    "g8-graphs-02":(assessment_graphs_lesson2.MASTERY_BANK, assessment_graphs_lesson2.REASSESSMENT_BANK,
                    assessment_graphs_lesson2.MISCONCEPTION_REPAIRS, assessment_graphs_lesson2.REPAIR_RULES),
    "g8-algebraic-expressions-01":(assessment_expressions.MASTERY_BANK, assessment_expressions.REASSESSMENT_BANK,
                                    assessment_expressions.MISCONCEPTION_REPAIRS, assessment_expressions.REPAIR_RULES),
    "g8-algebraic-expressions-02":(assessment_expressions_lesson2.MASTERY_BANK, assessment_expressions_lesson2.REASSESSMENT_BANK,
                                    assessment_expressions_lesson2.MISCONCEPTION_REPAIRS, assessment_expressions_lesson2.REPAIR_RULES),
    "g8-algebraic-expressions-03":(assessment_expressions_lesson3.MASTERY_BANK, assessment_expressions_lesson3.REASSESSMENT_BANK,
                                    assessment_expressions_lesson3.MISCONCEPTION_REPAIRS, assessment_expressions_lesson3.REPAIR_RULES),
    "g8-algebraic-expressions-04":(assessment_expressions_lesson4.MASTERY_BANK, assessment_expressions_lesson4.REASSESSMENT_BANK,
                                    assessment_expressions_lesson4.MISCONCEPTION_REPAIRS, assessment_expressions_lesson4.REPAIR_RULES),
    "g8-algebraic-expressions-05":(assessment_expressions_lesson5.MASTERY_BANK, assessment_expressions_lesson5.REASSESSMENT_BANK,
                                    assessment_expressions_lesson5.MISCONCEPTION_REPAIRS, assessment_expressions_lesson5.REPAIR_RULES),
    "g8-algebraic-expressions-06":(assessment_expressions_lesson6.MASTERY_BANK, assessment_expressions_lesson6.REASSESSMENT_BANK,
                                    assessment_expressions_lesson6.MISCONCEPTION_REPAIRS, assessment_expressions_lesson6.REPAIR_RULES),
    "g8-algebraic-expressions-07":(assessment_expressions_lesson7.MASTERY_BANK, assessment_expressions_lesson7.REASSESSMENT_BANK,
                                    assessment_expressions_lesson7.MISCONCEPTION_REPAIRS, assessment_expressions_lesson7.REPAIR_RULES),
    "g8-algebraic-expressions-08":(assessment_expressions_lesson8.MASTERY_BANK, assessment_expressions_lesson8.REASSESSMENT_BANK,
                                    assessment_expressions_lesson8.MISCONCEPTION_REPAIRS, assessment_expressions_lesson8.REPAIR_RULES),
    "g8-algebraic-expressions-09":(assessment_expressions_lesson9.MASTERY_BANK, assessment_expressions_lesson9.REASSESSMENT_BANK,
                                    assessment_expressions_lesson9.MISCONCEPTION_REPAIRS, assessment_expressions_lesson9.REPAIR_RULES),
    "g8-algebraic-expressions-10":(assessment_expressions_lesson10.MASTERY_BANK, assessment_expressions_lesson10.REASSESSMENT_BANK,
                                    assessment_expressions_lesson10.MISCONCEPTION_REPAIRS, assessment_expressions_lesson10.REPAIR_RULES),
    "g8-functions-relationships-01":(assessment_functions_lesson1.MASTERY_BANK, assessment_functions_lesson1.REASSESSMENT_BANK,
                                    assessment_functions_lesson1.MISCONCEPTION_REPAIRS, assessment_functions_lesson1.REPAIR_RULES),
    "g8-functions-relationships-02":(assessment_functions_lesson2.MASTERY_BANK, assessment_functions_lesson2.REASSESSMENT_BANK,
                                    assessment_functions_lesson2.MISCONCEPTION_REPAIRS, assessment_functions_lesson2.REPAIR_RULES),
    "g8-functions-relationships-03":(assessment_functions_lesson3.MASTERY_BANK, assessment_functions_lesson3.REASSESSMENT_BANK,
                                    assessment_functions_lesson3.MISCONCEPTION_REPAIRS, assessment_functions_lesson3.REPAIR_RULES),
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
@router.get("/topics/grade-8/functions-relationships/diagnostic")
def get_functions_topic_diagnostic():
    return {"topic_id": "functions-relationships", "questions": topic3_items(),
            "note": "This short check recommends where to revise; it does not replace lesson mastery."}

class TopicDiagnosticSubmission(BaseModel):
    answers: dict[str,str] = Field(min_length=18,max_length=18)

@router.post("/topics/grade-8/functions-relationships/diagnostic")
def submit_functions_topic_diagnostic(payload: TopicDiagnosticSubmission):
    try:
        return topic3_score(payload.answers)
    except ValueError as error:
        raise HTTPException(422, str(error)) from error

class Grade8TopicCheckSubmission(BaseModel):
    answers: dict[str,str]

def _grade8_topic_check(topic_id: str):
    topic=curriculum_repository.get_topic("grade-8",topic_id)
    if topic is None:raise HTTPException(404,"Grade 8 topic not found")
    lessons=[lesson for subtopic in topic.subtopics for lesson in subtopic.lessons]
    if not lessons or any(lesson.id not in ASSESSMENT_BANKS for lesson in lessons):
        raise HTTPException(409,"A topic check is not available for every lesson")
    # These are existing, reviewed lesson items. This is a revision check, not a
    # fresh parallel reassessment or a replacement for each lesson's mastery.
    return [(lesson,list(ASSESSMENT_BANKS[lesson.id][0][:2])) for lesson in lessons]

@router.get("/topics/grade-8/{topic_id}/diagnostic")
def get_grade8_topic_check(topic_id: str):
    groups=_grade8_topic_check(topic_id)
    return {"topic_id":topic_id,"questions":[item.public() for _,bank in groups for item in bank],
            "note":"Revision check using existing lesson questions. Complete each lesson mastery assessment separately."}

@router.post("/topics/grade-8/{topic_id}/diagnostic")
def submit_grade8_topic_check(topic_id: str,payload: Grade8TopicCheckSubmission):
    groups=_grade8_topic_check(topic_id)
    expected={item.id for _,bank in groups for item in bank}
    if set(payload.answers)!=expected:raise HTTPException(422,"Submit exactly one answer for every question in this topic check")
    if any(not isinstance(value,str) or not 0<len(value.strip())<=1000 for value in payload.answers.values()):
        raise HTTPException(422,"Every answer must contain 1 to 1000 characters")
    areas=[];review=[]
    for lesson,bank in groups:
        correct,rows,_=_score_assessment(bank,{item.id:payload.answers[item.id] for item in bank})
        areas.append({"lesson_id":lesson.id,"title":lesson.title,"correct":correct,
                      "total":len(bank),"needs_review":correct<len(bank)})
        review.extend({"id":row["id"],"lesson_id":lesson.id,"correct":row["correct"],
                       "answer":row["answer"],"explanation":" ".join(row["solution"])} for row in rows)
    return {"score":sum(area["correct"] for area in areas),"total":len(expected),"areas":areas,
            "recommended_lesson_id":next((area["lesson_id"] for area in areas if area["needs_review"]),None),
            "review":review,"note":"This check directs revision; it does not certify topic mastery. Complete each lesson mastery and any required repair and reassessment."}

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
    mastered=(earned_marks >= 16 if lesson_id.startswith('g8-algebraic-expressions-') else correct>=4) and context_verified
    decision=("ready" if mastered else "repeat_diagnostic_required" if lesson_id == "g8-algebraic-equations-10" and correct<=2 else "targeted_repair_required")
    updated=dict(session.responses or {});updated["__mastery__"]={"correct":correct,"mastered":mastered,"tags":tags,"decision":decision,"context_verified":context_verified};session.responses=updated;db.add(session);db.commit()
    score=(earned_marks * 5 if lesson_id.startswith('g8-algebraic-expressions-') else correct*20)
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
