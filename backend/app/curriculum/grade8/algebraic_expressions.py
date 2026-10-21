"""Authored Grade 8 algebraic expressions lesson; generated data is source-derived.

The DOCX remains the review source. The runtime intentionally contains no AI
question generation and does not put private solution text in visual parameters.
"""
from __future__ import annotations

import json
from pathlib import Path

from app.curriculum.schemas import (AccessLevel, ContentStatus, Lesson, LessonBlock,
    MathematicalOperation, SemanticObject, StepExplanation, TeachingStep,
    TimelineEvent, VisualizationInstruction, VisualizationState, WhiteboardBlock,
    WhiteboardQuestion)

DATA = json.loads((Path(__file__).with_name('generated') / 'algebraic_expressions_01.json').read_text(encoding='utf-8'))
SOURCE = DATA['source_document']
LESSON_ID = 'g8-algebraic-expressions-01'

# Given objects only. Intermediate calculations and answers come from the gated
# teaching states, never from the initial visualization parameters.
MODELS = [
 ('expression_tiles', ['4', 'x', '+7'], 'coefficient, variable and constant'),
 ('signed_terms', ['-3', 'a', '+5'], 'signed multiplier, variable and constant'),
 ('signed_terms', ['2x', '-4y', '+9'], 'terms'),
 ('grouped_terms', ['n', 'n', 'n', '+5'], 'three copies'),
 ('grouped_terms', ['n', 'n', 'n', '-5'], 'three copies'),
 ('fraction_bar', ['p', '÷2', '+7'], 'half then increase'),
 ('square_comparison', ['x = 3', '2 × x', 'x × x'], 'two operations'),
 ('like_term_sort', ['4x', '+2x', '-3'], 'sort like terms'),
 ('unlike_term_sort', ['2a', '+3b', 'claim: 5ab'], 'different variables'),
 ('square_comparison', ['-2', 'x = -3', 'x × x'], 'square the variable'),
 ('receipt', ['R12 × t passengers', 'R8 once'], 'trip receipt'),
 ('receipt', ['R12 × 5 passengers', 'R8 once'], 'five passenger receipt'),
 ('grouped_terms', ['x + 3', 'x + 3', 'claim: 2x + 3'], 'two complete groups'),
 ('rectangle', ['x + 3 cm', 'x cm', 'x + 3 cm', 'x cm'], 'four sides'),
 ('grouped_terms', ['n + 2', 'n + 2', 'n + 2'], 'three complete groups'),
]


