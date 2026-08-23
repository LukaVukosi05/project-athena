"""
services/math_verification.py — checks AI-generated maths is correct
before it ever reaches a learner.

Responsibilities when implemented:
  - verify_step(before_expr, operation, after_expr) -> bool/diagnostic,
    using a symbolic math library (e.g. SymPy) to confirm each step
    in an AI-produced teaching plan is actually mathematically valid
    — this is the "Math verification" stage in the Phase 4 pipeline:
    AI Gateway -> Model -> Structured response -> Math verification
    -> Teaching response.
  - This exists because brief section 61 says: "A learner who asks
    200 AI questions but learns nothing is a failure" — an
    unverified but confident-sounding wrong step is worse than no
    answer at all.

# TODO (Phase 4, built and benchmarked independently before being
# wired into ai_tutor.py, per the brief's engineering principle of
# never integrating an unfamiliar tool directly into production)
"""
