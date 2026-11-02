"""Independent Grade 8 global-graph assessment with private solution keys."""
from app.curriculum.grade8.graphs_lesson6 import LESSON_ID, SOURCE, QUESTIONS
from app.curriculum.grade8.assessment_expressions import AssessmentQuestion
from app.practice.schemas import AnswerNormalisation, PracticeQuestion, WorkedSolutionStep
PRACTICE=[('A graph shows 7 L at minute 2. A learner says 5 L. What is the correct level?', '7', 'Read y at x = 2.'), ('Temperature moves from 20°C to 25°C. A learner says it falls. Is it rising or falling?', 'rising', '25 > 20.'), ('A candle goes from 8 to 6 cm. A learner says it grows 2 cm. What actually happens?', 'shrinks', '6 is 2 cm less than 8.'), ('A distance graph stays at 4 km for an hour. A learner says the person returned. Is the graph rising, falling or flat?', 'flat', 'Equal endpoints mean no distance change.'), ('Speeds are 8, 17 and 13 km/h. A learner says 13 is highest. What is the maximum?', '17', '17 exceeds both 8 and 13.'), ('A plant rises by 2, 3, then 4 cm in equal weeks. A learner calls it constant growth. Are the increases equal?', 'no', '2, 3 and 4 differ.'), ('Books counted are 3 at day 2 and 6 at day 3. A learner reads 3 for day 3. What is correct?', '6', 'At x = 3 read y = 6.'), ('Freezer temperature changes from −3 to −8°C. A learner says it warms. Does it warm or cool?', 'cools', '−8 is colder than −3.'), ('A reservoir rises from 4 to 14 ML. A learner says the gain is 14. What is the gain?', '10', '14 − 4 = 10 ML.'), ('Data balance is 6 GB at day 1 and 6 GB at day 2. A learner says 6 GB was used. What is the change?', '0', '6 − 6 = 0.'), ('Rainfall total rises from 5 to 8 mm. A learner says no rain fell. How much was added?', '3', '8 − 5 = 3 mm.'), ('A graph counts whole tickets. A learner joins points to imply half a ticket. Should points be joined? Answer yes or no.', 'no', 'A half ticket is not an allowed count.'), ('Readings are −4°C at hour 1 and 2°C at hour 2. A learner says hour 1 is first positive. Which hour is first positive?', '2', '−4 is negative; 2 is positive at hour 2.'), ('A traveller is 6 km away during a flat interval. A learner says they are home. How far from home?', '6', 'A flat line stays at 6 km, not zero.'), ('A tank falls from 15 L to 4 L. A learner says it loses 15 L. What is the loss?', '11', '15 − 4 = 11 L.')]
MASTERY_DATA=[('At hour 2 a graph reads 11; a learner reads 8. What is correct?', '11', 'Project x = 2 to y = 11.'), ('Height falls 9 to 5. Does it increase or decrease?', 'decrease', '5 < 9.'), ('A graph is flat at 4 L. What is its change?', '0', '4 − 4 = 0.'), ('Temperatures −6, −2, 3. What is the first positive reading?', '3', '−6 and −2 are negative.'), ('A count is of whole books. Join the dots? Answer yes or no.', 'no', 'No fractional book.')]
REASSESSMENT_DATA=[('A graph shows 12 km at hour 1. A learner reads 10. What is correct?', '12', 'Read the graph at x = 1.'), ('From 5 to 5 L, is the change 0? Answer yes or no.', 'yes', '5 − 5 = 0.'), ('A count of whole chairs is discrete. Join fractional inputs? Answer yes or no.', 'no', 'Only whole chair counts.')]
TAG="graph-comparison" if 6==5 else "graph-claim-repair"
def _practice(row,number):
    prompt,answer,memo=row
    return PracticeQuestion(id=f"g8-graphs-l06-p{number:02}",lesson_id=LESSON_ID,question_number=number,
        difficulty="foundation" if number<=3 else "easy" if number<=6 else "standard" if number<=9 else "exam" if number<=12 else "advanced",
        cognitive_level="knowledge" if number<=3 else "routine" if number<=9 else "complex",marks=2 if number<=3 else 3 if number<=9 else 5,
        type="short_text",prompt=prompt,accepted_answers=[answer,answer.replace(" ",""),answer.replace("-","−")],
        answer_normalisation=AnswerNormalisation(),hints=["Read the horizontal input before the vertical output and compare endpoints.",memo],
        worked_solution=[WorkedSolutionStep(expression="Read the labelled values",explanation="Identify which quantity is horizontal and which is vertical.",why="An interpretation needs its original axis labels."),
            WorkedSolutionStep(expression=answer,explanation=memo,why=memo,verification=memo)],
        misconception_tags=[TAG],verification={"original_question_check":memo},correct_feedback="Correct; the values agree with the stated graph.",
        source=SOURCE.name,answer_hidden_before_submission=True)
PRACTICE_BANK=[_practice(row,n) for n,row in enumerate(PRACTICE,1)]
def _assessment(row,number,mastery):
    prompt,answer,memo=row
    return AssessmentQuestion(id=f"g8-graphs-l06-{'m' if mastery else 'r'}{number:02}",number=number,prompt=prompt,
        marks=4 if mastery else None,answer=answer,solution=[memo,answer],verification=memo,
        misconception_tags=[TAG],accepted_answers=[answer.replace(" ",""),answer.replace("-","−")])
MASTERY_BANK=[_assessment(row,n,True) for n,row in enumerate(MASTERY_DATA,1)]
REASSESSMENT_BANK=[_assessment(row,n,False) for n,row in enumerate(REASSESSMENT_DATA,1)]
MISCONCEPTION_REPAIRS={TAG:{"diagnosis":"The axis, interval, direction, scale or domain was misread.",
    "repair":"Read the axis labels; identify the endpoints of one interval; calculate the vertical change and justify the domain."}}
REPAIR_RULES={TAG:"Reattempt with a new context and changed axis values; explain each interval before stating the answer."}
