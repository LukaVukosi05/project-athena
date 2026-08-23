"""
api/v1/ai_tutor.py — the AI Tutor chat/interaction endpoint (Phase 4).

NOT built until Phases 1–3 (frontend, learning engine, animation
engine) are working and validated, per the brief's phased plan.

Endpoints to implement:

  POST /api/v1/ai-tutor/ask
    body: { lesson_id, question, mode }
    mode is one of: "explain" | "hint" | "show_me" | "practice" | "test_me"
    (brief section 21 — the tutor must never default to just
    answering; each mode has a distinct, constrained behaviour)

    Flow (brief section 18):
      AI Reasoning -> Structured Teaching Plan -> Animation
      Instruction -> app/services/animation_service.py validates
      the instruction against the known TEMPLATES registry (the
      same names as frontend/js/engine/animation-engine.js's
      TEMPLATES object) -> app/services/math_verification.py
      checks the maths is actually correct -> response returned
      to the frontend

    The AI must NEVER be allowed to emit arbitrary rendering code —
    only a template name + step values from the fixed registry.
    This endpoint is the enforcement point for that rule.

  POST /api/v1/ai-tutor/scan  (OCR upload, later in Phase 4)
    body: multipart image upload of a handwritten/printed problem
    -> passes to an OCR service, then the same reasoning pipeline

# TODO (Phase 4 — do not build before Phases 1-3 are validated)
"""
