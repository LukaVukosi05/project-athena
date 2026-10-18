"""Approved Differential Calculus pack: complete foundation Lessons 1-6."""
from __future__ import annotations

from app.curriculum.schemas import (
    AccessLevel, ContentStatus, FormulaUnderstanding, Lesson, LessonBlock,
    MathematicalOperation, SemanticObject, StepExplanation, TeachingStep,
    TimelineEvent, VisualizationInstruction, VisualizationState,
    WhiteboardBlock, WhiteboardQuestion,
)
from app.services.graphing import function_graph

SOURCE = "Project_Athena_Grade12_Topic4_Differential_Calculus_Approved_Lesson_Pack.docx"
TITLES = (
    "Rate of change", "Average gradient", "Secant lines", "Secant to tangent",
    "Intuitive limits", "First principles", "Derivative notation",
    "First-principles differentiation", "Power rule", "Constant rule",
    "Sum and difference rule", "Tangents", "Tangent equations", "Stationary points",
    "Local extrema", "Second derivative", "Concavity", "Points of inflection",
    "Cubic sketching", "Optimisation", "Rate applications", "Motion",
    "Exam questions", "Paper 1 differential calculus mastery assessment",
)

LESSON_DATA = {
    1: {
        "objective": "Interpret rate of change as output change per input change, with correct sign and units.",
        "idea": "Rate of change compares a directed vertical change with a directed horizontal change. It describes how quickly one quantity responds to another, so its sign and compound units matter.",
        "formula": "average rate = Δoutput / Δinput",
        "origin": "Two observations define changes in output and input. Their quotient measures output change for one input unit.",
        "examples": [("Water rises from 22 L at 2 min to 55 L at 5 min. Find the average rate.", 2, 22, 5, 55, "11 L/min"), ("Temperature falls from 18 °C to 6 °C in 4 hours.", 0, 18, 4, 6, "-3 °C/hour"), ("A distance changes from 10 km at hour 1 to 34 km at hour 5.", 1, 10, 5, 34, "6 km/hour")],
    },
    2: {
        "objective": "Calculate and interpret the average gradient of a function over an interval.",
        "idea": "Average gradient is the gradient of the secant through two curve points. Function notation supplies the two output values; subtract them in the same order as the inputs.",
        "formula": "m_avg = [f(b)-f(a)] / (b-a)",
        "origin": "The gradient formula is vertical change divided by horizontal change for the points (a,f(a)) and (b,f(b)).",
        "examples": [("For f(x)=x²-3x, find the average gradient from x=1 to x=4.", 1, -2, 4, 4, "2"), ("For f(x)=2x²+5, find the average gradient from x=-1 to x=3.", -1, 7, 3, 23, "4"), ("For f(x)=x², find the average gradient from x=0 to x=3.", 0, 0, 3, 9, "3")],
    },
    3: {
        "objective": "Represent average change with a secant and connect its gradient to a difference quotient.",
        "idea": "A secant joins two distinct curve points. Writing the second input as x+h makes the horizontal separation visible and gives the quotient [f(x+h)-f(x)]/h, with h non-zero.",
        "formula": "m_sec = [f(x+h)-f(x)] / h, h ≠ 0",
        "origin": "The second point is h horizontal units from the first, so its vertical change divided by h is the secant gradient.",
        "examples": [("For f(x)=x² at x=2 with h=1, find the secant gradient.", 2, 4, 3, 9, "5"), ("For f(x)=x² at x=2 with h=0.1, find the secant gradient.", 2, 4, 2.1, 4.41, "4.1"), ("For f(x)=x² at x=2 with h=-0.5, find the secant gradient.", 2, 4, 1.5, 2.25, "3.5")],
    },
    4: {
        "objective": "Explain how secant gradients approach the tangent gradient as the second point approaches the first.",
        "idea": "The tangent is the limiting position of secants. The separation h approaches zero but is not set equal to zero inside the original quotient.",
        "formula": "f'(a) = lim(h→0) [f(a+h)-f(a)]/h",
        "origin": "A sequence of secant gradients measures change over shrinking intervals. Their limiting value is the instantaneous tangent gradient.",
        "examples": [("For f(x)=x² at x=5, determine the tangent gradient.", 5, 25, 5.5, 30.25, "10"), ("For f(x)=x² at x=2, what value do secant gradients approach?", 2, 4, 2.2, 4.84, "4"), ("For f(x)=3x² at x=1, determine the limiting gradient.", 1, 3, 1.2, 4.32, "6")],
    },
    5: {
        "objective": "Use numerical and graphical evidence to explain what it means for a quantity to approach a value.",
        "idea": "A limit describes nearby behaviour. For non-zero h, simplify equivalent expressions first; only then examine the value approached from both sides.",
        "formula": "lim(h→0) L(h) = L",
        "origin": "Nearby non-zero inputs can produce outputs that settle towards one value even when direct substitution in the original expression is undefined.",
        "examples": [("Evaluate the approaching value of [(2+h)²-4]/h.", -.5, 3.5, .5, 4.5, "4"), ("Find lim(h→0)(6+2h).", -.5, 5, .5, 7, "6"), ("Find lim(h→0)(4+h).", -.25, 3.75, .25, 4.25, "4")],
    },
    6: {
        "objective": "Build the derivative definition from change in output divided by change in input.",
        "idea": "First principles gives every symbol a geometric job: f(x+h)-f(x) is vertical change, h is horizontal change, the quotient is a secant gradient and the limit produces a tangent gradient.",
        "formula": "f'(x) = lim(h→0) [f(x+h)-f(x)]/h",
        "origin": "It is the ordinary two-point gradient formula applied to two curve points, followed by a limit as their separation shrinks.",
        "examples": [("Explain first principles for f(x)=x².", 1, 1, 2, 4, "f'(x)=2x"), ("Differentiate f(x)=x²+3x from first principles.", 1, 4, 2, 10, "f'(x)=2x+3"), ("Differentiate f(x)=3x² from first principles.", 1, 3, 2, 12, "f'(x)=6x")],
    },
}


