---
id: g12-aei-03
grade: 12
subject: mathematics
topic: algebra-equations-and-inequalities
lesson_number: 3
title: Algebraic fractions and restrictions
paper: 1
term: pending_authority_review
duration_minutes: 100
mastery_threshold: 80
prerequisites: [g12-aei-01, g12-aei-02]
caps_outcomes: [simplify algebraic fractions, add and subtract algebraic fractions, preserve restrictions]
cognitive_levels: {knowledge: 4, routine_procedures: 8, complex_procedures: 8, problem_solving: 4}
status: authored-not-integrated
source_document: DBE CAPS Mathematics Grades 10-12
---

# Algebraic fractions and restrictions

## Learning objective

**Simplify and operate with algebraic fractions while preserving denominator restrictions.**

## CAPS scope

This lesson uses factorisation to simplify and operate with algebraic fractions. CAPS includes Grade 12 algebraic fractions and denominators involving factorisable forms; the examples establish the transferable rules without moving into unrelated polynomial units.

## Prerequisite knowledge and diagnostic entry

1. Factorise `x²−9`. Expected `(x−3)(x+3)`.
2. State the excluded value for `5/(x+2)`. Expected `x≠−2`.
3. Simplify `6/15`. Expected `2/5`, by cancelling a common factor.
4. Find the LCD of `1/(x−1)` and `1/(x+1)`. Expected `(x−1)(x+1)` with `x≠±1`.

Failures route to Lesson 2 difference-of-squares/HCF or Lesson 1 fraction/restriction repair before continuing.

## Conceptual teaching explanation

An algebraic fraction is a quotient. Its domain is determined **before** simplification: every value that makes an original denominator zero is excluded. Simplification may remove the written factor, but it cannot change the domain of the original expression.

### Factors may cancel; terms may not cancel

Cancellation is division by the same non-zero factor in numerator and denominator:

`[(x−3)(x+3)]/(x−3)=x+3`, provided `x≠3`.

The pieces of `x+3` are terms joined by addition; neither is a factor of the whole sum. Therefore an `x` in `(x+3)/x` cannot be crossed out. Factor first, then identify an identical factor, then cancel while retaining its non-zero condition.

### Operations

- **Add/subtract:** preserve restrictions, factor denominators, select the LCD, create equivalent numerators, then combine.
- **Multiply:** factor first and cancel only common non-zero factors across the product.
- **Divide:** multiply by the reciprocal of the divisor, adding the condition that the divisor itself is non-zero, then factor and simplify.
- **Complex fractions:** simplify the small fractions or multiply the entire numerator and denominator by a common LCD; never multiply only selected terms.
- **Verify:** compare original and simplified values at two permitted inputs and compare domains. Numerical checks support, but do not replace, algebraic proof.

## Vocabulary and notation

`numerator`, `denominator`, `restriction/excluded value`, `domain`, `common factor`, `term`, `lowest common denominator (LCD)`, `reciprocal`, `equivalent expression`, `complex fraction`, `permitted value`.

## Teacher-style narration

“Before touching the fraction, protect its domain. Mark every denominator zero. Then expose products by factorising. A cancellation line means division by the same non-zero factor; it can pass through a product, never through addition or subtraction. The restriction stays in the final answer because it belongs to the original question.”

## Primary worked examples and whiteboard teaching specifications

### Example 1 — simplify and retain the hole

Simplify `(x²−9)/(x−3)`.

1. Original denominator: `x−3≠0`, so `x≠3`.
2. Factor numerator: `x²−9=(x−3)(x+3)`.
3. Identical non-zero factor `(x−3)` is now visible above and below.
4. Cancel the factor: result `x+3`, **with `x≠3`**.
5. Verify at `x=5`: original `16/2=8`; simplified `8`. At `x=3`, the original remains undefined.

