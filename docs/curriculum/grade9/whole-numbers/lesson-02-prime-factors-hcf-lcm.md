# Grade 9 · Topic 1 Whole Numbers · Lesson 2: Prime factors, HCF and LCM

**Status:** authored source pack for review; no runtime lesson is registered. **Stable lesson ID:** `g9-whole-numbers-02`. **ATP source:** [DBE 2026 Grade 9 Mathematics ATP, Term 1, Whole Numbers](https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2026%20ATPs/2026_ATP_Mathematics_Grade%209.pdf). It explicitly requires prime factorisation to find LCM and HCF. Athena's questions are original, informed by the skill boundary, and are not reproduced DBE exam questions.

## Teaching contract

**Objective:** Factor positive integers greater than 1 into primes; use the *lowest shared powers* for the highest common factor (HCF) and the *highest powers present anywhere* for the lowest common multiple (LCM); decide which result a context needs, include units, and verify against the original numbers. **Prerequisites:** multiplication and division facts, divisibility tests, exponents with nonnegative integer powers. **Time:** approximately 65–80 minutes plus independent practice.

**Definitions:** A prime is an integer greater than 1 with exactly two positive factors. `1` is not prime. HCF is the largest positive integer dividing each given number. LCM is the smallest positive integer divisible by each given number. Use positive integers in this lesson; a request to factorise zero into primes is invalid. Prime powers are exact, not approximations.

**Whiteboard layout and rhythm:** Keep the problem above a two-column stage: *factor trees or aligned prime columns* on the left, and the cumulative written solution on the right. The trees use the question's actual values and animate one split at a time. Prime leaves settle into aligned rows by base. On HCF, highlight only common prime columns and select the smaller exponent; on LCM, illuminate all columns and select the larger exponent. Display the operation `2² × 3 = 12` or equivalent as a separate visible step, followed by a divisibility or multiple check. A context uses actual coloured groups, lengths or clock tracks rather than a decorative diagram. The result and its unit remain visible when the check appears. A learner can inspect a previous state without losing the earlier written lines. Semantic IDs per question: `given-a`, `given-b`, `tree-a`, `tree-b`, `prime-row-a`, `prime-row-b`, `selection`, `product`, `context-model`, `check`. For three-number examples add `given-c`, `tree-c`, `prime-row-c`. In every question, the step descriptions below specify successive visible states; do not reveal their products in the initial state. Narration and caption must match each transition.

## Worked whiteboard bank — 15 distinct questions

Each semicolon-separated action is a separate teaching transition with its own persistent memo line. The final check is another visible state; an HCF must divide **all** given numbers and an LCM must be a multiple of **all** given numbers. The visual must never fill a missing prime power with the value zero *as a factor*; absent powers have exponent 0 for LCM comparison only.

