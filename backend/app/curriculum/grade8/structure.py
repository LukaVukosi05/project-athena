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

GRADE_8 = GradeCurriculum(
    id="grade-8",
    grade=8,
    status=ContentStatus.DRAFT,
    topics=[ALGEBRAIC_EQUATIONS_TOPIC],
)
