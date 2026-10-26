"""Source, answer-gating and mathematical state checks for expressions Lesson 2."""
import hashlib
from pathlib import Path

from fastapi.testclient import TestClient
from app.main import app
from app.curriculum.grade8.algebraic_expressions_lesson2 import DATA, LESSON, SOURCE
from app.curriculum.grade8.assessment_expressions_lesson2 import PRACTICE_BANK, MASTERY_BANK, REASSESSMENT_BANK
from app.curriculum.grade8.structure import GRADE_8
from app.curriculum.validation import validate_curriculum
from app.api.v1.practice import _score_assessment


def test_full_bank_and_source_integrity():
    path=Path(__file__).resolve().parents[2]/'docs/curriculum/grade8/algebraic-expressions'/SOURCE
    assert hashlib.sha256(path.read_bytes()).hexdigest()==DATA['source_sha256']
    assert len(LESSON.whiteboard_questions)==len(PRACTICE_BANK)==15
    assert len(MASTERY_BANK)==5 and sum(q.marks for q in MASTERY_BANK)==20
    assert len(REASSESSMENT_BANK)==3
    assert not [failure for failure in validate_curriculum([GRADE_8]) if failure.lesson_id==LESSON.id]
    assert {q.whiteboard.visualization.template for q in LESSON.whiteboard_questions} >= {'like_term_sort','bracket_negation','grouped_polynomials','rectangle'}
    for item, question in zip(DATA['worked_examples'], LESSON.whiteboard_questions):
        board=question.whiteboard
        assert board.visualization.parameters.get('model_lanes')==item['model']['lanes']
        assert len(board.steps)==len(item['steps'])+1
        assert board.steps[-1].after_expression.startswith('Checked:')
        assert board.steps[-1].state_after['verification_complete']
        assert all(step.before_expression!=step.after_expression and step.events for step in board.steps)


def test_public_question_first_and_private_assessment_keys():
    with TestClient(app) as client:
        result=client.get('/api/v1/lessons/g8-algebraic-expressions-02')
        assert result.status_code==200, result.text
        questions=result.json()['whiteboard_questions']
        assert len(questions)==15
        assert all(q['solution_gated'] and len(q['whiteboard']['steps'])==1 for q in questions)
        assert all('answer' not in q and 'full_memo' not in q and not q['whiteboard']['steps'][0]['events'] for q in questions)
        reveal=client.post('/api/v1/lessons/g8-algebraic-expressions-02/questions/g8-ex-l02-w15/reveal')
        assert reveal.status_code==200 and len(reveal.json()['whiteboard']['steps'])==4
        assert client.post('/api/v1/lessons/g8-algebraic-expressions-02/questions/g8-ex-l01-w01/reveal').status_code==404
        practice=client.get('/api/v1/practice/g8-algebraic-expressions-02')
        assert practice.status_code==200 and len(practice.json()['questions'])==15
        assert all('accepted_answers' not in row for row in practice.json()['questions'])
        mastery=client.get('/api/v1/practice/g8-algebraic-expressions-02/mastery')
        assert mastery.status_code==200 and len(mastery.json()['questions'])==5
        assert all('answer' not in row for row in mastery.json()['questions'])


def test_assessment_scores_every_authored_answer():
    answers={item.id:item.answer for item in MASTERY_BANK}
    correct, reviewed, tags=_score_assessment(MASTERY_BANK,answers)
    assert correct==5 and not tags and all(row['correct'] for row in reviewed)
