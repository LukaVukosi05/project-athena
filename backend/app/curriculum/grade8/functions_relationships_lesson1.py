"""Original Grade 8 functions lesson; teacher review remains required."""
import json
from pathlib import Path

from app.curriculum.schemas import (
    AccessLevel, ContentStatus, Lesson, LessonBlock, MathematicalOperation,
    SemanticObject, StepExplanation, TeachingStep, TimelineEvent,
    VisualizationInstruction, VisualizationState, WhiteboardBlock, WhiteboardQuestion,
)

DATA=json.loads((Path(__file__).with_name('generated')/'functions_relationships_01.json').read_text(encoding='utf-8'))
SOURCE=DATA['source_document']
LESSON_ID='g8-functions-relationships-01'


def question(item,index):
    model=item['model'];family=model['family'];givens=model['inputs'];derived=model['outputs']
    objects=[SemanticObject(id='problem',type='label',value=item['q'][:160],group='given'),
             SemanticObject(id='model',type='term',value=model['description'],group='visual'),
             SemanticObject(id='operation',type='operation',value='one legal action',group='working'),
             SemanticObject(id='result',type='result',value='current result',group='working'),
             SemanticObject(id='verification',type='verification',value='check original rule',group='check')]
    objects += [SemanticObject(id=f'given-{i}',type='term',value=v,group='model') for i,v in enumerate(givens,1)]
    objects += [SemanticObject(id=f'derived-{i}',type='term',value='output revealed after teaching',group='model') for i,_ in enumerate(derived,1)]
    states=item['states'];moves=item['steps'];complete=moves+[dict(title='Check the original rule',action='Run the answer through the given rule or table.',narration=item['verify'])]
    chain=states+[f"Checked: {item['verify']}"]
    steps=[]
    for i,(move,before,after) in enumerate(zip(complete,chain,chain[1:])):
        narration=move['narration'];duration=max(4400,400*len(narration.split()))
        focus=f"given-{min(i+1,len(givens))}"
        events=[TimelineEvent(at_ms=0,type='caption',text=narration),
                TimelineEvent(at_ms=0,type='narration',text=narration),
                TimelineEvent(at_ms=250,type='focus',targets=[focus]),
                TimelineEvent(at_ms=900,type='show_operation',targets=['operation'],label=move['title']),
                TimelineEvent(at_ms=duration//2,type='reveal',targets=['result'],label=after),
                TimelineEvent(at_ms=duration-200,type='verify' if i==len(complete)-1 else 'complete',
                    targets=['verification' if i==len(complete)-1 else 'result'])]
        steps.append(TeachingStep(id=f"{item['id']}-step-{i+1:02}",step_number=i,title=move['title'],
            before_expression=before,working_expression=move['action'],
            operation=MathematicalOperation(type=f'{family}_step',value=move['action'],
                action='verify_solution' if i==len(complete)-1 else 'transform_expression'),
            after_expression=after,
            explanation=StepExplanation(what=narration,why=item['misconception'],
                purpose=move['action'],remember=item['repair']),
            common_mistake=item['misconception'],animation_template=family,
            screen_reader_description=f'{before}. {narration} {after}.',
            visualization_state=VisualizationState(objects=[o.id for o in objects],highlights=[focus],
                annotations=[f'stage:{i+1}'],target=focus,before_state=before,
                working_state=move['action'],after_state=after),
            instructional_goal=narration,duration_ms=duration,events=events,narration=narration,
            state_after={'stage':i+1,'question_id':item['id'],
                'verification_complete':i==len(complete)-1,'verification_link':item['verify'],
                'completion_state':after}))
    board=WhiteboardBlock(id=f"{item['id']}-board",representation='visual',
        problem=item['q'],initial_expression=states[0],steps=steps,
        visualization=VisualizationInstruction(type='algebra',template=family,
            parameters={'prompt':item['q'],'question_id':item['id'],
                'given_objects':givens,'derived_objects':derived,'total_steps':len(steps),
                **({'input_values':[row[0] for row in model['rows']],
                    'output_values':[row[1] if row[1] is not None else '?' for row in model['rows']]}
                   if 'rows' in model else {}),
                **({'resolved_outputs':model['resolved_outputs'],
                    'output_reveal_steps':model['output_reveal_steps']}
                   if 'resolved_outputs' in model else {}),
                **({'scene_json':json.dumps(model['scene'],ensure_ascii=False)}
                   if 'scene' in model else {})}),
        semantic_objects=objects)
    return WhiteboardQuestion(id=item['id'],order=index+1,difficulty=item['level'],
        is_core_example=index==0,guidance_level='high' if index<5 else 'moderate' if index<10 else 'reduced',
        whiteboard=board,cognitive_level='knowledge' if index<3 else 'routine' if index<8 else 'complex' if index<13 else 'problem_solving',
        marks=item['marks'],answer=item['answer'],
        full_memo=[f"{move['title']}: {before} → {after}. {move['narration']}"
            for move,before,after in zip(moves,states,states[1:])]+[f"Verify the original: {item['verify']}"],
        misconception_tags=[item['misconception']],expected_evidence=item['verify'])


QUESTIONS=[question(item,n) for n,item in enumerate(DATA['worked_examples'])]
LESSON=Lesson(id=LESSON_ID,order=1,title='Input output values and rules',
    objective='Find input values, output values and rules from flow diagrams, tables, formulae and equations, and compare representations with checks.',
    why_it_matters='Interpreting how a quantity changes helps learners model costs, patterns and later graphs without losing the meaning of each input.',
    intuition='Follow each arrow in order; record intermediate outputs. When an input is missing, reverse the arrows in the opposite order. Test the rule on every given row.',
    prerequisites=['integer operations','simple algebraic expressions','substitution'],estimated_minutes=90,
    difficulty='foundation',access_level=AccessLevel.FREE,status=ContentStatus.TEACHER_REVIEW_REQUIRED,
    blocks=[LessonBlock(type='concept',title='A rule maps each input to an output',
            content='Label the input and output. Show operations in the given order, keep a value between arrows, reverse the flow for a missing input, and check tables row by row.'),
        QUESTIONS[0].whiteboard,
        LessonBlock(type='mistake',title='Find the first wrong arrow',
            content='Compare the operation printed in the machine with the learner move. Keep intermediate values, signed inputs, fixed amounts and units visible.',
            data={'repairs':[{'question_id':q['id'],'repair':q['repair']} for q in DATA['worked_examples']]}),
        LessonBlock(type='practice',title='Independent practice',content='Solve each new flow, table and context before viewing a hint or worked memo.',
            data={'practice_bank_id':LESSON_ID}),
        LessonBlock(type='summary',title='Return to the original relationship',
            content='Run the recovered input forward, check every table row and keep fixed and repeated quantities separate.')],
    whiteboard_questions=QUESTIONS,mastery_threshold=.8,paper=None,
    source_document=SOURCE,source_sha256=DATA['source_sha256'],release_approved=False,
    assessment_contract={'worked_example_count':15,'practice_count':15,
        'mastery_question_count':5,'parallel_reassessment_count':3,
        'answer_hidden_before_submission':True,'progression_threshold':.8,
        'runtime_conversion':'functions_relationships_lesson_1'})
