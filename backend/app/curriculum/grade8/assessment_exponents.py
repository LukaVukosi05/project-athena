"""Unseen exact exponent practice and assessment, never included in initial lesson payload."""
from app.curriculum.grade8.exponent_math import solve as exponent_solve
from app.curriculum.grade8.exponent_roots_math import solve as roots_solve
from app.curriculum.grade8.exponent_reasoning_math import solve as reasoning_solve
from app.curriculum.grade8.exponents_inputs import PRACTICE as OLD_PRACTICE,MASTERY as OLD_MASTERY,REASSESS as OLD_REASSESS
from app.curriculum.grade8.exponents_roots_inputs import PRACTICE as ROOT_PRACTICE,MASTERY as ROOT_MASTERY,REASSESS as ROOT_REASSESS
from app.curriculum.grade8.exponent_reasoning_inputs import PRACTICE as REASON_PRACTICE,MASTERY as REASON_MASTERY,REASSESS as REASON_REASSESS
PRACTICE={**OLD_PRACTICE,**ROOT_PRACTICE,**REASON_PRACTICE};MASTERY={**OLD_MASTERY,**ROOT_MASTERY,**REASON_MASTERY};REASSESS={**OLD_REASSESS,**ROOT_REASSESS,**REASON_REASSESS}
def solve_for(n,kind,values):return (exponent_solve if n<3 else roots_solve if n<5 else reasoning_solve)(kind,values)
from app.curriculum.grade8.exponents_runtime import build
from app.curriculum.grade8.assessment_expressions import AssessmentQuestion
from app.practice.schemas import AnswerNormalisation,PracticeQuestion,WorkedSolutionStep

def banks(n):
 if n not in (1,2,3,4,5,6):raise ValueError('Only authored exponent lessons supported')
 lesson,questions,scenes,source=build(n);tag={1:'exponent-representation',2:'exponent-laws',3:'square-cube-roots',4:'exponent-applications',5:'exponent-error-diagnosis',6:'exponent-integrated-reasoning'}[n]
 practice=[]
 for i,((kind,values),worked) in enumerate(zip(PRACTICE[n],questions,strict=True),1):
  answer,rows,prompt,check=solve_for(n,kind,values)
  practice.append(PracticeQuestion(id=f'g8-exp-l{n:02}-p{i:02}',lesson_id=lesson.id,question_number=i,difficulty=worked.difficulty,cognitive_level=worked.cognitive_level,marks=worked.marks,type='short_text',prompt=prompt,accepted_answers=[answer],answer_normalisation=AnswerNormalisation(),hints=(["Identify the square array or the cube's three equal edges.","Reverse the operation: square or cube a candidate, then check units."] if n>=3 else (['Read the original claim or measurement; identify what is actually being asked.','Build the factor, root or dimension model before calculating, then verify units.'] if n>=5 else ['Identify the base and number of equal factors or the whole-number place shift.','Expand factors or cancel matching nonzero factors before using a law.'])),worked_solution=[WorkedSolutionStep(expression=row,explanation=('Work through this error trace or contextual measurement.' if n>=5 else 'Work through this root or measurement step.' if n>=3 else 'Work through this factor or place shift.'),why=('Match every derived value to the original shape or expression.' if n>=3 else 'Keep the mathematical value linked to the original problem.')) for row in rows]+[WorkedSolutionStep(expression=answer,explanation=check,why='Verify the original expression.',verification=check)],misconception_tags=[tag],verification={'original_question_check':check},correct_feedback='Correct; the original expression confirms the result.',source=source.name,answer_hidden_before_submission=True))
 def item(case,i,prefix):
  answer,rows,prompt,check=solve_for(n,*case)
  return AssessmentQuestion(id=f'g8-exp-l{n:02}-{prefix}{i:02}',number=i,prompt=prompt,marks=4 if prefix=='m' else None,answer=answer,solution=[*rows,check],verification=check,misconception_tags=[tag],accepted_answers=[answer])
 mastery=[item(case,i,'m') for i,case in enumerate(MASTERY[n],1)]
 parallel=[item(case,i,'r') for i,case in enumerate(REASSESS[n],1)]
 return practice,mastery,parallel,{tag:{'diagnosis':('Find the first wrong sign, exponent law, root, measure or unit.' if n>=5 else 'Find the first wrong root, shape dimension or operation order.' if n>=3 else 'Find the first wrong factor, sign, cancellation or place shift.'),'repair':'Replay that operation with distinct values, then attempt a parallel problem.'}},{tag:'Reassess after repairing the first incorrect mathematical action.'}
PRACTICE_1,MASTERY_1,REASSESS_1,REPAIRS_1,RULES_1=banks(1)
PRACTICE_2,MASTERY_2,REASSESS_2,REPAIRS_2,RULES_2=banks(2)
PRACTICE_3,MASTERY_3,REASSESS_3,REPAIRS_3,RULES_3=banks(3)
PRACTICE_4,MASTERY_4,REASSESS_4,REPAIRS_4,RULES_4=banks(4)
PRACTICE_5,MASTERY_5,REASSESS_5,REPAIRS_5,RULES_5=banks(5)
PRACTICE_6,MASTERY_6,REASSESS_6,REPAIRS_6,RULES_6=banks(6)
