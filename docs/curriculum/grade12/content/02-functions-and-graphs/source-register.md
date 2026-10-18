# Source register and appendices

# Appendix A — Function-family reference

| Family | Core form | Features to expose |
| --- | --- | --- |
| Linear | y=mx+c | gradient, intercepts, rate |
| Quadratic | y=a(x−p)²+q | vertex, axis, roots, range |
| Hyperbola | y=a/(x−p)+q | asymptotes, domain/range, branches |
| Exponential | y=ab^(x−p)+q | growth/decay, asymptote, range |
| Logarithmic | y=log_b(x−p)+q | inverse, domain, vertical asymptote |

# Appendix B — Whiteboard acceptance checks

- Axes, origin, scale and units are visible.

- Key points are exact and labelled.

- Asymptotes appear before branches.

- Transformations animate from the parent graph.

- Equation, table and graph remain synchronised.

- Inverse graphs reflect in y=x and swap domain/range.

- Interval answers project onto the x-axis.

- Colour is reinforced by labels or patterns.

- Previous/next steps are deterministic.

- All calculations and restrictions are independently checked.

# Appendix C — Question and solution schema

| Field | Requirement |
| --- | --- |
| Identity | Stable ID, lesson ID, order, difficulty, cognitive level and marks. |
| Prompt | Original wording matched to the lesson objective and NSC-style demand. |
| Graph state | Exact equation, domain, viewport, axes, asymptotes, points and labels. |
| Support | Two or three progressive hints from strategy to specific support. |
| Solution | Numbered mathematical steps; each step includes expression, explanation and why. |
| Verification | Substitution, feature comparison, graph intersection or inverse composition. |
| Provenance | Athena-authored or exact DBE source with year, paper and question metadata. |

# Appendix D — Integration acceptance criteria

- The Grade 12 API returns Functions and Graphs exactly once as product order 2.

- The topic endpoint returns one learning path and all 18 ordered lessons.

- No lesson card says “Awaiting approved lesson-pack conversion” after conversion.

- Lesson breadcrumbs, position and next/previous navigation come from API metadata.

- The first three lessons are complete vertical slices before mass conversion.

- Every graph specification is validated mathematically and visually.

- Sequences and Series remains unchanged.

- Development unlocking is backend-authoritative and cannot operate in production.

- Automated tests cover API registration, ordering, graph states, practice state and mobile rendering.

# Appendix E — Source register

- Department of Basic Education, Grade 12 Mathematics Examination Guidelines (2021).

- Department of Basic Education, Mathematics Annual Teaching Plan, Grade 12 (2023/24).

- Department of Basic Education, Mathematics Paper 1 and marking guidelines, November 2020.

- Department of Basic Education, Mathematics Paper 1 and marking guidelines, November 2022.

- Department of Basic Education, Mathematics Paper 1 and marking guidelines, November 2023.

- Department of Basic Education, Mathematics Paper 1 and marking guidelines, November 2024.

# Appendix F — Review sign-off

| Reviewer | Checks | Name/date |
| --- | --- | --- |
| Grade 12 teacher | Pacing, explanation and classroom realism |  |
| Mathematics reviewer | Equations, graphs, domains and answers |  |
| Assessment reviewer | CAPS scope and cognitive demand |  |
| UX/accessibility | Interaction, focus and non-colour cues |  |
| Engineering QA | Graph state, tests and responsive rendering |  |
