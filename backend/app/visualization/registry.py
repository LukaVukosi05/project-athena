"""Allow-listed, parameter-validated mathematical visualization catalogue."""
from dataclasses import dataclass
from collections.abc import Callable
import re

from app.curriculum.schemas import WhiteboardBlock

ParameterValidator = Callable[[dict], None]

@dataclass(frozen=True)
class TemplateDefinition:
    required: frozenset[str]
    optional: frozenset[str]
    validate: ParameterValidator
    requires_step_states: bool = False

def _reject_unsafe(parameters: dict) -> None:
    for value in parameters.values():
        values = value if isinstance(value, list) else [value]
        if len(values) > 100:
            raise ValueError("Visualization parameter collection exceeds 100 values")
        for item in values:
            if isinstance(item, str) and (len(item) > 160 or re.search(r"<|>|javascript:|\beval\b|\bfunction\s*\(", item, re.I)):
                raise ValueError("Unsafe visualization parameter")

def _bounded_number(name: str, minimum: float, maximum: float) -> ParameterValidator:
    def validate(parameters: dict) -> None:
        value = parameters[name]
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not minimum < value < maximum:
            raise ValueError(f"{name} must be between {minimum} and {maximum}")
    return validate

def _numeric_lists(*names: str) -> ParameterValidator:
    def validate(parameters: dict) -> None:
        lengths = set()
        for name in names:
            values = parameters[name]
            if not isinstance(values, list) or not 2 <= len(values) <= 100 or any(not isinstance(v, (int, float)) or isinstance(v, bool) for v in values):
                raise ValueError(f"{name} must contain 2 to 100 numbers")
            lengths.add(len(values))
        if len(lengths) > 1:
            raise ValueError("Related visualization parameter collections must have equal lengths")
    return validate

def _noop(parameters: dict) -> None: pass

def _oblique_triangle(parameters: dict) -> None:
    _bounded_number("included_angle", 0, 180)(parameters)
    for name in ("side_a", "side_b"):
        value = parameters[name]
        if not isinstance(value, (int, float)) or isinstance(value, bool) or value <= 0 or value > 10000:
            raise ValueError(f"{name} must be a positive bounded number")

def _sequence_timeline(parameters: dict) -> None:
    terms = parameters["terms"]
    positions = parameters["positions"]
    if not isinstance(terms, list) or not 3 <= len(terms) <= 12:
        raise ValueError("terms must contain 3 to 12 values")
    if not isinstance(positions, list) or len(positions) != len(terms):
        raise ValueError("positions must align with terms")
    if any(not isinstance(value, (int, float)) or isinstance(value, bool) for value in [*terms, *positions]):
        raise ValueError("Sequence terms and positions must be numeric")

CATALOGUE: dict[tuple[str, str], TemplateDefinition] = {
    ("geometry", "central_angle_theorem"): TemplateDefinition(frozenset({"central_angle"}), frozenset({"target"}), _bounded_number("central_angle", 0, 180), True),
    ("geometry", "cyclic_quadrilateral"): TemplateDefinition(frozenset({"known_angle"}), frozenset(), _bounded_number("known_angle", 0, 180), True),
    ("geometry", "tangent_radius"): TemplateDefinition(frozenset(), frozenset({"radius_label","tangent_label"}), _noop, True),
    ("geometry", "same_segment"): TemplateDefinition(frozenset(), frozenset({"angle"}), _noop, True),
    ("geometry", "angle_in_semicircle"): TemplateDefinition(frozenset(), frozenset(), _noop, True),
    ("geometry", "equal_tangents"): TemplateDefinition(frozenset({"length"}), frozenset(), _bounded_number("length", 0, 10000), True),
    ("geometry", "similar_triangles"): TemplateDefinition(frozenset(), frozenset({"scale_factor"}), _noop, True),
    ("coordinate_geometry", "coordinate_plane"): TemplateDefinition(frozenset({"x_values","y_values"}), frozenset({"title","show_line","show_circle"}), _numeric_lists("x_values","y_values"), True),
    ("function_graph", "cartesian_function"): TemplateDefinition(frozenset({"graph_spec_id"}), frozenset(), _noop),
    ("calculus", "secant_to_tangent"): TemplateDefinition(frozenset({"graph_spec_id"}), frozenset(), _noop),
    ("trigonometry", "right_triangle"): TemplateDefinition(frozenset({"opposite","adjacent","hypotenuse"}), frozenset({"angle"}), _noop, True),
    ("trigonometry", "oblique_triangle"): TemplateDefinition(frozenset({"side_a","side_b","included_angle"}), frozenset({"target_side"}), _oblique_triangle, True),
    ("trigonometry", "unit_circle"): TemplateDefinition(frozenset({"angle"}), frozenset(), _bounded_number("angle", -721, 721), True),
    ("statistics", "data_plot"): TemplateDefinition(frozenset({"values"}), frozenset({"kind","title"}), _numeric_lists("values"), True),
    ("sequences", "sequence_timeline"): TemplateDefinition(frozenset({"terms","positions","mode"}), frozenset({"title","differences","second_differences","ratios","next_term","next_change"}), _sequence_timeline, True),
}
TEMPLATES = {kind: {template for candidate, template in CATALOGUE if candidate == kind} for kind in {kind for kind, _ in CATALOGUE}}

def template_manifest() -> set[str]:
    return {f"{kind}:{template}" for kind, template in CATALOGUE}

def validate_visualization(board: WhiteboardBlock) -> None:
    instruction = board.visualization
    if board.representation == "symbolic":
        return
    if instruction is None:
        raise ValueError("VISUALIZATION_REQUIRED_BUT_MISSING")
    definition = CATALOGUE.get((instruction.type, instruction.template))
    if definition is None:
        raise ValueError(f"VISUALIZATION_TEMPLATE_UNKNOWN:{instruction.type}:{instruction.template}")
    parameters = instruction.parameters
    missing = definition.required - parameters.keys()
    unexpected = parameters.keys() - definition.required - definition.optional
    if missing: raise ValueError(f"Missing visualization parameters: {sorted(missing)}")
    if unexpected: raise ValueError(f"Unexpected visualization parameters: {sorted(unexpected)}")
    _reject_unsafe(parameters)
    definition.validate(parameters)
    if definition.requires_step_states and any(step.visualization_state is None for step in board.steps):
        raise ValueError(f"{instruction.template} requires explicit visual states")
    if instruction.template == "central_angle_theorem":
        angle = float(parameters["central_angle"]); answer = angle / 2
        expected = f"{answer:g}°"
        if expected not in board.steps[-1].after_expression:
            raise ValueError("Central-angle result does not agree with parameters")
