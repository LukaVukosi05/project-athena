# Grade 8 Functions and Relationships — Lesson 6: First-error diagnosis and relationship repair

Original Athena authoring aligned with Grade 8 CAPS §2.2. Teacher review required. Source: https://www.education.gov.za/Portals/0/CD/National%20Curriculum%20Statements%20and%20Vocational/CAPS%20SP%20%20MATHEMATICS%20GR%207-9.pdf

This pack specifies individual mathematical states and visual objects. The board starts with the question and givens, shows an operation before its value, keeps prior work visible and checks the original.

## Worked examples

### 01 — foundation (2 marks)

**Question:** A learner claims double x then add 3 is 2(x+3). Find the first error and repair for x=2.
**Answer:** Correct: 2x+3, so x=2 gives 7; learner gives 10
**Question scene:** {"input": 2, "candidates": [{"label": "learner", "value": 10, "a": 0, "b": 2, "c": 6}, {"label": "correct", "value": 7, "a": 0, "b": 2, "c": 3}], "chosen": "correct", "given": ["double x → add 3", "learner 2(x+3)"], "mode": "repair"}
**Board states:** Read the learner claim and original evidence → Test the claim at input 2 → Learner path → 10; repair path → 7 → Correct: 2x+3, so x=2 gives 7; learner gives 10
- Locate the first unsupported claim. Narration/caption: Check the given statement or pair before accepting the learner move. The learner grouped the addition inside doubling.
- Compare at input 2. Narration/caption: The learner path gives 10; the repaired path gives 7. The difference identifies the error.
- Repair and verify with the original. Narration/caption: Double x first; add three once afterwards. Correct: 2x+3, so x=2 gives 7; learner gives 10
**Verification:** At input 2, correct gives 7; recheck against the original words, rows or formula.
**Misconception:** The learner grouped the addition inside doubling.
**Targeted repair:** Double x first; add three once afterwards.

### 02 — easy (2 marks)

**Question:** A learner claims the table 0→4,1→7 follows y=4x+3. Diagnose with x=0.
**Answer:** Correct: 3x+4; x=0 must output 4
**Question scene:** {"input": 0, "candidates": [{"label": "learner", "value": 3, "a": 0, "b": 4, "c": 3}, {"label": "correct", "value": 4, "a": 0, "b": 3, "c": 4}], "chosen": "correct", "given": ["0→4; 1→7", "learner 4x+3"], "mode": "repair"}
**Board states:** Read the learner claim and original evidence → Test the claim at input 0 → Learner path → 3; repair path → 4 → Correct: 3x+4; x=0 must output 4
- Locate the first unsupported claim. Narration/caption: Check the given statement or pair before accepting the learner move. The zero input output was used as the coefficient.
- Compare at input 0. Narration/caption: The learner path gives 3; the repaired path gives 4. The difference identifies the error.
- Repair and verify with the original. Narration/caption: Set x to zero to locate the constant. Correct: 3x+4; x=0 must output 4
**Verification:** At input 0, correct gives 4; recheck against the original words, rows or formula.
**Misconception:** The zero input output was used as the coefficient.
**Targeted repair:** Set x to zero to locate the constant.

### 03 — easy (3 marks)

**Question:** A learner writes add 2 then triple as 3x+2. Find the first missed operation and test x=1.
**Answer:** Correct: 3(x+2); at x=1 the output is 9
**Question scene:** {"input": 1, "candidates": [{"label": "learner", "value": 5, "a": 0, "b": 3, "c": 2}, {"label": "correct", "value": 9, "a": 0, "b": 3, "c": 6}], "chosen": "correct", "given": ["x → +2 → ×3", "learner 3x+2"], "mode": "repair"}
**Board states:** Read the learner claim and original evidence → Test the claim at input 1 → Learner path → 5; repair path → 9 → Correct: 3(x+2); at x=1 the output is 9
- Locate the first unsupported claim. Narration/caption: Check the given statement or pair before accepting the learner move. The triple did not act on the entire previous result.
- Compare at input 1. Narration/caption: The learner path gives 5; the repaired path gives 9. The difference identifies the error.
- Repair and verify with the original. Narration/caption: Keep x+2 together when tripling. Correct: 3(x+2); at x=1 the output is 9
**Verification:** At input 1, correct gives 9; recheck against the original words, rows or formula.
**Misconception:** The triple did not act on the entire previous result.
**Targeted repair:** Keep x+2 together when tripling.

