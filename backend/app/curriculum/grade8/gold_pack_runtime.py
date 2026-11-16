"""Shared conversion helpers for Grade 8 algebraic-equation Gold Packs.

Lesson modules retain their own authored timelines and mathematical board logic.
Only common question metadata and renderer parameters are constructed here.
"""

from app.curriculum.schemas import WhiteboardBlock, WhiteboardQuestion

SEMANTIC_ANIMATION_OPERATIONS = frozenset(
    {
        "focus_object",
        "evaluate_expression",
        "introduce_inverse",
        "apply_to_both_sides",
        "cancel_inverse_pair",
        "simplify_expression",
        "substitute_value",
        "replace_unknown",
        "reverse_equality",
        "compare_both_sides",
        "tilt_balance",
        "restore_balance",
        "mark_incorrect_step",
        "repair_incorrect_step",
        "verify_original",
        "show_conclusion",
    }
)


def visual_parameters(
    item: dict, *, total_steps: int | None = None, family: str | None = None
) -> dict:
    """Keep exact author data, with explicit lesson-specific step/family values."""
    parameters = {
        "prompt": item["prompt"],
        "source_data": item["question_data"],
        "initial_state": item["initial_state"],
        "family": item["renderer"].split(":", 1)[1] if family is None else family,
        "question_id": item["id"],
    }
    if total_steps is not None:
        parameters["total_steps"] = total_steps
    return parameters


def whiteboard_question(item: dict, board: WhiteboardBlock) -> WhiteboardQuestion:
    difficulty = "advanced" if item["difficulty"] == "challenge" else item["difficulty"]
    return WhiteboardQuestion(
        id=item["id"],
        order=item["number"],
        difficulty=difficulty,
        is_core_example=item["number"] == 1,
        guidance_level=(
            "high"
            if item["number"] <= 5
            else "moderate" if item["number"] <= 10 else "reduced"
        ),
        whiteboard=board,
        cognitive_level=item["cognitive_level"],
        marks=item["marks"],
        answer=item["answer"],
        full_memo=item["memo"],
        misconception_tags=item["misconception_tags"],
        expected_evidence=item["verification"],
    )
