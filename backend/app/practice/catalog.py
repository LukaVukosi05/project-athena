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
from app.curriculum.grade8.assessment_functions_lesson5 import PRACTICE_BANK as GRADE8_FUNCTIONS_5_PRACTICE
from app.curriculum.grade8.assessment_functions_lesson6 import PRACTICE_BANK as GRADE8_FUNCTIONS_6_PRACTICE
from app.curriculum.grade8.assessment_graphs_lesson1 import PRACTICE_BANK as GRADE8_GRAPHS_1_PRACTICE
from app.curriculum.grade8.assessment_graphs_lesson2 import PRACTICE_BANK as GRADE8_GRAPHS_2_PRACTICE
from app.curriculum.grade8.assessment_graphs_lesson3 import PRACTICE_BANK as GRADE8_GRAPHS_3_PRACTICE
from app.curriculum.grade8.assessment_graphs_lesson4 import PRACTICE_BANK as GRADE8_GRAPHS_4_PRACTICE
from app.curriculum.grade8.assessment_graphs_lesson5 import PRACTICE_BANK as GRADE8_GRAPHS_5_PRACTICE
from app.curriculum.grade8.assessment_graphs_lesson6 import PRACTICE_BANK as GRADE8_GRAPHS_6_PRACTICE

from app.curriculum.grade8.assessment_patterns import PRACTICE_1 as PATTERNS_1_PRACTICE, PRACTICE_2 as PATTERNS_2_PRACTICE

from app.curriculum.grade8.assessment_patterns_34 import PRACTICE_3 as PATTERNS_3_PRACTICE, PRACTICE_4 as PATTERNS_4_PRACTICE
from app.curriculum.grade8.assessment_patterns_56 import PRACTICE_5 as PATTERNS_5_PRACTICE, PRACTICE_6 as PATTERNS_6_PRACTICE
from app.curriculum.grade8.assessment_whole_numbers import PRACTICE_1 as WHOLE_1_PRACTICE, PRACTICE_2 as WHOLE_2_PRACTICE
from app.curriculum.grade8.assessment_integers import PRACTICE_1 as INTEGER_1_PRACTICE, PRACTICE_2 as INTEGER_2_PRACTICE
from app.curriculum.grade8.assessment_integers_advanced import PRACTICE_3 as INTEGER_3_PRACTICE, PRACTICE_4 as INTEGER_4_PRACTICE
from app.curriculum.grade8.assessment_integers_reasoning import PRACTICE_5 as INTEGER_5_PRACTICE, PRACTICE_6 as INTEGER_6_PRACTICE
from app.curriculum.grade8.assessment_fractions import PRACTICE_1 as FRACTIONS_1_PRACTICE, PRACTICE_2 as FRACTIONS_2_PRACTICE
from app.curriculum.grade8.assessment_fractions_operations import PRACTICE_3 as FRACTIONS_3_PRACTICE, PRACTICE_4 as FRACTIONS_4_PRACTICE
from app.curriculum.grade8.assessment_fractions_56 import PRACTICE_5 as FRACTIONS_5_PRACTICE, PRACTICE_6 as FRACTIONS_6_PRACTICE
from app.curriculum.grade8.assessment_fractions_78 import PRACTICE_7 as FRACTIONS_7_PRACTICE, PRACTICE_8 as FRACTIONS_8_PRACTICE
from app.curriculum.grade8.assessment_decimals import PRACTICE_1 as DECIMALS_1_PRACTICE, PRACTICE_2 as DECIMALS_2_PRACTICE
from app.curriculum.grade8.assessment_decimals_operations import PRACTICE_3 as DECIMALS_3_PRACTICE, PRACTICE_4 as DECIMALS_4_PRACTICE
from app.curriculum.grade8.assessment_decimals_powers import PRACTICE_5 as DECIMALS_5_PRACTICE, PRACTICE_6 as DECIMALS_6_PRACTICE
from app.curriculum.grade8 import assessment_exponents
from app.curriculum.grade8.assessment_exponents import PRACTICE_1 as EXPONENT_1_PRACTICE, PRACTICE_2 as EXPONENT_2_PRACTICE

PRACTICE_BANKS = {
    "g8-patterns-03": PATTERNS_3_PRACTICE,
    "g8-patterns-04": PATTERNS_4_PRACTICE,
    "g8-patterns-05": PATTERNS_5_PRACTICE,
    "g8-patterns-06": PATTERNS_6_PRACTICE,
    "g8-whole-numbers-01": WHOLE_1_PRACTICE,
    "g8-whole-numbers-02": WHOLE_2_PRACTICE,
    "g8-integers-01": INTEGER_1_PRACTICE,
    "g8-integers-02": INTEGER_2_PRACTICE,
    "g8-integers-03": INTEGER_3_PRACTICE,
    "g8-integers-04": INTEGER_4_PRACTICE,
    "g8-integers-05": INTEGER_5_PRACTICE,
    "g8-integers-06": INTEGER_6_PRACTICE,
    "g8-common-fractions-01": FRACTIONS_1_PRACTICE,
    "g8-common-fractions-02": FRACTIONS_2_PRACTICE,
    "g8-common-fractions-03": FRACTIONS_3_PRACTICE,
    "g8-common-fractions-04": FRACTIONS_4_PRACTICE,
    "g8-common-fractions-05": FRACTIONS_5_PRACTICE,
    "g8-common-fractions-06": FRACTIONS_6_PRACTICE,
    "g8-common-fractions-07": FRACTIONS_7_PRACTICE,
    "g8-common-fractions-08": FRACTIONS_8_PRACTICE,
    "g8-decimal-fractions-01": DECIMALS_1_PRACTICE,
    "g8-decimal-fractions-02": DECIMALS_2_PRACTICE,
    "g8-decimal-fractions-03": DECIMALS_3_PRACTICE,
    "g8-decimal-fractions-04": DECIMALS_4_PRACTICE,
    "g8-decimal-fractions-05": DECIMALS_5_PRACTICE,
    "g8-decimal-fractions-06": DECIMALS_6_PRACTICE,
    "g8-exponents-01": EXPONENT_1_PRACTICE,
    "g8-exponents-02": EXPONENT_2_PRACTICE,
    "g8-exponents-03": assessment_exponents.PRACTICE_3,
    "g8-exponents-04": assessment_exponents.PRACTICE_4,
    "g8-exponents-05": assessment_exponents.PRACTICE_5,
    "g8-exponents-06": assessment_exponents.PRACTICE_6,
    "g8-patterns-01": PATTERNS_1_PRACTICE,
    "g8-patterns-02": PATTERNS_2_PRACTICE,
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
    "g8-functions-relationships-05": GRADE8_FUNCTIONS_5_PRACTICE,
    "g8-functions-relationships-06": GRADE8_FUNCTIONS_6_PRACTICE,
    "g8-graphs-01": GRADE8_GRAPHS_1_PRACTICE,
    "g8-graphs-02": GRADE8_GRAPHS_2_PRACTICE,
    "g8-graphs-03": GRADE8_GRAPHS_3_PRACTICE,
    "g8-graphs-04": GRADE8_GRAPHS_4_PRACTICE,
    "g8-graphs-05": GRADE8_GRAPHS_5_PRACTICE,
    "g8-graphs-06": GRADE8_GRAPHS_6_PRACTICE,
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
