"""Stateful geometry stages for the three integrated straight-line lessons."""
from pathlib import Path
import hashlib
import json
from app.curriculum.grade8.straight_lines_chain_cases import LESSONS
from app.curriculum.schemas import (AccessLevel, ContentStatus, Lesson, LessonBlock, MathematicalOperation,
    SemanticObject, StepExplanation, TeachingStep, TimelineEvent, VisualizationInstruction,
    VisualizationState, WhiteboardBlock, WhiteboardQuestion)

SOURCE=Path(__file__).resolve().parents[4]/'docs/curriculum/grade8/geometry-of-straight-lines'
TITLES={3:'Mixed angle diagrams and justified relationships',4:'Unknowns in multi-step parallel-line diagrams',
        5:'First-error angle diagnosis and parallel reassessment'}
TEMPLATES={3:'grade8_angle_chain',4:'grade8_angle_equation',5:'grade8_angle_error'}


def build(number):
    questions=[];template=TEMPLATES[number]
    for i,case in enumerate(LESSONS[number],1):
        scene=case.scene
        objects=[SemanticObject(id=oid,type=kind,value=value,group=group) for oid,kind,value,group in (
            ('model','label',case.family,'visual'),('problem','label','two marked intersections','given'),
            ('angle-given','term',f'{case.given}°','given'),('angle-intermediate','term','pending','working'),
            ('angle-target','term',scene['target_label'],'unknown'),('angle-reason','label',scene['relation'],'working'),
            ('learner-claim','label',case.wrong_claim or 'none','working'),('operation','operation','theorem','working'),
            ('result','result','step result','working'),('verification','verification','check original angles','check'))]
        actions=(*case.working,f'Check the original diagram: {case.check}')
        steps=[];previous=case.problem
        for n,action in enumerate(actions,1):
            final=n==len(actions)
            after=(f'Verified: {case.check} Therefore x = {case.answer}{"°" if number!=4 else ""}.'
                   if final else f'Step {n}: {action}')
            duration=max(5200,len(action.split())*430)
            step=TeachingStep(id=f'{case.id}-step-{n:02}',step_number=n-1,title=action,
                before_expression=previous,working_expression=action,
                operation=MathematicalOperation(type=f'grade8_angle_{"chain" if number==3 else "equation" if number==4 else "error"}_stage',
                    value=action,action='verify_solution' if final else 'transform_expression'),
                after_expression=after,
                explanation=StepExplanation(what=action,why='Parallel marks, adjacent sectors and vertical sectors determine the reason; the picture is not measured.',
                    purpose=action,remember=case.misconception),common_mistake=case.misconception,
                animation_template=template,screen_reader_description=f'{previous}. {action}. {after}.',
                visualization_state=VisualizationState(objects=[o.id for o in objects],highlights=['angle-given','angle-intermediate','angle-target'],
                    annotations=[f'stage:{n}'],target='model',before_state=previous,working_state=action,after_state=after),
                instructional_goal=action,duration_ms=duration,
                events=[TimelineEvent(at_ms=0,type='caption',text=action),TimelineEvent(at_ms=0,type='narration',text=action),
                    TimelineEvent(at_ms=240,type='focus',targets=['angle-given','angle-intermediate']),
                    TimelineEvent(at_ms=850,type='show_operation',targets=['operation'],label=action),
                    TimelineEvent(at_ms=duration//2,type='reveal',targets=['result'],label=after[:240]),
                    TimelineEvent(at_ms=duration-180,type='verify' if final else 'complete',targets=['verification' if final else 'result'])],
                narration=action,state_after={'stage':n,'question_id':case.id,'verification_complete':final,'verification_link':case.check})
            steps.append(step);previous=after
        board=WhiteboardBlock(id=f'{case.id}-board',representation='visual',problem=case.problem,initial_expression=case.problem,steps=steps,
            visualization=VisualizationInstruction(type='geometry',template=template,parameters={
                'scene_json':json.dumps(scene,ensure_ascii=False),'question_id':case.id,'prompt':case.problem,'total_steps':len(actions)}),semantic_objects=objects)
        questions.append(WhiteboardQuestion(id=case.id,order=i,difficulty='foundation' if i==1 else 'easy' if i<=3 else 'standard' if i<=8 else 'intermediate' if i<=10 else 'exam',
            is_core_example=i==1,guidance_level='high' if i<=5 else 'moderate' if i<=10 else 'reduced',whiteboard=board,
            cognitive_level='knowledge' if i<=2 else 'routine' if i<=8 else 'complex',marks=2 if i<=3 else 4 if i<=10 else 6,
            answer=f'x = {case.answer}{"°" if number!=4 else ""}',full_memo=[*case.working,f'Check: {case.check}'],
            misconception_tags=['angle-reasoning',case.family],expected_evidence=case.check))
    source=SOURCE/f'lesson-{number:02}.md'
    return Lesson(id=f'g8-straight-lines-{number:02}',order=number,title=TITLES[number],
        objective=('Choose and justify both angle relationships in one diagram; carry each intermediate result into the next step.' if number==3 else
                   'Use two angle relationships to form and solve the correct linear equation, distinguishing x from the angle.' if number==4 else
                   'Identify the first unsupported angle claim, repair the theorem and reassess on changed values.'),
        why_it_matters='Multi-step angle problems reward justified reasoning; an attractive but unmarked diagram does not prove a theorem.',
        intuition='Keep the given, intermediate and target sectors in fixed positions. Select a relation from the line markings before calculation.',
        prerequisites=[f'g8-straight-lines-{number-1:02}'],estimated_minutes=90,difficulty='exam',
        access_level=AccessLevel.PREMIUM,status=ContentStatus.TEACHER_REVIEW_REQUIRED,release_approved=False,
        blocks=[LessonBlock(type='concept',title='Trace two justified relationships',content='Mark the given sector, transfer or supplement it, then evaluate the separate target sector.'),
                questions[0].whiteboard,
                LessonBlock(type='mistake',title='Locate the first unsupported claim',content='Check line markings and angle position before accepting equality or a 180-degree sum.'),
                LessonBlock(type='practice',title='Independent changed diagrams',content='Attempt all questions before revealing the memo.',data={'practice_bank_id':f'g8-straight-lines-{number:02}'}),
                LessonBlock(type='summary',title='Check in the original diagram',content='Substitute the result, verify the first angle pair and the second angle pair separately.')],
        whiteboard_questions=questions,mastery_threshold=.8,paper=None,source_document=source.name,
        source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        assessment_contract={'worked_example_count':15,'practice_count':15,'mastery_question_count':5,
            'parallel_reassessment_count':3,'answer_hidden_before_submission':True,'runtime_conversion':'teacher_review_browser_pending'})

LESSON_3=build(3)
LESSON_4=build(4)
LESSON_5=build(5)
