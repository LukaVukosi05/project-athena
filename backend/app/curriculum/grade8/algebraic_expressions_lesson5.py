"""Original Grade 8 Expressions Lesson 5; source awaits teacher review."""
import json
from pathlib import Path

from app.curriculum.grade8.algebraic_expressions import question
from app.curriculum.schemas import AccessLevel, ContentStatus, Lesson, LessonBlock

DATA=json.loads((Path(__file__).with_name('generated')/'algebraic_expressions_05.json').read_text(encoding='utf-8'))
SOURCE=DATA['source_document']
LESSON_ID='g8-algebraic-expressions-05'
QUESTIONS=[question(item,n,item['model']) for n,item in enumerate(DATA['worked_examples'])]
for item,worked in zip(DATA['worked_examples'],QUESTIONS):
    worked.full_memo=[
        f"{step['title']}: {before} → {after}. {step['narration']}"
        for step,before,after in zip(item['steps'],item['states'],item['states'][1:])
    ]+[f"Verify against the original: {item['verify']}"]

LESSON=Lesson(
    id=LESSON_ID,order=5,title='Dividing algebraic expressions',
    objective='Divide each signed term of a monomial, binomial or trinomial by an integer or nonzero monomial; preserve sign, exponents and domain restrictions.',
    why_it_matters='Dividing only one term or cancelling too many variable factors changes the value of an expression. This skill supports algebraic simplification and checking.',
    intuition='The divisor is shared with every signed term in the numerator. Factor cancellation happens inside each separate quotient, and a variable divisor cannot be zero.',
    prerequisites=['Lesson 2 signed like terms','Lesson 3 multiplying monomials and exponents','Lesson 4 distribution across brackets'],
    estimated_minutes=85,difficulty='standard',access_level=AccessLevel.FREE,
    status=ContentStatus.TEACHER_REVIEW_REQUIRED,
    blocks=[
        LessonBlock(type='concept',title='One divisor per signed term',
            content='Name each signed term, make a quotient lane for every term, then reduce coefficients and matching variable factors separately. State x ≠ 0 before cancelling x in a divisor. Check by reconstructing the original at a permitted input.'),
        QUESTIONS[0].whiteboard,
        LessonBlock(type='mistake',title='Find the first missed division',
            content='Compare every numerator term with its quotient lane. Repair the first undivided term, sign, factor or zero restriction before reassessment.',
            data={'repairs':[{'question_id':q['id'],'repair':q['repair']} for q in DATA['worked_examples']]}),
        LessonBlock(type='practice',title='Independent practice',
            content='Submit each quotient before viewing an authored hint or memo.',
            data={'practice_bank_id':LESSON_ID}),
        LessonBlock(type='summary',title='Reconstruct to verify',
            content='Count signed numerator terms; divide every term; cancel only matching factors; keep any zero exclusion; multiply back at a permitted value.')],
    whiteboard_questions=QUESTIONS,mastery_threshold=.8,paper=None,
    source_document=SOURCE,source_sha256=DATA['source_sha256'],release_approved=False,
    assessment_contract={'worked_example_count':15,'practice_count':15,
        'mastery_question_count':5,'parallel_reassessment_count':3,
        'answer_hidden_before_submission':True,'progression_threshold':.8,
        'runtime_conversion':'algebraic_expressions_lesson_5'},
)
