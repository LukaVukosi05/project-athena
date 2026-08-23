"""
services/animation_service.py — server-side animation instruction
validator/producer (Phase 3–4).

This is the backend half of the architecture described in the
brief and mirrored in frontend/js/engine/animation-engine.js:

  AI Reasoning -> Structured Teaching Plan -> Animation Instruction
  -> Pre-built Animation Template -> Rendered Lesson

Responsibilities when implemented:
  - Keep a server-side registry of valid template names that must
    stay in lockstep with the TEMPLATES object in
    frontend/js/engine/animation-engine.js (e.g.
    "linear_equation_balance", "tangent_line") — adding a template
    means updating both places deliberately, never independently.
  - validate_instruction(instruction: dict) -> raises if the AI (or
    curriculum author) produced a step referencing an unknown
    template, an unknown "op", or malformed values. This is the
    safety boundary described in the brief: "This is dramatically
    safer than allowing an LLM to directly control arbitrary
    frontend code."
  - For curated (non-AI) lessons, this is also where curriculum
    authors' animation_spec JSON (see db/models/curriculum.py) gets
    validated before being saved.

# TODO (Phase 3, once the animation template library has more than
# the two demo templates currently in the frontend)
"""
