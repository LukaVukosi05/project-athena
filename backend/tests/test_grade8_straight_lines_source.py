"""Check the mathematical facts before geometry lessons enter the runtime catalogue."""
import pytest

from app.curriculum.grade8.straight_lines_cases import LESSON_1, LESSON_2, _expression, validate_all


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