### 04 — standard (3 marks)

**Question:** From pairs 0→6,2→12 a learner writes y=6x+6. Identify the wrong rate and predict y at x=4.
**Answer:** Correct: y=3x+6; at x=4, y=18
**Question scene:** {"input": 4, "candidates": [{"label": "learner", "value": 30, "a": 0, "b": 6, "c": 6}, {"label": "correct", "value": 18, "a": 0, "b": 3, "c": 6}], "chosen": "correct", "given": ["0→6; 2→12", "learner y=6x+6"], "mode": "repair"}
**Board states:** Read the learner claim and original evidence → Test the claim at input 4 → Learner path → 30; repair path → 18 → Correct: y=3x+6; at x=4, y=18
- Locate the first unsupported claim. Narration/caption: Check the given statement or pair before accepting the learner move. Six output units were counted per one input unit.
- Compare at input 4. Narration/caption: The learner path gives 30; the repaired path gives 18. The difference identifies the error.
- Repair and verify with the original. Narration/caption: Divide Δy=6 by Δx=2. Correct: y=3x+6; at x=4, y=18
**Verification:** At input 4, correct gives 18; recheck against the original words, rows or formula.
**Misconception:** Six output units were counted per one input unit.
**Targeted repair:** Divide Δy=6 by Δx=2.

### 05 — standard (3 marks)

**Question:** For a R8 joining fee plus R5 per visit, a learner writes C=8v+5. Correct the swapped fee and find cost at v=3.
**Answer:** Correct: C=8+5v, C(3)=R23
**Question scene:** {"input": 3, "candidates": [{"label": "learner", "value": 29, "a": 0, "b": 8, "c": 5}, {"label": "correct", "value": 23, "a": 0, "b": 5, "c": 8}], "chosen": "correct", "given": ["R8 once", "R5 each visit", "learner 8v+5"], "mode": "repair"}
**Board states:** Read the learner claim and original evidence → Test the claim at input 3 → Learner path → 29; repair path → 23 → Correct: C=8+5v, C(3)=R23
- Locate the first unsupported claim. Narration/caption: Check the given statement or pair before accepting the learner move. The once-off charge was multiplied by visits.
- Compare at input 3. Narration/caption: The learner path gives 29; the repaired path gives 23. The difference identifies the error.
- Repair and verify with the original. Narration/caption: Place the visit fee beside v and joining fee separately. Correct: C=8+5v, C(3)=R23
**Verification:** At input 3, correct gives 23; recheck against the original words, rows or formula.
**Misconception:** The once-off charge was multiplied by visits.
**Targeted repair:** Place the visit fee beside v and joining fee separately.

### 06 — standard (4 marks)

**Question:** A learner sees −2→−3,0→1,2→5 and proposes y=2x−1. Find the first counterexample and predict x=3.
**Answer:** Correct: y=2x+1; at x=3, y=7
**Question scene:** {"input": 3, "candidates": [{"label": "learner", "value": 5, "a": 0, "b": 2, "c": -1}, {"label": "correct", "value": 7, "a": 0, "b": 2, "c": 1}], "chosen": "correct", "given": ["−2→−3; 0→1; 2→5", "learner 2x−1"], "mode": "repair"}
**Board states:** Read the learner claim and original evidence → Test the claim at input 3 → Learner path → 5; repair path → 7 → Correct: y=2x+1; at x=3, y=7
- Locate the first unsupported claim. Narration/caption: Check the given statement or pair before accepting the learner move. The zero-row intercept sign was copied incorrectly.
- Compare at input 3. Narration/caption: The learner path gives 5; the repaired path gives 7. The difference identifies the error.
- Repair and verify with the original. Narration/caption: Substitute x=0 into the candidate before forecasting. Correct: y=2x+1; at x=3, y=7
**Verification:** At input 3, correct gives 7; recheck against the original words, rows or formula.
**Misconception:** The zero-row intercept sign was copied incorrectly.
**Targeted repair:** Substitute x=0 into the candidate before forecasting.

