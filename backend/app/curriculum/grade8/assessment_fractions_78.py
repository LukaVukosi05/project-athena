"""Independent percentages practice and parallel checks, separate from the 15 worked scenes."""
from app.curriculum.grade8.percentage_math import answer
from app.curriculum.grade8.fractions_runtime import build
from app.curriculum.grade8.assessment_expressions import AssessmentQuestion
from app.practice.schemas import AnswerNormalisation,PracticeQuestion,WorkedSolutionStep

PRACTICE={7:[('convert','2/5'),('convert','3/8'),('convert','11/20'),('of','20','75'),('of','35','120'),('part','16','40'),('convert','7/16'),('of','12.5','96'),('part','33','60'),('of','42.5','200'),('part','56','80'),('convert','13/8'),('of','62.5','192'),('part','117','90'),('of','87.5','160')],8:[('increase','20','45'),('decrease','10','90'),('increase','25','144'),('decrease','15','240'),('change','132','120'),('increase','12.5','480'),('decrease','37.5','160'),('change','63','84'),('increase','8.5','400'),('decrease','17.5','320'),('change','96','80'),('decrease','12.5','640'),('increase','32.5','240'),('change','108','180'),('decrease','22.5','800')]}
MASTERY={7:[('convert','7/25'),('of','22.5','80'),('part','42','70'),('of','62.5','224'),('part','126','84')],8:[('increase','17.5','240'),('decrease','12.5','320'),('change','132','110'),('increase','37.5','160'),('change','90','120')]}
REASSESS={7:[('convert','13/40'),('of','37.5','144'),('part','84','60')],8:[('increase','22.5','160'),('decrease','25','360'),('change','112','140')]}

def prompt(v):
 kind,*values=v;a=values[0];b=values[1] if len(values)>1 else None
 return {'convert':f'Express {a} as a percentage.', 'of':f'Find {a}% of {b}.','part':f'What percentage of {b} is {a}?','increase':f'Increase {b} by {a}%.','decrease':f'Decrease {b} by {a}%.','change':f'The amount changes from {b} to {a}. Find the percentage change and direction.'}[kind]

def reasoning(v):
 kind,*values=v;a=values[0];b=values[1] if len(values)>1 else '1';result=answer(kind,values)
 return f'Identify original whole {b}. Measure the part or change against that original whole, then multiply by 100 when finding a rate. Check by reversing the calculation. Answer: {result}.'

def banks(n):
 lesson,questions,scenes,source=build(n);tag='percentage-original-whole'
 practice=[]
 for i,(v,q) in enumerate(zip(PRACTICE[n],questions,strict=True),1):
  kind,*values=v;final=answer(kind,values);explain=reasoning(v)
  practice.append(PracticeQuestion(id=f'g8-frac-l{n:02}-p{i:02}',lesson_id=lesson.id,question_number=i,difficulty=q.difficulty,cognitive_level=q.cognitive_level,marks=q.marks,type='short_text',prompt=prompt(v),accepted_answers=[final],answer_normalisation=AnswerNormalisation(),hints=['Underline the original whole. It represents 100%.','Find one percent, or divide change by the original amount.'],worked_solution=[WorkedSolutionStep(expression=f'Original whole: {values[-1] if len(values)>1 else "1"}',explanation='Anchor the 100% reference.',why='A percentage needs a named whole.'),WorkedSolutionStep(expression=explain,explanation='Calculate using the original whole.',why='Each percentage step refers to the same base.'),WorkedSolutionStep(expression=final,explanation='Check against the original question.',why='Reverse the change or compare part with whole.',verification=explain)],misconception_tags=[tag],verification={'original_question_check':explain},correct_feedback='Correct. The original whole and percentage agree.',source=source.name,answer_hidden_before_submission=True))
 def check(v,i,prefix):
  kind,*values=v;final=answer(kind,values);explain=reasoning(v)
  return AssessmentQuestion(id=f'g8-frac-l{n:02}-{prefix}{i:02}',number=i,prompt=prompt(v),marks=4 if prefix=='m' else None,answer=final,solution=[explain,final],verification=explain,misconception_tags=[tag],accepted_answers=[final])
 mastery=[check(v,i,'m') for i,v in enumerate(MASTERY[n],1)];parallel=[check(v,i,'r') for i,v in enumerate(REASSESS[n],1)]
 repairs={tag:{'diagnosis':'The original whole or direction of change was misidentified.','repair':'Mark the original whole as 100%, rebuild the hundred-part model and retry with new values.'}}
 return practice,mastery,parallel,repairs,{tag:'Use parallel values after reconstructing the original whole.'}
PRACTICE_7,MASTERY_7,REASSESS_7,REPAIRS_7,RULES_7=banks(7)
PRACTICE_8,MASTERY_8,REASSESS_8,REPAIRS_8,RULES_8=banks(8)
