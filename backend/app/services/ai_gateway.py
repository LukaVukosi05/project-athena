"""
services/ai_gateway.py — abstraction over the underlying AI model(s).

Responsibilities when implemented (brief section 64's learning
sequence: run locally -> call via API -> wrap in FastAPI -> add an
abstraction layer):
  - A single `ask(prompt, mode, context) -> StructuredResponse`
    function/class that api/v1/ai_tutor.py calls, so swapping the
    underlying model (open-source vs a premium API fallback) never
    touches the API layer.
  - Enforces the "AI should have multiple modes" rule from the
    brief (explain / hint / show_me / practice / test_me) at the
    prompt-construction level, not just trusting the model to
    behave.
  - Returns a structured teaching plan (not raw prose) that
    animation_service.py can validate and turn into an animation
    instruction.

# TODO (Phase 4). Per brief section 65, prototype this in a
# standalone script first — "experiment -> proof of concept ->
# benchmark -> wrapper/service -> automated tests -> production
# integration" — before wiring it into any endpoint.
"""