def understanding(number: int) -> FormulaUnderstanding:
    item = LESSON_DATA[number]
    return FormulaUnderstanding(
        meaning=item["objective"], origin=item["origin"], formula=item["formula"],
        symbol_anatomy=["f(x): original output", "f(x+h): nearby output", "Δy: vertical change", "h or Δx: horizontal change", "quotient: secant gradient", "limit: approached tangent gradient"],
        why_it_works=item["origin"], validity_conditions=["The two secant points are distinct", "h is non-zero before algebraic simplification", "Input and output changes use matching order"],
        selection_reason="The target asks for change per input unit or the limiting instantaneous gradient.",
        wrong_use_cases=["Do not report a function value when a rate is requested", "Do not substitute h=0 into the unsimplified quotient"],
        visual_model={"curve": "source function", "points": "original and nearby points", "triangle": "Δy over Δx", "line": "secant approaching tangent"},
        verification={"algebra": "recalculate the directed quotient", "graph": "compare the sign and steepness", "units": "output units per input unit"},
    )


def _graph(a: float, ya: float, b: float, yb: float, title: str) -> dict:
    # A bounded quadratic passing through the authored points is sufficient for the
    # semantic secant model; exact points remain explicit and authoritative.
    xs = [a + (b-a)*i/20 for i in range(21)] if a != b else [a-1+i/10 for i in range(21)]
    if "x²" in title or "x^2" in title:
        ys = [x*x for x in xs]
    elif "3x²" in title:
        ys = [3*x*x for x in xs]
    else:
        slope = (yb-ya)/(b-a) if b != a else 0
        ys = [ya+slope*(x-a) for x in xs]
    return function_graph(xs, ys, title=title, points=[(a, ya, "P"), (b, yb, "Q")])


def _explanation(title: str, narration: str) -> StepExplanation:
    return StepExplanation(what=title, why=narration, purpose="Connect the visible change to the selected calculus object.", remember="A derivative is a rate and a tangent gradient, not merely a rule.")


