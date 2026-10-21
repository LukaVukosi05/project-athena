"""Authored, server-gated diagnostic and cross-cluster assessment for Lesson 10."""
from __future__ import annotations
from pydantic import BaseModel, Field
from app.curriculum.grade8.lesson10_runtime import SOURCE_DATA, SOURCE
from app.practice.schemas import AnswerNormalisation, PracticeQuestion, WorkedSolutionStep

# The independent answer includes a diagnosis and the repaired mathematical result.
# These authored variants are intentionally strict about the first-error concept.
DIAGNOSTIC_ANSWERS = {
 1:['inverse-direction; a=21'],2:['division-by-coefficient-error; b=7'],
 3:['inverse-direction; c=6'],4:['division-by-coefficient-error; d=-7'],
 5:['first line correct; e=7','two-step-order-error; e=7'],
 6:['distribution-error; f=7'],7:['fraction-structure-error; g=20'],
 8:['context-model-error; 3h-6=24; h=10'],
 9:['context-model-error; x=4; 5cm by 4cm'],
 10:['classification-error; infinitely many solutions'],11:['classification-error; no solution'],
 12:['distribution-error; m=5'],13:['context-model-error; 25+7u=74; u=7'],
 14:['fraction-structure-error; n=32/3'],15:['distribution-error; p=12'],
}

def _practice(item):
    number=item['number']; solution=item['solution']
    return PracticeQuestion(
        id=item['id'],lesson_id=SOURCE_DATA['id'],question_number=number,
        difficulty='source_unspecified',cognitive_level='source_unspecified',marks=item['marks'],
        type='short_text',prompt=item['prompt'],
        accepted_answers=[item['answer'],*DIAGNOSTIC_ANSWERS[number]],
        answer_normalisation=AnswerNormalisation(),
        hints=[f"Compare consecutive learner lines. Focus on {item['misconception_tags'][0].replace('-', ' ')}.",
               solution[0]],
        worked_solution=[WorkedSolutionStep(expression=line,explanation=line,why=line,
                         verification=solution[-1] if index==len(solution)-1 else '')
                         for index,line in enumerate(solution)],
        misconception_tags=item['misconception_tags'],
        verification={'original_question_check':solution[-1]},
        correct_feedback='Correct diagnosis and repair.',source=SOURCE,
        answer_hidden_before_submission=True)
PRACTICE_BANK=[_practice(item) for item in SOURCE_DATA['practice_questions']]

class AssessmentQuestion(BaseModel):
    id: str = Field(pattern=r'^g8-ae-l10-[mr]\d{2}$')
    number: int = Field(ge=1,le=5)
    prompt: str
    marks: int | None = Field(default=None,ge=1,le=10)
    answer: str
    solution: list[str] = Field(min_length=1)
    verification: str = Field(min_length=1)
    misconception_tags: list[str] = Field(default_factory=list)
    accepted_answers: list[str] = Field(default_factory=list)
    def public(self): return self.model_dump(include={'id','number','prompt','marks'})

ASSESSMENT_TAGS={
 'm01':'inverse-direction','m02':'distribution-error','m03':'fraction-structure-error',
 'm04':'classification-error','m05':'context-model-error',
 'r01':'classification-error','r02':'distribution-error','r03':'context-model-error',
}
# For M05 the learner must state the correct fixed/variable model, hours and
# an explicit substitution into the original tariff; a bare '7' is not ready.
ALTERNATIVES={
 'm01':['inverse-direction; x=8'],
 'm02':['distribution-error; y=6'],
 'm03':['fraction-structure-error; z=12'],
 'm04':['no solution','classification-error; no solution'],
 'm05':['35+9h=98; h=7; 35+9(7)=98','35 + 9h = 98; h = 7 hours; check: 35 + 9(7) = 98'],
 'r01':['infinitely many solutions'],
 'r02':['distribution-error; c=10'],
 'r03':['40+6v=88; v=8 visits; 40+6(8)=88'],
}
def _assessment(item):
    suffix=item['id'].split('-')[-1]
    return AssessmentQuestion(**{**item,'verification':item['solution'][-1],
        'accepted_answers':ALTERNATIVES[suffix],
        'misconception_tags':[ASSESSMENT_TAGS[suffix]]})
MASTERY_BANK=[_assessment(item) for item in SOURCE_DATA['mastery_questions']]
REASSESSMENT_BANK=[_assessment(item) for item in SOURCE_DATA['reassessment_questions']]
MISCONCEPTION_REPAIRS={item['tag']:{'diagnosis':item['diagnosis'],'repair':item['repair']}
                        for item in SOURCE_DATA['misconceptions']}
REPAIR_RULES=SOURCE_DATA['repair_rules']
