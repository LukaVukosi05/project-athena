"""Private practice and assessment answers for the fourth functions lesson."""
from app.curriculum.grade8.functions_relationships_lesson4 import LESSON_ID, SOURCE, DATA
from app.curriculum.grade8.assessment_expressions import AssessmentQuestion
from app.practice.schemas import AnswerNormalisation, PracticeQuestion, WorkedSolutionStep

PRACTICE = [
    ('Rectangle 6 cm by 3 cm: area in cm²?', '18','6 × 3 = 18 cm².'),
    ('Rectangle 8 m by 5 m: area in m²?', '40','8 × 5 = 40 m².'),
    ('Area 28 cm², width 4 cm: length in cm?', '7','28 ÷ 4 = 7 cm.'),
    ('Area 63 m², length 9 m: width in m?', '7','63 ÷ 9 = 7 m.'),
    ('Area 45 cm², width 5 cm: length in cm?', '9','45 ÷ 5 = 9 cm.'),
    ('Rectangle 7 cm by 4 cm: perimeter in cm?', '22','2(7 + 4) = 22 cm.'),
    ('Area 72 m², width 8 m: length in m?', '9','72 ÷ 8 = 9 m.'),
    ('Area 9 m², width 2.25 m: length in m?', '4','9 ÷ 2.25 = 4 m.'),
    ('Rectangle length (x+3) cm and width 2 cm: area at x=5, in cm²?', '16','2(5 + 3) = 16 cm².'),
    ('Area 48 m², width 6 m, tiles R50/m²: total tile cost in rand?', '2400','48 × 50 = R2400.'),
    ('Perimeter 34 cm, length 10 cm: width in cm?', '7','34 ÷ 2 − 10 = 7 cm.'),
    ('Area 50 cm², length 10 cm: perimeter in cm?', '30','Width = 5 cm, so P = 2(10 + 5) = 30 cm.'),
    ('Area 98 cm², length twice width: positive width in cm?', '7','2w² = 98, hence w² = 49 and w = 7 cm.'),
    ('If x=4, length (x+6) cm and width x cm: area in cm²?', '40','(4 + 6) × 4 = 40 cm².'),
    ('Area 80 m², width 2 m less than length: whole-number length in m?', '10','10 × (10 − 2) = 80 m².'),
]

def practice(row,n):
    prompt,answer,memo=row
    return PracticeQuestion(id=f'g8-fr-l04-p{n:02}',lesson_id=LESSON_ID,question_number=n,
        difficulty='foundation' if n<=3 else 'easy' if n<=6 else 'standard' if n<=9 else 'exam' if n<=12 else 'advanced',
        cognitive_level='knowledge' if n<=3 else 'routine' if n<=9 else 'complex',marks=2 if n<=6 else 4,
        type='short_text',prompt=prompt,accepted_answers=[answer],answer_normalisation=AnswerNormalisation(),
        hints=['Label the area, length and width in the correct formula slots.',memo],
        worked_solution=[WorkedSolutionStep(expression='Identify the known quantities',explanation='Use area or perimeter as appropriate.',why='The units identify the kind of measurement.'),
            WorkedSolutionStep(expression=answer,explanation=memo,why='Check against the original measurements.',verification=memo)],
        misconception_tags=[DATA['worked_examples'][n-1]['misconception']],verification={'original_question_check':memo},
        correct_feedback='Correct. The result matches the original rectangle.',source=SOURCE,answer_hidden_before_submission=True)

PRACTICE_BANK=[practice(row,n) for n,row in enumerate(PRACTICE,1)]
MASTERY=[
    ('Area 42 cm², width 6 cm: length in cm?', '7','7 × 6 = 42 cm².'),
    ('A rectangle 11 m long and 4 m wide: perimeter in m?', '30','2(11 + 4) = 30 m.'),
    ('Area 80 m², length 10 m: width in m?', '8','10 × 8 = 80 m².'),
    ('Perimeter 46 cm, length 15 cm: width in cm?', '8','46 ÷ 2 − 15 = 8 cm.'),
    ('Area 75 m², width 5 m; tile cost R60 per m²: total tile cost in rand?', '4500','75 × 60 = R4500.'),
]
REASSESS=[
    ('Area 56 cm², width 7 cm: length in cm?', '8','8 × 7 = 56 cm².'),
    ('Perimeter 38 m, length 12 m: width in m?', '7','38 ÷ 2 − 12 = 7 m.'),
    ('Area 36 m² and price R70/m²: total cost in rand?', '2520','36 × 70 = R2520.'),
]

def assessment(row,n,mastery):
    prompt,answer,memo=row
    return AssessmentQuestion(id=f'g8-fr-l04-{"m" if mastery else "r"}{n:02}',number=n,
        prompt=prompt,marks=4 if mastery else None,answer=answer,
        solution=[memo,answer],verification=memo,misconception_tags=['formula-direction-and-units'],accepted_answers=[answer])
MASTERY_BANK=[assessment(row,n,True) for n,row in enumerate(MASTERY,1)]
REASSESSMENT_BANK=[assessment(row,n,False) for n,row in enumerate(REASSESS,1)]
MISCONCEPTION_REPAIRS={'formula-direction-and-units':{'diagnosis':'Area and perimeter were confused, or the formula was used in the wrong direction.',
    'repair':'Draw and label the rectangle; use square units for area, divide area by a known side, and verify by multiplying back.'}}
REPAIR_RULES={'formula-direction-and-units':'Retry fresh dimensions and a separate area-to-side inverse problem.'}
