"""Private, teacher-facing timeline plans for Grade 8 Algebraic Equations Lesson 1.

The Gold Pack ``teaching_sequence`` values are renderer directions. They are
kept as ``internal_instruction`` and excluded from learner payloads. Captions
and narration below are deliberately written as mathematical teaching.
"""

from __future__ import annotations


def _step(instruction: str, action: str, target: str, before: str, working: str, after: str, narration: str) -> dict[str, str]:
    return {
        "internal_instruction": instruction,
        "action": action,
        "target": target,
        "before": before,
        "working": working,
        "after": after,
        "narration": narration,
    }


TEACHING_TIMELINES: dict[str, list[dict[str, str]]] = {
    "g8-ae-l01-w01": [
        _step("Reveal the complete equation; highlight the left-hand side.", "evaluate_expression", "left-expression", "7 + 5 = 9 + 3", "7 + 5 → 12", "12 = 9 + 3", "The equals sign asks whether both expressions have the same value. Start on the left: seven plus five gives twelve."),
        _step("Highlight and evaluate the right-hand side.", "evaluate_expression", "right-expression", "12 = 9 + 3", "9 + 3 → 12", "12 = 12", "Now evaluate the right-hand side. Nine plus three also gives twelve, while the left value remains twelve."),
        _step("Place 12 on both pans and level the beam.", "balance_scale", "balance-beam", "12 = 12", "compare 12 with 12", "12 = 12 — balanced", "Both sides have the same value, so the equation is balanced."),
        _step("Reveal True and state that equality compares values.", "compare_values", "balance-beam", "12 = 12 — balanced", "equal values make a true equation", "7 + 5 = 9 + 3 is true", "The statement is true because both expressions evaluate to twelve."),
        _step("Return to the original equation for verification.", "verify_solution", "verification", "7 + 5 = 9 + 3 is true", "7 + 5 = 12 and 9 + 3 = 12", "Checked: 12 = 12; therefore the statement is true", "Checking the original statement confirms that twelve equals twelve, so the statement is true."),
    ],
    "g8-ae-l01-w02": [
        _step("Evaluate the left side as 13.", "evaluate_expression", "left-expression", "9 + 4 = □ + 5", "9 + 4 → 13", "13 = □ + 5", "First find the known value. Nine plus four is thirteen, so the expression on the right must also total thirteen."),
        _step("Subtract 5 from the required right-side total.", "remove_from_both_sides", "right-expression", "13 = □ + 5", "13 − 5 = □", "8 = □", "Five is already added to the missing number. Subtracting five from thirteen leaves eight for the box."),
        _step("Write the resolved box as the answer.", "transform_expression", "variable-slot", "8 = □", "reverse the equality", "□ = 8", "Equality works in either direction, so write the resolved missing number clearly as box equals eight."),
        _step("Place 8 in the box and evaluate.", "substitute_value", "variable-slot", "□ = 8", "9 + 4 = 8 + 5", "13 = 8 + 5", "Substitute eight into the original equation. The right-hand side becomes eight plus five."),
        _step("Show the balanced scale.", "compare_values", "balance-beam", "13 = 8 + 5", "8 + 5 → 13", "13 = 13 — balanced", "Eight plus five is thirteen, matching the left-hand side exactly."),
        _step("Verify using the original equation.", "verify_solution", "verification", "13 = 13 — balanced", "9 + 4 = 8 + 5", "Checked: 13 = 13; therefore □ = 8", "Substitution in the original equation gives thirteen on both sides, so the missing number is eight."),
    ],
    "g8-ae-l01-w03": [
        _step("Highlight positive 3 beside the box.", "highlight_expression", "left-expression", "□ + 3 = 10", "undo +3 with −3", "□ + 3 − 3 = 10 − 3", "The box has three added to it. To isolate the box while preserving equality, subtract three from both sides."),
        _step("Cancel +3 and -3 on the left.", "transform_expression", "left-expression", "□ + 3 − 3 = 10 − 3", "+3 − 3 → 0", "□ = 10 − 3", "On the left, positive three and negative three cancel, leaving only the unknown."),
        _step("Calculate 10 - 3.", "evaluate_expression", "right-expression", "□ = 10 − 3", "10 − 3 → 7", "□ = 7", "The right-hand side is ten minus three, which equals seven."),
        _step("Return to the original equation.", "substitute_value", "variable-slot", "□ = 7", "7 + 3", "7 + 3 = 10", "Check seven in the original equation. Seven plus three gives ten."),
        _step("Complete verification.", "verify_solution", "verification", "7 + 3 = 10", "10 = 10", "Checked: 10 = 10; therefore □ = 7", "The original equation gives ten on both sides, so seven is the value represented by the box."),
    ],
    "g8-ae-l01-w04": [
        _step("Display 12 = 12 and prepare five units on each pan.", "add_to_both_sides", "operation", "12 = 12", "+5 on the left and +5 on the right", "12 + 5 = 12 + 5", "The equation begins balanced. Adding the same five to both sides preserves equality."),
        _step("Add the five units simultaneously.", "evaluate_expression", "left-expression", "12 + 5 = 12 + 5", "12 + 5 → 17", "17 = 12 + 5", "The new left-hand value is seventeen; the right-hand expression is unchanged for now."),
        _step("Evaluate the right side.", "evaluate_expression", "right-expression", "17 = 12 + 5", "12 + 5 → 17", "17 = 17", "The right-hand side also becomes seventeen."),
        _step("Keep the beam level.", "balance_scale", "balance-beam", "17 = 17", "compare 17 with 17", "17 = 17 — balanced", "Because equal amounts were added, the beam remains level and the equation remains true."),
        _step("Verify both new sides.", "verify_solution", "verification", "17 = 17 — balanced", "12 + 5 = 12 + 5", "Checked: 17 = 17; the equation remains true", "Evaluating both sides confirms seventeen equals seventeen, so the equation remains true."),
    ],
    "g8-ae-l01-w05": [
        _step("Animate three units leaving only the left pan.", "diagnose_error", "left-expression", "8 = 8", "left side only: 8 − 3", "5 ≠ 8", "Subtracting three from only the left side changes one value but not the other, so equality is broken."),
        _step("Mark the first error and reset.", "compare_values", "balance-beam", "5 ≠ 8", "unequal values tip the balance", "Reset: 8 = 8", "Five is not equal to eight. The first error is changing only one side, so return to the original equation."),
        _step("Remove three units from both pans.", "remove_from_both_sides", "operation", "Reset: 8 = 8", "−3 on both complete sides", "8 − 3 = 8 − 3", "The repair is to subtract three from both sides, keeping the changes equal."),
        _step("Evaluate both repaired sides.", "evaluate_expression", "balance-beam", "8 − 3 = 8 − 3", "5 on each side", "5 = 5 — balanced", "Both sides now simplify to five, so the repaired equation is true."),
        _step("Verify the repair rule.", "verify_solution", "verification", "5 = 5 — balanced", "8 − 3 = 8 − 3", "Checked: 5 = 5; subtracting three from both sides preserves equality", "The repaired equation simplifies to five equals five, confirming that subtracting the same number from both sides preserves equality."),
    ],
    "g8-ae-l01-w06": [
        _step("Replace x with 4 using substitution brackets.", "substitute_value", "variable-slot", "2x + 3 = 11", "x ← 4", "2(4) + 3 = 11", "To test the claim, substitute four for x in the original equation. The right-hand side stays eleven."),
        _step("Evaluate multiplication before addition.", "evaluate_expression", "left-expression", "2(4) + 3 = 11", "2 × 4 → 8", "8 + 3 = 11", "Multiplication comes first: two times four is eight."),
        _step("Evaluate the left total.", "evaluate_expression", "left-expression", "8 + 3 = 11", "8 + 3 → 11", "11 = 11", "Adding three gives eleven on the left, matching the unchanged right-hand side."),
        _step("Compare both values.", "balance_scale", "balance-beam", "11 = 11", "compare 11 with 11", "11 = 11 — balanced", "The two values are equal, so the candidate keeps the equation balanced."),
        _step("Verify the candidate.", "verify_solution", "verification", "11 = 11 — balanced", "2(4) + 3 = 11", "Checked: 11 = 11; yes, x = 4 is a solution", "The original equation gives eleven on both sides when x is four, so the answer is yes."),
    ],
    "g8-ae-l01-w07": [
        _step("Show subtraction of 5 beneath both sides.", "remove_from_both_sides", "operation", "x + 5 = 13", "−5 on both sides", "x + 5 − 5 = 13 − 5", "Five is added to x. Subtract five from both sides so equality is preserved."),
        _step("Cancel +5 with -5.", "transform_expression", "left-expression", "x + 5 − 5 = 13 − 5", "+5 − 5 → 0", "x = 13 − 5", "The positive five and negative five cancel, leaving x on its own."),
        _step("Evaluate the right side.", "evaluate_expression", "right-expression", "x = 13 − 5", "13 − 5 → 8", "x = 8", "Thirteen minus five is eight, so x equals eight."),
        _step("Substitute 8 into the original equation.", "substitute_value", "variable-slot", "x = 8", "8 + 5", "8 + 5 = 13", "Substitute eight into the original left-hand side to check the solution."),
        _step("Verify equality.", "verify_solution", "verification", "8 + 5 = 13", "13 = 13", "Checked: 13 = 13; therefore x = 8", "Eight plus five is thirteen, so both original sides equal thirteen and x equals eight."),
    ],
    "g8-ae-l01-w08": [
        _step("Partition both pans into four equal groups.", "divide_both_sides", "operation", "4x = 28", "divide both sides by 4", "4x ÷ 4 = 28 ÷ 4", "Four equal x-groups total twenty-eight. Divide both complete sides by four to compare one group."),
        _step("Simplify the left quotient.", "transform_expression", "left-expression", "4x ÷ 4 = 28 ÷ 4", "4x ÷ 4 → x", "x = 28 ÷ 4", "Four x divided into four equal groups leaves one x."),
        _step("Evaluate the right quotient.", "evaluate_expression", "right-expression", "x = 28 ÷ 4", "28 ÷ 4 → 7", "x = 7", "Twenty-eight divided by four is seven, so each group has value seven."),
        _step("Substitute 7 into 4x = 28.", "substitute_value", "variable-slot", "x = 7", "4(7)", "4(7) = 28", "Check seven in the original equation by multiplying it by four."),
        _step("Verify the product.", "verify_solution", "verification", "4(7) = 28", "4 × 7 → 28", "Checked: 28 = 28; therefore x = 7", "Four times seven is twenty-eight on the left, matching the right, which verifies x equals seven."),
    ],
    "g8-ae-l01-w09": [
        _step("Remove three units from both pans.", "remove_from_both_sides", "operation", "2x + 3 = 13", "−3 on both sides", "2x + 3 − 3 = 13 − 3", "Undo the added three first by subtracting three from both sides."),
        _step("Simplify after subtraction.", "transform_expression", "left-expression", "2x + 3 − 3 = 13 − 3", "+3 − 3 → 0; 13 − 3 → 10", "2x = 10", "The threes cancel on the left, and thirteen minus three is ten."),
        _step("Partition both sides into two groups.", "divide_both_sides", "operation", "2x = 10", "divide both sides by 2", "2x ÷ 2 = 10 ÷ 2", "Two equal x-groups total ten, so divide both sides by two."),
        _step("Evaluate one group.", "evaluate_expression", "right-expression", "2x ÷ 2 = 10 ÷ 2", "10 ÷ 2 → 5", "x = 5", "One x-group has value five."),
        _step("Verify in the original equation.", "verify_solution", "verification", "x = 5", "2(5) + 3 = 10 + 3", "Checked: 13 = 13; therefore x = 5", "Substituting five gives thirteen on the left, matching the original right-hand side, so x equals five."),
    ],
    "g8-ae-l01-w10": [
        _step("Compare the original and learner states.", "diagnose_error", "left-expression", "3x + 6 = 21", "learner wrote x + 6 = 7", "3x became x, but +6 stayed +6", "The learner divided the term three x and the right side by three, but did not divide the added six. That does not transform the complete left side."),
        _step("Show the equivalence test failing.", "compare_values", "balance-beam", "3x became x, but +6 stayed +6", "whole side was not changed consistently", "x + 6 = 7 is not equivalent", "Because only part of the left expression changed, the new equation is not equivalent to the original."),
        _step("Reset and subtract 6 from both sides.", "remove_from_both_sides", "operation", "x + 6 = 7 is not equivalent", "restart: 3x + 6 − 6 = 21 − 6", "3x = 15", "Return to the original equation and subtract six from both sides. This legally isolates the three x term."),
        _step("Divide both sides by 3.", "divide_both_sides", "operation", "3x = 15", "3x ÷ 3 = 15 ÷ 3", "x = 5", "Now divide both complete sides by three. Fifteen divided by three is five."),
        _step("Verify x = 5.", "verify_solution", "verification", "x = 5", "3(5) + 6 = 15 + 6", "Checked: 21 = 21; therefore x = 5", "Substituting five into the original equation gives twenty-one on both sides, confirming the corrected solution."),
    ],
    "g8-ae-l01-w11": [
        _step("Remove one x tile from both pans.", "remove_from_both_sides", "operation", "3x + 2 = x + 12", "−x on both sides", "3x − x + 2 = x − x + 12", "Subtract one x from both sides to collect the variable terms without disturbing equality."),
        _step("Simplify the variable terms.", "transform_expression", "left-expression", "3x − x + 2 = x − x + 12", "3x − x → 2x; x − x → 0", "2x + 2 = 12", "Three x minus one x leaves two x, while the x terms on the right cancel."),
        _step("Remove two from both sides.", "remove_from_both_sides", "operation", "2x + 2 = 12", "−2 on both sides", "2x = 10", "Subtract two from both sides to isolate the two equal x-groups."),
        _step("Divide both sides by two.", "divide_both_sides", "operation", "2x = 10", "2x ÷ 2 = 10 ÷ 2", "x = 5", "Dividing both sides by two shows that one x has value five."),
        _step("Evaluate both original sides.", "verify_solution", "verification", "x = 5", "3(5) + 2 = 5 + 12", "Checked: 17 = 17; therefore x = 5", "The original left side and right side both evaluate to seventeen, verifying x equals five."),
    ],
    "g8-ae-l01-w12": [
        _step("Add four units to both pans.", "add_to_both_sides", "operation", "5x − 4 = 21", "+4 on both sides", "5x − 4 + 4 = 21 + 4", "Undo subtracting four by adding four to both sides, which preserves equality."),
        _step("Simplify the new equation.", "transform_expression", "left-expression", "5x − 4 + 4 = 21 + 4", "−4 + 4 → 0; 21 + 4 → 25", "5x = 25", "Negative four and positive four cancel, while the right side becomes twenty-five."),
        _step("Divide into five equal groups.", "divide_both_sides", "operation", "5x = 25", "5x ÷ 5 = 25 ÷ 5", "x = 5", "Divide both sides by five. Each x-group therefore has value five."),
        _step("Substitute into the original equation.", "substitute_value", "variable-slot", "x = 5", "5(5) − 4 = 25 − 4", "5(5) − 4 = 21", "Checking five in the original expression gives twenty-five minus four."),
        _step("Verify the solution.", "verify_solution", "verification", "5(5) − 4 = 21", "25 − 4 → 21", "Checked: 21 = 21; therefore x = 5", "The check produces twenty-one on both sides, so x equals five."),
    ],
    "g8-ae-l01-w13": [
        _step("Define x and replace notebook images with x tiles.", "form_equation", "context", "3 notebooks + R6 pen = R45", "one notebook costs R x", "3x + 6 = 45", "Let x represent the price of one notebook. Three identical notebooks and the six-rand pen give the equation three x plus six equals forty-five."),
        _step("Subtract 6 from both sides.", "remove_from_both_sides", "operation", "3x + 6 = 45", "−6 on both sides", "3x = 39", "Remove the pen cost by subtracting six rand from both sides. The three notebooks cost thirty-nine rand."),
        _step("Divide by 3.", "divide_both_sides", "operation", "3x = 39", "3x ÷ 3 = 39 ÷ 3", "x = 13", "Share thirty-nine rand equally among the three notebooks. One notebook costs thirteen rand."),
        _step("Attach the correct unit.", "transform_expression", "variable-slot", "x = 13", "x is a price in rand", "one notebook = R13", "Because x represents a price, the answer must include the rand unit: one notebook costs thirteen rand."),
        _step("Rebuild the shopping total.", "verify_solution", "verification", "one notebook = R13", "3(R13) + R6 = R39 + R6", "Checked: R45 = R45; therefore one notebook costs R13", "Three thirteen-rand notebooks plus the six-rand pen total forty-five rand, so the thirteen-rand price is verified."),
    ],
    "g8-ae-l01-w14": [
        _step("Substitute 6 into the original left side.", "substitute_value", "variable-slot", "4x − 7 = 19; claim x = 6", "4(6) − 7", "24 − 7 = 19", "Test the learner's claim in the original equation. Four times six is twenty-four, before subtracting seven."),
        _step("Compare 17 with 19.", "evaluate_expression", "left-expression", "24 − 7 = 19", "24 − 7 → 17", "17 ≠ 19", "Twenty-four minus seven is seventeen, not nineteen, so six is not a solution."),
        _step("Add 7 to both sides of the original.", "add_to_both_sides", "operation", "17 ≠ 19", "restart: 4x − 7 + 7 = 19 + 7", "4x = 26", "Return to the original equation and add seven to both sides. This leaves four x equal to twenty-six."),
        _step("Divide both sides by 4.", "divide_both_sides", "operation", "4x = 26", "4x ÷ 4 = 26 ÷ 4", "x = 13/2 = 6.5", "Dividing both sides by four gives thirteen halves, which is the same as six comma five."),
        _step("Verify the corrected value.", "verify_solution", "verification", "x = 13/2 = 6.5", "4(6.5) − 7 = 26 − 7", "Checked: 19 = 19; the claim x = 6 is false and x = 6.5", "Substituting six comma five gives nineteen on the left, matching the original right-hand side; this confirms the corrected value and rejects six."),
    ],
    "g8-ae-l01-w15": [
        _step("Group x + 4 as one object and show two copies.", "group_equal_terms", "left-expression", "2(x + 4) = 18", "(x + 4) + (x + 4) = 18", "two equal groups total 18", "Treat the bracket x plus four as one group. Two identical groups together have value eighteen."),
        _step("Partition both sides into two groups.", "divide_both_sides", "operation", "two equal groups total 18", "2(x + 4) ÷ 2 = 18 ÷ 2", "x + 4 = 9", "Divide both complete sides by two. One bracket group must equal nine, so the equations are equivalent."),
        _step("Subtract 4 from the simpler equation.", "remove_from_both_sides", "operation", "x + 4 = 9", "−4 on both sides", "x + 4 − 4 = 9 − 4", "Subtract four from both sides of the simpler equivalent equation."),
        _step("Simplify to the solution.", "evaluate_expression", "right-expression", "x + 4 − 4 = 9 − 4", "+4 − 4 → 0; 9 − 4 → 5", "x = 5", "The fours cancel on the left, and nine minus four is five."),
        _step("Verify in the original bracket equation.", "verify_solution", "verification", "x = 5", "2(5 + 4) = 2(9)", "Checked: 18 = 18; therefore x = 5", "Substituting five into the original equation gives two times nine, which equals eighteen, so x equals five."),
    ],
}


