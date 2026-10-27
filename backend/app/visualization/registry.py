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
            limit = (6000 if key == "scene_json" else 400) if key in {"scene_json", "prompt"} and re.fullmatch(r"(?:g8-graphs-l01|g8-fr-l04)-w(?:0[1-9]|1[0-5])", str(parameters.get("question_id", ""))) else 600 if (key in {"source_data", "initial_state"} or key == "prompt" and str(parameters.get("question_id", "")).startswith(("g8-ae-l09-", "g8-ae-l10-"))) and re.fullmatch(r"g8-ae-l(?:0[1-9]|10)-w\d{2}", str(parameters.get("question_id", ""))) else 160
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

def _grade8_function_visual(parameters: dict) -> None:
    if not re.fullmatch(r"g8-fr-l0[1-4]-w(?:0[1-9]|1[0-5])", str(parameters["question_id"])):
        raise ValueError("Grade 8 functions question ID is invalid")
    if not isinstance(parameters["prompt"], str) or not parameters["prompt"].strip():
        raise ValueError("Functions problem text is required")
    for field, minimum, maximum in (("given_objects",2,5),("derived_objects",1,4)):
        values=parameters[field]
        if not isinstance(values,list) or not minimum<=len(values)<=maximum or any(not isinstance(v,str) or not v.strip() for v in values):
            raise ValueError(f"Functions {field} must contain {minimum}–{maximum} meaningful objects")
    if not isinstance(parameters["total_steps"],int) or not 3<=parameters["total_steps"]<=12:
        raise ValueError("Functions require complete progressive teaching steps")
    if parameters["question_id"].startswith("g8-fr-l03-"):
        xs=parameters.get("input_values")
        ys=parameters.get("output_values")
        if not isinstance(xs,list) or not isinstance(ys,list) or not 2<=len(xs)==len(ys)<=5 or any(
            not isinstance(x,int) or isinstance(x,bool) or not -100<=x<=100 for x in xs) or any(
            y!='?' and (not isinstance(y,int) or isinstance(y,bool) or not -10000<=y<=10000) for y in ys):
            raise ValueError("Grade 8 table requires bounded, aligned input/output values")
        if len(set(xs))!=len(xs):
            raise ValueError("Grade 8 table inputs must be unique")
        if "resolved_outputs" in parameters:
            resolved = parameters["resolved_outputs"]
            reveal = parameters.get("output_reveal_steps")
            if not isinstance(resolved, list) or len(resolved) != len(xs) or not isinstance(reveal, list) or len(reveal) != len(xs):
                raise ValueError("Resolved outputs and reveal steps must align with the table")
            if any(not isinstance(value, (str, int, float)) or isinstance(value, bool) for value in resolved):
                raise ValueError("Resolved outputs must be mathematical labels")
            if any(step is not None and (not isinstance(step, int) or isinstance(step, bool) or not -1 <= step <= parameters["total_steps"]) for step in reveal):
                raise ValueError("Output reveal steps must refer to valid teaching steps")


