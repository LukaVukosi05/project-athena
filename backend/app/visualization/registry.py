"""Allow-listed, parameter-validated mathematical visualization catalogue."""
from dataclasses import dataclass
from collections.abc import Callable
import math
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
            limit = (6000 if key == "scene_json" else 400) if key in {"scene_json", "prompt"} and re.fullmatch(r"(?:g8-graphs-l0[1-6]|g8-patterns-l0[1-6]|g8-whole-l0[1-2]|g8-int-l0[1-6]|g8-frac-l0[1-8]|g8-dec-l0[1-6]|g8-exp-l0[1-6]|g8-fr-l0[4-6]|g8-shapes-0[1-5]|g8-pyth-0[1-5]|g8-lines-0[3-5]|g9-whole-l0[1-8]|g9-int-l0[1-5]|g9-exp-l0[1-6]|g9-pat-l0[1-5]|g9-fn-l0[1-5]|g9-aex-l0[1-9]|g9-eq-l0[1-6]|g9-gr-l0[1-7]|g9-lines-l0[1-5]|g9-shapes-l0[1-8]|g9-area-l0[1-5]|g9-data-l0[1-8]|g9-prob-l0[1-5]|g9-solid-l0[1-4]|g9-sv-l0[1-6]|g9-tg-l0[1-7]|g10-aex-l0[1-6]|g10-eei-l0[1-9]|g10-trig-l0[1-7]|g10-euc-l0[1-6]|g10-ag-l0[1-6]|g10-fn-l0[1-7]|g10-stat-l0[1-6])-w(?:0[1-9]|1[0-5])", str(parameters.get("question_id", ""))) else 600 if (key in {"source_data", "initial_state"} or key == "prompt" and str(parameters.get("question_id", "")).startswith(("g8-ae-l09-", "g8-ae-l10-"))) and re.fullmatch(r"g8-ae-l(?:0[1-9]|10)-w\d{2}", str(parameters.get("question_id", ""))) else 160
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
    if not re.fullmatch(r"g8-fr-l0[1-6]-w(?:0[1-9]|1[0-5])", str(parameters["question_id"])):
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


def _grade8_fraction_strips(parameters: dict) -> None:
    import json
    from app.curriculum.grade8.fractions_math import answer,common_denominator,value
    scene=json.loads(parameters["scene_json"])
    values=scene.get("values")
    kind=scene.get("kind")
    if (scene.get("id")!=parameters["question_id"] or scene.get("problem")!=parameters["prompt"]
        or kind not in {"equivalent","compare","order","convert","arithmetic"}
        or not isinstance(values,list) or not 1<=len(values)<=4
        or len(scene.get("rows",[]))!=3 or parameters["total_steps"]!=5):
        raise ValueError("Fraction question requires its own bounded complete strips")
    if any(not isinstance(v,str) or not 1<=len(v)<=12 or not 0<value(v)<=5 or value(v).denominator>24 for v in values):
        raise ValueError("Fraction strips require positive bounded rational values")
    if len(values)!={"equivalent":2,"compare":2,"order":3,"convert":1}.get(kind,len(values)):
        raise ValueError("Fraction task uses the wrong number of original values")
    operators=scene.get("operators")
    if kind=="arithmetic":
        if not isinstance(operators,list) or len(operators)!=len(values)-1 or any(op not in {"+","-"} for op in operators):
            raise ValueError("Fraction calculation must preserve the original operations")
    elif operators is not None:
        raise ValueError("Comparison does not use arithmetic operators")
    expected=answer(kind,values,operators)
    if scene.get("answer")!=expected or scene.get("common_denominator")!=common_denominator(values):
        raise ValueError("Fraction answer or common unit does not match the source fractions")
    if kind=="arithmetic" and not isinstance(scene.get("memo"),str):
        raise ValueError("Fraction arithmetic needs a verification memo")


def _grade8_fraction_operations(parameters: dict) -> None:
    import json
    from app.curriculum.grade8.fractions_math import answer,common_denominator,value
    scene=json.loads(parameters["scene_json"])
    values=scene.get("values")
    kind=scene.get("kind")
    if (scene.get("id")!=parameters["question_id"] or scene.get("problem")!=parameters["prompt"]
        or kind not in {"multiply","divide"} or not isinstance(values,list) or len(values)!=2
        or len(scene.get("rows",[]))!=3 or parameters["total_steps"]!=5):
        raise ValueError("Fraction operation requires a matching question and complete steps")
    if any(not isinstance(v,str) or not 1<=len(v)<=12 or not 0<value(v)<=36 or value(v).denominator>24 for v in values):
        raise ValueError("Fraction group/area requires positive bounded operands")
    if scene.get("common_denominator") != common_denominator(values) or scene.get("answer") != answer(kind,values):
        raise ValueError("Fraction result or partition disagrees with exact rational arithmetic")
    if any(not isinstance(row,str) or not row.strip() for row in scene['rows']) or not isinstance(scene.get('memo'),str):
        raise ValueError("Fraction operation requires authored reasoning and verification")


def _grade8_decimal_operation(parameters: dict, expected_kind: str) -> None:
    import json,re
    from app.curriculum.grade8.decimal_math import operation
    scene=json.loads(parameters['scene_json']);values=scene.get('values')
    if (scene.get('kind')!=expected_kind or not isinstance(values,list) or len(values)!=2
        or not all(isinstance(v,str) and re.fullmatch(r'\d{1,3}\.\d{1,5}',v) for v in values)
        or scene.get('id')!=parameters['question_id'] or scene.get('problem')!=parameters['prompt']):
        raise ValueError('Decimal operation needs matching bounded source values and task')
    try:answer,rows,problem,memo=operation(expected_kind,values)
    except (ValueError,ArithmeticError) as exc:raise ValueError('Unsupported decimal operation') from exc
    if (scene.get('answer')!=answer or scene.get('rows')!=rows or scene.get('problem')!=problem
        or scene.get('memo')!=memo or parameters['total_steps']!=len(rows)+2
        or scene.get('visual_family')!=('decimal_product' if expected_kind=='multiply' else 'decimal_quotient')):
        raise ValueError('Decimal operation scene disagrees with exact arithmetic or teaching steps')


def _grade8_decimal_product(parameters: dict) -> None:
    _grade8_decimal_operation(parameters,'multiply')


def _grade8_decimal_quotient(parameters: dict) -> None:
    _grade8_decimal_operation(parameters,'divide')


def _grade8_line_scene(parameters: dict, expected_lesson: int) -> None:
    import json
    from app.curriculum.grade8.straight_lines_cases import LESSON_1, LESSON_2
    from app.curriculum.grade8.straight_lines_runtime import _labels
    cases = (LESSON_1, LESSON_2)[expected_lesson-1]
    case = next((case for case in cases if case.id == parameters['question_id']), None)
    if case is None or parameters['prompt'] != case.problem or parameters['total_steps'] != len(case.working)+1:
        raise ValueError('Grade 8 straight-line visualization disagrees with the authored question')
    scene = json.loads(parameters['scene_json'])
    given,target = _labels(case)
    if scene != {'diagram':case.diagram,'relationship':case.relationship,'given_label':given,
                 'target_label':target,'reason':case.relationship.replace('_',' ')}:
        raise ValueError('Grade 8 straight-line diagram labels or relationship disagree with the question')


def _grade8_angle_chain_scene(parameters: dict, expected_lesson: int) -> None:
    import json
    from app.curriculum.grade8.straight_lines_chain_cases import LESSONS
    case=next((item for item in LESSONS[expected_lesson] if item.id==parameters['question_id']),None)
    if (case is None or parameters['prompt']!=case.problem or
        parameters['total_steps']!=len(case.working)+1 or
        json.loads(parameters['scene_json'])!=case.scene):
        raise ValueError('Grade 8 angle-chain diagram disagrees with the authored question or its values')


def _grade8_shape_scene(parameters: dict, family: str) -> None:
    import json
    from app.curriculum.grade8.shapes_cases import LESSONS
    matches=[case for cases in LESSONS.values() for case in cases if case.id==parameters['question_id']]
    if len(matches)!=1:
        raise ValueError('Unknown Grade 8 shape question')
    case=matches[0]
    if (case.family!=family or parameters['prompt']!=case.problem
        or parameters['total_steps']!=len(case.working)+1
        or json.loads(parameters['scene_json'])!={**case.scene,'family':case.family}):
        raise ValueError('Grade 8 shape diagram or its marked values disagree with the question')
    pts=case.scene['points']
    if len(pts) not in (3,4) or any(len(p)!=2 or not all(0<=v<=360 for v in p) for p in pts):
        raise ValueError('Grade 8 shape vertices must be complete and inside the stage')


def _grade8_pythagoras_scene(parameters: dict, family: str) -> None:
    import json
    from app.curriculum.grade8.pythagoras_cases import LESSONS
    matches=[case for cases in LESSONS.values() for case in cases if case.id==parameters['question_id']]
    if len(matches)!=1:
        raise ValueError('Unknown Pythagoras question ID')
    case=matches[0]
    expected={'family':case.family,'a':case.a,'b':case.b,'c':case.c,
              'context':case.context,'problem':case.problem}
    if (case.family!=family or parameters['prompt']!=case.problem or
        parameters['total_steps']!=len(case.working)+1 or
        json.loads(parameters['scene_json'])!=expected):
        raise ValueError('Pythagoras diagram, data or steps disagree with authored mathematics')
    if family=='converse' and sorted((case.a,case.b,case.c))[0]+sorted((case.a,case.b,case.c))[1]<=max(case.a,case.b,case.c):
        raise ValueError('Invalid triangle side lengths')


def _grade8_exponent_scene(parameters: dict, expected_lesson: int) -> None:
    import json,re
    from app.curriculum.grade8.exponent_math import solve
    from app.curriculum.grade8.exponent_roots_math import solve as roots_solve
    from app.curriculum.grade8.exponent_reasoning_math import solve as reasoning_solve
    scene=json.loads(parameters['scene_json']);values=scene.get('values');kind=scene.get('kind')
    allowed={1:{'expand','negative','compare','science'},
             2:{'product','quotient','zero','power_product','mixed'},
             3:{'square_root','cube_root','root_pair','square_area','cube_volume'},
             4:{'mixed','square_area','cube_volume'},
             5:{'sign_audit','root_audit','quotient_audit','root_sum_audit','mixed_audit'},
             6:{'square_perimeter_gap','cube_edge_gap','side_area_gap','root_power_compare','combined_perimeter'}}[expected_lesson]
    if (kind not in allowed or not isinstance(values,list) or not 1<=len(values)<=4
        or any(not isinstance(v,str) or not re.fullmatch(r'-?\d{1,9}',v) for v in values)
        or scene.get('id')!=parameters['question_id'] or scene.get('problem')!=parameters['prompt']):
        raise ValueError('Exponent lesson requires a matching bounded question and type')
    answer,rows,problem,memo=(solve if expected_lesson<3 else roots_solve if expected_lesson<5 else reasoning_solve)(kind,values)
    if (scene.get('answer')!=answer or scene.get('rows')!=rows or scene.get('problem')!=problem
        or scene.get('memo')!=memo or parameters['total_steps']!=len(rows)+2
        or scene.get('visual_family')!=('ten_place_shift' if kind=='science' else 'power_factors' if expected_lesson<3 else 'root_square_cube' if expected_lesson==3 else 'root_application' if expected_lesson==4 else 'exponent_error_trace' if expected_lesson==5 else 'exponent_context_measure')):
        raise ValueError('Exponent scene disagrees with exact arithmetic or steps')


def _grade8_decimal_power_root(parameters: dict, expected_kind: str) -> None:
    import json,re
    from app.curriculum.grade8.decimal_math import power_root
    scene=json.loads(parameters['scene_json']);values=scene.get('values')
    if (scene.get('kind')!=expected_kind or not isinstance(values,list) or len(values)!=2
        or not isinstance(values[0],str) or not re.fullmatch(r'\d{1,3}\.\d{1,5}',values[0])
        or values[1] not in ('2','3') or scene.get('id')!=parameters['question_id']
        or scene.get('problem')!=parameters['prompt']):
        raise ValueError('Decimal powers/roots need matching bounded values and task')
    answer,rows,problem,memo=power_root(expected_kind,values)
    if (scene.get('answer')!=answer or scene.get('rows')!=rows or scene.get('problem')!=problem
        or scene.get('memo')!=memo or parameters['total_steps']!=len(rows)+2
        or scene.get('visual_family')!=('decimal_power' if expected_kind=='power' else 'decimal_root')):
        raise ValueError('Decimal power/root scene disagrees with exact arithmetic')


