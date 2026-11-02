"""Private practice and checks for first-error relationship diagnosis."""
from app.curriculum.grade8.functions_relationships_lesson6 import LESSON_ID, SOURCE, DATA
from app.curriculum.grade8.assessment_expressions import AssessmentQuestion
from app.practice.schemas import AnswerNormalisation, PracticeQuestion, WorkedSolutionStep
PRACTICE=[
('A learner says double then add 2 gives 2(x+2). Correct output at x=3?', '8', '2×3+2=8; the learner would get 10.'),
('0→7,1→9: learner writes 7x+2. Correct output at x=2?', '11', 'Use 2x+7, so at two the output is 11.'),
('Add 1 then triple: learner writes 3x+1. Correct output at x=2?', '9', '3(2+1)=9.'),
('0→5,2→13: learner calls rate 8. Correct output at x=3?', '17', 'Rate 8÷2=4 and fixed value 5: 4×3+5=17.'),
('R6 once plus R3 per visit. Learner charges 6v+3. Correct for v=4?', '18', '6+3×4=18.'),
('−1→−2,0→1,1→4: learner rule 3x−1. Correct output x=2?', '7', 'The zero row makes the constant +1; 3×2+1=7.'),
('y=x²+1 at x=3: learner claims outputs change by two each input. Correct output?', '10', '3²+1=10; the differences grow.'),
('Learner expands 3(x+4) as 3x+4. Correct output at x=2?', '18', '3×2+12=18.'),
('Perimeter 26 cm and length 9 cm: learner says width 17. Correct width in cm?', '4', 'Half the perimeter is 13; 13−9=4.'),
('0→3,1→4,2→7: learner chooses x+3. Correct output at x=2?', '7', 'x²+3 gives 7, while x+3 gives 5.'),
('Square side 5: learner uses 4n for area. Correct area in unit squares?', '25', '5²=25; 4×5 is perimeter.'),
('Output 23 after tripling then adding 5: learner divides by 3 first. Correct input?', '6', '(23−5)÷3=6.'),
('−1→0,0→1,1→4: learner claims x²+1. Correct output at x=1?', '4', 'x²+2x+1 gives 4; learner gives 2.'),
('R14 fixed plus R2 per item: learner uses 14x+2. Correct for x=5?', '24', '14+2×5=24.'),
('Learner writes 4(x−3)=4x−3. Correct value at x=5?', '8', '4(5−3)=8; correct expansion is 4x−12.'),
]
MASTERY=[
('Double then add 5: learner writes 2(x+5). Correct output x=4?', '13', '2×4+5=13.'),
('0→4,2→10: learner calls rate six. Correct output x=4?', '16', 'Rate 6/2=3; 3×4+4=16.'),
('A square side 8: learner gives perimeter as area. Correct area?', '64', '8×8=64 square units.'),
('Output 19 from x→×2→+3. Correct input?', '8', '(19−3)/2=8.'),
('R12 once plus R5 per trip: learner multiplies twelve. Correct for 4 trips?', '32', '12+5×4=32.'),
]
REASSESS=[
('Add 4 then double: learner writes 2x+4. Correct at x=3?', '14', '2(3+4)=14.'),
('0→9,3→18: learner rate nine. Correct output at x=5?', '24', 'Rate three: 9+3×5=24.'),
('Square side 6: learner uses 4n as area. Correct area?', '36', '6×6=36.'),
]

def practice(row,n):
    prompt,answer,memo=row
    return PracticeQuestion(id=f'g8-fr-l06-p{n:02}',lesson_id=LESSON_ID,question_number=n,
        difficulty='foundation' if n<=3 else 'easy' if n<=6 else 'standard' if n<=9 else 'exam' if n<=12 else 'advanced',
        cognitive_level='knowledge' if n<=3 else 'routine' if n<=9 else 'complex',marks=2 if n<=6 else 4,
        type='short_text',prompt=prompt,accepted_answers=[answer],answer_normalisation=AnswerNormalisation(),
        hints=['Compare the learner step to the complete original rule; stop at the first mismatch.',memo],
        worked_solution=[WorkedSolutionStep(expression='Check the first learner move',explanation='Test a given input or the operation order.',why='Later lines inherit an earlier error.'),
                         WorkedSolutionStep(expression=answer,explanation=memo,why='Verify with the original input or given row.',verification=memo)],
        misconception_tags=[DATA['worked_examples'][n-1]['misconception']],verification={'original_question_check':memo},
        correct_feedback='Correct. You repaired the original relationship.',source=SOURCE,answer_hidden_before_submission=True)
PRACTICE_BANK=[practice(row,n) for n,row in enumerate(PRACTICE,1)]

def assessment(row,n,mastery):
    q,a,memo=row
    return AssessmentQuestion(id=f'g8-fr-l06-{"m" if mastery else "r"}{n:02}',number=n,prompt=q,
      marks=4 if mastery else None,answer=a,solution=[memo,a],verification=memo,
      misconception_tags=['first-error-relationship'],accepted_answers=[a])
MASTERY_BANK=[assessment(row,n,True) for n,row in enumerate(MASTERY,1)]
REASSESSMENT_BANK=[assessment(row,n,False) for n,row in enumerate(REASSESS,1)]
MISCONCEPTION_REPAIRS={'first-error-relationship':{'diagnosis':'The earliest wrong operation, rate, fixed fee or formula was accepted without checking the original.',
 'repair':'Pause at the first changed line. Check a given row, mark the incorrect operation, then solve a fresh parallel example.'}}
REPAIR_RULES={'first-error-relationship':'Reassess operation order, table rate and area interpretation with fresh values.'}
