"""Runtime conversion of the approved Grade 12 Paper 2 Topics 8 and 9 packs."""

from __future__ import annotations

import json
import re
from pathlib import Path

from app.curriculum.schemas import (
    AccessLevel, ContentStatus, Lesson, LessonBlock, MathematicalOperation,
    PresentationContract, PresentationEvent, PresentationSemanticObject,
    SemanticObject, StepExplanation, TeachingStep, TimelineEvent, VoiceCue,
    VisualizationInstruction, VisualizationState, WhiteboardBlock, WhiteboardQuestion,
)
from app.practice.schemas import (
    ANALYTICAL_GEOMETRY_SOURCE, STATISTICS_SOURCE, PracticeQuestion,
    WorkedSolutionStep,
)


ROOT = Path(__file__).parent
STATISTICS_PACK = json.loads((ROOT / "statistics_regression_pack.json").read_text(encoding="utf-8"))
ANALYTICAL_GEOMETRY_PACK = json.loads((ROOT / "analytical_geometry_pack.json").read_text(encoding="utf-8"))

STATISTICS_CANVAS_FAMILIES = [
    "data_studio", "balance_and_rank", "spread_number_line", "five_number_ribbon",
    "ogive_builder", "box_plot_builder", "outlier_fence_lab", "deviation_calculator_lab",
    "distribution_comparison", "scatter_builder", "correlation_continuum", "least_squares_fit",
    "regression_calculator", "interpolation_trace", "extrapolation_risk_zone", "influence_lab",
    "integrated_statistics_dashboard", "question_first_assessment",
]
ANALYTICAL_GEOMETRY_CANVAS_FAMILIES = [
    "coordinate_distance_lab", "midpoint_bisection", "slope_triangle", "line_equation_link",
    "parallel_comparison", "perpendicular_rotation", "inclination_arc", "circle_construction",
    "complete_square_morph", "circle_condition_intersection", "radius_tangent_contact",
    "tangent_equation_construction", "external_tangent_length", "coordinate_proof_studio",
    "integrated_coordinate_scene", "question_first_assessment",
]


def slug(value: str) -> str:
    result = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
    result = result or "object"
    return result if result[0].isalpha() else f"object-{result}"


def level_fields(level: str) -> tuple[str, str, int]:
    return {
        "Foundation": ("foundation", "knowledge", 1),
        "Routine": ("standard", "routine", 2),
        "Complex": ("advanced", "complex", 3),
        "Exam-level": ("exam", "problem_solving", 4),
    }[level]


def demands(level: str, prompt: str) -> list[str]:
    result = ["identify_and_apply"]
    if level in {"Routine", "Complex", "Exam-level"}:
        result.append("multi_step_procedure")
    if level in {"Complex", "Exam-level"}:
        result.extend(["connect_representations", "verify_original"])
    if level == "Exam-level":
        result.extend(["dependency_reasoning", "evaluate_and_justify"])
    if "interpret" in prompt.casefold():
        result.append("interpret_in_context")
    if "exact" in prompt.casefold():
        result.append("preserve_exact_form")
    return result


def operation_signature(level: str, prompt: str) -> list[str]:
    return list(dict.fromkeys(demands(level, prompt)))


def semantic_objects(lesson: dict) -> list[PresentationSemanticObject]:
    labels = [item.strip() for item in lesson["presentation"]["design"]["Semantic objects"].split(",") if item.strip()]
    seen: dict[str, int] = {}
    objects = []
    for label in labels:
        base = slug(label)
        seen[base] = seen.get(base, 0) + 1
        identifier = base if seen[base] == 1 else f"{base}-{seen[base]}"
        objects.append(PresentationSemanticObject(id=identifier, type=slug(label).replace("-", "_"), accessible_label=label))
    return objects


