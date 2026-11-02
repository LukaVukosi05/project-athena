"""Source-backed Grade 8 whole-number property and factor lessons."""
import hashlib
import json
from pathlib import Path
from app.curriculum.schemas import (AccessLevel,ContentStatus,Lesson,LessonBlock,MathematicalOperation,
    SemanticObject,StepExplanation,TeachingStep,TimelineEvent,VisualizationInstruction,
    VisualizationState,WhiteboardBlock,WhiteboardQuestion)

ROOT=Path(__file__).resolve().parents[4]
DIR=ROOT/'docs/curriculum/grade8/whole-numbers'

def build(number):
    name={1:'properties',2:'factors'}[number]
    source=DIR/f'lesson-{number:02}-{name}.md'
    scenes=json.loads((DIR/f'lesson-{number:02}-scenes.json').read_text(encoding='utf-8'))['scenes']
    if len(scenes)!=15:raise ValueError('Whole Numbers pack needs fifteen worked examples')
    questions=[]
    for index,scene in enumerate(scenes,1):
        qid=f'g8-whole-l{number:02}-w{index:02}'
        if scene['id']!=qid or len(scene['actions'])<4 or len(scene['actions'])>8:
            raise ValueError(f'{qid}: source question or mathematical split count mismatches runtime')
        objects=[SemanticObject(id=key,type=kind,value=text,group=group) for key,kind,text,group in (
            ('problem','label',scene['problem'][:160],'given'),('model','label','Question-specific whole-number model','visual'),
            ('operation','operation','Current calculation','working'),('result','result','Result of current operation','working'),
            ('verification','verification','Original-question check','check'))]
        for k,v in enumerate(scene.get('values',scene.get('numbers')),1):
            objects.append(SemanticObject(id=f'given-{k}',type='term',value=str(v),group='given'))
        before='Read the original whole-number question';steps=[]
        for step_index,action in enumerate(scene['actions'],1):
            last=step_index==len(scene['actions'])
            after=f'Verified: {scene["memo"]}' if last else f'{step_index}. {action}'
            duration=max(5500,len(action.split())*430)
            steps.append(TeachingStep(id=f'{qid}-step-{step_index:02}',step_number=step_index-1,
                title=action,before_expression=before,working_expression=action,
                operation=MathematicalOperation(type='whole_number_step',value=action,
                    action='verify_solution' if last else 'transform_expression'),after_expression=after,
                explanation=StepExplanation(what=action,why=('A property must preserve the original operation and its complete groups.' if number==1 else
                    'Prime factors multiply back to the original number; the HCF and LCM use different prime powers.'),
                    purpose=action,remember=('Test the property on the original numbers.' if number==1 else
                        'Check the selected factors against every original number.')),
                common_mistake=scene['misconception'],animation_template='grade8_whole_number_board',
                screen_reader_description=f'{before}. {action} {after}.',
                visualization_state=VisualizationState(objects=[o.id for o in objects],highlights=['model'],
                    annotations=[f'stage:{step_index}'],target='model',before_state=before,working_state=action,after_state=after),
                instructional_goal=action,duration_ms=duration,
                events=[TimelineEvent(at_ms=0,type='caption',text=action),TimelineEvent(at_ms=0,type='narration',text=action),
                    TimelineEvent(at_ms=250,type='focus',targets=['model']),
                    TimelineEvent(at_ms=850,type='show_operation',targets=['operation'],label=action),
                    TimelineEvent(at_ms=duration//2,type='reveal',targets=['result'],label=after[:240]),
                    TimelineEvent(at_ms=duration-180,type='verify' if last else 'complete',targets=['verification' if last else 'result'])],
                narration=action,state_after={'stage':step_index,'question_id':qid,
                    'verification_complete':last,'verification_link':scene['memo'],'completion_state':after}))
            before=after
        board=WhiteboardBlock(id=f'{qid}-board',representation='visual',problem=scene['problem'],
            initial_expression='Read the original whole-number question',steps=steps,
            visualization=VisualizationInstruction(type='algebra',template='grade8_whole_number_board',parameters={
                'scene_json':json.dumps(scene,ensure_ascii=False),'question_id':qid,'prompt':scene['problem'],
                'total_steps':len(scene['actions'])}),
            semantic_objects=objects)
        difficulty='foundation' if index==1 else 'easy' if index<=3 else 'standard' if index<=6 else 'intermediate' if index<=9 else 'exam' if index<=12 else 'advanced'
        questions.append(WhiteboardQuestion(id=qid,order=index,difficulty=difficulty,is_core_example=index==1,
            guidance_level='high' if index<=5 else 'moderate' if index<=10 else 'reduced',whiteboard=board,
            cognitive_level='knowledge' if index<=3 else 'routine' if index<=6 else 'complex' if index<=12 else 'problem_solving',
            marks=2 if index<=3 else 3 if index<=6 else 5 if index<=12 else 7,
            answer=scene['memo'],full_memo=[*scene['actions'],f'Check: {scene["memo"]}'],
            misconception_tags=['whole-property-confusion' if number==1 else 'hcf-lcm-prime-powers'],
            expected_evidence=scene['memo']))
    lesson_id=f'g8-whole-numbers-{number:02}'
    title='Whole-number properties and zero' if number==1 else 'Prime factors, HCF and LCM'
    lesson=Lesson(id=lesson_id,order=number,title=title,
        objective=('Use commutative, associative, distributive and identity properties and explain why division by zero is undefined.' if number==1 else
            'Decompose whole numbers into primes, choose correct powers for HCF or LCM and verify by division or multiplication.'),
        why_it_matters='Whole-number structure makes mental calculation and later algebra reliable.',
        intuition=('Changing order or grouping preserves a permitted sum or product; distribution changes a grouped product into equal parts.' if number==1 else
            'A factor tree breaks each number into prime building blocks; shared blocks make the HCF and all needed blocks make the LCM.'),
        prerequisites=[] if number==1 else ['g8-whole-numbers-01'],estimated_minutes=75 if number==1 else 90,
        difficulty='foundation' if number==1 else 'standard',access_level=AccessLevel.FREE if number==1 else AccessLevel.PREMIUM,
        status=ContentStatus.TEACHER_REVIEW_REQUIRED,
        blocks=[LessonBlock(type='concept',title=title,content=('Compare two complete expressions, build their groups and name only the property that actually applies.' if number==1 else
            'Split composite roots into prime leaves. Rebuild each original product before selecting the common or maximum powers.')),
            questions[0].whiteboard,LessonBlock(type='mistake',title='Diagnose the first mistake',
                content=('Division by zero is undefined. An identity does not change the original number.' if number==1 else
                    'HCF uses the lowest shared prime powers; LCM uses the highest powers needed by any number.')),
            LessonBlock(type='practice',title='Try independently',content='Solve changed values and submit before seeing the memo.',data={'practice_bank_id':lesson_id}),
            LessonBlock(type='summary',title='Check the original numbers',content=('Calculate both expressions and compare.' if number==1 else
                'Multiply prime leaves back to the roots and test the HCF or LCM against each given number.'))],
        whiteboard_questions=questions,mastery_threshold=.8,paper=None,source_document=source.name,
        source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),release_approved=False,
        assessment_contract={'worked_example_count':15,'practice_count':15,'mastery_question_count':5,
            'parallel_reassessment_count':3,'answer_hidden_before_submission':True,'progression_threshold':.8,
            'runtime_conversion':f'whole_numbers_lesson_{number}_teacher_review'})
    return lesson,questions,scenes,source

LESSON_1,QUESTIONS_1,SCENES_1,SOURCE_1=build(1)
LESSON_2,QUESTIONS_2,SCENES_2,SOURCE_2=build(2)
