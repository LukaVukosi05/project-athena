"""Original Grade 8 Expressions Lesson 7; source awaits teacher review."""
import json
from pathlib import Path

from app.curriculum.grade8.algebraic_expressions import question
from app.curriculum.schemas import AccessLevel, ContentStatus, Lesson, LessonBlock

DATA=json.loads((Path(__file__).with_name('generated')/'algebraic_expressions_07.json').read_text(encoding='utf-8'))
SOURCE=DATA['source_document']
LESSON_ID='g8-algebraic-expressions-07'
QUESTIONS=[question(item,n,item['model']) for n,item in enumerate(DATA['worked_examples'])]
for item,worked in zip(DATA['worked_examples'],QUESTIONS):
    worked.full_memo=[
        f"{step['title']}: {before} → {after}. {step['narration']}"
        for step,before,after in zip(item['steps'],item['states'],item['states'][1:])
    ]+[f"Verify against the original: {item['verify']}"]

LESSON=Lesson(
    id=LESSON_ID,order=7,title='Evaluating expressions by substitution',
    objective='Substitute given values into every named variable, preserve signed brackets and operation order, then verify the numerical value in the original expression.',
    why_it_matters='Substitution connects a rule to a measurable number; it also checks equivalent expressions, geometry formulas and permitted values.',
    intuition='A variable is a labelled slot. Put the given signed value in every matching slot, keep the expression structure, then calculate one operation at a time.',
    prerequisites=['signed integer operations','Lesson 6 powers and roots','brackets and order of operations'],
    estimated_minutes=85,difficulty='standard',access_level=AccessLevel.FREE,
    status=ContentStatus.TEACHER_REVIEW_REQUIRED,
    blocks=[
        LessonBlock(type='concept',title='Fill every variable slot before calculating',
            content='Show the original expression and each labelled value chip. Replace one occurrence of each variable with a complete bracketed value before calculating. Keep separate lanes for multiple inputs, powers, fraction denominators and geometry dimensions.'),
        QUESTIONS[0].whiteboard,
        LessonBlock(type='mistake',title='Find the first invalid substitution',
            content='Check every variable occurrence, negative bracket and fraction bar. Diagnose the first error, then retry a parallel question.',
            data={'repairs':[{'question_id':q['id'],'repair':q['repair']} for q in DATA['worked_examples']]}),
        LessonBlock(type='practice',title='Independent practice',
            content='Submit the numerical value before viewing a hint or worked memo.',
            data={'practice_bank_id':LESSON_ID}),
        LessonBlock(type='summary',title='Check in the original expression',
            content='Map values to slots, insert brackets for negatives, apply powers and multiplication before addition, reject zero denominators, then recheck the original expression.')],
    whiteboard_questions=QUESTIONS,mastery_threshold=.8,paper=None,
    source_document=SOURCE,source_sha256=DATA['source_sha256'],release_approved=False,
    assessment_contract={'worked_example_count':15,'practice_count':15,
        'mastery_question_count':5,'parallel_reassessment_count':3,
        'answer_hidden_before_submission':True,'progression_threshold':.8,
        'runtime_conversion':'algebraic_expressions_lesson_7'},
)
