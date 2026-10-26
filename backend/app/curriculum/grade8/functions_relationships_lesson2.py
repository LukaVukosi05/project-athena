"""Original Grade 8 equivalent-representations lesson; teacher review required."""
import json
from pathlib import Path

from app.curriculum.grade8.functions_relationships_lesson1 import question
from app.curriculum.schemas import AccessLevel, ContentStatus, Lesson, LessonBlock

DATA=json.loads((Path(__file__).with_name('generated')/'functions_relationships_02.json').read_text(encoding='utf-8'))
LESSON_ID='g8-functions-relationships-02'
SOURCE=DATA['source_document']
QUESTIONS=[question(item,n) for n,item in enumerate(DATA['worked_examples'])]

LESSON=Lesson(
    id=LESSON_ID,order=2,title='Equivalent forms of a relationship',
    objective='Translate among words, flow diagrams, tables and formulae; justify an identity by algebra and reject a false equivalence with a shared-input counterexample.',
    why_it_matters='The same relationship appears in different forms in questions and real situations. A learner must recognize when the forms agree and when similar-looking rules change the operation or domain.',
    intuition='Name the input and the operations in order. Use brackets when an arrow acts on a whole quantity. Check given rows, prove all-input claims by a valid transformation, and disprove a claim with one shared input that differs.',
    prerequisites=['g8-functions-relationships-01','distributive law','substitution'],estimated_minutes=90,
    difficulty='standard',access_level=AccessLevel.FREE,status=ContentStatus.TEACHER_REVIEW_REQUIRED,
    blocks=[LessonBlock(type='concept',title='Same relationship, different descriptions',
        content='Read the verbal rule and show its flow, formula and table. Agreement on displayed rows is evidence only for those rows. Distribution can prove an identity on the common domain; one counterexample disproves equivalence.'),
        QUESTIONS[0].whiteboard,
        LessonBlock(type='mistake',title='Stop at the first changed operation',
            content='Find where the bracket, order, sign, fixed amount or domain changed between two representations.',
            data={'repairs':[{'question_id':item['id'],'repair':item['repair']} for item in DATA['worked_examples']]}),
        LessonBlock(type='practice',title='Independent translation and comparison',
            content='Build and test each new representation before revealing a worked explanation.',data={'practice_bank_id':LESSON_ID}),
        LessonBlock(type='summary',title='Prove or disprove with the right evidence',
            content='To show equivalence for all inputs, derive the same expression with legal algebra and the same domain. To show non-equivalence, find one input where outputs differ.')],
    whiteboard_questions=QUESTIONS,mastery_threshold=.8,paper=None,
    source_document=SOURCE,source_sha256=DATA['source_sha256'],release_approved=False,
    assessment_contract={'worked_example_count':15,'practice_count':15,'mastery_question_count':5,
        'parallel_reassessment_count':3,'answer_hidden_before_submission':True,
        'progression_threshold':.8,'runtime_conversion':'functions_relationships_lesson_2'})