def _grade8_decimal_scene(parameters: dict) -> None:
    import json,re
    from app.curriculum.grade8.decimal_math import solution
    scene=json.loads(parameters['scene_json'])
    kind=scene.get('kind');values=scene.get('values')
    expected_len={'place':2,'compare':2,'order':3,'round':2,'estimate':3}
    if (kind not in expected_len or not isinstance(values,list) or len(values)!=expected_len[kind]
        or scene.get('id')!=parameters['question_id'] or scene.get('problem')!=parameters['prompt']
        or parameters['total_steps']!=5 or len(scene.get('rows',[]))!=3):
        raise ValueError('Decimal scene requires complete matching question data')
    numeric=values[:1] if kind in {'place','round'} else values[:2] if kind in {'compare','estimate'} else values
    if any(not isinstance(v,str) or not re.fullmatch(r'\d{1,3}\.\d{1,5}',v) for v in numeric):
        raise ValueError('Decimal operands must be bounded and include decimal digits')
    try: answer,rows,problem,check=solution(kind,values)
    except (ValueError,ArithmeticError) as exc:raise ValueError('Unsupported decimal values or place') from exc
    if any(scene.get(k)!=v for k,v in {'answer':answer,'rows':rows,'problem':problem,'memo':check}.items()):
        raise ValueError('Decimal scene disagrees with exact place-value arithmetic')
    family='decimal_columns' if kind in {'place','compare','order'} else 'decimal_rounding'
    if scene.get('visual_family')!=family:raise ValueError('Decimal visual family disagrees with task')


def _grade8_decimal_columns(parameters: dict) -> None:
    _grade8_decimal_scene(parameters)
    import json
    if json.loads(parameters['scene_json'])['kind'] not in {'place','compare','order'}:
        raise ValueError('Decimal columns require a place-value or comparison question')


def _grade8_decimal_rounding(parameters: dict) -> None:
    _grade8_decimal_scene(parameters)
    import json
    if json.loads(parameters['scene_json'])['kind'] not in {'round','estimate'}:
        raise ValueError('Decimal rounding requires a rounding or estimate question')


def _grade8_percentage_grid(parameters: dict) -> None:
    import json
    from fractions import Fraction
    from app.curriculum.grade8.percentage_math import answer
    scene=json.loads(parameters['scene_json'])
    values=scene.get('values',[])
    kind=scene.get('kind')
    if scene.get('id')!=parameters['question_id'] or scene.get('problem')!=parameters['prompt'] or parameters['total_steps']!=5 or len(scene.get('rows',[]))!=3 or kind not in {'convert','of','part','increase','decrease','change'}:
        raise ValueError('Percentage scene requires five authored question-specific states')
    if len(values)!=(1 if kind=='convert' else 2) or any(not isinstance(v,str) or not 0<Fraction(v)<=1000 for v in values):
        raise ValueError('Percentage values require bounded positive rational numbers')
    if scene.get('answer')!=answer(kind,values) or not all(isinstance(v,str) and v.strip() for v in scene['rows']):
        raise ValueError('Percentage answer or reasoning disagrees with exact arithmetic')


def _grade8_fraction_powers_context(parameters: dict) -> None:
    import json
    from app.curriculum.grade8.fractions_math import answer,value
    scene=json.loads(parameters["scene_json"])
    vals=scene.get('values')
    kind=scene.get('kind')
    if (scene.get('id')!=parameters['question_id'] or scene.get('problem')!=parameters['prompt']
        or kind not in {'square','cube','root','context'} or not isinstance(vals,list)
        or len(vals)!=(2 if kind=='context' else 1) or len(scene.get('rows',[]))!=3
        or parameters['total_steps']!=5):
        raise ValueError('Fraction power/context requires a complete matching scene')
    if any(not isinstance(v,str) or not 1<=len(v)<=12 or not 0<value(v)<=48 or value(v).denominator>144 for v in vals):
        raise ValueError('Fraction operands must be bounded positive rationals')
    if kind=='context':
        op=scene.get('operation')
        if op not in {'multiply','divide','add','subtract'} or not isinstance(scene.get('unit'),str) or not 1<=len(scene['unit'])<=20:
            raise ValueError('Fraction context requires supported operation and unit')
    else:
        op=scene.get('exponent')
        if op not in (2,3):raise ValueError('Fraction exponent must be 2 or 3')
    if scene.get('answer')!=answer(kind,vals,op):
        raise ValueError('Fraction power/context answer disagrees with exact arithmetic')
    if any(not isinstance(row,str) or not row.strip() for row in scene['rows']) or not isinstance(scene.get('memo'),str):
        raise ValueError('Fraction power/context requires authored explanation and verification')


def _grade8_integer_reasoning(parameters: dict) -> None:
    import json
    from app.curriculum.grade8.integer_evaluator import evaluate
    scene=json.loads(parameters["scene_json"])
    if (scene.get("id")!=parameters["question_id"] or scene.get("problem")!=parameters["prompt"]
        or len(scene.get("rows",[]))!=3 or len(scene.get("actions",[]))!=parameters["total_steps"]
        or parameters["total_steps"]!=5 or not isinstance(scene.get("memo"),str)):
        raise ValueError("Integer reasoning requires complete question-specific operations")
    if evaluate(scene["source_expression"])!=(scene.get("left_value") if "comparison_expression" in scene else scene.get("answer")):
        raise ValueError("Integer reasoning result does not match original expression")
    if "comparison_expression" in scene and scene.get("answer")!=("true" if scene.get("claim_true") else "false"):
        raise ValueError("Property answer must state the verified truth value")
    if "comparison_expression" in scene:
        if scene.get("model") not in {"commutative_add","commutative_mul","noncommutative_sub","associative_add","associative_mul","nonassociative_sub","distributive","false_distribution","additive_inverse","additive_identity","multiplicative_identity","zero_product","inverse_associative"}:
            raise ValueError("Unsupported property comparison")
        if (evaluate(scene["source_expression"])==evaluate(scene["comparison_expression"])) is not scene.get("claim_true"):
            raise ValueError("Property claim does not match the two evaluated sides")
    elif scene.get("model") not in {"temperature","bank","elevation","score"} or not isinstance(scene.get("start"),int) or not scene.get("unit"):
        raise ValueError("Context board requires its own starting value and unit")


def _grade8_integer_operations(parameters: dict) -> None:
    import json
    from app.curriculum.grade8.integer_evaluator import evaluate
    scene=json.loads(parameters["scene_json"])
    if (scene.get("id")!=parameters["question_id"] or scene.get("problem")!=parameters["prompt"]
        or scene.get("model") not in {"groups","pattern","sign_pattern","inverse","zero","factor_chain","powers","roots","mixed"}
        or not isinstance(scene.get("actions"),list) or not isinstance(scene.get("rows"),list)
        or len(scene["rows"])!=3 or len(scene["actions"])!=parameters["total_steps"]
        or not 5<=parameters["total_steps"]<=7):
        raise ValueError("Integer operation scene must match the question and its complete teaching states")
    if evaluate(scene["source_expression"])!=scene.get("answer"):
        raise ValueError("Integer operation answer disagrees with exact expression evaluation")
    if not isinstance(scene.get("memo"),str) or not scene["memo"]:
        raise ValueError("Integer operation requires a checked original-question memo")


def _grade8_integer_board(parameters: dict) -> None:
    import json
    scene=json.loads(parameters["scene_json"])
    if (scene.get("id")!=parameters["question_id"] or scene.get("problem")!=parameters["prompt"]
        or not isinstance(scene.get("actions"),list) or len(scene["actions"])!=parameters["total_steps"]
        or not 4<=parameters["total_steps"]<=7):
        raise ValueError("Integer question, source actions and displayed steps must match")
    axis=scene.get("axis")
    if not isinstance(axis,list) or len(axis)!=2 or any(type(v) is not int for v in axis) or not -100<=axis[0]<axis[1]<=100:
        raise ValueError("Signed axis must have two bounded ordered endpoints")
    if scene.get("model")=="integer_line":
        values=scene.get("values")
        if not isinstance(values,list) or not 1<=len(values)<=5 or any(type(v) is not int or not axis[0]<v<axis[1] for v in values):
            raise ValueError("Integer markers must lie on the given axis")
        decision=scene.get("decision")
        answer=(max(values) if decision in ("larger","greatest") else min(values) if decision in ("smaller","least") else
            -values[0] if decision=="opposite" and len(values)==1 else
            abs(values[1]-values[0]) if decision=="distance" and len(values)==2 else None)
        if answer is None or scene.get("answer")!=answer:
            raise ValueError("Signed order, opposite or distance answer does not match the markers")
    elif scene.get("model")=="integer_jumps":
        start,operations=scene.get("start"),scene.get("operations")
        if type(start) is not int or not isinstance(operations,list) or not 1<=len(operations)<=4:
            raise ValueError("Integer journey requires a starting value and bounded operations")
        path=[start]
        for operation in operations:
            if (not isinstance(operation,list) or len(operation)!=2 or operation[0] not in ("+","-")
                or type(operation[1]) is not int or not -50<=operation[1]<=50):
                raise ValueError("Every signed jump needs an operation and bounded integer")
            path.append(path[-1]+(operation[1] if operation[0]=="+" else -operation[1]))
        if (scene.get("path")!=path or scene.get("answer")!=path[-1]
            or parameters["total_steps"]!=len(operations)+3
            or any(not axis[0]<v<axis[1] for v in path)):
            raise ValueError("Integer jumps, final answer, and visible steps must agree")
    else:
        raise ValueError("Unsupported signed integer visual model")


def _grade8_whole_number_board(parameters: dict) -> None:
    import json
    import math
    scene=json.loads(parameters["scene_json"])
    if (scene.get("id")!=parameters["question_id"] or scene.get("problem")!=parameters["prompt"]
        or not 4<=parameters["total_steps"]<=8 or not isinstance(scene.get("actions"),list)
        or len(scene["actions"])!=parameters["total_steps"]):
        raise ValueError("Whole-number board ID, original question and step count must match")
    if scene.get("model")=="property":
        vals=scene.get("values")
        if not isinstance(vals,list) or len(vals)!=3 or any(type(v) is not int or not 0<=v<=1000 for v in vals):
            raise ValueError("Property board requires three bounded whole-number inputs")
        a,b,c=vals;kind=scene.get("kind")
        expected={"comm_add":lambda:a+b,"comm_mul":lambda:a*b,
            "assoc_add":lambda:a+b+c,"assoc_mul":lambda:a*b*c,
            "dist":lambda:a*(b+c),"add_identity":lambda:a,
            "mul_identity":lambda:a,"zero_div":lambda:"undefined"}
        if kind not in expected or scene.get("answer")!=expected[kind]():
            raise ValueError("Whole-number property and answer disagree")
        if kind=="add_identity" and b!=0 or kind=="mul_identity" and b!=1 or kind=="zero_div" and b!=0:
            raise ValueError("The identity or zero-divisor picture does not match its operands")
    elif scene.get("model")=="factor_tree":
        nums,factors=scene.get("numbers"),scene.get("factors")
        if not isinstance(nums,list) or not 1<=len(nums)<=3 or any(type(n) is not int or not 2<=n<=999 for n in nums):
            raise ValueError("Factor-tree roots must be bounded whole numbers")
        if not isinstance(factors,list) or len(factors)!=len(nums):
            raise ValueError("Each factor tree needs its own prime leaves")
        if parameters["total_steps"]!=3+max(len(leaves)-1 for leaves in factors):
            raise ValueError("Every composite split requires a visible teaching step")
        def prime(p):return p>=2 and all(p%d for d in range(2,math.isqrt(p)+1))
        for root,leaves in zip(nums,factors):
            if not isinstance(leaves,list) or not leaves or any(type(v) is not int or not prime(v) for v in leaves) or math.prod(leaves)!=root:
                raise ValueError("Prime leaves must multiply to the original root")
        kind=scene.get("kind")
        expected=max(factors[0]) if kind=="largest_prime" else math.gcd(*nums) if kind=="hcf" else math.lcm(*nums) if kind=="lcm" else None
        if expected is None or scene.get("answer")!=expected:
            raise ValueError("Factor-tree HCF/LCM answer disagrees with the original roots")
    else:
        raise ValueError("Unsupported whole-number visual model")


def _grade10_stat_board(parameters: dict, number: int) -> None:
    """Validate the authored dataset, answer and visual stages together."""
    import json
    from pathlib import Path
    scene=json.loads(parameters['scene_json']);qid=parameters.get('question_id')
    if (scene.get('id')!=qid or scene.get('problem')!=parameters.get('prompt')
        or scene.get('lesson')!=number or len(scene.get('actions',[]))!=parameters.get('total_steps')
        or len(scene['actions'])!=5 or scene['actions'][-1]!=scene.get('check')
        or scene.get('visual',{}).get('family')!='grade10_statistics'):
        raise ValueError('Statistics question, dataset and stages disagree')
    source=Path(__file__).resolve().parents[1]/'curriculum/grade10/generated'/f'statistics_{number:02}.json'
    authored=next((q for q in json.loads(source.read_text(encoding='utf-8'))['worked'] if q['id']==qid),None)
    if scene!=authored or ''.join(scene['answer'].split()) not in ''.join(scene['check'].split()):
        raise ValueError('Statistics answer, data or stages differ from authored source')

