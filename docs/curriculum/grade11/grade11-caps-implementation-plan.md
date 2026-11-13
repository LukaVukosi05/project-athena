# Grade 11 Mathematics: source and implementation plan

Status: Topics 1–10 have authored runtime previews, source files, whiteboard
timelines and assessment banks. They remain teacher-review-required. Browser
acceptance and teacher approval have not been recorded; do not label them
published. Topics 11–12 remain plans, not interactive lessons.

Topic 10 has six finance lessons with original questions and staged amount, exchange and rate models. Rounding, quote direction, hire-purchase conventions and final verification require teacher and browser acceptance.

Topic 9 has seven original Probability lessons covering relative frequency,
two- and three-event Venn diagrams, independent events, dependent draws,
contingency tables and first-error repair. The 2023/24 ATP and Mathematics CAPS
list these event models for Term 3. Each question owns its diagram and exact
fraction arithmetic. Grade 11 teacher review must check the example range,
diagram region placement, language and Paper 1 interpretation in a live browser.

Topic 8 now has seven authored Statistics lessons with individual data sets, diagrams and assessments. The 2023/24 ATP explicitly lists central tendency, quartiles, histograms, frequency polygons, ogives, ungrouped standard deviation, skew and outliers. The seventh lesson adds CAPS bivariate scatterplots and model choice. The paper label is Paper 2. Teacher and desktop/mobile browser acceptance remain outstanding.

Topic 7 now contains five original triangle-rule lessons with 75 worked examples, 75 practice, 25 mastery and 15 reassessment items. Proofs, live diagrams, angle labels and the alternate sine branch require teacher and browser acceptance.

Topic 6 uses four Paper 1 algebraic graph lessons and four Paper 2
trigonometric graph lessons. Each has staged, question-specific plots, source
questions and assessments. The graph sampling, tangent asymptotes, exact-value
notations and difficulty progression still require live browser and teacher
acceptance before publication.

Topic 5 has six original coordinate lessons with plotted points, staged
constructions and assessment banks. Mathematical correctness is checked by
independent coordinate arithmetic. Actual desktop/mobile browser acceptance
and teacher review are still required. The lesson progression should be
checked against real Grade 11 assessment papers before release.

Topic 4's eight lessons currently teach numerical circle-theorem applications
and combined riders. Formal theorem proofs, all available converses, and
exterior-angle constructions still need their own teacher-authored examples
before the topic can be described as complete. A teacher must also verify
diagram geometry, reasons and the full question progression in a live browser.

## Authority and scope

Primary source: [DBE 2023/24 Grade 11 Mathematics ATP](https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2023%20ATPs/FET%20Content%20Subjects/Grade%2011/1.590%20ATP%202023-24%20Gr%2011%20Maths%20final.pdf?ver=2022-12-22-114024-067), pages 1–5. The DBE site currently publishes this under its FET ATP collection. Confirm the applicable school-year ATP before calling the lessons 2027-aligned.

The ATP names teaching blocks, not a fixed number of lessons. The proposed lesson
counts below are Athena authoring decisions. Paper labels follow the ATP's
150-mark Paper 1 and Paper 2 content breakdown.

