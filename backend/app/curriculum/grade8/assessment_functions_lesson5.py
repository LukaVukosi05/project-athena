"""Private practice and checks for matching Grade 8 relationships."""
from app.curriculum.grade8.functions_relationships_lesson5 import LESSON_ID, SOURCE, DATA
from app.curriculum.grade8.assessment_expressions import AssessmentQuestion
from app.practice.schemas import AnswerNormalisation, PracticeQuestion, WorkedSolutionStep
PRACTICE=[
('Double x then add 4: output at x=3?', '10', '2×3+4=10.'),
('Add 4 then double: output at x=3?', '14', '2(3+4)=14.'),
('0→5,1→8,2→11: output at x=3?', '14', 'The rule 3x+5 gives 14.'),
('0→3,2→11: linear output at x=4?', '19', 'Rate (11−3)/2=4; 4×4+3=19.'),
('R10 fixed plus R3 per item: cost for 4 items in rand?', '22', '10+3×4=22.'),
('Square side n=4: number of unit squares?', '16', 'n²=4×4=16.'),
('Subtract 2 then triple: output at x=7?', '15', '3(7−2)=15.'),
('R25 once plus R4 per ticket: cost for 5 tickets?', '45', '25+4×5=45.'),
('Which is equivalent to 5(x+2): 5x+2 or 5x+10? Type the latter expression.', '5x+10', 'Distribute five to both terms: 5x+10.'),
('For y=2x+3, output at x=−2?', '-1', '2(−2)+3=−1.'),
('0→9,3→21: linear output at x=5?', '29', 'Rate 12/3=4; 9+4×5=29.'),
('A square side 6 has how many unit squares?', '36', 'Six rows of six give 36.'),
('Double then add 8: output at x=−4?', '0', '2(−4)+8=0.'),
('3(x−4) and 3x−12 at x=−2 both give what output?', '-18', '3(−2−4)=−18.'),
('Fixed R7 plus R6/km. Bill for 8 km in rand?', '55', '7+6×8=55.'),
]
MASTERY=[
('Add 5 then triple: output for x=2?', '21', '3(2+5)=21.'),
('0→8,2→14: linear output at x=4?', '20', 'Rate three, constant eight: 3×4+8=20.'),
('R11 fixed plus R4 per ride: total for 6 rides in rand?', '35', '11+4×6=35.'),
('Side n=7 square: area in unit squares?', '49', '7²=49.'),
('4(x−3) at x=−1 gives what output?', '-16', '4(−1−3)=−16.'),
]
REASSESS=[
('Subtract 3 then double: output at x=8?', '10', '2(8−3)=10.'),
('0→6,2→16: linear output at x=4?', '26', 'Rate five, constant six: 5×4+6=26.'),
('R9 once plus R7 per unit: cost for 3 units?', '30', '9+7×3=30.'),
]

def practice(row,n):
    prompt,answer,memo=row
    return PracticeQuestion(id=f'g8-fr-l05-p{n:02}',lesson_id=LESSON_ID,question_number=n,
        difficulty='foundation' if n<=3 else 'easy' if n<=6 else 'standard' if n<=9 else 'exam' if n<=12 else 'advanced',
        cognitive_level='knowledge' if n<=3 else 'routine' if n<=9 else 'complex',marks=2 if n<=6 else 4,
        type='short_text',prompt=prompt,accepted_answers=[answer],answer_normalisation=AnswerNormalisation(),
        hints=['Write the given representation and mark each operation in its order.',memo],
        worked_solution=[WorkedSolutionStep(expression='Identify the fixed and changing parts',explanation='Match the words or rows to an equation.',why='The same input must give the same output.'),
                         WorkedSolutionStep(expression=answer,explanation=memo,why='Verify using the original description.',verification=memo)],
        misconception_tags=[DATA['worked_examples'][n-1]['misconception']],verification={'original_question_check':memo},
        correct_feedback='Correct. This output matches the original representation.',source=SOURCE,answer_hidden_before_submission=True)
PRACTICE_BANK=[practice(row,n) for n,row in enumerate(PRACTICE,1)]

def assessment(row,n,mastery):
    q,a,memo=row
    return AssessmentQuestion(id=f'g8-fr-l05-{"m" if mastery else "r"}{n:02}',number=n,prompt=q,
       marks=4 if mastery else None,answer=a,solution=[memo,a],verification=memo,
       misconception_tags=['representation-match'],accepted_answers=[a])
MASTERY_BANK=[assessment(row,n,True) for n,row in enumerate(MASTERY,1)]
REASSESSMENT_BANK=[assessment(row,n,False) for n,row in enumerate(REASSESS,1)]
MISCONCEPTION_REPAIRS={'representation-match':{'diagnosis':'The rule order, zero output or context units were misread.',
    'repair':'Show the same input in each representation. Mark the fixed part and apply operations in order.'}}
REPAIR_RULES={'representation-match':'Retry a fresh words-to-flow problem and a table with a different input gap.'}
