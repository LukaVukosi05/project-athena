"""Private four-option practice and assessment banks from the authored packs."""
from pydantic import BaseModel, Field
from app.curriculum.grade9.whole_numbers_runtime import DATA_1,DATA_2,LESSON_1,LESSON_2,EXTENDED,INTEGER_LESSONS
from app.practice.schemas import PracticeQuestion,WorkedSolutionStep


class AssessmentQuestion(BaseModel):
    id:str
    number:int=Field(ge=1,le=5)
    prompt:str
    options:list[str]=Field(min_length=4,max_length=4)
    marks:int|None=None
    answer:str
    solution:list[str]
    verification:str
    misconception_tags:list[str]
    accepted_answers:list[str]
    def public(self):
        return self.model_dump(include={'id','number','prompt','options','marks'})


def banks(number,topic='whole-numbers'):
    lesson,data=INTEGER_LESSONS[number] if topic=='integers' else (LESSON_1,DATA_1) if number==1 else (LESSON_2,DATA_2) if number==2 else EXTENDED[number]
    tag=f'grade9-integers-{number:02}' if topic=='integers' else 'number-set-classification' if number==1 else 'prime-power-selection' if number==2 else f'grade9-whole-numbers-{number:02}'
    practice=[]
    for index,item in enumerate(data['practice'],1):
        reason=item['memo'].split('. ',1)[-1]
        correct=item['options'][item['answer_index']]
        practice.append(PracticeQuestion(id=item['id'],lesson_id=lesson.id,question_number=index,
            difficulty=lesson.whiteboard_questions[index-1].difficulty,
            cognitive_level=lesson.whiteboard_questions[index-1].cognitive_level,marks=2 if index<=5 else 3,
            type='multiple_choice',prompt=item['prompt'],options=item['options'],accepted_answers=[correct],
            hints=['Write the original signed quantities and one operation in your book before choosing.' if topic=='integers' else 'Write or factorise the exact number in your book before choosing.',
                   'Check sign, parentheses and the first incorrect step against the original question.' if topic=='integers' else 'Check whether the question asks for the smallest set, HCF, LCM or a context quantity.'],
            worked_solution=[WorkedSolutionStep(expression=item['prompt'],explanation='Start with the original givens.',why='A choice without working may hide a misconception.'),
                WorkedSolutionStep(expression=correct,explanation=reason,why=reason,verification=reason)],
            misconception_tags=[tag],verification={'original_question_check':reason},
            correct_feedback='Correct. Compare your written method with the worked review.',source=data['source'],
            answer_hidden_before_submission=True))
    def assessment(item,index,prefix):
        correct=item['options'][item['answer_index']]
        reason=item['memo'].split('. ',1)[-1]
        return AssessmentQuestion(id=item['id'],number=index,prompt=item['prompt'],options=item['options'],
            marks=4 if prefix=='m' else None,answer=correct,accepted_answers=[correct],
            solution=[reason,correct],verification=reason,misconception_tags=[tag])
    mastery=[assessment(item,i,'m') for i,item in enumerate(data['mastery'],1)]
    reassessment=[assessment(item,i,'r') for i,item in enumerate(data['reassessment'],1)]
    repairs={tag:{'diagnosis':'Check the first sign, grouping or operation that differs from the original expression.' if topic=='integers' else 'The first incorrect choice used the wrong mathematical classification or prime-power rule.',
        'repair':'Rewrite the signed operation, show its correct result and retry with changed numbers.' if topic=='integers' else 'Rebuild the exact value or every prime tree, identify the first incorrect step, then retry changed numbers.'}}
    rules={tag:'Use a parallel item with new numbers; verify the result against all original givens.'}
    return practice,mastery,reassessment,repairs,rules


PRACTICE_1,MASTERY_1,REASSESSMENT_1,REPAIRS_1,RULES_1=banks(1)
PRACTICE_2,MASTERY_2,REASSESSMENT_2,REPAIRS_2,RULES_2=banks(2)
EXTENDED_BANKS={number:banks(number) for number in range(3,9)}
INTEGER_BANKS={number:banks(number,'integers') for number in range(1,6)}
