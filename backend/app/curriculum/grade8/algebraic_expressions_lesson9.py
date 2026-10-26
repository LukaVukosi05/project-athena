"""Original Grade 8 Expressions Lesson 9; source awaits teacher review."""
import json
from pathlib import Path

from app.curriculum.grade8.algebraic_expressions import question
from app.curriculum.schemas import AccessLevel, ContentStatus, Lesson, LessonBlock

DATA=json.loads((Path(__file__).with_name('generated')/'algebraic_expressions_09.json').read_text(encoding='utf-8'))
SOURCE=DATA['source_document']
LESSON_ID='g8-algebraic-expressions-09'
QUESTIONS=[question(item,n,item['model']) for n,item in enumerate(DATA['worked_examples'])]
for item,worked in zip(DATA['worked_examples'],QUESTIONS):
    worked.full_memo=[
        f"{step['title']}: {before} → {after}. {step['narration']}"
        for step,before,after in zip(item['steps'],item['states'],item['states'][1:])
    ]+[f"Verify against the original: {item['verify']}"]

LESSON=Lesson(
    id=LESSON_ID,order=9,title='Representations and contextual expressions',
    objective='Translate between verbal rules, tables, flow diagrams and formulae; model fixed and variable quantities and check the rule in its context.',
    why_it_matters='A correct algebraic rule lets learners predict and compare real quantities, identify a wrong fee or unit and move between different representations.',
    intuition='Label the variable and its unit, trace repeated and fixed parts separately, then check the model with a concrete input.',
    prerequisites=['Lesson 7 substitution','Lesson 8 mixed simplification','input-output tables'],
    estimated_minutes=100,difficulty='standard',access_level=AccessLevel.FREE,
    status=ContentStatus.TEACHER_REVIEW_REQUIRED,
    blocks=[
        LessonBlock(type='concept',title='Build a rule from the story or representation',
            content='Identify the input, repeated rate, one-off amount and operation order. Trace the scenario with a receipt, table, flow or dimension model, then write a general rule and verify its units and outputs.'),
        QUESTIONS[0].whiteboard,
        LessonBlock(type='mistake',title='Find the first mismatch with the story',
            content='Check whether a one-off amount was repeated, an operation was applied in the wrong order, or a unit was lost; repair that first mismatch.',
            data={'repairs':[{'question_id':q['id'],'repair':q['repair']} for q in DATA['worked_examples']]}),
        LessonBlock(type='practice',title='Independent practice',
            content='Build the rule and calculate the requested outputs before viewing a hint or memo.',
            data={'practice_bank_id':LESSON_ID}),
        LessonBlock(type='summary',title='Return to the original context',
            content='Name the varying quantity, attach units, repeat only per-unit amounts, trace the flow order and check each table row against the original story.')],
    whiteboard_questions=QUESTIONS,mastery_threshold=.8,paper=None,
    source_document=SOURCE,source_sha256=DATA['source_sha256'],release_approved=False,
    assessment_contract={'worked_example_count':15,'practice_count':15,
        'mastery_question_count':5,'parallel_reassessment_count':3,
        'answer_hidden_before_submission':True,'progression_threshold':.8,
        'runtime_conversion':'algebraic_expressions_lesson_9'},
)
