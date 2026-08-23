"""Original Paper 2 practice lessons; all require teacher review before publication."""

from app.curriculum.schemas import (
    AccessLevel, ContentStatus, Lesson, LessonBlock, MathematicalOperation,
    StepExplanation, TeachingStep, WhiteboardBlock, WhiteboardQuestion,
)


def item(prompt: str, answer: str, options: list[str], explanation: str) -> dict:
    return {"question": prompt, "answer": answer, "options": options,
            "correct_index": options.index(answer), "explanation": explanation,
            "instruction": "Work this out fully on paper before checking the solution.",
            "solution_steps": [
                f"Write down exactly what is given: {prompt}",
                "Identify what must be found. Do not look at the answer choices yet.",
                f"Choose and apply the relevant formula, definition or theorem: {explanation}",
                f"Simplify completely and check signs, coordinates, angles and units: {answer}",
                f"State the answer clearly: {answer}."
            ]}


def explain(what: str, why: str, purpose: str, remember: str) -> StepExplanation:
    return StepExplanation(what=what, why=why, purpose=purpose, remember=remember)


def worked_whiteboard(topic_id: str, level: str, row: dict) -> WhiteboardBlock:
    problem, method, answer = row["question"], row["explanation"], row["answer"]
    states = [
        ("Read and identify the target", "read_problem", topic_id,
         problem, problem,
         explain("Underline the given information and what must be found.", "A correct method starts by interpreting the question accurately.", "This prevents solving for the wrong quantity.", "Given first; required second."),
         "Choosing an option before doing the mathematics.", "problem_annotation"),
        ("Choose the mathematical method", "select_method", method,
         problem, method,
         explain("Write the relevant formula, definition or theorem.", "Naming the method makes every following line justifiable.", "This creates the plan before values are substituted.", "Formula or theorem before substitution."),
         "Writing unexplained calculator output with no method.", "method_selection"),
        ("Carry out every calculation", "show_working", answer,
         method, f"{method}; ∴ {answer}",
         explain("Substitute the given values and simplify one operation at a time.", "Visible intermediate lines reveal sign, substitution and arithmetic errors.", "This produces the result while preserving method marks.", "One equality per logical change; never jump over the working."),
         "Skipping directly from the formula to the final option.", "progressive_working"),
        ("State and check the answer", "verify_result", answer,
         f"{method}; ∴ {answer}", f"{answer} ✓",
         explain("State the answer and check it against the original question.", "A calculation is not complete until its meaning is checked.", "This catches avoidable sign, unit and interpretation errors.", "Answer the question that was asked, with units where required."),
         "Leaving an unlabeled number that does not answer the question.", "result_verification"),
    ]
    return WhiteboardBlock(id=f"g12-p2-{topic_id}-{level}-worked-example",
        problem=f"EXAM-STYLE QUESTION: {problem}", initial_expression=problem,
        steps=[TeachingStep(step_number=index, title=state[0],
            operation=MathematicalOperation(type=state[1], value=state[2]),
            before_expression=state[3], working_expression=state[4],
            after_expression=state[4], explanation=state[5],
            common_mistake=state[6], animation_template=state[7],
            screen_reader_description=f"Worked solution state {index + 1}: {state[4]}")
            for index, state in enumerate(states)])


def identity_whiteboard(identifier: str, expression: str, identity: str,
                        result: str, what: str, watch_out: str) -> WhiteboardBlock:
    """A concise, mathematics-first plan for a curated identity example."""
    specific = explain(
        what,
        f"{identity} is a standard identity that applies to this expression.",
        "Using the identity replaces the matching expression immediately.",
        "Sine squared plus cosine squared equals one.",
    )
    return WhiteboardBlock(
        id=identifier, problem=f"Simplify: {expression}", initial_expression=expression,
        steps=[
            TeachingStep(step_number=0, title="Recognise the expression",
                before_expression=expression, working_expression=expression,
                operation=MathematicalOperation(type="present_expression", value=expression),
                after_expression=expression, explanation=specific,
                common_mistake=watch_out, animation_template="expression_presentation",
                screen_reader_description=f"Simplify {expression}."),
            TeachingStep(step_number=1, title="Use the identity",
                before_expression=expression, working_expression=identity,
                operation=MathematicalOperation(type="identity_recognition", value=identity),
                after_expression=identity, explanation=specific,
                common_mistake=watch_out, animation_template="identity_highlight",
                screen_reader_description=f"Use {identity}. The expression simplifies to {result}."),
            TeachingStep(step_number=2, title="Final answer",
                before_expression=identity, working_expression=f"{expression}; = {result}",
                operation=MathematicalOperation(type="state_simplified_result", value=result),
                after_expression=f"∴ {result}",
                explanation=explain("State the simplified expression.",
                    "The matching identity has already justified the simplification.",
                    "Present the result clearly without adding an irrelevant verification step.",
                    "Use an identity only when the complete pattern matches."),
                animation_template="simplified_result",
                screen_reader_description=f"Therefore the simplified result is {result}."),
        ])