def presentation_contract(lesson: dict, family: str, pronunciation_hints: list[str]) -> PresentationContract:
    objects = semantic_objects(lesson)
    object_ids = [item.id for item in objects]
    events = []
    cues = []
    event_types = ["orient", "predict", "operate", "inspect", "verify", "summarise"]
    for index, (beat, event_type) in enumerate(zip(lesson["presentation"]["beats"], event_types), 1):
        event_id = f"{slug(lesson['id'])}-event-{index:02}"
        events.append(PresentationEvent(
            event_id=event_id, sequence=index, event_type=event_type,
            visual_instruction=beat["Visual event"], semantic_object_ids=object_ids,
            hold_after=event_type in {"predict", "verify"},
        ))
        narration = beat["Future narration / interaction"]
        cues.append(VoiceCue(
            cue_id=f"{slug(lesson['id'])}-cue-{index:02}", start_event=event_id,
            end_event=event_id, spoken_text=narration, caption_text=narration,
            pronunciation_hints=pronunciation_hints, wait_for_user=event_type == "predict",
        ))
    design = lesson["presentation"]["design"]
    return PresentationContract(
        paper="Paper 2", canvas_family=family, semantic_objects=objects, events=events,
        voice_cues=cues,
        reduced_motion_sequence=[beat["Visual event"] for beat in lesson["presentation"]["beats"]],
        animation_choreography=design["Animation choreography"],
        voice_direction=design["Voice direction"], prohibited_fallback=design["Do not use"],
        question_first=True,
    )

def numeric_list(text: str, pattern: str = r"\[([^\]]+)\]") -> list[float]:
    match = re.search(pattern, text, re.I)
    if not match:
        return []
    return [float(value) for value in re.findall(r"-?\d+(?:\.\d+)?", match.group(1))]

def paired_lists(text: str) -> tuple[list[float], list[float]]:
    x = numeric_list(text, r"x\s*=\s*\[([^\]]+)\]")
    y = numeric_list(text, r"y\s*=\s*\[([^\]]+)\]")
    if x and y:
        return x, y
    pairs = re.findall(r"\((-?\d+(?:\.\d+)?),\s*(-?\d+(?:\.\d+)?)\)", text)
    return ([float(a) for a, _ in pairs], [float(b) for _, b in pairs])

