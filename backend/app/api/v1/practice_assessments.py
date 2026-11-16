"""Mastery assessment, targeted repair and reassessment endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_optional_user
from app.db.database import get_db
from app.db.models.user import User


from app.practice.schemas import AssessmentSubmission
from app.practice.assessment_scoring import _score_assessment
from app.practice.session_store import assessment_or_404, session_or_404, save_response

router = APIRouter()


@router.get("/{lesson_id}/mastery")
def get_mastery(lesson_id: str):
    mastery, _, _, _ = assessment_or_404(lesson_id)
    return {
        "lesson_id": lesson_id,
        "mastery_threshold": 0.8,
        "questions": [item.public() for item in mastery],
    }


@router.post("/{lesson_id}/sessions/{session_id}/mastery")
def submit_mastery(
    lesson_id: str,
    session_id: str,
    payload: AssessmentSubmission,
    user: User | None = Depends(get_optional_user),
    db: Session = Depends(get_db),
):
    mastery, _, repairs, _ = assessment_or_404(lesson_id)
    session = session_or_404(lesson_id, session_id, db, user)
    correct, reviewed, tags = _score_assessment(mastery, payload.answers)
    context_verified = next(
        (row["correct"] for row in reviewed if row["id"] == "g8-ae-l10-m05"), True
    )
    earned_marks = sum(
        (question.marks or 0)
        for question, row in zip(mastery, reviewed)
        if row["correct"]
    )
    mastered = (
        earned_marks >= 16
        if lesson_id.startswith("g8-algebraic-expressions-")
        else correct >= 4
    ) and context_verified
    decision = (
        "ready"
        if mastered
        else (
            "repeat_diagnostic_required"
            if lesson_id == "g8-algebraic-equations-10" and correct <= 2
            else "targeted_repair_required"
        )
    )
    save_response(
        session,
        "__mastery__",
        {
            "correct": correct,
            "mastered": mastered,
            "tags": tags,
            "decision": decision,
            "context_verified": context_verified,
        },
        db,
    )
    score = (
        earned_marks * 5
        if lesson_id.startswith("g8-algebraic-expressions-")
        else correct * 20
    )
    return {
        "questions_correct": correct,
        "total_questions": 5,
        "score": score,
        "mastered": mastered,
        "readiness_decision": decision,
        "context_verified": context_verified,
        "diagnosis": tags,
        "worked_review": reviewed,
        "repair_routes": (
            []
            if mastered
            else [{"tag": tag, **repairs[tag]} for tag in tags if tag in repairs]
        ),
    }


@router.get("/{lesson_id}/sessions/{session_id}/repair")
def get_repair(
    lesson_id: str,
    session_id: str,
    user: User | None = Depends(get_optional_user),
    db: Session = Depends(get_db),
):
    _, _, repairs, rules = assessment_or_404(lesson_id)
    session = session_or_404(lesson_id, session_id, db, user)
    mastery = (session.responses or {}).get("__mastery__")
    if not mastery or mastery.get("mastered"):
        raise HTTPException(409, "Targeted repair is not required")
    tags = mastery.get("tags", [])
    return {
        "diagnosis": tags,
        "routes": [{"tag": tag, **repairs[tag]} for tag in tags if tag in repairs],
        "source_rules": rules,
    }


@router.post("/{lesson_id}/sessions/{session_id}/repair/complete")
def complete_repair(
    lesson_id: str,
    session_id: str,
    user: User | None = Depends(get_optional_user),
    db: Session = Depends(get_db),
):
    session = session_or_404(lesson_id, session_id, db, user)
    mastery = (session.responses or {}).get("__mastery__")
    if not mastery or mastery.get("mastered"):
        raise HTTPException(409, "Targeted repair is not required")
    if (
        lesson_id == "g8-algebraic-equations-10"
        and mastery.get("decision") == "repeat_diagnostic_required"
    ):
        raise HTTPException(409, "Review prerequisites and use a fresh diagnostic form")
    save_response(
        session, "__repair__", {"complete": True, "tags": mastery.get("tags", [])}, db
    )
    return {"repair_complete": True, "reassessment_unlocked": True}


@router.get("/{lesson_id}/sessions/{session_id}/reassessment")
def get_reassessment(
    lesson_id: str,
    session_id: str,
    user: User | None = Depends(get_optional_user),
    db: Session = Depends(get_db),
):
    _, reassessment, _, _ = assessment_or_404(lesson_id)
    session = session_or_404(lesson_id, session_id, db, user)
    if not (session.responses or {}).get("__repair__", {}).get("complete"):
        raise HTTPException(409, "Complete targeted repair first")
    return {
        "lesson_id": lesson_id,
        "questions": [item.public() for item in reassessment],
    }


@router.post("/{lesson_id}/sessions/{session_id}/reassessment")
def submit_reassessment(
    lesson_id: str,
    session_id: str,
    payload: AssessmentSubmission,
    user: User | None = Depends(get_optional_user),
    db: Session = Depends(get_db),
):
    _, reassessment, _, _ = assessment_or_404(lesson_id)
    session = session_or_404(lesson_id, session_id, db, user)
    if not (session.responses or {}).get("__repair__", {}).get("complete"):
        raise HTTPException(409, "Complete targeted repair first")
    correct, reviewed, tags = _score_assessment(reassessment, payload.answers)
    mastery = (session.responses or {}).get("__mastery__", {})
    if lesson_id == "g8-algebraic-equations-10":
        essential = {
            "distribution-error": "g8-ae-l10-r02",
            "classification-error": "g8-ae-l10-r01",
            "context-model-error": "g8-ae-l10-r03",
            "fraction-structure-error": "g8-ae-l10-r03",
            "inverse-direction": "g8-ae-l10-r01",
        }
        failed_ids = {row["id"] for row in reviewed if not row["correct"]}
        repeated = any(
            essential.get(tag) in failed_ids for tag in mastery.get("tags", [])
        )
        ready = (
            correct == 3
            and not repeated
            and mastery.get("correct", 0) >= 4
            and (
                mastery.get("context_verified", False)
                or "g8-ae-l10-r03" not in failed_ids
            )
        )
    else:
        ready = correct / 3 >= 0.8
    save_response(
        session,
        "__reassessment__",
        {"correct": correct, "ready": ready, "tags": tags},
        db,
    )
    return {
        "questions_correct": correct,
        "total_questions": 3,
        "score": round(correct / 3 * 100),
        "ready": ready,
        "readiness_decision": "ready" if ready else "more_repair_required",
        "diagnosis": tags,
        "worked_review": reviewed,
    }
