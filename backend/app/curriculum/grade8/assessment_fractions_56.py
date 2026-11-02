"""Independent exact-rational practice, mastery and parallel reassessments for lessons 5-6."""
from app.curriculum.grade8.fractions_math import answer
from app.curriculum.grade8.fractions_runtime import build
from app.curriculum.grade8.assessment_expressions import AssessmentQuestion
from app.practice.schemas import AnswerNormalisation,PracticeQuestion,WorkedSolutionStep

POWERS_PRACTICE=[('square','4/7',2),('square','5/8',2),('root','16/25',2),('cube','3/5',3),('root','27/125',3),('square','7/4',2),('root','49/64',2),('cube','2/5',3),('root','125/216',3),('square','1 1/4',2),('cube','1 1/2',3),('root','36/49',2),('root','8/125',3),('square','9/8',2),('root','169/196',2)]
POWERS_MASTERY=[('square','3/7',2),('root','25/49',2),('cube','2/5',3),('root','64/343',3),('square','1 3/4',2)]
POWERS_REASSESS=[('square','4/9',2),('root','49/81',2),('cube','3/7',3)]
CONTEXT_PRACTICE=[
 ('4/5','25','multiply','learners'),('3/7','28','multiply','books'),('5/8','32','multiply','metres'),
 ('3 1/2','7','divide','litres'),('2/3','1 1/2','multiply','cups'),('7/8','1/3','subtract','litres'),
 ('4','2/5','divide','metres'),('3/4','20','multiply','kilograms'),('2 1/4','3/4','divide','litres'),
 ('9/10','1/5','subtract','metres'),('3/7','2/5','multiply','hectares'),('3 3/4','5/8','divide','litres'),
 ('2/5','7/12','add','kilograms'),('4/7','2 5/8','multiply','litres'),('4 1/6','1 3/4','subtract','metres')]
CONTEXT_MASTERY=[('5/6','30','multiply','learners'),('3 1/2','1/4','divide','cups'),('11/12','1/3','subtract','metres'),('2/5','1 1/2','multiply','litres'),('1/3','5/8','add','kilograms')]
CONTEXT_REASSESS=[('3/4','28','multiply','books'),('2 1/4','3/8','divide','litres'),('7/10','1/6','subtract','litres')]

def banks(n):
 if n not in (5,6):raise ValueError('Only fraction lessons 5 and 6 are supported')
 lesson,questions,scenes,source=build(n)
 tag='fraction-power-root' if n==5 else 'fraction-context-unit'
 variants=POWERS_PRACTICE if n==5 else CONTEXT_PRACTICE
 def prompt(data):
  if n==5:
   kind,a,index=data;return (f'Find the positive {"square" if index==2 else "cube"} root of {a}; check by raising your result to power {index}.' if kind=='root' else f'Calculate ({a})^{index}; show the numerator and denominator powers.')
  a,b,operation,unit=data
  if operation=='multiply':return f'A quantity is {b} {unit}. Find {a} of it. Give the numerical amount in {unit}.'
  if operation=='divide':return f'A quantity is {a} {unit}; each group uses {b} {unit}. How many groups, including partial groups?'
  if operation=='add':return f'Combine {a} {unit} and {b} {unit}. What is the total in {unit}?'
  return f'Start with {a} {unit} and use {b} {unit}. How much remains in {unit}?'
 def result(data):
  if n==5:kind,a,index=data;return answer(kind,[a],index)
  a,b,operation,_=data;return answer('context',[a,b],operation)
 def memo(data):
  final=result(data)
  if n==5:
   kind,a,index=data
   return f'Start from {a}; apply the {index}th power or its positive root to both numerator and denominator. Check with the inverse operation: {final}.'
  a,b,operation,unit=data
  return f'Label the original whole in {unit}; perform {operation} on {a} and {b} with equal-sized parts. Result {final} {"groups" if operation=="divide" else unit}; reverse the operation to verify.'
 practice=[]
 for i,(data,q) in enumerate(zip(variants,questions,strict=True),1):
  final=result(data);explain=memo(data)
  practice.append(PracticeQuestion(id=f'g8-frac-l{n:02}-p{i:02}',lesson_id=lesson.id,question_number=i,
   difficulty=q.difficulty,cognitive_level=q.cognitive_level,marks=q.marks,type='short_text',prompt=prompt(data),
   accepted_answers=[final],answer_normalisation=AnswerNormalisation(),
   hints=['Name the original fraction and its whole before calculating.',
    'For powers and roots change numerator and denominator; in a context, keep the unit and equal-sized parts.'],
   worked_solution=[WorkedSolutionStep(expression='Label the original quantity',explanation='Keep the original whole and its unit in view.',why='This avoids a change of unit.'),
    WorkedSolutionStep(expression='Build equal parts or equal dimensions',explanation=explain,why='Each visible partition has the same size.',verification=explain),
    WorkedSolutionStep(expression=final,explanation='State the simplified result and verify.',why='The inverse check returns the original quantity.',verification=explain)],
   misconception_tags=[tag],verification={'original_question_check':explain},correct_feedback='Correct; the original quantity checks.',
   source=source.name,answer_hidden_before_submission=True))
 def check(data,i,prefix):
  final=result(data);explain=memo(data)
  return AssessmentQuestion(id=f'g8-frac-l{n:02}-{prefix}{i:02}',number=i,prompt=prompt(data),
   marks=4 if prefix=='m' else None,answer=final,solution=[explain,final],verification=explain,
   misconception_tags=[tag],accepted_answers=[final])
 mastery=[check(data,i,'m') for i,data in enumerate(POWERS_MASTERY if n==5 else CONTEXT_MASTERY,1)]
 parallel=[check(data,i,'r') for i,data in enumerate(POWERS_REASSESS if n==5 else CONTEXT_REASSESS,1)]
 repairs={tag:{'diagnosis':'Locate the first numerator, denominator or context-unit mismatch.',
               'repair':'Rebuild the original whole; show equal dimensions or measured parts, then check with the inverse operation.'}}
 rules={tag:'Reassess with new values after the first mismatched step has been repaired.'}
 return practice,mastery,parallel,repairs,rules
PRACTICE_5,MASTERY_5,REASSESS_5,REPAIRS_5,RULES_5=banks(5)
PRACTICE_6,MASTERY_6,REASSESS_6,REPAIRS_6,RULES_6=banks(6)
