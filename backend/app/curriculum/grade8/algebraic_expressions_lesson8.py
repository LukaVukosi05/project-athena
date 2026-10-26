"""Original Grade 8 Expressions Lesson 8; source awaits teacher review."""
import json
from pathlib import Path

from app.curriculum.grade8.algebraic_expressions import question
from app.curriculum.schemas import AccessLevel, ContentStatus, Lesson, LessonBlock

DATA=json.loads((Path(__file__).with_name('generated')/'algebraic_expressions_08.json').read_text(encoding='utf-8'))
SOURCE=DATA['source_document']
LESSON_ID='g8-algebraic-expressions-08'
QUESTIONS=[question(item,n,item['model']) for n,item in enumerate(DATA['worked_examples'])]
for item,worked in zip(DATA['worked_examples'],QUESTIONS):
    worked.full_memo=[
        f"{step['title']}: {before} → {after}. {step['narration']}"
        for step,before,after in zip(item['steps'],item['states'],item['states'][1:])
    ]+[f"Verify against the original: {item['verify']}"]

LESSON=Lesson(
    id=LESSON_ID,order=8,title='Mixed simplification and verification',
    objective='Choose and sequence expansion, termwise division and like-term collection; preserve restrictions and verify the simplified expression.',
    why_it_matters='Choosing the right operation order connects earlier algebra skills and lets learners audit formulas, geometry and equivalent expressions.',
    intuition='Read the whole expression, finish each bracket or quotient path, sort terms by variable and power, and verify in the original.',
    prerequisites=['Lesson 4 expansion','Lesson 5 division','Lesson 7 substitution'],
    estimated_minutes=95,difficulty='standard',access_level=AccessLevel.FREE,
    status=ContentStatus.TEACHER_REVIEW_REQUIRED,
    blocks=[
        LessonBlock(type='concept',title='Choose a legal simplification path',
            content='Mark variable denominator restrictions first. Expand both paths of every bracket, divide each numerator term, then sort matching variable powers and constants. Keep every completed state on the board.'),
        QUESTIONS[0].whiteboard,
        LessonBlock(type='mistake',title='Find the first invalid operation',
            content='Check each distribution arrow, quotient term and sign. Diagnose the first invalid operation, then retry a parallel expression.',
            data={'repairs':[{'question_id':q['id'],'repair':q['repair']} for q in DATA['worked_examples']]}),
        LessonBlock(type='practice',title='Independent practice',
            content='Simplify independently before viewing a hint or worked memo.',
            data={'practice_bank_id':LESSON_ID}),
        LessonBlock(type='summary',title='Return to the original expression',
            content='State denominator restrictions, complete every expansion and quotient, collect only matching term types and substitute a permitted value to check the result.')],
    whiteboard_questions=QUESTIONS,mastery_threshold=.8,paper=None,
    source_document=SOURCE,source_sha256=DATA['source_sha256'],release_approved=False,
    assessment_contract={'worked_example_count':15,'practice_count':15,
        'mastery_question_count':5,'parallel_reassessment_count':3,
        'answer_hidden_before_submission':True,'progression_threshold':.8,
        'runtime_conversion':'algebraic_expressions_lesson_8'},
)
