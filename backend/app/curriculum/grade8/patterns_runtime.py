"""Original, question-bound Grade 8 numeric and geometric pattern lessons."""
import hashlib
import json
from pathlib import Path
from app.curriculum.schemas import (AccessLevel, ContentStatus, Lesson, LessonBlock,
    MathematicalOperation, SemanticObject, StepExplanation, TeachingStep,
    TimelineEvent, VisualizationInstruction, VisualizationState, WhiteboardBlock, WhiteboardQuestion)

ROOT=Path(__file__).resolve().parents[4]
DIR=ROOT/'docs/curriculum/grade8/numeric-geometric-patterns'

def _question(scene, lesson, number):
    qid=f'g8-patterns-l{lesson:02}-w{number:02}'
    if scene['id']!=qid or len(scene['terms']) not in (4,6) or len(scene['actions'])!=4:
        raise ValueError(f'{qid}: source scene invalid')
    objects=[SemanticObject(id=key,type=kind,value=value,group=group) for key,kind,value,group in [
        ('problem','label',scene['problem'][:160],'given'),('model','label','Pattern position and terms','visual'),
        ('operation','operation','Current pattern action','working'),('result','result','Result of current action','working'),
        ('verification','verification','Check each source position','check')]]
    objects += [SemanticObject(id=f'term-{i}',type='term',value=str(v),group='given') for i,v in enumerate(scene['terms'],1)]
    steps=[]; before='Read the given pattern and its position labels'
    for index,action in enumerate(scene['actions'],1):
        last=index==4
        after=(f'Verified: {scene["answer"]}. {scene["memo"]}' if last else f'{index}. {action}')
        duration=max(5500,len(action.split())*450)
        narration=action
        steps.append(TeachingStep(id=f'{qid}-step-{index:02}',step_number=index-1,title=action,
            before_expression=before,working_expression=action,
            operation=MathematicalOperation(type='pattern_step',value=action,action='verify_solution' if last else 'transform_expression'),
            after_expression=after,explanation=StepExplanation(what=narration,
                why=('A single matching term cannot prove a proposed rule.' if lesson==5 else
                     'The first incorrect calculation explains why a predicted value fails.' if lesson==6 else
                     'A proposed pattern must account for all the given positions, not only the last two.'),
                purpose=action,remember=('Find a counterexample before choosing a rule.' if lesson==5 else
                    'Repair the earliest mismatch and check two distant given positions.' if lesson==6 else
                    'Test the rule on every given term and then extend the diagram.')),
            common_mistake=scene.get('misconception','Extending a rule from only one pair of values.'),animation_template='grade8_pattern_board',
            screen_reader_description=f'{before}. {narration} {after}.',
            visualization_state=VisualizationState(objects=[o.id for o in objects],highlights=['model'],annotations=[f'stage:{index}'],target='model',
                before_state=before,working_state=action,after_state=after),
            instructional_goal=narration,duration_ms=duration,
            events=[TimelineEvent(at_ms=0,type='caption',text=narration),TimelineEvent(at_ms=0,type='narration',text=narration),
                TimelineEvent(at_ms=250,type='focus',targets=['model']),TimelineEvent(at_ms=900,type='show_operation',targets=['operation'],label=action),
                TimelineEvent(at_ms=duration//2,type='reveal',targets=['result'],label=after[:240]),
                TimelineEvent(at_ms=duration-200,type='verify' if last else 'complete',targets=['verification' if last else 'result'])],
            narration=narration,state_after={'stage':index,'question_id':qid,'verification_complete':last,'verification_link':scene['memo'],'completion_state':after}))
        before=after
    board=WhiteboardBlock(id=f'{qid}-board',representation='visual',problem=scene['problem'],
        initial_expression='Read the given pattern and its position labels',steps=steps,
        visualization=VisualizationInstruction(type='algebra',template='grade8_pattern_board',parameters={
            'scene_json':json.dumps(scene,ensure_ascii=False),'question_id':qid,'prompt':scene['problem'],'total_steps':4}),semantic_objects=objects)
    difficulty='foundation' if number==1 else 'easy' if number<=3 else 'standard' if number<=6 else 'intermediate' if number<=9 else 'exam' if number<=12 else 'advanced'
    return WhiteboardQuestion(id=qid,order=number,difficulty=difficulty,is_core_example=number==1,
        guidance_level='high' if number<=5 else 'moderate' if number<=10 else 'reduced',whiteboard=board,
        cognitive_level='knowledge' if number<=3 else 'routine' if number<=6 else 'complex' if number<=12 else 'problem_solving',
        marks=2 if number<=3 else 3 if number<=6 else 5 if number<=12 else 7,
        answer=scene['memo'],full_memo=[*scene['actions'],f'Check: {scene["memo"]}'],
        misconception_tags=[('candidate-rule-matches-one-term' if lesson==5 else
                             'pattern-first-error' if lesson==6 else 'pattern-rule-from-too-few-terms')],expected_evidence=scene['memo'])

def build(number):
    name={1:'numeric-rules',2:'geometric-models',3:'algebraic-rules',4:'missing-values',
          5:'competing-rules',6:'repair-pattern-claims'}[number]
    source=DIR/f'lesson-{number:02}-{name}.md'
    scenes=json.loads((DIR/f'lesson-{number:02}-scenes.json').read_text(encoding='utf-8'))['scenes']
    if len(scenes)!=15: raise ValueError('Pattern pack needs fifteen original examples')
    questions=[_question(s,number,n) for n,s in enumerate(scenes,1)]
    title={1:'Numeric pattern rules',2:'Geometric pattern models',3:'Writing an algebraic rule',
           4:'Finding and checking missing values',5:'Testing competing rules',
           6:'Diagnosing and repairing pattern claims'}[number]
    lesson_id=f'g8-patterns-{number:02}'
    lesson=Lesson(id=lesson_id,order=number,title=title,
        objective={1:'Find and justify rules for numeric patterns, including non-constant differences and alternating paths.',
                   2:'Construct and extend geometric patterns by counting added groups, rows, borders and areas.',
                   3:'Use aligned position and output rows to write and verify a linear algebraic rule.',
                   4:'Substitute into linear and non-linear pattern rules to find and check a missing value.',
                   5:'Reject a plausible but incorrect rule with a counterexample and verify a surviving rule.',
                   6:'Locate the first error in a pattern prediction and repair it using the position and rule.'}[number],
        why_it_matters='Patterns connect observed changes with a rule that predicts later positions.',
        intuition='Position labels anchor the rule; a difference, ratio or figure group must be checked at every given position.',
        prerequisites=[] if number==1 else [f'g8-patterns-{number-1:02}'],estimated_minutes=80,
        difficulty='foundation' if number==1 else 'standard',access_level=AccessLevel.FREE if number==1 else AccessLevel.PREMIUM,
        status=ContentStatus.TEACHER_REVIEW_REQUIRED,
        blocks=[LessonBlock(type='concept',title=title,content=(
            'Two rules can agree at position one. Put each prediction beside the four given outputs, find the first mismatch and then extend the rule that survives.' if number==5 else
            'A learner claim can follow a convincing but invalid continuation. Locate the first broken operation, rebuild the rule from the givens and test a new position.' if number==6 else
            'Read every figure and position. Compare changes, test a candidate rule across the givens, then extend it once and check.')),
            questions[0].whiteboard,
            LessonBlock(type='mistake',title='Check the rule',content=(
                'Reject a rule as soon as its prediction disagrees with a known term. Matching a single term proves nothing.' if number==5 else
                'A copied last difference fails for square, triangular, and ratio patterns; a shifted position fails even for a linear pattern.' if number==6 else
                'A rule fitting the last two values can still fail earlier terms. For a picture, count actual new pieces before writing a formula.')),
            LessonBlock(type='practice',title='Try independently',content='Find the next term and explain why the rule works for all givens.',data={'practice_bank_id':lesson_id}),
            LessonBlock(type='summary',title='From picture or row to rule',content='Label positions, compare changes, justify the structure and verify each given value.')],
        whiteboard_questions=questions,mastery_threshold=.8,paper=None,source_document=source.name,
        source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),release_approved=False,
        assessment_contract={'worked_example_count':15,'practice_count':15,'mastery_question_count':5,
            'parallel_reassessment_count':3,'answer_hidden_before_submission':True,'progression_threshold':.8,
            'runtime_conversion':f'patterns_lesson_{number}_teacher_review'})
    return lesson,questions,scenes,source

LESSON_1,QUESTIONS_1,SCENES_1,SOURCE_1=build(1)
LESSON_2,QUESTIONS_2,SCENES_2,SOURCE_2=build(2)

LESSON_3,QUESTIONS_3,SCENES_3,SOURCE_3=build(3)
LESSON_4,QUESTIONS_4,SCENES_4,SOURCE_4=build(4)
LESSON_5,QUESTIONS_5,SCENES_5,SOURCE_5=build(5)
LESSON_6,QUESTIONS_6,SCENES_6,SOURCE_6=build(6)
