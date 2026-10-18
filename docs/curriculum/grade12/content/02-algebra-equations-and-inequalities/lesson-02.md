---
id: g12-aei-02
grade: 12
subject: mathematics
topic: algebra-equations-and-inequalities
lesson_number: 2
title: Factorisation toolkit
paper: 1
term: pending_authority_review
duration_minutes: 90
mastery_threshold: 80
prerequisites: [g12-aei-01]
caps_outcomes: [factorise algebraic expressions, manipulate algebraic expressions]
cognitive_levels: {knowledge: 4, routine_procedures: 9, complex_procedures: 7, problem_solving: 4}
status: authored-not-integrated
source_document: DBE CAPS Mathematics Grades 10-12
---

# Factorisation toolkit

## Learning objective

**Select and correctly apply an appropriate factorisation method.**

## CAPS scope

This lesson consolidates the school-level toolkit needed before equations and algebraic fractions: highest common factor (HCF), difference of two squares, trinomials, grouping and expressions containing powers. CAPS also includes later cubic-polynomial work; that is not imported into these introductory three lessons. “Does not factorise” here means no factorisation over the reals by the expected methods in this lesson.

## Prerequisite knowledge and diagnostic entry

- D1 finds an HCF; D2 recognises two square terms with subtraction; D3 expands two binomials; D4 identifies the structure of a trinomial.
- Failure on expansion routes to Lesson 1 R4 because expansion is the verification method for every factorisation.

## Conceptual teaching explanation

Factorisation rewrites a sum or difference as a product. It is the reverse of expansion. The decision comes before the mechanics:

1. **Always inspect for an HCF first.** Removing it simplifies everything that follows.
2. **Count terms and inspect signs.** Two square terms separated by subtraction suggest `A²−B²=(A−B)(A+B)`. A sum of squares does not use this identity over the reals.
3. **For `x²+bx+c`,** choose two numbers whose product is `c` and sum is `b`.
4. **For `ax²+bx+c`,** split the middle term using numbers with product `ac` and sum `b`, then group.
5. **For four terms,** test grouping in pairs and look for a common binomial.
6. **Treat repeated powers structurally.** For example, `x⁴−5x²+4` is a trinomial in `x²`.
7. **Verify by expansion.** Correct factors must reproduce every term and sign of the original.

## Vocabulary and notation

`factor`, `product`, `HCF`, `difference of squares`, `trinomial`, `grouping`, `common binomial factor`, `irreducible over the reals`, `identity`, `verification by expansion`.

## Teacher-style narration

“Do not begin by guessing brackets. First read the expression’s structure. Ask: is there a common factor; how many terms are there; are any perfect squares; can one repeated power act as a temporary variable? Your method choice is part of the mathematics.”

## Primary worked examples and whiteboard teaching specifications

### Example 1 — HCF before anything else

Factorise `12x³−18x²`.

The numerical HCF is 6 and the lowest shared power is `x²`, so `12x³−18x²=6x²(2x−3)`. Expand to verify: `6x²·2x−6x²·3=12x³−18x²`.

```yaml
instructional_goal: identify and extract the complete HCF
events:
  - {type: focus, targets: [coefficient-12, coefficient-18]}
  - {type: compare, targets: [x-cubed, x-squared], relation: lowest-common-power}
  - {type: reveal, target: hcf, value: "6x^2"}
  - {type: factor, source: original-expression, factor: "6x^2", result: "6x^2(2x-3)"}
  - {type: checkpoint, prompt: "How can expansion check both signs?"}
  - {type: expand, target: proposed-factors}
  - {type: verify, expected: "12x^3-18x^2"}
accessibility_text: "Six x squared is common to both terms and is extracted."
```

### Example 2 — method selection for a trinomial

Factorise `2x²−7x+3`.

`ac=6`. Numbers with product `6` and sum `−7` are `−6` and `−1`. Split and group:
`2x²−6x−x+3 = 2x(x−3)−1(x−3) = (2x−1)(x−3)`.
Expansion gives `2x²−6x−x+3=2x²−7x+3`.

