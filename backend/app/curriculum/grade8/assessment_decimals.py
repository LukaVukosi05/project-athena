"""Private, unseen practice and assessment variants for Grade 8 decimal lessons."""
from app.curriculum.grade8.decimal_math import solution
from app.curriculum.grade8.decimals_runtime import build
from app.curriculum.grade8.assessment_expressions import AssessmentQuestion
from app.practice.schemas import AnswerNormalisation,PracticeQuestion,WorkedSolutionStep
PRACTICE={
 1:[('place','7.209','tenths'),('place','4.087','hundredths'),('place','0.071','thousandths'),('compare','6.3','6.30'),('compare','2.06','2.006'),('compare','0.105','0.15'),('place','29.403','hundredths'),('compare','8.08','8.008'),('order','0.7','0.707','0.07'),('order','3.04','3.4','3.004'),('compare','15.051','15.501'),('order','5.5','5.055','5.505'),('place','140.072','thousandths'),('order','0.808','0.88','0.088'),('order','9.009','9.09','9.9')],
 2:[('round','4.367','2'),('round','6.282','2'),('round','1.475','2'),('round','13.456','2'),('round','8.751','1'),('round','0.1985','3'),('round','29.995','2'),('round','3.455','2'),('round','89.999','2'),('round','0.055','2'),('estimate','3.58','4.63','1'),('estimate','10.235','9.564','2'),('estimate','0.985','0.475','2'),('estimate','39.995','3.875','2'),('estimate','8.995','0.059','2')]
}
MASTERY={1:[('place','23.079','hundredths'),('compare','0.490','0.409'),('order','2.009','2.09','2.9'),('compare','10.010','10.001'),('order','7.07','7.007','7.7')],2:[('round','7.995','2'),('round','0.475','2'),('round','19.999','2'),('estimate','8.995','0.176','2'),('estimate','2.45','0.55','1')]}
REASSESS={1:[('place','9.507','hundredths'),('compare','0.707','0.77'),('order','3.09','3.009','3.9')],2:[('round','1.265','2'),('round','0.0995','3'),('estimate','6.985','4.176','2')]}

def banks(n):
 lesson,questions,scenes,source=build(n);tag='decimal-place-value' if n==1 else 'decimal-rounding'
 practice=[]
 for i,(v,q) in enumerate(zip(PRACTICE[n],questions,strict=True),1):
  answer,rows,prompt,check=solution(v[0],list(v[1:]));verification=' '.join(rows)+' '+check
  practice.append(PracticeQuestion(id=f'g8-dec-l{n:02}-p{i:02}',lesson_id=lesson.id,question_number=i,difficulty=q.difficulty,cognitive_level=q.cognitive_level,marks=q.marks,type='short_text',prompt=prompt,accepted_answers=[answer],answer_normalisation=AnswerNormalisation(),hints=['Align decimal points or mark the original on a number line.','Compare equal place columns; for rounding, locate the midpoint before choosing.'],worked_solution=[WorkedSolutionStep(expression=rows[0],explanation='Establish the decimal positions.',why='Every digit has a fixed place value.'),WorkedSolutionStep(expression=rows[1],explanation='Find the deciding column or midpoint.',why='This determines the comparison or rounding choice.'),WorkedSolutionStep(expression=rows[2],explanation=check,why='Check the original question.',verification=verification)],misconception_tags=[tag],verification={'original_question_check':check},correct_feedback='Correct; the original decimal values confirm the result.',source=source.name,answer_hidden_before_submission=True))
 def check(v,i,prefix):
  ans,rows,prompt,verification=solution(v[0],list(v[1:]))
  return AssessmentQuestion(id=f'g8-dec-l{n:02}-{prefix}{i:02}',number=i,prompt=prompt,marks=4 if prefix=='m' else None,answer=ans,solution=[*rows,verification],verification=verification,misconception_tags=[tag],accepted_answers=[ans])
 mastery=[check(v,i,'m') for i,v in enumerate(MASTERY[n],1)]
 reassess=[check(v,i,'r') for i,v in enumerate(REASSESS[n],1)]
 repairs={tag:{'diagnosis':'Locate the first incorrect digit column or rounding midpoint.','repair':'Restore equal place columns or the two neighbouring marks, then retry unseen numbers.'}}
 return practice,mastery,reassess,repairs,{tag:'Reassess with fresh values after repairing the first incorrect decimal step.'}
PRACTICE_1,MASTERY_1,REASSESS_1,REPAIRS_1,RULES_1=banks(1)
PRACTICE_2,MASTERY_2,REASSESS_2,REPAIRS_2,RULES_2=banks(2)