def question(item: dict, index: int) -> WhiteboardQuestion:
    family, tokens, description = MODELS[index]
    objects = [SemanticObject(id='problem', type='label', value=item['q'][:160], group='given'),
               SemanticObject(id='model', type='term', value=description, group='visual'),
               SemanticObject(id='operation', type='operation', value='one teaching action', group='working'),
               SemanticObject(id='result', type='result', value='result of current action', group='working'),
               SemanticObject(id='verification', type='verification', value='check the original question', group='check')]
    objects += [SemanticObject(id=f'token-{n}', type='term', value=token, group='model') for n, token in enumerate(tokens, 1)]
    steps = []
    states = item['states']
    authored_steps = list(item['steps']) + [('Check the original question',
        'Substitute or reconstruct the original quantities and compare both sides.',
        item['verify'])]
    verified_states = list(states) + [f"Checked: {item['verify']}"]
    for n, ((title, action, narration), before, after) in enumerate(zip(authored_steps, verified_states, verified_states[1:])):
        # The action is made visible first; the mathematical result follows.
        duration = max(4400, 400 * len(narration.split()))
        focus = f'token-{min(n + 1, len(tokens))}'
        events = [TimelineEvent(at_ms=0, type='caption', text=narration),
                  TimelineEvent(at_ms=0, type='narration', text=narration),
                  TimelineEvent(at_ms=250, type='focus', targets=[focus]),
                  TimelineEvent(at_ms=900, type='show_operation', targets=['operation'], label=title),
                  TimelineEvent(at_ms=duration // 2, type='reveal', targets=['result'], label=after),
                  TimelineEvent(at_ms=duration - 200, type='verify' if n == len(authored_steps)-1 else 'complete',
                                targets=['verification' if n == len(authored_steps)-1 else 'result'])]
        steps.append(TeachingStep(
            id=f"{item['id']}-step-{n+1:02}", step_number=n, title=title,
            before_expression=before, working_expression=action,
            operation=MathematicalOperation(type=f'{family}_step', value=action,
                action='verify_solution' if n == len(authored_steps)-1 else 'transform_expression'),
            after_expression=after,
            explanation=StepExplanation(what=narration, why=item['misconception'],
                purpose=action, remember=item['repair']),
            common_mistake=item['misconception'], animation_template=family,
            screen_reader_description=f'{before}. {narration} {after}.',
            visualization_state=VisualizationState(objects=[o.id for o in objects],
                highlights=[focus], annotations=[f'stage:{n+1}'], target=focus,
                before_state=before, working_state=action, after_state=after),
            instructional_goal=narration, duration_ms=duration, events=events,
            narration=narration,
            state_after={'stage':n+1, 'question_id':item['id'],
                'verification_complete':n == len(authored_steps)-1,
                'verification_link':item['verify'],
                'completion_state':after},
        ))
    board = WhiteboardBlock(id=f"{item['id']}-board", representation='visual',
        problem=item['q'], initial_expression=states[0], steps=steps,
        visualization=VisualizationInstruction(type='algebra', template=family,
            parameters={'prompt':item['q'], 'question_id':item['id'],
                'model_tokens':tokens, 'model_description':description,
                'total_steps':len(steps)}), semantic_objects=objects)
    level=item['level'].lower()
    return WhiteboardQuestion(id=item['id'], order=index+1, difficulty=level,
        is_core_example=index==0, guidance_level='high' if index<5 else 'moderate' if index<10 else 'reduced',
        whiteboard=board, cognitive_level='knowledge' if index<3 else 'routine' if index<8 else 'complex' if index<13 else 'problem_solving',
        marks=item['marks'], answer=item['answer'],
        full_memo=[f'{title}: {action}. {narration}' for title,action,narration in item['steps']] + [item['verify']],
        misconception_tags=[item['misconception']], expected_evidence=item['verify'])


QUESTIONS = [question(item, n) for n,item in enumerate(DATA['examples'])]
LESSON = Lesson(id=LESSON_ID, order=1, title='Reading and building algebraic expressions',
    objective='Identify variables, signed terms, coefficients and exponents; translate and simplify expressions and verify them.',
    why_it_matters='Reading each symbol correctly prepares learners to use formulas, solve equations and model real quantities.',
    intuition='An expression is built from quantities. A signed term stays together, and only terms of the same kind can be combined.',
    prerequisites=['integer signs', 'multiplication and division', 'order of operations'],
    estimated_minutes=70, difficulty='foundation', access_level=AccessLevel.FREE,
    status=ContentStatus.TEACHER_REVIEW_REQUIRED,
    blocks=[LessonBlock(type='concept', title='Build the language of algebra', content='Letters represent changing quantities. A coefficient multiplies a variable. The sign belongs to the following term. Compare tiles, grouping and numeric checks before combining terms.'),
        QUESTIONS[0].whiteboard,
        LessonBlock(type='mistake', title='Find the first wrong step', content='Compare the learner line with the original expression. Keep signed terms together, distinguish multiplication from powers, and check every bracket term.', data={'repairs':[{'question_id':q['id'], 'repair':q['repair']} for q in DATA['examples']]}),
        LessonBlock(type='practice', title='Independent practice', content='Try each question before submitting. Hints and the worked solution appear only through the practice flow.', data={'practice_bank_id':LESSON_ID}),
        LessonBlock(type='summary', title='What to remember', content='Read the whole expression, preserve signed terms, build the described operation in order, combine only like terms, and substitute to check a result.')],
    whiteboard_questions=QUESTIONS, mastery_threshold=.8, paper=None,
    source_document=SOURCE, source_sha256=DATA['source_sha256'], release_approved=False,
    assessment_contract={'worked_example_count':15,'practice_count':15,'mastery_question_count':5,
        'parallel_reassessment_count':3,'answer_hidden_before_submission':True,
        'progression_threshold':.8,'runtime_conversion':'algebraic_expressions_lesson_1'})
