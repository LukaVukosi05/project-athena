"""Whiteboard validation entry point independent from API and content."""

from app.curriculum.schemas import WhiteboardBlock
from app.whiteboard.registry import registry
from app.visualization.registry import validate_visualization


def validate_whiteboard(plan: WhiteboardBlock) -> None:
    registry.validate(plan)
    validate_visualization(plan)
