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
    for key, value in parameters.items():
        values = value if isinstance(value, list) else [value]
        if len(values) > 100:
            raise ValueError("Visualization parameter collection exceeds 100 values")
        for item in values:
            # Comparison signs are valid mathematics (for example ``x > 2``).
            # Reject markup-like starts and executable protocols instead of
            # rejecting the mathematical angle-bracket characters themselves.
            limit = 600 if (key in {"source_data", "initial_state"} or key == "prompt" and str(parameters.get("question_id", "")).startswith(("g8-ae-l09-", "g8-ae-l10-"))) and re.fullmatch(r"g8-ae-l(?:0[1-9]|10)-w\d{2}", str(parameters.get("question_id", ""))) else 160
            if isinstance(item, str) and (len(item) > limit or re.search(r"<\s*/?\s*[A-Za-z!][^>]{0,80}>|javascript:|\beval\b|\bfunction\s*\(", item, re.I)):
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

def _sequence_native(parameters: dict) -> None:
    terms,positions=parameters["terms"],parameters["positions"]
    if not isinstance(terms,list) or not 2 <= len(terms) <= 12 or not isinstance(positions,list) or len(positions)!=len(terms):
        raise ValueError("Native sequence terms and positions must contain 2 to 12 aligned values")
    if any(not isinstance(value,(int,float)) or isinstance(value,bool) for value in [*terms,*positions]):
        raise ValueError("Native sequence terms and positions must be numeric")
    lines=parameters["working_lines"]
    if not isinstance(lines,list) or not lines or len(lines)>12 or any(not isinstance(line,str) or not line.strip() for line in lines):
        raise ValueError("Sequence working_lines must contain 1 to 12 mathematical steps")
    for name in ("title","method","answer"):
        if not isinstance(parameters[name],str) or not parameters[name].strip():
            raise ValueError(f"Sequence {name} must be non-empty")
    objects=parameters["objects"]
    if not isinstance(objects,list) or len(objects)!=6 or len(set(objects))!=6:
        raise ValueError("Sequence native visuals require six unique semantic object IDs")
    for name in ("differences","second_differences","partial_sums","ratios"):
        if name in parameters and (not isinstance(parameters[name],list) or any(not isinstance(value,(int,float)) or isinstance(value,bool) for value in parameters[name])):
            raise ValueError(f"Sequence {name} must be numeric")

def _finance_timeline(parameters: dict) -> None:
    periods = parameters["periods"]
    rate = parameters["periodic_rate"]
    cashflows = parameters["cashflows"]
    if not isinstance(periods, int) or isinstance(periods, bool) or not 1 <= periods <= 360:
        raise ValueError("periods must be an integer from 1 to 360")
    if not isinstance(rate, (int, float)) or isinstance(rate, bool) or not -1 < rate < 1:
        raise ValueError("periodic_rate must be between -1 and 1")
    if not isinstance(cashflows, list) or not 2 <= len(cashflows) <= 30:
        raise ValueError("cashflows must contain 2 to 30 bounded labels")
    if any(not isinstance(item, str) or not item.strip() for item in cashflows):
        raise ValueError("cashflow labels must be non-empty strings")

def _algebra_reasoning(parameters: dict) -> None:
    allowed_modes={"balance","factorisation","zero_product","quadratic_formula","method_selection","surd","quadratic_form","exponential","linear_simultaneous","nonlinear_simultaneous","inequality","discriminant","parameter_roots","rational_restrictions","proof","modelling","integrated","mastery"}
    if parameters["mode"] not in allowed_modes:
        raise ValueError("Unsupported algebra reasoning mode")
    if any(not isinstance(parameters[name],str) or not parameters[name].strip() for name in ("prompt","answer","method")):
        raise ValueError("Algebra prompt, answer and method must be non-empty strings")
    if "values" in parameters and (not isinstance(parameters["values"],list) or len(parameters["values"])>6 or any(not isinstance(value,(int,float)) or isinstance(value,bool) for value in parameters["values"])):
        raise ValueError("Algebra values must be a bounded numeric list")


def _grade8_equation_visual(parameters: dict) -> None:
    for name in ("prompt", "source_data", "initial_state", "family", "question_id"):
        if not isinstance(parameters[name], str) or not parameters[name].strip():
            raise ValueError(f"Grade 8 equation {name} must be non-empty")
    if not re.fullmatch(r"g8-ae-l(?:0[1-9]|10)-w\d{2}", parameters["question_id"]):
        raise ValueError("Grade 8 equation question_id is invalid")

