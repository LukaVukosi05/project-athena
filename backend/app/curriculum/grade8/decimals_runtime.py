"""Authored Grade 8 decimal lessons with deterministic question-level teaching states."""
import hashlib,json
from pathlib import Path
from app.curriculum.schemas import (AccessLevel,ContentStatus,Lesson,LessonBlock,MathematicalOperation,SemanticObject,StepExplanation,TeachingStep,TimelineEvent,VisualizationInstruction,VisualizationState,WhiteboardBlock,WhiteboardQuestion)
ROOT=Path(__file__).resolve().parents[4]
DIR=ROOT/'docs/curriculum/grade8/decimal-fractions'
SLUGS={1:'place-value-comparison',2:'rounding-estimating',3:'multiplying-decimals',4:'dividing-decimals',5:'powers-of-decimals',6:'roots-of-decimals'}
TITLES={1:'Decimal place value, comparison and order',2:'Rounding and estimating decimals',3:'Multiplying decimal fractions',4:'Dividing decimal fractions',5:'Squares and cubes of decimal fractions',6:'Square and cube roots of decimal fractions'}
OBJECTIVES={1:'Read decimal digits to thousandths, compare values with aligned place columns, and order decimals on a number line.',2:'Round decimal values using neighbouring marks and midpoints, then estimate sums by rounding each term first.',3:'Multiply decimals by aligning integer partial products then restoring their combined place values.',4:'Divide a decimal by a decimal through equal scaling and complete quotient-digit reasoning.',5:'Calculate squares and cubes using repeated equal decimal factors and exact place value.',6:'Find principal square and cube roots of decimal fractions and verify by powers.'}

