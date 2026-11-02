"""Private Grade 8 table-to-graph assessment answers and targeted repair."""
from app.curriculum.grade8.graphs_lesson2 import LESSON_ID, SOURCE, QUESTIONS
from app.curriculum.grade8.assessment_expressions import AssessmentQuestion
from app.practice.schemas import AnswerNormalisation, PracticeQuestion, WorkedSolutionStep

# These are separate from the worked examples and require an independent attempt.
PRACTICE = [
    ("A table pairs x = 0 with y = 4. Give the ordered pair.", "(0, 4)", "Match one column: input 0 is x and output 4 is y."),
    ("For y = x + 2, what is y when x = 2?", "4", "Substitute 2: y = 2 + 2 = 4."),
    ("The graph has a dot at x = 1 and y = 5. Give its ordered pair.", "(1, 5)", "Project the dot to both labelled axes; x comes first."),
    ("For y = 6 − x, give the output at x = 4.", "2", "6 − 4 = 2."),
    ("For y = 3x, give the pair when x = −2.", "(-2, -6)", "3(−2) = −6, so plot two left and six down."),
    ("A table has x: 0, 1, 2 and y: 7, 7, 7. Is the graph horizontal or vertical?", "horizontal", "The output stays at y = 7 while x changes."),
    ("For y = 2x + 3, give the plotted pair at x = 2.", "(2, 7)", "2(2) + 3 = 7; keep x = 2."),
    ("A learner plots table column x = −1, y = 4 at (4, −1). Give the correct pair.", "(-1, 4)", "Read input first, output second."),
    ("With y-axis ticks of 5, how many intervals above zero is y = 15?", "3", "15 ÷ 5 = 3 intervals."),
    ("A graph shows points (0, 2), (1, 4), (2, 6). What y belongs to x = 1?", "4", "Read the dot directly above x = 1."),
    ("For y = 2x + 1, a learner plots x = 3 at y = 6. What y is correct?", "7", "2(3) + 1 = 7, so the plotted y-value was one too small."),
    ("A booking fee is R8 and each whole ticket costs R4. Should points for ticket counts be joined? Answer yes or no.", "no", "Only whole-number ticket counts are valid; a joined line suggests fractional tickets."),
    ("Time x is in hours and temperature y in °C. Interpret point (3, 9): what is the temperature after 3 hours?", "9", "The y-coordinate gives 9 °C at x = 3 hours."),
    ("For y = 2x + 5, find the next y after x: 0, 1, 2, 3 when x = 3.", "11", "2(3) + 5 = 11; plot (3, 11)."),
    ("For equal x-steps, y rises 1, then 3, then 5. Does one straight line fit every dot? Answer yes or no.", "no", "A straight line has a constant y-change for equal x-steps."),
]

def _practice(row,number):
    prompt,answer,memo=row
    return PracticeQuestion(id=f"g8-graphs-l02-p{number:02}",lesson_id=LESSON_ID,question_number=number,
        difficulty="foundation" if number<=3 else "easy" if number<=6 else "standard" if number<=10 else "exam" if number<=13 else "advanced",
        cognitive_level="knowledge" if number<=3 else "routine" if number<=10 else "complex",marks=2 if number<=6 else 3 if number<=13 else 4,
        type="short_text",prompt=prompt,accepted_answers=[answer,answer.replace(" ",""),answer.replace("-","−")],
        answer_normalisation=AnswerNormalisation(),hints=["First match an input to its own output or inspect the axis domain.",memo],
        worked_solution=[WorkedSolutionStep(expression="Read the matching column",explanation="Pair x with its own y, respecting labels and scale.",why="The two entries form one plotted point."),
            WorkedSolutionStep(expression=answer,explanation=memo,why=memo,verification=memo)],
        misconception_tags=QUESTIONS[number-1].misconception_tags,verification={"original_question_check":memo},
        correct_feedback="Correct. This agrees with the supplied table, rule or axis domain.",source=SOURCE.name,answer_hidden_before_submission=True)

PRACTICE_BANK=[_practice(row,n) for n,row in enumerate(PRACTICE,1)]
MASTERY_DATA=[
    ("For y = 3x − 1, what is the output when x = 2?", "5", "3(2) − 1 = 5."),
    ("A point is at x = −2, y = 6. Write the ordered pair.", "(-2, 6)", "Input first: (−2, 6)."),
    ("If x-axis ticks represent 2 units, how many intervals right is x = 8?", "4", "8 ÷ 2 = 4."),
    ("For a whole-number count of bags, should the plotted dots be joined?", "no", "Fractions of a bag are outside the question domain."),
    ("Equal x-steps produce y-rises 2, 2, 2. Is a straight line consistent?", "yes", "Constant rises for equal x-steps are collinear."),
]
REASSESSMENT_DATA=[
    ("For y = 4x + 2, what output belongs to x = 2?", "10", "4(2) + 2 = 10."),
    ("At y ticks of 3, how many intervals above zero represents y = 12?", "4", "12 ÷ 3 = 4."),
    ("Whole-number ticket counts are plotted. Should a line connect the points?", "no", "Half a ticket is not an allowed input."),
]

def _assessment(row,number,mastery):
    prompt,answer,memo=row
    return AssessmentQuestion(id=f"g8-graphs-l02-{'m' if mastery else 'r'}{number:02}",number=number,prompt=prompt,
        marks=4 if mastery else None,answer=answer,solution=[memo,answer],verification=memo,
        misconception_tags=["table-graph-link"],accepted_answers=[answer.replace(" ",""),answer.replace("-","−")])

MASTERY_BANK=[_assessment(row,n,True) for n,row in enumerate(MASTERY_DATA,1)]
REASSESSMENT_BANK=[_assessment(row,n,False) for n,row in enumerate(REASSESSMENT_DATA,1)]
MISCONCEPTION_REPAIRS={"table-graph-link":{"diagnosis":"An input-output column, axis scale, sign or domain was misread.",
    "repair":"Read one table column aloud, project it to the labelled axes, then ask whether intermediate x-values are allowed."}}
REPAIR_RULES={"table-graph-link":"Use a fresh rule and scale, and decide separately whether the points should be joined."}