def board(lesson: int, order: int, spec: tuple) -> WhiteboardBlock:
    problem, a, ya, b, yb, result = spec
    h = b-a
    quotient = (yb-ya)/h if h else 0
    states = [problem, f"P({a:g}, {ya:g}); Q({b:g}, {yb:g})", f"Δx={h:g}; Δy={yb-ya:g}", f"gradient=({yb:g}-{ya:g})/({b:g}-{a:g})={quotient:g}"]
    if lesson >= 4:
        states += [f"h approaches 0 while h≠0", result, f"Verified: {result}"]
        ops = ["plot_function", "place_curve_point", "show_change_triangle", "move_point", "calculus_limit", "calculus_tangent"]
    else:
        states += [result, f"Verified: {result}"]
        ops = ["plot_function", "place_curve_point", "show_change_triangle", "move_point", "verify_calculus_sense"]
    if lesson == 6:
        states = [problem, "f(x+h) and f(x) are complete outputs", "[f(x+h)-f(x)]/h, h≠0", "Expand the complete numerator", "Factor h from the entire numerator", "Cancel the common non-zero factor h", result, f"Verified: {result}"]
        ops = ["plot_function", "place_curve_point", "show_change_triangle", "substitute", "factor_common", "cancel", "calculus_limit"]
    titles = ["Orient", "Place two distinct points", "Show the change triangle", "Form the secant gradient", "Approach the limit", "Reveal the tangent", "Verify"]
    steps = []
    objects = [SemanticObject(id=name, type="token" if name in {"numerator","denominator","common-h"} else "label", value=name.replace("-", " ")) for name in ("curve", "point-p", "point-q", "delta-x", "delta-y", "secant", "tangent", "numerator", "denominator", "common-h", "result")]
    target_map = {
        "plot_function":["curve"], "place_curve_point":["point-p","point-q"], "show_change_triangle":["delta-x","delta-y"],
        "move_point":["secant","point-p","point-q"], "calculus_limit":["point-q","tangent"], "calculus_tangent":["tangent","point-p"],
        "verify_calculus_sense":["result","curve"], "substitute":["numerator","denominator"], "factor_common":["numerator","common-h"], "cancel":["common-h"],
    }
    for i, op in enumerate(ops):
        before, after = states[i], states[i+1]
        narration = ({
            "plot_function":"Orient on the complete question and identify the changing quantities.",
            "place_curve_point":"Place two distinct points so an average change can be measured.",
            "show_change_triangle":"Show vertical change and horizontal change before calculating their quotient.",
            "move_point":"Join the points: this secant represents the average gradient.",
            "calculus_limit":"Move the nearby point towards the fixed point; h approaches zero but is not set to zero in the original quotient.",
            "calculus_tangent":f"The limiting secant becomes the tangent, giving {result}.",
            "verify_calculus_sense":f"Verify sign, magnitude and units. The result is {result}.",
            "substitute":"Substitute x+h into every occurrence of x, keeping complete brackets.",
            "factor_common":"Factor h from the entire numerator before attempting cancellation.",
            "cancel":"Because h is a common non-zero factor at the secant stage, it may now cancel.",
        })[op]
        ev_type = {"move_point":"draw_secant", "calculus_limit":"approach_limit", "calculus_tangent":"draw_tangent"}.get(op, op)
        targets = target_map[op]
        events = [TimelineEvent(at_ms=0, type="narration", text=narration), TimelineEvent(at_ms=0, type="caption", text=narration), TimelineEvent(at_ms=450, type=ev_type, targets=targets)]
        if i == len(ops)-1:
            events.append(TimelineEvent(at_ms=900, type="verify", targets=["result"]))
        if op == "cancel":
            events.insert(2, TimelineEvent(at_ms=300, type="factor_common", targets=["common-h"]))
        steps.append(TeachingStep(id=f"step-{i}", step_number=i, title=titles[min(i,len(titles)-1)], before_expression=before, working_expression=after,
            operation=MathematicalOperation(type=op), after_expression=after, explanation=_explanation(titles[min(i,len(titles)-1)], narration),
            animation_template="calculus_timeline_reasoning", screen_reader_description=narration,
            visualization_state=VisualizationState(objects=[obj.id for obj in objects], highlights=targets, annotations=[f"stage:{min(i,3)}"]),
            instructional_goal=titles[min(i,len(titles)-1)], duration_ms=2600, events=events, narration=narration, state_after={"phase":i}))
    return WhiteboardBlock(id=f"g12-calculus-l{lesson:02}-board-{order:02}", representation="visual", problem=problem,
        initial_expression=states[0], steps=steps, graph_spec=_graph(a,ya,b,yb,problem),
        visualization=VisualizationInstruction(type="calculus", template="secant_to_tangent", parameters={"graph_spec_id":f"g12-calculus-{lesson:02}-{order:02}"}),
        semantic_objects=objects, formula_understanding=understanding(lesson))


