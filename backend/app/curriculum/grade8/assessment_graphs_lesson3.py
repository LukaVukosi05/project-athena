"""Independent Grade 8 global-graph assessment with private solution keys."""
from app.curriculum.grade8.graphs_lesson3 import LESSON_ID, SOURCE, QUESTIONS
from app.curriculum.grade8.assessment_expressions import AssessmentQuestion
from app.practice.schemas import AnswerNormalisation, PracticeQuestion, WorkedSolutionStep
PRACTICE=[('A water-level graph has values 3, 5, 7 litres at hours 0, 1, 2. What is the level at hour 1?', '5', 'At x = 1 hour, read y = 5 litres.'), ('A temperature graph has 15, 15, 15 degrees at hours 0, 1, 2. Is it increasing, constant or decreasing?', 'constant', 'All three heights are equal, so the graph is horizontal.'), ('A candle falls from 9 cm to 4 cm. How many centimetres did it shrink?', '5', 'Subtract the final height from the first: 9 − 4 = 5.'), ('A traveller is 2 km away at hour 1 and still 2 km away at hour 2. What is the graph doing between these hours?', 'constant', 'The y-value does not change while time moves forward.'), ('Speed values at minutes 0, 1, 2 are 0, 8, 6 km/h. Give the maximum speed.', '8', 'The greatest vertical value is 8 km/h.'), ('A plant grows 2, then 4, then 8 cm in equal weeks. Are the rises equal? Answer yes or no.', 'no', 'The consecutive increases are 2 and 4, so they differ.'), ('A graph shows 3 books on day 1 and 9 books on day 2. What is the increase?', '6', 'Read the two y-values at their days and subtract 9 − 3 = 6.'), ('Temperature is −5 at noon and −1 an hour later. Is the temperature increasing or decreasing?', 'increasing', '−1 is greater than −5, so the line rises.'), ('A graph shows water at 2, 8, 11 at hours 0, 1, 2. Which hour interval rises more?', 'hour 0 to hour 1', 'The first rise is 6; the next rise is 3.'), ('Mobile data use is 1 GB at day 2 and 4 GB at day 3. How much is used in that interval?', '3', '4 − 1 = 3 GB.'), ('A rain gauge remains at 7 mm from hour 4 to 5. What does the flat interval mean?', 'no additional rain', 'The accumulated total did not increase.'), ('A graph counts whole people. Should dots be joined to show half a person? Answer yes or no.', 'no', 'Half a person is outside the input domain.'), ('Freezer readings at three hours are −2, −7, −4 degrees C. Give the minimum.', '-7', '−7 lies lowest on the temperature axis.'), ('A walker is 0, 6, 6, 2 km from home at hours 0–3. How far from home at hour 3?', '2', 'At x = 3, the graph has y = 2 km.'), ('A tank holds 13 L, then 13 L, then 5 L. How many litres drained on the final interval?', '8', '13 − 5 = 8 L; the earlier flat interval is separate.')]
MASTERY_DATA=[('Values 1, 4, 4 at hours 0–2. What is the change from hour 1 to 2?', '0', '4 − 4 = 0.'), ('A graph reaches 11 cm at week 2 and 9 cm at week 3. Which is higher?', 'week 2', '11 > 9.'), ('Temperatures −1, −6, 0. Give the minimum.', '-6', '−6 is the lowest.'), ('People counted at 0, 1, 2. Join the dots? Answer yes or no.', 'no', 'Half a person is impossible.'), ('A reservoir falls from 20 to 8 ML. What is the decrease?', '12', '20 − 8 = 12.')]
REASSESSMENT_DATA=[('A tank rises from 4 L to 10 L. Give the increase.', '6', '10 − 4 = 6.'), ('A graph stays at 6 km for two hours. Is this interval constant or increasing?', 'constant', 'Equal heights make a flat interval.'), ('A temperature graph reads −2, −4, −1. Give the minimum.', '-4', '−4 is lowest.')]
TAG="graph-interpretation" if 3==3 else "graph-construction"
def _practice(row,number):
    prompt,answer,memo=row
    return PracticeQuestion(id=f"g8-graphs-l03-p{number:02}",lesson_id=LESSON_ID,question_number=number,
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
    return AssessmentQuestion(id=f"g8-graphs-l03-{'m' if mastery else 'r'}{number:02}",number=number,prompt=prompt,
        marks=4 if mastery else None,answer=answer,solution=[memo,answer],verification=memo,
        misconception_tags=[TAG],accepted_answers=[answer.replace(" ",""),answer.replace("-","−")])
MASTERY_BANK=[_assessment(row,n,True) for n,row in enumerate(MASTERY_DATA,1)]
REASSESSMENT_BANK=[_assessment(row,n,False) for n,row in enumerate(REASSESSMENT_DATA,1)]
MISCONCEPTION_REPAIRS={TAG:{"diagnosis":"The axis, interval, direction, scale or domain was misread.",
    "repair":"Read the axis labels; identify the endpoints of one interval; calculate the vertical change and justify the domain."}}
REPAIR_RULES={TAG:"Reattempt with a new context and changed axis values; explain each interval before stating the answer."}