def statistics_visualization(item: dict, family: str, object_ids: list[str]) -> VisualizationInstruction:
    prompt, memo = item["Problem"], item["Worked evidence / memo"]
    common = {"objects": object_ids, "title": prompt[:120]}
    if family == "data_studio":
        scenario = re.search(r"studies\s+(.+?)\s+for a sample of\s+(\d+)", prompt, re.I)
        population = re.search(r"Population:\s*(.+?);\s*variable:", memo, re.I)
        variable_type = re.search(r"variable:\s*(.+?);\s*suitable display:", memo, re.I)
        display = re.search(r"suitable display:\s*(.+?)\.\s*Check", memo, re.I)
        if not all((scenario,population,variable_type,display)):
            raise ValueError(f"{item['ID']}: data-language question is missing its structured classification")
        return VisualizationInstruction(type="statistics",template="data_studio",parameters={
            **common,"sample_size":int(scenario.group(2)),"variable":scenario.group(1),
            "population":population.group(1),"variable_type":variable_type.group(1),"display":display.group(1),
        })
    if family == "five_number_ribbon":
        summary = numeric_list(memo, r"^\s*\(([^)]+)\)")
        return VisualizationInstruction(type="statistics", template="five_number_summary", parameters={**common, "five_number_summary": summary})
    if family == "ogive_builder":
        bounds = numeric_list(prompt, r"Classes end at\s*([^w]+?)\s+with frequencies")
        cumulative = numeric_list(memo, r"Cumulative frequencies\s*=\s*\[([^\]]+)\]")
        return VisualizationInstruction(type="statistics", template="ogive", parameters={**common, "upper_boundaries": bounds, "cumulative_frequencies": cumulative})
    if family == "outlier_fence_lab":
        values = numeric_list(prompt)
        q1 = float(re.search(r"Q1\s*=\s*(-?\d+(?:\.\d+)?)", memo).group(1))
        q3 = float(re.search(r"Q3\s*=\s*(-?\d+(?:\.\d+)?)", memo).group(1))
        fences = re.search(r"fences\s+(-?\d+(?:\.\d+)?)\s+to\s+(-?\d+(?:\.\d+)?)", memo, re.I)
        return VisualizationInstruction(type="statistics", template="outlier_fence", parameters={**common, "q1": q1, "q3": q3, "lower_fence": float(fences.group(1)), "upper_fence": float(fences.group(2)), "values": values})
    if family == "deviation_calculator_lab":
        values = numeric_list(prompt)
        variance = float(re.search(r"variance\s*=\s*(-?\d+(?:\.\d+)?)", memo, re.I).group(1))
        sd = float(re.search(r"deviation\s*=.*?=\s*(-?\d+(?:\.\d+)?)", memo, re.I).group(1))
        return VisualizationInstruction(type="statistics", template="deviation_panel", parameters={**common, "values": values, "mean": sum(values) / len(values), "variance": variance, "standard_deviation": sd})
    if family == "distribution_comparison":
        match = re.search(r"Class A has mean\s+(-?\d+(?:\.\d+)?)\s+and standard deviation\s+(-?\d+(?:\.\d+)?); Class B has mean\s+(-?\d+(?:\.\d+)?)\s+and standard deviation\s+(-?\d+(?:\.\d+)?)", prompt, re.I)
        return VisualizationInstruction(type="statistics", template="distribution_comparison", parameters={**common, "mean_a": float(match.group(1)), "sd_a": float(match.group(2)), "mean_b": float(match.group(3)), "sd_b": float(match.group(4))})
    if family in {"scatter_builder", "influence_lab"}:
        x, y = paired_lists(prompt)
        return VisualizationInstruction(type="statistics", template="scatter_plot", parameters={**common, "x_values": x, "y_values": y, **({"outlier_index": len(x) - 1} if family == "influence_lab" else {})})
    if family == "correlation_continuum":
        coefficient = float(re.search(r"r\s*=\s*(-?\d+(?:\.\d+)?)", prompt).group(1))
        return VisualizationInstruction(type="statistics", template="correlation_continuum", parameters={**common, "r": coefficient})
    if family in {"least_squares_fit", "regression_calculator", "interpolation_trace", "extrapolation_risk_zone", "integrated_statistics_dashboard", "question_first_assessment"}:
        x, y = paired_lists(prompt)
        equation = re.search(r"(?:y-hat|a)\s*=\s*(-?\d+(?:\.\d+)?)\s*\+\s*(?:b\s*=\s*)?(-?\d+(?:\.\d+)?)\s*x", f"{prompt} {memo}", re.I)
        if not equation:
            coefficients = re.search(r"a\s*=\s*(-?\d+(?:\.\d+)?),\s*b\s*=\s*(-?\d+(?:\.\d+)?)", memo, re.I)
            intercept, slope = float(coefficients.group(1)), float(coefficients.group(2))
        else:
            intercept, slope = float(equation.group(1)), float(equation.group(2))
        observed = re.search(r"observed x-values from\s*(-?\d+(?:\.\d+)?)\s*to\s*(-?\d+(?:\.\d+)?)", prompt, re.I)
        x_min, x_max = (float(observed.group(1)), float(observed.group(2))) if observed else (min(x), max(x))
        estimate = re.search(r"(?:when|at)\s*x\s*=\s*(-?\d+(?:\.\d+)?)", prompt, re.I)
        parameters = {**common, "x_min": x_min, "x_max": x_max, "intercept": intercept, "slope": slope}
        if x and y:
            parameters.update({"x_values": x, "y_values": y})
        if estimate:
            parameters["estimate_x"] = float(estimate.group(1))
        return VisualizationInstruction(type="statistics", template="regression_line", parameters=parameters)
    values = numeric_list(prompt)
    if len(values) >= 2:
        return VisualizationInstruction(type="statistics", template="data_table", parameters={**common, "values": values, "sorted_values": sorted(values)})
    return VisualizationInstruction(type="statistics", template=family, parameters={"prompt": prompt[:160], "answer": memo[:160], "method": "Use the question data", "family": family, "objects": object_ids})

