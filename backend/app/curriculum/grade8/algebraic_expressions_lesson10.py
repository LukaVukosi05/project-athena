"""Original Grade 8 Expressions Lesson 10; source awaits teacher review."""
import json
from pathlib import Path

from app.curriculum.grade8.algebraic_expressions import question
from app.curriculum.schemas import AccessLevel, ContentStatus, Lesson, LessonBlock

DATA=json.loads((Path(__file__).with_name('generated')/'algebraic_expressions_10.json').read_text(encoding='utf-8'))
SOURCE=DATA['source_document']
LESSON_ID='g8-algebraic-expressions-10'
QUESTIONS=[question(item,n,item['model']) for n,item in enumerate(DATA['worked_examples'])]
for item,worked in zip(DATA['worked_examples'],QUESTIONS):
    worked.full_memo=[
        f"{step['title']}: {before} → {after}. {step['narration']}"
        for step,before,after in zip(item['steps'],item['states'],item['states'][1:])
    ]+[f"Verify against the original: {item['verify']}"]

LESSON=Lesson(
    id=LESSON_ID,order=10,title='Diagnosis and transfer of expressions',
    objective='Identify the earliest invalid algebraic operation, repair the misconception, finish the working and verify against the original question with a fresh input.',
    why_it_matters='Finding the first error prevents learners from memorising an incorrect procedure and transfers the repair to later algebra and mathematical models.',
    intuition='Keep the original and the learner claim visible, compare consecutive lines, reveal a legal operation, check it and try fresh values independently.',
    prerequisites=['Lessons 1–9: expressions, simplification, substitution and contextual rules'],
    estimated_minutes=110,difficulty='standard',access_level=AccessLevel.FREE,
    status=ContentStatus.TEACHER_REVIEW_REQUIRED,
    blocks=[
        LessonBlock(type='concept',title='Spot the first invalid move',
            content='Keep the entire original question and learner claim visible. Check each signed term, multiplication branch, quotient, exponent scope or contextual charge in sequence; stop at the earliest invalid transformation and repair it.'),
        QUESTIONS[0].whiteboard,
        LessonBlock(type='mistake',title='Repair the underlying misconception',
            content='Identify the first incorrect operation and its cause, demonstrate a legal replacement and attempt a fresh parallel question.',
            data={'repairs':[{'question_id':q['id'],'repair':q['repair']} for q in DATA['worked_examples']]}),
        LessonBlock(type='practice',title='Independent practice',
            content='First solve or diagnose independently; submit before the hint and full solution appear.',
            data={'practice_bank_id':LESSON_ID}),
        LessonBlock(type='summary',title='Check the original before moving on',
            content='Keep signs and operation order, state any excluded values, verify with the original expression or context and use a new example to prove the repair transfers.')],
    whiteboard_questions=QUESTIONS,mastery_threshold=.8,paper=None,
    source_document=SOURCE,source_sha256=DATA['source_sha256'],release_approved=False,
    assessment_contract={'worked_example_count':15,'practice_count':15,
        'mastery_question_count':5,'parallel_reassessment_count':3,
        'answer_hidden_before_submission':True,'progression_threshold':.8,
        'runtime_conversion':'algebraic_expressions_lesson_10'},
)
