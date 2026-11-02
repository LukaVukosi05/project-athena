"""Private independent work and mastery for comparing and repairing patterns."""
from app.curriculum.grade8.patterns_runtime import build
from app.curriculum.grade8.assessment_expressions import AssessmentQuestion
from app.practice.schemas import AnswerNormalisation, PracticeQuestion, WorkedSolutionStep


def value(family, a, b, n):
    return {'linear': lambda: a*n+b, 'square_offset': lambda: a*n*n+b,
            'triangular': lambda: a*n*(n+1)//2+b,
            'rectangle': lambda: a*n*(n+1)+b,
            'geometric': lambda: a*b**(n-1)}[family]()


def banks(number):
    lesson, questions, scenes, source = build(number)
    practice=[]
    for i, scene in enumerate(scenes, 1):
        n=scene['target_position']+1
        if number==5:
            chosen=scene['candidates'][0 if scene['correct_label']=='A' else 1]
            answer=str(value(chosen['family'],chosen['a'],chosen['b'],n))
            prompt=(f"{scene['title']}: positions 1–4 have outputs {', '.join(map(str,scene['terms']))}. "
                    f"Compare Rule A ({scene['candidates'][0]['rule']}) and Rule B "
                    f"({scene['candidates'][1]['rule']}). Which value does the rule fitting all four predict at position {n}?")
            memo=(f"At position {scene['wrong_index']}, the false rule gives "
                  f"{value(next(c['family'] for j,c in enumerate(scene['candidates']) if j!=(0 if scene['correct_label']=='A' else 1)),next(c['a'] for j,c in enumerate(scene['candidates']) if j!=(0 if scene['correct_label']=='A' else 1)),next(c['b'] for j,c in enumerate(scene['candidates']) if j!=(0 if scene['correct_label']=='A' else 1)),scene['wrong_index'])}, "
                  f"not {scene['terms'][scene['wrong_index']-1]}. Rule {scene['correct_label']} fits; T({n})={answer}.")
            tag='candidate-rule-matches-one-term'
        else:
            answer=str(value(scene['family'],scene['a'],scene['b'],n))
            wrong=scene['claimed']
            prompt=(f"{scene['title']}: positions 1–4 give {', '.join(map(str,scene['terms']))}. "
                    f"The claim T({scene['target_position']})={wrong} may be wrong. Recheck the rule and predict T({n}).")
            memo=f"Reject the claim {wrong}; use T(n)={scene['rule']}. Check T(1)={scene['terms'][0]} and T(4)={scene['terms'][3]}. Then T({n})={answer}."
            tag='pattern-first-error'
        practice.append(PracticeQuestion(id=f'g8-patterns-l{number:02}-p{i:02}',lesson_id=lesson.id,question_number=i,
            difficulty=questions[i-1].difficulty,cognitive_level=questions[i-1].cognitive_level,marks=questions[i-1].marks,
            type='short_text',prompt=prompt,accepted_answers=[answer],answer_normalisation=AnswerNormalisation(),
            hints=['Align each position with its output.','Test both proposed calculations at the first and fourth positions.'],
            worked_solution=[WorkedSolutionStep(expression='Find the first mismatch',explanation='Check all given outputs.',why='One matching term is insufficient.'),
                WorkedSolutionStep(expression=answer,explanation=memo,why=memo,verification=memo)],
            misconception_tags=[tag],verification={'original_question_check':memo},
            correct_feedback='The repaired rule matches the given positions and the requested value.',
            source=source.name,answer_hidden_before_submission=True))
    def assessment(scene, i, prefix):
        n=scene['target_position']+(2 if prefix=='m' else 3)
        if number==5:
            good=scene['candidates'][0 if scene['correct_label']=='A' else 1]
            answer=str(value(good['family'],good['a'],good['b'],n))
            prompt=(f"{scene['title']}: the outputs are {', '.join(map(str,scene['terms']))}. "
                    f"Which of Rule A ({scene['candidates'][0]['rule']}) and Rule B "
                    f"({scene['candidates'][1]['rule']}) fits every output? Give its value at position {n}.")
            memo=f"Rule {scene['correct_label']} fits all four positions; substitute n={n} to get {answer}."
            tag='candidate-rule-matches-one-term'
        else:
            answer=str(value(scene['family'],scene['a'],scene['b'],n))
            prompt=(f"{scene['title']}: outputs at positions 1–4 are {', '.join(map(str,scene['terms']))}. "
                    f"A learner claims {scene['claimed']} at position {scene['target_position']}. "
                    f"Repair the rule and calculate the output at position {n}.")
            memo=f"The learner's claim is wrong. T(n)={scene['rule']}; T({n})={answer}."
            tag='pattern-first-error'
        return AssessmentQuestion(id=f'g8-patterns-l{number:02}-{prefix}{i:02}',number=i,
            prompt=prompt,marks=4 if prefix=='m' else None,answer=answer,solution=[memo,answer],
            verification=memo,misconception_tags=[tag],accepted_answers=[answer])
    mastery=[assessment(s,i,'m') for i,s in enumerate(scenes[7:12],1)]
    parallel=[assessment(s,i,'r') for i,s in enumerate(scenes[12:15],1)]
    key='candidate-rule-matches-one-term' if number==5 else 'pattern-first-error'
    repairs={key:{'diagnosis':'A proposed rule or continuation was trusted without checking every given position.',
        'repair':'Align the rows, identify the earliest mismatch, test the corrected rule at positions one and four, then retry on a different target.'}}
    rules={key:'Use a parallel question with new coefficients and explain the first counterexample before calculating the target.'}
    return practice,mastery,parallel,repairs,rules


PRACTICE_5,MASTERY_5,REASSESSMENT_5,REPAIRS_5,RULES_5=banks(5)
PRACTICE_6,MASTERY_6,REASSESSMENT_6,REPAIRS_6,RULES_6=banks(6)