| Order | ATP block | Term | Paper | Proposed lessons | Visual families that must be question-specific |
| ---: | --- | ---: | --- | ---: | --- |
| 1 | Exponents and surds | 1 | 1 | 6 | Exponent factor stacks, rational-root construction, surd factor trees, domain restrictions |
| 2 | Equations and inequalities | 1 | 1 | 7 | Completing-square area, parabola/line intersections, sign chart and solution intervals |
| 3 | Trigonometry: reduction formulae, equations and general solutions | 1 | 2 | 7 | Unit-circle quadrant signs, reference angles, identity triangles and periodic solution arcs |
| 4 | Euclidean geometry: circle theorems and riders | 2 | 2 | 8 | Chords, centre, tangent, arc, marked equal angles and justified proof links |
| 5 | Analytical geometry | 2 | 2 | 6 | Coordinate plane, gradients, perpendicular lines and inclination arcs |
| 6 | Functions, including trigonometric graphs | 2 | 1 and 2 | 8 | Plotted coordinates, parameter-controlled curves and intercept/asymptote/period marks |
| 7 | Trigonometry: sine, cosine and area rules | 3 | 2 | 5 | Labelled oblique triangles, ambiguous cases and area decomposition |
| 8 | Statistics | 3 | 2 | 7 | Grouped tables, five-number box plots, frequency polygons, ogives and deviation plots |
| 9 | Probability | 3 | 1 | 7 | Venn regions, two/three-event counts, dependent trees and contingency tables |
| 10 | Finance, growth and decay | 3 | 1 | 6 | Amount timelines, compounding-period comparisons and rate conversions |
| 11 | Quadratic number patterns | 4 | 1 | 5 | Figural growth, first/second-difference tables and term-position plots |
| 12 | Measurement revision and integration | 4 | 2 | 4 | Solid nets, exposed surfaces, dimension scaling and composite solids |

The ATP's separate Term 4 algebra and trigonometry revision should be attached
as reassessment and recovery paths to Topics 1–3, rather than counted as invented
new mathematical topics. The Paper 1/Paper 2 split for Functions reflects
algebraic versus trigonometric function questions and requires a teacher check
against the final examination blueprint.

## Topic 1: Exponents and surds — lesson blueprint

| Lesson | Mathematics and difficulty progression | Specific visual and teaching actions |
| ---: | --- | --- |
| 1 | Positive rational powers, `x^(p/q)`, restrictions `x > 0, q > 0` | Separate the denominator's root index from the numerator's power; reveal root groups and exponent units one at a time; verify by raising back to `q`. |
| 2 | Laws of exponents with rational, zero and negative powers | Keep a single base and visible domain; show factor-stack cancellation and reciprocal movement; check the original against the result at a legal value. |
| 3 | Simplifying simple surds | Build a prime-square factor tree for each actual radicand, extract pairs, preserve the remaining radicand, and square the result as a check. |
| 4 | Adding, subtracting and multiplying surds | Simplify each radicand first; group only like radicals; use an area or two-branch product model for multiplication; verify a numerical estimate. |
| 5 | Division and rationalising simple surds | Show the original denominator, multiply numerator and denominator by the same nonzero surd or conjugate, then simplify and compare numerically. |
| 6 | Simple surd equations and first-error reassessment | Mark the principal-root restriction, isolate the radical, square both sides visibly, test every candidate in the original and cross out extraneous roots. |

Each lesson requires 15 authored worked questions with a foundation-to-exam
progression, 15 independent four-option questions, five mastery questions and
three parallel reassessments. All four answer options must be distinct and
validated against the exact question. The last worked questions must demand
multi-step selection and checking, not just larger numbers.

## Runtime contract for the next batch

1. Register only lessons with actual source questions, visual templates and
   assessment banks; expose their teacher-review status accurately.
2. Use stable lesson and question IDs. Every visual parameter derives from its
   question; no single generic surd diagram may stand in for every case.
3. Show the original expression, current operation and cumulative written
   solution simultaneously. Reveal exactly one mathematical action at each
   step; maintain the previous steps during replay, Previous and Next.
4. Give each action matching narration and caption, a relevant visual target,
   enough time to finish, and deterministic pause/resume. Audio-off and reduced
   motion must preserve the complete mathematics.
5. Hide final answers before the appropriate reveal or submission. The final
   state must contain the checked answer, including domain and extraneous-root
   decisions.
6. Test content arithmetic, source hashes, question-specific visual changes,
   desktop/mobile overflow, API answer gating, assessment gates and direct URL
   restoration. Independent teacher review and actual browser acceptance are
   distinct gates; neither may be claimed from automated tests alone.

## Existing Grade 10 carry-forward issue

Measurement's topic was correctly tagged Paper 2 while its generated lessons
were tagged Paper 1. The runtime metadata must be aligned before Grade 11 uses
these labels. Grade 10 source lessons remain marked teacher-review-required;
their counts are authored preview counts, not published counts.
