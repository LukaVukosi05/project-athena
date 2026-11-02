"""Private exact decimal powers and roots banks for lessons 5–6."""
from app.curriculum.grade8.decimal_math import power_root
from app.curriculum.grade8.decimals_runtime import build
from app.curriculum.grade8.assessment_expressions import AssessmentQuestion
from app.practice.schemas import AnswerNormalisation,PracticeQuestion,WorkedSolutionStep
BANKS={5: {'practice': [('0.3', 2), ('0.7', 2), ('1.6', 2), ('0.4', 3), ('2.3', 2), ('0.9', 3), ('1.35', 2), ('3.6', 2), ('0.25', 2), ('1.7', 3), ('2.15', 2), ('0.7', 3), ('4.25', 2), ('2.6', 3), ('1.85', 2)], 'mastery': [('0.45', 2), ('1.8', 3), ('3.15', 2), ('0.9', 3), ('5.25', 2)], 'reassess': [('0.55', 2), ('1.9', 3), ('3.35', 2)]}, 6: {'practice': [('0.4', 2), ('0.7', 2), ('1.6', 2), ('0.3', 3), ('1.7', 2), ('0.9', 3), ('2.35', 2), ('0.7', 3), ('3.6', 2), ('1.4', 3), ('0.25', 2), ('2.6', 3), ('4.25', 2), ('1.4', 3), ('6.5', 2)], 'mastery': [('0.45', 2), ('1.8', 3), ('3.15', 2), ('0.9', 3), ('5.25', 2)], 'reassess': [('0.55', 2), ('1.9', 3), ('3.35', 2)]}}

def banks(n):
 if n not in (5,6):raise ValueError('Decimal power/root lesson required')
 lesson,questions,scenes,source=build(n);kind='power' if n==5 else 'root';tag='decimal-power-scale' if n==5 else 'decimal-root-check'
 def values(pair):
  a,d=pair
  if n==6:
   from decimal import Decimal
   from app.curriculum.grade8.decimal_math import render
   return [render(Decimal(a)**d),str(d)]
  return [a,str(d)]
 practice=[]
 for i,(pair,q) in enumerate(zip(BANKS[n]['practice'],questions,strict=True),1):
  ans,rows,prompt,check=power_root(kind,values(pair))
  practice.append(PracticeQuestion(id=f'g8-dec-l{n:02}-p{i:02}',lesson_id=lesson.id,question_number=i,difficulty=q.difficulty,cognitive_level=q.cognitive_level,marks=q.marks,type='short_text',prompt=prompt,accepted_answers=[ans],answer_normalisation=AnswerNormalisation(),hints=['Identify the base/exponent or the radicand/root index.','Track the decimal scale; test a candidate before revealing the answer.'],worked_solution=[WorkedSolutionStep(expression=row,explanation='Show this decimal place-value step.',why='Keep the mathematical operation visible.') for row in rows]+[WorkedSolutionStep(expression=ans,explanation=check,why='Verify with the original number.',verification=check)],misconception_tags=[tag],verification={'original_question_check':check},correct_feedback='Correct; the inverse check returns the original number.',source=source.name,answer_hidden_before_submission=True))
 def item(pair,i,prefix):
  ans,rows,prompt,check=power_root(kind,values(pair))
  return AssessmentQuestion(id=f'g8-dec-l{n:02}-{prefix}{i:02}',number=i,prompt=prompt,marks=4 if prefix=='m' else None,answer=ans,solution=[*rows,check],verification=check,misconception_tags=[tag],accepted_answers=[ans])
 mastery=[item(v,i,'m') for i,v in enumerate(BANKS[n]['mastery'],1)]
 reassess=[item(v,i,'r') for i,v in enumerate(BANKS[n]['reassess'],1)]
 repairs={tag:{'diagnosis':'Find the first wrong factor, scale, root candidate or inverse check.','repair':'Rebuild that one operation and attempt new values independently.'}}
 return practice,mastery,reassess,repairs,{tag:'Use parallel decimal values only after repairing the first mistaken step.'}
PRACTICE_5,MASTERY_5,REASSESS_5,REPAIRS_5,RULES_5=banks(5)
PRACTICE_6,MASTERY_6,REASSESS_6,REPAIRS_6,RULES_6=banks(6)
