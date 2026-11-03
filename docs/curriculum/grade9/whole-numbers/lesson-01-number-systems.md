# Grade 9 · Topic 1 Whole Numbers · Lesson 1: The real number system

**Status:** authored source pack for review; no runtime lesson is registered. **Stable lesson ID:** `g9-whole-numbers-01`. **ATP source:** [DBE 2026 Grade 9 Mathematics ATP, Term 1, Whole Numbers](https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2026%20ATPs/2026_ATP_Mathematics_Grade%209.pdf). The ATP requires recognition and distinction of natural, whole, integer, rational and irrational numbers. Athena's examples below are original; this is not an official DBE question paper.

## Teaching contract

**Objective:** Classify a value in its *smallest named set*, name all larger sets to which it belongs, and justify the classification from an exact representation. Assume natural numbers begin at 1: N = {1, 2, 3, ...}; W = {0, 1, 2, ...}; Z includes negative integers; Q contains ratios a/b of integers with b ≠ 0; irrational numbers are real numbers outside Q. The real numbers R comprise Q and the irrational numbers I. Show the convention for N on screen. **Prerequisites:** Grade 8 integers, fractions, decimal representations, squares and roots. **Time:** approximately 55–70 minutes plus independent practice.

**Why it matters:** A value that *looks* like a radical or fraction may simplify to a different set. Classifying from appearance alone causes later algebra and graph errors. An undefined expression is not a number and cannot be forced into a set.

**Common whiteboard shell:** Prompt at top, set diagram and exact-value work on the left, persistent written solution on the right. Initial view shows only the problem and the relevant empty set regions. Reveal the expression simplification first when needed; animate a token moving into its smallest set; then illuminate each containing region; conclude with a verification statement tied to the original expression. The written lines accumulate and never disappear. Stable semantic IDs: `given`, `simplification`, `smallest-set`, `containing-sets`, `reason`, `check`. For an undefined or nonreal expression, highlight the blocked operation outside the real-number diagram. Do not place a final answer or a lit region in the initial state. The stage-specific instructions in the table are required content, not a replacement for typed event data at implementation.

## Worked whiteboard bank — 15 distinct questions

Each row gives the complete mathematical result and the order of operations. A full runtime timeline must make each semicolon-separated action a separate visible state, with its own caption and retained written line. `N ⊂ W ⊂ Z ⊂ Q ⊂ R`; `I ⊂ R` and `I ∩ Q = ∅`. A value may have several memberships but only one smallest set in this model.

