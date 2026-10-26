"""Grade 8 expressions Lesson 2, authored from the reviewed source pack."""
import json
from pathlib import Path

from app.curriculum.grade8.algebraic_expressions import question
from app.curriculum.schemas import AccessLevel, ContentStatus, Lesson, LessonBlock

DATA = json.loads((Path(__file__).with_name('generated') / 'algebraic_expressions_02.json').read_text(encoding='utf-8'))
SOURCE = DATA['source_document']
LESSON_ID = 'g8-algebraic-expressions-02'
QUESTIONS = [question(item, n, item['model']) for n, item in enumerate(DATA['worked_examples'])]

LESSON = Lesson(id=LESSON_ID, order=2, title='Adding and subtracting like terms',
    objective='Simplify signed algebraic expressions by grouping terms of the same variable and power, distribute subtraction across brackets, and verify by substitution.',
    why_it_matters='A missed sign or an unlike-term combination changes every later equation and geometry answer.',
    intuition='Count matching algebra tiles together: x bars, y bars and x² squares each have a separate lane. The sign belongs to its tile.',
    prerequisites=['reading signed algebraic terms', 'integer addition and subtraction', 'substitution'],
    estimated_minutes=75, difficulty='standard', access_level=AccessLevel.FREE,
    status=ContentStatus.TEACHER_REVIEW_REQUIRED,
    blocks=[LessonBlock(type='concept', title='Sort by kind, then calculate',
        content='Group terms only when their variable and exponent match. Move a negative term with its sign. Subtracting a bracket changes each term inside it. Keep each intermediate state visible and check by substitution.'),
        QUESTIONS[0].whiteboard,
        LessonBlock(type='mistake', title='Locate the first wrong action',
            content='Inspect the first operation that changes a sign, joins unlike terms, or omits a bracket term; repair that action before proceeding.',
            data={'repairs':[{'question_id':q['id'], 'repair':q['repair']} for q in DATA['worked_examples']]}),
        LessonBlock(type='practice', title='Independent practice',
            content='Try all questions first; hints and a worked solution follow the practice submission.',
            data={'practice_bank_id':LESSON_ID}),
        LessonBlock(type='summary', title='Check every kind of term',
            content='Keep the sign attached; group identical variable powers; change every sign when subtracting a bracket; evaluate the original and final expressions at a test value.')],
    whiteboard_questions=QUESTIONS, mastery_threshold=.8, paper=None,
    source_document=SOURCE, source_sha256=DATA['source_sha256'], release_approved=False,
    assessment_contract={'worked_example_count':15,'practice_count':15,'mastery_question_count':5,
        'parallel_reassessment_count':3,'answer_hidden_before_submission':True,
        'progression_threshold':.8,'runtime_conversion':'algebraic_expressions_lesson_2'})
