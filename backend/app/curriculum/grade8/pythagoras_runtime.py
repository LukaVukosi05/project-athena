"""Five complete, question-specific Grade 8 Pythagoras teaching lessons."""
import hashlib,json
from pathlib import Path
from app.curriculum.grade8.pythagoras_cases import LESSONS
from app.curriculum.schemas import (AccessLevel,ContentStatus,Lesson,LessonBlock,MathematicalOperation,
    SemanticObject,StepExplanation,TeachingStep,TimelineEvent,VisualizationInstruction,
    VisualizationState,WhiteboardBlock,WhiteboardQuestion)

ROOT=Path(__file__).resolve().parents[4]
SOURCE=ROOT/'docs/curriculum/grade8/pythagoras'
TITLES={1:'Squares on the sides of a right triangle',2:'Find the hypotenuse',3:'Find a missing perpendicular side',4:'Test whether a triangle is right-angled',5:'Pythagoras in practical contexts'}


def build(number):
    cases=LESSONS[number];source=SOURCE/f'lesson-{number:02}.md'
    questions=[]
    for index,case in enumerate(cases,1):
        scene={'family':case.family,'a':case.a,'b':case.b,'c':case.c,'context':case.context,'problem':case.problem}
        objects=[SemanticObject(id=id,type=kind,value=value[:160],group=group) for id,kind,value,group in (
            ('problem','label',case.problem,'given'),('model','label',case.family,'visual'),
            ('shape-given','term',case.problem,'given'),('shape-reason','label',case.family,'working'),
            ('operation','operation','active geometric operation','working'),
            ('result','result','current calculation','working'),('verification','verification','original triangle check','check'))]
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
                explanation=StepExplanation(what=action,why='Identify the perpendicular legs and hypotenuse, then calculate square areas in the correct order.',purpose=action,remember=case.misconception),
                common_mistake=case.misconception,animation_template=f'grade8_pythagoras_{case.family}',
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
            visualization=VisualizationInstruction(type='geometry',template=f'grade8_pythagoras_{case.family}',parameters={
                'scene_json':json.dumps(scene,ensure_ascii=False),'question_id':case.id,'prompt':case.problem,'total_steps':len(actions)}),semantic_objects=objects)
        questions.append(WhiteboardQuestion(id=case.id,order=index,difficulty='foundation' if index==1 else 'easy' if index<=5 else 'standard' if index<=10 else 'intermediate',
            is_core_example=index==1,guidance_level='high' if index<=5 else 'moderate' if index<=10 else 'reduced',whiteboard=board,
            cognitive_level='knowledge' if index<=3 else 'routine' if index<=10 else 'complex',marks=2 if index<=3 else 3 if index<=10 else 5,
            answer=case.answer,full_memo=[*case.working,f'Check: {case.check}'],misconception_tags=['pythagoras-reasoning',case.family],expected_evidence=case.check))
    lesson_id=f'g8-pythagoras-{number:02}'
    return Lesson(id=lesson_id,order=number,title=TITLES[number],
        objective={1:'Develop the theorem by comparing the three square areas.',2:'Find a hypotenuse exactly, including irrational lengths.',3:'Find a missing leg exactly by subtraction.',4:'Classify triangles using the converse without assuming a right angle.',5:'Model and solve practical right-triangle distances.'}[number],
        why_it_matters='A right-angle model turns an unfamiliar distance into two known square areas.',
        intuition=('Identify the longest given side and test both shorter squares before deciding whether an angle is right.' if number==4 else 'Find the right angle, name the longest side, calculate each square and check the original triangle.'),
        prerequisites=['g8-shapes-05'] if number==1 else [f'g8-pythagoras-{number-1:02}'],estimated_minutes=90,difficulty='standard',
        access_level=AccessLevel.FREE if number==1 else AccessLevel.PREMIUM,
        status=ContentStatus.TEACHER_REVIEW_REQUIRED,release_approved=False,
        blocks=[LessonBlock(type='concept',title=TITLES[number],content=('The triangle is drawn from its three given lengths. Do not assume a right angle; test the longest side with the converse.' if number==4 else 'The marked diagram follows this question’s given sides. Identify the right angle and compare square areas before revealing a length.')),questions[0].whiteboard,
                LessonBlock(type='mistake',title='Find the first incorrect square or side choice',content=cases[0].misconception),
                LessonBlock(type='practice',title='Changed figure; independent attempt',content='Submit before revealing the memo.',data={'practice_bank_id':lesson_id}),
                LessonBlock(type='summary',title='Verify with original markings',content='Substitute the exact side squares back into the original relation.')],
        whiteboard_questions=questions,mastery_threshold=.8,paper=None,source_document=source.name,
        source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        assessment_contract={'worked_example_count':15,'practice_count':15,'mastery_question_count':5,
            'parallel_reassessment_count':3,'answer_hidden_before_submission':True,'progression_threshold':.8,'runtime_conversion':'teacher_review_browser_pending'})

LESSONS_RUNTIME={n:build(n) for n in LESSONS}
