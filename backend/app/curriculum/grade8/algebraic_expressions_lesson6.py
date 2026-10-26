"""Original Grade 8 Expressions Lesson 6; source awaits teacher review."""
import json
from pathlib import Path

from app.curriculum.grade8.algebraic_expressions import question
from app.curriculum.schemas import AccessLevel, ContentStatus, Lesson, LessonBlock

DATA=json.loads((Path(__file__).with_name('generated')/'algebraic_expressions_06.json').read_text(encoding='utf-8'))
SOURCE=DATA['source_document']
LESSON_ID='g8-algebraic-expressions-06'
QUESTIONS=[question(item,n,item['model']) for n,item in enumerate(DATA['worked_examples'])]
for item,worked in zip(DATA['worked_examples'],QUESTIONS):
    worked.full_memo=[
        f"{step['title']}: {before} → {after}. {step['narration']}"
        for step,before,after in zip(item['steps'],item['states'],item['states'][1:])
    ]+[f"Verify against the original: {item['verify']}"]

LESSON=Lesson(
    id=LESSON_ID,order=6,title='Powers and roots of algebraic terms',
    objective='Find squares, cubes, square roots and cube roots of algebraic terms, explaining signed factors and the principal square root.',
    why_it_matters='Powers and roots occur in area, volume and algebraic simplification. A missed sign or root condition changes the answer.',
    intuition='A square uses two identical factors and a cube uses three. Square roots pair factors and return nonnegative magnitudes; cube roots group factors in threes.',
    prerequisites=['Lesson 3 signed monomial products','square and cube numbers','repeated multiplication'],
    estimated_minutes=85,difficulty='standard',access_level=AccessLevel.FREE,
    status=ContentStatus.TEACHER_REVIEW_REQUIRED,
    blocks=[
        LessonBlock(type='concept',title='Group factors before applying a power or root',
            content='Draw two or three copies of the entire base. Square-root diagrams pair equal factors and return the nonnegative value; cube-root diagrams form triples and preserve the sign. Check at both positive and negative inputs when unrestricted.'),
        QUESTIONS[0].whiteboard,
        LessonBlock(type='mistake',title='Find the first sign or root error',
            content='Compare each copied factor, sign and root condition with the original. Repair the first error before a parallel retry.',
            data={'repairs':[{'question_id':q['id'],'repair':q['repair']} for q in DATA['worked_examples']]}),
        LessonBlock(type='practice',title='Independent practice',
            content='Submit each power or root before viewing the authored hint or memo.',
            data={'practice_bank_id':LESSON_ID}),
        LessonBlock(type='summary',title='Raise the root result to its power',
            content='Count complete base factors; pair for a square root, group triples for a cube root; retain the principal square-root sign and verify against the original.')],
    whiteboard_questions=QUESTIONS,mastery_threshold=.8,paper=None,
    source_document=SOURCE,source_sha256=DATA['source_sha256'],release_approved=False,
    assessment_contract={'worked_example_count':15,'practice_count':15,
        'mastery_question_count':5,'parallel_reassessment_count':3,
        'answer_hidden_before_submission':True,'progression_threshold':.8,
        'runtime_conversion':'algebraic_expressions_lesson_6'},
)
