# Project Athena — Phase 1 Build

A visual AI mathematics learning platform for South African Grade
8–12 learners, aligned to CAPS and supporting IEB preparation. This
package is the **Phase 1 foundation**: a fully working frontend UI,
plus an annotated (non-functional) backend scaffold ready for
Phase 2 onward.

## What's actually working right now

Open `frontend/index.html` in a browser (or serve the folder — see
below) and you can:

- Browse the home page, pick a grade, open a topic
- Open a lesson and play/pause/step through an **animated
  whiteboard** (the animation engine) showing a worked example
- Take that lesson's **quiz** — you must pass it before the next
  lesson unlocks (progress is saved in `localStorage`)
- Hit a paywall on a premium-flagged lesson and "unlock" it (a
  Phase 1 stub — no real payment yet)
- Sign up through the 3-step flow, or log in (both are stubs that
  set a local session — no real backend account yet)

Two topics are seeded with real content so the flow is testable
end-to-end: **Grade 10 — Equations & Inequalities** (3 lessons) and
**Grade 12 — Differential Calculus** (1 lesson).

## How to run it

No build step — it's plain HTML/CSS/JS. From `frontend/`:

```bash
# any static server works, e.g.:
python3 -m http.server 8080
# then open http://localhost:8080
```

Opening `index.html` directly via `file://` also works, since
nothing here calls a backend yet.

## File structure

```
project-athena/
├── frontend/                    ← Phase 1: fully functional
│   ├── index.html                 Home / marketing page
│   ├── signup.html, login.html    Auth (stubbed — see js/pages/)
│   ├── dashboard.html             Learner dashboard
│   ├── grade.html                 Grade overview + term progress
│   ├── topic.html                 Topic detail + lesson list (locking)
│   ├── lesson.html                Animated lesson + quiz gate
│   ├── css/
│   │   ├── tokens.css               Design tokens (colour/type/space)
│   │   ├── base.css                 Reset + accessibility defaults
│   │   ├── components.css           Buttons, cards, nav, whiteboard, quiz
│   │   └── pages.css                Page-specific layout
│   └── js/
│       ├── data/curriculum-data.js  Mock curriculum "database" + query API
│       ├── engine/
│       │   ├── state.js               Progress/auth store (localStorage)
│       │   ├── animation-engine.js    ★ the animation engine
│       │   ├── quiz-engine.js         ★ the per-lesson quiz + gating
│       │   └── navigation.js          Shared top nav
│       └── pages/
│           ├── dashboard.js, grade.js, topic.js, lesson.js
│           └── signup.js, login.js
│
├── backend/                     ← NOT functional — annotated scaffold only
│   ├── README.md                  Build order + how to start Phase 2
│   ├── requirements.txt           Target dependency set (commented)
│   └── app/
│       ├── main.py                  FastAPI entrypoint (TODO)
│       ├── core/config.py, security.py
│       ├── db/database.py
│       ├── db/models/user.py, curriculum.py, progress.py
│       ├── api/v1/auth.py, curriculum.py, lessons.py, quizzes.py,
│       │         ai_tutor.py, payments.py
│       └── services/animation_service.py, ai_gateway.py,
│                     math_verification.py
│
└── README.md                    ← this file
```

Every backend file has a real docstring explaining what it will do
and which frontend file it eventually replaces or talks to — read
`backend/README.md` first for build order.

## How the animation engine works (and how to add a new one)

`frontend/js/engine/animation-engine.js` never runs arbitrary
code — it only knows how to render named **templates**:

```js
TEMPLATES = {
  linear_equation_balance(ctx, w, h, step) { ... },
  tangent_line(ctx, w, h, step) { ... }
}
```

A lesson's animation is just declarative JSON in
`curriculum-data.js`:

```js
animation: {
  template: "linear_equation_balance",
  steps: [
    { op: "subtract_both_sides", value: 5, before: "2x + 5 = 15", after: "2x = 10", narration: "..." },
    ...
  ]
}
```

To add a new visual concept (e.g. factorisation, a unit circle),
add one new function to `TEMPLATES` — never scatter
`if (type === "x")` branches across the page files. This is the
same contract the backend's `services/animation_service.py` will
enforce server-side once the AI Tutor (Phase 4) starts generating
these instructions instead of a curriculum author.

## Quiz-to-progress gating

Every lesson has a `quiz` object in `curriculum-data.js`. A learner
must score at or above `passMark` (currently 70%) to mark that
lesson complete. `AthenaState.isLessonUnlocked(topic, lessonId)` in
`state.js` checks whether the *previous* lesson in the topic is
complete before allowing access — the first lesson in any topic is
always open. This is currently enforced client-side only; the
`backend/README.md` notes exactly where this needs to move
server-side (`api/v1/quizzes.py`) so it can't be bypassed by editing
local storage.

## Design direction

Palette, type, and layout follow the brief's "Education Blue"
system (calm, academic, not AI-chatbot-looking), refined for
accessible contrast: **Lora** for headings (a textbook feel),
**Inter** for UI/body text, and a monospace face for equations
until a proper math-typesetting library (e.g. KaTeX) is wired in.

## What's intentionally NOT here yet

Per the brief's phased plan (`Phase 1 → 9`) and "what we should not
build yet" list: no real backend, no real payments, no AI Tutor, no
OCR, no native apps. The backend directory documents exactly what
each of those needs once its phase starts.
