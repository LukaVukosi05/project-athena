"""Private independent assessment for ordering and directed integer journeys."""
from app.curriculum.grade8.integers_runtime import build
from app.curriculum.grade8.assessment_expressions import AssessmentQuestion
from app.practice.schemas import AnswerNormalisation,PracticeQuestion,WorkedSolutionStep


def variant(scene,shift):
    if scene['model']=='integer_line':
        values=[v+shift for v in scene['values']]
        if scene['kind']=='distance':values[0]-=2*shift
        choice=scene['decision']
        answer=(max(values) if choice in ('larger','greatest') else min(values) if choice in ('smaller','least') else
                -values[0] if choice=='opposite' else abs(values[1]-values[0]))
        prompt=(f'Which is {choice} among {", ".join(map(str,values))}?' if choice not in ('opposite','distance') else
            f'What is the opposite of {values[0]}?' if choice=='opposite' else
            f'What is the integer distance between {values[0]} and {values[1]}?')
        memo=f'Plot {values} on an axis with zero. For {choice}, the requested value is {answer}.'
    else:
        start=scene['start']+shift
        current=start;path=[current]
        for sign,v in scene['operations']:
            current+=v if sign=='+' else -v;path.append(current)
        answer=current
        changes=', '.join(f'{sign} ({v})' for sign,v in scene['operations'])
        prompt=f'Start at {start}. Apply the signed operations in order: {changes}. What is the final integer?'
        memo=f'Draw every directed jump: {" → ".join(map(str,path))}. Verify the original operations to get {answer}.'
    return prompt,str(answer),memo


def banks(number):
    lesson,questions,scenes,source=build(number)
    tag='integer-order' if number==1 else 'integer-sign-jump'
    practice=[]
    for index,scene in enumerate(scenes,1):
        prompt,answer,memo=variant(scene,2)
        practice.append(PracticeQuestion(id=f'g8-int-l{number:02}-p{index:02}',lesson_id=lesson.id,
            question_number=index,difficulty=questions[index-1].difficulty,cognitive_level=questions[index-1].cognitive_level,
            marks=questions[index-1].marks,type='short_text',prompt=prompt,accepted_answers=[answer],
            answer_normalisation=AnswerNormalisation(),hints=['Mark zero and every given signed value first.',
                'Keep earlier values or arrows visible while you check the next operation.'],
            worked_solution=[WorkedSolutionStep(expression='Label the axis',explanation='Use the given signed values.',why='A shifted practice problem needs a new axis.'),
                WorkedSolutionStep(expression=answer,explanation=memo,why=memo,verification=memo)],
            misconception_tags=[tag],verification={'original_question_check':memo},
            correct_feedback='Correct; the signed positions agree with the original question.',
            source=source.name,answer_hidden_before_submission=True))
    def assess(scene,i,prefix):
        prompt,answer,memo=variant(scene,4 if prefix=='m' else 6)
        return AssessmentQuestion(id=f'g8-int-l{number:02}-{prefix}{i:02}',number=i,
            prompt=prompt,marks=4 if prefix=='m' else None,answer=answer,solution=[memo,answer],
            verification=memo,misconception_tags=[tag],accepted_answers=[answer])
    mastery=[assess(s,i,'m') for i,s in enumerate(scenes[7:12],1)]
    parallel=[assess(s,i,'r') for i,s in enumerate(scenes[12:15],1)]
    repairs={tag:{'diagnosis':'The first signed position or jump was placed on the wrong side of zero.',
        'repair':'Return to the first mismatched tick, label zero, rebuild every directed movement and retry new values.'}}
    rules={tag:'Use a parallel line with new values and explain the first incorrect sign choice.'}
    return practice,mastery,parallel,repairs,rules


PRACTICE_1,MASTERY_1,REASSESSMENT_1,REPAIRS_1,RULES_1=banks(1)
PRACTICE_2,MASTERY_2,REASSESSMENT_2,REPAIRS_2,RULES_2=banks(2)
