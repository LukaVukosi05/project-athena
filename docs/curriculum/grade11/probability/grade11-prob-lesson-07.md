# Grade 11 Topic 9, Lesson 7: Mixed probability problems and first-error diagnosis

Curriculum: [DBE Grade 11 ATP](https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2023%20ATPs/FET%20Content%20Subjects/Grade%2011/1.590%20ATP%202023-24%20Gr%2011%20Maths%20final.pdf) and [Mathematics CAPS](https://www.education.gov.za/Portals/0/CD/National%20Curriculum%20Statements%20and%20Vocational/CAPS%20FET%20_%20MATHEMATICS%20_%20GR%2010-12%20_%20Web_1133.pdf).

Original Athena questions and worked steps; teacher review and live browser acceptance required.

Fraction probabilities are exact and simplified. The tree distinguishes replacement from no replacement.

## g11-prob-l07-w01: A bag has 4 red and 6 blue counters. Two are drawn without replacement. A learner uses (4/10) × (4/10) for two red. Find the first error and the correct result.

Question-specific visual values: `{"family": "grade11_probability", "values": {"mode": "tree", "red": 4, "blue": 6, "replacement": false, "target": "two red"}}`

1. The first red branch has probability 4/10.

2. The learner wrongly reused the original bag after removing a red counter.

3. The second red branch is (4-1)/(10-1) = 3/9.

4. Multiply 4/10 × 3/9 = 2/15.

5. Answer: P(two red) = 2/15. Check the second draw has 9 counters.

Answer: P(two red) = 2/15. Check: Answer: P(two red) = 2/15. Check the second draw has 9 counters.

## g11-prob-l07-w02: A survey table has A/X=6, A/Y=5, B/X=7, B/Y=4. A learner claims P(A among Y)=5/22. Find the first error and correct probability.

Question-specific visual values: `{"family": "grade11_probability", "values": {"mode": "table", "cells": [6, 5, 7, 4], "target": "first row given second column"}}`

1. Locate the Y column: A/Y=5 and B/Y=4.

2. The learner used the grand total 22 even though the selection is restricted to Y.

3. The appropriate denominator is the Y column: 5+4=9.

4. The favourable cell is 5 of those 9 Y outcomes.

5. Answer: P(A given Y) = 5/9. The first error was using the wrong denominator.

Answer: P(A given Y) = 5/9. Check: Answer: P(A given Y) = 5/9. The first error was using the wrong denominator.

## g11-prob-l07-w03: A=11, B=12, both=5, neither=2 in a group of 20. A learner claims P(A or B)=23/20. Find and repair the first error.

Question-specific visual values: `{"family": "grade11_probability", "values": {"mode": "venn2", "aonly": 6, "both": 5, "bonly": 7, "neither": 2, "target": "union"}}`

1. Draw the overlap 5 once, with A only 6 and B only 7.

2. The learner added A and B and counted their shared 5 twice.

3. Subtract the overlap: |A or B| = 11 + 12 − 5 = 18.

4. Check 18 + neither 2 = 20.

5. Answer: P(A or B) = 9/10. The first error was double-counting the overlap.

Answer: P(A or B) = 9/10. Check: Answer: P(A or B) = 9/10. The first error was double-counting the overlap.

## g11-prob-l07-w04: A bag has 7 red and 7 blue counters. Two are drawn without replacement. A learner uses (7/14) × (7/14) for two red. Find the first error and the correct result.

Question-specific visual values: `{"family": "grade11_probability", "values": {"mode": "tree", "red": 7, "blue": 7, "replacement": false, "target": "two red"}}`

1. The first red branch has probability 7/14.

2. The learner wrongly reused the original bag after removing a red counter.

3. The second red branch is (7-1)/(14-1) = 6/13.

4. Multiply 7/14 × 6/13 = 3/13.

5. Answer: P(two red) = 3/13. Check the second draw has 13 counters.

Answer: P(two red) = 3/13. Check: Answer: P(two red) = 3/13. Check the second draw has 13 counters.

## g11-prob-l07-w05: A survey table has A/X=9, A/Y=3, B/X=10, B/Y=3. A learner claims P(A among Y)=3/25. Find the first error and correct probability.

Question-specific visual values: `{"family": "grade11_probability", "values": {"mode": "table", "cells": [9, 3, 10, 3], "target": "first row given second column"}}`

1. Locate the Y column: A/Y=3 and B/Y=3.

2. The learner used the grand total 25 even though the selection is restricted to Y.

3. The appropriate denominator is the Y column: 3+3=6.

4. The favourable cell is 3 of those 6 Y outcomes.

5. Answer: P(A given Y) = 1/2. The first error was using the wrong denominator.

Answer: P(A given Y) = 1/2. Check: Answer: P(A given Y) = 1/2. The first error was using the wrong denominator.

## g11-prob-l07-w06: A=8, B=8, both=4, neither=2 in a group of 14. A learner claims P(A or B)=16/14. Find and repair the first error.

Question-specific visual values: `{"family": "grade11_probability", "values": {"mode": "venn2", "aonly": 4, "both": 4, "bonly": 4, "neither": 2, "target": "union"}}`

1. Draw the overlap 4 once, with A only 4 and B only 4.

2. The learner added A and B and counted their shared 4 twice.

3. Subtract the overlap: |A or B| = 8 + 8 − 4 = 12.

4. Check 12 + neither 2 = 14.

5. Answer: P(A or B) = 6/7. The first error was double-counting the overlap.

Answer: P(A or B) = 6/7. Check: Answer: P(A or B) = 6/7. The first error was double-counting the overlap.

## g11-prob-l07-w07: A bag has 5 red and 8 blue counters. Two are drawn without replacement. A learner uses (5/13) × (5/13) for two red. Find the first error and the correct result.

Question-specific visual values: `{"family": "grade11_probability", "values": {"mode": "tree", "red": 5, "blue": 8, "replacement": false, "target": "two red"}}`

1. The first red branch has probability 5/13.

2. The learner wrongly reused the original bag after removing a red counter.

3. The second red branch is (5-1)/(13-1) = 4/12.

4. Multiply 5/13 × 4/12 = 5/39.

5. Answer: P(two red) = 5/39. Check the second draw has 12 counters.

Answer: P(two red) = 5/39. Check: Answer: P(two red) = 5/39. Check the second draw has 12 counters.

## g11-prob-l07-w08: A survey table has A/X=5, A/Y=6, B/X=7, B/Y=2. A learner claims P(A among Y)=6/20. Find the first error and correct probability.

Question-specific visual values: `{"family": "grade11_probability", "values": {"mode": "table", "cells": [5, 6, 7, 2], "target": "first row given second column"}}`

1. Locate the Y column: A/Y=6 and B/Y=2.

2. The learner used the grand total 20 even though the selection is restricted to Y.

3. The appropriate denominator is the Y column: 6+2=8.

4. The favourable cell is 6 of those 8 Y outcomes.

5. Answer: P(A given Y) = 3/4. The first error was using the wrong denominator.

Answer: P(A given Y) = 3/4. Check: Answer: P(A given Y) = 3/4. The first error was using the wrong denominator.

## g11-prob-l07-w09: A=10, B=10, both=3, neither=2 in a group of 19. A learner claims P(A or B)=20/19. Find and repair the first error.

Question-specific visual values: `{"family": "grade11_probability", "values": {"mode": "venn2", "aonly": 7, "both": 3, "bonly": 7, "neither": 2, "target": "union"}}`

1. Draw the overlap 3 once, with A only 7 and B only 7.

2. The learner added A and B and counted their shared 3 twice.

3. Subtract the overlap: |A or B| = 10 + 10 − 3 = 17.

4. Check 17 + neither 2 = 19.

5. Answer: P(A or B) = 17/19. The first error was double-counting the overlap.

Answer: P(A or B) = 17/19. Check: Answer: P(A or B) = 17/19. The first error was double-counting the overlap.

## g11-prob-l07-w10: A bag has 3 red and 4 blue counters. Two are drawn without replacement. A learner uses (3/7) × (3/7) for two red. Find the first error and the correct result.

Question-specific visual values: `{"family": "grade11_probability", "values": {"mode": "tree", "red": 3, "blue": 4, "replacement": false, "target": "two red"}}`

1. The first red branch has probability 3/7.

2. The learner wrongly reused the original bag after removing a red counter.

3. The second red branch is (3-1)/(7-1) = 2/6.

4. Multiply 3/7 × 2/6 = 1/7.

5. Answer: P(two red) = 1/7. Check the second draw has 6 counters.

Answer: P(two red) = 1/7. Check: Answer: P(two red) = 1/7. Check the second draw has 6 counters.

## g11-prob-l07-w11: A survey table has A/X=8, A/Y=4, B/X=10, B/Y=5. A learner claims P(A among Y)=4/27. Find the first error and correct probability.

Question-specific visual values: `{"family": "grade11_probability", "values": {"mode": "table", "cells": [8, 4, 10, 5], "target": "first row given second column"}}`

1. Locate the Y column: A/Y=4 and B/Y=5.

2. The learner used the grand total 27 even though the selection is restricted to Y.

3. The appropriate denominator is the Y column: 4+5=9.

4. The favourable cell is 4 of those 9 Y outcomes.

5. Answer: P(A given Y) = 4/9. The first error was using the wrong denominator.

Answer: P(A given Y) = 4/9. Check: Answer: P(A given Y) = 4/9. The first error was using the wrong denominator.

## g11-prob-l07-w12: A=7, B=6, both=2, neither=2 in a group of 13. A learner claims P(A or B)=13/13. Find and repair the first error.

Question-specific visual values: `{"family": "grade11_probability", "values": {"mode": "venn2", "aonly": 5, "both": 2, "bonly": 4, "neither": 2, "target": "union"}}`

1. Draw the overlap 2 once, with A only 5 and B only 4.

2. The learner added A and B and counted their shared 2 twice.

3. Subtract the overlap: |A or B| = 7 + 6 − 2 = 11.

4. Check 11 + neither 2 = 13.

5. Answer: P(A or B) = 11/13. The first error was double-counting the overlap.

Answer: P(A or B) = 11/13. Check: Answer: P(A or B) = 11/13. The first error was double-counting the overlap.

## g11-prob-l07-w13: A bag has 6 red and 5 blue counters. Two are drawn without replacement. A learner uses (6/11) × (6/11) for two red. Find the first error and the correct result.

Question-specific visual values: `{"family": "grade11_probability", "values": {"mode": "tree", "red": 6, "blue": 5, "replacement": false, "target": "two red"}}`

1. The first red branch has probability 6/11.

2. The learner wrongly reused the original bag after removing a red counter.

3. The second red branch is (6-1)/(11-1) = 5/10.

4. Multiply 6/11 × 5/10 = 3/11.

5. Answer: P(two red) = 3/11. Check the second draw has 10 counters.

Answer: P(two red) = 3/11. Check: Answer: P(two red) = 3/11. Check the second draw has 10 counters.

## g11-prob-l07-w14: A survey table has A/X=4, A/Y=7, B/X=7, B/Y=4. A learner claims P(A among Y)=7/22. Find the first error and correct probability.

Question-specific visual values: `{"family": "grade11_probability", "values": {"mode": "table", "cells": [4, 7, 7, 4], "target": "first row given second column"}}`

1. Locate the Y column: A/Y=7 and B/Y=4.

2. The learner used the grand total 22 even though the selection is restricted to Y.

3. The appropriate denominator is the Y column: 7+4=11.

4. The favourable cell is 7 of those 11 Y outcomes.

5. Answer: P(A given Y) = 7/11. The first error was using the wrong denominator.

Answer: P(A given Y) = 7/11. Check: Answer: P(A given Y) = 7/11. The first error was using the wrong denominator.

## g11-prob-l07-w15: A=8, B=12, both=5, neither=2 in a group of 17. A learner claims P(A or B)=20/17. Find and repair the first error.

Question-specific visual values: `{"family": "grade11_probability", "values": {"mode": "venn2", "aonly": 3, "both": 5, "bonly": 7, "neither": 2, "target": "union"}}`

1. Draw the overlap 5 once, with A only 3 and B only 7.

2. The learner added A and B and counted their shared 5 twice.

3. Subtract the overlap: |A or B| = 8 + 12 − 5 = 15.

4. Check 15 + neither 2 = 17.

5. Answer: P(A or B) = 15/17. The first error was double-counting the overlap.

Answer: P(A or B) = 15/17. Check: Answer: P(A or B) = 15/17. The first error was double-counting the overlap.

## Practice key

- g11-prob-l07-p01: A bag has 4 red and 6 blue counters. Two are drawn without replacement. A learner uses (4/10) × (4/10) for two red. Find the first error and the correct result. Options: P(two red) = 1/3 | P(two red) = 4/15 | P(two red) = 2/15 | P(two red) = 4/25. Correct: P(two red) = 2/15. The first red branch has probability 4/10. The learner wrongly reused the original bag after removing a red counter. The second red branch is (4-1)/(10-1) = 3/9. Multiply 4/10 × 3/9 = 2/15. Answer: P(two red) = 2/15. Check the second draw has 9 counters.

- g11-prob-l07-p02: A survey table has A/X=7, A/Y=5, B/X=10, B/Y=3. A learner claims P(A among Y)=5/25. Find the first error and correct probability. Options: P(A given Y) = 3/8 | P(A given Y) = 5/8 | P(A given Y) = 1/5 | P(A given Y) = 7/17. Correct: P(A given Y) = 5/8. Locate the Y column: A/Y=5 and B/Y=3. The learner used the grand total 25 even though the selection is restricted to Y. The appropriate denominator is the Y column: 5+3=8. The favourable cell is 5 of those 8 Y outcomes. Answer: P(A given Y) = 5/8. The first error was using the wrong denominator.

- g11-prob-l07-p03: A=10, B=8, both=4, neither=2 in a group of 16. A learner claims P(A or B)=18/16. Find and repair the first error. Options: P(A or B) = 7/8 | P(A or B) = 9/8 | P(A or B) = 5/8 | P(A or B) = 1/8. Correct: P(A or B) = 7/8. Draw the overlap 4 once, with A only 6 and B only 4. The learner added A and B and counted their shared 4 twice. Subtract the overlap: |A or B| = 10 + 8 − 4 = 14. Check 14 + neither 2 = 16. Answer: P(A or B) = 7/8. The first error was double-counting the overlap.

- g11-prob-l07-p04: A bag has 7 red and 7 blue counters. Two are drawn without replacement. A learner uses (7/14) × (7/14) for two red. Find the first error and the correct result. Options: P(two red) = 1/4 | P(two red) = 6/13 | P(two red) = 7/26 | P(two red) = 3/13. Correct: P(two red) = 3/13. The first red branch has probability 7/14. The learner wrongly reused the original bag after removing a red counter. The second red branch is (7-1)/(14-1) = 6/13. Multiply 7/14 × 6/13 = 3/13. Answer: P(two red) = 3/13. Check the second draw has 13 counters.

- g11-prob-l07-p05: A survey table has A/X=10, A/Y=3, B/X=7, B/Y=2. A learner claims P(A among Y)=3/22. Find the first error and correct probability. Options: P(A given Y) = 10/17 | P(A given Y) = 2/5 | P(A given Y) = 3/5 | P(A given Y) = 3/22. Correct: P(A given Y) = 3/5. Locate the Y column: A/Y=3 and B/Y=2. The learner used the grand total 22 even though the selection is restricted to Y. The appropriate denominator is the Y column: 3+2=5. The favourable cell is 3 of those 5 Y outcomes. Answer: P(A given Y) = 3/5. The first error was using the wrong denominator.

- g11-prob-l07-p06: A=7, B=10, both=3, neither=2 in a group of 16. A learner claims P(A or B)=17/16. Find and repair the first error. Options: P(A or B) = 1/8 | P(A or B) = 7/8 | P(A or B) = 17/16 | P(A or B) = 11/16. Correct: P(A or B) = 7/8. Draw the overlap 3 once, with A only 4 and B only 7. The learner added A and B and counted their shared 3 twice. Subtract the overlap: |A or B| = 7 + 10 − 3 = 14. Check 14 + neither 2 = 16. Answer: P(A or B) = 7/8. The first error was double-counting the overlap.

- g11-prob-l07-p07: A bag has 5 red and 8 blue counters. Two are drawn without replacement. A learner uses (5/13) × (5/13) for two red. Find the first error and the correct result. Options: P(two red) = 5/39 | P(two red) = 25/169 | P(two red) = 1/3 | P(two red) = 10/39. Correct: P(two red) = 5/39. The first red branch has probability 5/13. The learner wrongly reused the original bag after removing a red counter. The second red branch is (5-1)/(13-1) = 4/12. Multiply 5/13 × 4/12 = 5/39. Answer: P(two red) = 5/39. Check the second draw has 12 counters.

- g11-prob-l07-p08: A survey table has A/X=6, A/Y=6, B/X=10, B/Y=5. A learner claims P(A among Y)=6/27. Find the first error and correct probability. Options: P(A given Y) = 2/9 | P(A given Y) = 3/8 | P(A given Y) = 5/11 | P(A given Y) = 6/11. Correct: P(A given Y) = 6/11. Locate the Y column: A/Y=6 and B/Y=5. The learner used the grand total 27 even though the selection is restricted to Y. The appropriate denominator is the Y column: 6+5=11. The favourable cell is 6 of those 11 Y outcomes. Answer: P(A given Y) = 6/11. The first error was using the wrong denominator.

- g11-prob-l07-p09: A=9, B=6, both=2, neither=2 in a group of 15. A learner claims P(A or B)=15/15. Find and repair the first error. Options: P(A or B) = 11/15 | P(A or B) = 2/15 | P(A or B) = 13/15 | P(A or B) = 1. Correct: P(A or B) = 13/15. Draw the overlap 2 once, with A only 7 and B only 4. The learner added A and B and counted their shared 2 twice. Subtract the overlap: |A or B| = 9 + 6 − 2 = 13. Check 13 + neither 2 = 15. Answer: P(A or B) = 13/15. The first error was double-counting the overlap.

- g11-prob-l07-p10: A bag has 3 red and 4 blue counters. Two are drawn without replacement. A learner uses (3/7) × (3/7) for two red. Find the first error and the correct result. Options: P(two red) = 2/7 | P(two red) = 1/7 | P(two red) = 9/49 | P(two red) = 1/3. Correct: P(two red) = 1/7. The first red branch has probability 3/7. The learner wrongly reused the original bag after removing a red counter. The second red branch is (3-1)/(7-1) = 2/6. Multiply 3/7 × 2/6 = 1/7. Answer: P(two red) = 1/7. Check the second draw has 6 counters.

- g11-prob-l07-p11: A survey table has A/X=9, A/Y=4, B/X=7, B/Y=4. A learner claims P(A among Y)=4/24. Find the first error and correct probability. Options: P(A given Y) = 1/2 | P(A given Y) = 1/6 | P(A given Y) = 9/16 | P(A given Y) = 21/40. Correct: P(A given Y) = 1/2. Locate the Y column: A/Y=4 and B/Y=4. The learner used the grand total 24 even though the selection is restricted to Y. The appropriate denominator is the Y column: 4+4=8. The favourable cell is 4 of those 8 Y outcomes. Answer: P(A given Y) = 1/2. The first error was using the wrong denominator.

- g11-prob-l07-p12: A=10, B=12, both=5, neither=2 in a group of 19. A learner claims P(A or B)=22/19. Find and repair the first error. Options: P(A or B) = 22/19 | P(A or B) = 12/19 | P(A or B) = 2/19 | P(A or B) = 17/19. Correct: P(A or B) = 17/19. Draw the overlap 5 once, with A only 5 and B only 7. The learner added A and B and counted their shared 5 twice. Subtract the overlap: |A or B| = 10 + 12 − 5 = 17. Check 17 + neither 2 = 19. Answer: P(A or B) = 17/19. The first error was double-counting the overlap.

- g11-prob-l07-p13: A bag has 6 red and 5 blue counters. Two are drawn without replacement. A learner uses (6/11) × (6/11) for two red. Find the first error and the correct result. Options: P(two red) = 1/2 | P(two red) = 131/440 | P(two red) = 3/11 | P(two red) = 36/121. Correct: P(two red) = 3/11. The first red branch has probability 6/11. The learner wrongly reused the original bag after removing a red counter. The second red branch is (6-1)/(11-1) = 5/10. Multiply 6/11 × 5/10 = 3/11. Answer: P(two red) = 3/11. Check the second draw has 10 counters.

- g11-prob-l07-p14: A survey table has A/X=5, A/Y=7, B/X=10, B/Y=3. A learner claims P(A among Y)=7/25. Find the first error and correct probability. Options: P(A given Y) = 3/10 | P(A given Y) = 7/10 | P(A given Y) = 7/25 | P(A given Y) = 1/3. Correct: P(A given Y) = 7/10. Locate the Y column: A/Y=7 and B/Y=3. The learner used the grand total 25 even though the selection is restricted to Y. The appropriate denominator is the Y column: 7+3=10. The favourable cell is 7 of those 10 Y outcomes. Answer: P(A given Y) = 7/10. The first error was using the wrong denominator.

- g11-prob-l07-p15: A=7, B=8, both=4, neither=2 in a group of 13. A learner claims P(A or B)=15/13. Find and repair the first error. Options: P(A or B) = 11/13 | P(A or B) = 15/13 | P(A or B) = 7/13 | P(A or B) = 2/13. Correct: P(A or B) = 11/13. Draw the overlap 4 once, with A only 3 and B only 4. The learner added A and B and counted their shared 4 twice. Subtract the overlap: |A or B| = 7 + 8 − 4 = 11. Check 11 + neither 2 = 13. Answer: P(A or B) = 11/13. The first error was double-counting the overlap.

## Mastery key

- g11-prob-l07-m01: A bag has 4 red and 6 blue counters. Two are drawn without replacement. A learner uses (4/10) × (4/10) for two red. Find the first error and the correct result. Options: P(two red) = 4/15 | P(two red) = 2/15 | P(two red) = 4/25 | P(two red) = 1/3. Correct: P(two red) = 2/15. The first red branch has probability 4/10. The learner wrongly reused the original bag after removing a red counter. The second red branch is (4-1)/(10-1) = 3/9. Multiply 4/10 × 3/9 = 2/15. Answer: P(two red) = 2/15. Check the second draw has 9 counters.

- g11-prob-l07-m02: A survey table has A/X=8, A/Y=5, B/X=7, B/Y=2. A learner claims P(A among Y)=5/22. Find the first error and correct probability. Options: P(A given Y) = 5/7 | P(A given Y) = 5/22 | P(A given Y) = 8/15 | P(A given Y) = 2/7. Correct: P(A given Y) = 5/7. Locate the Y column: A/Y=5 and B/Y=2. The learner used the grand total 22 even though the selection is restricted to Y. The appropriate denominator is the Y column: 5+2=7. The favourable cell is 5 of those 7 Y outcomes. Answer: P(A given Y) = 5/7. The first error was using the wrong denominator.

- g11-prob-l07-m03: A=9, B=10, both=3, neither=2 in a group of 18. A learner claims P(A or B)=19/18. Find and repair the first error. Options: P(A or B) = 19/18 | P(A or B) = 13/18 | P(A or B) = 1/9 | P(A or B) = 8/9. Correct: P(A or B) = 8/9. Draw the overlap 3 once, with A only 6 and B only 7. The learner added A and B and counted their shared 3 twice. Subtract the overlap: |A or B| = 9 + 10 − 3 = 16. Check 16 + neither 2 = 18. Answer: P(A or B) = 8/9. The first error was double-counting the overlap.

- g11-prob-l07-m04: A bag has 7 red and 7 blue counters. Two are drawn without replacement. A learner uses (7/14) × (7/14) for two red. Find the first error and the correct result. Options: P(two red) = 6/13 | P(two red) = 7/26 | P(two red) = 3/13 | P(two red) = 1/4. Correct: P(two red) = 3/13. The first red branch has probability 7/14. The learner wrongly reused the original bag after removing a red counter. The second red branch is (7-1)/(14-1) = 6/13. Multiply 7/14 × 6/13 = 3/13. Answer: P(two red) = 3/13. Check the second draw has 13 counters.

- g11-prob-l07-m05: A survey table has A/X=4, A/Y=3, B/X=10, B/Y=5. A learner claims P(A among Y)=3/22. Find the first error and correct probability. Options: P(A given Y) = 5/8 | P(A given Y) = 3/8 | P(A given Y) = 3/22 | P(A given Y) = 2/7. Correct: P(A given Y) = 3/8. Locate the Y column: A/Y=3 and B/Y=5. The learner used the grand total 22 even though the selection is restricted to Y. The appropriate denominator is the Y column: 3+5=8. The favourable cell is 3 of those 8 Y outcomes. Answer: P(A given Y) = 3/8. The first error was using the wrong denominator.

## Reassessment key

- g11-prob-l07-r01: A bag has 4 red and 6 blue counters. Two are drawn without replacement. A learner uses (4/10) × (4/10) for two red. Find the first error and the correct result. Options: P(two red) = 2/15 | P(two red) = 4/25 | P(two red) = 1/3 | P(two red) = 4/15. Correct: P(two red) = 2/15. The first red branch has probability 4/10. The learner wrongly reused the original bag after removing a red counter. The second red branch is (4-1)/(10-1) = 3/9. Multiply 4/10 × 3/9 = 2/15. Answer: P(two red) = 2/15. Check the second draw has 9 counters.

- g11-prob-l07-r02: A survey table has A/X=9, A/Y=5, B/X=10, B/Y=5. A learner claims P(A among Y)=5/29. Find the first error and correct probability. Options: P(A given Y) = 5/29 | P(A given Y) = 9/19 | P(A given Y) = 21/40 | P(A given Y) = 1/2. Correct: P(A given Y) = 1/2. Locate the Y column: A/Y=5 and B/Y=5. The learner used the grand total 29 even though the selection is restricted to Y. The appropriate denominator is the Y column: 5+5=10. The favourable cell is 5 of those 10 Y outcomes. Answer: P(A given Y) = 1/2. The first error was using the wrong denominator.

- g11-prob-l07-r03: A=8, B=6, both=2, neither=2 in a group of 14. A learner claims P(A or B)=14/14. Find and repair the first error. Options: P(A or B) = 5/7 | P(A or B) = 1/7 | P(A or B) = 6/7 | P(A or B) = 1. Correct: P(A or B) = 6/7. Draw the overlap 2 once, with A only 6 and B only 4. The learner added A and B and counted their shared 2 twice. Subtract the overlap: |A or B| = 8 + 6 − 2 = 12. Check 12 + neither 2 = 14. Answer: P(A or B) = 6/7. The first error was double-counting the overlap.