| ID / difficulty | Original question | Required animated actions and cumulative memo | Final check / first error to diagnose |
|---|---|---|---|
| W01 foundation | Is 21 prime? Write one prime factorisation. | Test division by 3 with three groups of seven; split `21 → 3 × 7`; mark both leaves prime. Written: `21 = 3 × 7`, therefore composite. | Check `3 × 7 = 21`. Error: calling every odd number prime. |
| W02 easy | Write 36 as a product of prime powers. | Split `36 → 6 × 6`; split each 6 into `2 × 3`; collect two 2s and two 3s; write `36 = 2² × 3²`. | Check `4 × 9 = 36`. Error: stopping the tree at composite 6. |
| W03 easy | Find the HCF of 18 and 24 by prime factors. | Trees `18 = 2 × 3²`, `24 = 2³ × 3`; align bases 2 and 3; highlight the smaller shared powers `2¹` and `3¹`; multiply to get `HCF = 6`. | Check `18 ÷ 6 = 3`, `24 ÷ 6 = 4`; no larger common prime power remains. Error: taking the larger exponents. |
| W04 standard | Find the LCM of 12 and 18 by prime factors. | Trees `12 = 2² × 3`, `18 = 2 × 3²`; select `2²` and `3²`; multiply `4 × 9 = 36`; write `LCM = 36`. | Check `36 ÷ 12 = 3` and `36 ÷ 18 = 2`. Error: selecting shared *smaller* powers, which gives the HCF. |
| W05 standard | Find both HCF and LCM of 20 and 30. | Align `20 = 2² × 5`, `30 = 2 × 3 × 5`; HCF selects `2 × 5 = 10`; reset only the exponent highlights, retain trees and first result; LCM selects `2² × 3 × 5 = 60`. | Check 10 divides both and 60 is divisible by both; `10 × 60 = 20 × 30`. Error: omitting prime 3 from the LCM. |
| W06 standard | Find the HCF of 72 and 108. | Split `72 = 2³ × 3²` and `108 = 2² × 3³`; align prime columns; select `2² × 3²`; multiply `4 × 9 = 36`. | Check `72 ÷ 36 = 2`, `108 ÷ 36 = 3`. Error: selecting 2³ or 3³ for HCF. |
| W07 standard | Find the LCM of 8, 12 and 15. | Three trees `8 = 2³`, `12 = 2² × 3`, `15 = 3 × 5`; compare powers across all three; select `2³ × 3 × 5`; multiply `8 × 3 × 5 = 120`. | Check `120 ÷ 8 = 15`, `120 ÷ 12 = 10`, `120 ÷ 15 = 8`. Error: only compare the first two numbers. |
| W08 intermediate | Find the HCF of 35 and 48. Explain a result of 1. | Display `35 = 5 × 7` and `48 = 2⁴ × 3`; align bases and show no shared prime column; write `HCF = 1`; distinguish 1 as a factor, not a prime. | Check 1 divides both and no prime divides both. Error: insisting that 1 itself is prime. |
| W09 intermediate | Two bells ring every 12 and 18 minutes and ring together at 09:00. When do they next ring together? | Show separate 12-minute and 18-minute clock tracks starting 09:00; factor `12 = 2² × 3`, `18 = 2 × 3²`; select LCM `2² × 3² = 36`; advance both tracks 36 minutes to `09:36`. | Check `36/12 = 3` and `36/18 = 2` cycles. Error: using HCF because the word “together” occurs. |
| W10 intermediate | Cut 84 cm and 126 cm ribbons into equal pieces of the greatest possible length without waste. Find length and number of pieces. | Draw two proportional ribbons labelled 84 cm and 126 cm; factor `84 = 2² × 3 × 7`, `126 = 2 × 3² × 7`; highlight HCF `2 × 3 × 7 = 42 cm`; partition into 2 and 3 pieces, respectively; total 5. | Check `2 × 42 = 84`, `3 × 42 = 126`; answer **42 cm each, 5 pieces total**. Error: returning the LCM as a piece length. |
| W11 exam | A learner uses `2³ × 3² = 72` as the HCF of 24 and 36. Identify the first wrong choice, then correct it. | Show `24 = 2³ × 3`, `36 = 2² × 3²`; highlight learner's 2³ choice when 36 has only 2²; replace with the *smaller* powers `2² × 3 = 12`; keep the crossed-out choice as an identified error, not a disappearing line. | Check `24 ÷ 12 = 2` and `36 ÷ 12 = 3`; 72 does not divide 24. Error: mixing largest exponents into an HCF. |
| W12 exam | Three buses leave together at 07:15, then every 8, 12 and 20 minutes. When is the first common departure after 07:15? | Draw three labelled clock tracks; factor `8 = 2³`, `12 = 2² × 3`, `20 = 2² × 5`; select `2³ × 3 × 5 = 120 min`; convert to 2 hours; advance 07:15 to **09:15**. | Check 120/8 = 15, 120/12 = 10, 120/20 = 6; no smaller shared positive interval from the prime selection. Error: treat 120 as 120 hours or omit a bus. |
| W13 exam | Find the smallest positive number divisible by 18 and 30 that is also a multiple of 4. | Note “multiple of 4” makes this the LCM of 18, 30, 4; factor `18 = 2 × 3²`, `30 = 2 × 3 × 5`, `4 = 2²`; select `2² × 3² × 5`; multiply `4 × 9 × 5 = 180`. | Check 180/18 = 10, 180/30 = 6, 180/4 = 45. Error: find LCM(18,30) = 90 and forget the third condition. |
| W14 advanced | The HCF of 54 and a positive integer `n` is 18. Which of 24, 36, 45 and 72 are possible? Explain. | Factor `54 = 2 × 3³`; require a candidate with shared `2 × 3²` but not `3³`; test 24: HCF 6; test 36: HCF 18; test 45: HCF 9; test 72: HCF 18; retain the full candidate table. Conclude **both 36 and 72** are possible; the prompt deliberately has more than one correct candidate. | Check Euclidean divisions or shared powers for 36 and 72. Error: assuming a multiple-choice list must have one answer. This is a worked example, never a four-option single-key practice item. |
| W15 advanced | A club has 96 red and 144 blue counters. Make the greatest number of identical packs using all counters. How many packs and how many of each colour per pack? | Show two colour-labelled inventories; factor `96 = 2⁵ × 3`, `144 = 2⁴ × 3²`; HCF is `2⁴ × 3 = 48` packs; distribute 96/48 = 2 red and 144/48 = 3 blue per pack; show 48 identical pack icons as a count label, not 48 tiny shapes. | Check `48 × 2 = 96`, `48 × 3 = 144`; answer **48 packs, 2 red and 3 blue in each**. Error: saying 48 counters per pack or forgetting the per-pack division. |