TRIG_IDENTITY_SPECS = [
    ("sin²x + cos²x", "sin²x + cos²x = 1", "1", "Recognise the Pythagorean identity.", "The squares are essential: sin x + cos x is not equal to 1."),
    ("1 - sin²x", "sin²x + cos²x = 1", "cos²x", "Rearrange the Pythagorean identity for cos²x.", "Do not drop the square on cos x."),
    ("1 - cos²x", "sin²x + cos²x = 1", "sin²x", "Rearrange the Pythagorean identity for sin²x.", "The result is sin²x, not sin x."),
    ("sin²x + cos²x + 3", "sin²x + cos²x = 1", "4", "Recognise the identity inside a larger sum.", "Replace only the matching identity, then combine constants."),
    ("2sin²x + 2cos²x", "2(sin²x + cos²x) = 2(1)", "2", "Factor out the common factor before using the identity.", "Both terms must be included inside the bracket."),
    ("(1 - cos²x) / sin²x", "1 - cos²x = sin²x", "1", "Replace the numerator using the rearranged identity.", "Cancellation requires sin x ≠ 0 in the original quotient."),
    ("sin²x / (1 - cos²x)", "1 - cos²x = sin²x", "1", "Replace the denominator using the rearranged identity.", "Keep the denominator grouped while substituting."),
    ("(1 - sin²x) / cos²x", "1 - sin²x = cos²x", "1", "Replace the numerator using the rearranged identity.", "Cancellation requires cos x ≠ 0 in the original quotient."),
    ("3sin²x + 3cos²x - 1", "3(sin²x + cos²x) = 3(1)", "2", "Factor the identity pair, then simplify the constants.", "The minus one remains after applying the identity."),
    ("sin²x + cos²x - tan²x", "sin²x + cos²x = 1", "1 - tan²x", "Replace the identity pair and retain the remaining term.", "There is no identity that makes 1 - tan²x equal to zero."),
    ("(sin²x + cos²x) / 2", "sin²x + cos²x = 1", "1 / 2", "Use the identity in the numerator.", "The denominator 2 is not part of the identity."),
    ("4 - 4sin²x", "1 - sin²x = cos²x", "4cos²x", "Factor out 4, then use the rearranged identity.", "Factor first: 4 - 4sin²x = 4(1 - sin²x)."),
]


def trig_identity_questions() -> list[WhiteboardQuestion]:
    difficulties = ["foundation"] * 3 + ["easy"] * 2 + ["standard"] * 3 + ["intermediate"] * 2 + ["exam"] + ["advanced"]
    guidance = ["high"] * 3 + ["moderate"] * 4 + ["reduced"] * 3 + ["minimal"] * 2
    return [WhiteboardQuestion(id=f"trig-identity-{index + 1:02}", order=index + 1,
        difficulty=difficulties[index], estimated_minutes=3, is_core_example=index == 0,
        guidance_level=guidance[index], whiteboard=identity_whiteboard(
            f"trig-identity-{index + 1:02}", *spec))
        for index, spec in enumerate(TRIG_IDENTITY_SPECS)]