def _semantic_workbench(parameters: dict) -> None:
    for name in ("prompt", "answer", "family"):
        if not isinstance(parameters[name], str) or not parameters[name].strip():
            raise ValueError(f"{name} must be non-empty")
    objects = parameters.get("objects", [])
    if not isinstance(objects, list) or not 3 <= len(objects) <= 40 or any(not isinstance(item, str) or not item for item in objects):
        raise ValueError("objects must contain 3 to 40 semantic object IDs")

def _box_plot(parameters: dict) -> None:
    names = ("minimum", "q1", "median", "q3", "maximum")
    values = [parameters[name] for name in names]
    if any(not isinstance(value, (int, float)) or isinstance(value, bool) for value in values):
        raise ValueError("Box-plot values must be numeric")
    if any(not -1_000_000 <= value <= 1_000_000 for value in values):
        raise ValueError("Box-plot values exceed the supported range")
    if values != sorted(values):
        raise ValueError("Box-plot values must satisfy minimum <= q1 <= median <= q3 <= maximum")
    if values[0] == values[-1]:
        raise ValueError("A box plot requires a non-zero axis range")
    for name in ("show_labels", "show_iqr", "show_range"):
        if name in parameters and not isinstance(parameters[name], bool):
            raise ValueError(f"{name} must be boolean")

def _ordered_five(parameters: dict) -> None:
    values = parameters["five_number_summary"]
    if not isinstance(values, list) or len(values) != 5:
        raise ValueError("five_number_summary must contain exactly five values")
    shadow = {"minimum": values[0], "q1": values[1], "median": values[2], "q3": values[3], "maximum": values[4]}
    _box_plot(shadow)

def _paired_values(parameters: dict) -> None:
    _numeric_lists("x_values", "y_values")(parameters)

def _regression(parameters: dict) -> None:
    for name in ("x_min", "x_max", "intercept", "slope"):
        if not isinstance(parameters[name], (int, float)) or isinstance(parameters[name], bool):
            raise ValueError(f"{name} must be numeric")
    if parameters["x_min"] >= parameters["x_max"]:
        raise ValueError("x_min must be less than x_max")
    if ("x_values" in parameters) != ("y_values" in parameters):
        raise ValueError("Regression points require both x_values and y_values")
    if "x_values" in parameters:
        _paired_values(parameters)

def _outlier_fence(parameters: dict) -> None:
    for name in ("q1", "q3", "lower_fence", "upper_fence"):
        if not isinstance(parameters[name], (int, float)) or isinstance(parameters[name], bool):
            raise ValueError(f"{name} must be numeric")
    if not parameters["q1"] <= parameters["q3"] or not parameters["lower_fence"] <= parameters["q1"] <= parameters["q3"] <= parameters["upper_fence"]:
        raise ValueError("Outlier fence parameters are not ordered")
    _numeric_lists("values")(parameters)

def _data_studio(parameters: dict) -> None:
    if not isinstance(parameters["sample_size"],int) or isinstance(parameters["sample_size"],bool) or not 1 <= parameters["sample_size"] <= 1_000_000:
        raise ValueError("sample_size must be a positive bounded integer")
    for name in ("variable","population","variable_type","display"):
        if not isinstance(parameters[name],str) or not parameters[name].strip():
            raise ValueError(f"Data studio {name} must be non-empty")
    _semantic_workbench({**parameters,"prompt":"data scenario","answer":"classification","family":"data_studio"})

def _coordinate_distance(parameters: dict) -> None:
    _numeric_lists("x_values", "y_values")(parameters)
    if len(parameters["x_values"]) != 2:
        raise ValueError("Coordinate distance requires exactly two points")
    if len(parameters.get("labels", [])) != 2:
        raise ValueError("Coordinate distance requires two point labels")

def _circle_construction(parameters: dict) -> None:
    for name in ("centre_x", "centre_y", "radius"):
        if not isinstance(parameters[name], (int, float)) or isinstance(parameters[name], bool):
            raise ValueError(f"{name} must be numeric")
    if parameters["radius"] <= 0:
        raise ValueError("Circle radius must be positive")