**Teacher review note:** W14 intentionally demonstrates that a mathematically valid question can have two answers. Its teaching point is to check all constraints. It must not be converted to a single-answer MCQ. The common identity `HCF(a,b) × LCM(a,b) = ab` applies here to two positive integers only and supplements, rather than substitutes for, prime-power reasoning.

## Independent practice — 15 book-first, four-option items

Show: “Work it out in your book, then choose one answer.” The key and explanations below stay **private**; the public payload carries the prompt and four option texts only. Options have exactly one mathematically correct answer under the stated question. The validator must detect duplicate/equivalent options and remap keys if options are reordered.

| ID | Question | A | B | C | D | Key and private reason |
|---|---|---|---|---|---|---|
| P01 | Which is a prime factorisation of 42? | `2 × 3 × 7` | `6 × 7` | `2 × 21` | `3 × 14` | **A**. All three leaves are prime; others retain a composite factor. |
| P02 | Which is the prime-power form of 48? | `2³ × 3` | `2⁴ × 3` | `2³ × 3²` | `2⁴ × 2` | **B**. `16 × 3 = 48`; A = 24, C = 72, D = 32. |
| P03 | HCF of 24 and 40? | 4 | 16 | 8 | 120 | **C**. `24 = 2³×3`, `40 = 2³×5`; shared `2³=8`. |
| P04 | LCM of 10 and 15? | 5 | 60 | 15 | 30 | **D**. `2×3×5=30`; A is HCF, B doubles the minimum, C not divisible by 10. |
| P05 | HCF of 45 and 60? | 15 | 180 | 5 | 30 | **A**. `45=3²×5`, `60=2²×3×5`; shared `3×5=15`. |
| P06 | LCM of 16 and 24? | 8 | 48 | 24 | 96 | **B**. `2⁴×3=48`; A is HCF, C omits a 2, D is a larger common multiple. |
| P07 | HCF of 32 and 27? | 3 | 9 | 1 | 6 | **C**. `32=2⁵`, `27=3³` share no prime; 1 is not prime but is their HCF. |
| P08 | LCM of 6, 8 and 9? | 24 | 18 | 36 | 72 | **D**. `2³×3²=72`; alternatives fail at least one divisor. |
| P09 | Two alarms sound every 6 and 14 minutes. How many minutes until they first sound together again? | 42 | 20 | 84 | 7 | **A**. LCM `2×3×7=42`; B adds periods, C is larger, D is not a common multiple. |
| P10 | Longest equal piece length, with no waste, from 56 cm and 70 cm strips? | 280 cm | 14 cm | 7 cm | 28 cm | **B**. HCF `2×7=14`; A is LCM, C is a shorter valid cut, D does not divide 70. |
| P11 | HCF of 54 and 90? | 9 | 30 | 18 | 270 | **C**. `54=2×3³`, `90=2×3²×5`; common `2×3²=18`. |
| P12 | LCM of 9 and 12? | 3 | 108 | 18 | 36 | **D**. `9=3²`, `12=2²×3`; LCM `2²×3²=36`. |
| P13 | Greatest number of identical packs from 60 red and 84 blue items, using all items? | 12 | 7 | 420 | 24 | **A**. HCF `2²×3=12`; 5 red and 7 blue per pack. |
| P14 | LCM of 12 and 25? | 1 | 300 | 100 | 150 | **B**. Coprime `12=2²×3`, `25=5²`; product 300. |
| P15 | Which statement is true for positive integers 18 and 27? | HCF is 18 | LCM is 27 | HCF is 9 and LCM is 54 | HCF is 3 and LCM is 81 | **C**. `18=2×3²`, `27=3³`; min shared gives 9, max gives 54. |

