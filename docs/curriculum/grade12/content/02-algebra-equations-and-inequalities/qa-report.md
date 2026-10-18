# Topic 2 authoring QA report

Status: **Lessons 1–3 authored; Lessons 4–18 pending; not integrated.**

## Structural QA

| Check | Result |
|---|---|
| Topic manifest contains the prescribed 18 stable lesson IDs/titles | Pass |
| Only Lessons 1–3 have authored lesson files | Pass |
| Required front matter and 80% threshold | Pass |
| Each authored lesson contains 24 items | Pass |
| Per-lesson categories are 4 diagnostic / 6 guided / 10 independent / 2 misconception / 2 exam-style | Pass |
| All item IDs unique | Pass |
| Topic 1 untouched | Pass (verified by scoped Git diff) |
| Application/catalogue/routes/runtime whiteboard untouched | Pass (verified by scoped Git diff) |

## Question counts and cognition

| Lesson | K | R | C | P | Total |
|---|---:|---:|---:|---:|---:|
| 1 | 6 | 8 | 7 | 3 | 24 |
| 2 | 4 | 9 | 7 | 4 | 24 |
| 3 | 4 | 8 | 8 | 4 | 24 |
| **Total** | **14** | **25** | **22** | **11** | **72** |
| **Actual** | **19.4%** | **34.7%** | **30.6%** | **15.3%** | **100%** |
| **CAPS target** | **20%** | **35%** | **30%** | **15%** | **100%** |

Rounding to whole questions gives the closest balanced 72-item allocation while retaining the required per-lesson variety.

## Practice record contract

Every numbered bank record supplies, in a compact terminal-readable format:

- stable ID, difficulty, cognitive level and marks;
- question type where it is not self-evidently short-text/numeric;
- prompt and accepted answer representation;
- two progressive hints (three where an additional scaffold is necessary);
- worked solution operations;
- a distinct plain-language **Why?** explanation;
- verification;
- misconception classification from its lesson repair table/category;
- source metadata inherited explicitly from the bank heading: `DBE CAPS skill scope; Athena-original; no past-paper wording`.

The eventual runtime conversion must preserve these fields and gate full solutions until an attempt. This authoring increment deliberately does not modify runtime schemas.

## Mathematical QA performed

- Expanded every proposed HCF, difference-of-squares, trinomial, grouping and repeated-power factorisation back to its source expression.
- Recomputed all fraction arithmetic and equation solutions using exact rational arithmetic.
- Re-factored every algebraic-fraction numerator/denominator and derived restrictions from the **original** denominator before cancellation.
- For division of algebraic fractions, also excluded inputs that make the divisor zero.
- Checked algebraic-fraction equivalence at permitted values and separately compared domains.
- Confirmed that no cancellation is applied to terms joined by addition/subtraction.
- Checked the correction log items after authoring.

## Whiteboard content QA

Allowed semantic events used are a subset of:

`focus`, `dim`, `reveal`, `write`, `expand`, `factor`, `substitute`, `apply_both_sides`, `cancel_factor`, `compare`, `group`, `mark_restriction`, `checkpoint`, `verify`.

Each primary timeline orients through its prompt/context, focuses relevant symbols, displays the operation before the result, gives a checkpoint, and ends in verification. No JavaScript, HTML, SVG, expression evaluator or runtime callback is embedded.

## Serious misconception gates

- Lesson 1: negative signs, exponent-law misuse, one-sided equation changes.
- Lesson 2: invalid identity selection and inability to verify by expansion.
- Lesson 3: cancelling terms and omitting original restrictions.

These block mastery until a correction item is passed, even if the aggregate is at least 80%.

## Accessibility/content review

- Semantic targets have learner-readable accessibility text on primary timelines.
- Meaning is not encoded by colour.
- Narration states the mathematical reason rather than describing decoration.
- Symbolic notation is accompanied by plain-language meaning.
- Checkpoints can be answered without relying on motion.

## Open QA item

The current official Grade 12 Mathematics ATP was not located locally or verified from an official DBE publication during this pass. Term/week metadata remains pending. It must be resolved before publication; no assumed pacing has been authored.
