import json
from pathlib import Path

import pytest

from app.curriculum.repository import curriculum_repository
from app.curriculum.schemas import VisualizationInstruction
from app.visualization.registry import template_manifest, validate_visualization
from app.whiteboard.validation import validate_whiteboard


def lesson_one():
    return curriculum_repository.get_lesson("g12-sequences-series-01")[2]


def test_all_active_visual_questions_use_the_registered_sequence_template():
    lesson = lesson_one()
    for question in lesson.whiteboard_questions:
        board = question.whiteboard
        assert board.representation == "visual"
        assert board.visualization.type == "sequences"
        assert board.visualization.template == "sequence_timeline"
        validate_whiteboard(board)


def test_sequence_visualization_rejects_unknown_and_unsafe_parameters():
    board = lesson_one().whiteboard_questions[0].whiteboard
    unknown = board.model_copy(update={"visualization":VisualizationInstruction(type="sequences",template="unknown",parameters={})})
    with pytest.raises(ValueError,match="TEMPLATE_UNKNOWN"):
        validate_visualization(unknown)
    unsafe = board.model_copy(update={"visualization":VisualizationInstruction(type="sequences",template="sequence_timeline",parameters={"terms":[1,2,3],"positions":[1,2,3],"mode":"<script>"})})
    with pytest.raises(ValueError,match="Unsafe"):
        validate_visualization(unsafe)


def test_backend_and_frontend_template_manifests_remain_aligned():
    manifest = Path(__file__).parents[2] / "frontend/js/visualization/template-manifest.json"
    assert template_manifest() == set(json.loads(manifest.read_text(encoding="utf-8")))


def statistics_box_plot_questions():
    topic = next(item for item in curriculum_repository.get_grade("grade-12").topics if item.id == "statistics-regression")
    return topic.subtopics[0].lessons[5].whiteboard_questions


def test_box_plot_contract_validates_values_and_question_template():
    board = statistics_box_plot_questions()[0].whiteboard
    assert board.visualization.template == "box_plot"
    assert board.visualization.parameters == {
        "minimum": 8.0, "q1": 13.0, "median": 17.0, "q3": 22.0,
        "maximum": 28.0, "title": "Five-number summary",
        "show_labels": True, "show_iqr": True, "show_range": True,
    }
    validate_whiteboard(board)
    reversed_values = board.model_copy(update={"visualization": VisualizationInstruction(
        type="statistics", template="box_plot",
        parameters={**board.visualization.parameters, "q1": 19, "median": 17},
    )})
    with pytest.raises(ValueError, match="minimum <= q1 <= median <= q3 <= maximum"):
        validate_visualization(reversed_values)
    missing = board.model_copy(update={"visualization": VisualizationInstruction(
        type="statistics", template="box_plot", parameters={"minimum": 8},
    )})
    with pytest.raises(ValueError, match="Missing visualization parameters"):
        validate_visualization(missing)
    generic = board.model_copy(update={"visualization": VisualizationInstruction(
        type="statistics", template="data_plot", parameters={"values": [8, 13, 17, 22, 28]},
    )})
    with pytest.raises(ValueError, match="BOX_PLOT_QUESTION_REQUIRES"):
        validate_visualization(generic)


def test_box_plot_visual_data_is_fresh_progressive_and_mathematically_consistent():
    questions = statistics_box_plot_questions()
    parameter_ids = [id(item.whiteboard.visualization.parameters) for item in questions]
    summaries = [
        tuple(item.whiteboard.visualization.parameters[key] for key in ("minimum", "q1", "median", "q3", "maximum"))
        for item in questions
    ]
    assert len(set(parameter_ids)) == len(questions)
    assert len(set(summaries)) == len(questions)
    for question, summary in zip(questions, summaries):
        minimum, q1, median, q3, maximum = summary
        assert q3 - q1 >= 0
        assert maximum - minimum > 0
        board = question.whiteboard
        assert len(board.steps) == 14
        assert board.steps[0].visualization_state.objects == ["boxplot-axis"]
        assert set(board.steps[-1].visualization_state.objects) == {item.id for item in board.semantic_objects}
        targets = {target for step in board.steps for event in step.events for target in event.targets}
        assert targets <= {item.id for item in board.semantic_objects}
        assert all(
            [event.text for event in step.events if event.type == "caption"]
            == [event.text for event in step.events if event.type == "narration"]
            for step in board.steps
        )
