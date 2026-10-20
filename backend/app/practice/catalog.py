"""Grade-neutral server-authoritative practice catalogue."""

from app.curriculum.grade12.lessons.practice_catalog import PRACTICE_BANKS as GRADE12_BANKS
from app.curriculum.grade8.assessment import PRACTICE_BANK as GRADE8_LESSON1_PRACTICE
from app.curriculum.grade8.assessment_lesson2 import PRACTICE_BANK as GRADE8_LESSON2_PRACTICE
from app.curriculum.grade8.assessment_lesson3 import PRACTICE_BANK as GRADE8_LESSON3_PRACTICE
from app.curriculum.grade8.assessment_lesson4 import PRACTICE_BANK as GRADE8_LESSON4_PRACTICE
from app.curriculum.grade8.assessment_lesson5 import PRACTICE_BANK as GRADE8_LESSON5_PRACTICE
from app.curriculum.grade8.assessment_lesson6 import PRACTICE_BANK as GRADE8_LESSON6_PRACTICE
from app.curriculum.grade8.assessment_lesson7 import PRACTICE_BANK as GRADE8_LESSON7_PRACTICE
from app.curriculum.grade8.assessment_lesson8 import PRACTICE_BANK as GRADE8_LESSON8_PRACTICE

PRACTICE_BANKS = {
    **GRADE12_BANKS,
    "g8-algebraic-equations-01": GRADE8_LESSON1_PRACTICE,
    "g8-algebraic-equations-02": GRADE8_LESSON2_PRACTICE,
    "g8-algebraic-equations-03": GRADE8_LESSON3_PRACTICE,
    "g8-algebraic-equations-04": GRADE8_LESSON4_PRACTICE,
    "g8-algebraic-equations-05": GRADE8_LESSON5_PRACTICE,
    "g8-algebraic-equations-06": GRADE8_LESSON6_PRACTICE,
    "g8-algebraic-equations-07": GRADE8_LESSON7_PRACTICE,
    "g8-algebraic-equations-08": GRADE8_LESSON8_PRACTICE,
}
PRACTICE_BY_ID = {
    question.id: question
    for bank in PRACTICE_BANKS.values()
    for question in bank
}
