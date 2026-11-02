"""Authored Grade 8 exponent lessons with deterministic question-level teaching states."""
import hashlib,json
from pathlib import Path
from app.curriculum.schemas import (AccessLevel,ContentStatus,Lesson,LessonBlock,MathematicalOperation,SemanticObject,StepExplanation,TeachingStep,TimelineEvent,VisualizationInstruction,VisualizationState,WhiteboardBlock,WhiteboardQuestion)
ROOT=Path(__file__).resolve().parents[4]
DIR=ROOT/'docs/curriculum/grade8/exponents'
SLUGS={1:'representing-and-comparing-powers',2:'laws-of-exponents',3:'square-and-cube-roots',4:'powers-and-roots-in-context',5:'diagnosing-exponent-errors',6:'integrated-exponents-readiness'}
TITLES={1:'Representing and comparing powers',2:'Laws of exponents',3:'Square and cube roots',4:'Powers and roots in context',5:'Diagnosing exponent errors',6:'Integrated powers and roots'}
OBJECTIVES={1:'Represent and compare whole and integer powers; write large whole numbers in scientific notation using positive exponents.',2:'Derive and apply the product, quotient, product-power and zero-exponent laws within Grade 8 scope.',3:'Find and verify exact square and cube roots, using square arrays and cube layers.',4:'Solve multi-step numerical and geometric problems involving powers and roots with correct units.',5:'Identify the first incorrect exponent or root operation and verify the correction.',6:'Solve connected powers, roots and measurements with correct order and units.'}

