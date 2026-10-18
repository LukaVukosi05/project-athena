---
id: g12-aei-01
grade: 12
subject: mathematics
topic: algebra-equations-and-inequalities
lesson_number: 1
title: Algebra readiness diagnostic
paper: 1
term: pending_authority_review
duration_minutes: 75
mastery_threshold: 80
prerequisites: []
caps_outcomes: [algebraic manipulation, equations and inequalities]
cognitive_levels: {knowledge: 6, routine_procedures: 8, complex_procedures: 7, problem_solving: 3}
status: authored-not-integrated
source_document: DBE CAPS Mathematics Grades 10-12
---

# Algebra readiness diagnostic

## Learning objective

**Identify and repair prerequisite weaknesses in signs, fractions, exponents, expansion, factorisation, substitution and equation balance.**

## CAPS scope

This targeted readiness lesson revises only tools needed for Grade 12 algebra. It supports CAPS algebraic manipulation and equations; it is not a replacement Grade 10 course. Evidence from each diagnostic item routes the learner to a short repair segment.

## Prerequisite knowledge and diagnostic entry

Attempt D1–D4 without notes. Record the first line where reasoning breaks, not only the final score.

1. **D1:** Evaluate `−7+12−9`. Expected `−4`; a wrong answer routes to **R1 signs**.
2. **D2:** Calculate `3/4−5/6`. Expected `−1/12`; route to **R2 fractions**.
3. **D3:** Simplify `2x³·3x²÷x`. Expected `6x⁴`, with `x≠0` for the written quotient; route to **R3 exponents/restrictions**.
4. **D4:** Solve `3(x−2)=2x+5`. Expected `x=11`; route to **R4 expansion/equation balance**.

Serious evidence codes are `negative-sign`, `exponent-law`, and `one-sided-equation-operation`. They must be repaired before mastery.

## Conceptual teaching explanation

Algebra is a language of structure. An **expression** such as `3x−2` names a value; an **equation** such as `3x−2=10` claims two expressions are equal; an **inequality** such as `3x−2<10` compares their order. An equals sign is a balance, not an instruction to calculate whatever is on its left.

### R1 — signs

Subtraction means adding an opposite: `a−b=a+(−b)`. Multiplication or division of like signs is positive; unlike signs is negative. Brackets protect the sign of a substituted value: for `x=−3`, `x²=(−3)²=9`, while `−x²=−(x²)=−9`.

### R2 — fractions

Addition and subtraction require equivalent fractions with a common denominator. Multiplication acts numerator-to-numerator and denominator-to-denominator. Division means multiplication by the reciprocal. A denominator may never be zero.

### R3 — exponent laws and restrictions

Exponent laws apply to powers with the same base: `x^m·x^n=x^(m+n)`, `x^m/x^n=x^(m−n)` for `x≠0`, and `(x^m)^n=x^(mn)`. They do not turn `x^2+x^3` into `x^5` because addition is not multiplication.

### R4 — expansion, like terms and factorisation

The distributive law gives `a(b+c)=ab+ac`. Only like terms combine: `3x+2x=5x`, but `3x+2x²` cannot combine. Factorisation reverses expansion: `ab+ac=a(b+c)`.

### R5 — substitution and equation balance

Substitution replaces a symbol with a bracketed value. Solving an equation preserves its solution set by performing a legal reversible operation on both sides. For `2x−8=20`, add 8 to both sides, then divide both sides by 2. Never teach “move it and change the sign” as the reason.

### R6 — restrictions

An expression such as `5/x` carries `x≠0`. A later cancellation cannot restore a value excluded by the original expression.

## Vocabulary and notation

| Term | Meaning |
|---|---|
| expression | mathematical phrase with no relation sign |
| equation | statement that two expressions are equal |
| inequality | comparison using `<`, `>`, `≤` or `≥` |
| term | part separated by addition/subtraction at the outer level |
| factor | quantity multiplied to form a product |
| coefficient | numerical factor of a variable term |
| exponent | number of repeated factors represented by a power |
| substitute | replace a symbol by a specified value |
| restriction | value excluded because an original operation would be undefined |
| equivalent | same value/solution set on the stated domain |

## Teacher-style narration

“Today is a diagnostic, not a judgement. Each answer tells us which small tool to repair before Grade 12 algebra becomes demanding. Watch the structure: signs attach to terms, exponent laws follow operations, and an equation stays true only when both sides remain balanced.”

## Primary worked examples and semantic whiteboard specifications

### Example 1 — sign and substitution discipline

Evaluate `2a²−3b` for `a=−2`, `b=5`.

1. Substitute with brackets: `2(−2)²−3(5)`.
2. Evaluate the power before the leading multiplication: `2(4)−15`.
3. Calculate: `8−15=−7`.
4. Verify independently: `a²=4` and `3b=15`, hence `2a²−3b=8−15`.

