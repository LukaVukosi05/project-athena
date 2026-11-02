"""Private exact-decimal practice, mastery and parallel reassessment for Lessons 3–4."""
from app.curriculum.grade8.decimal_math import operation
from app.curriculum.grade8.decimals_runtime import build
from app.curriculum.grade8.assessment_expressions import AssessmentQuestion
from app.practice.schemas import AnswerNormalisation,PracticeQuestion,WorkedSolutionStep
PRACTICE={3:[('0.6','0.2'),('1.4','0.5'),('0.35','0.6'),('2.45','1.3'),('0.08','0.9'),('1.75','0.32'),('4.06','0.45'),('0.225','0.04'),('5.24','1.06'),('0.065','2.4'),('11.05','0.38'),('3.65','1.15'),('0.006','3.5'),('14.75','0.036'),('8.125','2.06')],4:[('1.5','0.3'),('3.6','0.6'),('0.90','0.25'),('4.8','0.12'),('0.63','0.07'),('5.25','0.15'),('0.072','0.008'),('6.125','0.25'),('13.44','0.16'),('0.675','0.075'),('19.8','0.045'),('1.344','0.024'),('26.875','1.25'),('0.516','0.012'),('47.52','0.048')]}
MASTERY={3:[('0.36','0.4'),('2.75','0.18'),('0.125','0.064'),('7.06','3.25'),('18.75','0.024')],4:[('2.7','0.09'),('0.875','0.025'),('9.216','0.048'),('17.64','0.28'),('25.875','0.075')]}
REASSESS={3:[('0.45','0.8'),('3.25','0.16'),('6.375','2.04')],4:[('3.75','0.15'),('0.525','0.035'),('10.752','0.064')]}

def banks(n):
 if n not in (3,4):raise ValueError('Decimal operation lesson required')
 lesson,questions,scenes,source=build(n);kind='multiply' if n==3 else 'divide';tag='decimal-product-scale' if n==3 else 'decimal-quotient-scale'
 practice=[]
 for i,(v,q) in enumerate(zip(PRACTICE[n],questions,strict=True),1):
  ans,rows,prompt,check=operation(kind,list(v))
  practice.append(PracticeQuestion(id=f'g8-dec-l{n:02}-p{i:02}',lesson_id=lesson.id,question_number=i,difficulty=q.difficulty,cognitive_level=q.cognitive_level,marks=q.marks,type='short_text',prompt=prompt,accepted_answers=[ans],answer_normalisation=AnswerNormalisation(),hints=['Keep both original decimal points in view.','For multiplication align partial products; for division scale BOTH operands by the same power of ten.'],worked_solution=[WorkedSolutionStep(expression=row,explanation='Perform this exact place-value move.',why='Keep every digit and scale linked to the original values.') for row in rows]+[WorkedSolutionStep(expression=ans,explanation=check,why='Reverse the operation.',verification=check)],misconception_tags=[tag],verification={'original_question_check':check},correct_feedback='Correct; reverse calculation confirms the original numbers.',source=source.name,answer_hidden_before_submission=True))
 def check(v,i,prefix):
  ans,rows,prompt,verification=operation(kind,list(v))
  return AssessmentQuestion(id=f'g8-dec-l{n:02}-{prefix}{i:02}',number=i,prompt=prompt,marks=4 if prefix=='m' else None,answer=ans,solution=[*rows,verification],verification=verification,misconception_tags=[tag],accepted_answers=[ans])
 mastery=[check(v,i,'m') for i,v in enumerate(MASTERY[n],1)]
 parallel=[check(v,i,'r') for i,v in enumerate(REASSESS[n],1)]
 repairs={tag:{'diagnosis':'Find the first misplaced partial product, unequal scaling or incorrect quotient remainder.', 'repair':'Rebuild the decimal scale and replay that one digit operation before a fresh parallel problem.'}}
 return practice,mastery,parallel,repairs,{tag:'Reassess unseen decimal values after repairing the first incorrect step.'}
PRACTICE_3,MASTERY_3,REASSESS_3,REPAIRS_3,RULES_3=banks(3)
PRACTICE_4,MASTERY_4,REASSESS_4,REPAIRS_4,RULES_4=banks(4)
