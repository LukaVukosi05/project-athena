"""Backend-authoritative practice for complete Differential Calculus Lessons 1-6."""
from app.practice.schemas import (
    AnswerNormalisation, CALCULUS_SOURCE, PracticeQuestion, WorkedSolutionStep,
)

DATA = {
  1: [("A tank rises from 14 L at 1 min to 38 L at 4 min. Find the average rate.","8","numeric"),("Temperature changes from 20 °C to 8 °C in 3 hours. Find the signed rate.","-4","numeric"),("What units describe a change of 45 km over 3 hours?","km/hour","short_text"),("A learner reports 55 L instead of a rate. Identify the error.","rate vs value","error_analysis")],
  2: [("For f(x)=x², find the average gradient from x=1 to x=3.","4","numeric"),("For f(x)=2x²+1, find the average gradient from x=0 to x=2.","4","numeric"),("Which line represents average gradient over an interval?","secant","multiple_choice"),("Why must numerator and denominator subtraction use the same order?","preserve the directed gradient","short_text")],
  3: [("For f(x)=x² at x=3 with h=1, find the secant gradient.","7","numeric"),("For f(x)=x² at x=2 with h=0.5, find the secant gradient.","4.5","numeric"),("At the secant stage, may h equal zero?","no","multiple_choice"),("A learner calls a two-point line a tangent. Identify it correctly.","secant","error_analysis")],
  4: [("For f(x)=x², what tangent gradient is approached at x=4?","8","numeric"),("For f(x)=3x², what tangent gradient is approached at x=2?","12","numeric"),("What becomes a tangent in the limit?","secant","multiple_choice"),("What approaches zero without being set to zero in the original quotient?","h","short_text")],
  5: [("Find lim(h→0)(4+h).","4","numeric"),("Find lim(h→0)(6+2h).","6","numeric"),("Why inspect positive and negative h-values?","approach from both sides","short_text"),("May the original quotient be evaluated by dividing by zero?","no","error_analysis")],
  6: [("What does f(x+h)-f(x) represent?","vertical change","multiple_choice"),("What does h represent in first principles?","horizontal change","multiple_choice"),("When may a common h factor cancel?","after factorisation","short_text"),("State the derivative of x² obtained from first principles.","2x","short_text")],
}

OPTIONS = {
 (1,4):["rate vs value","secant vs tangent","unit conversion"], (2,3):["secant","tangent","asymptote"],
 (3,3):["no","yes","only at the first step"], (3,4):["secant","tangent","normal"],
 (4,3):["secant","vertical axis","function value"], (5,4):["no","yes","only from the right"],
 (6,1):["vertical change","horizontal change","tangent point"], (6,2):["horizontal change","vertical change","final derivative"],
}

def question(lesson: int, number: int, prompt: str, answer: str, kind: str) -> PracticeQuestion:
    formula = "change in output / change in input" if lesson < 3 else "[f(x+h)-f(x)]/h with h≠0 before the limit"
    return PracticeQuestion(
      id=f"g12-calculus-l{lesson:02}-p{number:02}", lesson_id=f"g12-calculus-{lesson:02}",
      question_number=number, difficulty="foundation" if number==1 else "standard",
      cognitive_level="knowledge" if kind=="multiple_choice" else "complex" if kind=="error_analysis" else "routine",
      marks=2 if number<4 else 4, type=kind, prompt=prompt, options=OPTIONS.get((lesson,number),[]),
      accepted_answers=[answer], answer_normalisation=AnswerNormalisation(accept_fraction_decimal_equivalence=kind=="numeric"),
      hints=["Name the target: value, average rate, secant gradient, limit or tangent gradient.",
             f"Use the visual meaning of {formula}.", "Write the directed changes first, then calculate and verify the graph sense."],
      worked_solution=[
        WorkedSolutionStep(expression="Identify the requested object", explanation="Separate a value from a rate and a secant from a tangent.", why="The target determines the valid formula.", focus=["target"]),
        WorkedSolutionStep(expression=formula, explanation="Write the formula together with its conditions.", why="Each symbol must correspond to the visual model.", focus=["formula"]),
        WorkedSolutionStep(expression=prompt, explanation="Substitute the authored information in matching order.", why="Matching order preserves the directed sign.", focus=["substitution"]),
        WorkedSolutionStep(expression=answer, explanation="Calculate or state the supported conclusion.", why="The result follows from the selected rate or limit object.", focus=["result"]),
        WorkedSolutionStep(expression="Verify using graph direction, units and conditions", explanation="Compare the answer with the curve or context.", why="Verification distinguishes a plausible calculus result from a procedural slip.", focus=["verification"]),
      ], misconception_tags=["LIMIT_ZERO" if lesson>=3 else "RATE_VS_VALUE", "SECANT_VS_TANGENT"],
      verification={"graph":"sign and steepness agree","conditions":"h remains non-zero before simplification"},
      correct_feedback="Correct. The formula choice, directed change and verification agree.", source=CALCULUS_SOURCE)

PRACTICE_BANKS={f"g12-calculus-{lesson:02}":[question(lesson,i,*item) for i,item in enumerate(items,1)] for lesson,items in DATA.items()}
PRACTICE_BY_ID={q.id:q for bank in PRACTICE_BANKS.values() for q in bank}
