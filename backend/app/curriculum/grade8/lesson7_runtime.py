"""Runtime conversion of the approved Grade 8 Lesson 7 Gold Pack.

The checked-in JSON is produced by ``tools/extract_grade8_lesson7.py``.  The
production application reads that deterministic artefact; it never parses the
DOCX during a request.
"""

from __future__ import annotations

import json
from pathlib import Path

from app.curriculum.schemas import (
    AccessLevel,
    ContentStatus,
    Lesson,
    LessonBlock,
    MathematicalOperation,
    SemanticObject,
    StepExplanation,
    TeachingStep,
    TimelineEvent,
    VisualizationInstruction,
    VisualizationState,
    WhiteboardBlock,
    WhiteboardQuestion,
)
from app.curriculum.grade8.bracket_timelines import STAGES

DATA_PATH = Path(__file__).with_name("generated") / "lesson_07.json"
SOURCE_DATA = json.loads(DATA_PATH.read_text(encoding="utf-8"))
SOURCE = SOURCE_DATA["source_document"]
SOURCE_SHA256 = SOURCE_DATA["source_sha256"]

RENDERER_TEMPLATES = frozenset(
    item["renderer"] for item in SOURCE_DATA["worked_examples"]
)

SEMANTIC_ANIMATION_OPERATIONS = frozenset({
    "focus_object", "evaluate_expression", "introduce_inverse",
    "apply_to_both_sides", "cancel_inverse_pair", "simplify_expression",
    "substitute_value", "replace_unknown", "reverse_equality",
    "compare_both_sides", "tilt_balance", "restore_balance",
    "mark_incorrect_step", "repair_incorrect_step", "verify_original",
    "show_conclusion", "distribute_to_each_term",
})


def _parameters(item: dict) -> dict:
    """Keep the exact author data while giving every renderer its own values."""
    return {
        "prompt": item["prompt"],
        "source_data": item["question_data"],
        "initial_state": item["initial_state"],
        "family": item["renderer"].split(":", 1)[1],
        "question_id": item["id"],
        "total_steps":len(STAGES[item["number"]]),
    }


