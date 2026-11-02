"""Grade 8 Algebraic Equations catalogue from the approved Gold Pack v1.0."""

from app.curriculum.schemas import (
    AccessLevel, ContentStatus, GradeCurriculum, Lesson, LessonBlock, Subtopic, Topic,
)
from app.curriculum.grade8.lesson1_runtime import LESSON_1
from app.curriculum.grade8.lesson2_runtime import LESSON_2
from app.curriculum.grade8.lesson3_runtime import LESSON_3
from app.curriculum.grade8.lesson4_runtime import LESSON_4
from app.curriculum.grade8.lesson5_runtime import LESSON_5
from app.curriculum.grade8.lesson6_runtime import LESSON_6
from app.curriculum.grade8.lesson7_runtime import LESSON_7
from app.curriculum.grade8.lesson8_runtime import LESSON_8
from app.curriculum.grade8.lesson9_runtime import LESSON_9
from app.curriculum.grade8.lesson10_runtime import LESSON_10
from app.curriculum.grade8.algebraic_expressions import LESSON as EXPRESSIONS_LESSON
from app.curriculum.grade8.algebraic_expressions_lesson2 import LESSON as EXPRESSIONS_LESSON_2
from app.curriculum.grade8.algebraic_expressions_lesson3 import LESSON as EXPRESSIONS_LESSON_3
from app.curriculum.grade8.algebraic_expressions_lesson4 import LESSON as EXPRESSIONS_LESSON_4
from app.curriculum.grade8.algebraic_expressions_lesson5 import LESSON as EXPRESSIONS_LESSON_5
from app.curriculum.grade8.algebraic_expressions_lesson6 import LESSON as EXPRESSIONS_LESSON_6
from app.curriculum.grade8.algebraic_expressions_lesson7 import LESSON as EXPRESSIONS_LESSON_7
from app.curriculum.grade8.algebraic_expressions_lesson8 import LESSON as EXPRESSIONS_LESSON_8
from app.curriculum.grade8.algebraic_expressions_lesson9 import LESSON as EXPRESSIONS_LESSON_9
from app.curriculum.grade8.algebraic_expressions_lesson10 import LESSON as EXPRESSIONS_LESSON_10
from app.curriculum.grade8.functions_relationships_lesson1 import LESSON as FUNCTIONS_LESSON_1
from app.curriculum.grade8.functions_relationships_lesson2 import LESSON as FUNCTIONS_LESSON_2
from app.curriculum.grade8.functions_relationships_lesson3 import LESSON as FUNCTIONS_LESSON_3
from app.curriculum.grade8.functions_relationships_lesson4 import LESSON as FUNCTIONS_LESSON_4
from app.curriculum.grade8.functions_relationships_lesson5 import LESSON as FUNCTIONS_LESSON_5
from app.curriculum.grade8.functions_relationships_lesson6 import LESSON as FUNCTIONS_LESSON_6
from app.curriculum.grade8.graphs_lesson1 import LESSON as GRAPHS_LESSON_1
from app.curriculum.grade8.graphs_lesson2 import LESSON as GRAPHS_LESSON_2
from app.curriculum.grade8.graphs_lesson3 import LESSON as GRAPHS_LESSON_3
from app.curriculum.grade8.graphs_lesson4 import LESSON as GRAPHS_LESSON_4
from app.curriculum.grade8.graphs_lesson5 import LESSON as GRAPHS_LESSON_5
from app.curriculum.grade8.graphs_lesson6 import LESSON as GRAPHS_LESSON_6

from app.curriculum.grade8.patterns_runtime import LESSON_1 as PATTERNS_LESSON_1, LESSON_2 as PATTERNS_LESSON_2, LESSON_3 as PATTERNS_LESSON_3, LESSON_4 as PATTERNS_LESSON_4, LESSON_5 as PATTERNS_LESSON_5, LESSON_6 as PATTERNS_LESSON_6

from app.curriculum.grade8.whole_numbers_runtime import LESSON_1 as WHOLE_LESSON_1, LESSON_2 as WHOLE_LESSON_2