```yaml
instructional_goal: choose split-middle-term factorisation from structure
events:
  - {type: focus, targets: [leading-coefficient, middle-coefficient, constant]}
  - {type: write, target: ac-product, value: "2*3=6"}
  - {type: checkpoint, prompt: "Which pair multiplies to 6 and adds to -7?"}
  - {type: reveal, target: split-pair, value: "-6 and -1"}
  - {type: write, target: split-trinomial, value: "2x^2-6x-x+3"}
  - {type: group, targets: [first-pair, second-pair]}
  - {type: factor, target: common-binomial, value: "(2x-1)(x-3)"}
  - {type: verify, method: expand}
```

### Example 3 — expression in powers

Factorise fully `x⁴−5x²+4`.

Let the structure `u=x²` guide method choice: `u²−5u+4=(u−1)(u−4)`. Restore `x²`: `(x²−1)(x²−4)`, then factor both differences of squares: `(x−1)(x+1)(x−2)(x+2)`. Verification may expand in stages.

```yaml
instructional_goal: recognise a trinomial in x-squared and continue to full factorisation
events:
  - {type: group, targets: [x-fourth, x-squared], label: "powers of x^2"}
  - {type: substitute, target: repeated-power, value: "u=x^2"}
  - {type: factor, target: u-trinomial, value: "(u-1)(u-4)"}
  - {type: substitute, target: u, value: "x^2"}
  - {type: checkpoint, prompt: "Is either factor still factorisable?"}
  - {type: factor, targets: [difference-square-1, difference-square-2]}
  - {type: verify, method: staged-expansion}
```

## Learner checkpoints

- “What is common to every term?”
- “Is this subtraction between two perfect squares, or a sum?”
- “Which pair has the required product **and** sum?”
- “After one factorisation, can any factor be factorised further?”

## Common misconceptions and repairs

| Misconception | Repair |
|---|---|
| skips HCF | run HCF scan before selecting another method |
| writes `A²+B²=(A+B)(A−B)` | expand the right side and observe it produces `A²−B²` |
| checks product but not sum for a trinomial | use a two-column product/sum decision table |
| loses a minus when grouping | factor `−1` explicitly from the second group |
| stops at `(x²−1)(x²−4)` | apply the “factor fully?” checkpoint to every resulting factor |
| assumes every expression factorises | verify discriminant/structure at the appropriate later stage; recognise school-level irreducibility here |

## Self-guided practice bank

All questions are Athena-original and based on the CAPS skill specification. Worked solutions remain hidden until an attempt. Each has 2–3 progressive hints, a non-repeating Why, misconception tags and expansion verification.

### Diagnostic (4)

1. **g12-aei-l02-d01 | foundation | K | 1.** Find the HCF of `18x³y` and `24x²y²`. **Answer:** `6x²y`. Hints: gcd of coefficients; minimum exponent per variable. Solution: `gcd(18,24)=6`, `min(x³,x²)=x²`, `min(y,y²)=y`. Why: an HCF divides every term exactly. Verify both quotients are monomials.
2. **g12-aei-l02-d02 | foundation | K | 1.** Select the method for `49−t²`. **Answer:** difference of squares. Hints: count terms; identify `7²` and `t²`. Solution: `7²−t²=(7−t)(7+t)`. Why: conjugate factors cancel middle terms. Verify by expansion.
3. **g12-aei-l02-d03 | foundation | K | 2.** Expand `(x−4)(x+3)`. **Answer:** `x²−x−12`. Hints: distribute each first-bracket term; collect middle terms. Solution: `x²+3x−4x−12=x²−x−12`. Why: this is the inverse check for factorisation.
4. **g12-aei-l02-d04 | easy | R | 2.** State the number pair for `x²+7x+12`. **Answer:** `3 and 4`. Hints: product 12; sum 7. Solution: `3·4=12`, `3+4=7`; factors `(x+3)(x+4)`. Why: expansion creates the middle coefficient from the pair’s sum.

