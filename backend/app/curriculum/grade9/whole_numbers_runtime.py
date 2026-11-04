"""First Grade 9 runtime batch, compiled from reviewed source tables."""
import hashlib
import json
from pathlib import Path

from app.curriculum.schemas import (
    AccessLevel, ContentStatus, GradeCurriculum, Lesson, LessonBlock, MathematicalOperation,
    SemanticObject, StepExplanation, Subtopic, TeachingStep, TimelineEvent, Topic,
    VisualizationInstruction, VisualizationState, WhiteboardBlock, WhiteboardQuestion,
)

ROOT=Path(__file__).resolve().parents[4]
SOURCE=ROOT/'docs/curriculum/grade9/whole-numbers'
GENERATED=Path(__file__).with_name('generated')


def build_lesson(number):
    data=json.loads((GENERATED/f'whole_numbers_{number:02}.json').read_text(encoding='utf-8'))
    source=SOURCE/data['source']
    lesson_id=f'g9-whole-numbers-{number:02}'
    template='grade9_number_sets' if number==1 else 'grade9_prime_factors'
    questions=[]
    for index,scene in enumerate(data['worked'],1):
        qid=scene['id'];actions=scene['actions'];previous='Read the original question';steps=[]
        ids=['problem','model','token','category','factor-roots','prime-leaves','selection','operation','result','verification']
        objects=[SemanticObject(id=key,type='label' if key in {'problem','model','category','selection','factor-roots','prime-leaves'} else 'operation' if key=='operation' else 'verification' if key=='verification' else 'result' if key=='result' else 'token',value=key.replace('-',' ')) for key in ids]
        for j,action in enumerate(actions,1):
            final=j==len(actions)
            # The result of each stage is retained by the shared cumulative memo.
            after=f'{j}. {action}'
            why=('The exact value decides its number set.' if number==1 else
                 'Each selected prime power must satisfy every original number.')
            spoken=(f'Let us check {action[7:]}' if action.startswith('Check: ')
                    else f'Our written result is {action[9:]}' if action.startswith('Written: ')
                    else f'We {action[0].lower()}{action[1:]}. {why}')
            duration=max(5500,min(24000,len(spoken.split())*500))
            steps.append(TeachingStep(id=f'{qid}-step-{j:02}',step_number=j-1,title=action,
                before_expression=previous,working_expression=f'From {previous} → {action}',
                operation=MathematicalOperation(type='grade9_set_step' if number==1 else 'grade9_factor_step',value=action,
                    action='verify_solution' if final else 'transform_expression'),
                after_expression=after,
                explanation=StepExplanation(what=action,
                    why='Classify the exact value after simplifying it.' if number==1 else
                        'Prime leaves reproduce the given number; compare powers only after factorising.',
                    purpose=action,remember='Check against the original expression.' if number==1 else
                        'For HCF choose shared smaller powers; for LCM choose all larger powers.'),
                common_mistake=scene['misconception'],animation_template=template,
                screen_reader_description=f'{previous}. {spoken}',
                visualization_state=VisualizationState(objects=ids,highlights=['model'],
                    annotations=[f'stage:{j}'],target='model',before_state=previous,
                    working_state=f'From {previous} → {action}',after_state=after),instructional_goal=action,
                duration_ms=duration,events=[TimelineEvent(at_ms=0,type='caption',text=spoken),
                    TimelineEvent(at_ms=0,type='narration',text=spoken),
                    TimelineEvent(at_ms=350,type='focus',targets=['model']),
                    TimelineEvent(at_ms=1100,type='show_operation',targets=['operation'],label=action[:200]),
                    TimelineEvent(at_ms=duration-600,type='reveal',targets=['result'],label=after[:200]),
                    TimelineEvent(at_ms=duration-120,type='verify' if final else 'complete',targets=['verification' if final else 'result'])],
                narration=spoken,state_after={'stage':j,'question_id':qid,'verification_complete':final,
                    'verification_link':scene['check'] if final else '', 'completion_state':after}))
            previous=after
        board=WhiteboardBlock(id=f'{qid}-board',representation='visual',problem=scene['problem'],
            initial_expression='Read the original question',steps=steps,
            visualization=VisualizationInstruction(type='algebra',template=template,parameters={
                'scene_json':json.dumps(scene,ensure_ascii=False),'question_id':qid,
                'prompt':scene['problem'],'total_steps':len(actions)}),semantic_objects=objects)
        questions.append(WhiteboardQuestion(id=qid,order=index,difficulty=scene['difficulty'],
            is_core_example=index==1,guidance_level='high' if index<=5 else 'moderate' if index<=10 else 'reduced',
            cognitive_level='knowledge' if index<=3 else 'routine' if index<=7 else 'complex' if index<=13 else 'problem_solving',
            marks=2 if index<=3 else 3 if index<=7 else 5 if index<=13 else 7,
            whiteboard=board,answer=scene['check'],full_memo=actions,
            misconception_tags=['number-set-classification' if number==1 else 'prime-power-selection'],
            expected_evidence=scene['check']))
    title='The real number system' if number==1 else 'Prime factors, HCF and LCM'
    lesson=Lesson(id=lesson_id,order=number,title=title,estimated_minutes=70 if number==1 else 80,
        objective='Distinguish natural, whole, integer, rational and irrational real numbers using exact values.' if number==1 else
            'Factorise positive integers, calculate HCF and LCM with prime powers, and check context units.',
        why_it_matters='Exact number classifications guide later algebra.' if number==1 else
            'Prime factors make shared groups and repeated cycles precise.',
        intuition='Simplify the value, then choose its smallest set and all containing sets.' if number==1 else
            'HCF keeps shared lowest powers; LCM keeps the highest powers present in any original number.',
        prerequisites=[] if number==1 else ['g9-whole-numbers-01'],difficulty='foundation' if number==1 else 'standard',
        access_level=AccessLevel.FREE if number==1 else AccessLevel.PREMIUM,
        status=ContentStatus.TEACHER_REVIEW_REQUIRED,release_approved=False,
        blocks=[LessonBlock(type='concept',title=title,content='Read the original givens and predict the next mathematical action.'),
            questions[0].whiteboard,
            LessonBlock(type='mistake',title='First error to avoid',content='Check the exact expression and the chosen mathematical rule.'),
            LessonBlock(type='practice',title='Work in your book, then choose',content='Choose one of four answers after working independently.',data={'practice_bank_id':lesson_id}),
            LessonBlock(type='summary',title='Check the original',content='Verify the result against the question, including units.')],
        whiteboard_questions=questions,mastery_threshold=.8,paper=None,source_document=source.name,
        source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),assessment_contract={
            'worked_example_count':15,'practice_count':15,'mastery_question_count':5,
            'parallel_reassessment_count':3,'answer_hidden_before_submission':True,
            'progression_threshold':.8,'runtime_conversion':'grade9_teacher_review_required'})
    return lesson,data


LESSON_1,DATA_1=build_lesson(1)
LESSON_2,DATA_2=build_lesson(2)

GRADE_9=GradeCurriculum(id='grade-9',grade=9,status=ContentStatus.TEACHER_REVIEW_REQUIRED,
    topics=[Topic(id='whole-numbers',product_order=1,title='Whole Numbers',official_caps_topic='Whole numbers',
        caps_sequence=1,term=1,expected_duration='Eight planned lessons; first two authored for review',
        caps_reference='DBE 2026 Grade 9 Mathematics ATP, Term 1',paper=None,
        exam_relevance='Grade 9 classroom and formal assessment',status=ContentStatus.TEACHER_REVIEW_REQUIRED,
        subtopics=[Subtopic(id='whole-numbers-learning-path',order=1,title='Properties, prime factors and applications',
            prerequisites=[],lessons=[LESSON_1,LESSON_2])])])