def geometry_visualization(item: dict, family: str, object_ids: list[str], method: str) -> VisualizationInstruction:
    prompt, memo = item["Problem"], item["Worked evidence / memo"]
    points = re.findall(r"([A-Z])\((-?\d+(?:\.\d+)?),\s*(-?\d+(?:\.\d+)?)\)", prompt)
    if family == "coordinate_distance_lab" and len(points) >= 2:
        dx = re.search(r"Delta x\s*=\s*(-?\d+(?:\.\d+)?)", memo)
        dy = re.search(r"Delta y\s*=\s*(-?\d+(?:\.\d+)?)", memo)
        return VisualizationInstruction(type="coordinate_geometry", template=family, parameters={
            "x_values":[float(points[0][1]),float(points[1][1])], "y_values":[float(points[0][2]),float(points[1][2])],
            "labels":[points[0][0],points[1][0]], "delta_x":float(dx.group(1)), "delta_y":float(dy.group(1)),
            "title":prompt[:120], "objects":object_ids,
        })
    if family == "circle_construction" and points:
        radius = re.search(r"radius\s+(-?\d+(?:\.\d+)?)", prompt, re.I)
        return VisualizationInstruction(type="coordinate_geometry", template=family, parameters={
            "centre_x":float(points[0][1]), "centre_y":float(points[0][2]), "radius":float(radius.group(1)),
            "title":prompt[:120], "objects":object_ids,
        })
    combined = f"{prompt} {memo}"
    scene_points = points or [("O", "0", "0")]
    parameters = {
        "x_values":[float(point[1]) for point in scene_points],
        "y_values":[float(point[2]) for point in scene_points],
        "labels":[point[0] for point in scene_points],
        "values":numeric_list(combined)[:40] or [0.0],
        "result":memo[:160], "title":prompt[:120], "objects":object_ids,
    }
    def parsed_number(token: str) -> float:
        if "/" in token:
            numerator, denominator = token.split("/", 1)
            return float(numerator) / float(denominator)
        return float(token)
    number_token = r"-?\d+(?:\.\d+)?(?:/\d+(?:\.\d+)?)?"
    midpoint = re.search(rf"(?:M|Midpoint\s+CT).*?\((-?\d+(?:\.\d+)?),\s*(-?\d+(?:\.\d+)?)\)(?:\.|$)", memo, re.I)
    centre = re.search(r"centre\s*\((-?\d+(?:\.\d+)?),\s*(-?\d+(?:\.\d+)?)\)", combined, re.I)
    radius = re.search(r"(?:circle\s+radius\s+is\s+|radius(?:\s+|\s*=\s*)|\br\s*=\s*)(-?\d+(?:\.\d+)?)", combined, re.I)
    gradients = re.findall(rf"(?:gradient|m(?:_[A-Za-z]+)?)\s*=\s*({number_token})", combined, re.I)
    inclination = re.search(r"theta\s*=\s*(-?\d+(?:\.\d+)?)", memo, re.I)
    intercept = re.search(r"y\s*=\s*-?\d+(?:\.\d+)?x\s*\+\s*(-?\d+(?:\.\d+)?)", memo, re.I)
    tangent_length = re.search(r"PT\s*=.*?=\s*(-?\d+(?:\.\d+)?)", memo, re.I)
    if midpoint: parameters.update({"midpoint_x":float(midpoint.group(1)), "midpoint_y":float(midpoint.group(2))})
    if centre: parameters.update({"centre_x":float(centre.group(1)), "centre_y":float(centre.group(2))})
    if radius: parameters["radius"] = float(radius.group(1))
    if gradients:
        parameters["gradient"] = parsed_number(gradients[0])
        if len(gradients) > 1: parameters["secondary_gradient"] = parsed_number(gradients[1])
    elif family == "slope_triangle" and len(scene_points) >= 2:
        dx = float(scene_points[1][1]) - float(scene_points[0][1])
        if dx: parameters["gradient"] = (float(scene_points[1][2]) - float(scene_points[0][2])) / dx
    if family == "line_equation_link":
        stated_gradient = re.search(rf"gradient\s+({number_token})", prompt, re.I)
        if stated_gradient: parameters["gradient"] = parsed_number(stated_gradient.group(1))
    if inclination: parameters["inclination"] = float(inclination.group(1))
    if intercept: parameters["line_intercept"] = float(intercept.group(1))
    if tangent_length: parameters["tangent_length"] = float(tangent_length.group(1))
    if family == "external_tangent_length":
        op_distance = re.search(r"OP\s*=\s*(-?\d+(?:\.\d+)?)", prompt, re.I)
        if op_distance: parameters["op_distance"] = float(op_distance.group(1))
    if family == "complete_square_morph":
        derived = re.search(r"centre\s*\((-?\d+(?:\.\d+)?),\s*(-?\d+(?:\.\d+)?)\),\s*radius\s+(-?\d+(?:\.\d+)?)", memo, re.I)
        if derived: parameters.update({"centre_x":float(derived.group(1)), "centre_y":float(derived.group(2)), "radius":float(derived.group(3))})
    if family == "circle_condition_intersection":
        circle = re.search(r"\(x-\((-?\d+(?:\.\d+)?)\)\)\^2\+\(y-\((-?\d+(?:\.\d+)?)\)\)\^2=(-?\d+(?:\.\d+)?)", prompt)
        if circle: parameters.update({"centre_x":float(circle.group(1)), "centre_y":float(circle.group(2)), "radius":float(circle.group(3)) ** .5})
    if family in {"radius_tangent_contact", "tangent_equation_construction", "integrated_coordinate_scene", "question_first_assessment"}:
        centre_point = next((point for point in scene_points if point[0] == "C"), None)
        if centre_point: parameters.update({"centre_x":float(centre_point[1]), "centre_y":float(centre_point[2])})
    if family == "inclination_arc":
        input_gradient = re.search(r"m\s*=\s*(-?\d+(?:\.\d+)?)", prompt)
        if input_gradient: parameters["gradient"] = float(input_gradient.group(1))
    return VisualizationInstruction(type="coordinate_geometry", template=family, parameters=parameters)


