"""Shared bank lookups, practice-session ownership and response persistence."""

from uuid import UUID

from fastapi import HTTPException

from app.db.models.progress import PracticeSession
from app.practice.catalog import PRACTICE_BANKS, PRACTICE_BY_ID
from app.practice.assessment_catalog import ASSESSMENT_BANKS


def assessment_or_404(lesson_id):
    result = ASSESSMENT_BANKS.get(lesson_id)
    if result is None:
        raise HTTPException(404, "Mastery bank not found")
    return result


def bank_or_404(lesson_id):
    bank = PRACTICE_BANKS.get(lesson_id)
    if bank is None:
        raise HTTPException(404, "Practice bank not found")
    return bank


def session_or_404(lesson_id, session_id, db, user=None):
    try:
        UUID(session_id)
    except ValueError as error:
        raise HTTPException(404, "Practice session not found") from error
    result = db.get(PracticeSession, session_id)
    if result is None or result.lesson_id != lesson_id:
        raise HTTPException(404, "Practice session not found")
    if result.user_id is not None and (user is None or result.user_id != user.id):
        raise HTTPException(404, "Practice session not found")
    return result


def question_or_404(lesson_id, question_id):
    question = PRACTICE_BY_ID.get(question_id)
    if question is None or question.lesson_id != lesson_id:
        raise HTTPException(404, "Practice question not found")
    return question


def save_response(session, question_id, response, db):
    updated = dict(session.responses or {})
    updated[question_id] = response
    session.responses = updated
    db.add(session)
    db.commit()
