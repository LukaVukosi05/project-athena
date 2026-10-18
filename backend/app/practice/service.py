"""Answer checking and state transitions for self-guided practice."""
from fractions import Fraction
import re
from app.practice.catalog import PRACTICE_BY_ID
from app.practice.schemas import PracticeQuestion, PracticeState

def normalise(value: str, question: PracticeQuestion) -> str:
    result = str(value).strip().casefold().replace("−", "-").replace("–", "-")
    result = re.sub(r"\s+", " ", result)
    if question.type in {"numeric", "missing_term"}:
        result = result.replace("r", "").replace(",", "").strip()
    if question.lesson_id.startswith("g8-algebraic-equations-"):
        result = result.replace(" ", "")
    return {"arithmetic sequence":"arithmetic","geometric sequence":"geometric","quadratic pattern":"quadratic","quadratic sequence":"quadratic"}.get(result, result)

def equivalent(answer: str, accepted: str, question: PracticeQuestion) -> bool:
    left, right = normalise(answer, question), normalise(accepted, question)
    if left == right: return True
    if question.type in {"numeric", "missing_term"} or question.answer_normalisation.accept_fraction_decimal_equivalence:
        try: return Fraction(left) == Fraction(right)
        except (ValueError, ZeroDivisionError): return False
    return False

def check_answer(question_id: str, answer: str) -> bool:
    question = PRACTICE_BY_ID[question_id]
    return any(equivalent(answer, accepted, question) for accepted in question.accepted_answers)

def blank_response() -> dict:
    return {"state":PracticeState.UNANSWERED,"answer":"","attempts":0,"hints_used":0,"correct":False,"first_attempt_correct":False,"solution_viewed":False}

def public_status(response: dict, question: PracticeQuestion) -> dict:
    attempts, hints = int(response.get("attempts",0)), int(response.get("hints_used",0))
    correct = bool(response.get("correct")); solution_available = correct or attempts >= 2 or hints >= len(question.hints)
    return {"state":str(response.get("state",PracticeState.UNANSWERED)),"answer":response.get("answer",""),"attempts":attempts,"hints_used":hints,"correct":correct,"first_attempt_correct":bool(response.get("first_attempt_correct")),"solution_viewed":bool(response.get("solution_viewed")),"solution_available":solution_available,"next_enabled":correct or bool(response.get("solution_viewed"))}

def mastery_summary(responses: dict, questions: list[PracticeQuestion], threshold: float=.8) -> dict:
    statuses=[responses.get(q.id,blank_response()) for q in questions]
    correct=sum(bool(x.get("correct")) for x in statuses); first=sum(bool(x.get("first_attempt_correct")) for x in statuses); hints=sum(int(x.get("hints_used",0)) for x in statuses)
    solution_only=sum(bool(x.get("solution_viewed")) and not bool(x.get("correct")) for x in statuses)
    tags={}
    for question,status in zip(questions,statuses):
        if not status.get("correct") or status.get("attempts",0)>1:
            for tag in question.misconception_tags: tags[tag]=tags.get(tag,0)+1
    score=correct/len(questions) if questions else 0
    algebra=bool(questions) and all(q.lesson_id.startswith("g12-algebra-") for q in questions)
    exam_items_correct=all(bool(statuses[index-1].get("correct")) for index in (11,12)) if algebra and len(statuses)>=12 else True
    mastered=score>=threshold and exam_items_correct
    recommendation="Review the tagged teaching segment and retry the practice." if score<threshold else "Complete both exam-level items correctly before continuing." if not exam_items_correct else "You are ready for the explain-back checkpoint."
    return {"score":round(score*100),"questions_correct":correct,"total_questions":len(questions),"first_attempt_accuracy":round(first/len(questions)*100) if questions else 0,"hints_used":hints,"solution_viewed_without_success":solution_only,"misconception_areas":[k for k,_ in sorted(tags.items(),key=lambda x:(-x[1],x[0]))],"mastery_threshold":round(threshold*100),"exam_items_correct":exam_items_correct,"explain_back_required":algebra,"mastered":mastered,"recommended_review":recommendation}