BANKS = {
"statistics": [
 item("Find the mean of 4, 7, 9, 10, 10.", "8", ["7", "8", "9", "10"], "The total is 40 and 40÷5=8."),
 item("Find the median of 3, 5, 8, 11, 14, 20.", "9.5", ["8", "9", "9.5", "11"], "Average the middle values: (8+11)÷2=9.5."),
 item("For Q₁=12 and Q₃=28, calculate the IQR.", "16", ["12", "16", "20", "40"], "IQR=Q₃−Q₁=28−12=16."),
 item("If Q₁=10 and IQR=8, find the lower outlier fence.", "−2", ["2", "−2", "−12", "6"], "Lower fence=Q₁−1.5(IQR)=10−12=−2."),
 item("A dataset has variance 49. Find its standard deviation.", "7", ["7", "24.5", "49", "98"], "Standard deviation is the positive square root of variance."),
 item("The regression line is ŷ=2.4x+5. Predict y when x=10.", "29", ["24", "25", "29", "34"], "ŷ=2.4(10)+5=29."),
 item("For 80 values, at what cumulative frequency is the median read from an ogive?", "40", ["20", "40", "60", "80"], "The median is at n÷2=40."),
 item("For 80 values, where is Q₃ read on an ogive?", "60", ["20", "40", "60", "75"], "Q₃ is at 3n÷4=60."),
 item("If r=−0.92, describe the correlation.", "Strong negative", ["Strong positive", "Weak negative", "Strong negative", "No correlation"], "A value near −1 indicates strong negative correlation."),
 item("A box plot has min 2, Q₁=5, median 9, Q₃=12, max 18. Find its range.", "16", ["7", "10", "13", "16"], "Range=max−min=18−2=16."),
 item("Which missing calculator result completes: σ=√36=___?", "6", ["3", "6", "18", "36"], "The principal square root of 36 is 6."),
 item("The line ŷ=−3x+42 models a score. Predict at x=8.", "18", ["18", "21", "24", "34"], "−3(8)+42=18."),
],
"analytical-geometry": [
 item("Find the gradient through A(2,3) and B(6,11).", "2", ["1/2", "2", "4", "8"], "m=(11−3)/(6−2)=8/4=2."),
 item("Find the midpoint of (−2,5) and (8,−1).", "(3,2)", ["(3,2)", "(5,4)", "(6,−3)", "(3,3)"], "Average corresponding coordinates."),
 item("Find the distance between (1,2) and (4,6).", "5", ["3", "4", "5", "7"], "√[(4−1)²+(6−2)²]=√25=5."),
 item("A line has gradient 3. Find the gradient of a perpendicular line.", "−1/3", ["1/3", "−1/3", "−3", "3"], "Perpendicular gradients multiply to −1."),
 item("State the centre of (x−4)²+(y+2)²=25.", "(4,−2)", ["(−4,2)", "(4,2)", "(4,−2)", "(−4,−2)"], "Centre-radius form is (x−a)²+(y−b)²=r²."),
 item("Find the radius of x²+y²−6x+8y−11=0.", "6", ["3", "4", "5", "6"], "Complete squares: (x−3)²+(y+4)²=36."),
 item("Find the equation of the line with gradient 2 through (1,3).", "y=2x+1", ["y=2x−1", "y=2x+1", "y=x+2", "y=3x−1"], "Use y−3=2(x−1)."),
 item("The radius MP has gradient −2. What is the tangent gradient at P?", "1/2", ["−1/2", "1/2", "2", "−2"], "A radius is perpendicular to its tangent."),
 item("Find the x-intercept of y=−3x+12.", "4", ["−4", "3", "4", "12"], "Set y=0: 3x=12."),
 item("For A(−1,4), B(5,4), calculate AB.", "6", ["4", "5", "6", "10"], "The segment is horizontal: 5−(−1)=6."),
 item("Complete: m_AB×m_perpendicular=___.", "−1", ["−1", "0", "1", "undefined"], "Non-vertical perpendicular gradients have product −1."),
 item("Circle centre O(0,0) passes through (3,4). Write its equation.", "x²+y²=25", ["x²+y²=5", "x²+y²=7", "x²+y²=25", "(x−3)²+(y−4)²=25"], "The radius is 5, so r²=25."),
],
"trigonometry": [
 item("Evaluate sin 30° without a calculator.", "1/2", ["0", "1/2", "√2/2", "1"], "30° is a special angle."),
 item("If sin θ=3/5 and θ is acute, find cos θ.", "4/5", ["2/5", "3/5", "4/5", "5/4"], "Use a 3-4-5 triangle."),
 item("Simplify sin²x+cos²x.", "1", ["0", "1", "sin x", "cos x"], "This is the Pythagorean identity."),
 item("State the period of y=sin 2x.", "180°", ["90°", "180°", "360°", "720°"], "Period=360°/2."),
 item("Solve sin x=0 for 0°≤x≤360°.", "0°,180°,360°", ["0°,180°,360°", "90°,270°", "0°,360°", "180° only"], "Sine is zero on the horizontal axis."),
 item("Expand cos(A+B).", "cosA cosB−sinA sinB", ["cosA cosB−sinA sinB", "cosA cosB+sinA sinB", "sinA cosB+cosA sinB", "sinA sinB−cosA cosB"], "The cosine-plus formula contains a minus."),
 item("If cos x=−1/2, find cos 2x.", "−1/2", ["−1", "−1/2", "0", "1/2"], "cos2x=2cos²x−1=2(1/4)−1."),
 item("Solve 2cos x−1=0 for 0°≤x≤360°.", "60°,300°", ["30°,330°", "60°,300°", "120°,240°", "60° only"], "cos x=1/2 in quadrants I and IV."),
 item("In ΔABC, a=8, b=6 and C=60°. Find c².", "52", ["28", "52", "76", "100"], "Cosine rule: c²=64+36−96(1/2)=52."),
 item("Two sides are 7 and 10 with included angle 30°. Find the area.", "17.5", ["17.5", "35", "60.6", "70"], "Area=½(7)(10)sin30°=17.5."),
 item("Complete the missing step: sin(A−B)=sinA cosB ___ cosA sinB.", "−", ["+", "−", "×", "÷"], "The sine difference identity uses subtraction."),
 item("A 20 m line of sight makes a 30° elevation angle. Find the vertical height.", "10 m", ["5 m", "10 m", "17.32 m", "20 m"], "Opposite=20sin30°=10."),
],
"euclidean-geometry": [
 item("An angle at the centre is 100°. Find the angle at the circumference on the same arc.", "50°", ["25°", "50°", "100°", "200°"], "The centre angle is twice the circumference angle."),
 item("Opposite angles of a cyclic quadrilateral sum to ___.", "180°", ["90°", "180°", "270°", "360°"], "Opposite angles in a cyclic quadrilateral are supplementary."),
 item("A tangent meets radius OP at P. Find the angle between them.", "90°", ["45°", "60°", "90°", "180°"], "A tangent is perpendicular to the radius at contact."),
 item("Angles subtended by the same chord in the same segment are ___.", "equal", ["equal", "supplementary", "complementary", "double"], "This is the same-segment theorem."),
 item("If AB∥DE in ΔCDE with A on CD and B on CE, which triangles are similar?", "ΔCAB and ΔCDE", ["ΔCAB and ΔCDE", "ΔABC and ΔDCE only", "ΔCAD and ΔCBE", "None"], "Corresponding angles are equal because AB∥DE."),
 item("Two similar triangles have side scale factor 3. Find their area scale factor.", "9", ["3", "6", "9", "27"], "Areas scale by the square of the side factor."),
 item("From the same external point T, tangents TA and TB touch a circle. If TA=12, find TB.", "12", ["6", "12", "24", "Cannot determine"], "Tangents from the same external point are equal."),
 item("A line through two sides of a triangle is parallel to the third side. It divides those sides ___.", "proportionally", ["equally", "perpendicularly", "proportionally", "randomly"], "This is the proportionality theorem."),
 item("If two angles of one triangle equal two angles of another, the triangles are similar by ___.", "AA", ["AA", "SSS", "SAS congruency", "RHS"], "Two equal angle pairs establish similarity."),
 item("Complete the proof reason: ∠A₁=∠C₂ because angles in the same ___ are equal.", "segment", ["radius", "segment", "tangent", "diameter"], "Both angles are subtended by the same chord."),
 item("A diameter subtends what angle at the circumference?", "90°", ["45°", "90°", "180°", "360°"], "Angle in a semicircle is 90°."),
 item("In similar triangles, AB/DE=2/3 and DE=12. Find AB.", "8", ["6", "8", "10", "18"], "AB=(2/3)(12)=8."),
]}


