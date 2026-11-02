"""First-error diagnosis across Grade 8 relationships; teacher review required."""
import json
from pathlib import Path
from app.curriculum.grade8.functions_relationships_lesson1 import question
from app.curriculum.schemas import AccessLevel, ContentStatus, Lesson, LessonBlock
DATA=json.loads((Path(__file__).with_name('generated')/'functions_relationships_06.json').read_text(encoding='utf-8'))
LESSON_ID=DATA['id'];SOURCE=DATA['source_document']
QUESTIONS=[question(row,n) for n,row in enumerate(DATA['worked_examples'])]
LESSON=Lesson(id=LESSON_ID,order=6,title=DATA['title'],
 objective='Find the first incorrect step in a stated relationship, demonstrate a counterexample, repair the rule and verify a fresh input or context.',
 why_it_matters='A later answer can look plausible after a wrong first step. Diagnosing that step lets a learner fix the idea and apply it to new values.',
 intuition='Read the original evidence first. Test the learner claim on a given input, name the first unsupported operation, and put the repaired path beside it. Check the new answer in the original situation.',
 prerequisites=['g8-functions-relationships-01','g8-functions-relationships-02','g8-functions-relationships-03','g8-functions-relationships-04','g8-functions-relationships-05'],estimated_minutes=100,difficulty='exam',
 access_level=AccessLevel.FREE,status=ContentStatus.TEACHER_REVIEW_REQUIRED,
 blocks=[LessonBlock(type='concept',title='Find the first wrong move',content='Check every given row and operation in order. Point to the earliest mismatch; compare the learner path and repaired path at the same input.'),
 QUESTIONS[0].whiteboard,LessonBlock(type='mistake',title='Targeted repairs',content='Repair the operation order, rate, intercept, inverse step or area interpretation before trying a fresh question.',data={'repairs':[{'question_id':row['id'],'repair':row['repair']} for row in DATA['worked_examples']]}),
 LessonBlock(type='practice',title='Diagnose a fresh learner claim',content='Commit to the first error and corrected value before opening hints or the memo.',data={'practice_bank_id':LESSON_ID}),
 LessonBlock(type='summary',title='Recheck the original',content='Prove the repaired relationship against the given words, table or formula; then retry fresh values.')],
 whiteboard_questions=QUESTIONS,mastery_threshold=.8,paper=None,source_document=SOURCE,source_sha256=DATA['source_sha256'],release_approved=False,
 assessment_contract={'worked_example_count':15,'practice_count':15,'mastery_question_count':5,'parallel_reassessment_count':3,
 'answer_hidden_before_submission':True,'progression_threshold':.8,'runtime_conversion':'functions_relationships_lesson_6_teacher_review'})
