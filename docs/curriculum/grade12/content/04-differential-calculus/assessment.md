# Differential Calculus assessment and runtime appendices

# Appendix A - Formula meaning and selection map

| Target | Formula / condition | Why this is the right object |
| --- | --- | --- |
| Average change | [f(b)-f(a)]/(b-a) | Two distinct inputs define a secant and an interval-wide rate. |
| Instantaneous change | f'(a) | The derivative is the limiting tangent gradient at one input. |
| Derivative from definition | lim [f(x+h)-f(x)]/h | Vertical change divided by horizontal change, then secant separation approaches zero. |
| Tangent equation | y-y1=f'(x1)(x-x1) | Derivative supplies slope; original function supplies the point. |
| Stationary point | f'(x)=0 | Stationary means horizontal tangent, hence zero gradient. |
| Concavity | sign of f''(x) | Second derivative describes whether slopes increase or decrease. |
| Inflection | f'' candidate plus sign change | An inflection requires a change of concavity, not merely f''=0. |
| Optimisation | model, domain, Q'=0, classify, compare | The derivative produces candidates; context decides the valid optimum. |

# Appendix B - Calculus whiteboard event vocabulary

| Event | Purpose |
| --- | --- |
| plot_function | Draw the source curve with accessible axes and labels. |
| place_curve_point | Attach a semantic point to a function value. |
| draw_secant | Join two distinct points and expose average gradient. |
| move_point | Move the second point while preserving its function relationship. |
| approach_limit | Animate h approaching zero without ever dividing by zero. |
| draw_tangent | Reveal the limiting line at the target point. |
| show_change_triangle | Display Delta y and Delta x as addressable objects. |
| differentiate_term | Animate coefficient and exponent changes with a reason. |
| solve_derivative_zero | Connect a horizontal tangent to f'(x)=0. |
| test_derivative_sign | Display rising/falling or concavity evidence across intervals. |
| classify_stationary | Name local max/min/inconclusive from evidence. |
| mark_inflection | Mark only after a verified concavity change. |
| build_objective | Transform a physical constraint into a one-variable function. |
| verify_calculus_sense | Check sign, units, point membership, domain and boundaries. |

# Appendix C - Question and solution schema

| Field | Requirement |
| --- | --- |
| Identity | Stable ID, lesson ID, order, difficulty, cognitive level and marks. |
| Concept target | The precise meaning or selection decision being assessed. |
| Visual model | Curve, points, secant/tangent, sign line, derivative graph or optimisation diagram. |
| Formula anatomy | Addressable tokens with meaning, origin and validity conditions. |
| Support | Two or three hints progressing from target recognition to first valid operation. |
| Worked solution | Numbered expression, explanation, why, focus targets and verification. |
| Provenance | Athena-authored or an exact DBE year, paper and question reference. |

# Appendix D - Misconception tags

| Tag | First invalid step to detect |
| --- | --- |
| RATE_VS_VALUE | A function value is reported when a rate was requested. |
| SECANT_VS_TANGENT | An interval gradient is treated as instantaneous. |
| LIMIT_ZERO | h is set equal to zero before cancellation. |
| INVALID_CANCELLATION | A term is cancelled across addition without factorisation. |
| POWER_RULE | Coefficient or exponent transformation is incomplete. |
| POINT_VS_SLOPE | f(a) and f'(a) are confused. |
| STATIONARY_COORDINATE | Only x is found or f'(x) is used for y. |
| CLASSIFICATION | Stationary is assumed to mean maximum/minimum without evidence. |
| INFLECTION_PROOF | f''=0 is accepted without a sign change. |
| OPTIMISATION_MODEL | Differentiation starts before a one-variable model and domain exist. |
| MOTION_SIGN | Velocity and speed or position and displacement are confused. |
| INTERPRETATION | A numerical result lacks units or contextual meaning. |

# Appendix E - Past-paper evidence protocol

- Inspect official DBE Paper 1 papers and memoranda across multiple years before finalising question banks.

- Record year, session, question, sub-question, marks, skill, cognitive demand, memo method, common error and lesson mapping in paper-evidence.md.

- Use papers to guide demand and mark structure; keep ordinary Athena questions original.

- If an exact DBE item is used, label its provenance and retain the corresponding memorandum reference.

- Do not infer paper trends from one year, and do not claim provenance that has not been verified from the paper itself.

# Appendix F - Integration acceptance criteria

- The Grade 12 API returns Differential Calculus exactly once as product order 4.

- Topics 1-3 remain unchanged and all four topic cards display.

- The topic endpoint returns all 24 lessons in the approved order with no placeholder conversion text.

- The existing calculus prototype is migrated or mapped without duplicate lessons or IDs.

- Every formula lesson includes meaning, origin, anatomy, validity, selection and verification fields.

- Whiteboards animate mathematical causality and preserve semantic graph objects under pause, replay and step navigation.

- Practice remains separate from the whiteboard and preserves attempts, hints and worked-solution state.

- Tests cover first principles, derivative rules, tangent equations, stationary classification, inflection proof, cubic features, optimisation, rates and motion.

- Accessibility and reduced-motion modes communicate the same reasoning without relying on colour or animation alone.

# Appendix G - Source register

- Department of Basic Education, Grade 12 Mathematics Examination Guidelines (2021).

- Department of Basic Education, Mathematics CAPS and Annual Teaching Plan, Grade 12.

- Department of Basic Education, official National Senior Certificate past-paper archive.

- Department of Basic Education, Mathematics Grade 12 support and revision material.

- Project Athena existing calculus foundation prototype and graph registry, audited as reusable infrastructure rather than authoritative full-topic content.

# Appendix H - Review sign-off

| Reviewer | Checks | Name/date |
| --- | --- | --- |
| Grade 12 teacher | Pacing, explanation, classroom realism and learner misconceptions |  |
| Mathematics reviewer | Definitions, derivations, formulae, graphs, calculations and answers |  |
| Assessment reviewer | CAPS scope, 35-mark Paper 1 demand and memo alignment |  |
| UX/accessibility | Interaction, narration, focus, non-colour cues and reduced motion |  |
| Engineering QA | Schema, deterministic timeline, graph events, tests and mobile |  |