```yaml
instructional_goal: cancel an identical factor without losing the original restriction
events:
  - {type: focus, targets: [original-denominator]}
  - {type: mark_restriction, expression: "x-3 != 0", result: "x != 3"}
  - {type: factor, target: numerator, result: "(x-3)(x+3)"}
  - {type: dim, targets: [factor-x-plus-3]}
  - {type: compare, targets: [numerator-factor-x-minus-3, denominator-factor-x-minus-3], relation: identical-nonzero-factor}
  - {type: cancel_factor, targets: [numerator-factor-x-minus-3, denominator-factor-x-minus-3], precondition: "x != 3"}
  - {type: reveal, target: simplified, value: "x+3; x != 3"}
  - {type: verify, permitted_value: 5, excluded_value: 3}
accessibility_text: "The common factor x minus three cancels only after x not equal to three is recorded."
```

### Example 2 — subtraction with an LCD

Simplify `2/(x−1)−3/(x+1)`.

Restrictions: `x≠1,−1`. LCD `(x−1)(x+1)`.

`[2(x+1)−3(x−1)]/[(x−1)(x+1)] = [2x+2−3x+3]/(x²−1) = (5−x)/(x²−1)`, with `x≠±1`.

```yaml
instructional_goal: create equivalent fractions before subtracting numerators
events:
  - {type: mark_restriction, values: ["x != 1", "x != -1"]}
  - {type: factor, targets: [denominator-1, denominator-2], role: lcd-analysis}
  - {type: reveal, target: lcd, value: "(x-1)(x+1)"}
  - {type: apply_both_sides, semantic_role: equivalent-fraction-scaling, multipliers: ["x+1", "x-1"]}
  - {type: write, target: combined-numerator, value: "2(x+1)-3(x-1)"}
  - {type: checkpoint, prompt: "Which signs are affected by subtracting the second numerator?"}
  - {type: expand, target: combined-numerator}
  - {type: reveal, target: final, value: "(5-x)/(x^2-1), x != ±1"}
  - {type: verify, permitted_value: 0}
```

### Example 3 — divide algebraic fractions

Simplify `[(x²−4)/(x²−x−2)] ÷ [(x+2)/(x−1)]`.

Original restrictions: first denominator `(x−2)(x+1)` gives `x≠2,−1`; divisor denominator gives `x≠1`; divisor must also be non-zero, so its numerator `x+2≠0`, giving `x≠−2`. Factor and reciprocate:

`[(x−2)(x+2)]/[(x−2)(x+1)] · (x−1)/(x+2) = (x−1)/(x+1)`,
with `x≠−2,−1,1,2`.

```yaml
instructional_goal: include denominator and zero-divisor restrictions before reciprocal multiplication
events:
  - {type: mark_restriction, values: ["x != 2", "x != -1", "x != 1", "x != -2"]}
  - {type: factor, targets: [all-factorisable-polynomials]}
  - {type: reveal, target: reciprocal-operation, value: "multiply by (x-1)/(x+2)"}
  - {type: compare, targets: [matching-x-minus-2, matching-x-plus-2], relation: common-factors}
  - {type: cancel_factor, targets: [matching-x-minus-2, matching-x-plus-2], precondition: restrictions-recorded}
  - {type: reveal, target: final, value: "(x-1)/(x+1) with x != -2,-1,1,2"}
  - {type: verify, permitted_value: 0, compare_domains: true}
```

## Learner checkpoints

- “Which values make an **original** denominator zero?”
- “Are the marked objects factors of a product, or terms in a sum?”
- “What multiplier creates the LCD for this fraction?”
- “When dividing, which extra values make the divisor zero?”

## Common misconceptions and repair

| Misconception | Repair |
|---|---|
| cancels the `x` in `(x+4)/x` | use boxes around terms and circles around factors; substitution at `x=2` disproves the false result |
| finds restrictions after cancellation | mark restrictions as the first semantic event |
| adds denominators | use numerical fractions to re-establish equivalent-unit reasoning |
| forgets to distribute a subtraction | retain brackets around the second numerator until expansion |
| reciprocates only one factor or forgets zero divisor | treat the whole divisor as one object and mark numerator-zero exclusions |
| reports simplified formula without domain | final state must display formula and inherited restrictions together |

