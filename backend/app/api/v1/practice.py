"""Compose practice routes in their established matching order.

Keep the historic registry and scorer imports available for existing callers.
"""

from fastapi import APIRouter

from app.api.v1.topic_diagnostics import router as diagnostics_router
from app.api.v1.practice_questions import router as questions_router
from app.api.v1.practice_assessments import router as assessments_router
from app.practice.assessment_catalog import ASSESSMENT_BANKS  # noqa: F401
from app.practice.assessment_scoring import _score_assessment  # noqa: F401

router = APIRouter()
router.include_router(diagnostics_router)
router.include_router(questions_router)
router.include_router(assessments_router)