def _board(item: dict) -> WhiteboardBlock:
    family = {"bracket_balance":"bracket_balance_native", "distributive_equation":"bracket_distribution_native",
              "factorised_comparison":"bracket_paths_native", "area_model_equation":"bracket_area_native",
              "context_to_equation":"bracket_rectangle_native"}[item["renderer"].split(":", 1)[1]]
    original = item["prompt"]
    plan = []
    for index, (working, after) in enumerate(STAGES[item["number"]]):
        narration = f"{working}. This produces {after}."
        prior = original if index == 0 else STAGES[item["number"]][index - 1][1]
        lowered = working.lower()
        action = ("verify_solution" if index == len(STAGES[item["number"]]) - 1 else
                  "transform_expression" if "distribute" in lowered or "multiply the two negative" in lowered or "take half" in lowered or "take two thirds" in lowered else
                  "diagnose_error" if "learner's first line" in lowered else
                  "divide_both_sides" if "divide" in lowered or "÷" in lowered else
                  "multiply_both_sides" if "multiply" in lowered or "reciprocal" in lowered else
                  "remove_from_both_sides" if "subtract" in lowered else
                  "add_to_both_sides" if "add" in lowered and "both" in lowered else
                  "form_equation" if "let " in lowered or "form" in lowered else
                  "evaluate_expression")
        plan.append({"before":prior,"working":working,"after":after,"narration":narration,
                     "target":"verification" if action == "verify_solution" else "result",
                     "action":action,"internal_instruction":item["teaching_sequence"][min(index,len(item["teaching_sequence"])-1)]})
    terminal = {"answer_state":item["answer"]}
    semantic_objects = [
        SemanticObject(id="problem", type="label", value=item["prompt"], group="question"),
        SemanticObject(id="factor", type="term", value="outside multiplier", group="bracket"),
        SemanticObject(id="term-1", type="term", value="first bracket term", group="bracket"),
        SemanticObject(id="term-2", type="term", value="second bracket term", group="bracket"),
        SemanticObject(id="left-expression", type="term", value="left-hand mathematical expression", group="equation"),
        SemanticObject(id="right-expression", type="term", value="right-hand mathematical expression", group="equation"),
        SemanticObject(id="variable-slot", type="token", value="unknown or substituted value", group="equation"),
        SemanticObject(id="balance-beam", type="result", value="equality balance", group="model"),
        SemanticObject(id="context", type="label", value="context quantities", group="model"),
        SemanticObject(id="operation", type="operation", value="current legal operation", group="working"),
        SemanticObject(id="result", type="result", value="current mathematical result", group="working"),
        SemanticObject(id="verification", type="verification", value=item["verification"], group="check"),
        SemanticObject(id="inverse-operation", type="operation", value="inverse operation introduced before it acts", group="working"),
        SemanticObject(id="left-operation", type="operation", value="operation applied to the complete left side", group="working"),
        SemanticObject(id="right-operation", type="operation", value="operation applied to the complete right side", group="working"),
        SemanticObject(id="cancellation", type="operation", value="inverse pair cancellation", group="working"),
        SemanticObject(id="substitution-slot", type="token", value="value substituted for the unknown", group="working"),
        SemanticObject(id="balance-left-pan", type="result", value="current left-side balance value", group="model"),
        SemanticObject(id="balance-right-pan", type="result", value="current right-side balance value", group="model"),
        SemanticObject(id="conclusion", type="result", value="verified mathematical conclusion", group="check"),
    ]
    steps: list[TeachingStep] = []
    for index, teaching in enumerate(plan):
        narration = teaching["narration"]
        target = teaching["target"]
        is_verification = index == len(plan) - 1
        contains_answer = str(terminal["answer_state"]).casefold() in teaching["after"].casefold()
        phase = "verification" if is_verification else "explicit_answer" if contains_answer else "operation"
        duration = max(3_600, len(narration.split()) * 380)
        operation_at = max(900, duration // 4)
        result_at = max(operation_at + 900, duration * 3 // 5)
        action_at = operation_at + max(300, (result_at - operation_at) // 2)
        action = teaching["action"]
        detail_events: list[TimelineEvent] = []
        detail_at = action_at
        if action in {"multiply_both_sides", "divide_both_sides", "add_to_both_sides", "remove_from_both_sides"}:
            mathematical_event = TimelineEvent(at_ms=action_at, type="apply_both_sides", targets=["left-expression", "right-expression"], style="operation")
            detail_events = [
                TimelineEvent(at_ms=max(operation_at + 100, action_at - 180), type="introduce_inverse", targets=["inverse-operation"], label=teaching["working"], style="operation"),
                TimelineEvent(at_ms=detail_at, type="apply_to_both_sides", targets=["left-operation", "right-operation"], style="operation"),
            ]
            if action in {"divide_both_sides", "multiply_both_sides", "add_to_both_sides", "remove_from_both_sides"}:
                detail_events.append(TimelineEvent(at_ms=min(result_at - 100, action_at + 180), type="cancel_inverse_pair", targets=["cancellation"], style="operation"))
        elif action == "substitute_value":
            mathematical_event = TimelineEvent(at_ms=action_at, type="substitute", targets=["variable-slot"], style="operation")
            detail_events = [
                TimelineEvent(at_ms=action_at, type="substitute_value", targets=["variable-slot"], style="operation"),
                TimelineEvent(at_ms=min(result_at - 100, action_at + 180), type="replace_unknown", targets=["substitution-slot"], style="operation"),
            ]
        elif action == "balance_scale":
            mathematical_event = TimelineEvent(at_ms=action_at, type="compare", targets=["balance-beam"], style="matching_pattern")
            detail_events = [
                TimelineEvent(at_ms=action_at, type="compare_both_sides", targets=["balance-left-pan", "balance-right-pan"], style="matching_pattern"),
                TimelineEvent(at_ms=min(result_at - 100, action_at + 180), type="restore_balance", targets=["balance-beam"], style="matching_pattern"),
            ]
        elif action == "verify_solution":
            mathematical_event = TimelineEvent(at_ms=action_at, type="compare", targets=["left-expression", "right-expression"], style="verification")
            detail_events = [TimelineEvent(at_ms=action_at, type="verify_original", targets=["problem", "verification"], style="verification")]
        elif action == "diagnose_error":
            mathematical_event = TimelineEvent(at_ms=action_at, type="simplify", targets=[target], style="operation")
            detail_events = [
                TimelineEvent(at_ms=action_at, type="mark_incorrect_step", targets=[target], style="operation"),
                TimelineEvent(at_ms=min(result_at - 100, action_at + 180), type="tilt_balance", targets=["balance-beam"], style="operation"),
            ]
        elif action == "compare_values":
            mathematical_event = TimelineEvent(at_ms=action_at, type="compare", targets=["left-expression", "right-expression"], style="matching_pattern")
            balance_event = "tilt_balance" if "≠" in teaching["after"] else "restore_balance"
            detail_events = [
                TimelineEvent(at_ms=action_at, type="compare_both_sides", targets=["balance-left-pan", "balance-right-pan"], style="matching_pattern"),
                TimelineEvent(at_ms=min(result_at - 100, action_at + 180), type=balance_event, targets=["balance-beam"], style="matching_pattern"),
            ]
        elif action == "transform_expression" and "reverse" in teaching["working"].casefold():
            mathematical_event = TimelineEvent(at_ms=action_at, type="simplify", targets=[target], style="operation")
            detail_events = [TimelineEvent(at_ms=action_at, type="reverse_equality", targets=["left-expression", "right-expression"], style="operation")]
        elif action == "transform_expression" and ("distribute" in lowered or "multiply the two negative" in lowered or "take half" in lowered or "take two thirds" in lowered):
            arrow_target = "term-2" if "negative factors" in lowered or "on the right" in lowered else "term-1"
            mathematical_event = TimelineEvent(at_ms=action_at, type="draw_arrow", from_target="factor", to_target=arrow_target, targets=["factor", arrow_target], style="operation")
            detail_events = [TimelineEvent(at_ms=min(result_at - 100, action_at + 180), type="evaluate_expression", targets=[target], style="operation")]
        elif action == "evaluate_expression":
            mathematical_event = TimelineEvent(at_ms=action_at, type="simplify", targets=[target], style="operation")
            detail_events = [TimelineEvent(at_ms=action_at, type="evaluate_expression", targets=[target], style="operation")]
        else:
            mathematical_event = TimelineEvent(at_ms=action_at, type="simplify", targets=[target], style="operation")
            detail_events = [TimelineEvent(at_ms=action_at, type="simplify_expression", targets=[target], style="operation")]
        events = [
            TimelineEvent(at_ms=0, type="caption", text=narration),
            TimelineEvent(at_ms=0, type="narration", text=narration),
            TimelineEvent(at_ms=350, type="focus", targets=[target], style="target"),
            TimelineEvent(at_ms=350, type="focus_object", targets=[target], style="target"),
            TimelineEvent(at_ms=operation_at, type="show_operation", targets=["operation"], label=teaching["working"], style="operation"),
            mathematical_event,
            *detail_events,
            TimelineEvent(at_ms=result_at, type="reveal", targets=["result"], style="result"),
        ]
        if contains_answer and not is_verification:
            events.append(TimelineEvent(at_ms=min(duration, result_at + 200), type="show_conclusion", targets=["conclusion"], style="result"))
        if teaching["action"] == "verify_solution":
            verify_at = max(result_at + 700, duration * 4 // 5)
            events.extend([
                TimelineEvent(at_ms=verify_at, type="verify", targets=["verification"], text=narration, style="verification"),
                TimelineEvent(at_ms=min(duration, verify_at + 100), type="show_conclusion", targets=["conclusion"], style="verification"),
            ])
        events.sort(key=lambda event: event.at_ms)
        steps.append(TeachingStep(
            id=f"{item['id']}-step-{index + 1:02}",
            step_number=index,
            title=f"Mathematical step {index + 1}",
            before_expression=teaching["before"],
            working_expression=teaching["working"],
            operation=MathematicalOperation(type=f"{family}_step", value=teaching["working"], action=teaching["action"]),
            after_expression=teaching["after"],
            explanation=StepExplanation(
                what=narration,
                why=narration,
                purpose=f"Use {teaching['action'].replace('_', ' ')} to preserve or test equality.",
                remember="A legal equation step must preserve equality or test it against the original equation.",
            ),
            animation_template=family,
            screen_reader_description=f"{teaching['before']}. {narration} Result: {teaching['after']}.",
            visualization_state=VisualizationState(
                objects=[item.id for item in semantic_objects],
                highlights=[target],
                annotations=[f"stage:{index + 1}", f"action:{teaching['action']}", f"phase:{phase}"],
                target=target,
                before_state=teaching["before"],
                working_state=teaching["working"],
                after_state=teaching["after"],
            ),
            instructional_goal=narration,
            duration_ms=duration,
            events=events,
            narration=narration,
            state_after={
                "stage": index + 1,
                "question_id": item["id"],
                "operation": teaching["action"],
                "target": target,
                "phase": phase,
                "terminal_answer": contains_answer,
                "verification_complete": is_verification,
                "verification_link": item["verification"],
                "scheduled_start_ms": 0,
                "minimum_duration_ms": duration,
                "completion_state": teaching["after"],
            },
            internal_instruction=teaching["internal_instruction"],
        ))
    return WhiteboardBlock(
        id=f"{item['id']}-board",
        representation="visual",
        problem=item["prompt"],
        initial_expression=plan[0]["before"],
        steps=steps,
        visualization=VisualizationInstruction(type="algebra", template=family, parameters=_parameters(item)),
        semantic_objects=semantic_objects,
    )


def _question(item: dict) -> WhiteboardQuestion:
    difficulty = "advanced" if item["difficulty"] == "challenge" else item["difficulty"]
    return WhiteboardQuestion(
        id=item["id"],
        order=item["number"],
        difficulty=difficulty,
        is_core_example=item["number"] == 1,
        guidance_level="high" if item["number"] <= 5 else "moderate" if item["number"] <= 10 else "reduced",
        whiteboard=_board(item),
        cognitive_level=item["cognitive_level"],
        marks=item["marks"],
        answer=item["answer"],
        full_memo=item["memo"],
        misconception_tags=item["misconception_tags"],
        expected_evidence=item["verification"],
    )


WHITEBOARD_QUESTIONS = [_question(item) for item in SOURCE_DATA["worked_examples"]]

LESSON_7 = Lesson(
    id=SOURCE_DATA["id"],
    order=7,
    title=SOURCE_DATA["title"],
    objective=SOURCE_DATA["objective"],
    why_it_matters=SOURCE_DATA["why_it_matters"],
    intuition="\n".join(SOURCE_DATA["concept_teaching"]),
    prerequisites=SOURCE_DATA["prerequisites"],
    estimated_minutes=SOURCE_DATA["estimated_minutes"],
    difficulty="exam",
    access_level=AccessLevel.PREMIUM,
    status=ContentStatus.PUBLISHED,
    blocks=[
        LessonBlock(
            type="concept",
            title="Concept teaching",
            content="\n".join(SOURCE_DATA["concept_teaching"]),
        ),
        LessonBlock(
            type="memory_tip",
            title="Vocabulary",
            content="\n".join(f"{item['term']}: {item['meaning']}" for item in SOURCE_DATA["vocabulary"]),
        ),
        LessonBlock(
            type="checkpoint",
            title="Entry diagnostic",
            content=SOURCE_DATA["entry_diagnostic"]["prompt"],
            data={"answer_gate": "server_submission_required"},
        ),
        WHITEBOARD_QUESTIONS[0].whiteboard,
        LessonBlock(
            type="mistake",
            title="Misconception diagnosis and targeted repair",
            content="\n".join(
                f"{item['tag']}: {item['diagnosis']} {item['repair']}"
                for item in SOURCE_DATA["misconceptions"]
            ),
            data={"misconceptions": SOURCE_DATA["misconceptions"]},
        ),
        LessonBlock(
            type="practice",
            title="Independent practice",
            content="Attempt independently, submit, then use the server-authoritative diagnosis and worked review.",
            data={"practice_bank_id": SOURCE_DATA["id"]},
        ),
        LessonBlock(type="summary", title="Lesson summary", content="\n".join(SOURCE_DATA["summary"])),
    ],
    whiteboard_questions=WHITEBOARD_QUESTIONS,
    mastery_threshold=SOURCE_DATA["mastery_threshold"],
    paper=None,
    source_document=SOURCE,
    source_sha256=SOURCE_SHA256,
    release_approved=True,
    assessment_contract={
        "worked_example_count": 15,
        "practice_count": 15,
        "mastery_question_count": 5,
        "parallel_reassessment_count": 3,
        "answer_hidden_before_submission": True,
        "progression_threshold": SOURCE_DATA["mastery_threshold"],
        "runtime_conversion": "lesson_7_bracket_equations",
    },
)