COMMAND_WORDS = frozenset({"reveal", "highlight", "display", "show", "place", "animate", "move"})


# Private release contract used to validate the authored mathematical endings.
# These values are not rendered as a generic client-side ending: each one must
# already occur in its question-specific timeline, in the declared order.
TERMINAL_CONTRACTS: dict[str, dict[str, object]] = {
    "g8-ae-l01-w01": {"approved_answer": "True", "answer_state": "statement is true", "verification_state": "12 = 12", "required_states": ["12 = 9 + 3", "12 = 12", "statement is true"]},
    "g8-ae-l01-w02": {"approved_answer": "8", "answer_state": "□ = 8", "verification_state": "13 = 13", "required_states": ["13 = □ + 5", "8 = □", "□ = 8", "9 + 4 = 8 + 5", "13 = 13"]},
    "g8-ae-l01-w03": {"approved_answer": "7", "answer_state": "□ = 7", "verification_state": "10 = 10", "required_states": ["□ + 3 − 3 = 10 − 3", "□ = 7", "7 + 3 = 10", "10 = 10"]},
    "g8-ae-l01-w04": {"approved_answer": "The equation remains true: 17 = 17.", "answer_state": "17 = 17", "verification_state": "17 = 17", "required_states": ["12 + 5 = 12 + 5", "17 = 17"]},
    "g8-ae-l01-w05": {"approved_answer": "Only the left side was changed. The correct equivalent equation is 8 - 3 = 8 - 3, so 5 = 5.", "answer_state": "5 = 5", "verification_state": "5 = 5", "required_states": ["5 ≠ 8", "8 − 3 = 8 − 3", "5 = 5"]},
    "g8-ae-l01-w06": {"approved_answer": "Yes", "answer_state": "x = 4 is a solution", "verification_state": "11 = 11", "required_states": ["2(4) + 3 = 11", "11 = 11", "x = 4 is a solution"]},
    "g8-ae-l01-w07": {"approved_answer": "x = 8", "answer_state": "x = 8", "verification_state": "13 = 13", "required_states": ["x = 8", "8 + 5 = 13", "13 = 13"]},
    "g8-ae-l01-w08": {"approved_answer": "x = 7", "answer_state": "x = 7", "verification_state": "28 = 28", "required_states": ["x = 7", "4(7) = 28", "28 = 28"]},
    "g8-ae-l01-w09": {"approved_answer": "x = 5", "answer_state": "x = 5", "verification_state": "13 = 13", "required_states": ["2x = 10", "x = 5", "2(5) + 3", "13 = 13"]},
    "g8-ae-l01-w10": {"approved_answer": "The learner divided only the 3x and 21 by 3. Correctly subtract 6 first to get 3x = 15, then divide both sides by 3 to get x = 5.", "answer_state": "x = 5", "verification_state": "21 = 21", "required_states": ["not equivalent", "3x = 15", "x = 5", "21 = 21"]},
    "g8-ae-l01-w11": {"approved_answer": "x = 5", "answer_state": "x = 5", "verification_state": "17 = 17", "required_states": ["2x + 2 = 12", "2x = 10", "x = 5", "17 = 17"]},
    "g8-ae-l01-w12": {"approved_answer": "x = 5", "answer_state": "x = 5", "verification_state": "21 = 21", "required_states": ["5x = 25", "x = 5", "5(5) − 4 = 21", "21 = 21"]},
    "g8-ae-l01-w13": {"approved_answer": "R13", "answer_state": "R13", "verification_state": "R45 = R45", "required_states": ["3x + 6 = 45", "x = 13", "R13", "R45 = R45"]},
    "g8-ae-l01-w14": {"approved_answer": "The claim is false; x = 6 gives 17, not 19. The correct solution is x = 6.5 or 13/2.", "answer_state": "x = 13/2 = 6.5", "verification_state": "19 = 19", "required_states": ["17 ≠ 19", "4x = 26", "x = 13/2 = 6.5", "19 = 19"]},
    "g8-ae-l01-w15": {"approved_answer": "Dividing both sides of 2(x + 4) = 18 by 2 gives x + 4 = 9, so the equations are equivalent. The solution is x = 5.", "answer_state": "x = 5", "verification_state": "18 = 18", "required_states": ["x + 4 = 9", "x = 5", "18 = 18"]},
}
