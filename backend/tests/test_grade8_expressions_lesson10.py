"""Grade 8 expressions diagnosis: authored source, privacy and transfer."""
import hashlib
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from app.api.v1.practice import _score_assessment
from app.curriculum.grade8.algebraic_expressions_lesson10 import DATA, LESSON, SOURCE
from app.curriculum.grade8.assessment_expressions_lesson10 import PRACTICE_BANK, MASTERY_BANK, REASSESSMENT_BANK
from app.curriculum.grade8.structure import GRADE_8
from app.curriculum.validation import validate_curriculum


def test_source_and_every_question_specific_teaching_state():
    doc=Path(__file__).resolve().parents[2]/'docs/curriculum/grade8/algebraic-expressions'/SOURCE
    assert hashlib.sha256(doc.read_bytes()).hexdigest()==DATA['source_sha256']
    assert len(LESSON.whiteboard_questions)==len(PRACTICE_BANK)==15
    assert len(MASTERY_BANK)==5 and sum(q.marks for q in MASTERY_BANK)==20
    assert len(REASSESSMENT_BANK)==3
    assert len({q.whiteboard.visualization.template for q in LESSON.whiteboard_questions})==15
    assert not [f for f in validate_curriculum([GRADE_8]) if f.lesson_id==LESSON.id]
    for item,question in zip(DATA['worked_examples'],LESSON.whiteboard_questions):
        board=question.whiteboard
        assert board.visualization.parameters['model_tokens']==item['model']['tokens']
        assert len(board.steps)==len(item['steps'])+1
        assert question.answer in item['answer']
        assert board.steps[-1].after_expression.startswith('Checked:')
        assert all(step.before_expression!=step.after_expression and step.events for step in board.steps)
        assert all(step.narration==next(e.text for e in step.events if e.type=='caption') for step in board.steps)
        assert item['states'][-1] in question.full_memo[-2]
        assert item['verify'] in question.full_memo[-1]
    assert DATA['worked_examples'][7]['answer'].startswith('|t|')
    assert DATA['worked_examples'][10]['answer'].endswith('a=0.')
    assert '5z−9' in DATA['worked_examples'][14]['answer']


def test_lesson10_public_preview_reveal_practice_and_assessment_privacy():
    with TestClient(app) as client:
        topic=client.get('/api/v1/curriculum/grades/grade-8/topics/algebraic-expressions')
        assert topic.status_code==200
        lessons=[lesson for part in topic.json()['subtopics'] for lesson in part['lessons']]
        assert len(lessons)==10 and lessons[-1]['id']==LESSON.id
        assert 'grade8-diagnostic-expressions-renderers.js?v=g8-ex-l10-v1' in client.get('/lesson.html').text
        response=client.get('/api/v1/lessons/'+LESSON.id)
        assert response.status_code==200,response.text
        examples=response.json()['whiteboard_questions']
        assert len(examples)==15
        assert all(q['solution_gated'] and q['diagnostic_submission_required'] and len(q['whiteboard']['steps'])==1 for q in examples)
        assert all('answer' not in q and 'full_memo' not in q for q in examples)
        blocked=client.post(f'/api/v1/lessons/{LESSON.id}/questions/g8-ex-l10-w15/reveal')
        assert blocked.status_code==409
        revealed=client.post(f'/api/v1/lessons/{LESSON.id}/questions/g8-ex-l10-w15/diagnose',json={'first_error_and_repair':'The first error is 2 times negative four; replace it with negative eight.'})
        assert revealed.status_code==200 and len(revealed.json()['whiteboard']['steps'])==5
        practice=client.get('/api/v1/practice/'+LESSON.id)
        assert practice.status_code==200 and len(practice.json()['questions'])==15
        assert all('accepted_answers' not in q for q in practice.json()['questions'])
        mastery=client.get('/api/v1/practice/'+LESSON.id+'/mastery')
        assert mastery.status_code==200 and len(mastery.json()['questions'])==5
        assert all('answer' not in q for q in mastery.json()['questions'])


def test_mastery_bank_correct_answers_score():
    score,reviewed,tags=_score_assessment(MASTERY_BANK,{q.id:q.answer for q in MASTERY_BANK})
    assert score==5 and all(item['correct'] for item in reviewed) and not tags
