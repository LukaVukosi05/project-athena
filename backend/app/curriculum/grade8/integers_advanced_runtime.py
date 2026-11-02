"""Authored integer operations lessons; original sources in docs/curriculum/grade8/integers."""
import hashlib
import json
from pathlib import Path
from app.curriculum.schemas import (AccessLevel,ContentStatus,Lesson,LessonBlock,MathematicalOperation,
    SemanticObject,StepExplanation,TeachingStep,TimelineEvent,VisualizationInstruction,
    VisualizationState,WhiteboardBlock,WhiteboardQuestion)

ROOT=Path(__file__).resolve().parents[4]
DIR=ROOT/'docs/curriculum/grade8/integers'
NAMES={3:'multiplication-division',4:'powers-roots',5:'integer-properties',6:'integer-contexts'}
TITLES={3:'Multiplying and dividing signed integers',4:'Powers, roots and mixed integer operations',5:'Properties of integer operations',6:'Solving contextual integer problems'}

def build(number):
    if number not in NAMES:raise ValueError('Unsupported integer lesson')
    source=DIR/f'lesson-{number:02}-{NAMES[number]}.md'
    scenes=json.loads((DIR/f'lesson-{number:02}-scenes.json').read_text(encoding='utf-8'))['scenes']
    if len(scenes)!=15:raise ValueError('Fifteen unique worked problems required')
    questions=[]
    for index,scene in enumerate(scenes,1):
        qid=f'g8-int-l{number:02}-w{index:02}'
        if scene['id']!=qid or not 5<=len(scene['actions'])<=7:raise ValueError(f'{qid}: source steps invalid')
        objects=[SemanticObject(id=k,type=t,value=v,group=g) for k,t,v,g in (
            ('problem','label',scene['problem'][:160],'given'),('model','label',scene['expression'],'visual'),
            ('operation','operation','Current mathematical action','working'),('result','result','Visible intermediate result','working'),
            ('verification','verification','Check the original expression','check'))]
        prior=scene['problem'];steps=[]
        for i,action in enumerate(scene['actions'],1):
            final=i==len(scene['actions'])
            after=(f'Verified claim: {scene["answer"]}. {scene["memo"]}' if final and number==5 else f'Verified: {scene["expression"]} = {scene["answer"]}' if final else f'Stage {i}: {action}')
            duration=max(5000,450*len(action.split()))
            steps.append(TeachingStep(id=f'{qid}-step-{i:02}',step_number=i-1,title=action,
                before_expression=prior,working_expression=action,
                operation=MathematicalOperation(type='integer_operation_stage' if number<=4 else 'integer_reasoning_stage',value=action,
                    action='verify_solution' if final else 'transform_expression'),after_expression=after,
                explanation=StepExplanation(what=action,why=('The sign follows equal groups or inverse multiplication.' if number==3 else
                    'The order of operations and scope of the exponent control each visible stage.' if number==4 else
                    'Both sides of the claim must be checked with legal integer properties.' if number==5 else
                    'Each real-world change must keep its direction, sequence and unit.'),
                    purpose=action,remember=scene['misconception']),
                common_mistake=scene['misconception'],animation_template='grade8_integer_operations' if number<=4 else 'grade8_integer_reasoning' if number<=4 else 'grade8_integer_reasoning',
                screen_reader_description=f'{prior}. {action}. {after}.',
                visualization_state=VisualizationState(objects=[o.id for o in objects],highlights=['model'],annotations=[f'stage:{i}'],
                    target='model',before_state=prior,working_state=action,after_state=after),
                instructional_goal=action,duration_ms=duration,
                events=[TimelineEvent(at_ms=0,type='caption',text=action),TimelineEvent(at_ms=0,type='narration',text=action),
                    TimelineEvent(at_ms=250,type='focus',targets=['model']),
                    TimelineEvent(at_ms=850,type='show_operation',targets=['operation'],label=action),
                    TimelineEvent(at_ms=duration//2,type='reveal',targets=['result'],label=after[:240]),
                    TimelineEvent(at_ms=duration-180,type='verify' if final else 'complete',targets=['verification' if final else 'result'])],
                narration=action,state_after={'stage':i,'question_id':qid,'verification_complete':final,'verification_link':scene['memo']}))
            prior=after
        board=WhiteboardBlock(id=f'{qid}-board',representation='visual',problem=scene['problem'],initial_expression=scene['problem'],steps=steps,
            visualization=VisualizationInstruction(type='algebra',template='grade8_integer_operations' if number<=4 else 'grade8_integer_reasoning',parameters={
                'scene_json':json.dumps(scene,ensure_ascii=False),'question_id':qid,'prompt':scene['problem'],'total_steps':len(steps)}),
            semantic_objects=objects)
        difficulty='foundation' if index==1 else 'easy' if index<=3 else 'standard' if index<=6 else 'intermediate' if index<=9 else 'exam' if index<=12 else 'advanced'
        tag=('integer-product-sign' if number==3 else 'integer-operation-order' if number==4 else 'integer-property-claim' if number==5 else 'integer-context-translation')
        questions.append(WhiteboardQuestion(id=qid,order=index,difficulty=difficulty,is_core_example=index==1,
            guidance_level='high' if index<=5 else 'moderate' if index<=10 else 'reduced',whiteboard=board,
            cognitive_level='knowledge' if index<=3 else 'routine' if index<=6 else 'complex' if index<=12 else 'problem_solving',
            marks=2 if index<=3 else 3 if index<=6 else 5 if index<=12 else 7,
            answer=str(scene['answer']),full_memo=[*scene['actions'],f'Check: {scene["memo"]}'],
            misconception_tags=[tag],expected_evidence=scene['memo']))
    lesson_id=f'g8-integers-{number:02}'
    objective=('Explain product and quotient signs using equal groups, patterns, inverse multiplication and left-to-right chains.' if number==3 else
        'Evaluate signed squares, cubes and exact roots before combining operations in the correct order.' if number==4 else
        'Test commutative, associative, distributive, identity and inverse claims with signed calculations.' if number==5 else
        'Translate multistep temperature, finance, elevation and scoring stories into signed expressions and verify units.')
    lesson=Lesson(id=lesson_id,order=number,title=TITLES[number],objective=objective,
        why_it_matters='Signed calculations support measurement, finance, coordinates and later algebra.',
        intuition=('The magnitude counts equal groups; the sign records direction and can be checked by undoing multiplication.' if number==3 else
            'An exponent acts on its base, which brackets define; roots undo powers and mixed calculations preserve operation order.' if number==4 else
        'Evaluate both sides before naming a property; a counterexample disproves a false rule.' if number==5 else
        'Each signed change modifies the current quantity; multiplication describes repeated equal changes.'),
        prerequisites=[f'g8-integers-{number-1:02}'],estimated_minutes={3:85,4:95,5:90,6:100}[number],
        difficulty='standard' if number in (3,5) else 'exam',access_level=AccessLevel.PREMIUM,status=ContentStatus.TEACHER_REVIEW_REQUIRED,
        blocks=[LessonBlock(type='concept',title=TITLES[number],content=objective),questions[0].whiteboard,
            LessonBlock(type='mistake',title='Find the first wrong mathematical action',content=('Check magnitude and sign separately, then use inverse multiplication.' if number==3 else
                'Circle the base of each exponent; calculate powers and roots before multiplication and addition.' if number==4 else
                'Evaluate both sides separately; a false claim needs a counterexample.' if number==5 else
                'Write a signed change for each event; preserve units and the intermediate balance.')),
            LessonBlock(type='practice',title='Try independently',content='Submit a different expression before seeing the answer.',data={'practice_bank_id':lesson_id}),
            LessonBlock(type='summary',title='Verify the original expression',content='Rebuild each step in order, keeping previous results visible.')],
        whiteboard_questions=questions,mastery_threshold=.8,paper=None,source_document=source.name,
        source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),release_approved=False,
        assessment_contract={'worked_example_count':15,'practice_count':15,'mastery_question_count':5,
            'parallel_reassessment_count':3,'answer_hidden_before_submission':True,'progression_threshold':.8,
            'runtime_conversion':f'integers_lesson_{number}_teacher_review'})
    return lesson,questions,scenes,source

LESSON_3,QUESTIONS_3,SCENES_3,SOURCE_3=build(3)
LESSON_4,QUESTIONS_4,SCENES_4,SOURCE_4=build(4)

LESSON_5,QUESTIONS_5,SCENES_5,SOURCE_5=build(5)
LESSON_6,QUESTIONS_6,SCENES_6,SOURCE_6=build(6)