def _coordinate_scene(parameters: dict) -> None:
    xs, ys, labels = parameters["x_values"], parameters["y_values"], parameters["labels"]
    if not isinstance(xs, list) or not isinstance(ys, list) or not isinstance(labels, list):
        raise ValueError("Coordinate scene points and labels must be arrays")
    if not 1 <= len(xs) <= 12 or len(xs) != len(ys) or len(xs) != len(labels):
        raise ValueError("Coordinate scene points and labels must have matching lengths from 1 to 12")
    if any(not isinstance(value, (int, float)) or isinstance(value, bool) or not -1_000_000 <= value <= 1_000_000 for value in [*xs, *ys]):
        raise ValueError("Coordinate scene coordinates must be bounded numbers")
    if any(not isinstance(label, str) or not label.strip() or len(label) > 12 for label in labels):
        raise ValueError("Coordinate scene labels must be short non-empty strings")
    values = parameters["values"]
    if not isinstance(values, list) or not values or len(values) > 40 or any(not isinstance(value, (int, float)) or isinstance(value, bool) or not -1_000_000 <= value <= 1_000_000 for value in values):
        raise ValueError("Coordinate scene values must be a non-empty bounded numeric array")
    _semantic_workbench({**parameters, "prompt":"coordinate scene", "answer":"coordinate result", "family":"coordinate_scene"})