from app.curriculum.grade8.integers_runtime import LESSON_1 as INTEGER_LESSON_1, LESSON_2 as INTEGER_LESSON_2
from app.curriculum.grade8.fractions_runtime import LESSON_1 as FRACTIONS_LESSON_1, LESSON_2 as FRACTIONS_LESSON_2, LESSON_3 as FRACTIONS_LESSON_3, LESSON_4 as FRACTIONS_LESSON_4, LESSON_5 as FRACTIONS_LESSON_5, LESSON_6 as FRACTIONS_LESSON_6, LESSON_7 as FRACTIONS_LESSON_7, LESSON_8 as FRACTIONS_LESSON_8
from app.curriculum.grade8.integers_advanced_runtime import LESSON_3 as INTEGER_LESSON_3, LESSON_4 as INTEGER_LESSON_4, LESSON_5 as INTEGER_LESSON_5, LESSON_6 as INTEGER_LESSON_6

SOURCE = "Project_Athena_Grade8_Algebraic_Equations_Gold_Pack_v1_0.docx"
SOURCE_SHA256 = "69b97ae1d9f85d0f9fb41aad170f6cbc777f2e39844dd6b8d6235bee6c093574"

LESSON_METADATA = (
    ("g8-algebraic-equations-01", "Meaning of equality", 55,
     "Interpret the equals sign as a statement that two expressions have the same value, preserve equality by applying the same legal operation to both sides, and verify a proposed solution by substitution.",
     "Every later equation method depends on equality. Learners who read the equals sign as an instruction to calculate often change only one side or move terms without understanding why the equation remains true.",
     "The equals sign means has the same value as. Equivalent equations preserve that equality by applying the same legal operation to both complete sides."),
    ("g8-algebraic-equations-02", "Equations by inspection", 60,
     "Solve simple and structured equations by inspecting number relationships, test candidate values efficiently, and explain why the selected value makes the original equation true.",
     "Inspection builds number sense before formal equation procedures and replaces unsupported guessing with inverse-operation evidence.",
     "Inspection uses a known number fact or inverse operation, followed by substitution into the original equation."),
    ("g8-algebraic-equations-03", "Additive inverse equations", 60,
     "Solve one-step equations by applying an additive inverse to both sides, represent each transformation on a balance or number line, and verify every solution in the original equation.",
     "Additive inverse reasoning replaces the unreliable phrase move it across and change the sign with a legal operation learners can explain.",
     "Apply the same addition or subtraction to both complete sides so the attached constant forms a zero pair beside the variable."),
    ("g8-algebraic-equations-04", "Multiplicative inverse equations", 60,
     "Solve equations of the forms ax = b and x divided by a = b by applying a multiplicative inverse to both sides, interpret the operation visually, and verify the result in the original equation.",
     "Multiplicative inverse reasoning prepares learners for multi-step equations, formula manipulation and proportional reasoning.",
     "Divide both complete sides by a non-zero coefficient, or multiply both sides by the divisor, then verify in the original equation."),
    ("g8-algebraic-equations-05", "Two step equations", 70,
     "Solve two-step linear equations by undoing addition or subtraction before undoing multiplication or division, preserve equality at every step, and verify solutions in the original equation.",
     "Two-step reasoning lets learners recover an unknown from a final result and prepares them for more advanced equation structures.",
     "Read the equation as an operation chain and reverse it one legal operation at a time, keeping both complete sides visible."),
    ("g8-algebraic-equations-06", "Variables on both sides", 75,
     "Solve linear equations with variable terms on both sides and distinguish equations with one solution, no solution or infinitely many solutions.",
     "Comparing two changing quantities produces this structure in break-even problems, equal-cost plans, geometry and functions.",
     "Remove one variable term by applying its additive inverse to both sides, then interpret any true or false statement left after cancellation."),
    ("g8-algebraic-equations-07", "Bracket equations", 80,
     "Solve linear equations containing brackets by interpreting the multiplier, distributing it to every term when useful, preserving equality, and verifying in the original bracketed equation.",
     "Brackets describe grouped quantities in area, perimeter, pricing and repeated-package problems.",
     "The outside factor multiplies every bracket term; division by the outside factor may be more efficient when the whole bracket equals a number."),
    ("g8-algebraic-equations-08", "Fraction equations", 85,
     "Solve linear equations containing numerical denominators by selecting a lowest common denominator, clearing denominators on both complete sides and checking the original fractional equation.",
     "Fraction equations appear in rates, sharing, recipes, measurement and later algebra.",
     "Multiply every term on both complete sides by a common denominator and cancel only common factors in products."),
    ("g8-algebraic-equations-09", "Forming equations from contexts", 90,
     "Translate verbal, numerical and visual situations into one-variable linear equations, define the unknown precisely, solve and verify with correct units.",
     "Real problems require learners to identify fixed and changing quantities and judge whether an answer makes sense in context.",
     "Define the variable with its unit, model the relationship, write an equality only for equal totals, and return to the original context to verify."),
    ("g8-algebraic-equations-10", "Mastery diagnosis and repair", 100,
     "Diagnose the first incorrect step, connect it to a specific misconception, repair the missing concept and complete a fresh parallel problem.",
     "Effective revision identifies the earliest invalid step and tests whether the learner can transfer the repair to a new problem.",
     "Compare consecutive learner lines, stop at the first invalid change, teach the smallest targeted repair and reassess with fresh values."),
)


