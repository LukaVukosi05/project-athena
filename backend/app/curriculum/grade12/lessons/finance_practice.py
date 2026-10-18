"""Backend-authoritative self-guided practice for complete Finance Lessons 1-3."""
from app.practice.schemas import AnswerNormalisation, FINANCE_SOURCE, PracticeQuestion, WorkedSolutionStep


def make(lesson, number, prompt, answer, model, substitution, conclusion, verification, *,
         kind="numeric", options=None, difficulty="standard", cognitive="routine", tags=None):
    steps = [
        WorkedSolutionStep(expression="Draw the timeline", explanation="Mark date 0, all cash flows and the focal date.", why="Amounts can be combined only at one declared date.", focus=["timeline"]),
        WorkedSolutionStep(expression=model, explanation="Select the model from the financial wording.", why="The formula must describe how the balance changes.", focus=["model"]),
        WorkedSolutionStep(expression=substitution, explanation="Substitute a periodic rate and matching period count.", why="The units of i and n must agree.", focus=["substitution"]),
        WorkedSolutionStep(expression=conclusion, explanation="Calculate with full intermediate precision.", why="Money is rounded only in the final line.", focus=["answer"]),
        WorkedSolutionStep(expression=verification, explanation="Check direction, magnitude, timing and units.", why="A contextual reasonableness check can expose a wrong model.", focus=["verification"]),
    ]
    return PracticeQuestion(
        id=f"g12-finance-l{lesson:02}-p{number:02}", lesson_id=f"g12-finance-{lesson:02}",
        question_number=number, difficulty=difficulty, cognitive_level=cognitive, marks=4,
        type=kind, prompt=prompt, options=options or [], accepted_answers=[answer],
        answer_normalisation=AnswerNormalisation(accept_fraction_decimal_equivalence=kind == "numeric"),
        hints=["Draw the timeline and declare the focal date.",
               "Write i and n with matching time units before selecting a formula.",
               f"Use {model}, retain precision, then perform the reasonableness check."],
        worked_solution=steps, misconception_tags=tags or [],
        verification={"method": "financial reasonableness", "result": verification},
        correct_feedback="Correct. The model, rate, periods and focal date are compatible.", source=FINANCE_SOURCE,
    )


BANKS = {
    "g12-finance-01": [
        make(1,1,"R12 000 earns 7% simple interest for 4 years. Find A.","15360","A=P(1+in)","A=12 000(1+0.07×4)","A=R15 360","Interest earned is R3 360, equal to 12 000×0.07×4.",difficulty="foundation",tags=["RATE_PERIOD"]),
        make(1,2,"R5 000 earns 8% compounded annually for 3 years. Find A.","6298.56","A=P(1+i)^n","A=5 000(1.08)^3","A=R6 298.56","A>P, as positive compound interest requires.",tags=["PV_FV_DIRECTION"]),
        make(1,3,"Which model adds the same rand amount of interest each period?","simple interest","A=P(1+in)","Interest each period=P×i","Simple interest","The base P remains fixed.",kind="multiple_choice",options=["Simple interest","Compound interest","Reducing-balance depreciation"],difficulty="foundation",cognitive="knowledge",tags=["MODEL_SELECTION"]),
        make(1,4,"Interest is based on the original principal, but a learner uses A=P(1+i)^n. Identify the error.","wrong model","A=P(1+in)","Original principal means a fixed interest base","Wrong model","The compound formula would use a changing balance.",kind="error_analysis",options=["Wrong model","Wrong focal date","Early rounding"],cognitive="complex",tags=["MODEL_SELECTION"]),
    ],
    "g12-finance-02": [
        make(2,1,"State the monthly periodic rate as a decimal for 8.4% p.a. compounded monthly.","0.007","i=j/m","i=0.084/12","i=0.007","0.007 is 0.7% per month.",difficulty="foundation",tags=["RATE_PERIOD"]),
        make(2,2,"How many monthly compounding periods occur in 3 years?","36","n=mt","n=12×3","n=36","Three years contain 36 monthly periods.",difficulty="foundation",tags=["RATE_PERIOD"]),
        make(2,3,"R9 000 earns 6% p.a. compounded monthly for 2 years. Find A.","10144.44","A=P(1+i)^n","A=9 000(1+0.06/12)^24","A=R10 144.44","A>P and the rate and exponent are both monthly.",tags=["RATE_PERIOD","ROUNDING"]),
        make(2,4,"A learner uses i=0.084 with n=36 for 8.4% compounded monthly over 3 years. Identify the first error.","periodic rate","i=j/12","i=0.084/12=0.007","Periodic rate","The annual rate was paired incorrectly with monthly n.",kind="error_analysis",options=["Periodic rate","Number of periods","Principal"],cognitive="complex",tags=["RATE_PERIOD"]),
    ],
    "g12-finance-03": [
        make(3,1,"A R200 000 asset depreciates at 15% p.a. reducing balance for 3 years. Find its value.","122825","A=P(1−i)^n","A=200 000(0.85)^3","A=R122 825","The value decreased but remains positive.",tags=["DEPRECIATION_MODEL"]),
        make(3,2,"A R90 000 asset loses 8% of original cost each year for 5 years. Find its value.","54000","A=P(1−in)","A=90 000(1−0.08×5)","A=R54 000","Five equal losses of R7 200 give R54 000.",tags=["DEPRECIATION_MODEL"]),
        make(3,3,"Which depreciation model has equal annual rand losses?","straight-line","A=P(1−in)","Annual loss=P×i","Straight-line","The original-cost base remains fixed.",kind="multiple_choice",options=["Straight-line","Reducing balance","Compound growth"],difficulty="foundation",cognitive="knowledge",tags=["DEPRECIATION_MODEL"]),
        make(3,4,"An asset loses 12% of its current value annually, but a learner uses A=P(1−in). Identify the error.","wrong depreciation model","A=P(1−i)^n","Current value means repeated percentage decay","Wrong depreciation model","Straight-line would remove an original-cost amount.",kind="error_analysis",options=["Wrong depreciation model","Wrong focal date","Wrong currency"],cognitive="complex",tags=["DEPRECIATION_MODEL"]),
    ],
}

PRACTICE_BANKS = BANKS
PRACTICE_BY_ID = {question.id: question for bank in BANKS.values() for question in bank}
