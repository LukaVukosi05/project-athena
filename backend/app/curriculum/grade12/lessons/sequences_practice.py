"""Lesson 1 practice authored from the approved Sequences and Series pack."""

from fractions import Fraction

from app.practice.schemas import AnswerNormalisation, PracticeQuestion, WorkedSolutionStep

LESSON_ID = "g12-sequences-series-01"


def step(expression: str, explanation: str, why: str, *focus: str) -> WorkedSolutionStep:
    return WorkedSolutionStep(expression=expression, explanation=explanation, why=why, focus=list(focus))


def arithmetic_solution(values: list[str], differences: list[str], conclusion: str, verification: str):
    return [
        step(f"Sequence: {', '.join(values)}, …", "Write the terms in order.", "Consecutive terms must be compared in their given order.", "sequence"),
        step("; ".join(differences), "Subtract each term from the term immediately after it.", "First differences measure the additive change between consecutive terms.", "consecutive-differences"),
        step("First differences: " + ", ".join(item.split("=")[-1] for item in differences), "Align the calculated differences.", "Equal first differences are the defining evidence for an arithmetic sequence.", "difference-row"),
        step(conclusion, "Classify the sequence and state its common difference.", "The same amount is added at every step.", "classification"),
        step(verification, "Rebuild the displayed terms using the common difference.", "Verification confirms that the classification works for every shown transition.", "verification"),
    ]


def geometric_solution(values: list[str], ratios: list[str], conclusion: str, verification: str):
    return [
        step(f"Sequence: {', '.join(values)}, …", "Write the terms in order.", "A ratio must compare consecutive non-zero terms.", "sequence"),
        step("; ".join(ratios), "Divide each term by the term immediately before it.", "Division tests for a constant multiplicative change; subtraction does not prove a sequence is geometric.", "consecutive-ratios"),
        step("Ratio row: " + ", ".join(item.split("=")[-1] for item in ratios), "Align the calculated ratios.", "Equal non-zero ratios are the defining evidence for a geometric sequence.", "ratio-row"),
        step(conclusion, "Classify the sequence and state its common ratio.", "Every new term is produced by the same multiplication.", "classification"),
        step(verification, "Rebuild the displayed terms using the common ratio.", "Verification checks every shown transition.", "verification"),
    ]


def quadratic_solution(values: list[str], first: list[str], second: list[str], conclusion: str, prediction: str, verification: str):
    return [
        step(f"Sequence: {', '.join(values)}, …", "Write the original term row.", "Quadratic evidence comes from comparing two levels of change.", "sequence"),
        step("First differences: " + ", ".join(first), "Calculate and align consecutive first differences.", "The first differences are not equal, so the sequence is not arithmetic.", "first-differences"),
        step("Second differences: " + ", ".join(second), "Subtract consecutive first differences.", "Constant second differences are the defining evidence for a quadratic number pattern.", "second-differences"),
        step(conclusion, "Classify the pattern from the constant second difference.", "Classification follows calculated evidence, not the appearance of increasing terms.", "classification"),
        step(prediction, "Continue the difference pattern before finding the next term.", "The next first difference changes by the same constant second difference.", "prediction"),
        step(verification, "Check the extended difference table.", "A valid prediction must preserve the constant second difference.", "verification"),
    ]


def q(number, difficulty, cognitive, marks, kind, prompt, accepted, hints, solution, tags, verification, feedback, options=None, fraction=False):
    return PracticeQuestion(
        id=f"g12-seq-l01-p{number:02}", lesson_id=LESSON_ID, question_number=number,
        difficulty=difficulty, cognitive_level=cognitive, marks=marks, type=kind,
        prompt=prompt, options=options or [], accepted_answers=accepted,
        answer_normalisation=AnswerNormalisation(accept_fraction_decimal_equivalence=fraction),
        hints=hints, worked_solution=solution, misconception_tags=tags,
        verification=verification, correct_feedback=feedback,
    )


