# Finance assessment and runtime appendices

# Appendix A — Formula and timeline reference

| Model | Formula | Timeline test |
| --- | --- | --- |
| Simple growth | A=P(1+in) | i and n share one time unit; interest is based on P. |
| Compound growth | A=P(1+i)^n | Count compounding periods crossed. |
| Reducing-balance decay | A=P(1−i)^n | Percentage acts on current value. |
| Effective annual rate | (1+j/m)^m−1 | Exactly one year contains m compounding steps. |
| FV annuity | S=x[(1+i)^n−1]/i | Last payment earns zero periods at immediate valuation. |
| PV annuity | P=x[1−(1+i)^−n]/i | First payment occurs one period after date 0. |
| Outstanding balance | B_k=x[1−(1+i)^−(n−k)]/i | State immediately before/after payment k. |

# Appendix B — Finance whiteboard event vocabulary

| Event | Purpose |
| --- | --- |
| place_cashflow | Place a labelled deposit, withdrawal, loan or instalment at an exact date. |
| set_focal_date | Declare the date at which all values will be compared. |
| label_period | Show the compounding/payment unit and period number. |
| match_rate_period | Pair periodic i with the matching n before substitution. |
| accumulate | Move a value forward through visible growth factors. |
| discount | Move a value backward through visible inverse factors. |
| count_payments | Reveal every payment arrow and the total n. |
| split_phase | Divide a timeline at a rate or cash-flow change. |
| verify_financial_sense | Check direction, magnitude, remaining payments and rounding. |

# Appendix C — Question and worked-solution schema

| Field | Requirement |
| --- | --- |
| Identity | Stable ID, lesson ID, order, difficulty, cognitive level and marks. |
| Prompt | Original wording aligned to CAPS and an observed NSC-style demand. |
| Timeline | Date 0, focal date, rate periods, cash flows, payment count and before/after qualifiers. |
| Support | Two or three hints progressing from strategy to specific structure. |
| Solution | Numbered steps; each includes expression, explanation, why and focus targets. |
| Verification | Reverse calculation, second balance method, target comparison or adjacent-period test. |
| Provenance | Athena-authored or an exact DBE year, paper and question reference. |

# Appendix D — Error tags

| Tag | First invalid step to detect |
| --- | --- |
| RATE_PERIOD | Rate and exponent/payment period use different units. |
| PV_FV_DIRECTION | Value is moved in the wrong time direction. |
| PAYMENT_TIMING | Payment count or first/last payment is off by one. |
| DEPRECIATION_MODEL | Straight-line and reducing-balance models are mixed. |
| FOCAL_DATE | Values from different dates are combined. |
| BALANCE_INSTANT | Before/after-payment wording is ignored. |
| ROUNDING | Intermediate values are rounded too early. |
| INTERPRETATION | The numerical answer is not connected to the context. |

# Appendix E — Integration acceptance criteria

- The Grade 12 API returns Finance, Growth and Decay exactly once as product order 3.

- The topic endpoint returns one learning path and all 16 ordered lessons.

- No finance lesson says ‘Awaiting approved lesson-pack conversion’ after conversion.

- Topics 1 and 2 remain unchanged and all three topic cards display.

- First three finance lessons are complete vertical slices before batch conversion.

- Every calculation uses compatible rate and period units and is independently tested.

- Whiteboards expose cash-flow timing and do not render formulas as unexplained snapshots.

- Practice remains separate from the whiteboard and preserves attempts, hints and worked-solution state.

- Development unlocking is backend-authoritative and impossible in production.

- Automated tests cover registration, order, formulas, payment counts, balances, accessibility and responsive rendering.

# Appendix F — Source register

- Department of Basic Education, Grade 12 Mathematics Examination Guidelines (2021).

- Department of Basic Education, Mathematics Annual Teaching Plan, Grade 12.

- Department of Basic Education, official National Senior Certificate past-paper archive.

- Department of Basic Education, Financial Mathematics Grade 12 support material.

- Department of Basic Education, Mathematics examiner diagnostic and revision material.

# Appendix G — Review sign-off

| Reviewer | Checks | Name/date |
| --- | --- | --- |
| Grade 12 teacher | Pacing, explanation and classroom realism |  |
| Mathematics reviewer | Formulae, timelines, calculations and answers |  |
| Assessment reviewer | CAPS scope and Paper 1 demand |  |
| UX/accessibility | Interaction, focus and non-colour cues |  |
| Engineering QA | Schema, deterministic timeline, tests and mobile |  |
