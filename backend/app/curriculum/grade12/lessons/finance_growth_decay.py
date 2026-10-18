"""Approved Finance, Growth and Decay runtime: complete Lessons 1-3 plus schedule."""
from __future__ import annotations

from app.curriculum.schemas import (
    AccessLevel, ContentStatus, Lesson, LessonBlock, MathematicalOperation,
    SemanticObject, StepExplanation, TeachingStep, TimelineEvent,
    VisualizationInstruction, VisualizationState, WhiteboardBlock, WhiteboardQuestion,
)

SOURCE = "Project_Athena_Grade12_Topic3_Finance_Growth_and_Decay_Approved_Lesson_Pack.docx"
TITLES = (
    "Growth revision and financial language", "Compound interest and period matching",
    "Depreciation models", "Nominal and effective interest rates",
    "Future value of a single amount", "Present value of a single amount",
    "Annuities and payment timing", "Future-value annuities", "Present-value annuities",
    "Loans and instalments", "Outstanding loan balances", "Sinking funds",
    "Solving for time", "Timelines and changing conditions", "Comparing financial options",
    "Paper 1 finance mastery assessment",
)
OBJECTIVES = (
    "Distinguish simple growth, compound growth and decay, and identify every variable with units.",
    "Calculate compound growth with rates and time expressed in compatible periods.",
    "Choose and use straight-line or reducing-balance depreciation from contextual evidence.",
)
TEACHING = (
    "Financial mathematics models how money changes over time. Start with a cash-flow timeline: mark date 0, the valuation date, every payment, the compounding frequency and the direction in which value is moved. Simple interest acts on the original principal; compound interest acts on the changing balance.",
    "A quoted annual rate is not automatically the rate used in the exponent. If interest is compounded m times per year, the periodic rate is the nominal annual rate divided by m and the number of periods is years multiplied by m.",
    "Straight-line depreciation removes a fixed amount based on the original cost each year. Reducing-balance depreciation removes a fixed percentage of the current value. State the model before substituting because the methods produce different values.",
)


def explain(what: str, why: str, purpose: str) -> StepExplanation:
    return StepExplanation(what=what, why=why, purpose=purpose,
                           remember="Match the rate, period count and focal date before calculating.")


def step(number: int, title: str, before: str, after: str, narration: str,
         event: str, state: VisualizationState) -> TeachingStep:
    return TeachingStep(
        id=f"step-{number}", step_number=number, title=title,
        before_expression=before, working_expression=after,
        operation=MathematicalOperation(type=event), after_expression=after,
        explanation=explain(title, narration, "Make the financial movement visible before using a formula."),
        animation_template="finance_timeline_reasoning", screen_reader_description=narration,
        visualization_state=state, instructional_goal=title, duration_ms=2600, narration=narration,
        events=[TimelineEvent(at_ms=0, type="narration", text=narration),
                TimelineEvent(at_ms=0, type="caption", text=narration),
                TimelineEvent(at_ms=500, type=event, targets=["timeline", "focal-date"])],
        state_after={"phase": number},
    )