Timeline:

```yaml
instructional_goal: preserve negative values during substitution
events:
  - {type: focus, targets: [a, b]}
  - {type: substitute, targets: [a, b], values: [-2, 5]}
  - {type: reveal, target: substituted-expression, value: "2(-2)^2-3(5)"}
  - {type: checkpoint, prompt: "Is (-2)^2 positive or negative?"}
  - {type: write, target: power-result, value: "2(4)-15"}
  - {type: verify, target: final, value: "-7"}
accessibility_text: "Negative two is enclosed in brackets before it is squared."
```

### Example 2 — legal operations on an equation

Solve `2x−8=20`.

1. Goal: isolate `2x`; the attached `−8` is undone by `+8`.
2. `2x−8+8=20+8` (add 8 to **both** sides).
3. `2x=28`.
4. `(2x)/2=28/2` (divide **both** sides by 2).
5. `x=14`.
6. Verify in the original: `2(14)−8=28−8=20`.

```yaml
instructional_goal: preserve equality while isolating x
events:
  - {type: focus, targets: [variable-term, attached-negative-eight]}
  - {type: dim, targets: [unrelated-caption]}
  - {type: apply_both_sides, operation: "+8", targets: [left-side, right-side]}
  - {type: cancel_factor, targets: [negative-eight, positive-eight], semantic_role: additive-inverses}
  - {type: reveal, target: equation-state-2, value: "2x=28"}
  - {type: checkpoint, prompt: "Which operation isolates x now?"}
  - {type: apply_both_sides, operation: "/2", targets: [left-side, right-side]}
  - {type: verify, target: original-equation, substitution: 14}
accessibility_text: "Eight is added to both sides; then both sides are divided by two."
```

### Example 3 — exponent law versus unlike terms

Simplify `(6x⁵)/(3x²)+2x³`.

1. Mark restriction `x≠0` from the original denominator.
2. Divide coefficients and subtract exponents in the quotient: `(6/3)x^(5−2)=2x³`.
3. Collect like terms: `2x³+2x³=4x³`.
4. Verify at permitted `x=2`: original `= (6·32)/(3·4)+16=16+16=32`; simplified `4·8=32`.

```yaml
instructional_goal: apply exponent laws only inside multiplication or division
events:
  - {type: mark_restriction, value: "x != 0"}
  - {type: group, targets: [coefficient-quotient, power-quotient]}
  - {type: write, target: exponent-operation, value: "x^(5-2)"}
  - {type: compare, targets: [first-2x3, second-2x3], relation: like-terms}
  - {type: reveal, target: final, value: "4x^3"}
  - {type: verify, permitted_value: 2}
accessibility_text: "The quotient becomes two x cubed, which combines with the like term."
```

## Learner checkpoints

- Before squaring a negative substitution: “Where must the brackets go?”
- Before combining terms: “Do the variable parts match exactly?”
- Before changing an equation: “What matching operation keeps the balance?”
- Before simplifying a quotient: “Which values make the original denominator zero?”

## Common misconceptions and repair

| Misconception | Diagnostic evidence | Repair |
|---|---|---|
| `−3²=9` | ignores operation order | Compare `−(3²)` with `(−3)²`; brackets decide what is squared. |
| `x²+x³=x⁵` | transfers product law to addition | Expand with `x=2`: `4+8=12`, not `32`; unlike powers do not combine. |
| `a/b+c/d=(a+c)/(b+d)` | adds denominators | Build equivalent fractions using a common denominator. |
| changes one equation side only | treats equality as an arrow | Use a balance diagram and matched `apply_both_sides` events. |
| cancels an excluded value back into the domain | loses original restriction | Mark restrictions before simplification and carry them to the answer. |

## Self-guided practice bank

The 24 original items below are authored for the eventual solve → submit → feedback → hint → worked solution flow. Solutions must remain collapsed until an attempt. `K/R/C/P` mean knowledge/routine/complex/problem-solving. Every item uses source metadata `DBE CAPS scope; Athena original`.

### Diagnostic (4)

