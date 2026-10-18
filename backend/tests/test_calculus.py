from pathlib import Path

import pytest

from app.curriculum.grade12 import GRADE_12
from app.curriculum.repository import curriculum_repository
from app.curriculum.schemas import MathematicalOperation, StepExplanation, TeachingStep, TimelineEvent
from app.curriculum.grade12.lessons.calculus_practice import PRACTICE_BANKS
from app.whiteboard.validation import validate_whiteboard

TITLES = [
 "Rate of change","Average gradient","Secant lines","Secant to tangent","Intuitive limits","First principles",
 "Derivative notation","First-principles differentiation","Power rule","Constant rule","Sum and difference rule","Tangents",
 "Tangent equations","Stationary points","Local extrema","Second derivative","Concavity","Points of inflection",
 "Cubic sketching","Optimisation","Rate applications","Motion","Exam questions","Paper 1 differential calculus mastery assessment",
]

def topic(): return GRADE_12.topics[3]

def test_topic_four_is_unique_ordered_and_staged():
    assert [t.id for t in GRADE_12.topics].count("differential-calculus") == 1
    assert topic().product_order == 4 and topic().paper == "Paper 1" and topic().term == 2
    lessons=topic().subtopics[0].lessons
    assert len(lessons)==24
    assert [l.id for l in lessons]==[f"g12-calculus-{n:02}" for n in range(1,25)]
    assert [l.title for l in lessons]==TITLES
    assert all(l.blocks and len(l.whiteboard_questions)==3 for l in lessons[:6])
    assert all(l.status.value=="coming_soon" and not l.blocks for l in lessons[6:])

def test_legacy_ids_resolve_without_duplicate_lessons():
    assert curriculum_repository.get_lesson("g12-calculus-average-rate")[2].id=="g12-calculus-01"
    assert curriculum_repository.get_lesson("g12-calculus-secant-to-tangent")[2].id=="g12-calculus-04"
    assert all("average-rate" not in l.id and "secant-to-tangent" not in l.id for l in topic().subtopics[0].lessons)

def test_foundation_formula_contract_and_whiteboards_are_valid():
    for lesson in topic().subtopics[0].lessons[:6]:
      for question in lesson.whiteboard_questions:
        board=question.whiteboard; validate_whiteboard(board)
        formula=board.formula_understanding
        assert formula and all((formula.meaning,formula.origin,formula.formula,formula.symbol_anatomy,formula.why_it_works,formula.validity_conditions,formula.selection_reason,formula.wrong_use_cases,formula.visual_model,formula.verification))
        assert board.graph_spec and board.visualization.template=="secant_to_tangent"

def test_first_principles_never_divides_by_zero_and_factors_before_cancel():
    board=topic().subtopics[0].lessons[5].whiteboard_questions[0].whiteboard
    text=" ".join([board.initial_expression,*[s.after_expression for s in board.steps]])
    assert "/0" not in text and "h≠0" in text
    operations=[s.operation.type for s in board.steps]
    assert operations.index("factor_common") < operations.index("cancel") < operations.index("calculus_limit")
    cancel=next(s for s in board.steps if s.operation.type=="cancel")
    assert [event.type for event in cancel.events].index("factor_common") < [event.type for event in cancel.events].index("cancel")

def test_schema_rejects_cancellation_without_prior_factor_or_inverse_operation():
    with pytest.raises(ValueError,match="Cancellation requires"):
      TeachingStep(step_number=0,title="invalid",before_expression="h+h",operation=MathematicalOperation(type="cancel"),after_expression="2",explanation=StepExplanation(what="x",why="x",purpose="x",remember="x"),animation_template="calculus_timeline_reasoning",screen_reader_description="invalid",duration_ms=500,events=[TimelineEvent(at_ms=100,type="cancel",targets=["h"])])

def test_calculus_practice_is_separate_and_uses_eighty_percent_mastery():
    assert set(PRACTICE_BANKS)=={f"g12-calculus-{i:02}" for i in range(1,7)}
    assert all(len(bank)==4 for bank in PRACTICE_BANKS.values())
    assert len({q.id for bank in PRACTICE_BANKS.values() for q in bank})==24
    assert all(q.source.endswith("Differential_Calculus_Approved_Lesson_Pack.docx") for bank in PRACTICE_BANKS.values() for q in bank)
    assert all(l.mastery_threshold==.8 for l in topic().subtopics[0].lessons)

def test_pack_was_completely_extracted_to_reviewable_files():
    root=Path(__file__).parents[2]/"docs/curriculum/grade12/content/04-differential-calculus"
    assert (root/"topic.yaml").exists() and (root/"assessment.md").exists()
    lessons=list(root.glob("lesson-*.md")); assert len(lessons)==24
    assert all(path.stat().st_size>4000 for path in lessons)
    evidence=(root/"paper-evidence.md").read_text(encoding="utf-8")
    assert "| 8.1" in evidence and "Official [DBE 2024 Mathematics P1 memo]" in evidence
