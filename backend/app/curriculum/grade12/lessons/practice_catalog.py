"""Single backend-authoritative practice catalogue for active Grade 12 lessons."""
from app.curriculum.grade12.lessons.functions_practice import PRACTICE_BANKS as FUNCTION_BANKS
from app.curriculum.grade12.lessons.finance_practice import PRACTICE_BANKS as FINANCE_BANKS
from app.curriculum.grade12.lessons.calculus_practice import PRACTICE_BANKS as CALCULUS_BANKS
from app.curriculum.grade12.lessons.algebra_practice import PRACTICE_BANKS as ALGEBRA_BANKS
from app.curriculum.grade12.lessons.sequences_practice_all import PRACTICE_BANKS as SEQUENCE_BANKS
from app.curriculum.grade12.lessons.paper2_topics import (
    ANALYTICAL_GEOMETRY_PRACTICE_BANKS, STATISTICS_PRACTICE_BANKS,
)

PRACTICE_BANKS = {**SEQUENCE_BANKS, **FUNCTION_BANKS, **FINANCE_BANKS,
                  **CALCULUS_BANKS, **ALGEBRA_BANKS,
                  **STATISTICS_PRACTICE_BANKS, **ANALYTICAL_GEOMETRY_PRACTICE_BANKS}
PRACTICE_BY_ID = {question.id: question for bank in PRACTICE_BANKS.values() for question in bank}