def board(lesson: int, order: int, problem: str, model: str, formula: str,
          periodic_rate_value: float, periods: int, cashflows: list[str],
          result: str, interpretation: str, direction: str = "forward") -> WhiteboardBlock:
    states = [
        problem,
        f"Timeline: date 0 to period {periods}",
        f"Model: {model}; i={periodic_rate_value:g}; n={periods}",
        f"Substitute: {formula}",
        f"Result: {result}",
        f"Verified: {interpretation}",
        f"Takeaway: {model} is valid at focal period {periods}",
    ]
    visual_states = [
        VisualizationState(objects=["timeline", "cashflows"], highlights=["date-zero"], annotations=[]),
        VisualizationState(objects=["timeline", "cashflows", "periods"], highlights=["focal-date"], annotations=["focal-date"]),
        VisualizationState(objects=["timeline", "cashflows", "periods", "rate"], highlights=["rate", "periods"], annotations=["matched-rate"]),
        VisualizationState(objects=["timeline", "cashflows", "periods", "rate", "movement"], highlights=["movement"], annotations=[direction]),
        VisualizationState(objects=["timeline", "cashflows", "periods", "rate", "movement", "result"], highlights=["result"], annotations=[direction]),
        VisualizationState(objects=["timeline", "cashflows", "periods", "rate", "movement", "result"], highlights=["result"], annotations=[direction, "verified"]),
    ]
    events = ["place_cashflow", "set_focal_date", "match_rate_period", "accumulate" if direction == "forward" else "discount", "calculate", "verify_financial_sense"]
    narrations = [
        "Orient on the cash flows: identify date zero, each amount and what must be found.",
        "Declare the focal date so every value will be compared at the same instant.",
        "Pair the periodic interest rate with the matching number of periods.",
        "Move each amount through time using the selected financial model before simplifying.",
        f"Calculate without intermediate rounding. The result is {result}.",
        interpretation,
    ]
    steps = [step(i, title, states[i], states[i+1], narrations[i], events[i], visual_states[i])
             for i, title in enumerate(("Orient", "Set focal date", "Match rate and periods", "Apply the model", "Calculate", "Verify and interpret"))]
    return WhiteboardBlock(
        id=f"g12-finance-l{lesson:02}-board-{order:02}", representation="visual",
        problem=problem, initial_expression=problem, steps=steps,
        visualization=VisualizationInstruction(type="finance", template="cashflow_timeline", parameters={
            "title": problem, "periods": periods, "periodic_rate": periodic_rate_value,
            "cashflows": cashflows, "focal_period": periods, "period_label": "period",
            "model": model, "formula": formula, "result": result, "direction": direction,
        }),
        semantic_objects=[SemanticObject(id="timeline", type="label", value="cash-flow timeline"),
                          SemanticObject(id="focal-date", type="label", value="valuation date")],
    )


SPECS = {
    1: [
        ("R8 000 earns 9% simple interest for 30 months. Find A.", "simple growth", "A=8 000(1+0.09×2.5)", .09, 3, ["R8 000 at date 0", "R9 800 at 30 months"], "R9 800.00", "The amount exceeds the principal by R1 800, which agrees with simple growth."),
        ("R8 000 earns 9% p.a. compounded annually for 2.5 years. Find A.", "compound growth", "A=8 000(1.09)^2.5", .09, 3, ["R8 000 at date 0", "R9 923.30 at 2.5 years"], "R9 923.30", "The amount exceeds the principal and compound growth is larger than simple growth over the same term."),
        ("Classify the model when interest is calculated only on the original principal.", "simple growth", "A=P(1+in)", .08, 4, ["P at date 0", "fixed interest each year", "A at year 4"], "Simple interest", "Equal rand interest is added each period because the base remains P."),
    ],
    2: [
        ("Invest R12 500 for 3 years at 8.4% p.a. compounded monthly.", "compound growth", "A=12 500(1+0.084/12)^36", .007, 36, ["R12 500 at month 0", "R16 068.34 at month 36"], "R16 068.34", "The monthly rate and 36 monthly periods match; the amount is greater than the principal."),
        ("R9 000 earns 6% p.a. compounded monthly for 2 years. Find A.", "compound growth", "A=9 000(1+0.06/12)^24", .005, 24, ["R9 000 at month 0", "R10 144.44 at month 24"], "R10 144.44", "The growth is positive and using 24 monthly periods reproduces the result."),
        ("Set up the time equation if R20 000 grows to R27 000 at 7.2% p.a. compounded quarterly.", "compound growth", "27 000=20 000(1+0.072/4)^(4t)", .018, 4, ["R20 000 at date 0", "R27 000 at quarter 4t"], "27 000=20 000(1.018)^(4t)", "The quarterly rate 0.018 is paired with 4t quarterly periods."),
    ],
    3: [
        ("A vehicle costing R480 000 depreciates by 18% p.a. reducing balance for 5 years.", "reducing-balance depreciation", "A=480 000(0.82)^5", -.18, 5, ["R480 000 at year 0", "R177 955.12 at year 5"], "R177 955.12", "The value falls but remains positive; each year's rand decrease is smaller."),
        ("Equipment costing R75 000 loses 12% of original cost each year for 6 years.", "straight-line depreciation", "A=75 000(1−0.12×6)", -.12, 6, ["R75 000 at year 0", "equal R9 000 losses", "R21 000 at year 6"], "R21 000.00", "Six equal losses of R9 000 reduce the original value to R21 000."),
        ("Compare the annual rand loss for straight-line and reducing-balance depreciation.", "model comparison", "fixed loss versus current-value percentage", -.15, 3, ["original value", "year 1", "year 2", "year 3"], "Straight-line has equal rand losses", "Reducing balance uses a shrinking base, so its rand losses decrease."),
    ],
}


