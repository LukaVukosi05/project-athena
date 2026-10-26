"""Private authoring answers for Grade 8 Algebraic Expressions Lesson 1."""
from __future__ import annotations
from pydantic import BaseModel, Field
from app.curriculum.grade8.algebraic_expressions import DATA, LESSON_ID, SOURCE
from app.practice.schemas import AnswerNormalisation, PracticeQuestion, WorkedSolutionStep


def practice(item, memo, index):
    suffix, prompt, answer, guide = item
    return PracticeQuestion(id=f'g8-ex-l01-{suffix.lower()}', lesson_id=LESSON_ID,
        question_number=index, difficulty=('foundation' if index<=3 else 'easy' if index<=6 else
            'standard' if index<=10 else 'exam' if index<=13 else 'advanced'),
        cognitive_level='knowledge' if index<=3 else 'routine' if index<=10 else 'complex',
        marks=2 if index<=6 else 3 if index<=13 else 4, type='short_text', prompt=prompt,
        accepted_answers=[answer, answer.rstrip('.'), answer.replace(' ', '').rstrip('.')],
        answer_normalisation=AnswerNormalisation(),
        hints=[f'Locate the relevant quantities: {guide.split(";")[0]}',
               f'Use the mathematical relationship: {guide}'],
        worked_solution=[WorkedSolutionStep(expression=guide,explanation=guide,why=guide),
            WorkedSolutionStep(expression=answer,explanation=memo,why=memo,verification=memo)],
        misconception_tags=[DATA['examples'][index-1]['misconception']],
        verification={'original_question_check':memo}, correct_feedback='Correct. Check the original question.',
        source=SOURCE, answer_hidden_before_submission=True)

PRACTICE_BANK=[practice(item,memo,n) for n,(item,memo) in enumerate(zip(DATA['practice'], DATA['practice_memos']),1)]

class AssessmentQuestion(BaseModel):
    id: str
    number: int = Field(ge=1,le=5)
    prompt: str
    marks: int | None = Field(default=None,ge=1,le=10)
    answer: str
    solution: list[str]
    verification: str
    misconception_tags: list[str]
    accepted_answers: list[str]
    def public(self):
        return self.model_dump(include={'id','number','prompt','marks'})

def assessment(item, number, prefix):
    suffix, *rest=item
    if prefix=='m': marks,prompt,answer,memo=rest
    else: prompt,answer,memo=rest;marks=None
    return AssessmentQuestion(id=f'g8-ex-l01-{suffix.lower()}',number=number,
        prompt=prompt,marks=marks,answer=answer,solution=[memo,answer],
        verification=memo,misconception_tags=['expression-reading'],accepted_answers=[answer.rstrip('.')])

MASTERY_BANK=[assessment(item,n,'m') for n,item in enumerate(DATA['mastery'],1)]
REASSESSMENT_BANK=[assessment(item,n,'r') for n,item in enumerate(DATA['parallel'],1)]
MISCONCEPTION_REPAIRS={item['id']:{'diagnosis':item['misconception'],'repair':item['repair']} for item in DATA['examples']}
REPAIR_RULES={'expression-reading': 'Rebuild the given objects, locate the first incorrect mathematical action and try the parallel reassessment.'}