def fallback_board(lesson: dict, item: dict, topic_key: str, family: str) -> WhiteboardBlock:
    prompt = item["Problem"]
    memo = item["Worked evidence / memo"]
    prefix = slug(item["ID"])
    states = [prompt, "Method selected from the lesson-native representation", memo]
    objects = [
        SemanticObject(id=f"{prefix}-source", type="label", value="complete question source"),
        SemanticObject(id=f"{prefix}-method", type="operation", value="selected method"),
        SemanticObject(id=f"{prefix}-evidence", type="result", value="worked evidence"),
    ]
    steps = [
        TeachingStep(
            id=f"{prefix}-step-00", step_number=0, title="Read and orient",
            before_expression=states[0], working_expression="Identify the givens, representation and target.",
            operation=MathematicalOperation(type="timeline_orient"),
            after_expression=states[1],
            explanation=StepExplanation(what="Read the complete source.", why="The representation determines the method.", purpose="Identify what is given and required.", remember="Do not infer evidence from appearance."),
            animation_template="semantic_timeline", screen_reader_description=prompt,
            instructional_goal="Orient to the complete source before selecting a method.",
            duration_ms=900, events=[TimelineEvent(at_ms=0, type="show_question", targets=[f"{prefix}-source"]), TimelineEvent(at_ms=500, type="checkpoint", targets=[f"{prefix}-method"], text="Predict the next defensible step.", checkpoint_type="predict_next_step")],
            visualization_state=VisualizationState(objects=[item.id for item in objects], highlights=[f"{prefix}-source"], annotations=["visual-stage:0"]),
        ),
        TeachingStep(
            id=f"{prefix}-step-01", step_number=1, title="Apply and verify",
            before_expression=states[1], working_expression="Apply the selected method and retain the required evidence.",
            operation=MathematicalOperation(type="timeline_verify"),
            after_expression=states[2],
            explanation=StepExplanation(what=memo, why="This is the approved evidence route.", purpose="Connect the result to the source and required conclusion.", remember=lesson["pass_contract"]),
            animation_template="semantic_timeline", screen_reader_description=memo,
            instructional_goal="Verify the result against the original source and required conclusion.",
            duration_ms=900, events=[TimelineEvent(at_ms=0, type="reveal", targets=[f"{prefix}-evidence"]), TimelineEvent(at_ms=500, type="verify", targets=[f"{prefix}-source", f"{prefix}-evidence"])],
            visualization_state=VisualizationState(objects=[item.id for item in objects], highlights=[f"{prefix}-evidence"], annotations=["visual-stage:1"]),
        ),
    ]
    return WhiteboardBlock(
        id=f"{prefix}-board", representation="visual", problem=prompt,
        initial_expression=prompt, steps=steps, semantic_objects=objects,
        visualization=statistics_visualization(item, family, [item.id for item in objects]) if topic_key == "statistics" else geometry_visualization(
            item, family, [item.id for item in objects], lesson["requirements"]["Mastery objective"]),
    )