1. **g12-aei-l01-d01 | foundation | K | 1 | numeric.** Prompt: `−8+3−6`. Accepted: `−11`. Hints: rewrite subtraction as adding a negative; move on a number line. Solution: `−8+3=−5`, then `−5−6=−11`. **Why?** Subtracting 6 moves six units left. Verify by regrouping `3+(−8−6)=3−14`.
2. **g12-aei-l01-d02 | foundation | R | 2 | numeric.** Prompt: `5/6−3/4`. Accepted: `1/12`. Hints: find LCM 12; rewrite both fractions. Solution: `10/12−9/12=1/12`. **Why?** Only equivalent parts with the same unit size may be subtracted. Verify decimal values differ by `0.0833…`.
3. **g12-aei-l01-d03 | foundation | K | 2 | short_text.** Prompt: simplify `x⁴·x³/x²` and state a restriction. Accepted: `x⁵, x≠0`. Hints: multiply means add exponents; division means subtract and denominator sets a restriction. Solution: `x^(4+3−2)=x⁵`, original denominator requires `x≠0`. **Why?** Cancelling repeated factors assumes a non-zero divisor. Verify at `x=2`.
4. **g12-aei-l01-d04 | easy | R | 2 | numeric.** Prompt: solve `4(x−1)=2x+10`. Accepted: `7`. Hints: expand first; apply the same subtraction/addition to both sides. Solution: `4x−4=2x+10`; subtract `2x`, add `4`: `2x=14`; divide by 2: `x=7`. **Why?** Matching operations preserve equality. Verify both sides equal 24.

### Guided (6)

5. **g12-aei-l01-g01 | foundation | K | 1 | classification.** Classify `7x−4`. Accepted: expression. Hints: look for a relation sign; there is none. Solution: it is an expression. **Why?** It names a value but makes no equality/comparison claim. Verification: no `=,<,>,≤,≥` occurs.
6. **g12-aei-l01-g02 | foundation | K | 1 | classification.** Classify `2x+1≤9`. Accepted: inequality. Hints: identify `≤`; compare, do not equate. Solution: inequality. **Why?** `≤` compares an order relation. Verification: replacing it with `=` changes the statement.
7. **g12-aei-l01-g03 | easy | R | 2 | numeric.** Evaluate `3p²−2q` for `p=−2,q=−1`. Accepted: `14`. Hints: bracket negative substitutions; powers before subtraction. Solution: `3(−2)²−2(−1)=12+2=14`. **Why?** Brackets preserve the substituted signs. Verify directly.
8. **g12-aei-l01-g04 | easy | R | 2 | short_text.** Simplify `5a−2b+3a+7b`. Accepted: `8a+5b`. Hints: group identical variable parts; add coefficients. Solution: `(5a+3a)+(−2b+7b)=8a+5b`. **Why?** Only like terms represent the same unit. Verify at `a=1,b=2`.
9. **g12-aei-l01-g05 | easy | R | 2 | short_text.** Expand `−3(2x−5)`. Accepted: `−6x+15`. Hints: multiply both bracket terms; track `negative × negative`. Solution: `−3·2x+(-3)(−5)=−6x+15`. **Why?** Distribution multiplies every term. Verify by re-factorising `−3(2x−5)`.
10. **g12-aei-l01-g06 | easy | R | 2 | short_text.** Factorise `8y²−12y`. Accepted: `4y(2y−3)`. Hints: find the numerical HCF; include the lowest power of `y`. Solution: `8y²−12y=4y(2y−3)`. **Why?** Factorisation reverses distribution. Verify by expansion.

### Independent and mixed (10)