def practice_lesson(topic_id: str, title: str, level: str, rows: list[dict], order: int) -> Lesson:
    display = "Foundation" if level == "foundation" else "Standard"
    return Lesson(id=f"g12-p2-{topic_id}-{level}", order=order,
        title=f"{display} worked-on-paper practice", objective=f"Solve six {display.lower()} {title} questions and justify each selected answer.",
        why_it_matters="Paper 2 awards method marks, so selecting an answer is only the final step after written working.",
        intuition="Write the formula or theorem first, substitute carefully, simplify, and only then compare your result with the choices.",
        prerequisites=[], estimated_minutes=35 if level == "foundation" else 45,
        difficulty=level, access_level=AccessLevel.FREE,
        status=ContentStatus.TEACHER_REVIEW_REQUIRED, mastery_threshold=0.7,
        blocks=[
            LessonBlock(type="concept", title="How to use this lesson", content="Do not guess from the options. Work every question on paper, circle your result, then select the matching answer."),
            worked_whiteboard(topic_id, level, rows[0]),
            LessonBlock(type="practice", title=f"{display} practice", content="Complete all six questions before opening any answer explanation.", data={"assessment_mode": "paper_multiple_choice", "questions": rows[:6]}),
            LessonBlock(type="checkpoint", title="Mastery quiz", content="Redo questions 4–6 without opening their answers. Your score is based on the selected choices.", data={"assessment_mode": "scored_multiple_choice", "questions": rows[3:6], "pass_mark": 0.67}),
            LessonBlock(type="mistake", title="Method-mark reminder", content="A correct option without written working does not prepare you for examination method marks. Keep your paper solution for review."),
            LessonBlock(type="summary", title="Next step", content="Score at least 67%, correct every written method, then continue to the next difficulty lesson."),
        ])