### 07 — intermediate (4 marks)

**Question:** A learner says y=x²+1 has constant differences for x=0,1,2,3. Show the first change that disproves this.
**Answer:** Outputs 1,2,5,10; differences 1,3,5 are not constant
**Question scene:** {"input": 3, "candidates": [{"label": "linear claim", "value": 7, "a": 0, "b": 2, "c": 1}, {"label": "square rule", "value": 10, "a": 1, "b": 0, "c": 1}], "chosen": "square rule", "given": ["x=0,1,2,3", "learner says constant changes"], "mode": "repair"}
**Board states:** Read the learner claim and original evidence → Test the claim at input 3 → Learner path → 7; repair path → 10 → Outputs 1,2,5,10; differences 1,3,5 are not constant
- Locate the first unsupported claim. Narration/caption: Check the given statement or pair before accepting the learner move. Comparing two outputs without checking later differences.
- Compare at input 3. Narration/caption: The learner path gives 7; the repaired path gives 10. The difference identifies the error.
- Repair and verify with the original. Narration/caption: Compute all successive changes. Outputs 1,2,5,10; differences 1,3,5 are not constant
**Verification:** At input 3, square rule gives 10; recheck against the original words, rows or formula.
**Misconception:** Comparing two outputs without checking later differences.
**Targeted repair:** Compute all successive changes.

### 08 — intermediate (4 marks)

**Question:** A learner says 2(x+4) and 2x+4 are equivalent. Give one counterexample at x=1 and repair.
**Answer:** At x=1: 10 versus 6; correct expansion is 2x+8
**Question scene:** {"input": 1, "candidates": [{"label": "learner", "value": 6, "a": 0, "b": 2, "c": 4}, {"label": "correct", "value": 10, "a": 0, "b": 2, "c": 8}], "chosen": "correct", "given": ["2(x+4)", "learner 2x+4"], "mode": "repair"}
**Board states:** Read the learner claim and original evidence → Test the claim at input 1 → Learner path → 6; repair path → 10 → At x=1: 10 versus 6; correct expansion is 2x+8
- Locate the first unsupported claim. Narration/caption: Check the given statement or pair before accepting the learner move. The outside factor was not applied to four.
- Compare at input 1. Narration/caption: The learner path gives 6; the repaired path gives 10. The difference identifies the error.
- Repair and verify with the original. Narration/caption: Distribute two to both terms. At x=1: 10 versus 6; correct expansion is 2x+8
**Verification:** At input 1, correct gives 10; recheck against the original words, rows or formula.
**Misconception:** The outside factor was not applied to four.
**Targeted repair:** Distribute two to both terms.

### 09 — intermediate (4 marks)

**Question:** For y=−2x+3 a learner says a negative input makes the output negative. At x=−4 find the first sign error and the correct output.
**Answer:** At x=−4, two negative factors give +8, so y=11
**Question scene:** {"input": -4, "candidates": [{"label": "learner", "value": -5, "a": 0, "b": 2, "c": 3}, {"label": "correct", "value": 11, "a": 0, "b": -2, "c": 3}], "chosen": "correct", "given": ["rule y=−2x+3", "learner treats −2×−4 as −8"], "mode": "repair"}
**Board states:** Read the learner claim and original evidence → Test the claim at input -4 → Learner path → -5; repair path → 11 → At x=−4, two negative factors give +8, so y=11
- Locate the first unsupported claim. Narration/caption: Check the given statement or pair before accepting the learner move. A negative times a negative was treated as negative.
- Compare at input -4. Narration/caption: The learner path gives -5; the repaired path gives 11. The difference identifies the error.
- Repair and verify with the original. Narration/caption: Keep the two signs visible before adding three. At x=−4, two negative factors give +8, so y=11
**Verification:** At input -4, correct gives 11; recheck against the original words, rows or formula.
**Misconception:** A negative times a negative was treated as negative.
**Targeted repair:** Keep the two signs visible before adding three.