def _grade8_expression_visual(parameters: dict) -> None:
    if not re.fullmatch(r"g8-ex-l(?:0[1-9]|10)-w(?:0[1-9]|1[0-5])", str(parameters["question_id"])):
        raise ValueError("Grade 8 expression question_id is invalid")
    if not isinstance(parameters["prompt"], str) or not parameters["prompt"].strip():
        raise ValueError("Expression prompt is required")
    tokens = parameters["model_tokens"]
    if not isinstance(tokens, list) or not 2 <= len(tokens) <= 8 or any(not isinstance(t, str) or not t.strip() for t in tokens):
        raise ValueError("Expression model needs 2–8 mathematical objects")
    if not isinstance(parameters["total_steps"], int) or not 3 <= parameters["total_steps"] <= 12:
        raise ValueError("Expression lesson needs progressive teaching steps")
    lanes = parameters.get('model_lanes')
    if lanes is not None and (not isinstance(lanes,list) or len(lanes)!=len(tokens) or any(not isinstance(lane,str) or not lane.strip() or len(lane)>24 for lane in lanes)):
        raise ValueError("Expression lanes must label each given object exactly once")
    scene=parameters.get('model_scene')
    if scene is not None:
        allowed={'rows','columns','unit','share','unit_price','square_rows','square_columns','rectangle_rows','rectangle_columns','side','segments','input_count'}
        if not isinstance(scene,dict) or not set(scene)<=allowed:
            raise ValueError("Expression scene has unsupported fields")
        if any(not isinstance(value,int) or isinstance(value,bool) or not 0<=value<=12 for key,value in scene.items() if key not in {'unit','share','side','segments'}):
            raise ValueError("Expression scene counts must be small non-negative integers")
        if 'input_count' in scene and not 1<=scene['input_count']<len(tokens):
            raise ValueError("Expression scene needs given factors and separately revealed results")
        if 'share' in scene and (not isinstance(scene['share'],(int,float)) or isinstance(scene['share'],bool) or not 0<scene['share']<=1):
            raise ValueError("Expression scene share must be between zero and one")
        if 'unit' in scene and (not isinstance(scene['unit'],str) or not scene['unit'].strip() or len(scene['unit'])>24):
            raise ValueError("Expression scene unit must be a short mathematical label")
        if 'side' in scene and (not isinstance(scene['side'],str) or not scene['side'].strip() or len(scene['side'])>24):
            raise ValueError("Expression scene side must be a short mathematical label")
        if 'segments' in scene and (not isinstance(scene['segments'],str) or len(scene['segments'].split('|'))!=2 or any(not part.strip() or len(part)>24 for part in scene['segments'].split('|'))):
            raise ValueError("Expression scene must describe two separate bracket widths")
        for first, second in (('rows','columns'),('square_rows','square_columns'),('rectangle_rows','rectangle_columns')):
            if first in scene and second in scene and scene[first]*scene[second]>48:
                raise ValueError("Expression scene grid exceeds 48 visible cells")

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


def _grade8_coordinate_plane(parameters: dict) -> None:
    import json
    try:
        scene = json.loads(parameters["scene_json"])
    except (TypeError, ValueError) as error:
        raise ValueError("Grade 8 coordinate scene must be valid JSON") from error
    if not isinstance(scene, dict) or not isinstance(scene.get("id"), str):
        raise ValueError("Grade 8 coordinate scene needs a stable ID")
    if parameters["question_id"] != scene["id"]:
        raise ValueError("Grade 8 coordinate scene must match the question ID")
    axis = scene.get("axis")
    if not isinstance(axis, dict):
        raise ValueError("Grade 8 coordinate scene needs axes")
    for key in ("x_min", "x_max", "y_min", "y_max", "x_tick", "y_tick"):
        value = axis.get(key)
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not -1000 <= value <= 1000:
            raise ValueError(f"Grade 8 coordinate {key} must be a bounded number")
    if not axis["x_min"] <= 0 < axis["x_max"] or not axis["y_min"] <= 0 < axis["y_max"]:
        raise ValueError("Grade 8 coordinate axes must contain the origin")
    if axis["x_tick"] <= 0 or axis["y_tick"] <= 0:
        raise ValueError("Grade 8 coordinate ticks must be positive")
    labels = set()
    for point in [*scene.get("given", []), *scene.get("derived", [])]:
        if not isinstance(point, dict) or not isinstance(point.get("label"), str):
            raise ValueError("Grade 8 coordinate point needs a label")
        if point["label"] in labels:
            raise ValueError("Grade 8 coordinate point labels must be unique")
        labels.add(point["label"])
        for coordinate, lower, upper in (("x", axis["x_min"], axis["x_max"]), ("y", axis["y_min"], axis["y_max"])):
            value = point.get(coordinate)
            if not isinstance(value, (int, float)) or isinstance(value, bool) or not lower <= value <= upper:
                raise ValueError(f"Grade 8 coordinate {coordinate} is outside the plotted axes")
        if point in scene.get("derived", []):
            step = point.get("reveal_step")
            if not isinstance(step, int) or isinstance(step, bool) or not 1 <= step <= parameters["total_steps"]:
                raise ValueError("Grade 8 derived point needs a valid reveal step")

def _grade8_formula_rectangle(parameters: dict) -> None:
    import json
    _grade8_function_visual(parameters)
    try:
        scene = json.loads(parameters["scene_json"])
    except (TypeError, ValueError) as error:
        raise ValueError("Rectangle scene must be valid JSON") from error
    if not isinstance(scene, dict) or scene.get("units") not in {"cm", "m"}:
        raise ValueError("Rectangle requires labelled units")
    for key in ("length", "width", "area"):
        value=scene.get(key)
        if not isinstance(value,(int,float)) or isinstance(value,bool) or not 0<value<=1000:
            raise ValueError(f"Rectangle {key} must be positive and bounded")
    if abs(scene["length"]*scene["width"]-scene["area"])>1e-8:
        raise ValueError("Rectangle area disagrees with its side lengths")
    if "perimeter" in scene and abs(2*(scene["length"]+scene["width"])-scene["perimeter"])>1e-8:
        raise ValueError("Rectangle perimeter disagrees with its side lengths")
    if "symbolic_length" in scene and (not isinstance(scene["symbolic_length"],str) or len(scene["symbolic_length"])>24):
        raise ValueError("Symbolic length must be a short label")