def _grade10_fn_board(parameters: dict, number: int) -> None:
    """Verify function family, coefficients, key features and stages from the authored source."""
    import json
    from pathlib import Path
    scene=json.loads(parameters['scene_json']);qid=parameters.get('question_id')
    if (scene.get('id')!=qid or scene.get('problem')!=parameters.get('prompt')
        or scene.get('lesson')!=number or len(scene.get('actions',[]))!=parameters.get('total_steps')
        or len(scene['actions'])!=5 or scene['actions'][-1]!=scene.get('check')
        or scene.get('visual',{}).get('family')!='grade10_functions'):
        raise ValueError('Function question, graph and stages disagree')
    source=Path(__file__).resolve().parents[1]/'curriculum/grade10/generated'/f'functions_{number:02}.json'
    authored=next((q for q in json.loads(source.read_text(encoding='utf-8'))['worked'] if q['id']==qid),None)
    if scene!=authored or ''.join(scene['answer'].split()) not in ''.join(scene['check'].split()):
        raise ValueError('Function answer, coefficients or stages differ from authored source')

def _grade10_ag_board(parameters: dict, number: int) -> None:
    """Match exact Cartesian points and every stage to the authored problem."""
    import json
    from pathlib import Path
    scene=json.loads(parameters['scene_json']);qid=parameters.get('question_id')
    if (scene.get('id')!=qid or scene.get('problem')!=parameters.get('prompt')
        or scene.get('lesson')!=number or len(scene.get('actions',[]))!=parameters.get('total_steps')
        or len(scene['actions'])!=5 or scene['actions'][-1]!=scene.get('check')
        or scene.get('visual',{}).get('family')!='grade10_analytical'):
        raise ValueError('Analytical geometry question, graph and stages disagree')
    source=Path(__file__).resolve().parents[1]/'curriculum/grade10/generated'/f'analytical_{number:02}.json'
    authored=next((q for q in json.loads(source.read_text(encoding='utf-8'))['worked'] if q['id']==qid),None)
    if scene!=authored or ''.join(scene['answer'].split()) not in ''.join(scene['check'].split()):
        raise ValueError('Coordinate answer, givens or stages differ from authored source')

def _grade10_euc_board(parameters: dict, number: int) -> None:
    """Match every marked construction and teaching action to authored source."""
    import json
    from pathlib import Path
    scene=json.loads(parameters['scene_json']);qid=parameters.get('question_id')
    if (scene.get('id')!=qid or scene.get('problem')!=parameters.get('prompt')
        or scene.get('lesson')!=number or len(scene.get('actions',[]))!=parameters.get('total_steps')
        or len(scene['actions'])!=5 or scene['actions'][-1]!=scene.get('check')
        or scene.get('visual',{}).get('family')!='grade10_euclidean'):
        raise ValueError('Euclidean geometry question, diagram and stages disagree')
    source=Path(__file__).resolve().parents[1]/'curriculum/grade10/generated'/f'euclidean_{number:02}.json'
    authored=next((q for q in json.loads(source.read_text(encoding='utf-8'))['worked'] if q['id']==qid),None)
    if scene!=authored or ''.join(scene['answer'].split()) not in ''.join(scene['check'].split()):
        raise ValueError('Euclidean answer, givens or stages differ from authored source')

def _grade10_trig_board(parameters: dict, number: int) -> None:
    """Reject changed angle, side, signs, answer or teaching stages."""
    import json
    from pathlib import Path
    scene=json.loads(parameters['scene_json']);qid=parameters.get('question_id')
    if (scene.get('id')!=qid or scene.get('problem')!=parameters.get('prompt')
        or scene.get('lesson')!=number or len(scene.get('actions',[]))!=parameters.get('total_steps')
        or len(scene['actions'])!=5 or scene['actions'][-1]!=scene.get('check')
        or scene.get('visual',{}).get('family')!='grade10_trigonometry'):
        raise ValueError('Grade 10 trigonometry question, visual and stages disagree')
    source=Path(__file__).resolve().parents[1]/'curriculum/grade10/generated'/f'trig_{number:02}.json'
    authored=next((q for q in json.loads(source.read_text(encoding='utf-8'))['worked'] if q['id']==qid),None)
    if scene!=authored or scene['answer'] not in scene['check']:
        raise ValueError('Trigonometry answer, angle or timeline differs from authored source')

def _grade10_eei_board(parameters: dict, number: int) -> None:
    """Verify the numerical model and every answer against the authored source."""
    import json
    from pathlib import Path
    scene=json.loads(parameters['scene_json'])
    qid=parameters.get('question_id')
    if (scene.get('id')!=qid or scene.get('problem')!=parameters.get('prompt')
        or scene.get('lesson')!=number or len(scene.get('actions',[]))!=parameters.get('total_steps')
        or len(scene['actions'])!=5 or scene['actions'][-1]!=scene.get('check')
        or scene.get('visual',{}).get('family')!='grade10_equations'):
        raise ValueError('Grade 10 equation source, question and stages disagree')
    # The generated pack is immutable runtime evidence; reject any visual, step,
    # answer, or prompt that has diverged from the exact authored question.
    source=Path(__file__).resolve().parents[1]/'curriculum/grade10/generated'/f'eei_{number:02}.json'
    authored=next((q for q in json.loads(source.read_text(encoding='utf-8'))['worked'] if q['id']==qid),None)
    if scene!=authored or scene['answer'] not in scene['check']:
        raise ValueError('Grade 10 equation answer, visual or timeline differs from the authored source')

def _grade10_algebra_board(parameters: dict, number: int) -> None:
    """Check that the illustrated factors and numerical results agree with the source."""
    import json,math
    scene=json.loads(parameters['scene_json']);v=scene.get('visual',{}).get('values',{})
    if (scene.get('id')!=parameters['question_id'] or scene.get('problem')!=parameters['prompt']
        or scene.get('lesson')!=number or scene.get('visual',{}).get('family')!='grade10_expressions'
        or v.get('lesson')!=number or len(scene.get('actions',[]))!=5
        or parameters['total_steps']!=5 or scene['actions'][-1]!=scene.get('check')):
        raise ValueError('Grade 10 algebra source, question and stages disagree')
    a,b,sign=v.get('a'),v.get('b'),v.get('sign')
    if any(type(x) is not int or abs(x)>100 or x==0 for x in (a,b,sign)) or sign not in (-1,1):
        raise ValueError('Invalid algebra parameters')
    if number in (1,2):
        rad=v.get('radicand');lo=v.get('lower');hi=v.get('upper')
        if type(rad) is not int or type(lo) is not int or type(hi) is not int or hi!=lo+1 or not (lo*lo<=rad<hi*hi):
            raise ValueError('Invalid surd interval')
        if number==1:
            if v.get('kind')=='rational' and rad==lo*lo:expected=f'rational; √{rad} = {lo}'
            elif v.get('kind')=='irrational' and lo*lo<rad<hi*hi:expected=f'irrational; {lo} < √{rad} < {hi}'
            else:raise ValueError('Incorrect rational classification')
        else:
            precision=v.get('precision')
            if precision not in (1,2) or v.get('decimal')!=f'{math.sqrt(rad):.{precision}f}':raise ValueError('Invalid rounded surd')
            expected=f'√{rad} ≈ {v["decimal"]}'
    elif number==3:
        d,t=v.get('d'),v.get('t');co=v.get('coefficients')
        if type(d) is not int or type(t) is not int or co!={'3':1,'2':a+d,'1':t+a*d,'0':a*t}:
            raise ValueError('Invalid expansion coefficients')
        def term(power,value):
            core=('x' if abs(value)==1 and power else str(abs(value)))+('²' if power==2 else '³' if power==3 else 'x' if power==1 and abs(value)!=1 else '')
            return str(abs(value)) if power==0 else core
        expected=''
        for power,value in ((3,1),(2,a+d),(1,t+a*d),(0,a*t)):
            if value:
                expected+=((' + ' if value>0 else ' − ') if expected else ('−' if value<0 else ''))+term(power,value)
        if str(co['0']) not in scene['check']:raise ValueError('Expansion check inconsistent')
    elif number==4:
        d=v.get('d');co=v.get('coefficients')
        if type(d) is not int or co!={'2':1,'1':a+d,'0':a*d}:raise ValueError('Invalid factorisation coefficients')
        expected=f'(x + {a})(x {"+" if d>=0 else "−"} {abs(d)})'
    elif number==5:
        cube=v.get('cube');minus=v.get('kind')=='difference'; middle=v.get('middle')
        if cube!=b**3 or v.get('kind') not in ('sum','difference') or middle!=(b if minus else -b):raise ValueError('Invalid cube identity')
        first=f'(x {"−" if minus else "+"} {b})';second=f'(x² {"+" if minus else "−"} {b}x + {b*b})';expected=first+second
    elif number==6:
        cube=v.get('cube');minus=sign<0;excluded=b if minus else -b
        first=f'(x {"−" if minus else "+"} {b})';second=f'(x² {"+" if minus else "−"} {b}x + {b*b})'
        if (cube!=b**3 or v.get('denominator')!=f'(x³ {"−" if minus else "+"} {cube})'
            or v.get('first')!=first or v.get('second')!=second or v.get('excluded')!=excluded
            or v.get('kind') not in ('combine','simplify')):raise ValueError('Invalid fraction factor or restriction')
        operator=v.get('operator','+')
        if operator not in ('+','−'):raise ValueError('Invalid fraction operation')
        expected=f'{(1-a if operator=="−" else 1+a) if v["kind"]=="combine" else 1}/{first}; x ≠ {excluded}'
    else:raise ValueError('Unsupported Grade 10 algebra lesson')
    if scene.get('answer')!=expected or (expected not in scene['check'] and expected.replace(';', ',') not in scene['check'] and number not in (1,2)):
        raise ValueError('Algebra answer does not match its question and visual')

def _grade9_transform_board(parameters: dict, number: int) -> None:
    """Reject inconsistent original/image pairs and mismatched source questions."""
    import json
    scene=json.loads(parameters['scene_json']); visual=scene.get('visual',{});v=visual.get('values',{})
    if (scene.get('id')!=parameters['question_id'] or scene.get('problem')!=parameters['prompt']
        or scene.get('lesson')!=number or visual.get('family')!='transformation'
        or v.get('lesson')!=number or v.get('model')!='coordinate_transform'
        or len(scene.get('actions',[]))!=5 or parameters['total_steps']!=5
        or scene['actions'][-1]!=scene.get('check')):
        raise ValueError('Transformation source, question and stages disagree')
    original=v.get('original');image=v.get('image');centre=v.get('centre')
    def pair(point):
        return isinstance(point,(list,tuple)) and len(point)==2 and all(type(x) in (int,float) and -100<=x<=100 for x in point)
    if (not isinstance(original,list) or len(original)!=3 or not all(map(pair,original))
        or not pair(centre) or not isinstance(image,list) or len(image)!=3 or not all(map(pair,image))
        or len({tuple(p) for p in original})!=3):
        raise ValueError('Transformation vertices or centre are invalid')
    kind=v.get('kind');dx=v.get('dx');dy=v.get('dy');k=v.get('factor');cx,cy=centre
    if kind not in ('translate','reflect_x','reflect_y','reflect_diag','rotate_ccw','rotate_cw','enlarge') or type(dx) is not int or type(dy) is not int or type(k) not in (int,float) or k not in (0.5,1,2):
        raise ValueError('Unsupported transformation rule')
    result=[]
    for x,y in original:
        if kind=='translate':result.append([x+dx,y+dy])
        elif kind=='reflect_x':result.append([x,-y])
        elif kind=='reflect_y':result.append([-x,y])
        elif kind=='reflect_diag':result.append([y,x])
        elif kind=='rotate_ccw':result.append([cx-(y-cy),cy+(x-cx)])
        elif kind=='rotate_cw':result.append([cx+(y-cy),cy-(x-cx)])
        else:result.append([cx+k*(x-cx),cy+k*(y-cy)])
    if result!=image or (number==6 and (kind!='enlarge' or v.get('original_area')!=(original[1][0]-original[0][0])*(original[2][1]-original[0][1])/2)):
        raise ValueError('Transformation image contradicts original coordinates')
    def fmt(points):return ', '.join(f'{label}({x:g}, {y:g})' for label,(x,y) in zip('ABC',points))
    shown=fmt(image).replace('A(','A′(').replace('B(','B′(').replace('C(','C′(')
    expected=(f'{shown}; perimeter factor {k:g}; area factor {k*k:g}' if number==6 else f"{v['rule']}; {shown}" if number in (5,7) else shown)
    if scene.get('answer')!=expected or shown not in scene['check'] or any(shown in a for a in scene['actions'][:4]):
        raise ValueError('Transformation answer or verification disagrees with image')