### 10 — exam (5 marks)

**Question:** Pairs 0→2,1→3,2→6 follow x²+2. A learner fits x+2 from the first two rows. Locate the counterexample.
**Answer:** At x=2, learner predicts 4 but given output is 6
**Question scene:** {"input": 2, "candidates": [{"label": "learner", "value": 4, "a": 0, "b": 1, "c": 2}, {"label": "correct", "value": 6, "a": 1, "b": 0, "c": 2}], "chosen": "correct", "given": ["0→2; 1→3; 2→6", "learner x+2"], "mode": "repair"}
**Board states:** Read the learner claim and original evidence → Test the claim at input 2 → Learner path → 4; repair path → 6 → At x=2, learner predicts 4 but given output is 6
- Locate the first unsupported claim. Narration/caption: Check the given statement or pair before accepting the learner move. Two rows cannot prove a unique rule.
- Compare at input 2. Narration/caption: The learner path gives 4; the repaired path gives 6. The difference identifies the error.
- Repair and verify with the original. Narration/caption: Check every supplied pair before accepting the rule. At x=2, learner predicts 4 but given output is 6
**Verification:** At input 2, correct gives 6; recheck against the original words, rows or formula.
**Misconception:** Two rows cannot prove a unique rule.
**Targeted repair:** Check every supplied pair before accepting the rule.

### 11 — exam (5 marks)

**Question:** A square tile array has side n; learner uses y=4n for area. At n=3 locate and repair the mix-up.
**Answer:** Area is n²=9 tiles; 4n=12 counts boundary edges
**Question scene:** {"input": 3, "candidates": [{"label": "learner", "value": 12, "a": 0, "b": 4, "c": 0}, {"label": "correct", "value": 9, "a": 1, "b": 0, "c": 0}], "chosen": "correct", "given": ["square side n", "learner area 4n"], "mode": "repair"}
**Board states:** Read the learner claim and original evidence → Test the claim at input 3 → Learner path → 12; repair path → 9 → Area is n²=9 tiles; 4n=12 counts boundary edges
- Locate the first unsupported claim. Narration/caption: Check the given statement or pair before accepting the learner move. The learner used perimeter for area.
- Compare at input 3. Narration/caption: The learner path gives 12; the repaired path gives 9. The difference identifies the error.
- Repair and verify with the original. Narration/caption: Count rows times columns for the interior. Area is n²=9 tiles; 4n=12 counts boundary edges
**Verification:** At input 3, correct gives 9; recheck against the original words, rows or formula.
**Misconception:** The learner used perimeter for area.
**Targeted repair:** Count rows times columns for the interior.

### 12 — exam (5 marks)

**Question:** A learner reverses y=3x+5 at y=20 by dividing 20 by 3, then subtracting 5. Diagnose and recover x.
**Answer:** Subtract 5 first, then divide by 3: x=5; check 3·5+5=20
**Question scene:** {"input": 20, "candidates": [{"label": "learner", "value": 1.66666667, "a": 0, "b": 0.3333333333333333, "c": -5}, {"label": "correct", "value": 5.0, "a": 0, "b": 0.3333333333333333, "c": -1.6666666666666667}], "chosen": "correct", "given": ["x → ×3 → +5", "output 20", "learner divide then subtract"], "mode": "repair"}
**Board states:** Read the learner claim and original evidence → Test the claim at input 20 → Learner path → 1.66666667; repair path → 5.0 → Subtract 5 first, then divide by 3: x=5; check 3·5+5=20
- Locate the first unsupported claim. Narration/caption: Check the given statement or pair before accepting the learner move. The inverse operations were applied in forward order.
- Compare at input 20. Narration/caption: The learner path gives 1.66666667; the repaired path gives 5.0. The difference identifies the error.
- Repair and verify with the original. Narration/caption: Undo the last +5 before the earlier ×3. Subtract 5 first, then divide by 3: x=5; check 3·5+5=20
**Verification:** At input 20, correct gives 5.0; recheck against the original words, rows or formula.
**Misconception:** The inverse operations were applied in forward order.
**Targeted repair:** Undo the last +5 before the earlier ×3.