def questions(lesson: int) -> list[WhiteboardQuestion]:
    levels = ("foundation", "easy", "standard")
    return [WhiteboardQuestion(
        id=f"g12-finance-l{lesson:02}-wbq-{index:02}", order=index,
        difficulty=levels[index-1], estimated_minutes=5, is_core_example=index == 1,
        guidance_level="high" if index == 1 else "moderate",
        whiteboard=board(lesson, index, *spec), cognitive_level="routine" if index < 3 else "complex",
        marks=4, answer=spec[6], full_memo=[spec[2], spec[6], spec[7]],
        misconception_tags=["rate-period", "focal-date"], calculator_allowed=True,
    ) for index, spec in enumerate(SPECS[lesson], 1)]


def complete_lesson(number: int) -> Lesson:
    qs = questions(number)
    misconceptions = (
        "Do not select one formula merely because the word interest appears. Identify whether interest acts on the original principal or changing balance.",
        "Do not use the annual rate with a monthly exponent. Divide the nominal rate by 12 and multiply years by 12.",
        "Do not mix straight-line and reducing-balance rules. Ask whether the percentage acts on original cost or current value.",
    )
    return Lesson(
        id=f"g12-finance-{number:02}", order=number, title=TITLES[number-1],
        objective=OBJECTIVES[number-1], why_it_matters="Finance contributes approximately 15 marks to CAPS Mathematics Paper 1.",
        intuition=TEACHING[number-1], prerequisites=[] if number == 1 else [f"g12-finance-{number-1:02}"],
        estimated_minutes=60, difficulty="foundation" if number == 1 else "standard",
        access_level=AccessLevel.FREE if number == 1 else AccessLevel.PREMIUM,
        status=ContentStatus.TEACHER_REVIEW_REQUIRED, blocks=[
            LessonBlock(type="concept", title="Teach the idea", content=TEACHING[number-1], data={"source": SOURCE}),
            qs[0].whiteboard,
            LessonBlock(type="mistake", title="Misconception diagnosis and repair", content=misconceptions[number-1]),
            LessonBlock(type="practice", title="Self-guided practice", content="Solve, submit, then compare your method.", data={"practice_bank_id": f"g12-finance-{number:02}"}),
            LessonBlock(type="checkpoint", title="Exit quiz", content="Explain why the rate, period count and focal date belong together.", data={"options": ["I can explain and verify them", "I need to review the timeline"], "correct_index": 0, "feedback": "Complete self-guided practice to establish 80% mastery."}),
            LessonBlock(type="summary", title="Key takeaway", content=OBJECTIVES[number-1]),
        ], whiteboard_questions=qs, mastery_threshold=.8,
    )


def scheduled_lesson(number: int) -> Lesson:
    return Lesson(
        id=f"g12-finance-{number:02}", order=number, title=TITLES[number-1],
        objective="Approved lesson-pack conversion is scheduled for a controlled QA batch.",
        why_it_matters="This scheduled lesson is not published yet.",
        intuition="Content remains unavailable until its authored timeline, practice and calculations pass review.",
        prerequisites=[f"g12-finance-{number-1:02}"], estimated_minutes=60, difficulty="standard",
        access_level=AccessLevel.PREMIUM, status=ContentStatus.COMING_SOON, blocks=[], mastery_threshold=.8,
    )


FINANCE_GROWTH_DECAY_LESSONS = [complete_lesson(i) if i <= 3 else scheduled_lesson(i) for i in range(1, 17)]
