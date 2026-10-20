"""Grade-neutral server-authoritative practice catalogue."""

from app.curriculum.grade12.lessons.practice_catalog import PRACTICE_BANKS as GRADE12_BANKS
from app.curriculum.grade8.assessment import PRACTICE_BANK as GRADE8_LESSON1_PRACTICE
from app.curriculum.grade8.assessment_lesson2 import PRACTICE_BANK as GRADE8_LESSON2_PRACTICE
from app.curriculum.grade8.assessment_lesson3 import PRACTICE_BANK as GRADE8_LESSON3_PRACTICE

PRACTICE_BANKS = {
    **GRADE12_BANKS,
    "g8-algebraic-equations-01": GRADE8_LESSON1_PRACTICE,
    "g8-algebraic-equations-02": GRADE8_LESSON2_PRACTICE,
    "g8-algebraic-equations-03": GRADE8_LESSON3_PRACTICE,
}
PRACTICE_BY_ID = {
    question.id: question
    for bank in PRACTICE_BANKS.values()
    for question in bank
}