## Misconception-repair example

A learner “simplifies” `(x+6)/x` to `6`. Test `x=2`: original `8/2=4`, proposed result `6`; therefore they are not equivalent. The `x` is a term in the numerator sum, not a factor of the whole numerator. No cancellation is legal. By contrast, `x(x+6)/x=x+6` for `x≠0`, because the numerator visibly has an `x` factor.

## Self-guided practice bank

All 24 items are Athena-original from the CAPS skill scope. Each solution is separate from the teaching whiteboard and must be gated behind an attempt/support flow.

### Diagnostic (4)

1. **g12-aei-l03-d01 | foundation | K | 1.** State restrictions for `7/[x(x−4)]`. **Answer:** `x≠0,4`. Hints: set each denominator factor non-zero; solve. Solution: `x≠0` and `x−4≠0`. Why: division by zero is undefined. Verify both excluded inputs zero the denominator.
2. **g12-aei-l03-d02 | foundation | K | 1.** Factorise `x²−16`. **Answer:** `(x−4)(x+4)`. Hints: two squares; conjugate factors. Why: difference-of-squares identity. Verify expansion.
3. **g12-aei-l03-d03 | foundation | K | 2.** Simplify `12x/18`, state restrictions if any. **Answer:** `2x/3`; none from denominator. Hints: HCF 6; 18 is never zero. Solution: divide numerator and denominator by 6. Why: common numerical factors may cancel. Verify values.
4. **g12-aei-l03-d04 | easy | R | 2.** Find LCD of `1/[x(x+1)]` and `1/[x²−1]`. **Answer:** `x(x−1)(x+1)`, restrictions `x≠0,±1`. Hints: factor `x²−1`; include each distinct factor at highest power. Why: the LCD must be divisible by both denominators. Verify division yields factors.

### Guided (6)

5. **g12-aei-l03-g01 | easy | R | 2.** Simplify `(x²−25)/(x−5)`. **Answer:** `x+5, x≠5`. Hints: restriction first; factor numerator. Solution: `(x−5)(x+5)/(x−5)`. Why: identical non-zero factors cancel. Verify at `x=7` and domain at 5.
6. **g12-aei-l03-g02 | easy | R | 2.** Simplify `6x²y/(9xy²)`. **Answer:** `2x/(3y)`, restrictions `x≠0,y≠0`. Hints: original denominator factors; reduce coefficients and powers. Why: cancellation is division by shared factors. Verify at `(3,2)`.
7. **g12-aei-l03-g03 | standard | R | 3.** Add `2/x+3/(2x)`. **Answer:** `7/(2x), x≠0`. Hints: LCD `2x`; scale first numerator by 2. Solution: `4/(2x)+3/(2x)=7/(2x)`. Why: equal denominators represent equal-sized parts. Verify `x=1`.
8. **g12-aei-l03-g04 | standard | R | 3.** Subtract `1/(x−2)−1/(x+2)`. **Answer:** `4/(x²−4), x≠±2`. Hints: LCD conjugate product; preserve numerator brackets. Solution: `[(x+2)−(x−2)]/[(x−2)(x+2)]=4/(x²−4)`. Why: subtraction affects the entire second numerator. Verify at `x=3`.
9. **g12-aei-l03-g05 | standard | R | 3.** Multiply `(x²−9)/(x²+x−6) · (x+3)/x`. **Answer:** `(x−3)(x+3)/[x(x−2)]`, restrictions `x≠−3,0,2`. Hints: factor both polynomials; cancel identical factors only. Solution: `[(x−3)(x+3)]/[(x+3)(x−2)]·(x+3)/x = (x−3)(x+3)/[x(x−2)]`. Why: one matching `x+3` factor cancels; the remaining factors are not identical. Verification at `x=3` gives zero in both forms, and at `x=1` both give `8`.
10. **g12-aei-l03-g06 | standard | C | 3.** Divide `(x²−1)/(x²+2x+1) ÷ (x−1)/(x+1)`. **Answer:** `1`, restrictions `x≠−1,1`. Hints: factor; divisor zero adds `x≠1`; multiply reciprocal. Solution: `[(x−1)(x+1)/(x+1)²]·[(x+1)/(x−1)]=1`. Why: all cancellation factors are non-zero on the recorded domain. Verify at `x=2`.

