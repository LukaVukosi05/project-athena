"""Independent Grade 8 global-graph assessment with private solution keys."""
from app.curriculum.grade8.graphs_lesson5 import LESSON_ID, SOURCE, QUESTIONS
from app.curriculum.grade8.assessment_expressions import AssessmentQuestion
from app.practice.schemas import AnswerNormalisation, PracticeQuestion, WorkedSolutionStep
PRACTICE=[('Pump A adds 8 L and B adds 6 L over the same hour. Which adds more?', 'A', 'Compare changes over the same hour: 8 > 6.'), ('At minute 2, cyclist A is 9 km away and B is 12 km away. Who is farther?', 'B', 'Compare at x = 2: 12 > 9.'), ('Two temperatures rise from 2°C to 8°C and 5°C to 9°C. Which rises more?', 'A', 'A rises 6°C; B rises 4°C.'), ('Two candles fall from 15 to 10 cm and 15 to 8 cm. Which loses more height?', 'B', 'The losses are 5 and 7 cm.'), ('At week 3, jar A has R12 and jar B R11. Which has more?', 'A', 'Compare the two outputs at week 3.'), ('Two runners start at 0; A finishes at 18 m and B at 21 m. Who ran farther?', 'B', 'At the same end time, 21 > 18.'), ('At day 2, reservoir A has 5 ML and B has 7 ML. Which is lower?', 'A', 'Compare vertically at day 2.'), ('From week 1 to 2, plant A grows from 4 to 8 cm and B from 5 to 10 cm. Which grows more?', 'B', 'A grows 4 cm; B grows 5 cm.'), ('Taxi A changes from 6 to 6 km and B from 4 to 9 km over hour 1 to 2. Which travels farther?', 'B', 'A changes 0; B changes 5 km.'), ('At hour 3, battery A is 35% and B 28%. Which retains more?', 'A', '35% exceeds 28% at the same hour.'), ('Gauge A rises from 4 to 10 mm in the final hour, while B rises 8 to 11 mm. Which adds more?', 'A', 'A adds 6 mm and B adds 3 mm.'), ('At minute 2, queue A holds 9 people and B holds 12. Which is larger?', 'B', 'Compare integer counts at the same minute.'), ('At hour 3, freezer A is −8°C and B is −6°C. Which is colder?', 'A', '−8°C lies below −6°C.'), ('From hour 1 to 2, cyclist A goes 5 to 11 km and B 6 to 13 km. Which gains more distance?', 'B', 'A gains 6; B gains 7 km.'), ('Pump A goes from 3 to 17 L and pump B from 2 to 15 L. Which adds more overall?', 'A', 'A adds 14 L; B adds 13 L.')]
MASTERY_DATA=[('A rises from 0 to 8 and B from 0 to 6. Which rises more?', 'A', '8 > 6.'), ('At x = 2, A = 5 and B = 7. Which is higher?', 'B', '7 > 5.'), ('A falls by 4 and B by 9. Which falls more?', 'B', '9 > 4.'), ('A and B are both 10 at x = 3. Are they equal then? Answer yes or no.', 'yes', 'Same input and output.'), ('A goes 4 to 12 and B goes 2 to 9. Which gains more?', 'A', '8 > 7.')]
REASSESSMENT_DATA=[('At day 2, A has 7 and B 9. Which is higher?', 'B', '9 > 7.'), ('A goes 2 to 8; B goes 4 to 7. Which rises more?', 'A', 'A rises 6 and B 3.'), ('A is −4°C and B −2°C. Which is colder?', 'A', '−4 lies lower.')]
TAG="graph-comparison" if 5==5 else "graph-claim-repair"
def _practice(row,number):
    prompt,answer,memo=row
    return PracticeQuestion(id=f"g8-graphs-l05-p{number:02}",lesson_id=LESSON_ID,question_number=number,
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
    return AssessmentQuestion(id=f"g8-graphs-l05-{'m' if mastery else 'r'}{number:02}",number=number,prompt=prompt,
        marks=4 if mastery else None,answer=answer,solution=[memo,answer],verification=memo,
        misconception_tags=[TAG],accepted_answers=[answer.replace(" ",""),answer.replace("-","−")])
MASTERY_BANK=[_assessment(row,n,True) for n,row in enumerate(MASTERY_DATA,1)]
REASSESSMENT_BANK=[_assessment(row,n,False) for n,row in enumerate(REASSESSMENT_DATA,1)]
MISCONCEPTION_REPAIRS={TAG:{"diagnosis":"The axis, interval, direction, scale or domain was misread.",
    "repair":"Read the axis labels; identify the endpoints of one interval; calculate the vertical change and justify the domain."}}
REPAIR_RULES={TAG:"Reattempt with a new context and changed axis values; explain each interval before stating the answer."}
