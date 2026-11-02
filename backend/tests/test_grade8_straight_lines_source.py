"""Check the mathematical facts before geometry lessons enter the runtime catalogue."""
import pytest

from app.curriculum.grade8.straight_lines_cases import LESSON_1, LESSON_2, _expression, validate_all
from app.curriculum.grade8.straight_lines_runtime import LESSON_1 as RUNTIME_1, LESSON_2 as RUNTIME_2
from app.visualization.registry import validate_visualization
from app.whiteboard.registry import registry
from app.curriculum.grade8 import assessment_straight_lines as assessment
from fastapi.testclient import TestClient
from app.main import app


def test_thirty_distinct_diagram_cases_have_checked_angle_answers():
    assert validate_all()
    assert len(LESSON_1) == len(LESSON_2) == 15
    assert {x.diagram for x in LESSON_1} == {'intersection', 'perpendicular'}
    assert {x.relationship for x in LESSON_2} == {'corresponding', 'alternate', 'cointerior'}
    assert len({x.problem for x in LESSON_1 + LESSON_2}) == 30
    assert all('0x' not in x.problem for x in LESSON_1 + LESSON_2)


def test_parallel_equal_and_supplementary_relationships_do_not_conflate():
    assert LESSON_2[0].answer == 48
    assert LESSON_2[2].answer == 68
    assert LESSON_2[6].answer == 29
    assert LESSON_2[-1].answer == 20


def test_invalid_case_cannot_enter_source_bank():
    with pytest.raises(ValueError):
        _expression(16, 'transversal', 'cointerior', 3, 17, 2, 10)


def test_native_visual_contract_and_all_timelines_are_valid():
    for lesson in (RUNTIME_1, RUNTIME_2):
        assert len(lesson.whiteboard_questions) == 15
        assert not lesson.release_approved
        for question in lesson.whiteboard_questions:
            board = question.whiteboard
            validate_visualization(board)
            registry.validate(board)
            assert 'answer' not in board.visualization.parameters['scene_json']
            assert board.steps[-1].state_after['verification_complete']


def test_unseen_banks_and_public_lesson_gate():
    for number in (1,2):
        practice, mastery, reassess, repairs, rules = assessment.banks(number)
        assert (len(practice),len(mastery),len(reassess)) == (15,5,3)
        assert repairs and rules
        assert {q.prompt for q in practice}.isdisjoint({q.problem for q in (LESSON_1,LESSON_2)[number-1]})
        lesson_id=f'g8-straight-lines-{number:02}'
        with TestClient(app) as client:
            response=client.get(f'/api/v1/lessons/{lesson_id}')
            bank=client.get(f'/api/v1/practice/{lesson_id}')
            if response.status_code == 200:
                payload=response.json()
                assert len(payload['whiteboard_questions']) == 15
                assert all('answer' not in q and 'full_memo' not in q for q in payload['whiteboard_questions'])
                assert all(len(q['whiteboard']['steps']) == 1 for q in payload['whiteboard_questions'])
                revealed=client.post(f'/api/v1/lessons/{lesson_id}/questions/{(LESSON_1,LESSON_2)[number-1][0].id}/reveal')
                assert revealed.status_code in (200,401)
            assert bank.status_code == 200
            assert len(bank.json()['questions']) == 15
