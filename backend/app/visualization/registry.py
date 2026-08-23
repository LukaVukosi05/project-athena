"""Server-side allow-list for structured visualization instructions."""
from app.curriculum.schemas import WhiteboardBlock

TEMPLATES = {
    "geometry": {"central_angle_theorem"},
    "coordinate_geometry": set(), "function_graph": {"cartesian_function"},
    "trigonometry": set(), "statistics": set(), "probability": set(),
    "calculus": {"secant_to_tangent"},
}

def validate_visualization(board: WhiteboardBlock) -> None:
    instruction = board.visualization
    if instruction is None:
        return
    if instruction.template not in TEMPLATES[instruction.type]:
        raise ValueError(f"Unsupported {instruction.type} visualization template: {instruction.template}")
    if instruction.type == "geometry" and instruction.template == "central_angle_theorem":
        angle = instruction.parameters.get("central_angle")
        if not isinstance(angle, (int, float)) or isinstance(angle, bool) or not 0 < angle < 180:
            raise ValueError("central_angle must be between 0 and 180 degrees")
        if len(board.steps) != 6 or any(step.visualization_state is None for step in board.steps):
            raise ValueError("central_angle_theorem requires six explicit visual states")