### Independent and mixed (10)

11. **g12-aei-l03-i01 | standard | R | 2.** Simplify `(3x²−12x)/(6x)`. **Answer:** `(x−4)/2`, `x≠0`. Hints: factor numerator `3x(x−4)`; cancel factors. Why: an entire `x` factor is shared. Verify at `x=2`.
12. **g12-aei-l03-i02 | standard | C | 3.** Simplify `(x²+x−6)/(x²−4)`. **Answer:** `(x+3)/(x+2)`, `x≠±2`. Hints: factor numerator and denominator; match `x−2`. Why: restriction `x≠2` remains after cancellation. Verify at `x=3`.
13. **g12-aei-l03-i03 | standard | C | 4.** Add `3/(x+1)+2/(x−1)`. **Answer:** `(5x−1)/(x²−1)`, `x≠±1`. Hints: mark restrictions; LCD `(x+1)(x−1)`. Solution: `[3(x−1)+2(x+1)]/(x²−1)=(5x−1)/(x²−1)`. Why: each numerator is scaled by its missing factor. Verify at `x=2`.
14. **g12-aei-l03-i04 | standard | C | 4.** Simplify `x/(x−3)−3/(3−x)`. **Answer:** `(x+3)/(x−3)`, `x≠3`. Hints: `3−x=−(x−3)`; rewrite second fraction. Solution: `x/(x−3)+3/(x−3)`. Why: opposite factors differ by `−1`. Verify at `x=4`.
15. **g12-aei-l03-i05 | intermediate | C | 4.** Multiply `(a²−b²)/(a²+2ab+b²) · (a+b)/(a−b)`. **Answer:** `1`, restrictions `a≠−b,a≠b`. Hints: factor both special forms; record all denominator and reciprocal-relevant factors. Solution: `[(a−b)(a+b)/(a+b)²]·[(a+b)/(a−b)]=1`. Why: cancellation is legal only on the excluded-value domain. Verify at `(a,b)=(3,1)`.
16. **g12-aei-l03-i06 | intermediate | C | 4.** Divide `2x/(x²−9) ÷ 4x²/(x+3)`. **Answer:** `1/[2x(x−3)]`, restrictions `x≠−3,0,3`. Hints: denominator restrictions first; divisor numerator adds `x≠0`; reciprocal and factor. Solution: `2x/[(x−3)(x+3)]·(x+3)/(4x²)`. Why: division requires a non-zero divisor. Verify at `x=1`.
17. **g12-aei-l03-i07 | intermediate | C | 4.** Simplify complex fraction `(1/x+1/y)/(1/x−1/y)`. **Answer:** `(x+y)/(y−x)`, restrictions `x≠0,y≠0,x≠y`. Hints: multiply full numerator and denominator by `xy`; denominator of whole fraction may not be zero. Solution: top `x+y`, bottom `y−x`. Why: scaling the whole numerator and denominator by the same non-zero LCD preserves the quotient. Verify at `(2,3)`.
18. **g12-aei-l03-i08 | intermediate | C | 4.** Simplify `1/(x−2)+x/(x²−4)`. **Answer:** `(2x+2)/(x²−4)=2(x+1)/(x²−4)`, `x≠±2`. Hints: factor second denominator; scale first numerator by `x+2`. Solution: `(x+2+x)/(x²−4)`. Why: LCD keeps both original restrictions. Verify at `x=0`.
19. **g12-aei-l03-i09 | intermediate | P | 5.** Determine `k` if `1/(x−1)+k/(x+1)=[(4x−2)/(x²−1)]` for all permitted `x`. **Answer:** `k=3`. Hints: combine left numerators; compare coefficients. Solution: numerator `(x+1)+k(x−1)=(1+k)x+(1−k)`; match `4x−2`, giving `k=3`. Why: equivalent rational expressions agree coefficient-wise on their domain. Verify.
20. **g12-aei-l03-i10 | intermediate | P | 5.** A rectangle has area `(x²−9)/(x−3)` square units for `x>3`. Simplify its area and explain domain. **Answer:** `x+3`, with contextual `x>3` (and algebraic exclusion 3 already outside). Hints: factor; retain source restriction and context. Why: cancellation changes form, not allowed inputs. Verify at `x=5`.