### 13 — advanced (6 marks)

**Question:** The rows −1→0,0→1,1→4 agree with x²+2x+1. A learner claims x²+1 from nonnegative rows. Identify a counterexample.
**Answer:** At x=1, learner gives 2 instead of 4; correct rule gives 4
**Question scene:** {"input": 1, "candidates": [{"label": "learner", "value": 2, "a": 1, "b": 0, "c": 1}, {"label": "correct", "value": 4, "a": 1, "b": 2, "c": 1}], "chosen": "correct", "given": ["−1→0; 0→1; 1→4", "learner x²+1"], "mode": "repair"}
**Board states:** Read the learner claim and original evidence → Test the claim at input 1 → Learner path → 2; repair path → 4 → At x=1, learner gives 2 instead of 4; correct rule gives 4
- Locate the first unsupported claim. Narration/caption: Check the given statement or pair before accepting the learner move. One matching zero row does not determine a rule.
- Compare at input 1. Narration/caption: The learner path gives 2; the repaired path gives 4. The difference identifies the error.
- Repair and verify with the original. Narration/caption: Check the signed and positive rows. At x=1, learner gives 2 instead of 4; correct rule gives 4
**Verification:** At input 1, correct gives 4; recheck against the original words, rows or formula.
**Misconception:** One matching zero row does not determine a rule.
**Targeted repair:** Check the signed and positive rows.

### 14 — advanced (6 marks)

**Question:** A service charges R15 fixed and R4 per unit. Learner sees 0→15,3→27 but uses 15x+4. Find first wrong row and repair at x=5.
**Answer:** At x=0 learner gives 4 instead of 15; correct cost at 5 is R35
**Question scene:** {"input": 5, "candidates": [{"label": "learner", "value": 79, "a": 0, "b": 15, "c": 4}, {"label": "correct", "value": 35, "a": 0, "b": 4, "c": 15}], "chosen": "correct", "given": ["0→15; 3→27", "learner 15x+4"], "mode": "repair"}
**Board states:** Read the learner claim and original evidence → Test the claim at input 5 → Learner path → 79; repair path → 35 → At x=0 learner gives 4 instead of 15; correct cost at 5 is R35
- Locate the first unsupported claim. Narration/caption: Check the given statement or pair before accepting the learner move. The fixed charge and variable rate were reversed.
- Compare at input 5. Narration/caption: The learner path gives 79; the repaired path gives 35. The difference identifies the error.
- Repair and verify with the original. Narration/caption: Start at zero, then compute Δcost/Δunits=12/3. At x=0 learner gives 4 instead of 15; correct cost at 5 is R35
**Verification:** At input 5, correct gives 35; recheck against the original words, rows or formula.
**Misconception:** The fixed charge and variable rate were reversed.
**Targeted repair:** Start at zero, then compute Δcost/Δunits=12/3.

### 15 — advanced (7 marks)