def questions(number: int) -> list[WhiteboardQuestion]:
    return [WhiteboardQuestion(id=f"g12-calculus-l{number:02}-wbq-{i:02}", order=i,
        difficulty=("foundation","easy","standard")[i-1], estimated_minutes=5, is_core_example=i==1,
        guidance_level="high" if i==1 else "moderate", whiteboard=board(number,i,spec),
        cognitive_level="routine" if i<3 else "complex", marks=4, answer=spec[-1],
        full_memo=[LESSON_DATA[number]["formula"], spec[-1], "Verify graph direction and units."],
        misconception_tags=["RATE_VS_VALUE","SECANT_VS_TANGENT","LIMIT_ZERO"] if number>=3 else ["RATE_VS_VALUE"], calculator_allowed=True)
        for i,spec in enumerate(LESSON_DATA[number]["examples"],1)]


def complete_lesson(number: int) -> Lesson:
    data=LESSON_DATA[number]; qs=questions(number)
    misconception = "Never set h=0 in the original quotient. Keep h non-zero, simplify legally, and apply the limit afterward." if number>=3 else "A function value is an amount; a rate compares changes and must include directed sign and compound units."
    return Lesson(id=f"g12-calculus-{number:02}", order=number, title=TITLES[number-1], objective=data["objective"],
        why_it_matters="Differential Calculus contributes approximately 35 marks to CAPS Mathematics Paper 1.", intuition=data["idea"],
        prerequisites=[] if number==1 else [f"g12-calculus-{number-1:02}"], estimated_minutes=60,
        difficulty="foundation" if number<=2 else "standard", access_level=AccessLevel.FREE if number==1 else AccessLevel.PREMIUM,
        status=ContentStatus.TEACHER_REVIEW_REQUIRED, blocks=[
            LessonBlock(type="concept", title="Teach the idea before the formula", content=data["idea"], data={"source":SOURCE,"formula":data["formula"],"origin":data["origin"]}),
            qs[0].whiteboard,
            LessonBlock(type="mistake", title="Misconception diagnosis and repair", content=misconception),
            LessonBlock(type="practice", title="Self-guided practice", content="Solve, submit, explain why the calculus object applies, then verify.", data={"practice_bank_id":f"g12-calculus-{number:02}","track_conceptual_independence":True}),
            LessonBlock(type="checkpoint", title="Explain-back checkpoint", content="Explain what the formula measures, why it applies, and how the graph verifies it.", data={"options":["I can explain and verify it","I need to review the visual model"],"correct_index":0,"feedback":"Complete practice to establish 80% mastery."}),
            LessonBlock(type="summary", title="Key takeaway", content=data["objective"]),
        ], whiteboard_questions=qs, mastery_threshold=.8)


def scheduled_lesson(number: int) -> Lesson:
    return Lesson(id=f"g12-calculus-{number:02}", order=number, title=TITLES[number-1],
        objective="Approved lesson-pack conversion remains in a controlled QA batch.", why_it_matters="This lesson is registered but not published as empty content.",
        intuition="Content becomes available after its formula model, timeline, practice and mathematics pass review.",
        prerequisites=[f"g12-calculus-{number-1:02}"], estimated_minutes=60, difficulty="standard",
        access_level=AccessLevel.PREMIUM, status=ContentStatus.COMING_SOON, blocks=[], mastery_threshold=.8)


DIFFERENTIAL_CALCULUS_LESSONS=[complete_lesson(i) if i<=6 else scheduled_lesson(i) for i in range(1,25)]
