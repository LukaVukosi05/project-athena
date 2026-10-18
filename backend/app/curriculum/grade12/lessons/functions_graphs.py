"""Approved Functions and Graphs runtime: complete Lessons 1-3 plus schedule."""
from __future__ import annotations

from app.curriculum.schemas import (
    AccessLevel, ContentStatus, Lesson, LessonBlock, MathematicalOperation,
    SemanticObject, StepExplanation, TeachingStep, TimelineEvent, VisualizationInstruction, VisualizationState,
    WhiteboardBlock, WhiteboardQuestion,
)
from app.services.graphing import function_graph

SOURCE = "Project_Athena_Grade12_Topic2_Functions_and_Graphs_Approved_Lesson_Pack.docx"
TITLES = (
    "Function language, notation and representations", "Domain, range, intercepts and key features",
    "Linear functions and parameter meaning", "Quadratic functions: forms and features",
    "Quadratic graphs from limited information", "Hyperbolic functions", "Exponential functions",
    "Logarithms as inverse exponentials", "Inverse functions: concept and notation",
    "Inverse quadratic functions", "Transformations of functions", "Intersections and simultaneous equations",
    "Graphical equations and inequalities", "Average gradient and rate of change",
    "Parameters, restrictions and reconstruction", "Integrated function interpretation",
    "Functions error clinic", "Paper 1 functions mastery assessment",
)
OBJECTIVES = (
    "Interpret f(x), inputs, outputs and mappings across words, tables, equations and graphs.",
    "Determine and communicate the defining features of a graph.",
    "Analyse y=mx+c and connect gradient to constant rate of change.",
)
TEACHING = (
    "A function assigns each allowed input exactly one output. f(x) is the output produced by input x; it does not mean f multiplied by x. Domain describes allowed inputs and range describes resulting outputs.",
    "Graph analysis begins with domain, range, intercepts, turning points and asymptotes. An x-intercept has y=0; a y-intercept has x=0.",
    "For a non-vertical line, m is the change in y per unit change in x and c is the y-intercept. Parallel lines have equal gradients; perpendicular non-vertical gradients multiply to −1.",
)


def explanation(what: str, why: str, purpose: str, remember: str) -> StepExplanation:
    return StepExplanation(what=what, why=why, purpose=purpose, remember=remember)


def timed(step_number: int, title: str, before: str, working: str, after: str, operation: str,
          narration: str, targets: list[str]) -> TeachingStep:
    return TeachingStep(
        id=f"step-{step_number}", step_number=step_number, title=title,
        before_expression=before, working_expression=working,
        operation=MathematicalOperation(type=operation), after_expression=after,
        explanation=explanation(title, narration, "Connect equation, table and graph.", "Verify each exact feature."),
        animation_template="progressive_graph_reasoning", screen_reader_description=narration,
        visualization_state=VisualizationState(objects=["axes", "equation", "table", "points", "curve"],
                                               annotations=[f"stage:{step_number}"]),
        instructional_goal=title, duration_ms=2600, narration=narration,
        events=[TimelineEvent(at_ms=0, type="narration", text=narration),
                TimelineEvent(at_ms=0, type="caption", text=narration),
                TimelineEvent(at_ms=350, type="focus", targets=targets),
                TimelineEvent(at_ms=700, type="verify" if operation == "verify_result" else "reveal", targets=targets)],
        state_after={"phase": step_number},
    )


def board(lesson: int, order: int, problem: str, equation: str, xs: list[float], ys: list[float],
          points: list[tuple[float, float, str]], conclusion: str, verification: str) -> WhiteboardBlock:
    graph = function_graph(xs, ys, title=equation, points=points)
    states = [problem, f"Equation: {equation}", "Exact table and key points", conclusion, verification]
    steps = [
        timed(0, "Orient", states[0], f"Identify the function: {equation}", states[1], "read_problem", "Read the question and identify the input, output and function family.", ["equation"]),
        timed(1, "Identify structure", states[1], f"Calculate table values for {equation}", states[2], "select_method", "Identify the parameters and calculate exact values before plotting.", ["table"]),
        timed(2, "Plot exact information", states[2], "Plot each exact point before drawing the curve", states[3], "show_working", "Plot the exact points one at a time and connect them with the correct graph shape.", ["points","curve"]),
        timed(3, "Verify and summarise", states[3], f"Check: {verification}", states[4], "verify_result", verification, ["verification"]),
    ]
    objects=[SemanticObject(id=name,type="label",value=name) for name in ("axes","equation","table","points","curve","verification")]
    return WhiteboardBlock(
        id=f"g12-functions-l{lesson:02}-board-{order:02}", representation="visual",
        problem=problem, initial_expression=problem, steps=steps, graph_spec=graph,
        visualization=VisualizationInstruction(type="function_graph", template="cartesian_function",
                                               parameters={"graph_spec_id": f"g12-functions-l{lesson:02}-graph-{order:02}"}),
        semantic_objects=objects,
    )


