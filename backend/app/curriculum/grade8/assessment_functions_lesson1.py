"""Private Grade 8 functions Lesson 1 answer and assessment banks."""
from app.curriculum.grade8.functions_relationships_lesson1 import DATA, LESSON_ID, SOURCE
from app.curriculum.grade8.assessment_expressions import AssessmentQuestion
from app.practice.schemas import AnswerNormalisation, PracticeQuestion, WorkedSolutionStep


def practice(item,index):
    suffix,prompt,answer,hint,memo=item
    return PracticeQuestion(id=f'g8-fr-l01-{suffix}',lesson_id=LESSON_ID,
        question_number=index,difficulty='foundation' if index<=3 else 'easy' if index<=6 else 'standard' if index<=10 else 'exam' if index<=13 else 'advanced',
        cognitive_level='knowledge' if index<=3 else 'routine' if index<=10 else 'complex',
        marks=2 if index<=6 else 3 if index<=13 else 4,type='short_text',
        prompt=prompt,accepted_answers=[answer,answer.rstrip('.'),answer.replace(' ','').rstrip('.')],
        answer_normalisation=AnswerNormalisation(),
        hints=[hint,'Trace the original rule in order, then check a new input.'],
        worked_solution=[WorkedSolutionStep(expression=hint,explanation=hint,why=hint),
            WorkedSolutionStep(expression=answer,explanation=memo,why=memo,verification=memo)],
        misconception_tags=[DATA['worked_examples'][index-1]['misconception']],
        verification={'original_question_check':memo},
        correct_feedback='Correct. The input and output agree with the given rule.',
        source=SOURCE,answer_hidden_before_submission=True)


PRACTICE_BANK=[practice(item,i) for i,item in enumerate(DATA['practice_questions'],1)]


def assessment(item,index,mastery):
    if mastery:suffix,marks,prompt,answer,memo=item
    else:suffix,prompt,answer,memo=item;marks=None
    return AssessmentQuestion(id=f'g8-fr-l01-{suffix}',number=index,prompt=prompt,marks=marks,
        answer=answer,solution=[memo,answer],verification=memo,
        misconception_tags=['relationship-rule-order'],accepted_answers=[answer.rstrip('.')])


MASTERY_BANK=[assessment(item,i,True) for i,item in enumerate(DATA['mastery_questions'],1)]
REASSESSMENT_BANK=[assessment(item,i,False) for i,item in enumerate(DATA['reassessment_questions'],1)]
MISCONCEPTION_REPAIRS={item['id']:{'diagnosis':item['misconception'],'repair':item['repair']}
    for item in DATA['worked_examples']}
MISCONCEPTION_REPAIRS['relationship-rule-order']={
    'diagnosis':'An input-output rule is read in the wrong direction, order or context.',
    'repair':'Trace each arrow with intermediate values and verify the input in the original rule.'}
REPAIR_RULES={'relationship-rule-order':'Rebuild the rule visually and solve a parallel flow or table.'}
