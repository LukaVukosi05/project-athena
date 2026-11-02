"""Independent Grade 8 global-graph assessment with private solution keys."""
from app.curriculum.grade8.graphs_lesson4 import LESSON_ID, SOURCE, QUESTIONS
from app.curriculum.grade8.assessment_expressions import AssessmentQuestion
from app.practice.schemas import AnswerNormalisation, PracticeQuestion, WorkedSolutionStep
PRACTICE=[('A tank contains 3 L at minute 0 and 7 L at minute 1. Give the first two plotted pairs.', '(0, 3), (1, 7)', 'Time is the horizontal coordinate; volume is vertical.'), ('A car travels 12 km in the first hour then waits until hour 2. What point represents the end of the wait?', '(2, 12)', 'The distance stays 12 km while time reaches 2 hours.'), ('A drink cools from 18°C to 14°C in one minute. Is its first segment increasing or decreasing?', 'decreasing', 'The vertical temperature falls by 4.'), ('A class counts 1, 3, 4 books on successive days. Should the points be joined? Answer yes or no.', 'no', 'Whole book counts are separate outcomes.'), ('A bus is 7 km away at hour 1 and 0 km away at hour 2. Which point ends the return?', '(2, 0)', 'After two hours, distance from home is zero.'), ('The temperature is −3°C at dawn then 2°C one hour later. Give the two plotted pairs.', '(0, -3), (1, 2)', 'Time goes first in each pair; negative temperature lies below zero.'), ('Savings are R4 at week 0 and rise R3 each week. What is the point at week 2?', '(2, 10)', '4 + 2(3) = 10 rand, so the pair is (2, 10).'), ('A tap fills a pool to 9 cm by hour 1 and stays there until hour 2. Is that second segment rising or flat?', 'flat', 'Both endpoints have vertical coordinate 9.'), ('An elevator is at floor 0 at minute 0, floor 4 at minute 1, floor 4 at minute 2. What is the point at minute 2?', '(2, 4)', 'The elevator waits at floor 4 while time advances.'), ('A ball reaches 3 m at second 1 and 5 m at second 2. Does a single horizontal line fit? Answer yes or no.', 'no', 'Height rises between the two seconds.'), ('A tank begins at 16 L and loses 2 L each hour. What point belongs to hour 3?', '(3, 10)', '16 − 3(2) = 10 L.'), ('A ticket counter records 0, 1, 2 tickets for 0, 1, 2 customers. Is the input domain discrete or continuous?', 'discrete', 'Only whole numbers of customers are meaningful.'), ('A cyclist speeds up to 20 km/h and stays there for an hour. How is the last interval drawn?', 'horizontal', 'The vertical speed remains 20 km/h while time advances.'), ('A lift travels from floor 5 at minute 1 down to floor 2 at minute 2. Give the final plotted pair.', '(2, 2)', 'Place time 2 on x and floor 2 on y.'), ('A pool is 12 cm deep at hour 1 and 7 cm at hour 2. How should the final segment move?', 'decreasing', 'It falls from y = 12 to y = 7 as x increases.')]
MASTERY_DATA=[('Start at 2 L at time 0. Give the first point.', '(0, 2)', 'Input time comes first.'), ('From (1, 3) to (2, 3), is the segment flat? Answer yes or no.', 'yes', 'The vertical values agree.'), ('From (1, 8) to (2, 5), is the segment rising or falling?', 'falling', '5 < 8.'), ('If only whole bags count, join the plotted dots? Answer yes or no.', 'no', 'The domain is discrete.'), ('From 0 km at hour 0 to 6 km at hour 1, give the endpoint.', '(1, 6)', 'Time 1 is x; distance 6 is y.')]
REASSESSMENT_DATA=[('An empty bottle gains 4 L by hour 1. Give the end point.', '(1, 4)', 'Time 1 and volume 4.'), ('A distance graph stays at 5 km while time advances. Is the segment flat? Answer yes or no.', 'yes', 'Equal distances imply a horizontal segment.'), ('For whole eggs counted, should points be joined? Answer yes or no.', 'no', 'Egg counts are whole.')]
TAG="graph-interpretation" if 4==3 else "graph-construction"
def _practice(row,number):
    prompt,answer,memo=row
    return PracticeQuestion(id=f"g8-graphs-l04-p{number:02}",lesson_id=LESSON_ID,question_number=number,
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
    return AssessmentQuestion(id=f"g8-graphs-l04-{'m' if mastery else 'r'}{number:02}",number=number,prompt=prompt,
        marks=4 if mastery else None,answer=answer,solution=[memo,answer],verification=memo,
        misconception_tags=[TAG],accepted_answers=[answer.replace(" ",""),answer.replace("-","−")])
MASTERY_BANK=[_assessment(row,n,True) for n,row in enumerate(MASTERY_DATA,1)]
REASSESSMENT_BANK=[_assessment(row,n,False) for n,row in enumerate(REASSESSMENT_DATA,1)]
MISCONCEPTION_REPAIRS={TAG:{"diagnosis":"The axis, interval, direction, scale or domain was misread.",
    "repair":"Read the axis labels; identify the endpoints of one interval; calculate the vertical change and justify the domain."}}
REPAIR_RULES={TAG:"Reattempt with a new context and changed axis values; explain each interval before stating the answer."}