LESSON_ONE_PRACTICE = [
    q(1,"foundation","routine",2,"classification","Classify 18, 13, 8, 3, … using calculated evidence.",["arithmetic"],
      ["Compare each term with the term immediately before it.","Calculate 13−18, 8−13 and 3−8.","The three first differences are equal."],
      arithmetic_solution(["18","13","8","3"],["13−18=−5","8−13=−5","3−8=−5"],"Arithmetic; d=−5","18−5=13; 13−5=8; 8−5=3"),["classify-by-appearance","sign-error"],{"method":"constant first difference","result":"d=−5"},"Correct. The first differences are all −5, so the sequence is arithmetic.",options=["Arithmetic","Geometric","Quadratic"]),
    q(2,"easy","routine",2,"missing_term","Find the missing term and classify: 24, 17, __, 3, …",["10"],
      ["Look for the change from 24 to 17.","A constant change of −7 would continue the pattern.","Calculate 17−7."],
      arithmetic_solution(["24","17","10","3"],["17−24=−7","10−17=−7","3−10=−7"],"Arithmetic; d=−7","24−7=17; 17−7=10; 10−7=3"),["missing-term","sign-error"],{"classification":"arithmetic","result":"10"},"Correct. The missing term is 10 and the constant difference is −7."),
    q(3,"standard","complex",3,"numeric","The arithmetic sequence −11, −4, 3, 10, … continues. Enter the next term.",["17"],
      ["Calculate the change between the first two terms.","Check whether −4−(−11), 3−(−4), and 10−3 agree.","Add the common difference 7 to 10."],
      arithmetic_solution(["−11","−4","3","10"],["−4−(−11)=7","3−(−4)=7","10−3=7"],"Arithmetic; d=7","10+7=17"),["negative-number-subtraction"],{"method":"continue d=7","result":"17"},"Correct. Every first difference is 7, so the next term is 17."),
    q(4,"foundation","routine",2,"classification","Classify 81, 27, 9, 3, … using calculated evidence.",["geometric"],
      ["Test consecutive ratios, not differences.","Calculate 27÷81, 9÷27 and 3÷9.","Each ratio is one third."],
      geometric_solution(["81","27","9","3"],["27÷81=1/3","9÷27=1/3","3÷9=1/3"],"Geometric; r=1/3","81×1/3=27; 27×1/3=9; 9×1/3=3"),["use-differences-for-geometric"],{"method":"constant non-zero ratio","result":"r=1/3"},"Correct. The consecutive ratios are all 1/3, so the sequence is geometric.",options=["Arithmetic","Geometric","Quadratic"]),
    q(5,"standard","complex",3,"missing_term","Find the missing term: 64, −32, __, −8, …",["16"],
      ["The signs alternate, so test a negative ratio.","Calculate −32÷64.","Multiply −32 by −1/2."],
      geometric_solution(["64","−32","16","−8"],["−32÷64=−1/2","16÷(−32)=−1/2","−8÷16=−1/2"],"Geometric; r=−1/2","64×(−1/2)=−32; −32×(−1/2)=16; 16×(−1/2)=−8"),["alternating-signs","ratio-sign"],{"classification":"geometric","result":"16"},"Correct. Multiplying by −1/2 gives the missing term 16.",fraction=True),
    q(6,"intermediate","complex",3,"numeric","For 5, 10, 20, 40, …, predict the next term after proving the pattern type.",["80"],
      ["Compare consecutive terms using division.","The ratios 10÷5, 20÷10 and 40÷20 are equal.","Multiply 40 by the common ratio."],
      geometric_solution(["5","10","20","40"],["10÷5=2","20÷10=2","40÷20=2"],"Geometric; r=2","40×2=80"),["guess-next-term"],{"method":"continue r=2","result":"80"},"Correct. The ratio is constantly 2, so the next term is 80."),
    q(7,"foundation","routine",3,"classification","Classify 1, 5, 11, 19, … using a difference table.",["quadratic"],
      ["Calculate the first differences.","Compare 6−4 and 8−6.","The second differences are equal."],
      quadratic_solution(["1","5","11","19"],["4","6","8"],["2","2"],"Quadratic; constant second difference 2","Next first difference: 10; next term: 29","10−8=2 and 29−19=10"),["stop-at-first-differences"],{"method":"constant second difference","next_term":"29"},"Correct. Its first differences change, but its second differences are constantly 2.",options=["Arithmetic","Geometric","Quadratic"]),
    q(8,"standard","complex",3,"missing_term","Find the next term of 3, 8, 15, 24, … after classifying the pattern.",["35"],
      ["Find the first differences 5, 7 and 9.","The second differences are both 2.","The next first difference is 11."],
      quadratic_solution(["3","8","15","24"],["5","7","9"],["2","2"],"Quadratic; constant second difference 2","Next first difference: 11; next term: 35","11−9=2 and 35−24=11"),["assume-arithmetic-when-increasing"],{"method":"extend difference table","result":"35"},"Correct. Constant second differences give the next first difference 11 and next term 35."),
    q(9,"intermediate","complex",4,"numeric","The pattern 30, 22, 16, 12, … has negative first differences. Predict its next term.",["10"],
      ["Calculate each first difference, including its sign.","The first differences are −8, −6 and −4.","Their second difference is +2, so the next first difference is −2."],
      quadratic_solution(["30","22","16","12"],["−8","−6","−4"],["2","2"],"Quadratic; constant second difference 2","Next first difference: −2; next term: 10","−2−(−4)=2 and 10−12=−2"),["negative-first-differences","sign-error"],{"method":"extend second differences","result":"10"},"Correct. The next first difference is −2, giving the next term 10."),
    q(10,"exam","problem_solving",4,"multiple_choice","Which evidence correctly classifies 4, 10, 18, 28, …?",["constant second differences"],
      ["Test first differences before choosing a formula.","The first differences are 6, 8 and 10.","Now compare the changes between 6, 8 and 10."],
      quadratic_solution(["4","10","18","28"],["6","8","10"],["2","2"],"Quadratic; constant second difference 2","Next first difference: 12; next term: 40","12−10=2 and 40−28=12"),["classify-by-appearance"],{"method":"constant second differences","result":"quadratic"},"Correct. The first differences are not equal, but their differences are constantly 2.",options=["The terms increase","The first differences are constant","The ratios are constant","The second differences are constant"]),
    q(11,"exam","problem_solving",4,"multiple_choice","Which test should be used first to classify 64, 32, 16, 8, …?",["calculate consecutive ratios"],
      ["Ask whether the change is additive or multiplicative.","The terms halve each time.","Test 32÷64, 16÷32 and 8÷16."],
      geometric_solution(["64","32","16","8"],["32÷64=1/2","16÷32=1/2","8÷16=1/2"],"Geometric; r=1/2","64×1/2=32; 32×1/2=16; 16×1/2=8"),["choose-test","decreasing-means-arithmetic"],{"method":"consecutive ratios","result":"geometric"},"Correct. Consecutive ratios reveal the constant multiplicative change.",options=["Calculate consecutive ratios","Check whether all terms are positive","Calculate only the first difference","Assume decreasing means arithmetic"]),
    q(12,"advanced","problem_solving",4,"error_analysis","A learner says: “2, 6, 12, 20, … is arithmetic because it increases by even numbers.” Identify the first error.",["increasing does not prove arithmetic"],
      ["Classification needs a defining test, not a visual description.","Calculate the first differences 4, 6 and 8.","Unequal first differences rule out arithmetic; equal second differences prove quadratic."],
      quadratic_solution(["2","6","12","20"],["4","6","8"],["2","2"],"Quadratic, not arithmetic","Next first difference: 10; next term: 30","10−8=2 and 30−20=10"),["classify-by-appearance","increasing-means-arithmetic"],{"error":"appearance used instead of calculated evidence","repair":"constant second differences prove quadratic"},"Correct. Increasing values do not prove arithmetic; the constant second differences prove a quadratic pattern.",options=["Increasing does not prove arithmetic","Even terms always form a geometric sequence","The sequence should start at zero","Four terms are never enough to test a pattern"]),
]

assert len(LESSON_ONE_PRACTICE) == 12
assert [item.question_number for item in LESSON_ONE_PRACTICE] == list(range(1, 13))
assert len({item.id for item in LESSON_ONE_PRACTICE}) == 12

PRACTICE_BY_ID = {item.id: item for item in LESSON_ONE_PRACTICE}
