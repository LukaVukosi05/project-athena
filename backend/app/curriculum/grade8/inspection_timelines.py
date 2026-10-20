"""Question-specific, inspect-then-check mathematical stages for Lesson 2."""

# Each stage is (before, visible operation, after, learner-facing explanation).
# The complete equation remains in the question header; the stage is cumulative.
PLANS = {
 1: [
  ("x + 6 = 10", "What plus 6 makes 10?", "4 + 6 = 10", "Six needs four more to make ten, so four is our candidate."),
  ("4 + 6 = 10", "Replace x with 4", "x = 4; 4 + 6 = 10", "Put four in the unknown position. The original left side becomes ten."),
  ("x = 4; 4 + 6 = 10", "Compare both original sides", "Checked: 10 = 10; x = 4", "Ten equals ten in the original equation, so x is four."),
 ],
 2: [
  ("y − 7 = 5", "From 5, count forward seven", "5 + 7 = 12", "To find where the backwards jump began, count seven forward from five."),
  ("5 + 7 = 12", "Start at 12 and jump back seven", "12 − 7 = 5; y = 12", "The candidate is twelve. Jump seven backwards and we land at five."),
  ("12 − 7 = 5; y = 12", "Compare with the original landing", "Checked: 5 = 5; y = 12", "The original equation gives five on each side, confirming twelve."),
 ],
 3: [
  ("7a = 42", "Recall seven groups of six", "7 × 6 = 42", "Seven groups of six counters make forty-two, so six is a candidate."),
  ("7 × 6 = 42", "Place six in the a tile", "a = 6; 7(6) = 42", "Replace a with six in the original product."),
  ("a = 6; 7(6) = 42", "Count and compare", "Checked: 42 = 42; a = 6", "The seven groups total forty-two, matching the target."),
 ],
 4: [
  ("b ÷ 5 = 7", "Make five groups of seven", "5 × 7 = 35", "Five equal groups of seven contain thirty-five items altogether."),
  ("5 × 7 = 35", "Test the total in the original", "b = 35; 35 ÷ 5 = 7", "Share thirty-five into five groups: each group gets seven."),
  ("b = 35; 35 ÷ 5 = 7", "Compare the group size", "Checked: 7 = 7; b = 35", "Seven equals seven, so the missing total is thirty-five."),
 ],
 5: [
  ("2x + 1 = 9", "Test x = 3: 2(3) + 1", "x = 3 → 7 ≠ 9", "Three produces seven, not nine; reject this candidate."),
  ("x = 3 → 7 ≠ 9", "Test x = 4: 2(4) + 1", "x = 4 → 9 = 9", "Four produces nine in the original expression."),
  ("x = 4 → 9 = 9", "Compare the matching table row", "Checked: 9 = 9; x = 4", "Only the row for four matches the original target."),
 ],
 6: [
  ("3m − 4 = 11", "Undo the final subtraction mentally: 11 + 4", "3m must be 15", "Before subtracting four, the machine must have produced fifteen."),
  ("3m must be 15", "Recall three groups of five", "m = 5; 3(5) = 15", "Three groups of five make fifteen, so try five."),
  ("m = 5; 3(5) = 15", "Run the original chain: 15 − 4", "Checked: 11 = 11; m = 5", "Fifteen minus four is eleven, matching the untouched original equation."),
 ],
 7: [
  ("2(n + 1) = 10", "Two equal groups of what make ten?", "n + 1 = 5", "Each of the two identical bracket groups must be worth five."),
  ("n + 1 = 5", "What plus one makes five?", "n = 4; n + 1 = 5", "Four plus one gives five inside each group."),
  ("n = 4; n + 1 = 5", "Count two groups of five", "Checked: 10 = 10; n = 4", "Two copies of four plus one total ten in the original equation."),
 ],
 8: [
  ("18 − p = 11", "Measure the backward gap from 18 to 11", "18 − 11 = 7", "Eleven lies seven steps below eighteen, so seven was removed."),
  ("18 − 11 = 7", "Test a jump of seven from 18", "p = 7; 18 − 7 = 11", "A seven-unit backward jump lands exactly on eleven."),
  ("p = 7; 18 − 7 = 11", "Compare with original landing", "Checked: 11 = 11; p = 7", "The original left and right sides both equal eleven."),
 ],
 9: [
  ("−3q = 18", "Test positive six", "q = 6 → −18 ≠ 18", "Negative three times positive six is negative eighteen, so reject six."),
  ("q = 6 → −18 ≠ 18", "Test negative six", "q = −6 → 18 = 18", "Negative three times negative six is positive eighteen."),
  ("q = −6 → 18 = 18", "Compare with the original target", "Checked: 18 = 18; q = −6", "The original equation is true for negative six."),
 ],
 10: [
  ("x ÷ 4 − 2 = 3", "What number minus two gives three?", "x ÷ 4 must be 5", "The value before the last subtraction must be five."),
  ("x ÷ 4 must be 5", "Four groups of five make twenty", "x = 20; 20 ÷ 4 = 5", "A total of twenty gives five in each of four groups."),
  ("x = 20; 20 ÷ 4 = 5", "Run the original chain: five minus two", "Checked: 3 = 3; x = 20", "Twenty divided by four, then minus two, produces the target three."),
 ],
 11: [
  ("3x + 2 = 13; claim x = 4", "Test the proposed four", "3(4) + 2 = 14 ≠ 13", "Four produces fourteen, not thirteen, so the claim fails."),
  ("3(4) + 2 = 14 ≠ 13", "Find the value before adding two", "3x must be 11", "To reach thirteen after adding two, the three x term must be eleven."),
  ("3x must be 11", "Find one third of eleven", "x = 11/3", "Three copies of eleven thirds make eleven exactly."),
  ("x = 11/3", "Substitute into the original equation", "Checked: 13 = 13; x = 11/3", "Three times eleven thirds plus two equals thirteen, so this corrected value works."),
 ],
 12: [
  ("2x + 3 = x + 9", "Test four on both sides", "x = 4 → 11 ≠ 13", "At four the left side is eleven and the right is thirteen."),
  ("x = 4 → 11 ≠ 13", "Test five on both sides", "x = 5 → 13 ≠ 14", "At five the outputs differ by one, so the gap is closing."),
  ("x = 5 → 13 ≠ 14", "Test six on both sides", "x = 6 → 15 = 15", "At six both output columns contain fifteen."),
  ("x = 6 → 15 = 15", "Substitute six into the untouched equation", "Checked: 15 = 15; x = 6", "Both original sides give fifteen, so six is the solution."),
 ],
 13: [
  ("Rectangle: width 5 cm; area 60 cm²", "Area = length × width", "length × 5 cm = 60 cm²", "The unknown length times five centimetres must make sixty square centimetres."),
  ("length × 5 cm = 60 cm²", "Which length makes five groups total sixty?", "length = 12 cm", "Twelve groups of five give sixty; length uses centimetres, not square centimetres."),
  ("length = 12 cm", "Check the original rectangle area", "Checked: 60 cm² = 60 cm²; length = 12 cm", "Twelve centimetres times five centimetres equals sixty square centimetres."),
 ],
 14: [
  ("Two consecutive whole numbers sum to 21", "Call the smaller n and the larger n + 1", "n + (n + 1) = 21", "Consecutive numbers differ by one, so the second card is n plus one."),
  ("n + (n + 1) = 21", "Choose numbers either side of half of 21", "10 and 11 differ by 1", "Ten and eleven sit on opposite sides of ten and a half."),
  ("10 and 11 differ by 1", "Add the two candidate cards", "10 + 11 = 21", "Their sum is twenty-one, matching the original condition."),
  ("10 + 11 = 21", "Check consecutive and total", "Checked: 21 = 21; numbers 10 and 11", "The numbers are consecutive and their sum is twenty-one."),
 ],
 15: [
  ("0.5x + 3 = 8", "What plus three makes eight?", "0.5x must be 5", "The half of x must be five before adding three."),
  ("0.5x must be 5", "Two equal halves of five", "x = 10; half of 10 = 5", "A whole made of two five-unit halves is ten."),
  ("x = 10; half of 10 = 5", "Run the forward chain: five plus three", "Checked: 8 = 8; x = 10", "Half of ten is five, and five plus three is eight as required."),
 ],
}
