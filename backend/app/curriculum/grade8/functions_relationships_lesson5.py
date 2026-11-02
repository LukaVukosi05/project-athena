"""Matching words, flow diagrams, tables and equations; teacher review required."""
import json
from pathlib import Path
from app.curriculum.grade8.functions_relationships_lesson1 import question
from app.curriculum.schemas import AccessLevel, ContentStatus, Lesson, LessonBlock
DATA=json.loads((Path(__file__).with_name('generated')/'functions_relationships_05.json').read_text(encoding='utf-8'))
LESSON_ID=DATA['id'];SOURCE=DATA['source_document']
QUESTIONS=[question(row,n) for n,row in enumerate(DATA['worked_examples'])]
LESSON=Lesson(id=LESSON_ID,order=5,title=DATA['title'],
 objective='Match verbal, table, flow and algebraic representations by testing the same input and checking operation order, fixed amounts and square patterns.',
 why_it_matters='A relationship can look different in a bill, a table or an equation. Testing a shared input gives a concrete reason for choosing one rule.',
 intuition='Keep the original words and given rows visible. Identify a fixed amount and any repeated action, substitute the same input into both candidates, and check the evidence before predicting a new output.',
 prerequisites=['g8-functions-relationships-02','g8-functions-relationships-03'],estimated_minutes=95,difficulty='standard',
 access_level=AccessLevel.FREE,status=ContentStatus.TEACHER_REVIEW_REQUIRED,
 blocks=[LessonBlock(type='concept',title='One relationship, several descriptions',content='Follow the spoken operations in order; test both candidate rules at the same input. A table with a zero row identifies a fixed amount. Check every stated pair.'),
 QUESTIONS[0].whiteboard,LessonBlock(type='mistake',title='Repair an incorrect match',content='A shared input can expose swapped rates, incorrect brackets or a boundary mistaken for area.',data={'repairs':[{'question_id':row['id'],'repair':row['repair']} for row in DATA['worked_examples']]}),
 LessonBlock(type='practice',title='Match fresh relationships independently',content='Try the questions before revealing hints or memos.',data={'practice_bank_id':LESSON_ID}),
 LessonBlock(type='summary',title='Confirm the match',content='Substitute a shared input into each representation and check against the original words or table.')],
 whiteboard_questions=QUESTIONS,mastery_threshold=.8,paper=None,source_document=SOURCE,source_sha256=DATA['source_sha256'],release_approved=False,
 assessment_contract={'worked_example_count':15,'practice_count':15,'mastery_question_count':5,'parallel_reassessment_count':3,
 'answer_hidden_before_submission':True,'progression_threshold':.8,'runtime_conversion':'functions_relationships_lesson_5_teacher_review'})
