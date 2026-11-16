"""Practice questions, sessions, submission, hints and worked solutions."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_optional_user
from app.db.database import get_db
from app.db.models.user import User


from uuid import uuid4

from app.curriculum.repository import curriculum_repository
from app.db.models.progress import PracticeSession
from app.practice.catalog import PRACTICE_BY_ID
from app.practice.schemas import (
    PracticeAnswerRequest,
    PracticeBankResponse,
    PracticePublicQuestion,
    PracticeState,
)
from app.practice.service import (
    blank_response,
    check_answer,
    mastery_summary,
    public_status,
)
from app.practice.session_store import (
    bank_or_404,
    session_or_404,
    question_or_404,
    save_response,
)

router = APIRouter()


@router.get("/{lesson_id}", response_model=PracticeBankResponse)
def get_practice_bank(lesson_id: str):
    bank = bank_or_404(lesson_id)
    found = curriculum_repository.get_lesson(lesson_id)
    title = found[2].title if found else "Self-guided practice"
    return PracticeBankResponse(
        lesson_id=lesson_id,
        title="Self-guided practice",
        supporting_text=f"{title}: solve, submit, then compare your method.",
        mastery_threshold=0.8,
        questions=[
            PracticePublicQuestion(
                **q.model_dump(
                    include={
                        "id",
                        "question_number",
                        "difficulty",
                        "cognitive_level",
                        "marks",
                        "type",
                        "prompt",
                        "options",
                    }
                )
            )
            for q in bank
        ],
    )


@router.post("/{lesson_id}/sessions")
def start_practice(
    lesson_id: str,
    user: User | None = Depends(get_optional_user),
    db: Session = Depends(get_db),
):
    bank_or_404(lesson_id)
    session = PracticeSession(
        id=str(uuid4()),
        user_id=user.id if user else None,
        lesson_id=lesson_id,
        responses={},
    )
    db.add(session)
    db.commit()
    return {"session_id": session.id, "states": {}}


@router.get("/{lesson_id}/sessions/{session_id}")
def restore_practice(
    lesson_id: str,
    session_id: str,
    user: User | None = Depends(get_optional_user),
    db: Session = Depends(get_db),
):
    session = session_or_404(lesson_id, session_id, db, user)
    return {
        "session_id": session.id,
        "states": {
            qid: public_status(value, PRACTICE_BY_ID[qid])
            for qid, value in session.responses.items()
            if qid in PRACTICE_BY_ID
        },
    }


@router.post("/{lesson_id}/sessions/{session_id}/questions/{question_id}/submit")
def submit_answer(
    lesson_id: str,
    session_id: str,
    question_id: str,
    payload: PracticeAnswerRequest,
    user: User | None = Depends(get_optional_user),
    db: Session = Depends(get_db),
):
    session, question = session_or_404(
        lesson_id, session_id, db, user
    ), question_or_404(lesson_id, question_id)
    response = dict((session.responses or {}).get(question_id, blank_response()))
    response["state"] = PracticeState.CHECKING
    response["answer"] = payload.answer
    response["attempts"] = int(response.get("attempts", 0)) + 1
    correct = check_answer(question_id, payload.answer)
    response["correct"] = correct
    if correct:
        response["first_attempt_correct"] = response["attempts"] == 1
        response["state"] = PracticeState.CORRECT
        feedback = question.correct_feedback
    else:
        response["state"] = (
            PracticeState.INCORRECT_FIRST_ATTEMPT
            if response["attempts"] == 1
            else PracticeState.INCORRECT_RETRY
        )
        feedback = "Not quite yet."
    save_response(session, question_id, response, db)
    return {**public_status(response, question), "feedback": feedback}


@router.post("/{lesson_id}/sessions/{session_id}/questions/{question_id}/hint")
def request_hint(
    lesson_id: str,
    session_id: str,
    question_id: str,
    hint_index: int | None = None,
    user: User | None = Depends(get_optional_user),
    db: Session = Depends(get_db),
):
    session, question = session_or_404(
        lesson_id, session_id, db, user
    ), question_or_404(lesson_id, question_id)
    response = dict((session.responses or {}).get(question_id, blank_response()))
    index = int(response.get("hints_used", 0)) if hint_index is None else hint_index
    if index < 0 or index >= len(question.hints):
        raise HTTPException(409, "No further hints are available")
    response["hints_used"] = max(int(response.get("hints_used", 0)), index + 1)
    if response["hints_used"] >= len(question.hints) and not response.get("correct"):
        response["state"] = PracticeState.SOLUTION_AVAILABLE
    save_response(session, question_id, response, db)
    return {
        **public_status(response, question),
        "hint": question.hints[index],
        "hint_index": index,
        "hint_count": len(question.hints),
        "hints_remaining": len(question.hints) - index - 1,
        "hint_complete": index == len(question.hints) - 1,
    }


@router.get("/{lesson_id}/sessions/{session_id}/questions/{question_id}/solution")
def get_solution(
    lesson_id: str,
    session_id: str,
    question_id: str,
    user: User | None = Depends(get_optional_user),
    db: Session = Depends(get_db),
):
    session, question = session_or_404(
        lesson_id, session_id, db, user
    ), question_or_404(lesson_id, question_id)
    response = dict((session.responses or {}).get(question_id, blank_response()))
    status = public_status(response, question)
    if not status["solution_available"]:
        raise HTTPException(403, "Worked solution is not available yet")
    response["solution_viewed"] = True
    response["state"] = (
        PracticeState.COMPLETE
        if response.get("correct")
        else PracticeState.SOLUTION_VIEWED
    )
    save_response(session, question_id, response, db)
    return {
        **public_status(response, question),
        "worked_solution": [item.model_dump() for item in question.worked_solution],
        "verification": question.verification,
    }


@router.get("/{lesson_id}/sessions/{session_id}/summary")
def get_summary(
    lesson_id: str,
    session_id: str,
    user: User | None = Depends(get_optional_user),
    db: Session = Depends(get_db),
):
    return mastery_summary(
        session_or_404(lesson_id, session_id, db, user).responses or {},
        bank_or_404(lesson_id),
        0.8,
    )
