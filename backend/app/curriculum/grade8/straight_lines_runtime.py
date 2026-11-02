"""Grade 8 straight-line teaching timelines, held for teacher review."""
from dataclasses import asdict
import hashlib
import json
from pathlib import Path

from app.curriculum.grade8.straight_lines_cases import LESSON_1 as CASES_1, LESSON_2 as CASES_2
from app.curriculum.schemas import (AccessLevel, ContentStatus, Lesson, LessonBlock, MathematicalOperation,
    SemanticObject, StepExplanation, TeachingStep, TimelineEvent, VisualizationInstruction,
    VisualizationState, WhiteboardBlock, WhiteboardQuestion)

ROOT = Path(__file__).resolve().parents[4]
SOURCE = ROOT / 'docs/curriculum/grade8/geometry-of-straight-lines'


def _labels(case):
    if len(case.given) == 1:
        return f'{case.given[0]}°', 'x'
    a,b,c,d = case.given
    def fmt(k, offset):
        text = 'x' if k == 1 else f'{k}x' if k else ''
        return str(offset) if not k else text if not offset else f'{text} {"+" if offset>0 else "−"} {abs(offset)}'
    return f'({fmt(c,d)})°', f'({fmt(a,b)})°'


def build(number):
    cases = (CASES_1, CASES_2)[number-1]
    template = 'grade8_intersecting_angles' if number == 1 else 'grade8_parallel_angles'
    title = ('Angles at intersecting and perpendicular lines' if number == 1 else 'Parallel lines and a transversal')
    source = SOURCE / f'lesson-{number:02}.md'
    questions=[]
    for index,case in enumerate(cases,1):
        given,target = _labels(case)
        scene = {'diagram':case.diagram,'relationship':case.relationship,'given_label':given,
                 'target_label':target,'reason':case.relationship.replace('_',' ')}
        objects = [SemanticObject(id=id,type=typ,value=value,group=group) for id,typ,value,group in (
            ('problem','label',case.problem,'given'),('model','label',case.diagram,'visual'),
            ('angle-given','term',given,'given'),('angle-target','term',target,'unknown'),
            ('angle-reason','label',scene['reason'],'working'),('operation','operation','current theorem','working'),
            ('result','result','current angle calculation','working'),('verification','verification','check original diagram','check'))]
        actions = [*case.working, f'Check the labelled diagram: {case.check}']
        steps=[];previous=case.problem
        for j,action in enumerate(actions,1):
            final=j==len(actions)
            after=f'Verified: {case.check}; answer {case.answer}{"°" if len(case.given)==1 else ""}' if final else f'Geometry step {j}: {action}'
            duration=max(5200,len(action.split())*420)
            steps.append(TeachingStep(id=f'{case.id}-step-{j:02}',step_number=j-1,title=action,
                before_expression=previous,working_expression=action,
                operation=MathematicalOperation(type='grade8_angle_stage' if number==1 else 'grade8_parallel_angle_stage',value=action,action='verify_solution' if final else 'transform_expression'),
                after_expression=after,
                explanation=StepExplanation(what=action,why='The stated angle relationship comes from the actual marked lines, not the apparent size in the drawing.',purpose=action,remember=case.misconception),
                common_mistake=case.misconception,animation_template=template,
                screen_reader_description=f'{previous}. {action}. {after}.',
                visualization_state=VisualizationState(objects=[x.id for x in objects],highlights=['angle-given','angle-target'],annotations=[f'stage:{j}'],target='model',before_state=previous,working_state=action,after_state=after),
                instructional_goal=action,duration_ms=duration,
                events=[TimelineEvent(at_ms=0,type='caption',text=action),TimelineEvent(at_ms=0,type='narration',text=action),
                        TimelineEvent(at_ms=250,type='focus',targets=['angle-given','angle-target']),
                        TimelineEvent(at_ms=800,type='show_operation',targets=['operation'],label=action),
                        TimelineEvent(at_ms=duration//2,type='reveal',targets=['result'],label=after[:240]),
                        TimelineEvent(at_ms=duration-180,type='verify' if final else 'complete',targets=['verification' if final else 'result'])],
                narration=action,state_after={'stage':j,'question_id':case.id,'verification_complete':final,'verification_link':case.check}))
            previous=after
        board=WhiteboardBlock(id=f'{case.id}-board',representation='visual',problem=case.problem,initial_expression=case.problem,steps=steps,
            visualization=VisualizationInstruction(type='geometry',template=template,parameters={'scene_json':json.dumps(scene,ensure_ascii=False),'question_id':case.id,'prompt':case.problem,'total_steps':len(actions)}),semantic_objects=objects)
        difficulty='foundation' if index==1 else 'easy' if len(case.given)==1 else 'standard'
        questions.append(WhiteboardQuestion(id=case.id,order=index,difficulty=difficulty,is_core_example=index==1,
            guidance_level='high' if index<=5 else 'moderate' if index<=10 else 'reduced',whiteboard=board,
            cognitive_level='knowledge' if index<=3 else 'routine' if index<=9 else 'complex',marks=2 if index<=3 else 3 if index<=9 else 5,
            answer=f'{case.answer}{"°" if len(case.given)==1 else ""}',full_memo=[*case.working,f'Check: {case.check}'],
            misconception_tags=['angle-reasoning',case.relationship],expected_evidence=case.check))
    lesson_id=f'g8-straight-lines-{number:02}'
    lesson=Lesson(id=lesson_id,order=number,title=title,
        objective='Name the angle relationship, calculate the unknown and verify it using the labelled diagram.',
        why_it_matters='A measured-looking diagram does not establish an angle fact; the relationship must follow from the lines.',
        intuition='Highlight exactly the two angle sectors; write their relationship before solving for a value.',
        prerequisites=['g8-algebraic-equations-05'] if number==1 else ['g8-straight-lines-01'],estimated_minutes=90,
        difficulty='standard',access_level=AccessLevel.FREE if number==1 else AccessLevel.PREMIUM,
        status=ContentStatus.TEACHER_REVIEW_REQUIRED,release_approved=False,
        blocks=[LessonBlock(type='concept',title=title,content='Study the actual line markings, select the theorem, then solve and substitute.'),
                questions[0].whiteboard,LessonBlock(type='mistake',title='Repair an unsupported angle claim',content='Locate the first claim unsupported by the diagram and name the correct relationship.'),
                LessonBlock(type='practice',title='Try a changed diagram independently',content='Submit before revealing the worked memo.',data={'practice_bank_id':lesson_id}),
                LessonBlock(type='summary',title='Check against the diagram',content='Substitute the calculated angle into the original marked pair.')],
        whiteboard_questions=questions,mastery_threshold=.8,paper=None,source_document=source.name,
        source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        assessment_contract={'worked_example_count':15,'practice_count':15,'mastery_question_count':5,
            'parallel_reassessment_count':3,'answer_hidden_before_submission':True,'runtime_conversion':'teacher_review_browser_pending'})
    return lesson


LESSON_1=build(1)
LESSON_2=build(2)