def questions(lesson: int) -> list[WhiteboardQuestion]:
    specs = {
        1: [
            ("Build the table and graph of f(x)=2x−3.", "f(x)=2x−3", [-2,-1,0,1,2,3,4], [-7,-5,-3,-1,1,3,5], [(0,-3,"y-intercept"),(4,5,"f(4)=5")], "Each input has one output; domain and range are all real numbers.", "Substitution gives f(4)=5 and solving f(x)=5 gives x=4."),
            ("For f(x)=x²−4, find f(−3) and connect it to the graph.", "f(x)=x²−4", [-3,-2,-1,0,1,2,3], [5,0,-3,-4,-3,0,5], [(-3,5,"f(−3)=5"),(0,-4,"turning point")], "f(−3)=5.", "Substitution: (−3)²−4=5."),
            ("If g(x)=3x+1 and g(x)=19, find the input.", "g(x)=3x+1", [-2,0,2,4,6], [-5,1,7,13,19], [(6,19,"g(6)=19")], "The required input is x=6.", "3(6)+1=19."),
        ],
        2: [
            ("Determine the key features of y=x²−5x+6.", "y=x²−5x+6", [0,1,2,2.5,3,4,5], [6,2,0,-.25,0,2,6], [(2,0,"x-intercept"),(3,0,"x-intercept"),(0,6,"y-intercept"),(2.5,-.25,"turning point")], "Intercepts are (2,0), (3,0), (0,6); minimum is −1/4.", "Factorisation and substitution reproduce every labelled feature."),
            ("State the range and features of y=(x−2)²−4.", "y=(x−2)²−4", [-1,0,1,2,3,4,5], [5,0,-3,-4,-3,0,5], [(2,-4,"minimum"),(0,0,"intercept"),(4,0,"intercept")], "Domain: all real x; range: y≥−4.", "The square is non-negative, so the smallest output is −4."),
            ("Find both intercepts of y=−2x+8.", "y=−2x+8", [-1,0,1,2,3,4,5], [10,8,6,4,2,0,-2], [(0,8,"y-intercept"),(4,0,"x-intercept")], "Intercepts are (0,8) and (4,0).", "x=0 gives 8; y=0 gives x=4."),
        ],
        3: [
            ("Find the line through (2,5) and (6,13).", "y=2x+1", [-1,0,1,2,3,4,5,6], [-1,1,3,5,7,9,11,13], [(2,5,"given"),(6,13,"given"),(0,1,"intercept")], "m=2 and the equation is y=2x+1.", "Both supplied points satisfy y=2x+1."),
            ("Construct the line perpendicular to y=−3x+4 through (3,2).", "y=x/3+1", [-3,0,3,6,9], [0,1,2,3,4], [(3,2,"given"),(0,1,"intercept")], "The perpendicular gradient is 1/3; y=x/3+1.", "(−3)(1/3)=−1 and (3,2) satisfies the equation."),
            ("Interpret and graph a line with gradient −2 through (−1,4).", "y=−2x+2", [-2,-1,0,1,2,3], [6,4,2,0,-2,-4], [(-1,4,"given"),(0,2,"intercept")], "The output decreases by 2 per input unit.", "Every unit step right changes y by −2."),
        ],
    }
    levels = ["foundation", "easy", "standard"]
    return [WhiteboardQuestion(id=f"g12-functions-l{lesson:02}-wbq-{i:02}", order=i,
        difficulty=levels[i-1], estimated_minutes=5, is_core_example=i==1,
        guidance_level="high" if i==1 else "moderate", whiteboard=board(lesson,i,*spec),
        cognitive_level="routine" if i < 3 else "complex", marks=3,
        answer=spec[-2], full_memo=[spec[-2], spec[-1]], misconception_tags=["graph-feature-verification"])
        for i, spec in enumerate(specs[lesson], 1)]


def complete_lesson(number: int) -> Lesson:
    qs = questions(number)
    mistakes = (
        "Do not read f(3) as 3f. Replace x with brackets containing 3.",
        "Do not swap intercept procedures: an x-intercept lies where y=0.",
        "For perpendicular lines use the negative reciprocal and verify that the gradients multiply to −1.",
    )
    return Lesson(id=f"g12-functions-{number:02}", order=number, title=TITLES[number-1],
        objective=OBJECTIVES[number-1], why_it_matters="Functions connect equations, tables, mappings and exact graphs in CAPS Paper 1.",
        intuition=TEACHING[number-1], prerequisites=[] if number==1 else [f"g12-functions-{number-1:02}"],
        estimated_minutes=60, difficulty="foundation" if number==1 else "standard",
        access_level=AccessLevel.FREE if number==1 else AccessLevel.PREMIUM,
        status=ContentStatus.TEACHER_REVIEW_REQUIRED, blocks=[
            LessonBlock(type="concept", title="Teach the idea", content=TEACHING[number-1], data={"source":SOURCE}),
            qs[0].whiteboard,
            LessonBlock(type="mistake", title="Misconception diagnosis and repair", content=mistakes[number-1]),
            LessonBlock(type="practice", title="Self-guided practice", content="Solve, submit, then compare your method.", data={"practice_bank_id":f"g12-functions-{number:02}"}),
            LessonBlock(type="checkpoint", title="Exit quiz", content="Show your reasoning before checking the result.", data={"options":["Ready to explain and verify","Review the graph features"],"correct_index":0,"feedback":"Complete self-guided practice to establish 80% mastery."}),
            LessonBlock(type="summary", title="Key takeaway", content=OBJECTIVES[number-1]),
        ], whiteboard_questions=qs, mastery_threshold=.8)


def scheduled_lesson(number: int) -> Lesson:
    return Lesson(id=f"g12-functions-{number:02}", order=number, title=TITLES[number-1],
        objective="Coming soon — approved source extracted; runtime conversion pending review.",
        why_it_matters="This scheduled lesson is not yet published.", intuition="Content remains unavailable until its controlled conversion batch passes QA.",
        prerequisites=[f"g12-functions-{number-1:02}"], estimated_minutes=60, difficulty="standard",
        access_level=AccessLevel.PREMIUM, status=ContentStatus.COMING_SOON, blocks=[], mastery_threshold=.8)


FUNCTIONS_GRAPH_LESSONS = [complete_lesson(i) if i <= 3 else scheduled_lesson(i) for i in range(1, 19)]