| ID / difficulty | Original question | Required animated actions and cumulative memo | Final check / first error to diagnose |
|---|---|---|---|
| W01 foundation | Classify 6 in its smallest set and list every larger set. | Point to 6 as a positive counting number; place the 6 token in N; illuminate W, Z, Q and R outward. Written: `6 ∈ N; therefore 6 ∈ W, Z, Q, R`. | Check `6 = 6/1`. Error: calling Q its *smallest* set. |
| W02 easy | Is 0 natural or whole under the displayed convention? List its memberships. | Display N beginning at 1; show 0 at the origin; place 0 in W but outside N; illuminate Z, Q, R. Written: `0 ∈ W, Z, Q, R; 0 ∉ N`. | Check `0 = 0/1`. Error: silently changing the N convention. |
| W03 easy | Classify −7 in its smallest set. | Place −7 left of zero; note it is an integer, not whole; move token into Z; illuminate Q and R. Written: `−7 ∈ Z, Q, R; −7 ∉ W`. | Check `−7 = −7/1`. Error: assuming a negative number cannot be rational. |
| W04 standard | Classify 3/4 and justify whether it is an integer. | Draw four equal parts with three filled; write numerator and nonzero denominator; place in Q outside Z; illuminate R. Written: `3/4 ∈ Q, R; 3/4 ∉ Z`. | Check `0 < 3/4 < 1`. Error: calling every fraction an integer. |
| W05 standard | Classify −2.5 using a fraction. | Mark −2.5 on a line; rewrite `−2.5 = −25/10 = −5/2`; place in Q; illuminate R. | Check `−5 ÷ 2 = −2.5`. Error: treating negative decimals as irrational. |
| W06 standard | Classify 0.333… where the 3 repeats forever. | Highlight repeating digit; write `x = 0.333…`, `10x = 3.333…`, subtract to get `9x = 3`, hence `x = 1/3`; move into Q; illuminate R. | Check `1/3 = 0.333…`. Error: equating nonterminating with irrational. |
| W07 standard | Classify √49 after evaluating it. | Highlight radical; pair `7 × 7 = 49`; replace `√49` with `7` as the principal root; place in N, illuminate W, Z, Q, R. | Check `7² = 49` and `√49 ≥ 0`. Error: classifying by the radical sign or using ±7 as √49. |
| W08 intermediate | Classify √2, distinguishing it from √4. | Show √4 = 2 as a contrast, then locate √2 between 1 and 2; state its decimal does not terminate or repeat; place √2 in I, illuminate R only. | Check `1² < 2 < 2²`; do not claim a finite decimal is exact. Error: all radicals are irrational. |
| W09 intermediate | Classify −√81. | Find principal √81 = 9; apply the outside negative sign to obtain −9; place in Z, illuminate Q and R. | Check `−√81 = −9`, not +9; `9² = 81`. Error: dropping the outside minus. |
| W10 intermediate | Classify π and decide whether 22/7 is the same number. | Put π in I; draw an approximation arrow from 22/7 to π without an equality sign; show 22/7 is in Q; illuminate R for both. | Check `22/7 ≈ π` but is not equal. Error: an approximation inherits the exact number's set. |
| W11 exam | Classify −√16/2, reading the numerator as `−√16`. | Evaluate √16 = 4; retain outside minus: `−4/2`; divide to get −2; place in Z; illuminate Q and R. | Substitute back: `−√16/2 = −4/2 = −2`. Error: applying minus to denominator or classifying before simplification. |
| W12 exam | A learner says `2/0` is irrational because it is not rational. Diagnose the first error. | Highlight denominator 0; show division by zero is undefined; block the token outside R; distinguish `not rational` from `irrational real`. | Check no real y satisfies `0 × y = 2`. Error: taking complement of Q in all expressions instead of within R. |
| W13 exam | Classify `0.101001000100001…`, where each successive 1 has one more zero before it. | Mark successive increasing zero runs; note the decimal never terminates and has no repeating fixed block; place in I, illuminate R. | Check the displayed rule continues indefinitely. Error: mistaking visible repeated 1s for a repeating decimal period. |
| W14 advanced | Classify `(√50)/√2` using exact arithmetic. | Confirm denominator is nonzero; combine radicals for positive values: `√(50/2) = √25`; evaluate 5; move token from an unclassified radical expression into N; illuminate W, Z, Q, R. | Check `√50 = 5√2`, so ratio is 5. Error: declaring the original expression irrational because each radical looks irrational. |
| W15 advanced | Classify `√(−9)` in the real-number system and explain why it differs from `−√9`. | Show the negative lies *inside* the radical; no real square is −9, so place outside R; contrast with `−√9 = −3`, which belongs to Z, Q, R. | Check every real square is ≥0. Error: moving the minus outside the radical. |

**Teacher verification note:** W08 and W13 use known irrationality facts; at this level the visual provides a pattern/estimate and the teacher explains that the nonrepeating representation is the justification, not that a few displayed digits prove an infinite claim. W14's quotient uses positive radicals and a nonzero denominator. No complex-number claims are needed in Grade 9.

## Independent practice — 15 book-first, four-option items

Show: “Work it out in your book, then choose one answer.” The letter and full rationale below belong to the **private answer key**; the public question contains only the prompt and four option texts. Labels `N`, `W`, `Z`, `Q`, `I` mean *smallest set* unless the question explicitly asks for all memberships. Every distractor names a likely mistake. Options deliberately mix classifications and judgments so the learner must interpret each prompt.

