import pytest
from pydantic import ValidationError

from app.curriculum.repository import curriculum_repository
from app.curriculum.schemas import VisualizationInstruction
from app.visualization.registry import validate_visualization
from app.whiteboard.validation import validate_whiteboard


def geometry_board():
    _, _, lesson = curriculum_repository.get_lesson("g12-p2-euclidean-geometry-foundation")
    return lesson.whiteboard_questions[0].whiteboard


def test_central_angle_visualization_has_six_explicit_states():
    board = geometry_board()
    assert board.visualization.type == "geometry"
    assert board.visualization.template == "central_angle_theorem"
    assert board.visualization.parameters["central_angle"] == 100
    assert len(board.steps) == 6
    assert board.steps[0].visualization_state.objects == ["circle", "points", "radii", "chords"]
    assert "arc_ab" in board.steps[2].visualization_state.highlights
    assert board.steps[3].after_expression == "100° = 2x"
    assert board.steps[-1].after_expression == "∠ACB = 50°"
    validate_whiteboard(board)


def test_visualization_schema_and_registry_reject_unsafe_templates_and_angles():
    board = geometry_board()
    invalid_template = board.model_copy(update={"visualization": VisualizationInstruction(type="geometry", template="arbitrary_javascript", parameters={})})
    with pytest.raises(ValueError):
        validate_visualization(invalid_template)
    invalid_angle = board.model_copy(update={"visualization": VisualizationInstruction(type="geometry", template="central_angle_theorem", parameters={"central_angle": 220})})
    with pytest.raises(ValueError):
        validate_visualization(invalid_angle)
    with pytest.raises(ValidationError):
        VisualizationInstruction(type="geometry", template="bad-template!", parameters={})


def test_geometry_question_set_keeps_different_examples_after_visual_core():
    _, _, lesson = curriculum_repository.get_lesson("g12-p2-euclidean-geometry-foundation")
    assert len(lesson.whiteboard_questions) == 12
    assert lesson.whiteboard_questions[0].whiteboard.problem != lesson.whiteboard_questions[1].whiteboard.problem