def mastery_lesson(topic_id: str, rows: list[dict]) -> Lesson:
    selected = [rows[index] for index in (0, 2, 4, 5, 6, 8, 10, 11)]
    return Lesson(id=f"g12-p2-{topic_id}-mastery", order=3,
        title="Comprehensive topic mastery quiz",
        objective="Complete a comprehensive eight-question quiz after showing every method on paper.",
        why_it_matters="The quiz mixes foundational knowledge, calculations, interpretation and missing-step reasoning before exact past-paper practice.",
        intuition="Treat each option as a final-answer check, not a shortcut: solve independently, then select.",
        prerequisites=[f"g12-p2-{topic_id}-foundation", f"g12-p2-{topic_id}-standard"],
        estimated_minutes=50, difficulty="challenge", access_level=AccessLevel.FREE,
        status=ContentStatus.TEACHER_REVIEW_REQUIRED, mastery_threshold=0.75,
        blocks=[
            LessonBlock(type="concept", title="Quiz rules", content="Use paper. Show formulas, substitutions, reasons and units. Do not select an option until your written answer is complete."),
            worked_whiteboard(topic_id, "mastery", selected[0]),
            LessonBlock(type="checkpoint", title="Comprehensive mastery quiz", content="The quiz increases from core recall to standard calculations and multi-step reasoning.", data={"assessment_mode": "scored_multiple_choice", "questions": selected, "pass_mark": 0.75}),
            LessonBlock(type="mistake", title="After the quiz", content="For every incorrect choice, compare the explanation with your paper working and identify the first line where your method changed."),
            LessonBlock(type="summary", title="Exam readiness", content="A pass means you are ready to attempt the exact DBE question group. A lower score means return to the matching foundation or standard lesson."),
        ])


def exam_lesson(topic_id: str, rows: list[dict]) -> Lesson:
    selected = rows[2:12]
    identity_questions = trig_identity_questions() if topic_id == "trigonometry" else []
    core_whiteboard = identity_questions[0].whiteboard if identity_questions else worked_whiteboard(topic_id, "exam", selected[0])
    return Lesson(id=f"g12-p2-{topic_id}-exam", order=4,
        title="Native DBE-style exam course",
        objective="Complete a timed, comprehensive topic assessment using DBE Paper 2 questioning patterns.",
        why_it_matters="Examination-style questions are presented inside the learning platform without making learners navigate a scanned paper.",
        intuition="Read, plan, show every line, and only then choose the option matching your independent result.",
        prerequisites=[f"g12-p2-{topic_id}-mastery"], estimated_minutes=75,
        difficulty="exam", access_level=AccessLevel.FREE,
        status=ContentStatus.TEACHER_REVIEW_REQUIRED, mastery_threshold=0.75,
        whiteboard_questions=identity_questions,
        blocks=[
            LessonBlock(type="concept", title="Exam strategy", content="The questions increase in complexity. Complete all written working on paper and reserve time to check every result."),
            core_whiteboard,
            LessonBlock(type="checkpoint", title="Comprehensive DBE-style quiz", content="Ten native questions based on the supplied Paper 2 topic and questioning styles.", data={"assessment_mode": "scored_multiple_choice", "questions": selected, "pass_mark": 0.75}),
            LessonBlock(type="summary", title="Review your script", content="For every error, find the first incorrect written line and revisit the matching learning lesson before trying again."),
        ])


PAPER2_PRACTICE = {topic: [
    practice_lesson(topic, topic.replace("-", " ").title(), "foundation", rows[:6], 1),
    practice_lesson(topic, topic.replace("-", " ").title(), "standard", rows[6:12], 2),
    mastery_lesson(topic, rows),
    exam_lesson(topic, rows),
] for topic, rows in BANKS.items()}
