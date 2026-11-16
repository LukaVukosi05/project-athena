# Runtime refactor — 16 November 2026

Baseline: `a393b6c7b3ff883fc16c5f5c9922f5a0be660fe9`, from
`backup/athena-all-work-2026-11-13`. Work branch:
`refactor/modular-runtime-2026-11-16`.

## Changes

- Extracted public lesson documents from the HTTP router into `lessons/payload.py`.
  Grade 8 preview exceptions and Grade 9–11 visual redaction have separate owners.
- Replaced 29 repeated visual copy/remove/rebuild branches with one policy table
  and explicit conditional exceptions. Embedded boards and question previews use
  the same gated copy.
- Replaced separate practice/mastery lesson registrations with grade-specific
  five-component bank registrations. Public/private catalogues derive from them.
- Split practice routes into topic diagnostics, question/session operations and
  mastery/repair/reassessment. Kept historical registry/scorer imports available.
- Reused the same response persistence helper for mastery, repair and reassessment.
- Shared question metadata, renderer parameters and common animation operations
  across ten Grade 8 equation Gold Packs. Lesson 7 retains its extra distribution
  operation; Lesson 10 retains its diagnosis renderer family. Authored board
  logic, lesson IDs, assets and mathematical content stay in their existing files.
- Replaced six browser `escapeHtml()` definitions with one shared helper, loaded
  before consumers on all twelve application pages.
- Replaced obsolete scaffold READMEs, documented ownership and test commands,
  declared missing configuration/email validation dependencies and dev tools.
- Added a reusable baseline comparison tool and regression coverage for helper
  loading/escaping and authenticated practice-session ownership/persistence.

## Verification

| Check | Baseline | Refactored |
| --- | --- | --- |
| Full backend suite with development content unlock | 379 passed | 380 passed |
| Frontend Node suite | 255 passed | 257 passed |
| Access/auth/practice subset with unlock disabled | Not separately rerun | 16 passed before adding the ownership regression |
| Runtime JSON/API comparison | Reference | Exact match |

The runtime comparison covers **448 lesson entries, 5,572 worked-reveal results,
402 practice-bank entries with their associated assessment data, and the complete
OpenAPI schema**. JSON objects are compared by content after sorting object keys;
list ordering and response/error content remain part of the comparison. Counts
include registered entries and blocked/not-found reveal results; they are not
claims of approved or playable curriculum coverage.

A scan of top-level Python functions of at least six lines found two groups of
exact repeated definitions before the final helper extraction and none afterward.
This is a bounded syntactic check, not proof that all conceptual duplication or
unused code has been eliminated. Subject-specific teaching code was not collapsed
merely because it looked similar.

Full original backend tests with unlock disabled returned 345 passes and 34
premium-content failures. The original suite passes with the development unlock
because those content tests request premium lessons anonymously. Access tests
explicitly disable the override and check unauthenticated/non-premium denial and
production override rejection. Default application access behavior was preserved.
Two dependency deprecation warnings remain in this environment.

## Limits and follow-up

A live Chromium mobile/desktop comparison was attempted but could not start:
Chromium's required process socket was denied by the execution environment.
No browser screenshots or manual visual/audio acceptance are claimed. Recheck
lesson playback, example selection, hints, signup and mobile layouts locally
before merging. The Node rendering/controller suites and exact API comparisons
passed, but they do not validate the user's local browser, learner database or
production configuration.

This refactor does not add payments, promote teacher-review content, migrate a
database or establish production readiness. The user's untracked
`backend/athena-measurement-review.db` was unavailable here and was not inspected,
modified, uploaded or claimed as backed up. The saved backup branch is preserved.
See `docs/development.md` for rerun commands and extension rules.