11. **g12-aei-l01-i01 | standard | R | 2 | numeric.** Calculate `(-3/5)÷(9/10)`. Accepted: `−2/3`. Hints: multiply by reciprocal; cancel common factors. Solution: `(-3/5)(10/9)=−30/45=−2/3`. **Why?** Multiplying by the reciprocal undoes division. Verify `(-2/3)(9/10)=−3/5`.
12. **g12-aei-l01-i02 | standard | C | 3 | short_text.** Simplify `(2m³n²)²/(4mn)`, stating restrictions. Accepted: `m⁵n³, m≠0,n≠0`. Hints: power each factor; subtract denominator exponents. Solution: numerator `4m⁶n⁴`; quotient `m⁵n³`; original denominator requires `m,n≠0`. **Why?** Quotient cancellation assumes non-zero factors. Verify at `(2,1)`.
13. **g12-aei-l01-i03 | standard | C | 3 | numeric.** Solve `5−2(3x−1)=−9`. Accepted: `8/3`. Hints: expand `−2`; preserve both sides. Solution: `5−6x+2=−9`; `7−6x=−9`; subtract 7: `−6x=−16`; divide: `x=8/3`. **Why?** Each reversible operation preserves solutions. Verify substitution.
14. **g12-aei-l01-i04 | standard | C | 3 | short_text.** Simplify `2(x−3)−(x+4)+5`. Accepted: `x−5`. Hints: distribute the minus; collect constants. Solution: `2x−6−x−4+5=x−5`. **Why?** Subtracting a bracket changes both enclosed signs. Verify at `x=0`.
15. **g12-aei-l01-i05 | standard | C | 3 | short_text.** Make `h` the subject of `V=πr²h`. Accepted: `h=V/(πr²)`, `r≠0`. Hints: identify the factor multiplying `h`; divide both sides. Solution: `V/(πr²)=h`, provided `r≠0`. **Why?** Division by the same non-zero factor preserves equality. Substitute back.
16. **g12-aei-l01-i06 | standard | C | 3 | short_text.** Simplify `3(2x−1)−2(x+4)`. Accepted: `4x−11`. Hints: expand each product; combine like terms. Solution: `6x−3−2x−8=4x−11`. **Why?** Distribution precedes collection. Verify at `x=2`.
17. **g12-aei-l01-i07 | intermediate | C | 3 | numeric.** If `a=−1/2`, evaluate `4a³−2a`. Accepted: `1/2`. Hints: bracket the fraction; cube first. Solution: `4(−1/8)−2(−1/2)=−1/2+1=1/2`. **Why?** Odd powers retain a negative sign. Verify exactly.
18. **g12-aei-l01-i08 | intermediate | C | 3 | short_text.** Simplify `(x²−4x)/x` and state restrictions. Accepted: `x−4, x≠0`. Hints: factor numerator `x(x−4)`; only a common factor cancels. Solution: `x(x−4)/x=x−4`, retaining `x≠0`. **Why?** The original quotient is undefined at zero. Verify at `x=2`; compare domains.
19. **g12-aei-l01-i09 | intermediate | K | 4 | error_analysis.** Sam says `(a+b)²=a²+b²`. Explain and correct. Accepted: missing middle term; `a²+2ab+b²`. Hints: write two brackets; distribute every term. Solution: `(a+b)(a+b)=a²+ab+ab+b²`. **Why?** Both cross-products are part of multiplication. Verify with `a=b=1`: 4, not 2.
20. **g12-aei-l01-i10 | intermediate | P | 4 | short_text.** A rectangle has sides `x+3` and `x−2`. Write expanded area and state a meaningful restriction if lengths are positive. Accepted: `x²+x−6, x>2`. Hints: multiply binomials; both lengths must exceed zero. Solution: area `x²+x−6`; `x+3>0` and `x−2>0`, hence `x>2`. **Why?** Context can narrow an algebraic domain. Verify by factorising.

### Misconception/error analysis (2)

21. **g12-aei-l01-m01 | standard | K | 2 | error_analysis.** Learner writes `−2³=8`. Identify first error. Accepted: the exponent applies before the leading minus; answer `−8`. Hints: insert implied brackets; compare `−(2³)` and `(−2)³`. Solution: both are `−8` here; the stated positive sign is impossible for an odd power. **Why?** Three negative factors would also give a negative product. Verify multiplication.
22. **g12-aei-l01-m02 | standard | R | 3 | error_analysis.** From `3x+4=19`, a learner subtracts 4 only on the left. Accepted: equality was not preserved. Hints: draw a balance; use the same operation both sides. Solution: `3x+4−4=19−4`; `3x=15`; `x=5`. **Why?** One-sided change creates a different statement. Verify `3(5)+4=19`.

### Original exam-style (2)

23. **g12-aei-l01-e01 | advanced | P | 5 | short_text.** For non-zero `p,q`, simplify `[(6p⁻²q³)/(3pq⁻¹)]·p⁴/q²` with positive exponents. Accepted: `2pq²`. Hints: handle the first quotient exponent-by-exponent; then multiply. Solution: first quotient `2p⁻³q⁴`; product `2p^(−3+4)q^(4−2)=2pq²`. **Why?** Laws apply independently to like bases. Verify at `p=2,q=1`.
24. **g12-aei-l01-e02 | advanced | P | 5 | numeric.** Solve and verify `(2x−1)/3−(x+2)/2=1`. Accepted: `x=14`. Hints: multiply both sides by LCD 6; expand before collecting. Solution: `2(2x−1)−3(x+2)=6`; `4x−2−3x−6=6`; `x−8=6`; `x=14`. **Why?** Multiplying every term by non-zero 6 clears denominators without changing solutions. Verification: `27/3−16/2=9−8=1`.

## Exit quiz, mastery and remediation

Use D2, G5, I2, I3, I8, M2, E1 and E2 as an eight-item exit set. Mastery is 80–100%; 60–79% routes only to tagged repair segments; below 60% returns to the relevant teaching segment. Any unresolved serious misconception (`negative-sign`, `exponent-law`, `one-sided-equation-operation`) blocks mastery until a correction item is passed. Hints do not reduce academic credit; independence is reported separately.

## Content QA checklist

- [x] 24 unique original items: 4 diagnostic, 6 guided, 10 independent/mixed, 2 misconception, 2 exam-style.
- [x] Cognitive allocation: K6/R8/C7/P3.
- [x] Negative signs, fractions, exponents, expansion, like terms, factorisation, substitution, balance and restrictions covered.
- [x] Every equation change acts on both sides.
- [x] Worked examples end in substitution/numerical verification.
- [x] Semantic events contain no executable content.
- [x] Solutions are specified separately from the teaching whiteboard.
