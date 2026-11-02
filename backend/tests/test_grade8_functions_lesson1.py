"""Functions Lesson 1 checks source, semantic teaching, and public answer gating."""
import hashlib
from pathlib import Path

from fastapi.testclient import TestClient

from app.api.v1.practice import _score_assessment
from app.curriculum.grade8.assessment_functions_lesson1 import MASTERY_BANK, PRACTICE_BANK, REASSESSMENT_BANK
from app.curriculum.grade8.functions_relationships_lesson1 import DATA, LESSON, SOURCE
from app.curriculum.grade8.structure import GRADE_8
from app.curriculum.validation import validate_curriculum
from app.main import app


def test_authored_source_bank_and_mathematical_timeline():
    doc = Path(__file__).resolve().parents[2] / 'docs/curriculum/grade8/functions-relationships' / SOURCE
    assert hashlib.sha256(doc.read_bytes()).hexdigest() == DATA['source_sha256']
    assert len(LESSON.whiteboard_questions) == len(PRACTICE_BANK) == 15
    assert len(MASTERY_BANK) == 5 and sum(q.marks for q in MASTERY_BANK) == 20
    assert len(REASSESSMENT_BANK) == 3
    assert DATA['worked_examples'][3]['states'][0] == '?×4=28'
    assert LESSON.whiteboard_questions[3].whiteboard.initial_expression == '?×4=28'
    assert all('Ã' not in step.before_expression + step.after_expression
               for question in LESSON.whiteboard_questions for step in question.whiteboard.steps)
    assert len({q.whiteboard.visualization.template for q in LESSON.whiteboard_questions}) == 5
    assert not [f for f in validate_curriculum([GRADE_8]) if f.lesson_id == LESSON.id]
    for item, question in zip(DATA['worked_examples'], LESSON.whiteboard_questions):
        board = question.whiteboard
        assert len(board.steps) == len(item['steps']) + 1
        assert board.visualization.parameters['given_objects'] == item['model']['inputs']
        assert board.visualization.parameters['derived_objects'] == item['model']['outputs']
        assert board.steps[-1].after_expression.startswith('Checked:')
        assert board.steps[-1].state_after['verification_link'] == item['verify']
        assert all(step.before_expression != step.after_expression for step in board.steps)
        assert all(step.narration == next(e.text for e in step.events if e.type == 'caption') for step in board.steps)
        assert item['states'][-1] in question.full_memo[-2]


def test_public_preview_and_practice_keep_answers_private():
    with TestClient(app) as client:
        topic = client.get('/api/v1/curriculum/grades/grade-8/topics/functions-relationships')
        assert topic.status_code == 200
        assert [row['id'] for part in topic.json()['subtopics'] for row in part['lessons']] == [
            LESSON.id, 'g8-functions-relationships-02', 'g8-functions-relationships-03', 'g8-functions-relationships-04','g8-functions-relationships-05','g8-functions-relationships-06']
        assert 'grade8-functions-renderers.js' in client.get('/lesson.html').text
        lesson = client.get('/api/v1/lessons/' + LESSON.id)
        assert lesson.status_code == 200, lesson.text
        examples = lesson.json()['whiteboard_questions']
        assert len(examples) == 15
        assert all(q['solution_gated'] and len(q['whiteboard']['steps']) == 1 for q in examples)
        assert all('answer' not in q and 'full_memo' not in q for q in examples)
        revealed = client.post(f'/api/v1/lessons/{LESSON.id}/questions/g8-fr-l01-w15/reveal')
        assert revealed.status_code == 200 and len(revealed.json()['whiteboard']['steps']) > 2
        practice = client.get('/api/v1/practice/' + LESSON.id)
        assert practice.status_code == 200 and len(practice.json()['questions']) == 15
        assert all('accepted_answers' not in q for q in practice.json()['questions'])
        mastery = client.get('/api/v1/practice/' + LESSON.id + '/mastery')
        assert mastery.status_code == 200 and len(mastery.json()['questions']) == 5
        assert all('answer' not in q for q in mastery.json()['questions'])


def test_mastery_answer_key_scores():
    score, reviewed, tags = _score_assessment(MASTERY_BANK, {q.id: q.answer for q in MASTERY_BANK})
    assert score == 5 and all(row['correct'] for row in reviewed) and not tags
