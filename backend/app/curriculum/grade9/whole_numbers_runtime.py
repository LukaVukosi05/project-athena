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
EXTENDED_TITLES={3:'Ratio and rate',4:'Direct and inverse proportion',5:'Percentages and transactions',
                 6:'Budgets and accounts',7:'Loans and interest',8:'Exchange, commission and rentals'}
EXTENDED_TEMPLATES={3:'grade9_ratio_rate',4:'grade9_proportion',5:'grade9_transaction',
                    6:'grade9_ledger',7:'grade9_interest',8:'grade9_decision'}
INTEGER_TITLES={1:'Ordering and four operations',2:'Sign rules and integer properties',
                3:'Squares, cubes and integer roots',4:'Multi-operation integer contexts',
                5:'First-error diagnosis and reassessment'}
INTEGER_TEMPLATES={n:f'grade9_integer_{n}' for n in range(1,6)}


def build_lesson(number,topic='whole-numbers'):
    integers=topic=='integers'
    data=json.loads((GENERATED/f'{topic.replace("-","_")}_{number:02}.json').read_text(encoding='utf-8'))
    source=(ROOT/'docs/curriculum/grade9'/topic if integers else SOURCE)/data['source']
    lesson_id=f'g9-{topic}-{number:02}'
    template=INTEGER_TEMPLATES[number] if integers else 'grade9_number_sets' if number==1 else 'grade9_prime_factors' if number==2 else EXTENDED_TEMPLATES[number]
    questions=[]
    for index,scene in enumerate(data['worked'],1):
        qid=scene['id'];actions=scene['actions'];previous='Read the original question';steps=[]
        ids=['problem','model','token','category','factor-roots','prime-leaves','selection','operation','result','verification']
        objects=[SemanticObject(id=key,type='label' if key in {'problem','model','category','selection','factor-roots','prime-leaves'} else 'operation' if key=='operation' else 'verification' if key=='verification' else 'result' if key=='result' else 'token',value=key.replace('-',' ')) for key in ids]
        for j,action in enumerate(actions,1):
            final=j==len(actions)
            # The result of each stage is retained by the shared cumulative memo.
            after=f'{j}. {action}'
            why=('Keep the signed values and legal order of operations visible.' if integers else
                 'The exact value decides its number set.' if number==1 else
                 'Each selected prime power must satisfy every original number.' if number==2 else
                 'Read the labelled quantities and units before changing the model.')
            spoken=(f'Let us check {action[7:]}' if action.startswith('Check: ')
                    else f'Our written result is {action[9:]}' if action.startswith('Written: ')
                    else f'We {action[0].lower()}{action[1:]}. {why}')
            duration=max(5500,min(24000,len(spoken.split())*500))
            steps.append(TeachingStep(id=f'{qid}-step-{j:02}',step_number=j-1,title=action,
                before_expression=previous,working_expression=f'From {previous} → {action}',
                operation=MathematicalOperation(type=f'grade9_integer_{number}_step' if integers else 'grade9_set_step' if number==1 else 'grade9_factor_step' if number==2 else f'grade9_{number}_step',value=action,
                    action='verify_solution' if final else 'transform_expression'),
                after_expression=after,
                explanation=StepExplanation(what=action,
                    why='Show one signed operation, then check it against the original values.' if integers else
                        'Classify the exact value after simplifying it.' if number==1 else
                        'Prime leaves reproduce the given number; compare powers only after factorising.' if number==2 else
                        'Keep the original quantities and units attached to each calculation.',
                    purpose=action,remember='Check the original signs and order of operations.' if integers else 'Check against the original expression.' if number==1 else
                        'For HCF choose shared smaller powers; for LCM choose all larger powers.' if number==2 else
                        'Check every derived amount against the original givens.'),
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
            misconception_tags=[scene['misconception'] if integers else 'number-set-classification' if number==1 else 'prime-power-selection' if number==2 else scene['misconception']],
            expected_evidence=scene['check']))
    title=INTEGER_TITLES[number] if integers else 'The real number system' if number==1 else 'Prime factors, HCF and LCM' if number==2 else EXTENDED_TITLES[number]
    lesson=Lesson(id=lesson_id,order=number,title=title,estimated_minutes=70 if number==1 else 80,
        objective=f'Calculate and explain {title.lower()} with signed integers and verify each result.' if integers else
            'Distinguish natural, whole, integer, rational and irrational real numbers using exact values.' if number==1 else
            'Factorise positive integers, calculate HCF and LCM with prime powers, and check context units.' if number==2 else
            f'Use exact Grade 9 methods for {title.lower()} and verify the result with units.',
        why_it_matters='Signed quantities model changes, debt, temperature and later algebra.' if integers else
            'Exact number classifications guide later algebra.' if number==1 else
            'Prime factors make shared groups and repeated cycles precise.' if number==2 else
            'A correct relationship and the right base prevent costly arithmetic errors.',
        intuition='Keep the zero reference, the operation and the sign of each result visible.' if integers else
            'Simplify the value, then choose its smallest set and all containing sets.' if number==1 else
            'HCF keeps shared lowest powers; LCM keeps the highest powers present in any original number.' if number==2 else
            'Keep the original givens visible, apply one justified action and check units.',
        prerequisites=[] if number==1 else [f'g9-{topic}-{number-1:02}'],difficulty='foundation' if number==1 else 'standard',
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
EXTENDED={number:build_lesson(number) for number in range(3,9)}
INTEGER_LESSONS={number:build_lesson(number,'integers') for number in range(1,6)}

GRADE_9=GradeCurriculum(id='grade-9',grade=9,status=ContentStatus.TEACHER_REVIEW_REQUIRED,
    topics=[Topic(id='whole-numbers',product_order=1,title='Whole Numbers',official_caps_topic='Whole numbers',
        caps_sequence=1,term=1,expected_duration='Eight authored lessons awaiting teacher and browser review',
        caps_reference='DBE 2026 Grade 9 Mathematics ATP, Term 1',paper=None,
        exam_relevance='Grade 9 classroom and formal assessment',status=ContentStatus.TEACHER_REVIEW_REQUIRED,
        subtopics=[Subtopic(id='whole-numbers-learning-path',order=1,title='Properties, prime factors and applications',
            prerequisites=[],lessons=[LESSON_1,LESSON_2,*[EXTENDED[n][0] for n in range(3,9)]])]),
        Topic(id='integers',product_order=2,title='Integers',official_caps_topic='Integers',
            caps_sequence=2,term=1,expected_duration='Five authored lessons awaiting teacher and browser review',
            caps_reference='DBE 2026 Grade 9 Mathematics ATP, Term 1',paper=None,
            exam_relevance='Grade 9 classroom and formal assessment',status=ContentStatus.TEACHER_REVIEW_REQUIRED,
            subtopics=[Subtopic(id='integers-learning-path',order=1,title='Signed operations, properties, powers and contexts',
                prerequisites=[],lessons=[INTEGER_LESSONS[n][0] for n in range(1,6)])])])