def build(number):
 if number not in SLUGS:raise ValueError('Unsupported decimal lesson')
 source=DIR/f'lesson-{number:02}-{SLUGS[number]}.md'
 scenes=json.loads((DIR/f'lesson-{number:02}-scenes.json').read_text(encoding='utf-8'))['scenes']
 if len(scenes)!=15:raise ValueError('Decimal lesson requires 15 authored worked examples')
 questions=[]
 for index,s in enumerate(scenes,1):
  qid=f'g8-dec-l{number:02}-w{index:02}'
  if s['id']!=qid or (len(s['rows'])!=3 if number in (1,2) else not 5<=len(s['rows'])<=9):raise ValueError(f'{qid}: incomplete authored steps')
  objs=[SemanticObject(id=k,type=kind,value=v,group=g) for k,kind,v,g in (
    ('problem','label',s['problem'][:160],'given'),('model','label','Question-specific decimal positions','visual'),
    ('operation','operation','Place-value operation','working'),('result','result','Current result','working'),
    ('verification','verification','Original-value check','check'))]
  for j,value in enumerate(s['values'],1):objs.append(SemanticObject(id=f'decimal-{j}',type='term',value=value,group='given'))
  actions=[f'Read the complete question and identify the decimal point in {s["values"][0]}.',*s['rows'],f'Check against the original decimal values: {s["memo"]}']
  steps=[];prior=s['problem'];template={1:'grade8_decimal_columns',2:'grade8_decimal_rounding',3:'grade8_decimal_product',4:'grade8_decimal_quotient',5:'grade8_decimal_power',6:'grade8_decimal_root'}[number]
  for k,action in enumerate(actions,1):
   final=k==len(actions);after=f'Verified answer: {s["answer"]}. {s["memo"]}' if final else f'Stage {k}: {action}'
   duration=max(5400,len(action.split())*400)
   steps.append(TeachingStep(id=f'{qid}-step-{k:02}',step_number=k-1,title=action,before_expression=prior,working_expression=action,
    operation=MathematicalOperation(type={1:'decimal_column_stage',2:'decimal_round_stage',3:'decimal_product_stage',4:'decimal_quotient_stage',5:'decimal_power_stage',6:'decimal_root_stage'}[number],value=action,action='verify_solution' if final else 'transform_expression'),after_expression=after,
    explanation=StepExplanation(what=action,why='A decimal place is ten times the value of the place immediately to its right.',purpose=action,remember=s['misconception']),
    common_mistake=s['misconception'],animation_template=template,screen_reader_description=f'{prior}. {action}. {after}.',
    visualization_state=VisualizationState(objects=[o.id for o in objs],highlights=['model'],annotations=[f'stage:{k}'],target='model',before_state=prior,working_state=action,after_state=after),
    instructional_goal=action,duration_ms=duration,events=[TimelineEvent(at_ms=0,type='caption',text=action),TimelineEvent(at_ms=0,type='narration',text=action),TimelineEvent(at_ms=250,type='focus',targets=['model']),TimelineEvent(at_ms=800,type='show_operation',targets=['operation'],label=action),TimelineEvent(at_ms=duration//2,type='reveal',targets=['result'],label=after[:240]),TimelineEvent(at_ms=duration-180,type='verify' if final else 'complete',targets=['verification' if final else 'result'])],
    narration=action,state_after={'stage':k,'question_id':qid,'verification_complete':final,'verification_link':s['memo']}))
   prior=after
  board=WhiteboardBlock(id=f'{qid}-board',representation='visual',problem=s['problem'],initial_expression=s['problem'],steps=steps,
   visualization=VisualizationInstruction(type='algebra',template=template,parameters={'scene_json':json.dumps(s,ensure_ascii=False),'question_id':qid,'prompt':s['problem'],'total_steps':len(actions)}),semantic_objects=objs)
  difficulty='foundation' if index==1 else 'easy' if index<=3 else 'standard' if index<=6 else 'intermediate' if index<=9 else 'exam' if index<=12 else 'advanced'
  questions.append(WhiteboardQuestion(id=qid,order=index,difficulty=difficulty,is_core_example=index==1,guidance_level='high' if index<=5 else 'moderate' if index<=10 else 'reduced',whiteboard=board,cognitive_level='knowledge' if index<=3 else 'routine' if index<=6 else 'complex' if index<=12 else 'problem_solving',marks=2 if index<=3 else 3 if index<=6 else 5 if index<=12 else 7,answer=s['answer'],full_memo=[*actions,f'Check: {s["memo"]}'],misconception_tags=[{1:'decimal-place-value',2:'decimal-rounding',3:'decimal-product-scale',4:'decimal-quotient-scale',5:'decimal-power-scale',6:'decimal-root-check'}[number]],expected_evidence=s['memo']))
 lesson_id=f'g8-decimal-fractions-{number:02}'
 lesson=Lesson(id=lesson_id,order=number,title=TITLES[number],objective=OBJECTIVES[number],why_it_matters='Measurements, money and data require exact decimal place values and sensible calculations.',intuition={1:'Use columns of fixed place value and align decimal points before deciding which amount is larger.',2:'Rounding chooses the nearer neighbouring mark; calculate with the rounded terms only when estimating.',3:'Multiply integer factors through aligned partial products, then restore both decimal scales.',4:'Scale both operands equally until the divisor is whole; write each quotient digit and remainder.',5:'Expand the exponent into equal factors and track each decimal place.',6:'Test a non-negative candidate and reverse the root with the original power.'}[number],prerequisites=['g8-common-fractions-08'] if number==1 else [f'g8-decimal-fractions-{number-1:02}'],estimated_minutes=90, difficulty='foundation' if number==1 else 'standard',access_level=AccessLevel.FREE if number==1 else AccessLevel.PREMIUM,status=ContentStatus.TEACHER_REVIEW_REQUIRED,
  blocks=[LessonBlock(type='concept',title=TITLES[number],content=OBJECTIVES[number]),questions[0].whiteboard,LessonBlock(type='mistake',title='Repair the first incorrect decimal step',content={1:'Align decimal points and preserve zeros inside the number.',2:'Mark the two neighbours and midpoint before choosing; estimate each term separately.',3:'Repair the first misaligned partial product or decimal place count.',4:'Repair the first unequal scaling, missing quotient digit or incorrect remainder.',5:'Repair the first wrong repeated factor or decimal scale.',6:'Repair the first wrong root candidate, sign or inverse power check.'}[number]),LessonBlock(type='practice',title='Try unseen values independently',content='Submit before revealing the worked memo.',data={'practice_bank_id':lesson_id}),LessonBlock(type='summary',title='Check original decimal values',content='Reverse the operation with the original decimal values to verify the result.')],whiteboard_questions=questions,mastery_threshold=.8,paper=None,source_document=source.name,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),release_approved=False,assessment_contract={'worked_example_count':15,'practice_count':15,'mastery_question_count':5,'parallel_reassessment_count':3,'answer_hidden_before_submission':True,'progression_threshold':.8,'runtime_conversion':f'decimal_lesson_{number}_teacher_review'})
 return lesson,questions,scenes,source
LESSON_1,QUESTIONS_1,SCENES_1,SOURCE_1=build(1)
LESSON_2,QUESTIONS_2,SCENES_2,SOURCE_2=build(2)

LESSON_3,QUESTIONS_3,SCENES_3,SOURCE_3=build(3)
LESSON_4,QUESTIONS_4,SCENES_4,SOURCE_4=build(4)

LESSON_5,QUESTIONS_5,SCENES_5,SOURCE_5=build(5)
LESSON_6,QUESTIONS_6,SCENES_6,SOURCE_6=build(6)
