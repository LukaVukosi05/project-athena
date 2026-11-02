"""Independent, private assessments for the two whole-number lessons."""
from math import gcd,lcm
from app.curriculum.grade8.whole_numbers_runtime import build
from app.curriculum.grade8.assessment_expressions import AssessmentQuestion
from app.practice.schemas import AnswerNormalisation,PracticeQuestion,WorkedSolutionStep


def property_value(scene, increase):
    kind=scene['kind'];a,b,c=scene['values'];a+=increase
    if kind=='zero_div':return 'undefined'
    if kind in ('comm_add','add_identity'):return str(a+b)
    if kind=='assoc_add':return str(a+b+c)
    if kind=='assoc_mul':return str(a*b*c)
    if kind=='dist':return str(a*(b+c))
    return str(a*b)


def expression(kind,a,b,c):
    return {'comm_add':f'{a}+{b} and {b}+{a}', 'comm_mul':f'{a}×{b} and {b}×{a}',
        'assoc_add':f'({a}+{b})+{c} and {a}+({b}+{c})',
        'assoc_mul':f'({a}×{b})×{c} and {a}×({b}×{c})',
        'dist':f'{a}×({b}+{c}) and {a}×{b}+{a}×{c}',
        'add_identity':f'{a}+0', 'mul_identity':f'{a}×1', 'zero_div':f'{a}÷0'}[kind]


def factor_value(scene,multiplier):
    if scene['kind']=='largest_prime':
        # Prime-factor cases here have a largest leaf above all assessment multipliers.
        return str(max(scene['factors'][0]))
    values=[x*multiplier for x in scene['numbers']]
    return str(gcd(*values) if scene['kind']=='hcf' else lcm(*values))


def banks(number):
    lesson,questions,scenes,source=build(number)
    practice=[]
    for index,scene in enumerate(scenes,1):
        if number==1:
            a,b,c=scene['values'];a+=1
            answer=property_value(scene,1)
            expr=expression(scene['kind'],a,b,c)
            prompt=f'With new values, calculate {expr}. Give the result (or undefined), then name the property in your working.'
            memo=f'{expr}: {answer}. The original property remains {scene["property"]}.'
            tag='whole-property-confusion'
        else:
            nums=[v*2 for v in scene['numbers']]
            answer=factor_value(scene,2)
            prompt=(f'Find the largest prime factor of {nums[0]}; show its factor tree.' if scene['kind']=='largest_prime' else
                    f'Find the {scene["kind"].upper()} of {", ".join(map(str,nums))} by prime factorisation.')
            memo=f'The new roots are {nums}. Factor each into primes and select the {scene["kind"]} to obtain {answer}.'
            tag='hcf-lcm-prime-powers'
        practice.append(PracticeQuestion(id=f'g8-whole-l{number:02}-p{index:02}',lesson_id=lesson.id,
            question_number=index,difficulty=questions[index-1].difficulty,cognitive_level=questions[index-1].cognitive_level,
            marks=questions[index-1].marks,type='short_text',prompt=prompt,accepted_answers=[answer],
            answer_normalisation=AnswerNormalisation(),hints=['Write every original number in the model.',
                'Check the mathematical property or prime leaves before calculating.'],
            worked_solution=[WorkedSolutionStep(expression='Model the changed numbers',explanation='Use the actual givens.',why='The source example has different numbers.'),
                WorkedSolutionStep(expression=answer,explanation=memo,why=memo,verification=memo)],
            misconception_tags=[tag],verification={'original_question_check':memo},
            correct_feedback='Correct; your result matches the changed numbers.',source=source.name,
            answer_hidden_before_submission=True))
    def assessment(scene,i,prefix):
        scale=3 if prefix=='m' else 5
        if number==1:
            a,b,c=scene['values'];a+=scale
            answer=property_value(scene,scale)
            prompt=f'Calculate {expression(scene["kind"],a,b,c)}. Give its value (or undefined) and justify using the property.'
            memo=f'Use the {scene["property"]} on the changed numbers to obtain {answer}.'
            tag='whole-property-confusion'
        else:
            nums=[v*scale for v in scene['numbers']]
            answer=factor_value(scene,scale)
            prompt=(f'What is the largest prime factor of {nums[0]}?' if scene['kind']=='largest_prime' else
                f'Factor the numbers {", ".join(map(str,nums))} and find their {scene["kind"].upper()}.')
            memo=f'Prime-factor each new root, select the {scene["kind"]}, and verify {answer} against all numbers.'
            tag='hcf-lcm-prime-powers'
        return AssessmentQuestion(id=f'g8-whole-l{number:02}-{prefix}{i:02}',number=i,
            prompt=prompt,marks=4 if prefix=='m' else None,answer=answer,solution=[memo,answer],
            verification=memo,misconception_tags=[tag],accepted_answers=[answer])
    mastery=[assessment(s,i,'m') for i,s in enumerate(scenes[7:12],1)]
    parallel=[assessment(s,i,'r') for i,s in enumerate(scenes[12:15],1)]
    tag='whole-property-confusion' if number==1 else 'hcf-lcm-prime-powers'
    repairs={tag:{'diagnosis':'The original operation or factor choice was changed at an invalid step.',
        'repair':'Return to the first invalid transformation. Build the actual groups or prime tree, verify it, and try new values.'}}
    rules={tag:'Retry a changed-number question and explain why the earlier first step was invalid.'}
    return practice,mastery,parallel,repairs,rules


PRACTICE_1,MASTERY_1,REASSESSMENT_1,REPAIRS_1,RULES_1=banks(1)
PRACTICE_2,MASTERY_2,REASSESSMENT_2,REPAIRS_2,RULES_2=banks(2)
