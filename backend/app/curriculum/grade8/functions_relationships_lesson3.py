"""Original Grade 8 table-rule lesson; teacher review remains required."""
import json
from pathlib import Path

from app.curriculum.grade8.functions_relationships_lesson1 import question
from app.curriculum.schemas import AccessLevel,ContentStatus,Lesson,LessonBlock

DATA=json.loads((Path(__file__).with_name('generated')/'functions_relationships_03.json').read_text(encoding='utf-8'))
LESSON_ID='g8-functions-relationships-03'
SOURCE=DATA['source_document']
QUESTIONS=[question(item,n) for n,item in enumerate(DATA['worked_examples'])]
LESSON=Lesson(id=LESSON_ID,order=3,title='Finding and testing rules from tables',
    objective='Find candidate rules from aligned input-output tables, compare changes per unit input, check zero and signed rows, identify simple square patterns and reverse a rule for missing inputs.',
    why_it_matters='Tables often hide the rule. The learner must read both input and output changes to model the situation and avoid guessing from the output sequence alone.',
    intuition='Align each input with its output. Mark both input and output step widths, divide output change by input change for a proposed linear rate, then read the zero row. For changing gaps test a square-based candidate. Verify all given rows without claiming a finite table proves a unique formula.',
    prerequisites=['g8-functions-relationships-01','g8-functions-relationships-02','signed arithmetic','square numbers'],
    estimated_minutes=95,difficulty='standard',access_level=AccessLevel.FREE,
    status=ContentStatus.TEACHER_REVIEW_REQUIRED,
    blocks=[LessonBlock(type='concept',title='Read both table columns',
        content='Calculate output change per one input step, read or reconstruct the input-zero row, and test the rule on all displayed pairs. If gaps change, consider another pattern. A short table alone does not prove a unique rule.'),
        QUESTIONS[0].whiteboard,
        LessonBlock(type='mistake',title='Diagnose the first unsupported rule',
            content='Look for an ignored input gap, mistaken intercept, signed substitution, fixed fee, or a linear claim contradicted by a row.',
            data={'repairs':[{'question_id':row['id'],'repair':row['repair']} for row in DATA['worked_examples']]}),
        LessonBlock(type='practice',title='Find and check rules independently',
            content='Solve each new table and situation before using a hint or solution.',data={'practice_bank_id':LESSON_ID}),
        LessonBlock(type='summary',title='Check the table again',
            content='Name the rule family when needed, test every original row, and distinguish a fitting candidate from a uniquely proven rule.')],
    whiteboard_questions=QUESTIONS,mastery_threshold=.8,paper=None,
    source_document=SOURCE,source_sha256=DATA['source_sha256'],release_approved=False,
    assessment_contract={'worked_example_count':15,'practice_count':15,'mastery_question_count':5,
        'parallel_reassessment_count':3,'answer_hidden_before_submission':True,
        'progression_threshold':.8,'runtime_conversion':'functions_relationships_lesson_3'})
