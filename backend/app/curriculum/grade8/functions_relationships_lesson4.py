"""Grade 8 formulas in context; authored source is under teacher review."""
import json
from pathlib import Path
from app.curriculum.grade8.functions_relationships_lesson1 import question
from app.curriculum.schemas import AccessLevel, ContentStatus, Lesson, LessonBlock

DATA=json.loads((Path(__file__).with_name('generated')/'functions_relationships_04.json').read_text(encoding='utf-8'))
LESSON_ID=DATA['id']
SOURCE=DATA['source_document']
QUESTIONS=[question(item,n) for n,item in enumerate(DATA['worked_examples'])]
LESSON=Lesson(id=LESSON_ID,order=4,title='Formulas in context and reverse calculations',
    objective='Use a formula to calculate a rectangle area or perimeter, recover a missing dimension from area or perimeter, and verify the result with appropriate units.',
    why_it_matters='A formula links quantities in both directions. Many questions give the area and one side rather than two sides.',
    intuition='Draw and label the rectangle. Identify the known and unknown quantities, substitute into the correct formula, undo an operation only on the complete equation, then substitute back into the original context.',
    prerequisites=['g8-functions-relationships-01','g8-functions-relationships-02','multiplication and division'],
    estimated_minutes=95,difficulty='standard',access_level=AccessLevel.FREE,
    status=ContentStatus.TEACHER_REVIEW_REQUIRED,
    blocks=[LessonBlock(type='concept',title='Formulae work in both directions',
        content='Area counts unit squares. If area and width are known, divide area by width to recover length. Perimeter counts the four boundary sides. Name the given values and units before substitution.'),
        QUESTIONS[0].whiteboard,
        LessonBlock(type='mistake',title='Check the first incorrect substitution',
            content='Distinguish area from perimeter, match a number to its formula slot and test the recovered side against the original area.',
            data={'repairs':[{'question_id':item['id'],'repair':item['repair']} for item in DATA['worked_examples']]}),
        LessonBlock(type='practice',title='Try new measurements independently',
            content='Calculate each answer before using a hint or memo.',data={'practice_bank_id':LESSON_ID}),
        LessonBlock(type='summary',title='Verify the rectangle',
            content='Check by multiplying the two sides for area or adding all four sides for perimeter. Use linear units for sides and square units for area.')],
    whiteboard_questions=QUESTIONS,mastery_threshold=.8,paper=None,
    source_document=SOURCE,source_sha256=DATA['source_sha256'],release_approved=False,
    assessment_contract={'worked_example_count':15,'practice_count':15,'mastery_question_count':5,
        'parallel_reassessment_count':3,'answer_hidden_before_submission':True,
        'progression_threshold':.8,'runtime_conversion':'functions_relationships_lesson_4_teacher_review'})