CATALOGUE: dict[tuple[str, str], TemplateDefinition] = {
    ("algebra", "formula_rectangle"): TemplateDefinition(
        frozenset({"prompt", "question_id", "given_objects", "derived_objects", "total_steps", "scene_json"}),
        frozenset(), _grade8_formula_rectangle, True),
    **{("algebra", template): TemplateDefinition(
        frozenset({"prompt", "question_id", "given_objects", "derived_objects", "total_steps"}),
        frozenset(), _grade8_function_visual, True)
        for template in ("function_flow", "function_table", "function_reverse", "function_context", "function_compare",
                         "equivalence_translation", "equivalence_flow_table", "equivalence_counterexample",
                         "equivalence_context", "equivalence_domain", "equivalence_algebra")},
    **{("algebra", template): TemplateDefinition(
        frozenset({"prompt", "question_id", "given_objects", "derived_objects", "total_steps", "input_values", "output_values"}),
        frozenset({"resolved_outputs", "output_reveal_steps"}), _grade8_function_visual, True)
        for template in ("rule_difference", "rule_zero", "rule_signed", "rule_nonlinear", "rule_context", "rule_choice")},
    **{("algebra", template): TemplateDefinition(
        frozenset({"prompt", "question_id", "model_tokens", "model_description", "total_steps"}),
        frozenset({"model_lanes", "model_scene"}), _grade8_expression_visual, True)
        for template in ("expression_tiles", "signed_terms", "grouped_terms",
            "fraction_bar", "square_comparison", "like_term_sort", "unlike_term_sort",
            "receipt", "rectangle", "bracket_negation", "grouped_polynomials",
            "factor_array", "sign_grid", "area_product", "power_stack", "area_comparison",
            "distribute_strip", "signed_distribute", "trinomial_branches", "area_distribute", "compare_paths",
            "equal_share", "signed_quotient", "factor_cancel", "term_share", "three_term_share",
            "exponent_lanes", "context_packs", "error_division", "two_quotients", "square_grid", "signed_square", "cube_stack", "signed_cube", "sign_scope", "power_factor_stack", "root_pairs", "absolute_root", "cube_root", "fraction_cube", "error_root", "compare_powers", "compare_roots", "value_machine", "signed_slot", "exponent_scope", "compare_scope", "two_input", "bracket_input", "layered_order", "fraction_gate", "equivalent_value_paths", "error_substitution", "context_measure", "term_bins", "distribute_collect", "signed_distribution_collect", "quotient_collect", "dual_distribution_collect", "negative_bracket", "variable_quotient_collect", "power_bins", "distribution_error", "perimeter_mixed", "equivalent_mixed", "layered_mixed", "layered_quotient_mixed", "unit_receipt", "fixed_variable_receipt", "flow_rule", "input_table", "fare_table", "decrease_timeline", "packs_plus_loose", "context_perimeter", "plan_comparison", "fee_error", "equivalence_models", "general_table", "split_area_context", "parallel_flows", "fundraiser_audit", "diagnostic_term_sort", "diagnostic_signed_terms", "diagnostic_factor_array", "diagnostic_distribution_paths", "diagnostic_signed_distribution", "diagnostic_quotient_lanes", "diagnostic_exponent_scope", "diagnostic_root_pairs", "diagnostic_parallel_paths", "diagnostic_mixed_trace", "diagnostic_restricted_quotient", "diagnostic_context_receipt", "diagnostic_area_split", "diagnostic_parallel_flows", "diagnostic_integrated_trace")},
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
    ("coordinate_geometry", "grade8_coordinate_plane"): TemplateDefinition(
        frozenset({"scene_json", "question_id", "prompt", "total_steps"}), frozenset(), _grade8_coordinate_plane, True),
    ("graphs", "coordinate_plane"): TemplateDefinition(
        frozenset({"scene_json", "question_id", "prompt", "total_steps"}), frozenset(), _grade8_coordinate_plane, True),
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