def build(number):
 if number not in SLUGS:raise ValueError('Unsupported exponent lesson')
 source=DIR/f'lesson-{number:02}-{SLUGS[number]}.md'
 scenes=json.loads((DIR/f'lesson-{number:02}-scenes.json').read_text(encoding='utf-8'))['scenes']
 if len(scenes)!=15:raise ValueError('Exponent lesson requires 15 authored worked examples')
 questions=[]
 for index,s in enumerate(scenes,1):
  qid=f'g8-exp-l{number:02}-w{index:02}'
  if s['id']!=qid or not 5<=len(s['rows'])<=8:raise ValueError(f'{qid}: incomplete authored steps')
  objs=[SemanticObject(id=k,type=kind,value=v,group=g) for k,kind,v,g in (
    ('problem','label',s['problem'][:160],'given'),('model','label','Question-specific powers and place shifts','visual'),
    ('operation','operation','Factor or exponent operation','working'),('result','result','Current result','working'),
    ('verification','verification','Original-value check','check'))]
  for j,value in enumerate(s['values'],1):objs.append(SemanticObject(id=f'exponent-{j}',type='term',value=value,group='given'))
  actions=[f'Read the complete question; identify the base, exponent or original whole number.',*s['rows'],f'Check the original power or whole number: {s["memo"]}']
  steps=[];prior=s['problem'];template={1:'grade8_exponent_representation',2:'grade8_exponent_laws',3:'grade8_exponent_roots',4:'grade8_exponent_applications',5:'grade8_exponent_error_trace',6:'grade8_exponent_integrated'}[number]
  for k,action in enumerate(actions,1):
   final=k==len(actions);after=f'Verified answer: {s["answer"]}. {s["memo"]}' if final else f'Stage {k}: {action}'
   duration=max(5400,len(action.split())*400)
   steps.append(TeachingStep(id=f'{qid}-step-{k:02}',step_number=k-1,title=action,before_expression=prior,working_expression=action,
    operation=MathematicalOperation(type={1:'exponent_representation_stage',2:'exponent_laws_stage',3:'exponent_roots_stage',4:'exponent_applications_stage',5:'exponent_error_stage',6:'exponent_integrated_stage'}[number],value=action,action='verify_solution' if final else 'transform_expression'),after_expression=after,
    explanation=StepExplanation(what=action,why=('A legal root, exponent or measurement step must match the original given values and units.' if number>=5 else 'A root reverses equal factors; the unit and operation order must agree with the original situation.' if number>=3 else 'An exponent counts equal factors; each stated transformation preserves the original value.'),purpose=action,remember=s['misconception']),
    common_mistake=s['misconception'],animation_template=template,screen_reader_description=f'{prior}. {action}. {after}.',
    visualization_state=VisualizationState(objects=[o.id for o in objs],highlights=['model'],annotations=[f'stage:{k}'],target='model',before_state=prior,working_state=action,after_state=after),
    instructional_goal=action,duration_ms=duration,events=[TimelineEvent(at_ms=0,type='caption',text=action),TimelineEvent(at_ms=0,type='narration',text=action),TimelineEvent(at_ms=250,type='focus',targets=['model']),TimelineEvent(at_ms=800,type='show_operation',targets=['operation'],label=action),TimelineEvent(at_ms=duration//2,type='reveal',targets=['result'],label=after[:240]),TimelineEvent(at_ms=duration-180,type='verify' if final else 'complete',targets=['verification' if final else 'result'])],
    narration=action,state_after={'stage':k,'question_id':qid,'verification_complete':final,'verification_link':s['memo']}))
   prior=after
  board=WhiteboardBlock(id=f'{qid}-board',representation='visual',problem=s['problem'],initial_expression=s['problem'],steps=steps,
   visualization=VisualizationInstruction(type='algebra',template=template,parameters={'scene_json':json.dumps(s,ensure_ascii=False),'question_id':qid,'prompt':s['problem'],'total_steps':len(actions)}),semantic_objects=objs)
  difficulty='foundation' if index==1 else 'easy' if index<=3 else 'standard' if index<=6 else 'intermediate' if index<=9 else 'exam' if index<=12 else 'advanced'
  questions.append(WhiteboardQuestion(id=qid,order=index,difficulty=difficulty,is_core_example=index==1,guidance_level='high' if index<=5 else 'moderate' if index<=10 else 'reduced',whiteboard=board,cognitive_level='knowledge' if index<=3 else 'routine' if index<=6 else 'complex' if index<=12 else 'problem_solving',marks=2 if index<=3 else 3 if index<=6 else 5 if index<=12 else 7,answer=s['answer'],full_memo=[*actions,f'Check: {s["memo"]}'],misconception_tags=[{1:'exponent-representation',2:'exponent-laws',3:'square-cube-roots',4:'exponent-applications',5:'exponent-error-diagnosis',6:'exponent-integrated-reasoning'}[number]],expected_evidence=s['memo']))
 lesson_id=f'g8-exponents-{number:02}'
 lesson=Lesson(id=lesson_id,order=number,title=TITLES[number],objective=OBJECTIVES[number],why_it_matters='Exponents compress repeated multiplication, help compare scale and support later algebra.',intuition={1:'Expand powers into factors and track each place shift in scientific notation.',2:'Group equal factors before applying each exponent law; cancellation explains subtraction.',3:'Build equal square rows and cube layers, then reverse them.',4:'Draw the shape or expression, solve each power and root, and check units.',5:'Trace the learner claim against a factor or root model and fix the first invalid operation.',6:'Convert areas and volumes into the lengths asked for, then combine like units.'}[number],prerequisites=['g8-decimal-fractions-06'] if number==1 else [f'g8-exponents-{number-1:02}'],estimated_minutes=90, difficulty='foundation' if number==1 else 'standard',access_level=AccessLevel.FREE if number==1 else AccessLevel.PREMIUM,status=ContentStatus.TEACHER_REVIEW_REQUIRED,
  blocks=[LessonBlock(type='concept',title=TITLES[number],content=OBJECTIVES[number]),questions[0].whiteboard,LessonBlock(type='mistake',title='Repair the first incorrect exponent step',content={1:'Repair the first wrong repeated factor, integer sign or scientific shift.',2:'Repair the first mistaken common base, cancellation or distributed exponent.',3:'Repair the first incorrectly counted square row or cube layer.',4:'Repair the first wrong root, operation order or measurement unit.',5:'Repair the first incorrect sign scope, principal root, division law or addition of roots.',6:'Repair the first wrong measure, operation order or unit conversion.'}[number]),LessonBlock(type='practice',title='Try unseen values independently',content='Submit before revealing the worked memo.',data={'practice_bank_id':lesson_id}),LessonBlock(type='summary',title='Verify the original power',content='Expand or reverse the exponent operation to verify the result.')],whiteboard_questions=questions,mastery_threshold=.8,paper=None,source_document=source.name,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),release_approved=False,assessment_contract={'worked_example_count':15,'practice_count':15,'mastery_question_count':5,'parallel_reassessment_count':3,'answer_hidden_before_submission':True,'progression_threshold':.8,'runtime_conversion':f'exponent_lesson_{number}_teacher_review'})
 return lesson,questions,scenes,source

LESSON_1,QUESTIONS_1,SCENES_1,SOURCE_1=build(1)
LESSON_2,QUESTIONS_2,SCENES_2,SOURCE_2=build(2)
LESSON_3,QUESTIONS_3,SCENES_3,SOURCE_3=build(3)
LESSON_4,QUESTIONS_4,SCENES_4,SOURCE_4=build(4)
LESSON_5,QUESTIONS_5,SCENES_5,SOURCE_5=build(5)
LESSON_6,QUESTIONS_6,SCENES_6,SOURCE_6=build(6)