def _grade9_surface_board(parameters: dict, number: int) -> None:
    """Recompute measurements from pictured givens before a visual is accepted."""
    import json
    from fractions import Fraction
    scene=json.loads(parameters['scene_json']);v=scene.get('visual',{}).get('values',{})
    if (scene.get('id')!=parameters['question_id'] or scene.get('problem')!=parameters['prompt']
        or scene.get('lesson')!=number or scene.get('visual',{}).get('family')!='surface_volume'
        or v.get('lesson')!=number or len(scene.get('actions',[]))!=5 or parameters['total_steps']!=5
        or scene['actions'][-1]!=scene.get('check')):
        raise ValueError('Measurement source, question and stages disagree')
    def positive(key):
        value=v.get(key)
        if type(value) is not int or not 0<value<10000:raise ValueError(f'Invalid measurement {key}')
        return value
    if number==1:
        L,W,H=(positive(x) for x in ('length','width','height'));area=2*(L*W+L*H+W*H)
        cube=v.get('shape')=='cube';valid=(v.get('model')=='box_net' and v.get('shape') in ('cube','rectangular prism')
            and (not cube or L==W==H) and v.get('surface_area')==area)
        expected=f'surface area = {area} cm²'
        expected_problem=(f'A closed cube has edge {L} cm.' if cube else f'A closed rectangular prism has length {L} cm, width {W} cm and height {H} cm.')+' Draw its net and calculate its total surface area.'
    elif number==2:
        L,W,H=(positive(x) for x in ('length','width','height'));volume=L*W*H;litres=Fraction(volume,1000)
        valid=(v.get('model')=='box_layers' and v.get('volume')==volume and v.get('capacity_num')==litres.numerator and v.get('capacity_den')==litres.denominator)
        expected=f'volume = {volume} cm³; capacity = {litres} L'
        expected_problem=f'A water tank is a rectangular prism with internal length {L} cm, width {W} cm and height {H} cm. Find its volume in cm³ and capacity in litres.'
    elif number==3:
        B,T,C,length=(positive(x) for x in ('base','altitude','hypotenuse','length'));triangle=B*T//2;volume=triangle*length;area=2*triangle+(B+T+C)*length
        valid=(v.get('model')=='tri_prism' and B*T%2==0 and B*B+T*T==C*C and v.get('triangle_area')==triangle and v.get('volume')==volume and v.get('surface_area')==area)
        expected=f'volume = {volume} cm³; surface area = {area} cm²'
        expected_problem=f'A right triangular prism has perpendicular triangle sides {B} cm and {T} cm, third side {C} cm, and prism length {length} cm. Find its volume and total surface area.'
    elif number==4:
        r,h=(positive(x) for x in ('radius','height'));volume=r*r*h;area=2*r*(r+h)
        valid=(v.get('model')=='cylinder_net' and v.get('diameter')==2*r and v.get('volume_pi')==volume and v.get('surface_area_pi')==area)
        expected=f'volume = {volume}π cm³; surface area = {area}π cm²'
        expected_problem=f'A closed cylinder has radius {r} cm and height {h} cm. Give its volume and total surface area exactly in terms of π.'
    elif number==5:
        L,W,H=(positive(x) for x in ('length','width','height'));original=L*W*H;kind=v.get('kind');litres=Fraction(original,1000)
        valid=(v.get('model')=='scale_convert' and v.get('original')==original and v.get('litres_num')==litres.numerator
            and v.get('litres_den')==litres.denominator and kind in ('one_axis','all_axes','litres'))
        if kind=='one_axis':
            factor=2;expected=f'new volume = {factor*original} cm³; factor = {factor}'
            expected_problem=f'A rectangular prism measures {L} cm × {W} cm × {H} cm. Only its length is doubled. Find the new volume and the factor of change.'
        elif kind=='all_axes':
            factor=8;expected=f'new volume = {factor*original} cm³; factor = {factor}'
            expected_problem=f'A rectangular prism measures {L} cm × {W} cm × {H} cm. Every dimension is doubled. Find the new volume and the factor of change.'
        else:
            factor=1;expected=f'capacity = {litres} L'
            expected_problem=f'A rectangular tank measures {L} cm × {W} cm × {H} cm inside. Convert its capacity from cm³ to litres.'
        valid=valid and v.get('factor')==factor and v.get('new_volume')==factor*original
    else:
        kind=v.get('kind');H=positive('height');valid=v.get('model')=='applied_error' and kind in ('open_box','triangle','cylinder','double_all','convert')
        if kind=='cylinder':
            r=positive('radius');volume=r*r*H
            valid=valid and v.get('diameter')==2*r and v.get('correct_value')==volume
            expected=f'first error: used diameter; volume = {volume}π cm³'
            expected_problem=f'A closed cylinder has diameter {2*r} cm and height {H} cm. A learner squares the diameter as the radius. Find the first error and correct volume in terms of π.'
        else:
            L,W=(positive(x) for x in ('length','width'));original=L*W*H
            if kind=='open_box':
                area=L*W+2*L*H+2*W*H;valid=valid and v.get('correct_value')==area
                expected=f'first error: included a top; material area = {area} cm²'
                expected_problem=f'An open-top rectangular box has length {L} cm, width {W} cm, height {H} cm. A learner includes a top face. Find the first error and the required material area.'
            elif kind=='triangle':
                B,T,C=(positive(x) for x in ('base','altitude','hypotenuse'));length=positive('length');area=B*T//2;volume=area*length
                valid=valid and B*T%2==0 and B*B+T*T==C*C and length==H and v.get('triangle_area')==area and v.get('correct_value')==volume
                expected=f'first error: omitted ½; volume = {volume} cm³'
                expected_problem=f'A triangular prism has a right-triangle end with legs {B} cm and {T} cm, and length {length} cm. A learner omits ½. Find the first error and correct volume.'
            elif kind=='double_all':
                volume=8*original;valid=valid and v.get('correct_value')==volume
                expected=f'first error: used factor 2; new volume = {volume} cm³'
                expected_problem=f'A rectangular prism has dimensions {L} cm × {W} cm × {H} cm. A learner doubles its volume when all dimensions double. Find the first error and new volume.'
            else:
                litres=Fraction(original,1000);valid=valid and v.get('correct_value')==original
                expected=f'first error: divided by 100; capacity = {litres} L'
                expected_problem=f'A rectangular container measures {L} cm × {W} cm × {H} cm inside. A learner divides cm³ by 100 to obtain litres. Find the first error and correct capacity.'
            if kind=='convert':
                litres=Fraction(original,1000)
                valid=valid and v.get('litres_num')==litres.numerator and v.get('litres_den')==litres.denominator
    if not valid or scene.get('problem')!=expected_problem or scene.get('answer')!=expected:
        raise ValueError('Measurement answer or pictured dimensions disagree with question')