BOX_PLOT_OBJECTS = [
    "boxplot-axis", "boxplot-values", "boxplot-minimum", "boxplot-q1", "boxplot-median",
    "boxplot-q3", "boxplot-maximum", "boxplot-left-whisker",
    "boxplot-right-whisker", "boxplot-box", "boxplot-iqr",
    "boxplot-range", "boxplot-conclusion",
]

def box_plot_board(lesson: dict, item: dict) -> WhiteboardBlock:
    match = re.search(
        r"five-number summary\s*\(\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*\)",
        item["Problem"], re.I,
    )
    if not match:
        raise ValueError(f"{item['ID']}: box-plot question has no parseable five-number summary")
    minimum, q1, median, q3, maximum = (float(value) for value in match.groups())
    iqr, data_range = q3 - q1, maximum - minimum
    values = [minimum, q1, median, q3, maximum]
    prefix = slug(item["ID"])
    objects = [
        SemanticObject(id=identifier, type="result" if identifier in {"boxplot-iqr", "boxplot-range", "boxplot-conclusion"} else "label", value=identifier.replace("boxplot-", " ").replace("-", " "))
        for identifier in BOX_PLOT_OBJECTS
    ]
    actions = [
        ("Orient to the axis", "Show the complete question and a scaled number axis before constructing the plot.", "boxplot-axis"),
        ("Reveal the summary", "The five-number summary supplies the minimum, first quartile, median, third quartile and maximum.", "boxplot-values"),
        ("Place the minimum", f"Place the minimum at {minimum:g} on the number axis.", "boxplot-minimum"),
        ("Place the first quartile", f"Place the first quartile at {q1:g}.", "boxplot-q1"),
        ("Place the median", f"Place the median at {median:g}; this is the centre of the distribution.", "boxplot-median"),
        ("Place the third quartile", f"Place the third quartile at {q3:g}.", "boxplot-q3"),
        ("Place the maximum", f"Place the maximum at {maximum:g}.", "boxplot-maximum"),
        ("Construct the box", f"Draw the box from {q1:g} to {q3:g}; it contains the middle half of the data.", "boxplot-box"),
        ("Draw the median line", f"Draw the median line at {median:g} inside the box.", "boxplot-median"),
        ("Extend the whiskers", f"Extend the whiskers from {minimum:g} to {q1:g} and from {q3:g} to {maximum:g}.", "boxplot-left-whisker"),
        ("Calculate the IQR", f"The interquartile range is {q3:g} minus {q1:g}, which equals {iqr:g}.", "boxplot-iqr"),
        ("Calculate the range", f"The range is {maximum:g} minus {minimum:g}, which equals {data_range:g}.", "boxplot-range"),
        ("Interpret the plot", f"The centre is the median, {median:g}, and the middle half spans {iqr:g} units.", "boxplot-conclusion"),
        ("Verify the construction", f"Verify the ordered values {', '.join(f'{value:g}' for value in values)} against every marker, box boundary and whisker.", "boxplot-conclusion"),
    ]
    steps = []
    visible = ["boxplot-axis"]
    target_expansions = {
        1: ["boxplot-values"],
        7: ["boxplot-box"], 8: ["boxplot-median"],
        9: ["boxplot-left-whisker", "boxplot-right-whisker"],
        10: ["boxplot-iqr"], 11: ["boxplot-range"], 12: ["boxplot-conclusion"],
    }
    previous = item["Problem"]
    for index, (title, narration, target) in enumerate(actions):
        added = target_expansions.get(index, [target])
        after_visible = list(dict.fromkeys([*visible, *added]))
        after = narration if index < len(actions) - 1 else item["Worked evidence / memo"]
        event_type = "verify" if index == len(actions) - 1 else "reveal"
        operation = "timeline_orient" if index == 0 else "timeline_verify" if index == len(actions) - 1 else "timeline_inspect"
        events = [
            TimelineEvent(at_ms=0, type="focus", targets=[target]),
            TimelineEvent(at_ms=250, type=event_type, targets=added, style="verification" if event_type == "verify" else "operation"),
            TimelineEvent(at_ms=500, type="narration", text=narration),
            TimelineEvent(at_ms=500, type="caption", text=narration),
        ]
        steps.append(TeachingStep(
            id=f"{prefix}-boxplot-step-{index:02}", step_number=index, title=title,
            before_expression=previous, working_expression=narration,
            operation=MathematicalOperation(type=operation), after_expression=after,
            explanation=StepExplanation(what=title, why=narration, purpose="Build one mathematically meaningful component at a time.", remember=lesson["pass_contract"]),
            animation_template="semantic_timeline", screen_reader_description=narration,
            visualization_state=VisualizationState(objects=after_visible, highlights=[target], annotations=[f"boxplot-stage:{index}"]),
            instructional_goal=title, duration_ms=2600, events=events, narration=narration,
            state_after={"visible_objects": after_visible, "stage": index},
        ))
        visible, previous = after_visible, after
    return WhiteboardBlock(
        id=f"{prefix}-board", representation="visual", problem=item["Problem"],
        initial_expression=item["Problem"], steps=steps, semantic_objects=objects,
        visualization=VisualizationInstruction(
            type="statistics", template="box_plot",
            parameters={"minimum": minimum, "q1": q1, "median": median, "q3": q3, "maximum": maximum,
                        "title": "Five-number summary", "show_labels": True, "show_iqr": True, "show_range": True},
        ),
    )


