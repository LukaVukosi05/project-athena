# Architecture assessment

## Current state

The browser application is a dependency-free HTML/CSS/JavaScript prototype.
Its page controllers are small and reusable, but they synchronously read a
global curriculum object and enforce progress, answers and premium access in
local storage. The canvas whiteboard has a useful named-template boundary, but
each step redraws a final snapshot rather than resolving a mathematical
operation into reversible visual states.

The FastAPI backend has working SQLAlchemy configuration, JWT authentication and
a persisted user model. Curriculum endpoints exist, but use untyped in-memory
dictionaries. Curriculum, progress and animation database models, quiz grading,
subscription entitlement, animation validation and mathematical verification
are not implemented.

## Decisions

- Retain FastAPI, SQLAlchemy, JWT auth, the browser page shell, quiz interaction,
  canvas drawing helpers, narration and a registered animation-template model.
- Add a typed curriculum domain and repository boundary before database
  persistence. This gives teacher-reviewable source data without coupling API
  routes to Grade 12 files; SQLAlchemy repositories can replace it later.
- Separate curriculum structure, educational lesson blocks, whiteboard plans
  and question data.
- Seed the complete Grade 12 hierarchy as draft metadata. Only the Algebra
  Foundations linear-equation vertical slice is publishable initially.
- Resolve immutable whiteboard steps from registered operation renderers.
  Previous/Next selects a state deterministically; renderers do not mutate an
  earlier state.
- Enforce premium lesson retrieval in FastAPI. Client-side presentation remains
  a convenience, never the authority.

## Deferred deliberately

Teacher approval workflows, subscriptions with expiry, persisted mastery,
server-side quiz grading, rate limiting, KaTeX and symbolic verification need
their own migrations and tests. They should not be faked inside this vertical
slice.