CATALOGUE: dict[tuple[str, str], TemplateDefinition] = {
    **{
        ("algebra", template): TemplateDefinition(
            frozenset({"prompt", "source_data", "initial_state", "family", "question_id"}),
            frozenset({"total_steps"}),
            _grade8_equation_visual,
            True,
        )
        for template in (
            "equality_balance", "additive_inverse", "multiplicative_inverse",
            "two_step_balance", "variables_both_sides", "context_to_equation",
            "distributive_equation", "inspection_fact_family", "inspection_number_line",
            "inspection_substitution_table", "inspection_context",
            "additive_balance", "additive_number_line", "additive_context",
            "equal_groups", "fraction_scale", "multiplicative_balance", "multiplicative_context",
            "two_step_balance_native", "operation_machine", "two_step_number_line",
            "two_step_fraction_scale", "two_step_context", "variables_both_sides_native", "expression_comparison",
            "identity_contradiction", "dual_rate_timeline", "equal_sides_triangle",
            "bracket_balance_native", "bracket_distribution_native", "bracket_paths_native", "bracket_area_native", "bracket_rectangle_native",
            "fraction_bar_balance_native", "fraction_equivalence_native", "fraction_lcd_native", "fraction_error_native", "fraction_context_native",
            "context_translation_strip_native", "number_relationship_native", "money_model_native", "perimeter_model_native", "sharing_bar_model_native", "age_timeline_native", "rate_table_native", "error_diagnosis_context_native",
        )
    },
    **{
        ("algebra", template): TemplateDefinition(
            frozenset({"prompt", "source_data", "initial_state", "family", "question_id"}),
            frozenset({"total_steps"}), _grade8_equation_visual, True,
        ) for template in (
            "diagnosis_first_error_replay_native", "diagnosis_balance_equation_native",
            "diagnosis_signed_balance_native", "diagnosis_bracket_distribution_native",
            "diagnosis_denominator_lcm_native", "diagnosis_error_diagnosis_context_native",
            "diagnosis_perimeter_model_native", "diagnosis_identity_contradiction_native",
            "diagnosis_rate_table_native", "diagnosis_mastery_map_native",
        )
    },
    ("geometry", "central_angle_theorem"): TemplateDefinition(frozenset({"central_angle"}), frozenset({"target"}), _bounded_number("central_angle", 0, 180), True),
    ("geometry", "cyclic_quadrilateral"): TemplateDefinition(frozenset({"known_angle"}), frozenset(), _bounded_number("known_angle", 0, 180), True),
    ("geometry", "tangent_radius"): TemplateDefinition(frozenset(), frozenset({"radius_label","tangent_label"}), _noop, True),
    ("geometry", "same_segment"): TemplateDefinition(frozenset(), frozenset({"angle"}), _noop, True),
    ("geometry", "angle_in_semicircle"): TemplateDefinition(frozenset(), frozenset(), _noop, True),
    ("geometry", "equal_tangents"): TemplateDefinition(frozenset({"length"}), frozenset(), _bounded_number("length", 0, 10000), True),
    ("geometry", "similar_triangles"): TemplateDefinition(frozenset(), frozenset({"scale_factor"}), _noop, True),
    ("coordinate_geometry", "coordinate_plane"): TemplateDefinition(frozenset({"x_values","y_values"}), frozenset({"title","show_line","show_circle"}), _numeric_lists("x_values","y_values"), True),
    ("coordinate_geometry", "coordinate_distance_lab"): TemplateDefinition(frozenset({"x_values","y_values","labels","objects"}), frozenset({"title","delta_x","delta_y"}), lambda p: (_coordinate_distance(p), _semantic_workbench({**p,"prompt":"distance","answer":"distance","family":"coordinate_distance_lab"})), True),
    ("coordinate_geometry", "circle_construction"): TemplateDefinition(frozenset({"centre_x","centre_y","radius","objects"}), frozenset({"title"}), lambda p: (_circle_construction(p), _semantic_workbench({**p,"prompt":"circle","answer":"circle","family":"circle_construction"})), True),
    ("function_graph", "cartesian_function"): TemplateDefinition(frozenset({"graph_spec_id"}), frozenset(), _noop),
    ("calculus", "secant_to_tangent"): TemplateDefinition(frozenset({"graph_spec_id"}), frozenset(), _noop),
    ("trigonometry", "right_triangle"): TemplateDefinition(frozenset({"opposite","adjacent","hypotenuse"}), frozenset({"angle"}), _noop, True),
    ("trigonometry", "oblique_triangle"): TemplateDefinition(frozenset({"side_a","side_b","included_angle"}), frozenset({"target_side"}), _oblique_triangle, True),
    ("trigonometry", "unit_circle"): TemplateDefinition(frozenset({"angle"}), frozenset(), _bounded_number("angle", -721, 721), True),
    ("statistics", "data_plot"): TemplateDefinition(frozenset({"values"}), frozenset({"kind","title"}), _numeric_lists("values"), True),
    ("statistics", "data_studio"): TemplateDefinition(frozenset({"sample_size","variable","population","variable_type","display","objects"}), frozenset({"title"}), _data_studio, True),
    ("statistics", "box_plot"): TemplateDefinition(
        frozenset({"minimum", "q1", "median", "q3", "maximum"}),
        frozenset({"title", "show_labels", "show_iqr", "show_range"}),
        _box_plot, True,
    ),
    ("statistics", "five_number_summary"): TemplateDefinition(frozenset({"five_number_summary", "objects"}), frozenset({"title"}), lambda p: (_ordered_five(p), _semantic_workbench({**p, "prompt":"summary", "answer":"summary", "family":"five_number_summary"})), True),
    ("statistics", "ogive"): TemplateDefinition(frozenset({"upper_boundaries", "cumulative_frequencies", "objects"}), frozenset({"title"}), lambda p: (_numeric_lists("upper_boundaries", "cumulative_frequencies")(p), _semantic_workbench({**p, "prompt":"ogive", "answer":"ogive", "family":"ogive"})), True),
    ("statistics", "scatter_plot"): TemplateDefinition(frozenset({"x_values", "y_values", "objects"}), frozenset({"title", "outlier_index"}), lambda p: (_paired_values(p), _semantic_workbench({**p, "prompt":"scatter", "answer":"scatter", "family":"scatter_plot"})), True),
    ("statistics", "regression_line"): TemplateDefinition(frozenset({"x_min", "x_max", "intercept", "slope", "objects"}), frozenset({"title", "estimate_x", "x_values", "y_values", "observed_min", "observed_max"}), lambda p: (_regression(p), _semantic_workbench({**p, "prompt":"regression", "answer":"regression", "family":"regression_line"})), True),
    ("statistics", "outlier_fence"): TemplateDefinition(frozenset({"q1", "q3", "lower_fence", "upper_fence", "values", "objects"}), frozenset({"title"}), lambda p: (_outlier_fence(p), _semantic_workbench({**p, "prompt":"outlier", "answer":"outlier", "family":"outlier_fence"})), True),
    ("statistics", "distribution_comparison"): TemplateDefinition(frozenset({"mean_a", "sd_a", "mean_b", "sd_b", "objects"}), frozenset({"title"}), lambda p: _semantic_workbench({**p, "prompt":"comparison", "answer":"comparison", "family":"distribution_comparison"}), True),
    ("statistics", "deviation_panel"): TemplateDefinition(frozenset({"values", "mean", "variance", "standard_deviation", "objects"}), frozenset({"title"}), lambda p: (_numeric_lists("values")(p), _semantic_workbench({**p, "prompt":"deviation", "answer":"deviation", "family":"deviation_panel"})), True),
    ("statistics", "correlation_continuum"): TemplateDefinition(frozenset({"r", "objects"}), frozenset({"title"}), lambda p: _semantic_workbench({**p, "prompt":"correlation", "answer":"correlation", "family":"correlation_continuum"}), True),
    ("statistics", "data_table"): TemplateDefinition(frozenset({"values", "objects"}), frozenset({"title", "sorted_values"}), lambda p: (_numeric_lists("values")(p), _semantic_workbench({**p, "prompt":"data", "answer":"data", "family":"data_table"})), True),
    ("sequences", "sequence_timeline"): TemplateDefinition(frozenset({"terms","positions","mode"}), frozenset({"title","differences","second_differences","ratios","next_term","next_change"}), _sequence_timeline, True),
    ("sequences", "sequence_reasoning"): TemplateDefinition(frozenset({"prompt","answer","family","objects"}), frozenset({"method"}), _semantic_workbench, True),
    ("finance", "cashflow_timeline"): TemplateDefinition(
        frozenset({"periods", "periodic_rate", "cashflows", "focal_period"}),
        frozenset({"title", "period_label", "model", "formula", "result", "direction"}),
        _finance_timeline, True,
    ),
    ("algebra", "algebra_reasoning"): TemplateDefinition(
        frozenset({"mode","prompt","answer","method"}), frozenset({"values"}),
        _algebra_reasoning, True,
    ),
}
for _sequence_template in ("term_rows","difference_table","sigma_expansion","partial_sum","convergence_diagram","formula_decision","error_diagnosis"):
    CATALOGUE[("sequences",_sequence_template)] = TemplateDefinition(
        frozenset({"title","method","working_lines","answer","objects","positions","terms"}),
        frozenset({"differences","second_differences","partial_sums","ratios","mode"}),
        _sequence_native, True,
    )