def _grade9_whole_board(parameters: dict, family: str) -> None:
    import json
    import math
    scene=json.loads(parameters['scene_json'])
    if (scene.get('id')!=parameters['question_id'] or scene.get('problem')!=parameters['prompt']
        or scene.get('actions') is None or len(scene['actions'])!=parameters['total_steps']
        or not 3<=parameters['total_steps']<=18):
        raise ValueError('Grade 9 source scene, question and step count disagree')
    if family.startswith('solid_'):
        number=int(family.rsplit('_',1)[-1]);v=scene.get('visual',{}).get('values',{})
        if (scene.get('lesson')!=number or scene.get('visual',{}).get('family')!='solids'
            or v.get('lesson')!=number or len(scene['actions'])!=5
            or scene['actions'][-1]!=scene.get('check')):
            raise ValueError('Solid question, visual and step sequence disagree')
        solids={'tetrahedron':(4,6,4,'triangles'),'cube':(6,12,8,'squares'),
                'octahedron':(8,12,6,'triangles'),'dodecahedron':(12,30,20,'pentagons'),
                'icosahedron':(20,30,12,'triangles')}
        nets={'cube':(6,'6 equal squares','one matching square','5 equal squares'),
              'rectangular prism':(6,'6 rectangles in three matching pairs','one matching rectangle','5 rectangles'),
              'triangular prism':(5,'3 rectangles and 2 matching triangles','one matching triangle','3 rectangles and 1 triangle'),
              'square pyramid':(5,'1 square and 4 matching triangles','one matching triangle','1 square and 3 triangles'),
              'cylinder':(3,'1 rectangle and 2 matching circles','one matching circle','1 rectangle and 1 circle')}
        if number==1:
            shape=v.get('shape');valid=shape in solids and v.get('model')=='platonic'
            if valid:
                faces,edges,vertices,face_shape=solids[shape];target=v.get('target')
                valid=(target in ('faces','edges','vertices') and v.get('faces')==faces
                       and v.get('edges')==edges and v.get('vertices')==vertices
                       and v.get('face_shape')==face_shape and faces+vertices==edges+2
                       and all(str(x) in scene['problem'] for x in (shape,face_shape)))
                expected=f'{target} = '+str({'faces':faces,'edges':edges,'vertices':vertices}[target]) if target in ('faces','edges','vertices') else ''
            else:expected=''
        elif number==2:
            kind=v.get('model');context=v.get('context');valid=(kind in ('sphere','cylinder','compare')
                 and type(context) is str and context in scene['problem'])
            expected={'sphere':'sphere: 0 flat faces, 1 curved surface, 0 edges, 0 vertices',
                      'cylinder':'cylinder: 2 flat circular faces, 1 curved surface, 2 curved edges, 0 vertices',
                      'compare':'cylinder: circular flat faces; sphere: no edges'}.get(kind,'')
        else:
            shape=v.get('shape');valid=shape in nets and type(v.get('scale')) is int and 2<=v['scale']<=100
            if valid:
                count,parts,missing,observed=nets[shape]
                valid=(v.get('model')==('net' if number==3 else 'net_error')
                    and v.get('faces')==count and v.get('parts')==parts
                    and shape in scene['problem'] and str(v['scale']) in scene['problem'])
                if number==4:valid=valid and v.get('missing')==missing and v.get('observed')==observed and observed in scene['problem']
                else:valid=valid and v.get('missing') is False
                expected=(f'{shape} net: {parts}' if number==3 else f'missing {missing}; complete net: {parts}')
            else:expected=''
        if not valid or scene.get('answer')!=expected:
            raise ValueError('Solid answer or pictured faces disagree with the question')
        return
    if family.startswith('probability_'):
        from fractions import Fraction
        number=int(family.rsplit('_',1)[-1]);v=scene.get('visual',{}).get('values',{})
        if (scene.get('lesson')!=number or scene.get('visual',{}).get('family')!='probability'
            or v.get('lesson')!=number or len(scene['actions'])!=5
            or scene['actions'][-1]!=scene.get('check')):
            raise ValueError('Probability source, event and stages disagree')
        def positive(key):
            value=v.get(key)
            if type(value) is not int or not 0<value<10000:raise ValueError(f'Invalid probability {key}')
            return value
        if number==1:
            outcomes=v.get('outcomes');valid=isinstance(outcomes,list) and 6<=len(outcomes)<200 and outcomes==list(range(1,len(outcomes)+1))
            total=len(outcomes) if valid else 0;fav=total//3
            expected=f'sample space size = {total}; P(multiple of 3) = {Fraction(fav,total)}' if valid else ''
            valid=valid and v.get('model')=='sample_grid' and v.get('favourable')==fav and str(total) in scene['problem']
        elif number==2:
            table=v.get('table');valid=(isinstance(table,list) and len(table)==2 and all(isinstance(row,list) and len(row)==2 for row in table)
                and all(type(x) is int and 0<x<10000 for row in table for x in row))
            if valid:
                a,b=table[0];c,d=table[1];expected=f'P(bus | Grade 9) = {Fraction(a,a+b)}'
                valid=(v.get('model')=='two_way' and v.get('row_total')==a+b and v.get('column_total')==a+c
                    and v.get('grand_total')==a+b+c+d and all(str(x) in scene['problem'] for x in (a,b,c,d)))
            else:expected=''
        elif number==3:
            red,blue=positive('red'),positive('blue');total=red+blue;fraction=Fraction(red*(red-1),total*(total-1))
            expected=f'P(red then red) = {fraction}'
            valid=(v.get('model')=='tree' and red>1 and v.get('first_red_num')==red and v.get('first_red_den')==total
                and v.get('second_red_num')==red-1 and v.get('second_red_den')==total-1
                and v.get('prob_num')==fraction.numerator and v.get('prob_den')==fraction.denominator
                and all(str(x) in scene['problem'] for x in (red,blue)))
        elif number==4:
            trials,heads=positive('trials'),positive('heads');expected=f'experimental frequency = {Fraction(heads,trials)}; predicted heads in 50 = 25'
            valid=(v.get('model')=='relative_frequency' and heads<trials and v.get('tails')==trials-heads
                and v.get('predicted_heads')==25 and all(str(x) in scene['problem'] for x in (trials,heads)))
        else:
            total=positive('sectors');fav=total//3;fraction=Fraction(fav,2*total)
            expected=f'first error: added for AND; correct probability = {fraction}'
            valid=(v.get('model')=='joint_grid' and v.get('coin_outcomes')==['H','T']
                and v.get('multiples_of_three')==fav and v.get('favourable_pairs')==fav and v.get('total_pairs')==2*total
                and str(total) in scene['problem'])
        if not valid or scene.get('answer')!=expected:raise ValueError('Probability answer or pictured outcomes disagree with question')
        return
    if family.startswith('data_'):
        from fractions import Fraction
        n=int(family.rsplit('_',1)[-1]);v=scene.get('visual',{}).get('values',{})
        if (scene.get('lesson')!=n or scene.get('visual',{}).get('family')!='data'
            or v.get('lesson')!=n or len(scene['actions'])!=5
            or scene['actions'][-1]!=scene.get('check')):
            raise ValueError('Data scene, source and stages disagree')
        def positive(key):
            value=v.get(key)
            if type(value) is not int or not 0<value<10000:raise ValueError(f'Invalid data {key}')
            return value
        if n==1:
            a,b=positive('population'),positive('sample')
            expected=f'population = {a}; sample = {b}'
            valid=v.get('model')=='survey' and b<a and str(a) in scene['problem'] and str(b) in scene['problem']
        elif n==2:
            a,b=positive('young'),positive('old')
            expected='source: school register; stratified survey: 9 junior, 3 senior; volunteer sample biased'
            valid=(v.get('model')=='stratified' and a==3*b and v.get('young_pick')==9 and v.get('old_pick')==3
                and v.get('convenience_young')==12 and v.get('convenience_old')==0
                and str(a) in scene['problem'] and str(b) in scene['problem'])
        elif n in (3,6):
            counts=v.get('counts');expected=f'total = {sum(counts)}; '+('mode = 2' if n==3 else 'modal interval = 10–19 min') if isinstance(counts,list) and all(type(x) is int for x in counts) else ''
            valid=(len(counts)==3 and all(0<x<1000 for x in counts) and counts[1]>max(counts[0],counts[2])
                and v.get('total')==sum(counts) and v.get('model')==('frequency' if n==3 else 'histogram')
                and v.get('categories' if n==3 else 'intervals')==(['1','2','3'] if n==3 else ['0–9','10–19','20–29'])
                and v.get('mode' if n==3 else 'modal_interval')==('2' if n==3 else '10–19')) if isinstance(counts,list) else False
        elif n==4:
            values=v.get('values');valid=isinstance(values,list) and len(values)==7 and all(type(x) is int and 0<x<10000 for x in values) and values==sorted(values)
            if valid:
                total=sum(values);mean=total/7;span=values[-1]-values[0]
                expected=f'mean ≈ {mean:.2f}; median = {values[3]}; range = {span}; possible outlier = {values[-1]}'
                valid=(v.get('model')=='dotplot' and v.get('total')==total and v.get('median')==values[3]
                    and v.get('mean_rounded')==f'{mean:.2f}' and v.get('range')==span and v.get('outlier')==values[-1]
                    and all(str(x) in scene['problem'] for x in values))
            else:expected=''
        elif n==5:
            a,b=v.get('series_a'),v.get('series_b');valid=(isinstance(a,list) and isinstance(b,list) and len(a)==len(b)==2
                and all(type(x) is int and 0<x<10000 for x in a+b) and a[1]>a[0] and b[1]>b[0] and a[1]-a[0]>b[1]-b[0])
            expected=f'A gains {(a[1]-a[0])-(b[1]-b[0])} more members' if valid else ''
            valid=valid and v.get('model')=='double_bar' and v.get('gain_a')==a[1]-a[0] and v.get('gain_b')==b[1]-b[0] and all(str(x) in scene['problem'] for x in a+b)
        elif n==7 and v.get('model')=='pie':
            counts=v.get('counts');valid=isinstance(counts,list) and len(counts)==3 and all(type(x) is int and 0<x<10000 for x in counts)
            if valid:
                total=sum(counts);angle=Fraction(360*counts[0],total)
                expected=f'total = {total}; walking angle = {angle}°'
                valid=v.get('labels')==['walk','bus','car'] and v.get('total')==total and v.get('walk_angle_num')==angle.numerator and v.get('walk_angle_den')==angle.denominator and all(str(x) in scene['problem'] for x in counts)
            else:expected=''
        elif n==7 and v.get('model')=='scatter':
            points=v.get('points');valid=isinstance(points,list) and len(points)==5 and all(isinstance(p,list) and len(p)==2 and all(type(x) is int for x in p) for p in points)
            k=points[0][1]-2 if valid else 0
            expected=f'positive association; predicted score at 6 h = {12+k}'
            valid=valid and points==[[x,2*x+k] for x in range(1,6)] and v.get('prediction')==12+k
        elif n==8:
            a,b,baseline=positive('first'),positive('second'),positive('truncated_baseline')
            expected=f'difference = 6; increase ≈ {600/a:.2f}%; truncated axis exaggerates change'
            valid=(v.get('model')=='misleading_bar' and b==a+6 and baseline==a-5 and v.get('difference')==6
                and v.get('percent')==f'{600/a:.2f}' and all(str(x) in scene['problem'] for x in (a,b,baseline)))
        else:expected='';valid=False
        if not valid or scene.get('answer')!=expected:raise ValueError('Data calculation, source or chart disagrees with question')
        return
    if family.startswith('area_'):
        number=int(family.rsplit('_',1)[-1]);visual=scene.get('visual',{});v=visual.get('values',{})
        if (scene.get('lesson')!=number or visual.get('family')!='area' or v.get('lesson')!=number
            or len(scene.get('actions',[]))!=5 or scene['actions'][-1]!=scene.get('check')):
            raise ValueError('Area scene, five stages and original question must agree')
        def integer(key):
            value=v.get(key)
            if type(value) is not int or not 0<value<10000:raise ValueError(f'Invalid area {key}')
            return value
        L,W=integer('length'),integer('width')
        if number==1:
            perimeter=2*(L+W);area=L*W
            valid=(v.get('model')=='rectangle_units' and v.get('length_mm')==10*L and v.get('area')==area and v.get('perimeter')==perimeter
                and scene['answer']==f'P = {perimeter} cm; A = {area} cm²')
        elif number==2:
            cut_w,cut_h=integer('cut_width'),integer('cut_height');area=L*W-cut_w*cut_h;perimeter=2*(L+W)
            valid=(v.get('model')=='l_shape' and cut_w<L and cut_h<W and v.get('area')==area and v.get('perimeter')==perimeter
                and scene['answer']==f'A = {area} cm²; P = {perimeter} cm')
        elif number==3:
            radius=integer('radius');valid=(v.get('model')=='circle' and v.get('diameter')==2*radius and v.get('circumference_coefficient')==2*radius
                and v.get('area_coefficient')==radius*radius and scene['answer']==f'd = {2*radius} cm; C = {2*radius}π cm ≈ {math.pi*2*radius:.2f} cm; A = {radius*radius}π cm² ≈ {math.pi*radius*radius:.2f} cm²')
        elif number==4:
            k=integer('factor');mode=v.get('mode')
            new_l=L*(k if mode in ('both','length_only') else 1);new_w=W*(k if mode in ('both','width_only') else 1)
            valid=(v.get('model')=='scaled_rectangle' and mode in {'both','length_only','width_only'} and k==2
                and v.get('scaled_length')==new_l and v.get('scaled_width')==new_w
                and v.get('old_perimeter')==2*(L+W) and v.get('old_area')==L*W
                and v.get('new_perimeter')==2*(new_l+new_w) and v.get('new_area')==new_l*new_w
                and scene['answer']==f'P = {2*(new_l+new_w)} cm; A = {new_l*new_w} cm²')
        else:
            path=integer('path');outer_l,outer_w=L+2*path,W+2*path;area=outer_l*outer_w-L*W;fence=2*(outer_l+outer_w)
            valid=(v.get('model')=='garden_path' and v.get('outer_length')==outer_l and v.get('outer_width')==outer_w
                and v.get('path_area')==area and v.get('fence')==fence and scene['answer']==f'path = {area} m²; fence = {fence} m')
        if not valid:raise ValueError('Area measure, unit or figure disagrees with the question')
        return
    if family.startswith('shapes_'):
        number=int(family.rsplit('_',1)[-1]);visual=scene.get('visual',{});v=visual.get('values',{})
        if (scene.get('lesson')!=number or visual.get('family')!='shapes' or v.get('lesson')!=number
            or len(scene.get('actions',[]))!=5 or scene['actions'][-1]!=scene.get('check')
            or not isinstance(scene.get('answer'),str)):
            raise ValueError('Shape diagram, question and five reasoning stages must agree')
        def integer(key):
            value=v.get(key)
            if type(value) is not int or not 0<value<5000:raise ValueError(f'Invalid shape {key}')
            return value
        target=integer('target')
        if number==1:
            model=v.get('model')
            if model=='isosceles':
                apex=integer('apex');valid=apex<180 and 2*target+apex==180 and scene['answer']==f'∠B = {target}°'
            elif model=='equilateral':
                valid=integer('side')<100 and target==60 and scene['answer']=='∠B = 60°'
            elif model=='right':
                given=integer('given');valid=integer('side')<100 and given<90 and given+target==90 and scene['answer']==f'∠C = {target}°'
            else:valid=False
        elif number in (7,8):
            apex=integer('apex');valid=apex<180 and 2*target+apex==180 and scene['answer']==(f'x = {target}°' if number==7 else f'∠B = {target}°')
            if number==8:valid=valid and v.get('claimed')==180-apex
        elif number==2:
            left,right=integer('left'),integer('right');valid=left+right==target<180 and scene['answer']==f'∠ACD = {target}°'
        elif number==3:
            given=integer('given');model=v.get('model');side={'rectangle':'CD','square':'BC','kite':'AD'}.get(model)
            valid=(given+target==180 and scene['answer']==f'∠{("D" if model=="trapezium" else "B")} = {target}°' if model in {'parallelogram','rhombus','trapezium'} else
                target==given and scene['answer']==f'{side} = {target} cm' if side else False)
        elif number==4:
            if v.get('model')=='regular_polygon':
                sides=integer('sides');valid=4<=sides<=44 and target==(sides-2)*180 and v.get('each')==str(__import__('fractions').Fraction(target,sides)) and scene['answer']==f'sum = {target}°; each = {v["each"]}°'
            elif v.get('model')=='diagonals':
                given=integer('given');shape=v.get('shape')
                side='BD' if shape in {'rectangle','square'} else 'EC' if shape in {'parallelogram','rhombus'} else 'ED' if shape=='kite' else None
                valid=side is not None and target==given and scene['answer']==f'{side} = {target} cm'
            else:valid=False
        elif number==5:
            sides=v.get('sides');valid=isinstance(sides,list) and len(sides)==3 and all(type(s) is int and 2<=s<=50 for s in sides) and sides[2]==target and v.get('criterion') in {'SAS','SSS','ASA'} and scene['answer']==(f'EF = {target} cm' if v['criterion']=='SAS' else f'△ABC ≅ △DEF ({v["criterion"]})')
        else:
            small,scale=integer('small'),integer('scale');criterion=v.get('criterion');valid=criterion in {'given','AA','SAS','SSS'} and 2<=scale<=4 and (small+2)*scale==target and scene['answer']==('△ABC ∼ △DEF (SSS similarity)' if criterion=='SSS' else f'EF = {target} cm')
        if not valid:raise ValueError('Shape calculation and corresponding diagram disagree')
        return
    if family.startswith('lines_'):
        number=int(family.rsplit('_',1)[-1]);v=scene.get('visual',{}).get('values',{})
        theta,given,target=v.get('theta'),v.get('given'),v.get('target')
        if (scene.get('lesson')!=number or scene.get('visual',{}).get('family')!='straight_lines'
            or type(theta) is not int or not 40<=theta<=84 or type(given) is not int
            or type(target) is not int or scene['actions'][-1]!=scene.get('check')
            or v.get('kind') not in {'intersection','perpendicular','parallel'}):
            raise ValueError('Line-angle diagram needs bounded given, marked sectors and verification')
        relation=v.get('relation')
        if number==1:
            valid=(relation in {'vertical','linear','right'}
                and v['kind']==('perpendicular' if relation=='right' else 'intersection')
                and given==theta and target==(theta if relation=='vertical' else 90-theta if relation=='right' else 180-theta)
                and scene['answer']==f'x = {target}°')
        elif number in {2,5}:
            valid=(relation in {'corresponding','alternate','cointerior'} and v['kind']=='parallel'
                and given==(180-theta if relation=='cointerior' else theta) and target==theta
                and scene['answer']==f'x = {target}°')
            if number==5:valid=valid and v.get('claimed')==(given if relation=='cointerior' else 180-given) and v['claimed']!=target
        elif number==3:
            valid=(relation=='chain' and v['kind']=='parallel' and given==v.get('middle')==theta
                and target==180-theta and scene['answer']==f'x = {target}°')
        else:
            a,b,x=v.get('coefficient'),v.get('constant'),v.get('solution')
            valid=(relation=='algebra' and v['kind']=='parallel' and type(a) is int and 2<=a<=5
                and type(b) is int and type(x) is int and x>0 and a*x+b==target==180-theta
                and given==theta and v.get('middle')==theta and scene['answer']==f'x = {x}')
        if not valid:raise ValueError('Angle relationship, algebra or target disagrees with the question')
        return
    if family.startswith('graph_'):
        number=int(family.rsplit('_',1)[-1]);visual=scene.get('visual',{});v=visual.get('values',{})
        expected=('global','ordered','gradient','intercepts','line','infer','diagnosis')[number-1]
        points=v.get('points')
        if (scene.get('lesson')!=number or visual.get('family')!=expected
            or not isinstance(points,list) or not 2<=len(points)<=4
            or any(not isinstance(p,list) or len(p)!=2 or any(type(x) is not int or abs(x)>100 for x in p) for p in points)
            or scene.get('actions',[])[-1]!=scene.get('check') or not isinstance(scene.get('answer'),str)):
            raise ValueError('Graph needs bounded question-owned points, stages and check')
        if number==1:
            valid=(len(points)==4 and [p[0] for p in points]==[0,2,4,6]
                and points[0][1]<points[1][1]==points[2][1]>points[3][1]
                and v.get('peak')==points[1][1] and scene['answer']==f'maximum = {v["peak"]} litres')
        else:
            m,b=v.get('m'),v.get('b')
            valid=(type(m) is int and type(b) is int and all(y==m*x+b for x,y in points))
            if number==2:valid=valid and scene['answer']==f'(2, {2*m+b})' and points[-1]==[2,2*m+b]
            elif number==3:valid=valid and len(points)==2 and v.get('run')==points[1][0]-points[0][0]>0 and v.get('rise')==points[1][1]-points[0][1] and scene['answer']==f'gradient = {m}'
            elif number==4:valid=valid and b!=0 and points==[[v.get('x_intercept'),0],[0,b]] and scene['answer']==f'({v["x_intercept"]}, 0) and (0, {b})'
            elif number==5:valid=valid and [p[0] for p in points]==[-1,0,1,2] and scene['answer']==f'(0, {b}) and (1, {b+m})'
            else:valid=valid and [p[0] for p in points]==[0,1,2] and scene['answer']==f'y = {m}x {"+" if b>=0 else "−"} {abs(b)}'
            if number==7:valid=valid and v.get('claimed_gradient')!=m
        if not valid:raise ValueError('Graph points, gradient or intercept disagree with the answer')
        return
    if family.startswith('equation_'):
        v=scene.get('visual',{})
        expected={'1':'groups','2':'balance','3':'brackets','4':'powers','5':'zero_product','6':'table'}[family.rsplit('_',1)[-1]]
        if (v.get('family')!=expected or not isinstance(v.get('givens'),list)
            or not 2<=len(v['givens'])<=4 or any(not isinstance(g,str) or not g or len(g)>120 for g in v['givens'])
            or not isinstance(v.get('values'),dict) or scene.get('answer') is None
            or scene['actions'][-1]!=scene.get('check')):
            raise ValueError('Equation scene must match its lesson, givens, steps and verification')
        z=v['values']
        if expected=='zero_product':
            valid=(scene['answer']==f'x = {z["first"]} or x = {z["second"]}'
                   and z['middle']==-z['second']-z['first']
                   and z['constant']==z['first']*z['second'])
        elif expected=='powers':
            valid=z['base']>1 and z['left']+z['solution']==z['power']
        elif expected=='brackets':
            valid=z['multiplier']*(z['solution']+z['offset'])==z['other']*z['solution']+z['right']
        elif expected=='table':
            valid=all(z['multiplier']*z[key]+z['offset']==z[out] for key,out in
                [('input_one','out_one'),('input_two','out_two'),('solution','target')])
        else:
            valid=z['multiplier']*z['solution']+z['offset']==z['total']
        if not valid or (expected!='zero_product' and not scene['answer'].startswith(f'x = {z["solution"]}')):
            raise ValueError('Equation visual values disagree with its answer')
    elif family.startswith('expression_'):
        v=scene.get('visual')
        families={'terms','like_terms','distribution','area','division','substitution',
            'common_factor','difference_squares','trinomial','fraction','diagnosis'}
        if (not isinstance(v,dict) or v.get('family') not in families
            or not isinstance(v.get('givens'),list) or not 2<=len(v['givens'])<=5
            or any(not isinstance(item,str) or not item or len(item)>90 for item in v['givens'])
            or v.get('answer')!=scene.get('answer')
            or scene.get('actions',[])[-1]!=scene.get('check')
            or (scene.get('answer') not in scene['actions'][-2]
                and not (v['family']=='fraction' and scene['answer'].split(';')[0] in scene['actions'][-2]
                    and v.get('restriction') in scene['actions'][-2]))
            or (v['family']=='fraction' and not v.get('restriction'))):
            raise ValueError('Expression scene requires bounded original terms, answer, and a completed check')
    elif family.startswith('function_'):
        v=scene.get('visual')
        if (not isinstance(v,dict) or v.get('family') not in {'flow','table','formula','graph','diagnosis'}
            or v.get('kind') not in {'linear','square'} or not isinstance(v.get('a'),int)
            or not isinstance(v.get('b'),int) or not 1<=v['a']<=50 or abs(v['b'])>50
            or not isinstance(v.get('known_pairs'),list) or len(v['known_pairs'])!=4
            or not isinstance(v.get('target_input'),int) or abs(v['target_input'])>30
            or scene.get('actions',[])[-1]!=scene.get('check')
            or scene.get('answer') not in scene['actions'][-2]):
            raise ValueError('Function scene requires four bounded pairs, rule, result and check')
        a,b=v['a'],v['b']
        def f(x):return x*x+b if v['kind']=='square' else a*x+b
        expected_rule=(f'y = x² {"+" if b>=0 else "−"} {abs(b)}' if v['kind']=='square'
            else f'y = {a}x {"+" if b>=0 else "−"} {abs(b)}')
        if (v['known_pairs']!=[[x,f(x)] for x in ([-1,0,1,2] if v['family']=='graph' else [0,1,2,3])]
            or v.get('target_output')!=f(v['target_input']) or v.get('rule')!=expected_rule
            or scene['answer']!=(expected_rule if v['family'] in {'graph','diagnosis'} else str(v['target_input']) if v['family']=='table' else str(f(v['target_input'])))):
            raise ValueError('Function values or answer disagree with its source equation')
    elif family.startswith('pattern_'):
        visual=scene.get('visual',{})
        if (not isinstance(visual,dict) or visual.get('family') not in {'tiles','table','differences','rule','diagnosis'}
            or visual.get('kind') not in {'linear','geometric','square','stair','border'}
            or not isinstance(visual.get('known'),list) or len(visual['known']) not in (3,4)
            or any(type(x) is not int or abs(x)>10000 for x in visual['known'])
            or not isinstance(visual.get('a'),int) or not isinstance(visual.get('b'),int)
            or not isinstance(visual.get('target'),int) or not 4<=visual['target']<=20
            or scene.get('actions',[])[-1]!=scene.get('check')
            or scene.get('answer') not in scene['actions'][-2]):
            raise ValueError('Pattern needs its own bounded terms, mathematical rule and final check')
        a,b=visual['a'],visual['b']
        def t(n):
            return {'linear':lambda:a*n+b,'geometric':lambda:a*b**(n-1),
                'square':lambda:a*n*n+b,'stair':lambda:a*n*(n+1)//2+b,
                'border':lambda:a*(2*n+1)+b}[visual['kind']]()
        if (visual['known']!=[t(n) for n in range(1,len(visual['known'])+1)]
            or visual.get('target_value')!=t(visual['target'])
            or scene['answer']!=(visual['rule'] if visual['family'] in {'rule','diagnosis'} else str(t(visual['target'])))):
            raise ValueError('Pattern answer or pictured terms disagree with the source rule')
    elif family.startswith('exponent_'):
        visual=scene.get('visual')
        if (not isinstance(visual,dict) or visual.get('family') not in {'factors','law','reciprocal','scale','compare','context','diagnosis'}
            or not isinstance(scene.get('givens'),list) or not scene['givens']
            or not isinstance(scene.get('answer'),str) or not scene['answer']
            or not scene['actions'][-1].startswith('Check: ')
            or scene['answer'] not in scene['actions'][-2]):
            raise ValueError('Exponent scene must show exact givens, mathematical result and check')
        if visual['family'] in {'factors','law','reciprocal'}:
            if not isinstance(visual.get('base'),int) or abs(visual['base'])>20 or not isinstance(visual.get('exponents'),list) and visual['family']!='reciprocal':
                raise ValueError('Exponent base or power list is invalid')
        if visual['family']=='scale' and not -12<=visual.get('exponent',100)<=12:
            raise ValueError('Scientific exponent outside supported range')
    elif family.startswith('integer_'):
        visual=scene.get('visual')
        if (not isinstance(visual,dict) or visual.get('family') not in {'line','tiles','root','context','diagnosis'}
            or not isinstance(visual.get('values'),list) or not 1<=len(visual['values'])<=3
            or any(type(x) is not int or abs(x)>1000 for x in visual['values'])
            or not isinstance(visual.get('path'),list) or not 1<=len(visual['path'])<=3
            or any(type(x) is not int or abs(x)>100000 for x in visual['path'])
            or len(scene.get('givens',[]))<1 or not scene.get('answer')
            or not scene['actions'][-1].startswith('Check: ')
            or str(visual['path'][-1]) not in scene['actions'][-2]):
            raise ValueError('Integer scene must retain exact signed givens, staged path, answer and check')
    elif family=='sets':
        expected={'N','W','Z','Q','I','outside'}
        if scene.get('category') not in expected or not scene.get('token'):
            raise ValueError('Number-set scene requires an exact token and valid smallest set')
        if 'secondary_input' in scene and (scene.get('secondary_category') not in expected
            or not scene.get('secondary') or not 1<=scene.get('primary_stage',0)<parameters['total_steps']
            or not 1<=scene.get('secondary_stage',0)<parameters['total_steps']):
            raise ValueError('A comparison must stage two exact values and their distinct sets')
    elif family=='factors':
        numbers=scene.get('numbers');factors=scene.get('factors')
        if not isinstance(numbers,list) or not 1<=len(numbers)<=5 or any(type(n) is not int or not 2<=n<=999 for n in numbers):
            raise ValueError('Prime-factor scene needs bounded original roots')
        if not isinstance(factors,list) or len(factors)!=len(numbers):
            raise ValueError('Each root requires prime leaves')
        for n,leaves in zip(numbers,factors):
            if not isinstance(leaves,list) or not leaves or any(type(p) is not int or p<2 or any(p%d==0 for d in range(2,math.isqrt(p)+1)) for p in leaves) or math.prod(leaves)!=n:
                raise ValueError('Prime leaves do not reproduce their original root')
    else:
        visual=scene.get('visual')
        families={'ratio_rate':{'ratio','rate'},'proportion':{'direct','inverse','share'},
            'transaction':{'transaction'},'ledger':{'ledger'},'interest':{'interest'},
            'decision':{'exchange','commission','rental','rental_exchange'}}
        if (not isinstance(visual,dict) or visual.get('family') not in families[family]
            or len(scene.get('givens',[]))<2 or not scene.get('answer')
            or not scene['actions'][-1].startswith('Check: ')):
            raise ValueError('Grade 9 context scene needs its own givens, visual, result and check')