### Guided (6)

5. **g12-aei-l02-g01 | easy | R | 2.** Factorise `15a²−20a`. **Answer:** `5a(3a−4)`. Hints: HCF 5; lowest `a` power. Solution: extract `5a`. Why: both terms contain that entire factor. Verify expansion.
6. **g12-aei-l02-g02 | easy | R | 2.** Factorise `9m²−25`. **Answer:** `(3m−5)(3m+5)`. Hints: two terms and subtraction; square roots. Solution: `(3m)²−5²`. Why: `(A−B)(A+B)=A²−B²`. Verify.
7. **g12-aei-l02-g03 | easy | R | 2.** Factorise `x²−x−20`. **Answer:** `(x−5)(x+4)`. Hints: product −20; sum −1. Solution: pair `−5,4`. Why: signs must satisfy both tests. Verify.
8. **g12-aei-l02-g04 | standard | R | 3.** Factorise `3x²+11x+6`. **Answer:** `(3x+2)(x+3)`. Hints: `ac=18`; split 11 as 9+2. Solution: `3x²+9x+2x+6=3x(x+3)+2(x+3)`. Why: grouping exposes a common binomial. Verify.
9. **g12-aei-l02-g05 | standard | R | 3.** Factorise `ax+ay+bx+by`. **Answer:** `(a+b)(x+y)`. Hints: group first two and last two; extract common bracket. Solution: `a(x+y)+b(x+y)`. Why: the identical binomial is a factor. Verify.
10. **g12-aei-l02-g06 | standard | R | 3.** Factorise fully `4p³−36p`. **Answer:** `4p(p−3)(p+3)`. Hints: HCF first; remaining difference of squares. Solution: `4p(p²−9)=4p(p−3)(p+3)`. Why: factorisation continues until no supported factor remains. Verify.

### Independent and mixed (10)

11. **g12-aei-l02-i01 | standard | R | 2.** Factorise `6x²+9x`. **Answer:** `3x(2x+3)`. Hints: coefficient HCF; common variable. Solution and why: extract complete HCF `3x`; expansion verifies.
12. **g12-aei-l02-i02 | standard | C | 3.** Factorise `16y⁴−81`. **Answer:** `(2y−3)(2y+3)(4y²+9)`. Hints: first use squares `(4y²)²−9²`; one factor is another difference of squares. Solution: `(4y²−9)(4y²+9)=(2y−3)(2y+3)(4y²+9)`. Why: `4y²+9` is a sum of squares and stops over reals. Verify in stages.
13. **g12-aei-l02-i03 | standard | C | 3.** Factorise `2x²+x−6`. **Answer:** `(2x−3)(x+2)`. Hints: `ac=−12`; pair 4 and −3. Solution: `2x²+4x−3x−6=2x(x+2)−3(x+2)`. Why: split terms enable grouping. Verify.
14. **g12-aei-l02-i04 | standard | C | 3.** Factorise `5ab−10a+3b−6`. **Answer:** `(5a+3)(b−2)`. Hints: group in pairs; seek the same bracket. Solution: `5a(b−2)+3(b−2)`. Why: distributivity works in reverse. Verify.
15. **g12-aei-l02-i05 | intermediate | C | 4.** Factorise fully `2x³−8x²−10x+40`. **Answer:** `2(x−4)(x−√5)(x+√5)` over reals, or `2(x−4)(x²−5)` at school-level mixed form. Hints: HCF 2; group; inspect difference of squares over reals. Solution: `2[x²(x−4)−5(x−4)]=2(x−4)(x²−5)`. Why: grouping reveals the common binomial; `x²−5` has real surd factors if full real-linear factorisation is requested. Verify expansion. Accepted forms specify requested convention.
16. **g12-aei-l02-i06 | intermediate | C | 3.** Factorise `a²−6ab+9b²`. **Answer:** `(a−3b)²`. Hints: first/last are squares; middle is `−2AB`. Solution: perfect-square trinomial. Why: expansion gives two equal cross terms. Verify.
17. **g12-aei-l02-i07 | intermediate | C | 4.** Factorise fully `x⁴−13x²+36`. **Answer:** `(x−2)(x+2)(x−3)(x+3)`. Hints: treat `x²` as one object; pair product 36 sum −13. Solution: `(x²−4)(x²−9)`, then differences of squares. Why: repeated powers create trinomial structure. Verify staged expansion.
18. **g12-aei-l02-i08 | intermediate | C | 3.** Decide whether `x²+4x+8` factorises into real linear factors by these methods. **Answer:** no. Hints: pair product 8 sum 4; complete structural check/discriminant later gives `16−32<0`. Solution: no real pair and negative discriminant. Why: not every trinomial has real linear factors. Verify any guessed integer pair fails sum/product.
19. **g12-aei-l02-i09 | intermediate | P | 4.** The area `6x²−x−2` must be written as two binomial side lengths. **Answer:** `(3x−2)(2x+1)`. Hints: `ac=−12`; pair 3 and −4. Solution: `6x²+3x−4x−2=3x(2x+1)−2(2x+1)`. Why: factorisation recovers multiplicative dimensions. Verify expansion.
20. **g12-aei-l02-i10 | intermediate | P | 4.** Find integer `k` so `x²+kx+24=(x+6)(x+4)`. **Answer:** `k=10`. Hints: expand only the middle terms; add factor constants. Solution: expansion `x²+10x+24`. Why: the middle coefficient is the sum of constants. Verify identity.