for _coordinate_template in (
    "midpoint_bisection", "slope_triangle", "line_equation_link", "parallel_comparison",
    "perpendicular_rotation", "inclination_arc", "complete_square_morph",
    "circle_condition_intersection", "radius_tangent_contact",
    "tangent_equation_construction", "external_tangent_length",
    "coordinate_proof_studio", "integrated_coordinate_scene", "question_first_assessment",
):
    CATALOGUE[("coordinate_geometry", _coordinate_template)] = TemplateDefinition(
        frozenset({"x_values", "y_values", "labels", "values", "result", "objects"}),
        frozenset({"title", "gradient", "secondary_gradient", "inclination", "centre_x", "centre_y", "radius", "midpoint_x", "midpoint_y", "line_intercept", "tangent_length", "op_distance"}),
        _coordinate_scene, True,
    )
for _kind, _families in {
    "statistics": (
        "data_studio", "balance_and_rank", "spread_number_line", "five_number_ribbon", "ogive_builder", "box_plot_builder", "outlier_fence_lab", "deviation_calculator_lab", "distribution_comparison", "scatter_builder", "correlation_continuum", "least_squares_fit", "regression_calculator", "interpolation_trace", "extrapolation_risk_zone", "influence_lab", "integrated_statistics_dashboard", "question_first_assessment",
    ),
    "coordinate_geometry": (
        "coordinate_distance_lab", "midpoint_bisection", "slope_triangle", "line_equation_link", "parallel_comparison", "perpendicular_rotation", "inclination_arc", "circle_construction", "complete_square_morph", "circle_condition_intersection", "radius_tangent_contact", "tangent_equation_construction", "external_tangent_length", "coordinate_proof_studio", "integrated_coordinate_scene", "question_first_assessment",
    ),
}.items():
    for _family in _families:
        if (_kind, _family) not in CATALOGUE:
            CATALOGUE[(_kind, _family)] = TemplateDefinition(
                frozenset({"prompt", "answer", "family", "objects"}), frozenset({"method"}),
                _semantic_workbench, True,
            )
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
    problem_lower = board.problem.casefold()
    if ("five-number summary" in problem_lower and ("construct" in problem_lower or "box plot" in problem_lower)) and instruction.template != "box_plot":
        raise ValueError("BOX_PLOT_QUESTION_REQUIRES_STATISTICS_BOX_PLOT")
    if instruction.template == "box_plot":
        expected = [parameters[name] for name in ("minimum", "q1", "median", "q3", "maximum")]
        combined = " ".join([board.problem, *[step.after_expression for step in board.steps]])
        if not all(f"{value:g}" in combined for value in expected):
            raise ValueError("BOX_PLOT_STATES_DISAGREE_WITH_VISUAL_PARAMETERS")
    if definition.requires_step_states and any(step.visualization_state is None for step in board.steps):
        raise ValueError(f"{instruction.template} requires explicit visual states")
    if instruction.template == "central_angle_theorem":
        angle = float(parameters["central_angle"]); answer = angle / 2
        expected = f"{answer:g}°"
        if expected not in board.steps[-1].after_expression:
            raise ValueError("Central-angle result does not agree with parameters")
