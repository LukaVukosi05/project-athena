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
from app.curriculum.grade8.assessment_lesson9 import PRACTICE_BANK as GRADE8_LESSON9_PRACTICE
from app.curriculum.grade8.assessment_lesson10 import PRACTICE_BANK as GRADE8_LESSON10_PRACTICE
from app.curriculum.grade8.assessment_expressions import PRACTICE_BANK as GRADE8_EXPRESSIONS_PRACTICE
from app.curriculum.grade8.assessment_expressions_lesson2 import PRACTICE_BANK as GRADE8_EXPRESSIONS_2_PRACTICE
from app.curriculum.grade8.assessment_expressions_lesson3 import PRACTICE_BANK as GRADE8_EXPRESSIONS_3_PRACTICE
from app.curriculum.grade8.assessment_expressions_lesson4 import PRACTICE_BANK as GRADE8_EXPRESSIONS_4_PRACTICE
from app.curriculum.grade8.assessment_expressions_lesson5 import PRACTICE_BANK as GRADE8_EXPRESSIONS_5_PRACTICE
from app.curriculum.grade8.assessment_expressions_lesson6 import PRACTICE_BANK as GRADE8_EXPRESSIONS_6_PRACTICE
from app.curriculum.grade8.assessment_expressions_lesson7 import PRACTICE_BANK as GRADE8_EXPRESSIONS_7_PRACTICE
from app.curriculum.grade8.assessment_expressions_lesson8 import PRACTICE_BANK as GRADE8_EXPRESSIONS_8_PRACTICE
from app.curriculum.grade8.assessment_expressions_lesson9 import PRACTICE_BANK as GRADE8_EXPRESSIONS_9_PRACTICE
from app.curriculum.grade8.assessment_expressions_lesson10 import PRACTICE_BANK as GRADE8_EXPRESSIONS_10_PRACTICE
from app.curriculum.grade8.assessment_functions_lesson1 import PRACTICE_BANK as GRADE8_FUNCTIONS_1_PRACTICE
from app.curriculum.grade8.assessment_functions_lesson2 import PRACTICE_BANK as GRADE8_FUNCTIONS_2_PRACTICE
from app.curriculum.grade8.assessment_functions_lesson3 import PRACTICE_BANK as GRADE8_FUNCTIONS_3_PRACTICE
from app.curriculum.grade8.assessment_functions_lesson4 import PRACTICE_BANK as GRADE8_FUNCTIONS_4_PRACTICE
from app.curriculum.grade8.assessment_graphs_lesson1 import PRACTICE_BANK as GRADE8_GRAPHS_1_PRACTICE

PRACTICE_BANKS = {
    "g8-algebraic-expressions-01": GRADE8_EXPRESSIONS_PRACTICE,
    "g8-algebraic-expressions-02": GRADE8_EXPRESSIONS_2_PRACTICE,
    "g8-algebraic-expressions-03": GRADE8_EXPRESSIONS_3_PRACTICE,
    "g8-algebraic-expressions-04": GRADE8_EXPRESSIONS_4_PRACTICE,
    "g8-algebraic-expressions-05": GRADE8_EXPRESSIONS_5_PRACTICE,
    "g8-algebraic-expressions-06": GRADE8_EXPRESSIONS_6_PRACTICE,
    "g8-algebraic-expressions-07": GRADE8_EXPRESSIONS_7_PRACTICE,
    "g8-algebraic-expressions-08": GRADE8_EXPRESSIONS_8_PRACTICE,
    "g8-algebraic-expressions-09": GRADE8_EXPRESSIONS_9_PRACTICE,
    "g8-algebraic-expressions-10": GRADE8_EXPRESSIONS_10_PRACTICE,
    "g8-functions-relationships-01": GRADE8_FUNCTIONS_1_PRACTICE,
    "g8-functions-relationships-02": GRADE8_FUNCTIONS_2_PRACTICE,
    "g8-functions-relationships-03": GRADE8_FUNCTIONS_3_PRACTICE,
    "g8-functions-relationships-04": GRADE8_FUNCTIONS_4_PRACTICE,
    "g8-graphs-01": GRADE8_GRAPHS_1_PRACTICE,
    **GRADE12_BANKS,
    "g8-algebraic-equations-01": GRADE8_LESSON1_PRACTICE,
    "g8-algebraic-equations-02": GRADE8_LESSON2_PRACTICE,
    "g8-algebraic-equations-03": GRADE8_LESSON3_PRACTICE,
    "g8-algebraic-equations-04": GRADE8_LESSON4_PRACTICE,
    "g8-algebraic-equations-05": GRADE8_LESSON5_PRACTICE,
    "g8-algebraic-equations-06": GRADE8_LESSON6_PRACTICE,
    "g8-algebraic-equations-07": GRADE8_LESSON7_PRACTICE,
    "g8-algebraic-equations-08": GRADE8_LESSON8_PRACTICE,
    "g8-algebraic-equations-09": GRADE8_LESSON9_PRACTICE,
    "g8-algebraic-equations-10": GRADE8_LESSON10_PRACTICE,
}
PRACTICE_BY_ID = {
    question.id: question
    for bank in PRACTICE_BANKS.values()
    for question in bank
}