### Misconception/error analysis (2)

21. **g12-aei-l02-m01 | standard | K | 2.** A learner writes `x²+16=(x−4)(x+4)`. Diagnose. **Answer:** RHS is `x²−16`; a sum of squares is not this identity. Hints: expand; compare the constant sign. Why: conjugates create a difference, not a sum. Verification expansion.
22. **g12-aei-l02-m02 | standard | R | 3.** A learner stops at `3x(x−2)+5(x−2)`. Complete and explain. **Answer:** `(3x+5)(x−2)`. Hints: identify repeated factor; reverse distribution. Why: the whole binomial is common. Verify expansion to `3x²−x−10`.

### Original exam-style (2)

23. **g12-aei-l02-e01 | advanced | P | 5.** Factorise fully `3x⁴−27x²`. **Answer:** `3x²(x−3)(x+3)`. Hints: HCF first; inspect remaining binomial. Solution: `3x²(x²−9)=3x²(x−3)(x+3)`. Why: skipping HCF hides the next method. Verify expansion.
24. **g12-aei-l02-e02 | advanced | P | 5.** Given `2x²+px−15=(2x+5)(x−3)`, determine `p` without solving an equation in `x`. **Answer:** `p=−1`. Hints: expand RHS; compare corresponding coefficients. Solution: RHS `2x²−6x+5x−15=2x²−x−15`; hence `p=−1`. Why: polynomial identities have equal coefficients for every `x`. Verify at two values and by coefficient comparison.

## Detailed misconception-repair example

Claim: `x²+9=(x+3)(x−3)`. Expand the proposed factors: `x²−9`. The sign mismatch disproves the claim. The repair is not another guessed pair; it is recognising that the real difference-of-squares identity requires subtraction. The expression `x²+9` is irreducible over the reals using this toolkit.

## Exit quiz, mastery and remediation

Use G1, G2, G4, I2, I3, I7, M1 and E2. Scores 80–100% master the lesson; 60–79% receive items tagged to the missed method; below 60% returns to the decision tree and primary examples. Failure to distinguish a sum from a difference of squares or inability to verify by expansion blocks mastery until corrected.

## Content QA checklist

- [x] 24 unique items: 4/6/10/2/2 category distribution.
- [x] Cognitive allocation K4/R9/C7/P4.
- [x] All required methods and method selection included.
- [x] Every proposed factorisation includes expansion verification.
- [x] “Does not factorise” is domain/method qualified.
- [x] Whiteboard performs one legal semantic change per event.
- [x] No application or runtime whiteboard code is required.
