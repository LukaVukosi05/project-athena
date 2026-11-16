"""Grade-neutral server-authoritative practice catalogue.

Register Grade 8–11 lessons in practice/banks/ once for practice and assessment.
Grade 12 retains its existing practice-only authoring contract.
"""

from app.curriculum.grade12.lessons.practice_catalog import (
    PRACTICE_BANKS as GRADE12_BANKS,
)
from app.practice.banks import LESSON_BANKS

PRACTICE_BANKS = {
    **{lesson_id: bank[0] for lesson_id, bank in LESSON_BANKS.items()},
    **GRADE12_BANKS,
}
PRACTICE_BY_ID = {
    question.id: question for bank in PRACTICE_BANKS.values() for question in bank
}
