# Auth patch verification — 16 November 2026

Base: main at `442e8a4c9ec18180756fa454806b77a16bfb6ad8`.
Feature: `feature/auth-session-social-2026-11-16`.

- Full backend regression: **392 passed** (380 existing + 12 auth/migration checks).
- Frontend regression: **262 passed** (257 existing + 5 session checks).
- Lesson content comparison: all **448 lesson entries, 5,572 reveal results and
  402 practice-bank entries** match the saved content baseline. The API schema
  intentionally changes; use `verify_runtime_parity.py --content-only`.
- Fresh SQLite migration and existing-schema adoption: tested, including a
  validated backup and preservation of an existing account/hash.
- Synthetic database lab: committed create/read/update/delete and cleanup passed.
- Offline Google/Apple flow: exercised real Authlib OIDC validation with a signed
  test token and mocked provider transport. Wrong state, signature, issuer,
  audience, nonce, expiry and unverified email are rejected. Apple POST callback,
  one-time onboarding, CSRF protection, returning identity, existing-email
  collision, renewal and logout revocation were checked.
- Frontend checks cover per-tab renewal, absence of persistent access JWTs in
  localStorage after migration, deduplicated renewal, temporary failure handling
  and safe destination validation. Existing curriculum/whiteboard/practice checks
  continue to pass.

Limits: no live Google or Apple credential/consent test; no PostgreSQL migration
or load test; no executed Windows PowerShell test; no manual browser visual/audio
acceptance. Chromium was blocked by the environment's process socket restriction
in the preceding UI verification attempt. The PowerShell launcher and responsive
layout therefore need the user's local acceptance test. Three installed-library
deprecation warnings remain; they did not fail the suite.

This does not complete password recovery, email verification, guardian consent,
customer account deletion/export, abuse throttling or production security review.
Those gates are recorded in DATABASE_AND_RELEASE_PLAN.md. Keep main unchanged
until local/staging acceptance and review are complete.