def guided_questions(lesson: dict, topic_key: str, family: str) -> list[WhiteboardQuestion]:
    result = []
    for order, item in enumerate(lesson["guided_examples"], 1):
        difficulty, cognitive, marks = level_fields(item["Level"])
        combined = f"{item['Problem']} {item['Worked evidence / memo']}".casefold()
        approximate = "approximately" in combined or "approximate" in combined
        result.append(WhiteboardQuestion(
            id=item["ID"], order=order, difficulty=difficulty, estimated_minutes=6,
            is_core_example=order == 1,
            guidance_level="high" if order <= 2 else "moderate" if order <= 5 else "reduced" if order <= 8 else "minimal",
            whiteboard=box_plot_board(lesson, item) if topic_key == "statistics" and family == "box_plot_builder" else fallback_board(lesson, item, topic_key, family), cognitive_level=cognitive,
            marks=marks, answer=item["Worked evidence / memo"], full_memo=[item["Worked evidence / memo"]],
            misconception_tags=[lesson["requirements"]["Primary analytics tag"]],
            calculator_allowed=topic_key == "statistics", operation_signature=operation_signature(item["Level"], item["Problem"]),
            expected_evidence=item["Worked evidence / memo"], answer_tolerance=1.0 if approximate else None,
            approximate_answer=approximate,
        ))
    return result


def solution_steps(answer: str) -> list[WorkedSolutionStep]:
    parts = [part.strip() for part in re.split(r"(?<=[.!?])\s+", answer) if part.strip()]
    if not parts:
        parts = [answer]
    while len(parts) < 4:
        parts.append(parts[-1])
    return [WorkedSolutionStep(expression=f"Evidence {index}", explanation=part, why="Required by the approved memo route.", verification=answer if index == len(parts) else "") for index, part in enumerate(parts, 1)]


def concise_accepted_answer(answer: str) -> str:
    """Keep the full rubric while allowing the current exact-text checker a short response."""
    sentences = [part.strip() for part in re.split(r"(?<=[.!?])\s+", answer) if part.strip()]
    return sentences[0][:500] if sentences else answer[:500]