def _grade8_pattern_board(parameters: dict) -> None:
    import json
    scene=json.loads(parameters["scene_json"])
    if scene.get("id")!=parameters["question_id"] or scene.get("problem")!=parameters["prompt"] or parameters["total_steps"]!=4:
        raise ValueError("Pattern question, scene and four steps must match")
    terms=scene.get("terms")
    if not isinstance(terms,list) or len(terms) not in (4,6) or any(type(v) not in (int,float) or abs(v)>1000 for v in terms):
        raise ValueError("Pattern needs bounded numeric givens")
    if scene.get("model") not in ("numeric","geometric","rule_table","missing_table","compare_rules","repair_claim") or scene.get("kind") not in (
        "add","ratio","squares","triangular","cubes","recursive","alternating",
        "joined_squares","separate_squares","square_dots","staircase","border","l_shape",
        "triangle_edges","two_rows","rectangle","square_plus","fence","three_arms",
        "columns","square_plus_two","rectangle_two", None):
        raise ValueError("Unknown pattern visual model")
    if "answer" in scene and (type(scene["answer"]) not in (int,float,str) or
       isinstance(scene["answer"],(int,float)) and abs(scene["answer"])>100000 or
       isinstance(scene["answer"],str) and len(scene["answer"])>80):
        raise ValueError("Pattern result must be bounded")
    if scene["model"] in ("rule_table","missing_table"):
        family=scene.get("family");a=scene.get("a");b=scene.get("b")
        if family not in ("linear","square_offset","triangular","rectangle","geometric") or any(type(v) not in (int,float) or abs(v)>100 for v in (a,b)):
            raise ValueError("Pattern rule needs bounded coefficients and a supported family")
        def value(n):
            return {"linear":lambda:a*n+b,"square_offset":lambda:a*n*n+b,
                "triangular":lambda:a*n*(n+1)//2+b,"rectangle":lambda:a*n*(n+1)+b,
                "geometric":lambda:a*b**(n-1)}[family]()
        if len(terms)!=4 or terms!=[value(n) for n in range(1,5)]:
            raise ValueError("Pattern table values disagree with its algebraic rule")
        if scene["model"]=="missing_table" and (type(scene.get("target_position")) is not int or
           not 5<=scene["target_position"]<=8 or scene.get("answer",value(scene["target_position"]))!=value(scene["target_position"])):
            raise ValueError("Missing value must match the position and rule")
        if scene["model"]=="rule_table":
            expected_rule=(f"{a:g}n" if a else "0n")+(f" + {b:g}" if b>0 else f" − {-b:g}" if b<0 else "")
            if family!="linear" or scene.get("rule")!=expected_rule or scene.get("answer",expected_rule)!=expected_rule:
                raise ValueError("Linear rule must match the given coefficients and answer")
    if scene.get("model") in ("compare_rules","repair_claim"):
        family=scene.get("family")
        def calculate(f,a,b,n):
            return {"linear":lambda:a*n+b,"square_offset":lambda:a*n*n+b,
                "triangular":lambda:a*n*(n+1)//2+b,"rectangle":lambda:a*n*(n+1)+b,
                "geometric":lambda:a*b**(n-1)}[f]()
        if len(terms)!=4 or type(scene.get("target_position")) is not int or not 5<=scene["target_position"]<=8:
            raise ValueError("Pattern comparison needs four terms and a bounded target")
        if scene["model"]=="compare_rules":
            candidates=scene.get("candidates")
            if not isinstance(candidates,list) or len(candidates)!=2 or scene.get("correct_label") not in ("A","B"):
                raise ValueError("Two proposed rules and a correct label are required")
            if type(scene.get("wrong_index")) is not int or not 2<=scene["wrong_index"]<=4:
                raise ValueError("Counterexample must point to a given position")
            for candidate in candidates:
                if not isinstance(candidate,dict) or candidate.get("family") not in ("linear","square_offset","triangular","rectangle","geometric") or any(type(candidate.get(k)) is not int or abs(candidate[k])>100 for k in ("a","b")):
                    raise ValueError("Pattern candidate coefficients are invalid")
            good=candidates[0 if scene["correct_label"]=="A" else 1]
            bad=candidates[1 if scene["correct_label"]=="A" else 0]
            if terms!=[calculate(good["family"],good["a"],good["b"],n) for n in range(1,5)]:
                raise ValueError("Candidate labelled correct disagrees with the givens")
            if calculate(bad["family"],bad["a"],bad["b"],scene.get("wrong_index",0))==terms[scene.get("wrong_index",1)-1]:
                raise ValueError("Rejected candidate needs a real counterexample")
            if scene.get("answer")!=calculate(good["family"],good["a"],good["b"],scene["target_position"]):
                raise ValueError("Pattern answer disagrees with the surviving rule")
        else:
            a,b=scene.get("a"),scene.get("b")
            if family not in ("linear","square_offset","triangular","rectangle","geometric") or any(type(v) is not int or abs(v)>100 for v in (a,b)):
                raise ValueError("Repair needs a valid bounded rule")
            if terms!=[calculate(family,a,b,n) for n in range(1,5)] or scene.get("answer")!=calculate(family,a,b,scene["target_position"]):
                raise ValueError("Repaired prediction must agree with the rule and givens")
            if type(scene.get("claimed")) is not int or scene["claimed"]==scene["answer"]:
                raise ValueError("A repair requires an incorrect, bounded claim")
    if scene.get("model")=="geometric":
        n=5
        expected={"joined_squares":3*n+1,"separate_squares":4*n,"square_dots":n*n,
            "staircase":n*(n+1)//2,"border":4*n,"l_shape":2*n+1,"triangle_edges":3*n,
            "two_rows":2*n,"rectangle":n*(n+1),"square_plus":n*n+4,"fence":4*(n+1),
            "three_arms":3*n+1,"columns":4*n+2,"square_plus_two":n*n+2,"rectangle_two":n*(n+2)}
        if scene.get("answer",expected[scene["kind"]])!=expected[scene["kind"]]:
            raise ValueError("Geometric answer disagrees with constructed figure")

