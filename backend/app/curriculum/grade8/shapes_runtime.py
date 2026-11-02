"""Five bounded, question-specific Grade 8 2D shape teaching lessons."""
import hashlib,json
from pathlib import Path
from app.curriculum.grade8.shapes_cases import LESSONS
from app.curriculum.schemas import (AccessLevel,ContentStatus,Lesson,LessonBlock,MathematicalOperation,
    SemanticObject,StepExplanation,TeachingStep,TimelineEvent,VisualizationInstruction,
    VisualizationState,WhiteboardBlock,WhiteboardQuestion)

ROOT=Path(__file__).resolve().parents[4]
SOURCE=ROOT/'docs/curriculum/grade8/geometry-of-2d-shapes'
TITLES={1:'Classify triangles by their sides',2:'Interior angles of triangles',3:'Equilateral and isosceles triangles',4:'Classify quadrilaterals from evidence',5:'Quadrilateral and parallelogram angles'}


def build(number):
    cases=LESSONS[number];source=SOURCE/f'lesson-{number:02}.md'
    questions=[]
    for index,case in enumerate(cases,1):
        scene={**case.scene,'family':case.family}
        objects=[SemanticObject(id=id,type=kind,value=value[:160],group=group) for id,kind,value,group in (
            ('problem','label',case.problem,'given'),('model','label',case.scene['shape'],'visual'),
            ('shape-given','term',case.problem,'given'),('shape-reason','label',case.family,'working'),
            ('operation','operation','active geometric operation','working'),
            ('result','result','current calculation','working'),('verification','verification','original shape check','check'))]
        actions=(*case.working,f'Verify from the original markings: {case.check}')
        steps=[];previous=case.problem
        for j,action in enumerate(actions,1):
            last=j==len(actions)
            after=f'Verified: {case.check}; answer {case.answer}' if last else f'Step {j}: {action}'
            duration=max(5200,len(action.split())*420)
            steps.append(TeachingStep(id=f'{case.id}-step-{j:02}',step_number=j-1,title=action,
                before_expression=previous,working_expression=action,
                operation=MathematicalOperation(type=f'grade8_{case.family}_stage',value=action,action='verify_solution' if last else 'transform_expression'),
                after_expression=after,
                explanation=StepExplanation(what=action,why='Use the labelled geometric evidence and its property rather than estimating from the drawing.',purpose=action,remember=case.misconception),
                common_mistake=case.misconception,animation_template=f'grade8_{case.family}',
                screen_reader_description=f'{previous}. {action}. {after}.',
                visualization_state=VisualizationState(objects=[o.id for o in objects],highlights=['shape-given','model'],annotations=[f'stage:{j}'],target='model',before_state=previous,working_state=action,after_state=after),
                instructional_goal=action,duration_ms=duration,
                events=[TimelineEvent(at_ms=0,type='caption',text=action),TimelineEvent(at_ms=0,type='narration',text=action),
                        TimelineEvent(at_ms=250,type='focus',targets=['shape-given','model']),
                        TimelineEvent(at_ms=800,type='show_operation',targets=['operation'],label=action),
                        TimelineEvent(at_ms=duration//2,type='reveal',targets=['result'],label=after[:240]),
                        TimelineEvent(at_ms=duration-180,type='verify' if last else 'complete',targets=['verification' if last else 'result'])],
                narration=action,state_after={'stage':j,'question_id':case.id,'verification_complete':last,'verification_link':case.check}))
            previous=after
        board=WhiteboardBlock(id=f'{case.id}-board',representation='visual',problem=case.problem,initial_expression=case.problem,steps=steps,
            visualization=VisualizationInstruction(type='geometry',template=f'grade8_{case.family}',parameters={
                'scene_json':json.dumps(scene,ensure_ascii=False),'question_id':case.id,'prompt':case.problem,'total_steps':len(actions)}),semantic_objects=objects)
        questions.append(WhiteboardQuestion(id=case.id,order=index,difficulty='foundation' if index==1 else 'easy' if index<=5 else 'standard' if index<=10 else 'intermediate',
            is_core_example=index==1,guidance_level='high' if index<=5 else 'moderate' if index<=10 else 'reduced',whiteboard=board,
            cognitive_level='knowledge' if index<=3 else 'routine' if index<=10 else 'complex',marks=2 if index<=3 else 3 if index<=10 else 5,
            answer=case.answer,full_memo=[*case.working,f'Check: {case.check}'],misconception_tags=['shape-reasoning',case.family],expected_evidence=case.check))
    lesson_id=f'g8-shapes-{number:02}'
    return Lesson(id=lesson_id,order=number,title=TITLES[number],
        objective=f'{TITLES[number]} from labelled geometric evidence, and explain every step.',
        why_it_matters='Shapes are classified and calculated from stated properties, not from what a sketch seems to show.',
        intuition='Mark the given sides and angles, choose the property, work one calculation at a time and check the figure.',
        prerequisites=['g8-straight-lines-02'] if number==1 else [f'g8-shapes-{number-1:02}'],estimated_minutes=90,difficulty='standard',
        access_level=AccessLevel.FREE if number==1 else AccessLevel.PREMIUM,
        status=ContentStatus.TEACHER_REVIEW_REQUIRED,release_approved=False,
        blocks=[LessonBlock(type='concept',title=TITLES[number],content='Use this question’s labelled figure to select and justify the property.'),questions[0].whiteboard,
                LessonBlock(type='mistake',title='Find the first unsupported geometric claim',content=cases[0].misconception),
                LessonBlock(type='practice',title='Changed figure; independent attempt',content='Submit before revealing the memo.',data={'practice_bank_id':lesson_id}),
                LessonBlock(type='summary',title='Verify with original markings',content='Check the calculated or classified answer against the stated figure.')],
        whiteboard_questions=questions,mastery_threshold=.8,paper=None,source_document=source.name,
        source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        assessment_contract={'worked_example_count':15,'practice_count':15,'mastery_question_count':5,
            'parallel_reassessment_count':3,'answer_hidden_before_submission':True,'runtime_conversion':'teacher_review_browser_pending'})

LESSONS_RUNTIME={n:build(n) for n in LESSONS}