Option positions are A:4, B:4, C:4, D:3. Do not infer learner competence from selection alone: ask the learner to show book working before feedback, then display the factor rows and a check after submission. Practice numbers and contexts differ from the worked examples.

## Mastery and changed-value reassessment (private bank)

Five unseen mastery questions; provisional pass threshold four of five. Record chosen option, misconception tag, hints and time. After submission, show the reason and the original-number check; targeted reteaching precedes changed-value reassessment. The full memo and key must not appear in the initial lesson API.

| ID | Prompt | Four options A–D | Answer and check |
|---|---|---|---|
| M01 | HCF of 84 and 90? | 6; 3; 42; 30 | **A**. `84=2²×3×7`, `90=2×3²×5`; `2×3=6`. Both divide by 6. |
| M02 | LCM of 14 and 35? | 7; 70; 49; 140 | **B**. `14=2×7`, `35=5×7`; `2×5×7=70`, divisible by both. |
| M03 | Which is the prime-power form of 150? | `2×3×5`; `2×3²×5`; `2×3×5²`; `3×5²` | **C**. `2×3×25=150`; alternatives are 30, 90, 75. |
| M04 | Three lamps flash every 4, 6 and 9 seconds. First common flash after the initial one? | 18 s; 12 s; 72 s; 36 s | **D**. LCM `2²×3²=36 s`; divisible by 4, 6 and 9. |
| M05 | Greatest number of identical packs using 45 pencils and 75 pens, with none left? | 15; 5; 225; 30 | **A**. HCF `3×5=15`; each pack has 3 pencils and 5 pens. |

If tag `composite-leaf`, reteach W01/W02 with 30 and 42. If `hcf-power-direction`, reteach W03/W06/W11 with aligned prime powers. If `lcm-power-direction` or `forgot-third-number`, reteach W04/W07/W13. If `context-choice`, contrast W09 with W10 and ask which quantity repeats or partitions before calculating. Then administer one or more parallel items:

| ID | Prompt | Four options A–D | Answer and check |
|---|---|---|---|
| R01 | HCF of 48 and 80? | 8; 16; 240; 32 | **B**. `48=2⁴×3`, `80=2⁴×5`; common `2⁴=16`. |
| R02 | LCM of 15, 20 and 24? | 60; 240; 120; 30 | **C**. Select `2³×3×5=120`; divide by 15, 20 and 24 to check. |
| R03 | Longest equal pieces from 63 cm and 105 cm, without waste? | 315 cm; 7 cm; 35 cm; 21 cm | **D**. `63=3²×7`, `105=3×5×7`; HCF `3×7=21 cm`. |

## Conversion and acceptance ledger

- [x] ATP skill boundary and prerequisite relationship to Lesson 1 identified.
- [x] Fifteen worked prompts, distinct transitions, full results, original-number checks and error diagnoses authored.
- [x] Fifteen four-option practice prompts with unique answers and private rationales authored.
- [x] Five mastery and three changed-value reassessment prompts authored.
- [ ] Independent mathematics teacher review of wording, pacing and difficulty.
- [ ] Typed runtime questions and question-specific factor-tree/clock/ribbon animations implemented.
- [ ] Grade 9 catalogue and server-side four-option grading implemented; keys and memos remain private.
- [ ] Automated arithmetic, option uniqueness, HCF/LCM checks and Grade 8 regression passed.
- [ ] Desktop and mobile browser verification, including cumulative memo and backward/forward navigation.

Do not mark this lesson published or clickable while unchecked items remain. A written pack is a source, not a functioning interactive lesson.
