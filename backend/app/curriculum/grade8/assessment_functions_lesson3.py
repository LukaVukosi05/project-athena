"""Private keys for Grade 8 rule-finding practice and assessments."""
from app.curriculum.grade8.functions_relationships_lesson3 import DATA,LESSON_ID,SOURCE
from app.curriculum.grade8.assessment_expressions import AssessmentQuestion
from app.practice.schemas import AnswerNormalisation,PracticeQuestion,WorkedSolutionStep

def practice(item,index):
    suffix,prompt,answer,hint,memo=item
    return PracticeQuestion(id=f'g8-fr-l03-{suffix}',lesson_id=LESSON_ID,question_number=index,
        difficulty='foundation' if index<=3 else 'easy' if index<=6 else 'standard' if index<=10 else 'exam' if index<=13 else 'advanced',
        cognitive_level='knowledge' if index<=3 else 'routine' if index<=10 else 'complex',
        marks=2 if index<=6 else 3 if index<=13 else 4,type='short_text',prompt=prompt,
        accepted_answers=[answer,answer.rstrip('.'),answer.replace(' ','').rstrip('.')],
        answer_normalisation=AnswerNormalisation(),
        hints=[hint,'Check both input and output step sizes, and test every supplied row.'],
        worked_solution=[WorkedSolutionStep(expression=hint,explanation=hint,why=hint),
            WorkedSolutionStep(expression=answer,explanation=memo,why=memo,verification=memo)],
        misconception_tags=[DATA['worked_examples'][index-1]['misconception']],
        verification={'original_question_check':memo},
        correct_feedback='Correct. Your rule agrees with the stated pairs and assumptions.',
        source=SOURCE,answer_hidden_before_submission=True)

PRACTICE_BANK=[practice(row,n) for n,row in enumerate(DATA['practice_questions'],1)]

def assessment(row,index,mastery):
    if mastery:suffix,marks,prompt,answer,memo=row
    else:suffix,prompt,answer,memo=row;marks=None
    return AssessmentQuestion(id=f'g8-fr-l03-{suffix}',number=index,prompt=prompt,marks=marks,
        answer=answer,solution=[memo,answer],verification=memo,
        misconception_tags=['table-rule-evidence'],accepted_answers=[answer.rstrip('.')])

MASTERY_BANK=[assessment(row,n,True) for n,row in enumerate(DATA['mastery_questions'],1)]
REASSESSMENT_BANK=[assessment(row,n,False) for n,row in enumerate(DATA['reassessment_questions'],1)]
MISCONCEPTION_REPAIRS={row['id']:{'diagnosis':row['misconception'],'repair':row['repair']}
    for row in DATA['worked_examples']}
MISCONCEPTION_REPAIRS['table-rule-evidence']={
    'diagnosis':'The rule ignores step width, signed inputs or a contradictory row.',
    'repair':'Align the rows, calculate changes per input unit and test the new rule on each displayed pair.'}
REPAIR_RULES={'table-rule-evidence':'Use a new table with different step widths and reassess independently.'}
