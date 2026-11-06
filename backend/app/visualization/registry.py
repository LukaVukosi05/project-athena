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
            limit = (6000 if key == "scene_json" else 400) if key in {"scene_json", "prompt"} and re.fullmatch(r"(?:g8-graphs-l0[1-6]|g8-patterns-l0[1-6]|g8-whole-l0[1-2]|g8-int-l0[1-6]|g8-frac-l0[1-8]|g8-dec-l0[1-6]|g8-exp-l0[1-6]|g8-fr-l0[4-6]|g8-shapes-0[1-5]|g8-pyth-0[1-5]|g8-lines-0[3-5]|g9-whole-l0[1-8]|g9-int-l0[1-5]|g9-exp-l0[1-6]|g9-pat-l0[1-5]|g9-fn-l0[1-5])-w(?:0[1-9]|1[0-5])", str(parameters.get("question_id", ""))) else 600 if (key in {"source_data", "initial_state"} or key == "prompt" and str(parameters.get("question_id", "")).startswith(("g8-ae-l09-", "g8-ae-l10-"))) and re.fullmatch(r"g8-ae-l(?:0[1-9]|10)-w\d{2}", str(parameters.get("question_id", ""))) else 160
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


def _grade9_whole_board(parameters: dict, family: str) -> None:
    import json
    import math
    scene=json.loads(parameters['scene_json'])
    if (scene.get('id')!=parameters['question_id'] or scene.get('problem')!=parameters['prompt']
        or scene.get('actions') is None or len(scene['actions'])!=parameters['total_steps']
        or not 3<=parameters['total_steps']<=18):
        raise ValueError('Grade 9 source scene, question and step count disagree')
    if family.startswith('function_'):
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