def _lesson(number: int, row: tuple[str, str, int, str, str, str]) -> Lesson:
    lesson_id, title, duration, objective, why, teaching = row
    return Lesson(
        id=lesson_id,
        order=number,
        title=title,
        objective=objective,
        why_it_matters=why,
        intuition=teaching,
        prerequisites=[] if number == 1 else [LESSON_METADATA[number - 2][0]],
        estimated_minutes=duration,
        difficulty="foundation" if number <= 4 else "standard" if number <= 9 else "exam",
        access_level=AccessLevel.FREE if number == 1 else AccessLevel.PREMIUM,
        status=ContentStatus.COMING_SOON,
        blocks=[LessonBlock(
            type="concept",
            title="Approved concept teaching",
            content=teaching,
            data={"runtime_conversion": "required", "source_status": "approved_reference" if number == 1 else "authored"},
        )],
        whiteboard_questions=[],
        mastery_threshold=.8,
        paper=None,
        source_document=SOURCE,
        source_sha256=SOURCE_SHA256,
        assessment_contract={
            "worked_example_count": 15,
            "practice_count": 15,
            "mastery_question_count": 5,
            "parallel_reassessment_count": 3,
            "answer_hidden_before_submission": True,
            "runtime_conversion": "pending",
        },
    )


ALGEBRAIC_EQUATION_LESSONS = [
    LESSON_1 if number == 1 else LESSON_2 if number == 2 else LESSON_3 if number == 3 else LESSON_4 if number == 4 else LESSON_5 if number == 5 else LESSON_6 if number == 6 else LESSON_7 if number == 7 else LESSON_8 if number == 8 else LESSON_9 if number == 9 else LESSON_10 if number == 10 else _lesson(number, row)
    for number, row in enumerate(LESSON_METADATA, 1)
]

ALGEBRAIC_EQUATIONS_TOPIC = Topic(
    id="algebraic-equations",
    product_order=1,
    title="Algebraic Equations",
    official_caps_topic="Algebraic equations",
    caps_sequence=1,
    term=2,
    expected_duration="10 lessons",
    paper=None,
    caps_reference="CAPS Grade 8 Mathematics — Patterns, Functions and Algebra",
    curriculum="CAPS",
    ieb_relevant=True,
    exam_relevance="Grade 8 classroom and formal assessment",
    status=ContentStatus.TEACHER_REVIEW_REQUIRED,
    subtopics=[Subtopic(
        id="algebraic-equations-learning-path",
        order=1,
        title="Approved ten-lesson learning path",
        prerequisites=[],
        lessons=ALGEBRAIC_EQUATION_LESSONS,
    )],
)

ALGEBRAIC_EXPRESSIONS_TOPIC = Topic(
    id="algebraic-expressions", product_order=2, title="Algebraic Expressions",
    official_caps_topic="Algebraic expressions", caps_sequence=2, term=2,
    expected_duration="Ten lessons authored; teacher review and browser acceptance pending",
    paper=None, caps_reference="CAPS Grade 8 Mathematics — Algebraic expressions",
    curriculum="CAPS", ieb_relevant=True,
    exam_relevance="Grade 8 classroom and formal assessment",
    status=ContentStatus.TEACHER_REVIEW_REQUIRED,
    subtopics=[Subtopic(id="algebraic-expressions-learning-path", order=1,
        title="Algebraic language and expressions", prerequisites=[], lessons=[EXPRESSIONS_LESSON, EXPRESSIONS_LESSON_2, EXPRESSIONS_LESSON_3, EXPRESSIONS_LESSON_4, EXPRESSIONS_LESSON_5, EXPRESSIONS_LESSON_6, EXPRESSIONS_LESSON_7, EXPRESSIONS_LESSON_8, EXPRESSIONS_LESSON_9, EXPRESSIONS_LESSON_10])],
)

