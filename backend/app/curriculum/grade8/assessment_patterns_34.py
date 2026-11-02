"""Private independent assessment for authored Patterns Lessons 3 and 4."""
from app.curriculum.grade8.patterns_runtime import build
from app.curriculum.grade8.assessment_expressions import AssessmentQuestion
from app.practice.schemas import AnswerNormalisation, PracticeQuestion, WorkedSolutionStep


def evaluate(scene,n):
    a,b=scene['a'],scene['b'];family=scene['family']
    return {'linear':lambda:a*n+b,'square_offset':lambda:a*n*n+b,
            'triangular':lambda:a*n*(n+1)//2+b,'rectangle':lambda:a*n*(n+1)+b,
            'geometric':lambda:a*b**(n-1)}[family]()


def banks(number):
    lesson,questions,scenes,source=build(number)
    practice=[]
    for index,scene in enumerate(scenes,1):
        if number==3:
            # Shift every output by one to create a genuinely new intercept.
            new_b=scene['b']+1
            given=[v+1 for v in scene['terms']]
            rule=(f'{scene["a"]}n' if scene['a']!=0 else '0n')+(f' + {new_b}' if new_b>0 else f' − {-new_b}' if new_b<0 else '')
            prompt=f'The values at positions 1–4 are {", ".join(map(str,given))}. Find one linear rule T(n) and check it at position 4.'
            answer=rule
            memo=f'The change is {scene["a"]}. At position one, {given[0]} = {scene["a"]} + {new_b}; hence T(n) = {rule}. Check n=4 gives {given[3]}.'
            accepted=list(dict.fromkeys([answer,answer.replace(' ',''),f'T(n)={answer.replace(" ","")}',
                str(new_b) if scene['a']==0 else answer.replace('n','×n')]))
        else:
            n=scene['target_position']+1
            answer=str(evaluate(scene,n))
            prompt=f'For T(n) = {scene["rule"]}, calculate the value at position {n}; check it against the given outputs {", ".join(map(str,scene["terms"]))}.'
            memo=f'Substitute n={n} into {scene["rule"]}; T({n}) = {answer}. Check positions 1 and 4 using the same rule.'
            accepted=[answer]
        practice.append(PracticeQuestion(id=f'g8-patterns-l{number:02}-p{index:02}',lesson_id=lesson.id,question_number=index,
            difficulty=questions[index-1].difficulty,cognitive_level=questions[index-1].cognitive_level,marks=questions[index-1].marks,
            type='short_text',prompt=prompt,accepted_answers=accepted,answer_normalisation=AnswerNormalisation(),
            hints=['Align each position with its value and test the rule at position one.',
                   'Show the operation at the target position before giving the answer.'],
            worked_solution=[WorkedSolutionStep(expression='Check the givens',explanation='Substitute positions one and four.',why='A rule must fit all given values.'),
                WorkedSolutionStep(expression=answer,explanation=memo,why=memo,verification=memo)],
            misconception_tags=['pattern-position-or-rule'],verification={'original_question_check':memo},
            correct_feedback='Correct; the position and rule agree with the given table.',source=source.name,
            answer_hidden_before_submission=True))
    # New coefficients or a new target position make every assessment independent.
    def assess(scene,index,prefix):
        if number==3:
            offset=2 if prefix=='m' else 4
            b=scene['b']+offset
            terms=[v+offset for v in scene['terms']]
            a=scene['a']
            answer=(f'{a}n' if a!=0 else '0n')+(f' + {b}' if b>0 else f' − {-b}' if b<0 else '')
            prompt=f'At positions 1–4 the outputs are {", ".join(map(str,terms))}. Give one linear rule T(n).'
            memo=f'The change is {a}. At n=1, {terms[0]}={a}+{b}; T(n)={answer}. Check n=4 gives {terms[3]}.'
            accepted=[answer,answer.replace(' ',''),f'T(n)={answer.replace(" ","")}']
            if a==0: accepted.append(str(b))
        else:
            n=scene['target_position']+(2 if prefix=='m' else 3)
            prompt=f'For T(n) = {scene["rule"]}, find the value at position {n}.'
            answer=str(evaluate(scene,n));memo=f'T({n}) = {answer}; check the same rule at positions 1 and 4.'
            accepted=[answer]
        return AssessmentQuestion(id=f'g8-patterns-l{number:02}-{prefix}{index:02}',number=index,prompt=prompt,
            marks=4 if prefix=='m' else None,answer=answer,solution=[memo,answer],verification=memo,
            misconception_tags=['pattern-position-or-rule'],accepted_answers=accepted)
    mastery=[assess(s,n,'m') for n,s in enumerate(scenes[8:13],1)]
    parallel=[assess(s,n,'r') for n,s in enumerate((scenes[13],scenes[14],scenes[12]),1)]
    repairs={'pattern-position-or-rule':{'diagnosis':'A position, change, or substitution was mismatched with its output.',
        'repair':'Label the positions, test the rule at two distant given values, then substitute the requested position.'}}
    rules={'pattern-position-or-rule':'Rebuild a different position table, verify two given outputs, then try a parallel value.'}
    return practice,mastery,parallel,repairs,rules

PRACTICE_3,MASTERY_3,REASSESSMENT_3,REPAIRS_3,RULES_3=banks(3)
PRACTICE_4,MASTERY_4,REASSESSMENT_4,REPAIRS_4,RULES_4=banks(4)
