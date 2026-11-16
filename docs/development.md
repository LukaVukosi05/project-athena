# Development and file management

## Boundaries

Keep request parsing and HTTP endpoints in `backend/app/api/v1`. Public lesson
construction belongs in `app/lessons/payload.py`, Grade 8 exceptions in
`grade8_preview.py`, and Grade 9–11 visual-givens policies in `visual_preview.py`.
Payload construction starts from `model_dump()` and must not mutate authored
curriculum models. Conceal private results in both whiteboard question lists and
embedded block copies. Reveal and diagnosis endpoints retain their access gates.

Practice routes have three owners: `topic_diagnostics.py` for topic revision,
`practice_questions.py` for sessions/answers/hints/solutions, and
`practice_assessments.py` for mastery/repair/reassessment. `practice.py` only
composes these routes. Shared session lookup, ownership checks and response
writes live in `practice/session_store.py`; assessment scoring lives in
`practice/assessment_scoring.py`. Use the existing response-writing helper rather
than duplicating copy/assign/commit code for each assessment state.

## Registering content

For Grades 8–11, add each lesson once to `practice/banks/gradeN.py`, with the
existing five components: practice, mastery, parallel reassessment, repairs and
rules. The public practice catalogue takes component zero; the private assessment
catalogue takes the remaining four. Use `module_bank()` for authored modules with
named bank constants. Keep exceptional rules explicit, including the Grade 8
pattern-repair rules. Grade 12's existing practice-only contract remains separate.

`curriculum/grade8/gold_pack_runtime.py` owns shared question metadata and visual
parameter construction for the ten equation Gold Packs. Pass lesson-specific
board objects and timeline counts explicitly; retain each lesson's teaching logic
and extra animation operations in its module.

Keep lesson IDs, source filenames, JSON assets and renderer IDs stable. They are
referenced by catalogue generation, tests, source hashes and browser URLs. Do not
move authored documents or generated lesson JSON merely to shorten a directory
listing. Regenerate the curriculum catalogue through the existing script when
changing curriculum registrations; do not silently bypass its validation.

For a new Grade 9–11 visual, register its renderer family and private value keys
in `lessons/visual_preview.py`. Add mode-dependent redaction explicitly and verify
both its initial payload and reveal. Unknown families retain the generic givens
fallback; never default to exposing a complete private scene.

## Browser code

`frontend/js/engine/html.js` owns `escapeHtml()`. Load it before navigation,
page controllers or engines that use it. Do not redeclare that global in each
page. Keep native mathematical renderer modules under `js/visualization` and
whiteboard playback under `js/whiteboard`; shared helpers must not change a
subject-specific mathematical rule merely because its code looks similar.

`tools/` and `scripts/` contain authoring and QA utilities. They are not part of
application startup. Historical source packs and review tools are preserved until
their callers and provenance requirements are understood. No database/schema,
lesson readiness or billing changes are included in the runtime refactor.

## Verification

Install `backend/requirements-dev.txt`. From the repository root, use a test-only
JWT secret and a disposable SQLite database. In Bash:

```bash
export ATHENA_JWT_SECRET=local-tests-only
export ATHENA_DATABASE_URL=sqlite:////tmp/athena-tests.db
export PYTHONPATH=backend
ATHENA_UNLOCK_ALL_LESSONS=true python -m pytest backend/tests -q
ATHENA_UNLOCK_ALL_LESSONS=false python -m pytest backend/tests/test_lesson_access.py backend/tests/test_auth.py backend/tests/test_practice.py backend/tests/test_practice_session_ownership.py -q
node --test frontend/tests/*.test.js
python tools/verify_runtime_parity.py
```

In PowerShell, set environment values with `$env:NAME = 'value'`; use
`$env:ATHENA_DATABASE_URL = 'sqlite:///./backend/athena-tests.db'` and delete that
**test-only** file afterward. Never point this command at a learner database.
Full content tests assume the development unlock; access tests explicitly disable
it. Running the entire original suite with unlock disabled produces 34 content
failures because those tests request premium lessons anonymously.

The parity tool compares the current working tree against saved commit
`a393b6c7b3ff883fc16c5f5c9922f5a0be660fe9` by default. It uses a temporary Git
worktree and two isolated Python processes, with in-memory databases and a
synthetic premium user. It hashes the complete JSON content of every registered
lesson entry, reveal result and practice/assessment bank, plus the API schema.
It reports differing IDs and exits nonzero on changes. Pass `--baseline <ref>`
when comparing a later refactor. The comparison validates behavior preservation,
not mathematical correctness, production readiness or visual accessibility.

## Git and local files

Use a feature branch from the saved checkpoint. Keep the backup branch unchanged.
Commit reviewed source/docs/tests only; inspect `git status --short` first. Do not
commit `.env`, SQLite databases, virtual environments, browser output or logs.
Keep reproducible test artifacts outside tracked source or in ignored
`artifacts/`. Do not delete an untracked database as part of repository cleanup.
