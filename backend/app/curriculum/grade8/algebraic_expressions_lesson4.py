"""Authored Grade 8 Expressions Lesson 4; source remains under teacher review."""
import json
from pathlib import Path

from app.curriculum.grade8.algebraic_expressions import question
from app.curriculum.schemas import AccessLevel, ContentStatus, Lesson, LessonBlock

DATA = json.loads((Path(__file__).with_name('generated') / 'algebraic_expressions_04.json').read_text(encoding='utf-8'))
SOURCE = DATA['source_document']
LESSON_ID = 'g8-algebraic-expressions-04'
QUESTIONS = [question(item, n, item['model']) for n, item in enumerate(DATA['worked_examples'])]
for item, worked in zip(DATA['worked_examples'], QUESTIONS):
    worked.full_memo = [
        f"{step['title']}: {before} → {after}. {step['narration']}"
        for step, before, after in zip(item['steps'], item['states'], item['states'][1:])
    ] + [f"Verify against the original: {item['verify']}"]

LESSON = Lesson(id=LESSON_ID, order=4, title='Distributing a monomial',
    objective='Expand a monomial multiplied by a binomial or trinomial by multiplying every signed term and verify equivalence by substitution.',
    why_it_matters='Bracket expansion underpins area, pricing and later factorisation. Every missed term or sign changes the value of the expression.',
    intuition='Each signed bracket term receives its own copy of the outside multiplier. The separate partial products remain visible before simplification.',
    prerequisites=['Lesson 3 monomial products', 'signed terms', 'like terms'],
    estimated_minutes=80, difficulty='standard', access_level=AccessLevel.FREE,
    status=ContentStatus.TEACHER_REVIEW_REQUIRED,
    blocks=[LessonBlock(type='concept', title='Send a factor to every term',
        content='First mark the boundaries of the bracket and read every term with its sign. Multiply the outside monomial by each signed term. Show the partial products, simplify their coefficients and powers, then check the original expression at a chosen value.'),
        QUESTIONS[0].whiteboard,
        LessonBlock(type='mistake', title='Find the first missing path',
            content='Compare each bracket term with its own multiplication path. Repair the first missing term, lost sign or exponent before checking a new example.',
            data={'repairs':[{'question_id':q['id'],'repair':q['repair']} for q in DATA['worked_examples']]}),
        LessonBlock(type='practice', title='Independent practice',
            content='Submit your own expansion before hints and the authored memo are shown.',
            data={'practice_bank_id':LESSON_ID}),
        LessonBlock(type='summary', title='Check each path',
            content='Count the signed bracket terms; distribute to every one; retain unlike powers and units; check the expanded form against the original at a number.')],
    whiteboard_questions=QUESTIONS, mastery_threshold=.8, paper=None,
    source_document=SOURCE, source_sha256=DATA['source_sha256'], release_approved=False,
    assessment_contract={'worked_example_count':15,'practice_count':15,'mastery_question_count':5,
        'parallel_reassessment_count':3,'answer_hidden_before_submission':True,
        'progression_threshold':.8,'runtime_conversion':'algebraic_expressions_lesson_4'})
