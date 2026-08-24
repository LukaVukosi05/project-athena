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
