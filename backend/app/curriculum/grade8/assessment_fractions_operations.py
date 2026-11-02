"""Independent, exact-arithmetic practice and parallel checks for fraction products and quotients."""
from app.curriculum.grade8.fractions_math import answer,common_denominator
from app.curriculum.grade8.fractions_runtime import build
from app.curriculum.grade8.assessment_expressions import AssessmentQuestion
from app.practice.schemas import AnswerNormalisation,PracticeQuestion,WorkedSolutionStep

PRACTICE={
 3:[('2/5','25'),('3/7','21'),('4/9','36'),('7/8','16'),('3/4','2/5'),('2/3','9/10'),('1 1/4','2/5'),('2 1/2','4/5'),('5/6','30'),('7/10','1 3/7'),('3/8','4/9'),('1 2/3','3/5'),('8/11','33'),('1 3/4','4/7'),('9/16','48')],
 4:[('4','1/2'),('3','1/3'),('5/6','1/6'),('7/8','1/8'),('2/3','1/3'),('3/5','1/10'),('1 3/4','1/4'),('2 2/3','2/3'),('5','5/6'),('7/10','1/5'),('3/8','1/4'),('1 1/2','3/4'),('5/6','2'),('3 3/4','3/8'),('4/5','2/3')]
}
MASTERY={3:[('3/8','24'),('2/3','9/14'),('1 3/4','4/7'),('5/12','36'),('2 1/5','5/11')],
         4:[('5','1/4'),('3/4','3/8'),('1 1/2','2/3'),('5/8','2'),('3 1/3','5/6')]}
REASSESS={3:[('5/6','18'),('3/5','10/21'),('1 2/3','6/7')],
          4:[('4','2/5'),('7/9','1/3'),('1 1/4','5/8')]}

def banks(n):
 if n not in (3,4):raise ValueError('Unknown operation lesson')
 lesson,questions,scenes,source=build(n)
 kind='multiply' if n==3 else 'divide'
 tag='fraction-product' if n==3 else 'fraction-grouping'
 op='×' if n==3 else '÷'
 def prompt(a,b):return f'Calculate {a} {op} {b}. Use a diagram and show the exact answer.'
 def memo(a,b):
  result=answer(kind,[a,b]);method=('shade the selected groups, then multiply exact parts' if n==3 else 'mark divisor-sized groups, including fractional groups')
  return f'Start from {a} and {b}; {method}. Verify {a} {op} {b} = {result} with the reverse operation.'
 practice=[]
 for i,((a,b),q) in enumerate(zip(PRACTICE[n],questions,strict=True),1):
  result=answer(kind,[a,b]);explain=memo(a,b)
  practice.append(PracticeQuestion(id=f'g8-frac-l{n:02}-p{i:02}',lesson_id=lesson.id,question_number=i,
   difficulty=q.difficulty,cognitive_level=q.cognitive_level,marks=q.marks,type='short_text',prompt=prompt(a,b),
   accepted_answers=[result],answer_normalisation=AnswerNormalisation(),
   hints=['Draw equal-sized wholes and label both original quantities.',
    'Convert a mixed number to an improper fraction, or change both amounts into the same-sized parts.'],
   worked_solution=[WorkedSolutionStep(expression=f'Original quantities: {a} and {b}',explanation='Keep the units the same.',why='A fraction is meaningful only relative to its whole.'),
    WorkedSolutionStep(expression=f'Common partition: {common_denominator([a,b])} parts',explanation=explain,why='Visual groups and exact arithmetic agree.',verification=explain),
    WorkedSolutionStep(expression=result,explanation='Give the simplified answer.',why='Check with the inverse operation.',verification=explain)],
   misconception_tags=[tag],verification={'original_question_check':explain},correct_feedback='Correct; the inverse check agrees.',
   source=source.name,answer_hidden_before_submission=True))
 def check(pair,i,prefix):
  a,b=pair;result=answer(kind,[a,b]);explain=memo(a,b)
  return AssessmentQuestion(id=f'g8-frac-l{n:02}-{prefix}{i:02}',number=i,prompt=prompt(a,b),
   marks=4 if prefix=='m' else None,answer=result,solution=[explain,result],verification=explain,
   misconception_tags=[tag],accepted_answers=[result])
 mastery=[check(pair,i,'m') for i,pair in enumerate(MASTERY[n],1)]
 reassess=[check(pair,i,'r') for i,pair in enumerate(REASSESS[n],1)]
 repairs={tag:{'diagnosis':'Find the first place where the learner changed the whole or group size.',
               'repair':'Rebuild the original quantities with equal-sized parts; mark the selected part or divisor group before calculating.'}}
 rules={tag:'After the repair, solve a different fraction question and check with the inverse operation.'}
 return practice,mastery,reassess,repairs,rules
PRACTICE_3,MASTERY_3,REASSESS_3,REPAIRS_3,RULES_3=banks(3)
PRACTICE_4,MASTERY_4,REASSESS_4,REPAIRS_4,RULES_4=banks(4)
