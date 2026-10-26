"""Private original Grade 8 equivalent-forms assessment keys."""
from app.curriculum.grade8.functions_relationships_lesson2 import DATA, LESSON_ID, SOURCE
from app.curriculum.grade8.assessment_expressions import AssessmentQuestion
from app.practice.schemas import AnswerNormalisation, PracticeQuestion, WorkedSolutionStep


def practice(item,index):
    suffix,prompt,answer,hint,memo=item
    return PracticeQuestion(id=f'g8-fr-l02-{suffix}',lesson_id=LESSON_ID,
        question_number=index,difficulty='foundation' if index<=3 else 'easy' if index<=6 else 'standard' if index<=10 else 'exam' if index<=13 else 'advanced',
        cognitive_level='knowledge' if index<=3 else 'routine' if index<=10 else 'complex',
        marks=2 if index<=6 else 3 if index<=13 else 4,type='short_text',prompt=prompt,
        accepted_answers=[answer,answer.rstrip('.'),answer.replace(' ','').rstrip('.')],
        answer_normalisation=AnswerNormalisation(),
        hints=[hint,'Use the same input in each representation. A single mismatch disproves equivalence.'],
        worked_solution=[WorkedSolutionStep(expression=hint,explanation=hint,why=hint),
            WorkedSolutionStep(expression=answer,explanation=memo,why=memo,verification=memo)],
        misconception_tags=[DATA['worked_examples'][index-1]['misconception']],
        verification={'original_question_check':memo},
        correct_feedback='Correct. Your representations agree on the justified domain or your counterexample disproves the claim.',
        source=SOURCE,answer_hidden_before_submission=True)

PRACTICE_BANK=[practice(row,n) for n,row in enumerate(DATA['practice_questions'],1)]


def assessment(row,index,mastery):
    if mastery:suffix,marks,prompt,answer,memo=row
    else:suffix,prompt,answer,memo=row;marks=None
    return AssessmentQuestion(id=f'g8-fr-l02-{suffix}',number=index,prompt=prompt,marks=marks,
        answer=answer,solution=[memo,answer],verification=memo,
        misconception_tags=['equivalent-representations'],accepted_answers=[answer.rstrip('.')])

MASTERY_BANK=[assessment(row,n,True) for n,row in enumerate(DATA['mastery_questions'],1)]
REASSESSMENT_BANK=[assessment(row,n,False) for n,row in enumerate(DATA['reassessment_questions'],1)]
MISCONCEPTION_REPAIRS={row['id']:{'diagnosis':row['misconception'],'repair':row['repair']}
    for row in DATA['worked_examples']}
MISCONCEPTION_REPAIRS['equivalent-representations']={
    'diagnosis':'Two representations have been assumed identical without preserving operation order or domain.',
    'repair':'Construct both flows with the same input, then use an identity or counterexample as appropriate.'}
REPAIR_RULES={'equivalent-representations':'Rebuild both representations and solve a parallel translation problem.'}