def practice_questions(lesson: dict, source: str) -> list[PracticeQuestion]:
    hints = [row["Rule"] for row in lesson["support_contract"] if row["Stage"].startswith("Hint")]
    result = []
    for order, item in enumerate(lesson["practice_questions"], 1):
        required_level = "Foundation" if order <= 2 else "Routine" if order <= 5 else "Complex" if order <= 9 else "Exam-level"
        difficulty, cognitive, marks = level_fields(required_level)
        prompt, answer = item["Independent problem"], item["Answer / feedback route"]
        combined = f"{prompt} {answer}".casefold()
        approximate = "approximately" in combined or "approximate" in combined
        result.append(PracticeQuestion(
            id=item["ID"], lesson_id=lesson["id"], question_number=order,
            difficulty=difficulty, cognitive_level=cognitive, marks=min(marks, 6), type="short_text",
            prompt=prompt, accepted_answers=list(dict.fromkeys([concise_accepted_answer(answer), answer])), hints=hints,
            worked_solution=solution_steps(answer), misconception_tags=[lesson["requirements"]["Primary analytics tag"]],
            verification={"approved_memo": answer}, correct_feedback="Correct. Compare your evidence with the approved feedback route.",
            source=source, expected_evidence=answer, feedback_route=answer,
            operation_signature=operation_signature(required_level, prompt), reasoning_demands=demands(required_level, prompt),
            answer_tolerance=1.0 if approximate else None, approximate_answer=approximate,
        ))
    return result


def build_pack(pack: dict, families: list[str], topic_key: str, source: str) -> tuple[list[Lesson], dict[str, list[PracticeQuestion]]]:
    pronunciation = (["y-hat", "r", "sigma", "squared units"] if topic_key == "statistics" else ["ordered pairs", "negative coordinates", "angle notation", "squared units"])
    lessons = []
    banks = {}
    for lesson, family in zip(pack["lessons"], families):
        questions = guided_questions(lesson, topic_key, family)
        banks[lesson["id"]] = practice_questions(lesson, source)
        teaching = " ".join(value for value in lesson["teaching"] if value not in {"Teach the mathematical idea", "Lesson-native whiteboard"})
        assessment = lesson["order"] == len(pack["lessons"])
        lessons.append(Lesson(
            id=lesson["id"], order=lesson["order"], title=lesson["title"],
            objective=lesson["requirements"]["Mastery objective"],
            why_it_matters=f"This is a {pack['scope']['Official weighting']} Grade 12 Mathematics Paper 2 topic.",
            intuition=teaching, prerequisites=[] if lesson["order"] == 1 else [pack["lessons"][lesson["order"] - 2]["id"]],
            estimated_minutes=65, difficulty="exam" if assessment else "standard",
            access_level=AccessLevel.FREE if lesson["order"] == 1 else AccessLevel.PREMIUM,
            status=ContentStatus.TEACHER_REVIEW_REQUIRED, mastery_threshold=.8,
            blocks=[
                LessonBlock(type="concept", title="Teach the mathematical idea", content=teaching, data={"source": pack["source"], "mastery_objective": lesson["requirements"]["Mastery objective"]}),
                questions[0].whiteboard,
                LessonBlock(type="mistake", title="Misconception diagnosis and repair", content=f"Tag the first invalid decision with {lesson['requirements']['Primary analytics tag']} and replay only the missing concept."),
                LessonBlock(type="practice", title="Timed question-first assessment" if assessment else "Self-guided practice", content="Attempt and submit independently before any answer, hint or worked memo is available.", data={"practice_bank_id": lesson["id"], "question_first": True, "timed": assessment, "answer_hidden_before_submission": True, "reassessment": "changed_parallel_item", "support_contract": lesson["support_contract"]}),
                LessonBlock(type="summary", title="Completion contract", content=lesson["pass_contract"]),
            ],
            whiteboard_questions=questions, paper="Paper 2",
            presentation_contract=presentation_contract(lesson, family, pronunciation),
            source_document=pack["source"], source_sha256=pack["source_sha256"],
            assessment_contract={"question_first": True, "timed": assessment, "marks": 20 if assessment and topic_key == "statistics" else 40 if assessment else None, "worked_content_locked_until_submission": True, "changed_parallel_reassessment": True, "blueprint": pack["assessment_blueprint"] if assessment else []},
        ))
    return lessons, banks


STATISTICS_REGRESSION_LESSONS, STATISTICS_PRACTICE_BANKS = build_pack(STATISTICS_PACK, STATISTICS_CANVAS_FAMILIES, "statistics", STATISTICS_SOURCE)
ANALYTICAL_GEOMETRY_LESSONS, ANALYTICAL_GEOMETRY_PRACTICE_BANKS = build_pack(ANALYTICAL_GEOMETRY_PACK, ANALYTICAL_GEOMETRY_CANVAS_FAMILIES, "analytical_geometry", ANALYTICAL_GEOMETRY_SOURCE)