### Misconception/error analysis (2)

21. **g12-aei-l03-m01 | standard | K | 2.** Learner cancels the `x` in `(x+5)/x` to get 5. Diagnose. **Answer:** `x` is a term, not a factor of the whole numerator; no simplification, `x≠0`. Hints: factor numerator if possible; test `x=1`. Why: cancellation is common division of factors only. Verification at `x=1`: original 6, proposed 5.
22. **g12-aei-l03-m02 | standard | R | 3.** Learner simplifies `(x²−4)/(x−2)` to `x+2` and says all real `x`. Diagnose. **Answer:** form is correct but domain must retain `x≠2`. Hints: inspect original denominator; test whether original exists at 2. Why: simplification cannot fill a hole in the original domain. Verify domain comparison.

### Original exam-style (2)

23. **g12-aei-l03-e01 | advanced | P | 6.** Simplify `[(x²−4)/(x²−x−2)]−[2/(x+1)]`, state restrictions. **Answer:** `x/(x+1)`, `x≠−1,2`. Hints: factor first denominator `(x−2)(x+1)`; simplify first fraction only after restrictions; use common denominator. Solution: first fraction `(x+2)/(x+1)`; subtract `2/(x+1)` gives `x/(x+1)`. Why: inherited `x≠2` remains though its factor cancelled. Verify at `x=0` and compare domains.
24. **g12-aei-l03-e02 | advanced | P | 6.** Simplify `[(1/x)−(1/(x+1))] / [1/(x(x+1))]`, state restrictions. **Answer:** `1`, `x≠0,−1`. Hints: simplify numerator with LCD; treat entire denominator as divisor. Solution: numerator `[(x+1)−x]/[x(x+1)]=1/[x(x+1)]`; quotient equals 1 on its domain. Why: identical non-zero fractions divide to one. Verify at `x=1`.

## Exit quiz, mastery and remediation

Use G1, G4, G6, I2, I3, I7, M1 and E1. Mastery: 80–100%; 60–79% targeted practice; below 60% return to the matching teaching segment. `cancel-terms` and `missing-restriction` are serious misconceptions and block mastery until correction items are answered successfully. Academic marks are not reduced for hints; support use is tracked separately.

## Content QA checklist

- [x] 24 unique items: 4 diagnostic, 6 guided, 10 independent/mixed, 2 misconception, 2 exam-style.
- [x] Cognitive allocation K4/R8/C8/P4.
- [x] Restrictions precede all cancellation and persist in final states.
- [x] Only identical non-zero factors cancel; no term cancellation is endorsed.
- [x] Addition, subtraction, multiplication, division and a complex fraction are covered.
- [x] Every solution includes algebraic and/or permitted-value verification plus domain comparison.
- [x] Whiteboard events are semantic data, not executable code.
- [x] Practice presentation remains separate from whiteboard teaching.
