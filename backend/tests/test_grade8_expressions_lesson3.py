"""Lesson 3: source integrity, real teaching states and private answer gates."""
import hashlib
from pathlib import Path
import pytest

from fastapi.testclient import TestClient
from app.main import app
from app.curriculum.grade8.algebraic_expressions_lesson3 import DATA, LESSON, SOURCE
from app.curriculum.grade8.assessment_expressions_lesson3 import PRACTICE_BANK, MASTERY_BANK, REASSESSMENT_BANK
from app.curriculum.grade8.structure import GRADE_8
from app.curriculum.validation import validate_curriculum
from app.api.v1.practice import _score_assessment
from app.visualization.registry import _grade8_expression_visual


def test_source_and_full_question_bank():
    path=Path(__file__).resolve().parents[2]/'docs/curriculum/grade8/algebraic-expressions'/SOURCE
    assert hashlib.sha256(path.read_bytes()).hexdigest()==DATA['source_sha256']
    assert len(LESSON.whiteboard_questions)==len(PRACTICE_BANK)==15
    assert len(MASTERY_BANK)==5 and sum(q.marks for q in MASTERY_BANK)==20
    assert len(REASSESSMENT_BANK)==3
    assert not [f for f in validate_curriculum([GRADE_8]) if f.lesson_id==LESSON.id]
    assert {q.whiteboard.visualization.template for q in LESSON.whiteboard_questions}=={'factor_array','sign_grid','area_product','power_stack','area_comparison'}
    for item,q in zip(DATA['worked_examples'],LESSON.whiteboard_questions):
        board=q.whiteboard
        assert len(board.steps)==4 and board.steps[-1].after_expression.startswith('Checked:')
        assert board.visualization.parameters.get('model_scene')==item['model'].get('scene')
        assert [s.before_expression for s in board.steps][:3]==item['states'][:3]
        assert all(s.events and s.before_expression!=s.after_expression for s in board.steps)
        assert all(s.narration==next(event.text for event in s.events if event.type=='caption') for s in board.steps)


def test_learner_gets_initial_question_and_one_selected_reveal():
    with TestClient(app) as client:
        grade=client.get('/api/v1/curriculum/grades/grade-8')
        assert grade.status_code==200
        result=client.get('/api/v1/lessons/g8-algebraic-expressions-03')
        assert result.status_code==200, result.text
        questions=result.json()['whiteboard_questions']
        assert len(questions)==15
        assert all(q['solution_gated'] and len(q['whiteboard']['steps'])==1 for q in questions)
        assert all('answer' not in q and 'full_memo' not in q and not q['whiteboard']['steps'][0]['events'] for q in questions)
        reveal=client.post('/api/v1/lessons/g8-algebraic-expressions-03/questions/g8-ex-l03-w15/reveal')
        assert reveal.status_code==200 and len(reveal.json()['whiteboard']['steps'])==4
        assert client.post('/api/v1/lessons/g8-algebraic-expressions-03/questions/g8-ex-l02-w15/reveal').status_code==404
        practice=client.get('/api/v1/practice/g8-algebraic-expressions-03')
        assert practice.status_code==200 and len(practice.json()['questions'])==15
        assert all('accepted_answers' not in q for q in practice.json()['questions'])
        mastery=client.get('/api/v1/practice/g8-algebraic-expressions-03/mastery')
        assert mastery.status_code==200 and len(mastery.json()['questions'])==5
        assert all('answer' not in q for q in mastery.json()['questions'])


def test_all_authored_mastery_answers_grade_correct():
    correct,reviewed,tags=_score_assessment(MASTERY_BANK,{q.id:q.answer for q in MASTERY_BANK})
    assert correct==5 and all(row['correct'] for row in reviewed) and not tags


def test_scene_contract_rejects_invalid_grid_and_mismatched_lanes():
    example=LESSON.whiteboard_questions[0].whiteboard.visualization.parameters
    with pytest.raises(ValueError,match='48 visible cells'):
        _grade8_expression_visual({**example,'model_scene':{'rows':12,'columns':12,'unit':'x'}})
    with pytest.raises(ValueError,match='each given object'):
        _grade8_expression_visual({**example,'model_lanes':['only one lane']})