**Question:** A learner claims 3(x−2)=3x−2 and that y=3x−2 fits 0→−6,2→0. Find first invalid step and show a fresh check at x=4.
**Answer:** Distribute −2 as −6: 3x−6; at x=4, y=6
**Question scene:** {"input": 4, "candidates": [{"label": "learner", "value": 10, "a": 0, "b": 3, "c": -2}, {"label": "correct", "value": 6, "a": 0, "b": 3, "c": -6}], "chosen": "correct", "given": ["3(x−2)", "0→−6; 2→0", "learner 3x−2"], "mode": "repair"}
**Board states:** Read the learner claim and original evidence → Test the claim at input 4 → Learner path → 10; repair path → 6 → Distribute −2 as −6: 3x−6; at x=4, y=6
- Locate the first unsupported claim. Narration/caption: Check the given statement or pair before accepting the learner move. The three was not multiplied by −2.
- Compare at input 4. Narration/caption: The learner path gives 10; the repaired path gives 6. The difference identifies the error.
- Repair and verify with the original. Narration/caption: Build three copies of (x−2) and test both given rows. Distribute −2 as −6: 3x−6; at x=4, y=6
**Verification:** At input 4, correct gives 6; recheck against the original words, rows or formula.
**Misconception:** The three was not multiplied by −2.
**Targeted repair:** Build three copies of (x−2) and test both given rows.

## Practice bank

1. A learner says double then add 2 gives 2(x+2). Correct output at x=3?
   - Memo: 8. 2×3+2=8; the learner would get 10.

2. 0→7,1→9: learner writes 7x+2. Correct output at x=2?
   - Memo: 11. Use 2x+7, so at two the output is 11.

3. Add 1 then triple: learner writes 3x+1. Correct output at x=2?
   - Memo: 9. 3(2+1)=9.

4. 0→5,2→13: learner calls rate 8. Correct output at x=3?
   - Memo: 17. Rate 8÷2=4 and fixed value 5: 4×3+5=17.

5. R6 once plus R3 per visit. Learner charges 6v+3. Correct for v=4?
   - Memo: 18. 6+3×4=18.

6. −1→−2,0→1,1→4: learner rule 3x−1. Correct output x=2?
   - Memo: 7. The zero row makes the constant +1; 3×2+1=7.

7. y=x²+1 at x=3: learner claims outputs change by two each input. Correct output?
   - Memo: 10. 3²+1=10; the differences grow.

8. Learner expands 3(x+4) as 3x+4. Correct output at x=2?
   - Memo: 18. 3×2+12=18.

9. Perimeter 26 cm and length 9 cm: learner says width 17. Correct width in cm?
   - Memo: 4. Half the perimeter is 13; 13−9=4.

10. 0→3,1→4,2→7: learner chooses x+3. Correct output at x=2?
   - Memo: 7. x²+3 gives 7, while x+3 gives 5.

11. Square side 5: learner uses 4n for area. Correct area in unit squares?
   - Memo: 25. 5²=25; 4×5 is perimeter.

12. Output 23 after tripling then adding 5: learner divides by 3 first. Correct input?
   - Memo: 6. (23−5)÷3=6.

13. −1→0,0→1,1→4: learner claims x²+1. Correct output at x=1?
   - Memo: 4. x²+2x+1 gives 4; learner gives 2.

14. R14 fixed plus R2 per item: learner uses 14x+2. Correct for x=5?
   - Memo: 24. 14+2×5=24.

15. Learner writes 4(x−3)=4x−3. Correct value at x=5?
   - Memo: 8. 4(5−3)=8; correct expansion is 4x−12.

## Mastery bank

1. Double then add 5: learner writes 2(x+5). Correct output x=4?
   - Memo: 13. 2×4+5=13.

2. 0→4,2→10: learner calls rate six. Correct output x=4?
   - Memo: 16. Rate 6/2=3; 3×4+4=16.

3. A square side 8: learner gives perimeter as area. Correct area?
   - Memo: 64. 8×8=64 square units.

4. Output 19 from x→×2→+3. Correct input?
   - Memo: 8. (19−3)/2=8.

5. R12 once plus R5 per trip: learner multiplies twelve. Correct for 4 trips?
   - Memo: 32. 12+5×4=32.

## Reassess bank

1. Add 4 then double: learner writes 2x+4. Correct at x=3?
   - Memo: 14. 2(3+4)=14.

2. 0→9,3→18: learner rate nine. Correct output at x=5?
   - Memo: 24. Rate three: 9+3×5=24.

3. Square side 6: learner uses 4n as area. Correct area?
   - Memo: 36. 6×6=36.

Learner assessment keys stay server-side until submission.
