from math import isclose

import pytest

from app.curriculum.grade12 import GRADE_12
from app.curriculum.grade12.lessons.finance_growth_decay import TITLES
from app.curriculum.grade12.lessons.finance_practice import PRACTICE_BANKS
from app.services.finance_math import (
    compound_value, effective_annual_rate, future_value_annuity, periodic_rate,
    present_value_annuity, reducing_balance, simple_value, straight_line,
)
from app.visualization.registry import validate_visualization
from app.whiteboard.validation import validate_whiteboard


def test_finance_topic_registration_and_schedule():
    topic=GRADE_12.topics[2]
    assert topic.id=="finance-growth-decay" and topic.product_order==3
    assert topic.title=="Finance, Growth and Decay" and topic.paper=="Paper 1"
    lessons=topic.subtopics[0].lessons
    assert len(lessons)==16 and [lesson.id for lesson in lessons]==[f"g12-finance-{i:02}" for i in range(1,17)]
    assert [lesson.title for lesson in lessons]==list(TITLES)
    assert all(lesson.blocks and len(lesson.whiteboard_questions)==3 for lesson in lessons[:3])
    assert all(lesson.status.value=="coming_soon" and not lesson.blocks for lesson in lessons[3:])
    assert all("Awaiting approved lesson-pack conversion" not in lesson.model_dump_json() for lesson in lessons)


def test_finance_whiteboards_are_valid_and_deterministic():
    for lesson in GRADE_12.topics[2].subtopics[0].lessons[:3]:
        for question in lesson.whiteboard_questions:
            board=question.whiteboard;validate_visualization(board);validate_whiteboard(board)
            assert board.visualization.type=="finance" and board.visualization.template=="cashflow_timeline"
            assert board.steps[0].before_expression==board.initial_expression
            assert all(a.after_expression==b.before_expression for a,b in zip(board.steps,board.steps[1:]))
            assert board.steps[-1].events[-1].type=="verify_financial_sense"


def test_finance_calculations_retain_precision_and_match_pack():
    assert simple_value(8000,.09,2.5)==9800
    assert isclose(compound_value(8000,.09,2.5),9923.302530589302)
    assert isclose(compound_value(12500,periodic_rate(.084,12),36),16068.337790228881)
    assert isclose(reducing_balance(480000,.18,5),177955.124736)
    assert isclose(straight_line(75000,.12,6),21000)
    assert isclose(effective_annual_rate(.08,2),.0816)
    assert isclose(future_value_annuity(1000,.01,12),12682.503013196976)
    assert isclose(present_value_annuity(2000,.01,24),42486.774515255725)
    with pytest.raises(ValueError): straight_line(100,.6,2)


def test_finance_practice_is_backend_authoritative_and_unique():
    assert set(PRACTICE_BANKS)=={"g12-finance-01","g12-finance-02","g12-finance-03"}
    questions=[q for bank in PRACTICE_BANKS.values() for q in bank]
    assert len(questions)==12 and len({q.id for q in questions})==12
    assert all(q.source.endswith("Approved_Lesson_Pack.docx") and len(q.hints)==3 for q in questions)
    assert all(len(q.worked_solution)>=5 and q.verification for q in questions)
