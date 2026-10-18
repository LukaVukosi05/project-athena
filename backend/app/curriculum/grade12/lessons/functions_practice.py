"""Initial approved-pack practice for complete Functions Lessons 1-3."""
from app.practice.schemas import AnswerNormalisation, FUNCTIONS_SOURCE, PracticeQuestion, WorkedSolutionStep


def s(expression, explanation, why, focus):
    return WorkedSolutionStep(expression=expression, explanation=explanation, why=why, focus=[focus])


def make(lesson, number, prompt, answer, steps, *, kind="short_text", options=None,
         difficulty="standard", cognitive="routine", tags=None, feedback=None):
    return PracticeQuestion(id=f"g12-functions-l{lesson:02}-p{number:02}", lesson_id=f"g12-functions-{lesson:02}",
        question_number=number, difficulty=difficulty, cognitive_level=cognitive, marks=3, type=kind,
        prompt=prompt, options=options or [], accepted_answers=[answer], answer_normalisation=AnswerNormalisation(),
        hints=["Identify the function feature or operation requested before calculating.",
               "Use exact substitution or the defining graph condition.",
               f"Check your result against: {steps[-1][0]}."],
        worked_solution=[s(*item) for item in steps], misconception_tags=tags or [],
        verification={"method":"exact substitution or feature comparison","result":steps[-1][0]},
        correct_feedback=feedback or "Correct. Your answer agrees with the exact function evidence.",
        source=FUNCTIONS_SOURCE)


BANKS = {
"g12-functions-01": [
 make(1,1,"For f(x)=2x²−1, calculate f(−2).","7",[("f(−2)=2(−2)²−1","Substitute −2 in brackets.","Brackets preserve the negative input.","substitution"),("=2(4)−1","Evaluate the square first.","Order of operations applies.","power"),("=8−1","Multiply.","The coefficient scales the output.","product"),("=7","State the output.","f(−2) asks for an output, not an input.","answer")],kind="numeric",tags=["function-notation"]),
 make(1,2,"If h(x)=5−x and h(x)=−4, find x.","9",[("5−x=−4","Set the function expression equal to the given output.","The unknown is now the input.","equation"),("5−x−5=−4−5","Subtract 5 from both sides.","Matching operations preserve equality.","balance"),("−x=−9","Simplify.","The variable coefficient is −1.","simplify"),("x=9","Divide both sides by −1.","This isolates the input.","answer")],kind="numeric",tags=["input-output-confusion"]),
 make(1,3,"Does x²+y²=4 define y as a function of x?","no",[("x=0","Test one allowed input.","One counterexample can disprove the function rule.","input"),("y²=4","Substitute x=0.","The relation determines possible outputs.","substitute"),("y=2 or y=−2","Solve for y.","The same input has two outputs.","outputs"),("No","Apply the one-output-per-input rule.","A function cannot assign two outputs to input 0.","conclusion")],kind="multiple_choice",options=["Yes","No"],cognitive="complex",tags=["vertical-line-test"]),
 make(1,4,"State the domain of y=2x−7.","all real numbers",[("y=2x−7","Inspect the expression.","Restrictions arise from undefined operations.","equation"),("No denominator or even root","Check restriction sources.","A linear expression exists for every real x.","restriction"),("x∈R","Write the mathematical domain.","Every real input is permitted.","domain"),("All real numbers","State it in words.","Words and symbols must agree.","answer")],tags=["domain"]),
],
"g12-functions-02": [
 make(2,1,"Give both intercepts of y=−2x+8 as ordered pairs.","(4,0),(0,8)",[("0=−2x+8","Set y=0 for the x-intercept.","Points on the x-axis have y=0.","x-intercept"),("x=4","Solve.","This is the x-coordinate.","solve"),("y=−2(0)+8=8","Set x=0 for the y-intercept.","Points on the y-axis have x=0.","y-intercept"),("(4,0),(0,8)","State ordered pairs.","Intercepts are coordinates, not isolated values.","answer")],tags=["intercept-procedure"]),
 make(2,2,"State the range of y=x²+3.","y>=3",[("x²≥0","Use the square property.","A real square cannot be negative.","property"),("x²+3≥3","Translate outputs upward by 3.","Every output increases by 3.","transform"),("Minimum at (0,3)","Identify the turning point.","The minimum fixes the range boundary.","minimum"),("y≥3","State the range.","All outputs from 3 upward occur.","answer")],tags=["domain-range"]),
 make(2,3,"State the domain of y=1/(x−5).","x!=5",[("x−5≠0","Require a non-zero denominator.","Division by zero is undefined.","restriction"),("x≠5","Solve the restriction.","This identifies the excluded input.","domain"),("Vertical asymptote x=5","Connect restriction to graph.","The graph approaches but never reaches this line.","asymptote"),("Domain: x≠5","State the complete answer.","The restriction and graph agree.","answer")],tags=["restriction"]),
 make(2,4,"For y=(x−2)²−4, select the turning point.","(2,-4)",[("y=(x−p)²+q","Identify turning-point form.","This form exposes the vertex.","form"),("p=2, q=−4","Match parameters.","The inside sign is opposite the coordinate.","parameters"),("Minimum y=−4","Use the positive square coefficient.","The graph opens upward.","minimum"),("(2,−4)","State the coordinate.","It satisfies the equation and symmetry.","answer")],kind="multiple_choice",options=["(2,−4)","(−2,−4)","(2,4)"],tags=["turning-point-sign"]),
],
"g12-functions-03": [
 make(3,1,"Find the gradient through (−1,4) and (5,−8).","-2",[("m=(−8−4)/(5−(−1))","Use the same point order top and bottom.","Consistent order preserves the directed changes.","formula"),("m=−12/6","Simplify both changes.","Rise is −12 and run is 6.","changes"),("m=−2","Divide.","Gradient is output change per input unit.","gradient"),("Check: 4+6(−2)=−8","Rebuild the second y-value.","Verification uses the calculated rate.","verify")],kind="numeric",tags=["gradient-order"]),
 make(3,2,"Find the line parallel to y=4x−7 through (0,3).","y=4x+3",[("m=4","Use equal gradients for parallel lines.","Parallel non-vertical lines have the same rate.","gradient"),("y=4x+c","Keep the known gradient.","Only the intercept remains unknown.","form"),("3=4(0)+c","Substitute the supplied point.","A point on the line must satisfy its equation.","substitute"),("y=4x+3","Solve and state the equation.","The point gives c=3.","answer")],tags=["parallel-gradient"]),
 make(3,3,"Find the x-intercept of y=2.5x−10.","4",[("0=2.5x−10","Set y=0.","An x-intercept lies on the x-axis.","condition"),("10=2.5x","Add 10 to both sides.","Equality must remain balanced.","balance"),("x=4","Divide both sides by 2.5.","This isolates the input.","solve"),("2.5(4)−10=0","Verify.","The resulting point lies on the x-axis.","verify")],kind="numeric",tags=["intercept-procedure"]),
 make(3,4,"In a value-versus-time model, interpret m=−120.","value decreases by 120 per time unit",[("m=Δvalue/Δtime","Name the rate.","Gradient compares output and input changes.","meaning"),("m=−120","Inspect sign and magnitude.","Negative means output decreases as time increases.","sign"),("Δvalue=−120 for Δtime=1","Use one input unit.","This translates the ratio into context.","unit-rate"),("Value decreases by 120 per time unit","State units and direction.","A contextual answer needs both.","answer")],tags=["gradient-interpretation"]),
]}

PRACTICE_BANKS = BANKS
PRACTICE_BY_ID = {question.id: question for bank in BANKS.values() for question in bank}