def _grade8_global_story(parameters: dict) -> None:
    import json
    try:
        scene = json.loads(parameters["scene_json"])
    except (TypeError, ValueError) as error:
        raise ValueError("Global graph scene must be valid JSON") from error
    if not isinstance(scene, dict) or scene.get("id") != parameters["question_id"]:
        raise ValueError("Global graph scene ID must match the question")
    if scene.get("problem") != parameters["prompt"] or parameters["total_steps"] != 4:
        raise ValueError("Global graph prompt and four teaching steps must match")
    if scene.get("kind") not in {"read", "draw", "compare", "diagnose"} or scene.get("domain") not in {"continuous", "discrete"}:
        raise ValueError("Global graph needs a supported mode and explicit domain")
    axis = scene.get("axis")
    if not isinstance(axis, dict):
        raise ValueError("Global graph needs labelled axes")
    for key in ("x_min", "x_max", "y_min", "y_max", "x_tick", "y_tick"):
        value = axis.get(key)
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not -1000 <= value <= 1000:
            raise ValueError(f"Global graph {key} must be numeric and bounded")
    if not axis["x_min"] < axis["x_max"] or not axis["y_min"] < axis["y_max"] or axis["x_tick"] <= 0 or axis["y_tick"] <= 0:
        raise ValueError("Global graph axes need increasing bounds and positive ticks")
    if any(not isinstance(axis.get(key), str) or not axis[key].strip() or len(axis[key]) > 45 for key in ("x_unit", "y_unit")):
        raise ValueError("Global graph axes require short units")
    points = scene.get("points")
    if not isinstance(points, list) or len(points) != 4:
        raise ValueError("Global graph needs four ordered source points")
    for index, point in enumerate(points):
        if not isinstance(point, dict) or set(point) != {"x", "y"}:
            raise ValueError("Global graph point needs x and y")
        for coordinate in ("x", "y"):
            value = point[coordinate]
            if not isinstance(value, (int, float)) or isinstance(value, bool) or not axis[f"{coordinate}_min"] <= value <= axis[f"{coordinate}_max"]:
                raise ValueError("Global graph point is outside its axes")
        if index and not points[index-1]["x"] < point["x"]:
            raise ValueError("Global graph x-values must increase")
    if scene["kind"] == "compare":
        other = scene.get("secondary_points")
        if not isinstance(other, list) or len(other) != len(points) or scene.get("series_labels") != ["A", "B"]:
            raise ValueError("Comparison needs A and B on the same four inputs")
        for first, second in zip(points, other, strict=True):
            if not isinstance(second, dict) or set(second) != {"x", "y"} or second["x"] != first["x"]:
                raise ValueError("Comparison inputs must align")
            if not isinstance(second["y"], (int, float)) or isinstance(second["y"], bool) or not axis["y_min"] <= second["y"] <= axis["y_max"]:
                raise ValueError("Comparison point is outside the common axis")
        metrics = {
            "gain_all": lambda ys: ys[3] - ys[0], "loss_all": lambda ys: ys[0] - ys[3],
            "point2": lambda ys: ys[2], "point3": lambda ys: ys[3],
            "lower_point3": lambda ys: -ys[3], "gain_mid": lambda ys: ys[2] - ys[1],
            "gain_last": lambda ys: ys[3] - ys[2],
        }
        metric = scene.get("comparison_metric")
        if metric not in metrics:
            raise ValueError("Comparison needs an explicit checked metric")
        a_value = metrics[metric]([point["y"] for point in points])
        b_value = metrics[metric]([point["y"] for point in other])
        expected = "A" if a_value > b_value else "B" if b_value > a_value else "equal"
        if scene.get("answer") != expected:
            raise ValueError("Comparison answer disagrees with the plotted values")
    if scene["kind"] == "diagnose":
        if not isinstance(scene.get("claim"), str) or not scene["claim"].strip() or not isinstance(scene.get("focus_index"), int) or isinstance(scene["focus_index"], bool) or not 1 <= scene["focus_index"] <= 3:
            raise ValueError("Diagnosis needs a learner claim and a valid focus input")
    if not isinstance(scene.get("actions"), list) or len(scene["actions"]) != 4 or any(not isinstance(a, str) or not a.strip() for a in scene["actions"]):
        raise ValueError("Global graph needs four authored mathematical actions")
    if not isinstance(scene.get("answer"), str) or not scene["answer"].strip():
        raise ValueError("Global graph answer must be present")

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
    graph = scene.get("graph")
    if graph is not None:
        if not isinstance(graph, dict) or graph.get("mode") not in {"line", "given_line", "discrete", "nonlinear", "error"}:
            raise ValueError("Grade 8 graph needs a supported domain mode")
        rows = graph.get("table")
        points = graph.get("points")
        if not isinstance(rows, list) or not 3 <= len(rows) <= 5 or rows != points:
            raise ValueError("Grade 8 plotted points must match all table rows")
        if any(not isinstance(row, dict) or set(row) != {"x", "y"} or not all(isinstance(row[key], (int, float)) and not isinstance(row[key], bool) for key in ("x", "y")) for row in rows):
            raise ValueError("Grade 8 table rows require numeric x and y")
        if len({row["x"] for row in rows}) != len(rows):
            raise ValueError("Grade 8 table input values must be distinct")
        if graph["mode"] in {"line", "given_line", "error"}:
            x0, y0 = rows[0]["x"], rows[0]["y"]
            x1, y1 = rows[1]["x"], rows[1]["y"]
            if any(abs((row["y"] - y0) * (x1 - x0) - (row["x"] - x0) * (y1 - y0)) > 1e-8 for row in rows[2:]):
                raise ValueError("Grade 8 straight-line points must be collinear")
        if graph.get("line_reveal_step") != parameters["total_steps"]:
            raise ValueError("Grade 8 connecting line must wait for the final reasoning step")

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

def _grade8_relationship_compare(parameters: dict) -> None:
    import json
    _grade8_function_visual(parameters)
    try:
        scene=json.loads(parameters["scene_json"])
    except (TypeError, ValueError) as error:
        raise ValueError("Relationship comparison requires a JSON scene") from error
    if not isinstance(scene,dict) or scene.get("mode") not in {"match","repair"}:
        raise ValueError("Relationship comparison needs a supported mode")
    if not isinstance(scene.get("input"),(int,float)) or isinstance(scene["input"],bool) or abs(scene["input"])>100:
        raise ValueError("Comparison input must be bounded")
    candidates=scene.get("candidates")
    if not isinstance(candidates,list) or len(candidates)!=2 or scene.get("chosen") not in [c.get("label") for c in candidates if isinstance(c,dict)]:
        raise ValueError("Exactly two labelled paths and a valid chosen path required")
    for candidate in candidates:
        if not isinstance(candidate,dict) or not isinstance(candidate.get("label"),str) or not 0<len(candidate["label"])<=32:
            raise ValueError("Candidate path label required")
        for key in ("a","b","c","value"):
            v=candidate.get(key)
            if not isinstance(v,(int,float)) or isinstance(v,bool) or abs(v)>10000:
                raise ValueError("Candidate coefficients and value must be bounded numbers")
        x=scene["input"]
        if abs(candidate["a"]*x*x+candidate["b"]*x+candidate["c"]-candidate["value"])>1e-7:
            raise ValueError("Candidate evaluation disagrees with its coefficients")
    if candidates[0]["value"]==candidates[1]["value"]:
        raise ValueError("Comparison requires a distinguishing input")
    if not isinstance(scene.get("given"),list) or not 1<=len(scene["given"])<=4 or any(not isinstance(v,str) or not v.strip() or len(v)>120 for v in scene["given"]):
        raise ValueError("Original evidence must be question-specific")

