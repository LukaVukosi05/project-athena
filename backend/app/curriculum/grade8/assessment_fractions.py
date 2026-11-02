"""Private, independently authored fractions practice and parallel assessments."""
from app.curriculum.grade8.fractions_runtime import build
from app.curriculum.grade8.fractions_math import answer,common_denominator
from app.curriculum.grade8.assessment_expressions import AssessmentQuestion
from app.practice.schemas import AnswerNormalisation,PracticeQuestion,WorkedSolutionStep

PRACTICE_1_SOURCE=[
 ('equivalent',['3/5','9/15']),('equivalent',['2/7','6/21']),('equivalent',['4/9','12/26']),('equivalent',['5/8','15/25']),
 ('compare',['2/5','3/4']),('compare',['5/6','7/9']),('compare',['7/12','4/7']),('compare',['3/8','5/16']),
 ('compare',['13/10','1 1/4']),('compare',['7/8','11/12']),('order',['2/5','3/5','1/2']),
 ('order',['7/8','5/6','3/4']),('order',['1 2/5','7/6','5/4']),('convert',['2 2/5']),('convert',['19/8'])]
PRACTICE_2_SOURCE=[
 (['2/7','3/7'],['+']),(['7/10','1/10'],['-']),(['1/3','1/4'],['+']),(['5/6','1/12'],['-']),
 (['3/8','1/4'],['+']),(['5/9','1/6'],['+']),(['2 1/3','1/6'],['+']),(['3 1/2','5/6'],['-']),
 (['4 1/4','2 2/3'],['-']),(['11/12','2/3'],['-']),(['3/4','1/6','1/8'],['+','-']),
 (['2 1/6','5/12','1/4'],['+','-']),(['3 1/4','2/3'],['-']),(['2/5','1/3','1/10'],['+','+']),
 (['5 1/8','3 3/4','7/16'],['-','+'])]
MASTERY_1=[('equivalent',['5/12','10/24']),('compare',['7/8','6/7']),('order',['3/4','2/3','5/6']),('convert',['3 5/8']),('compare',['11/10','1 1/8'])]
REASSESS_1=[('equivalent',['7/9','21/27']),('order',['4/5','2/3','3/4']),('convert',['23/5'])]
MASTERY_2=[(['3/5','7/10'],['+']),(['2 1/3','5/6'],['-']),(['1/2','3/8','1/4'],['+','-']),(['4 1/6','2 3/4'],['-']),(['3 2/5','5/12','1/6'],['+','-'])]
REASSESS_2=[(['2/3','1/5'],['+']),(['3 1/4','1 5/6'],['-']),(['2 3/8','3/4','1/8'],['-','+'])]

def banks(number):
    lesson,questions,scenes,source=build(number)
    variants=PRACTICE_1_SOURCE if number==1 else PRACTICE_2_SOURCE
    tag='fraction-equivalence' if number==1 else 'fraction-common-unit'
    practice=[]
    for i,(variant,q) in enumerate(zip(variants,questions,strict=True),1):
        if number==1:
            kind,values=variant;solution=answer(kind,values);prompt=(f'Are {values[0]} and {values[1]} equivalent? Answer yes or no.' if kind=='equivalent' else f'Compare {values[0]} and {values[1]} using <, > or =.' if kind=='compare' else f'Order {", ".join(values)} from least to greatest.' if kind=='order' else f'Convert {values[0]} to the other fraction form.')
        else:
            values,operators=variant;kind='arithmetic';solution=answer(kind,values,operators)
            expression=values[0]+''.join(f' {op} {v}' for op,v in zip(operators,values[1:],strict=True))
            prompt=f'Calculate {expression}; show the equivalent fractions and simplify.'
        lcd=common_denominator(values)
        memo=f'Use equal unit strips divided into {lcd} pieces. Check the given fractions {", ".join(values)}. Answer: {solution}.'
        practice.append(PracticeQuestion(id=f'g8-frac-l{number:02}-p{i:02}',lesson_id=lesson.id,question_number=i,
            difficulty=q.difficulty,cognitive_level=q.cognitive_level,marks=q.marks,type='short_text',prompt=prompt,
            accepted_answers=[solution],answer_normalisation=AnswerNormalisation(),
            hints=['Draw same-sized wholes before comparing pieces.','Find a common denominator and change every numerator by the same factor.'],
            worked_solution=[WorkedSolutionStep(expression=f'Common denominator {lcd}',explanation='Repartition the original fractions.',why='Only like-sized pieces may be counted together.'),
                WorkedSolutionStep(expression=solution,explanation=memo,why='Verify with the given fractions.',verification=memo)],
            misconception_tags=[tag],verification={'original_question_check':memo},
            correct_feedback='Correct; the original fractions agree with your answer.',source=source.name,answer_hidden_before_submission=True))
    def assessment(variant,i,prefix):
        if number==1:kind,values=variant;operators=None;prompt=f'{kind.title()} {", ".join(values)}.'
        else:values,operators=variant;kind='arithmetic';prompt='Calculate '+values[0]+''.join(f' {op} {v}' for op,v in zip(operators,values[1:],strict=True))+'.'
        result=answer(kind,values,operators)
        memo=f'Use the common denominator {common_denominator(values)} to compare or combine equal-sized parts; answer {result}.'
        return AssessmentQuestion(id=f'g8-frac-l{number:02}-{prefix}{i:02}',number=i,prompt=prompt,
            marks=4 if prefix=='m' else None,answer=result,solution=[memo,result],verification=memo,
            misconception_tags=[tag],accepted_answers=[result])
    mastery=[assessment(v,i,'m') for i,v in enumerate(MASTERY_1 if number==1 else MASTERY_2,1)]
    parallel=[assessment(v,i,'r') for i,v in enumerate(REASSESS_1 if number==1 else REASSESS_2,1)]
    repairs={tag:{'diagnosis':'The first mismatch occurred when partitioning the unit or converting a numerator.',
        'repair':'Draw identical unit strips, mark the common denominator, correct the first partition and retry new values.'}}
    rules={tag:'Use a parallel fraction question with changed values after the first-error repair.'}
    return practice,mastery,parallel,repairs,rules

PRACTICE_1,MASTERY_BANK_1,REASSESSMENT_1,REPAIRS_1,RULES_1=banks(1)
PRACTICE_2,MASTERY_BANK_2,REASSESSMENT_2,REPAIRS_2,RULES_2=banks(2)
