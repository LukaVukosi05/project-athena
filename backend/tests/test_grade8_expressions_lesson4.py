"""Authoring integrity, answer privacy and API reachability for Lesson 4."""
import hashlib
from pathlib import Path

from fastapi.testclient import TestClient
from app.main import app
from app.curriculum.grade8.algebraic_expressions_lesson4 import DATA, LESSON, SOURCE
from app.curriculum.grade8.assessment_expressions_lesson4 import PRACTICE_BANK, MASTERY_BANK, REASSESSMENT_BANK
from app.curriculum.grade8.structure import GRADE_8
from app.curriculum.validation import validate_curriculum
from app.api.v1.practice import _score_assessment


def test_source_and_timeline_contract():
    path=Path(__file__).resolve().parents[2]/'docs/curriculum/grade8/algebraic-expressions'/SOURCE
    assert hashlib.sha256(path.read_bytes()).hexdigest()==DATA['source_sha256']
    assert len(LESSON.whiteboard_questions)==len(PRACTICE_BANK)==15
    assert len(MASTERY_BANK)==5 and sum(q.marks for q in MASTERY_BANK)==20
    assert len(REASSESSMENT_BANK)==3
    assert not [f for f in validate_curriculum([GRADE_8]) if f.lesson_id==LESSON.id]
    assert {q.whiteboard.visualization.template for q in LESSON.whiteboard_questions} == {
        'distribute_strip','signed_distribute','trinomial_branches','area_distribute','compare_paths'}
    for item, question in zip(DATA['worked_examples'],LESSON.whiteboard_questions):
        board=question.whiteboard
        assert len(board.steps)==len(item['steps'])+1
        assert board.steps[-1].after_expression.startswith('Checked:')
        assert board.visualization.parameters['model_tokens']==item['model']['tokens']
        assert all(step.events and step.before_expression!=step.after_expression for step in board.steps)
        assert all(step.narration==next(event.text for event in step.events if event.type=='caption') for step in board.steps)
        assert len(question.full_memo)==len(item['steps'])+1
        assert item['states'][-1] in question.full_memo[-2]


def test_public_preview_reveal_and_private_assessment():
    with TestClient(app) as client:
        page=client.get('/lesson.html')
        assert 'grade8-distribution-renderers.js?v=g8-ex-l04-v1' in page.text
        assert 'math-whiteboard-v18' in page.text
        lesson=client.get('/api/v1/lessons/g8-algebraic-expressions-04')
        assert lesson.status_code==200,lesson.text
        questions=lesson.json()['whiteboard_questions']
        assert len(questions)==15
        assert all(q['solution_gated'] and len(q['whiteboard']['steps'])==1 for q in questions)
        assert all('answer' not in q and 'full_memo' not in q and not q['whiteboard']['steps'][0]['events'] for q in questions)
        reveal=client.post('/api/v1/lessons/g8-algebraic-expressions-04/questions/g8-ex-l04-w15/reveal')
        assert reveal.status_code==200 and len(reveal.json()['whiteboard']['steps'])==4
        practice=client.get('/api/v1/practice/g8-algebraic-expressions-04')
        assert practice.status_code==200 and len(practice.json()['questions'])==15
        assert all('accepted_answers' not in q for q in practice.json()['questions'])
        mastery=client.get('/api/v1/practice/g8-algebraic-expressions-04/mastery')
        assert mastery.status_code==200 and len(mastery.json()['questions'])==5
        assert all('answer' not in q for q in mastery.json()['questions'])


def test_authored_mastery_answers_score():
    correct, reviewed, tags=_score_assessment(MASTERY_BANK,{q.id:q.answer for q in MASTERY_BANK})
    assert correct==5 and all(row['correct'] for row in reviewed) and not tags