CATALOGUE: dict[tuple[str, str], TemplateDefinition] = {
    **{("algebra", template): TemplateDefinition(
        frozenset({"prompt","question_id","given_objects","derived_objects","total_steps","scene_json"}),
        frozenset(),_grade8_relationship_compare,True)
        for template in ("relationship_match","relationship_repair")},
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
    ("algebra", "grade8_pattern_board"): TemplateDefinition(
        frozenset({"scene_json","question_id","prompt","total_steps"}), frozenset(), _grade8_pattern_board, True),
    ("algebra", "grade8_whole_number_board"): TemplateDefinition(
        frozenset({"scene_json","question_id","prompt","total_steps"}), frozenset(), _grade8_whole_number_board, True),
    ("algebra", "grade9_number_sets"): TemplateDefinition(
        frozenset({"scene_json","question_id","prompt","total_steps"}), frozenset(), lambda p:_grade9_whole_board(p,'sets'), True),
    ("algebra", "grade9_prime_factors"): TemplateDefinition(
        frozenset({"scene_json","question_id","prompt","total_steps"}), frozenset(), lambda p:_grade9_whole_board(p,'factors'), True),
    **{("algebra",f"grade9_{template}"): TemplateDefinition(
        frozenset({"scene_json","question_id","prompt","total_steps"}),frozenset(),
        lambda p,f=template:_grade9_whole_board(p,f),True)
       for template in ('ratio_rate','proportion','transaction','ledger','interest','decision')},
    **{("algebra",f"grade9_integer_{n}"): TemplateDefinition(
        frozenset({"scene_json","question_id","prompt","total_steps"}),frozenset(),
        lambda p,n=n:_grade9_whole_board(p,f'integer_{n}'),True)
       for n in range(1,6)},
    **{("algebra",f"grade9_exponent_{n}"): TemplateDefinition(
        frozenset({"scene_json","question_id","prompt","total_steps"}),frozenset(),
        lambda p,n=n:_grade9_whole_board(p,f'exponent_{n}'),True)
       for n in range(1,7)},
    **{("algebra",f"grade9_pattern_{n}"): TemplateDefinition(
        frozenset({"scene_json","question_id","prompt","total_steps"}),frozenset(),
        lambda p,n=n:_grade9_whole_board(p,f'pattern_{n}'),True)
       for n in range(1,6)},
    **{("algebra",f"grade9_function_{n}"): TemplateDefinition(
        frozenset({"scene_json","question_id","prompt","total_steps"}),frozenset(),
        lambda p,n=n:_grade9_whole_board(p,f'function_{n}'),True)
       for n in range(1,6)},
    **{("algebra",f"grade9_expression_{n}"): TemplateDefinition(
        frozenset({"scene_json","question_id","prompt","total_steps"}),frozenset(),
        lambda p,n=n:_grade9_whole_board(p,f'expression_{n}'),True)
       for n in range(1,10)},
    **{("geometry",f"grade9_area_{n}"): TemplateDefinition(
        frozenset({"scene_json","question_id","prompt","total_steps"}),frozenset(),
        lambda p,n=n:_grade9_whole_board(p,f'area_{n}'),True)
       for n in range(1,6)},
    **{("statistics",f"grade9_data_{n}"): TemplateDefinition(
        frozenset({"scene_json","question_id","prompt","total_steps"}),frozenset(),
        lambda p,n=n:_grade9_whole_board(p,f'data_{n}'),True)
       for n in range(1,9)},
    **{("algebra",f"grade10_algebra_{n}"): TemplateDefinition(
        frozenset({"scene_json","question_id","prompt","total_steps"}),frozenset(),
        lambda p,n=n:_grade10_algebra_board(p,n),True)
       for n in range(1,7)},
    **{("algebra",f"grade10_eei_{n}"): TemplateDefinition(
        frozenset({"scene_json","question_id","prompt","total_steps"}),frozenset(),
        lambda p,n=n:_grade10_eei_board(p,n),True)
       for n in range(1,10)},
    **{("algebra",f"grade10_fn_{n}"): TemplateDefinition(
        frozenset({"scene_json","question_id","prompt","total_steps"}),frozenset(),
        lambda p,n=n:_grade10_fn_board(p,n),True)
       for n in range(1,8)},
    **{("statistics",f"grade10_stat_{n}"): TemplateDefinition(
        frozenset({"scene_json","question_id","prompt","total_steps"}),frozenset(),
        lambda p,n=n:_grade10_stat_board(p,n),True)
       for n in range(1,7)},
    **{("geometry",f"grade10_ag_{n}"): TemplateDefinition(
        frozenset({"scene_json","question_id","prompt","total_steps"}),frozenset(),
        lambda p,n=n:_grade10_ag_board(p,n),True)
       for n in range(1,7)},
    **{("geometry",f"grade10_euc_{n}"): TemplateDefinition(
        frozenset({"scene_json","question_id","prompt","total_steps"}),frozenset(),
        lambda p,n=n:_grade10_euc_board(p,n),True)
       for n in range(1,7)},
    **{("geometry",f"grade10_trig_{n}"): TemplateDefinition(
        frozenset({"scene_json","question_id","prompt","total_steps"}),frozenset(),
        lambda p,n=n:_grade10_trig_board(p,n),True)
       for n in range(1,8)},
    **{("geometry",f"grade9_transform_{n}"): TemplateDefinition(
        frozenset({"scene_json","question_id","prompt","total_steps"}),frozenset(),
        lambda p,n=n:_grade9_transform_board(p,n),True)
       for n in range(1,8)},
    **{("geometry",f"grade9_surface_{n}"): TemplateDefinition(
        frozenset({"scene_json","question_id","prompt","total_steps"}),frozenset(),
        lambda p,n=n:_grade9_surface_board(p,n),True)
       for n in range(1,7)},
    **{("geometry",f"grade9_solid_{n}"): TemplateDefinition(
        frozenset({"scene_json","question_id","prompt","total_steps"}),frozenset(),
        lambda p,n=n:_grade9_whole_board(p,f'solid_{n}'),True)
       for n in range(1,5)},
    **{("statistics",f"grade9_probability_{n}"): TemplateDefinition(
        frozenset({"scene_json","question_id","prompt","total_steps"}),frozenset(),
        lambda p,n=n:_grade9_whole_board(p,f'probability_{n}'),True)
       for n in range(1,6)},
    **{("geometry",f"grade9_shapes_{n}"): TemplateDefinition(
        frozenset({"scene_json","question_id","prompt","total_steps"}),frozenset(),
        lambda p,n=n:_grade9_whole_board(p,f'shapes_{n}'),True)
       for n in range(1,9)},
    **{("geometry",f"grade9_lines_{n}"): TemplateDefinition(
        frozenset({"scene_json","question_id","prompt","total_steps"}),frozenset(),
        lambda p,n=n:_grade9_whole_board(p,f'lines_{n}'),True)
       for n in range(1,6)},
    **{("algebra",f"grade9_graph_{n}"): TemplateDefinition(
        frozenset({"scene_json","question_id","prompt","total_steps"}),frozenset(),
        lambda p,n=n:_grade9_whole_board(p,f'graph_{n}'),True)
       for n in range(1,8)},
    **{("algebra",f"grade9_equation_{n}"): TemplateDefinition(
        frozenset({"scene_json","question_id","prompt","total_steps"}),frozenset(),
        lambda p,n=n:_grade9_whole_board(p,f'equation_{n}'),True)
       for n in range(1,7)},
    ("algebra", "grade8_decimal_product"): TemplateDefinition(frozenset({"scene_json","question_id","prompt","total_steps"}),frozenset(),_grade8_decimal_product,True),
    ("algebra", "grade8_decimal_quotient"): TemplateDefinition(frozenset({"scene_json","question_id","prompt","total_steps"}),frozenset(),_grade8_decimal_quotient,True),
    ("algebra", "grade8_decimal_power"): TemplateDefinition(frozenset({"scene_json","question_id","prompt","total_steps"}),frozenset(),lambda parameters: _grade8_decimal_power_root(parameters,"power"),True),
    ("algebra", "grade8_decimal_root"): TemplateDefinition(frozenset({"scene_json","question_id","prompt","total_steps"}),frozenset(),lambda parameters: _grade8_decimal_power_root(parameters,"root"),True),
    ("geometry", "grade8_intersecting_angles"): TemplateDefinition(frozenset({"scene_json","question_id","prompt","total_steps"}),frozenset(),lambda parameters: _grade8_line_scene(parameters,1),True),
    ("geometry", "grade8_parallel_angles"): TemplateDefinition(frozenset({"scene_json","question_id","prompt","total_steps"}),frozenset(),lambda parameters: _grade8_line_scene(parameters,2),True),
    **{("geometry",template): TemplateDefinition(frozenset({"scene_json","question_id","prompt","total_steps"}),frozenset(),lambda parameters,n=number: _grade8_angle_chain_scene(parameters,n),True)
       for number,template in ((3,"grade8_angle_chain"),(4,"grade8_angle_equation"),(5,"grade8_angle_error"))},
    **{("geometry",f"grade8_{family}"): TemplateDefinition(frozenset({"scene_json","question_id","prompt","total_steps"}),frozenset(),lambda parameters,f=family: _grade8_shape_scene(parameters,f),True)
       for family in ("triangle_sides","triangle_sum","equal_triangle","quad_classify","quad_angle")},
    **{("geometry",f"grade8_pythagoras_{family}"): TemplateDefinition(frozenset({"scene_json","question_id","prompt","total_steps"}),frozenset(),lambda parameters,f=family: _grade8_pythagoras_scene(parameters,f),True)
       for family in ("square_areas","hypotenuse","missing_leg","converse","application")},
    ("algebra", "grade8_exponent_representation"): TemplateDefinition(frozenset({"scene_json","question_id","prompt","total_steps"}),frozenset(),lambda parameters: _grade8_exponent_scene(parameters,1),True),
    ("algebra", "grade8_exponent_laws"): TemplateDefinition(frozenset({"scene_json","question_id","prompt","total_steps"}),frozenset(),lambda parameters: _grade8_exponent_scene(parameters,2),True),
    ("algebra", "grade8_exponent_roots"): TemplateDefinition(frozenset({"scene_json","question_id","prompt","total_steps"}),frozenset(),lambda parameters: _grade8_exponent_scene(parameters,3),True),
    ("algebra", "grade8_exponent_applications"): TemplateDefinition(frozenset({"scene_json","question_id","prompt","total_steps"}),frozenset(),lambda parameters: _grade8_exponent_scene(parameters,4),True),
    ("algebra", "grade8_exponent_error_trace"): TemplateDefinition(frozenset({"scene_json","question_id","prompt","total_steps"}),frozenset(),lambda parameters: _grade8_exponent_scene(parameters,5),True),
    ("algebra", "grade8_exponent_integrated"): TemplateDefinition(frozenset({"scene_json","question_id","prompt","total_steps"}),frozenset(),lambda parameters: _grade8_exponent_scene(parameters,6),True),
    ("algebra", "grade8_decimal_columns"): TemplateDefinition(frozenset({"scene_json","question_id","prompt","total_steps"}),frozenset(),_grade8_decimal_columns,True),
    ("algebra", "grade8_decimal_rounding"): TemplateDefinition(frozenset({"scene_json","question_id","prompt","total_steps"}),frozenset(),_grade8_decimal_rounding,True),
    ("algebra", "grade8_percentage_grid"): TemplateDefinition(
        frozenset({"scene_json","question_id","prompt","total_steps"}), frozenset(), _grade8_percentage_grid, True),
    ("algebra", "grade8_fraction_powers_context"): TemplateDefinition(
        frozenset({"scene_json","question_id","prompt","total_steps"}), frozenset(), _grade8_fraction_powers_context, True),
    ("algebra", "grade8_fraction_operations"): TemplateDefinition(
        frozenset({"scene_json","question_id","prompt","total_steps"}), frozenset(), _grade8_fraction_operations, True),
    ("algebra", "grade8_fraction_strips"): TemplateDefinition(
        frozenset({"scene_json","question_id","prompt","total_steps"}), frozenset(), _grade8_fraction_strips, True),
    ("algebra", "grade8_integer_reasoning"): TemplateDefinition(
        frozenset({"scene_json","question_id","prompt","total_steps"}), frozenset(), _grade8_integer_reasoning, True),
    ("algebra", "grade8_integer_operations"): TemplateDefinition(
        frozenset({"scene_json","question_id","prompt","total_steps"}), frozenset(), _grade8_integer_operations, True),
    ("algebra", "grade8_integer_board"): TemplateDefinition(
        frozenset({"scene_json","question_id","prompt","total_steps"}), frozenset(), _grade8_integer_board, True),
    ("coordinate_geometry", "grade8_global_story"): TemplateDefinition(
        frozenset({"scene_json", "question_id", "prompt", "total_steps"}), frozenset(), _grade8_global_story, True),
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
    if ("five-number summary" in problem_lower and ("construct" in problem_lower or "box plot" in problem_lower)) and instruction.template not in {"box_plot", "grade10_stat_4"}:
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
