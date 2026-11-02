"""Original Grade 8 fraction scenes with exact rational answers and targetable states."""
import hashlib,json
from pathlib import Path
from app.curriculum.schemas import (AccessLevel,ContentStatus,Lesson,LessonBlock,MathematicalOperation,
 SemanticObject,StepExplanation,TeachingStep,TimelineEvent,VisualizationInstruction,VisualizationState,
 WhiteboardBlock,WhiteboardQuestion)
ROOT=Path(__file__).resolve().parents[4]
DIR=ROOT/'docs/curriculum/grade8/common-fractions'
NAMES={1:'equivalent-and-comparing',2:'adding-and-subtracting',3:'multiplying-fractions',4:'dividing-fractions',5:'powers-and-roots',6:'fraction-contexts',7:'percentage-of-a-whole',8:'percentage-change'}
TITLES={1:'Equivalent fractions and comparison',2:'Adding and subtracting common fractions',3:'Multiplying fractions and finding a fraction of a whole',4:'Dividing whole numbers and fractions by fractions',5:'Powers and roots of common fractions',6:'Fraction problems in context',7:'Percentage of a whole and part',8:'Percentage increase and decrease'}

def build(number):
 if number not in NAMES:raise ValueError('Unsupported fraction lesson')
 source=DIR/f'lesson-{number:02}-{NAMES[number]}.md'
 scenes=json.loads((DIR/f'lesson-{number:02}-scenes.json').read_text(encoding='utf-8'))['scenes']
 if len(scenes)!=15:raise ValueError('A fraction lesson requires 15 authored examples')
 questions=[]
 for index,scene in enumerate(scenes,1):
  qid=f'g8-frac-l{number:02}-w{index:02}'
  if scene['id']!=qid or len(scene['rows'])!=3:raise ValueError(f'{qid}: incomplete source scene')
  objs=[SemanticObject(id=key,type=kind,value=value,group=group) for key,kind,value,group in (
   ('problem','label',scene['problem'][:160],'given'),('model','label','Question-specific fraction strips','visual'),
   ('operation','operation','Current equivalence or arithmetic move','working'),('result','result','Result of this move','working'),
   ('verification','verification','Check against original fractions','check'))]
  for k,value in enumerate(scene['values'],1):objs.append(SemanticObject(id=f'fraction-{k}',type='term',value=value,group='given'))
  actions=[f'Read the complete question and label the original fraction units: {", ".join(scene["values"])}.',
           *scene['rows'],f'Verify the original fraction statement. {scene["memo"]}']
  prior=scene['problem'];steps=[]
  for k,action in enumerate(actions,1):
   final=k==len(actions);after=f'Verified answer: {scene["answer"]}. {scene["memo"]}' if final else f'Stage {k}: {action}'
   duration=max(5500,len(action.split())*410)
   steps.append(TeachingStep(id=f'{qid}-step-{k:02}',step_number=k-1,title=action,before_expression=prior,
    working_expression=action,operation=MathematicalOperation(type='percentage_stage' if number in (7,8) else 'fraction_model_stage' if number in (5,6) else 'fraction_operation_stage' if number in (3,4) else 'fraction_stage',value=action,
      action='verify_solution' if final else 'transform_expression'),after_expression=after,
    explanation=StepExplanation(what=action,why='Equal-sized wholes and a common unit preserve each fraction value.',purpose=action,remember=scene['misconception']),
    common_mistake=scene['misconception'],animation_template='grade8_percentage_grid' if number in (7,8) else 'grade8_fraction_powers_context' if number in (5,6) else 'grade8_fraction_operations' if number in (3,4) else 'grade8_fraction_strips',
    screen_reader_description=f'{prior}. {action}. {after}.',
    visualization_state=VisualizationState(objects=[o.id for o in objs],highlights=['model'],annotations=[f'stage:{k}'],target='model',
      before_state=prior,working_state=action,after_state=after),instructional_goal=action,duration_ms=duration,
    events=[TimelineEvent(at_ms=0,type='caption',text=action),TimelineEvent(at_ms=0,type='narration',text=action),
     TimelineEvent(at_ms=250,type='focus',targets=['model']),
     TimelineEvent(at_ms=850,type='show_operation',targets=['operation'],label=action),
     TimelineEvent(at_ms=duration//2,type='reveal',targets=['result'],label=after[:240]),
     TimelineEvent(at_ms=duration-180,type='verify' if final else 'complete',targets=['verification' if final else 'result'])],
    narration=action,state_after={'stage':k,'question_id':qid,'verification_complete':final,'verification_link':scene['memo']}))
   prior=after
  board=WhiteboardBlock(id=f'{qid}-board',representation='visual',problem=scene['problem'],initial_expression=scene['problem'],
   steps=steps,visualization=VisualizationInstruction(type='algebra',template='grade8_percentage_grid' if number in (7,8) else 'grade8_fraction_powers_context' if number in (5,6) else 'grade8_fraction_operations' if number in (3,4) else 'grade8_fraction_strips',parameters={
    'scene_json':json.dumps(scene,ensure_ascii=False),'question_id':qid,'prompt':scene['problem'],'total_steps':len(actions)}),
   semantic_objects=objs)
  difficulty='foundation' if index==1 else 'easy' if index<=3 else 'standard' if index<=6 else 'intermediate' if index<=9 else 'exam' if index<=12 else 'advanced'
  questions.append(WhiteboardQuestion(id=qid,order=index,difficulty=difficulty,is_core_example=index==1,
   guidance_level='high' if index<=5 else 'moderate' if index<=10 else 'reduced',whiteboard=board,
   cognitive_level='knowledge' if index<=3 else 'routine' if index<=6 else 'complex' if index<=12 else 'problem_solving',
   marks=2 if index<=3 else 3 if index<=6 else 5 if index<=12 else 7,answer=scene['answer'],
   full_memo=[*actions,f'Check: {scene["memo"]}'],misconception_tags=['percentage-whole' if number in (7,8) else 'fraction-equivalence' if number==1 else 'fraction-common-unit' if number==2 else 'fraction-product' if number==3 else 'fraction-grouping' if number==4 else 'fraction-power-root' if number==5 else 'fraction-context-unit'],
   expected_evidence=scene['memo']))
 lesson_id=f'g8-common-fractions-{number:02}'
 objective=('Convert fractions to percentages and calculate a percentage of a given whole or part.' if number==7 else 'Calculate percentage increase or decrease and measure change against the original amount.' if number==8 else 'Calculate exact squares, cubes, positive square roots and cube roots of fractions.' if number==5 else
  'Model fraction problems in measurement, sharing and daily contexts while retaining the whole and unit.' if number==6 else
  'Multiply common fractions and mixed numbers; find a fraction of a whole with area or group models.' if number==3 else
  'Divide whole numbers and fractions by common fractions using measured groups and verify by multiplication.' if number==4 else
  'Represent equivalent and mixed fractions, compare quantities with common units, and justify ordering.' if number==1 else
  'Add and subtract common fractions and mixed numbers using equivalent fractions, simplifying and checking each result.')
 lesson=Lesson(id=lesson_id,order=number,title=TITLES[number],objective=objective,
  why_it_matters='Fraction comparison and calculation support measurement, sharing, rates and later algebra.',
  intuition=('A percentage counts parts of one hundred; identify the whole before finding the part or the rate.' if number==7 else 'The original amount is always 100%; measure the change against it before adding or subtracting.' if number==8 else 'Powers repeat a fraction as every side; roots reverse that construction in both numerator and denominator.' if number==5 else
   'Label the unit and whole before selecting, combining or sharing equal parts.' if number==6 else
   'Multiplication finds a part of a quantity or a part of a part; preserve the same whole.' if number==3 else
   'Division counts how many divisor-sized groups fit in the given amount, including partial groups.' if number==4 else
   'The same-sized whole can be cut more finely without changing the amount.' if number==1 else
   'Common-sized pieces can be added or removed; denominators describe the pieces and are never added.'),
  prerequisites=[] if number==1 else [f'g8-common-fractions-{number-1:02}'],estimated_minutes=90 if number==1 else 100,
  difficulty='foundation' if number==1 else 'standard',access_level=AccessLevel.FREE if number==1 else AccessLevel.PREMIUM,
  status=ContentStatus.TEACHER_REVIEW_REQUIRED,
  blocks=[LessonBlock(type='concept',title=TITLES[number],content=objective),questions[0].whiteboard,
    LessonBlock(type='mistake',title='Repair the first incorrect fraction step',content=('Find the original whole first; check percent conversions and the direction of change against it.' if number in (7,8) else 'Apply powers and roots to both numerator and denominator; check by reversing the operation.' if number==5 else 'Name the whole and its unit, then use equal-sized parts for the context operation.' if number==6 else 'Compare equal-sized wholes; convert both quantities to the same denominator before counting parts.')),
    LessonBlock(type='practice',title='Try new fractions independently',content='Submit before revealing the memo.',data={'practice_bank_id':lesson_id}),
    LessonBlock(type='summary',title='Check the original question',content=('Check a part by multiplying the original whole by the percentage, or reverse the change.' if number in (7,8) else 'Raise the root to its index or count each repeated factor to verify the original fraction.' if number==5 else 'Recombine the measurement or reverse the operation with its original unit.' if number==6 else 'Rebuild the original quantities and verify the comparison or arithmetic result.'))],
  whiteboard_questions=questions,mastery_threshold=.8,paper=None,source_document=source.name,
  source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),release_approved=False,
  assessment_contract={'worked_example_count':15,'practice_count':15,'mastery_question_count':5,
   'parallel_reassessment_count':3,'answer_hidden_before_submission':True,'progression_threshold':.8,
   'runtime_conversion':f'fractions_lesson_{number}_teacher_review'})
 return lesson,questions,scenes,source
LESSON_1,QUESTIONS_1,SCENES_1,SOURCE_1=build(1)
LESSON_2,QUESTIONS_2,SCENES_2,SOURCE_2=build(2)
LESSON_3,QUESTIONS_3,SCENES_3,SOURCE_3=build(3)
LESSON_4,QUESTIONS_4,SCENES_4,SOURCE_4=build(4)
LESSON_5,QUESTIONS_5,SCENES_5,SOURCE_5=build(5)
LESSON_6,QUESTIONS_6,SCENES_6,SOURCE_6=build(6)

LESSON_7,QUESTIONS_7,SCENES_7,SOURCE_7=build(7)
LESSON_8,QUESTIONS_8,SCENES_8,SOURCE_8=build(8)
