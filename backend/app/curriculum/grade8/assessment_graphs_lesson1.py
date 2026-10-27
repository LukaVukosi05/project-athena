"""Private answer keys for Grade 8 Cartesian coordinate practice."""
from app.curriculum.grade8.graphs_lesson1 import LESSON_ID, SOURCE, QUESTIONS
from app.curriculum.grade8.assessment_expressions import AssessmentQuestion
from app.practice.schemas import AnswerNormalisation, PracticeQuestion, WorkedSolutionStep

PRACTICE = [
    ("Give the point one right and four up from the origin.", "(1, 4)", "Across first: x = 1; then y = 4."),
    ("Give the point two left and one up from the origin.", "(-2, 1)", "Left means a negative x-coordinate."),
    ("Give the coordinates of the point four below the origin on the y-axis.", "(0, -4)", "A point on the y-axis has x = 0."),
    ("Give the coordinates of the point five left of the origin on the x-axis.", "(-5, 0)", "A point on the x-axis has y = 0."),
    ("Give the point one left and three down from the origin.", "(-1, -3)", "Both directions are negative."),
    ("Give the point four right and two down from the origin.", "(4, -2)", "Move across before moving down."),
    ("Plot (2, -1). In which quadrant is it?", "IV", "Positive x and negative y is bottom right."),
    ("With x ticks of 2 and y ticks of 4, how many x and y intervals reach (6, 8)?", "3 right, 2 up", "Divide each coordinate by its own axis interval."),
    ("With both axes marked in threes, how many intervals reach (-6, 9)?", "2 left, 3 up", "Use -6 ÷ 3 and 9 ÷ 3."),
    ("What ordered pair has x = 0 and y = 5?", "(0, 5)", "Place x first, even when it is zero."),
    ("A learner places (-4, 2) at (2, -4). Give the correct ordered pair.", "(-4, 2)", "The learner swapped x and y."),
    ("Time is x in hours and cost is y in rand. What pair means 3 hours and R45?", "(3, 45)", "Match each number to its axis title."),
    ("From (1, -2), move up three units. Give the new pair.", "(1, 1)", "Keep x fixed; -2 + 3 = 1."),
    ("From (-3, 4), move right five units. Give the new pair.", "(2, 4)", "Change x only: -3 + 5 = 2."),
    ("At 5 y-units per tick, how many ticks up represents y = 10?", "2", "10 ÷ 5 = 2 ticks."),
]


def _practice(row, number):
    prompt, answer, memo = row
    return PracticeQuestion(id=f"g8-graphs-l01-p{number:02}", lesson_id=LESSON_ID,
        question_number=number,
        difficulty="foundation" if number <= 3 else "easy" if number <= 6 else "standard" if number <= 10 else "exam" if number <= 13 else "advanced",
        cognitive_level="knowledge" if number <= 3 else "routine" if number <= 10 else "complex",
        marks=2 if number <= 6 else 3 if number <= 13 else 4,
        type="short_text", prompt=prompt,
        accepted_answers=[answer, answer.replace(" ", ""), answer.replace("-", "−")],
        answer_normalisation=AnswerNormalisation(),
        hints=["Identify the horizontal coordinate or movement first.", memo],
        worked_solution=[WorkedSolutionStep(expression="Read x, then y", explanation="Use the labelled axes in order.", why="Coordinates are ordered."),
            WorkedSolutionStep(expression=answer, explanation=memo, why=memo, verification=memo)],
        misconception_tags=QUESTIONS[number-1].misconception_tags,
        verification={"original_question_check": memo},
        correct_feedback="Correct. The pair agrees with the original axes and scale.",
        source=SOURCE.name, answer_hidden_before_submission=True)


PRACTICE_BANK = [_practice(row, index) for index, row in enumerate(PRACTICE, 1)]

MASTERY_DATA = [
    ("Give the coordinates three left and two up.", "(-3, 2)", "x = -3; y = 2."),
    ("Give the ordered pair four below the origin on the y-axis.", "(0, -4)", "A point on the y-axis has x = 0."),
    ("With x ticks of 2 and y ticks of 5, how many intervals reach (4, -10)?", "2 right, 2 down", "4 ÷ 2 = 2 right; -10 ÷ 5 = -2 down."),
    ("A learner plots (-1, 3) at (3, -1). Give the correct pair.", "(-1, 3)", "The x and y roles were reversed."),
    ("Move three units up from (-2, -1). Give the new pair.", "(-2, 2)", "Keep x = -2; -1 + 3 = 2."),
]
REASSESSMENT_DATA = [
    ("Give the coordinates four left and one down.", "(-4, -1)", "x = -4; y = -1."),
    ("With x ticks of 3 and y ticks of 2, how many intervals reach (6, 4)?", "2 right, 2 up", "6 ÷ 3 = 2 and 4 ÷ 2 = 2."),
    ("Move five units up from (0, -3). Give the new pair.", "(0, 2)", "Keep x = 0; -3 + 5 = 2."),
]


def _assessment(row, number, mastery):
    prompt, answer, memo = row
    return AssessmentQuestion(id=f"g8-graphs-l01-{'m' if mastery else 'r'}{number:02}",
        number=number, prompt=prompt, marks=4 if mastery else None,
        answer=answer, solution=[memo, answer], verification=memo,
        misconception_tags=["coordinate-order-and-scale"],
        accepted_answers=[answer.replace(" ", ""), answer.replace("-", "−")])


MASTERY_BANK = [_assessment(row, index, True) for index, row in enumerate(MASTERY_DATA, 1)]
REASSESSMENT_BANK = [_assessment(row, index, False) for index, row in enumerate(REASSESSMENT_DATA, 1)]
MISCONCEPTION_REPAIRS = {"coordinate-order-and-scale": {
    "diagnosis": "The x/y order, sign, or tick scale was misread.",
    "repair": "Read axis titles and tick intervals, move across first, then up or down, and project back."}}
REPAIR_RULES = {"coordinate-order-and-scale": "Retry a different point with a changed axis scale."}