FUNCTIONS_RELATIONSHIPS_TOPIC = Topic(
    id="functions-relationships", product_order=3, title="Functions and Relationships",
    official_caps_topic="Functions and relationships", caps_sequence=3, term=2,
    expected_duration="Six lessons authored; teacher review and browser acceptance pending",
    paper=None, caps_reference="CAPS Grade 8 Mathematics — Functions and relationships",
    curriculum="CAPS", ieb_relevant=True,
    exam_relevance="Grade 8 classroom and formal assessment",
    status=ContentStatus.TEACHER_REVIEW_REQUIRED,
    subtopics=[Subtopic(id="functions-relationships-learning-path",order=1,
        title="Input-output values, equivalence and formula contexts",prerequisites=[],lessons=[FUNCTIONS_LESSON_1,FUNCTIONS_LESSON_2,FUNCTIONS_LESSON_3,FUNCTIONS_LESSON_4,FUNCTIONS_LESSON_5,FUNCTIONS_LESSON_6])],
)

GRAPHS_TOPIC = Topic(
    id="graphs", product_order=4, title="Graphs",
    official_caps_topic="Graphs", caps_sequence=4, term=2,
    expected_duration="Six graph lessons authored; teacher review and browser acceptance pending",
    paper=None, caps_reference="CAPS Grade 8 Mathematics — Graphs",
    curriculum="CAPS", ieb_relevant=True,
    exam_relevance="Grade 8 classroom and formal assessment",
    status=ContentStatus.TEACHER_REVIEW_REQUIRED,
    subtopics=[Subtopic(id="graphs-learning-path", order=1,
        title="Coordinates, graph reading and graph drawing", prerequisites=["functions-relationships"],
        lessons=[GRAPHS_LESSON_1, GRAPHS_LESSON_2, GRAPHS_LESSON_3, GRAPHS_LESSON_4, GRAPHS_LESSON_5, GRAPHS_LESSON_6])],
)

PATTERNS_TOPIC = Topic(
    id="numeric-geometric-patterns", product_order=5, title="Numeric and Geometric Patterns",
    official_caps_topic="Numeric and geometric patterns", caps_sequence=5, term=1,
    expected_duration="Six lessons authored; teacher review and browser acceptance pending",
    paper=None, caps_reference="2026 CAPS Grade 8 Mathematics ATP — Patterns",
    curriculum="CAPS", ieb_relevant=True, exam_relevance="Grade 8 classroom and formal assessment",
    status=ContentStatus.TEACHER_REVIEW_REQUIRED,
    subtopics=[Subtopic(id="patterns-learning-path",order=1,title="Numeric rules and geometric models",
        prerequisites=[],lessons=[PATTERNS_LESSON_1,PATTERNS_LESSON_2,PATTERNS_LESSON_3,PATTERNS_LESSON_4,PATTERNS_LESSON_5,PATTERNS_LESSON_6])],
)

WHOLE_NUMBERS_TOPIC = Topic(
    id="whole-numbers", product_order=6, title="Whole Numbers",
    official_caps_topic="Whole numbers", caps_sequence=1, term=1,
    expected_duration="Two lessons authored; remaining whole-number scope and teacher review pending",
    paper=None, caps_reference="2026 DBE Grade 8 Mathematics ATP — Term 1 Whole Numbers",
    curriculum="CAPS", ieb_relevant=True, exam_relevance="Grade 8 classroom and formal assessment",
    status=ContentStatus.TEACHER_REVIEW_REQUIRED,
    subtopics=[Subtopic(id="whole-numbers-learning-path",order=1,
        title="Properties, factors and multiples",prerequisites=[],lessons=[WHOLE_LESSON_1,WHOLE_LESSON_2])],
)

INTEGERS_TOPIC = Topic(
    id="integers",product_order=7,title="Integers",official_caps_topic="Integers",
    caps_sequence=2,term=1,expected_duration="Six lessons authored; review and enrichment still pending",
    paper=None,caps_reference="2026 DBE Grade 8 Mathematics ATP — Term 1 Integers",
    curriculum="CAPS",ieb_relevant=True,exam_relevance="Grade 8 classroom and formal assessment",
    status=ContentStatus.TEACHER_REVIEW_REQUIRED,
    subtopics=[Subtopic(id="integers-learning-path",order=1,title="Signed order and directed operations",
        prerequisites=[],lessons=[INTEGER_LESSON_1,INTEGER_LESSON_2,INTEGER_LESSON_3,INTEGER_LESSON_4,INTEGER_LESSON_5,INTEGER_LESSON_6])],
)

