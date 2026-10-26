"""Private authored Grade 8 Expressions Lesson 10 answer and assessment banks."""
from app.curriculum.grade8.algebraic_expressions_lesson10 import DATA,LESSON_ID,SOURCE
from app.curriculum.grade8.assessment_expressions import AssessmentQuestion
from app.practice.schemas import AnswerNormalisation,PracticeQuestion,WorkedSolutionStep

def practice(item,index):
    suffix,prompt,answer,hint,memo=item
    return PracticeQuestion(id=f'g8-ex-l10-{suffix}',lesson_id=LESSON_ID,
        question_number=index,difficulty='foundation' if index<=3 else 'easy' if index<=6 else 'standard' if index<=10 else 'exam' if index<=13 else 'advanced',
        cognitive_level='knowledge' if index<=3 else 'routine' if index<=10 else 'complex',
        marks=2 if index<=6 else 3 if index<=13 else 4,type='short_text',
        prompt=prompt,accepted_answers=[answer,answer.rstrip('.'),answer.replace(' ','').rstrip('.')],
        answer_normalisation=AnswerNormalisation(),
        hints=[hint,'Identify the first invalid action, repair it and check the original.'],
        worked_solution=[WorkedSolutionStep(expression=hint,explanation=hint,why=hint),
            WorkedSolutionStep(expression=answer,explanation=memo,why=memo,verification=memo)],
        misconception_tags=[DATA['worked_examples'][index-1]['misconception']],
        verification={'original_question_check':memo},
        correct_feedback='Correct. Verify the repair with the original expression or scenario.',source=SOURCE,
        answer_hidden_before_submission=True)

PRACTICE_BANK=[practice(item,n) for n,item in enumerate(DATA['practice_questions'],1)]

def assessment(item,number,mastery):
    if mastery: suffix,marks,prompt,answer,memo=item
    else: suffix,prompt,answer,memo=item;marks=None
    return AssessmentQuestion(id=f'g8-ex-l10-{suffix}',number=number,prompt=prompt,
        marks=marks,answer=answer,solution=[memo,answer],verification=memo,
        misconception_tags=['first-error-repair'],accepted_answers=[answer.rstrip('.')])

MASTERY_BANK=[assessment(item,n,True) for n,item in enumerate(DATA['mastery_questions'],1)]
REASSESSMENT_BANK=[assessment(item,n,False) for n,item in enumerate(DATA['reassessment_questions'],1)]
MISCONCEPTION_REPAIRS={item['id']:{'diagnosis':item['misconception'],'repair':item['repair']}
                        for item in DATA['worked_examples']}
MISCONCEPTION_REPAIRS['first-error-repair']={
    'diagnosis':'A transformation changes a sign, omits a factor, loses a restriction or reverses an operation.',
    'repair':'Locate the first invalid arrow, repair the operation and test with fresh values.'}
REPAIR_RULES={'first-error-repair':'Show the exact invalid move and require a parallel reassessment.'}
