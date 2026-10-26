"""Grade 8 expressions Lesson 3, authored from the reviewed source pack."""
import json
from pathlib import Path

from app.curriculum.grade8.algebraic_expressions import question
from app.curriculum.schemas import AccessLevel, ContentStatus, Lesson, LessonBlock

DATA = json.loads((Path(__file__).with_name('generated') / 'algebraic_expressions_03.json').read_text(encoding='utf-8'))
SOURCE = DATA['source_document']
LESSON_ID = 'g8-algebraic-expressions-03'
QUESTIONS = [question(item, n, item['model']) for n, item in enumerate(DATA['worked_examples'])]

LESSON = Lesson(id=LESSON_ID, order=3, title='Multiplying monomials',
    objective='Multiply signed integers and monomials, use the exponent rules for variable factors, and interpret products as area or grouped quantities.',
    why_it_matters='Products appear throughout algebra, geometry and cost models. Separating signs, numbers and variable factors prevents silent errors.',
    intuition='A product builds equal groups or an area: multiply signed counts, then count each kind of variable factor.',
    prerequisites=['signed multiplication', 'algebraic terms', 'meaning of exponents', 'Lesson 2 like terms'],
    estimated_minutes=75, difficulty='standard', access_level=AccessLevel.FREE,
    status=ContentStatus.TEACHER_REVIEW_REQUIRED,
    blocks=[LessonBlock(type='concept', title='Build the product from factors',
        content='Use repeated groups, sign badges, x-by-x area tiles and factor stacks to multiply. Multiply numerical coefficients, determine the sign, count variable factors, then verify by substitution.'),
        QUESTIONS[0].whiteboard,
        LessonBlock(type='mistake', title='Locate the first wrong action',
            content='Locate the first factor lost, negative sign mishandled, or power counted incorrectly. Restore it and replay the affected action.',
            data={'repairs':[{'question_id':q['id'], 'repair':q['repair']} for q in DATA['worked_examples']]}),
        LessonBlock(type='practice', title='Independent practice',
            content='Try all questions first; hints and a worked solution follow the practice submission.',
            data={'practice_bank_id':LESSON_ID}),
        LessonBlock(type='summary', title='Check every kind of term',
            content='Use all factors: multiply coefficients and signs, count matching variable factors, keep unlike factors, include squared area units, and test both forms at a numeric input.')],
    whiteboard_questions=QUESTIONS, mastery_threshold=.8, paper=None,
    source_document=SOURCE, source_sha256=DATA['source_sha256'], release_approved=False,
    assessment_contract={'worked_example_count':15,'practice_count':15,'mastery_question_count':5,
        'parallel_reassessment_count':3,'answer_hidden_before_submission':True,
        'progression_threshold':.8,'runtime_conversion':'algebraic_expressions_lesson_3'})