| ID | Question | A | B | C | D | Key and private reason |
|---|---|---|---|---|---|---|
| P01 | Smallest set for 14? | N | W | Z | Q | **A**. Counting number; B–D are larger containing sets. |
| P02 | Smallest set for 0 under N starting at 1? | N | Z | W | I | **C**. Zero is whole; A changes the convention, B is too broad, D ignores `0/1`. |
| P03 | Smallest set for −12? | W | I | Q | Z | **D**. Negative integer; A excludes negatives, B ignores `−12/1`, C is broader. |
| P04 | Smallest set for 5/8? | Z | Q | I | N | **B**. Ratio of integers; A/D claim integer, C confuses fraction with irrationality. |
| P05 | Smallest set for 1.75? | I | W | Q | Z | **C**. `7/4`; A confuses decimal with irrationality, B/D assume integer. |
| P06 | Smallest set for 0.272727…? | I | Q | W | Z | **B**. Repeated block makes it rational; A confuses nontermination, C/D assume integer. |
| P07 | Smallest set for √64? | N | I | Q | Z | **A**. Principal root 8; B classifies by appearance, C/D are broader. |
| P08 | Smallest set for √3? | Q | N | Z | I | **D**. √3 is irrational; A assumes fraction form, B/C assume exact integer. |
| P09 | Smallest set for −√25? | W | Q | Z | I | **C**. Value −5; A excludes negatives, B broader, D classifies by appearance. |
| P10 | Which statement about π and 3.14 is correct? | Both are irrational | They are exactly equal | π is rational and 3.14 irrational | π is irrational; 3.14 is rational | **D**. Finite 3.14 = 314/100; A/C conflate approximation, B replaces ≈ with =. |
| P11 | Smallest set for `0/6`? | W | Q | I | N | **A**. `0/6 = 0`; B broader, C ignores valid fraction, D starts N at 1. |
| P12 | How is `6/0` classified among real numbers? | Rational | Irrational | Not a real number: undefined | Whole | **C**. No division by zero; A/D falsely assign a value, B treats every non-rational expression as irrational. |
| P13 | Smallest set for `√18/√2`? | I | N | Q | Z | **B**. √9 = 3; A classifies before simplification, C/D broader. |
| P14 | Smallest set for −0.4? | I | Z | W | Q | **D**. `−2/5`; A calls terminating decimal irrational, B/C assume integer. |
| P15 | Which claim is true? | Every irrational is real | Every real is rational | Every integer is natural | No negative integer is rational | **A**. B omits irrationals; C omits negatives; D ignores a/1. |

Option positions are A:4, B:3, C:4, D:4. Before release, a validator must recompute correct answers and reject equivalent option meanings, altered ordering without remapped keys, or missing rationale. Practice variants differ from the worked questions and retain exact arithmetic.

## Mastery and changed-value reassessment (private bank)

Five mastery prompts are unseen relative to the practice bank. Preserve full memos and do not embed answers in the public payload. Four correct of five is the provisional 80% threshold; a selected option alone does not prove that the book working is sound. Record hints used and invite the learner to compare their working to the memo after submission.

| ID | Prompt | Four options A–D | Answer and memo |
|---|---|---|---|
| M01 | Smallest set for `−√36/3`? | N; W; Z; I | **C**. `−√36/3 = −6/3 = −2 ∈ Z`. |
| M02 | Which is irrational? | `√121`; `2/11`; `0.666…`; `√7` | **D**. First is 11, second is a fraction, third repeats. |
| M03 | Which is not a real number? | `−√16`; `√0`; `√(−4)`; `−4/2` | **C**. A real square cannot equal −4. |
| M04 | Which fraction equals a repeating decimal? | `3/8`; `1/3`; `7/20`; `9/10` | **B**. 1/3 = 0.333…; the other fractions terminate. |
| M05 | Which statement is valid? | `Q ⊂ Z`; `I ⊂ Q`; `Z ⊂ Q`; `R ⊂ W` | **C**. Every integer is a ratio `a/1`. |

If misconception tags show `classify-before-simplify`, reteach W07/W11/W14 with changed radicals. If `decimal-period`, reteach W06/W13 with an explicit finite/repeating/nonrepeating comparison. If `undefined-versus-irrational`, reteach W12/W15. Then use the parallel bank:

| ID | Prompt | Four options A–D | Answer and check |
|---|---|---|---|
| R01 | Smallest set for `√75/√3`? | I; Q; N; Z | **C**. `√25 = 5`; positive counting number. |
| R02 | Which value is undefined in the real system? | `√(−16)`; `−√16`; `0/8`; `√(16)` | **A**. No real square is −16; other values are −4, 0, 4. |
| R03 | Smallest set for 0.181818…? | I; Q; Z; W | **B**. Repeating block `18` implies a rational ratio (18/99). |

## Conversion and acceptance ledger

- [x] ATP skill boundary and first lesson objective identified.
- [x] Fifteen worked prompts, operations, final checks and misconceptions authored.
- [x] Fifteen four-option practice items with private keys and rationales authored.
- [x] Five mastery and three changed-value reassessment items authored.
- [ ] Independent mathematics teacher review of wording and difficulty.
- [ ] Typed runtime questions, semantic objects and ordered animation events implemented.
- [ ] Grade 9 ID/source schema and server-side MCQ grading implemented; key and full memo remain server-side.
- [ ] Automated mathematical/option validation, API reveal checks and Grade 8 regression passed.
- [ ] Browser acceptance on desktop and mobile for first, middle and advanced examples.

Do not mark this lesson published or clickable until the unchecked boxes are resolved. A written pack is a source, not a functioning interactive lesson.