from app.curriculum.grade8.decimals_runtime import LESSON_1 as DECIMAL_LESSON_1, LESSON_2 as DECIMAL_LESSON_2, LESSON_3 as DECIMAL_LESSON_3, LESSON_4 as DECIMAL_LESSON_4, LESSON_5 as DECIMAL_LESSON_5, LESSON_6 as DECIMAL_LESSON_6

DECIMALS_TOPIC = Topic(
    id="decimal-fractions",product_order=9,title="Decimal Fractions",official_caps_topic="Decimal Fractions",
    caps_sequence=4,term=1,expected_duration="Six decimal lessons authored; teacher review and browser acceptance pending",
    paper=None,caps_reference="2026 DBE Grade 8 Mathematics ATP — Term 1 Decimal Fractions",
    curriculum="CAPS",ieb_relevant=True,exam_relevance="Grade 8 classroom and formal assessment",
    status=ContentStatus.TEACHER_REVIEW_REQUIRED,
    subtopics=[Subtopic(id="decimal-learning-path",order=1,title="Decimal positions and rounding",prerequisites=["g8-common-fractions-08"],lessons=[DECIMAL_LESSON_1,DECIMAL_LESSON_2,DECIMAL_LESSON_3,DECIMAL_LESSON_4,DECIMAL_LESSON_5,DECIMAL_LESSON_6])],
)

FRACTIONS_TOPIC = Topic(
    id="common-fractions",product_order=8,title="Common Fractions",official_caps_topic="Common Fractions",
    caps_sequence=3,term=1,expected_duration="Eight foundational lessons authored; teacher review and browser acceptance pending",
    paper=None,caps_reference="2026 DBE Grade 8 Mathematics ATP — Common Fractions",
    curriculum="CAPS",ieb_relevant=True,exam_relevance="Grade 8 classroom and formal assessment",
    status=ContentStatus.TEACHER_REVIEW_REQUIRED,
    subtopics=[Subtopic(id="fractions-learning-path",order=1,title="Equivalent forms and fraction calculations",
        prerequisites=[],lessons=[FRACTIONS_LESSON_1,FRACTIONS_LESSON_2,FRACTIONS_LESSON_3,FRACTIONS_LESSON_4,FRACTIONS_LESSON_5,FRACTIONS_LESSON_6,FRACTIONS_LESSON_7,FRACTIONS_LESSON_8])],
)

from app.curriculum.grade8.exponents_runtime import LESSON_1 as EXPONENT_LESSON_1, LESSON_2 as EXPONENT_LESSON_2, LESSON_3 as EXPONENT_LESSON_3, LESSON_4 as EXPONENT_LESSON_4, LESSON_5 as EXPONENT_LESSON_5, LESSON_6 as EXPONENT_LESSON_6
EXPONENTS_TOPIC = Topic(
    id="exponents",product_order=10,title="Exponents",official_caps_topic="Exponents",
    caps_sequence=6,term=2,expected_duration="Six lessons authored; teacher review and browser acceptance pending",
    paper=None,caps_reference="2026 DBE Grade 8 Mathematics ATP — Term 2 Exponents",
    curriculum="CAPS",ieb_relevant=True,exam_relevance="Grade 8 classroom and formal assessment",
    status=ContentStatus.TEACHER_REVIEW_REQUIRED,
    subtopics=[Subtopic(id="exponents-learning-path",order=1,title="Power representation and laws",
        prerequisites=["g8-decimal-fractions-06"],lessons=[EXPONENT_LESSON_1,EXPONENT_LESSON_2,EXPONENT_LESSON_3,EXPONENT_LESSON_4,EXPONENT_LESSON_5,EXPONENT_LESSON_6])],
)

GRADE_8 = GradeCurriculum(
    id="grade-8",
    grade=8,
    status=ContentStatus.DRAFT,
    topics=[ALGEBRAIC_EQUATIONS_TOPIC, ALGEBRAIC_EXPRESSIONS_TOPIC, FUNCTIONS_RELATIONSHIPS_TOPIC, GRAPHS_TOPIC, PATTERNS_TOPIC, WHOLE_NUMBERS_TOPIC, INTEGERS_TOPIC, FRACTIONS_TOPIC, DECIMALS_TOPIC, EXPONENTS_TOPIC],
)
