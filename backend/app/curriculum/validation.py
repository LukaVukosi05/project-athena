"""Aggregate curriculum validation that reports every discovered failure."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import re

from app.curriculum.content_manifest import EXPLICITLY_RELEASED_LESSON_IDS, ReadinessState, readiness_for
from app.curriculum.schemas import GradeCurriculum
from app.visualization.registry import validate_visualization
from app.whiteboard.validation import validate_whiteboard


def _contains_in_order(states: list[str], required: list[str]) -> tuple[bool, str | None]:
    """Check mathematical stages in order, without treating HTML difference as proof."""
    cursor = 0
    for required_state in required:
        needle = required_state.casefold()
        while cursor < len(states) and needle not in states[cursor].casefold():
            cursor += 1
        if cursor == len(states):
            return False, required_state
        cursor += 1
    return True, None


def _verification_is_true(value: str) -> bool:
    """Evaluate the numeric equality asserted by a terminal verification state."""
    text = value.replace("R", "").replace("Checked:", "").replace(",", ".")
    matches = re.findall(r"(?<![\w.])(\d+(?:\.\d+)?)\s*=\s*(\d+(?:\.\d+)?)(?![\w.])", text)
    return bool(matches) and all(abs(float(left) - float(right)) < 1e-9 for left, right in matches)


@dataclass(frozen=True)
class ValidationFailure:
    grade_id: str
    topic_id: str
    lesson_id: str
    question_id: str
    step_id: str
    failure_reason: str

    def model_dump(self) -> dict[str, str]:
        return asdict(self)


def validate_curriculum(grades: list[GradeCurriculum]) -> list[ValidationFailure]:
    failures: list[ValidationFailure] = []

    def fail(grade_id: str, topic_id: str, lesson_id: str = "-", question_id: str = "-", step_id: str = "-", reason: str = "invalid") -> None:
        failures.append(ValidationFailure(grade_id, topic_id, lesson_id, question_id, step_id, reason))

    lesson_ids: set[str] = set()
    for grade in grades:
        for topic in grade.topics:
            seen_orders: set[int] = set()
            for subtopic in topic.subtopics:
                for lesson in subtopic.lessons:
                    context = (grade.id, topic.id, lesson.id)
                    if lesson.id in lesson_ids:
                        fail(*context, reason="duplicate stable lesson ID")
                    lesson_ids.add(lesson.id)
                    if lesson.order in seen_orders:
                        fail(*context, reason="duplicate lesson order within topic")
                    seen_orders.add(lesson.order)
                    state = readiness_for(lesson)
                    if lesson.status.value == "published" and not (lesson.release_approved or lesson.id in EXPLICITLY_RELEASED_LESSON_IDS):
                        fail(*context, reason="published lesson lacks an explicit release decision")
                    if state == ReadinessState.PUBLISHED and not lesson.blocks:
                        fail(*context, reason="published lesson has no teaching content")
                    if state in {ReadinessState.VERIFIED, ReadinessState.PUBLISHED} and not lesson.whiteboard_questions:
                        fail(*context, reason="usable teaching lesson has no questions")
                    if lesson.release_approved:
                        required_blocks = {"concept", "mistake", "practice", "summary"}
                        block_types = {block.type for block in lesson.blocks}
                        if not required_blocks.issubset(block_types):
                            fail(*context, reason=f"release gate missing teaching blocks: {sorted(required_blocks - block_types)}")
                        contract = lesson.assessment_contract
                        expected = {
                            "worked_example_count": len(lesson.whiteboard_questions),
                            "practice_count": 15,
                            "mastery_question_count": 5,
                            "parallel_reassessment_count": 3,
                        }
                        for key, count in expected.items():
                            if contract.get(key) != count:
                                fail(*context, reason=f"release gate {key} must equal {count}")
                        if contract.get("progression_threshold") != .8:
                            fail(*context, reason="release gate progression threshold must be 80%")
                        if contract.get("answer_hidden_before_submission") is not True:
                            fail(*context, reason="release gate requires hidden initial answers")
                        if lesson.id == "g8-algebraic-equations-01":
                            from app.curriculum.grade8.assessment import MASTERY_BANK, MISCONCEPTION_REPAIRS, PRACTICE_BANK, REASSESSMENT_BANK
                            if len(PRACTICE_BANK) != 15 or len(MASTERY_BANK) != 5 or len(REASSESSMENT_BANK) != 3:
                                fail(*context, reason="release gate assessment bank counts are incomplete")
                            if not MISCONCEPTION_REPAIRS:
                                fail(*context, reason="release gate has no targeted repair routes")
                        if lesson.id == "g8-algebraic-equations-02":
                            from app.curriculum.grade8 import assessment_lesson2 as bank
                            if len(bank.PRACTICE_BANK) != 15 or len(bank.MASTERY_BANK) != 5 or len(bank.REASSESSMENT_BANK) != 3:
                                fail(*context, reason="release gate Lesson 2 assessment banks incomplete")
                            if not bank.MISCONCEPTION_REPAIRS:
                                fail(*context, reason="release gate Lesson 2 has no targeted repair routes")
                        if lesson.id == "g8-algebraic-equations-03":
                            from app.curriculum.grade8 import assessment_lesson3 as bank
                            if len(bank.PRACTICE_BANK) != 15 or len(bank.MASTERY_BANK) != 5 or len(bank.REASSESSMENT_BANK) != 3:
                                fail(*context, reason="release gate Lesson 3 assessment banks incomplete")
                            if not bank.MISCONCEPTION_REPAIRS:
                                fail(*context, reason="release gate Lesson 3 has no targeted repair routes")
                    signatures: set[tuple[str, str, str, str]] = set()
                    for question in lesson.whiteboard_questions:
                        board = question.whiteboard
                        qcontext = (*context, question.id)
                        if not board.visualization:
                            fail(*qcontext, reason="whiteboard question has no visualization template")
                        if not board.semantic_objects:
                            fail(*qcontext, reason="whiteboard question has no semantic objects")
                        object_ids = [item.id for item in board.semantic_objects]
                        if len(object_ids) != len(set(object_ids)):
                            fail(*qcontext, reason="duplicate semantic object IDs")
                        try:
                            validate_whiteboard(board)
                        except (TypeError, ValueError) as error:
                            fail(*qcontext, reason=f"whiteboard contract: {error}")
                        if board.visualization:
                            try:
                                validate_visualization(board)
                            except (TypeError, ValueError) as error:
                                fail(*qcontext, reason=f"visualization parameters: {error}")
                        signature = (
                            board.problem.strip(),
                            (question.answer or "").strip(),
                            board.visualization.template if board.visualization else "",
                            repr(sorted((board.visualization.parameters if board.visualization else {}).items())),
                        )
                        if signature in signatures:
                            fail(*qcontext, reason="non-progressive example bank duplicates an operation signature")
                        signatures.add(signature)
                        if not any(step.events for step in board.steps):
                            fail(*qcontext, reason="whiteboard question has no timeline events")
                        for step in board.steps:
                            step_id = step.id or str(step.step_number)
                            if not any((step.before_expression.strip(), (step.working_expression or "").strip(), step.after_expression.strip())):
                                fail(*qcontext, step_id, reason="empty mathematical stage")
                            if step.events:
                                narration = " ".join(event.text for event in step.events if event.type == "narration" and event.text)
                                captions = " ".join(event.text for event in step.events if event.type == "caption" and event.text)
                                if not narration:
                                    fail(*qcontext, step_id, reason="teaching event narration is missing")
                                if not captions:
                                    fail(*qcontext, step_id, reason="teaching event caption is missing")
                                if narration != captions:
                                    fail(*qcontext, step_id, reason="caption and narration mismatch")
                                if step.internal_instruction and narration.strip().casefold() == step.internal_instruction.strip().casefold():
                                    fail(*qcontext, step_id, reason="learner narration duplicates the internal authoring instruction")
                                command_only = re.fullmatch(r"\s*(reveal|highlight|display|show|place|animate|move|reset|return)\b[^.?!]*[.?!]?\s*", narration, re.I)
                                if command_only:
                                    fail(*qcontext, step_id, reason="learner narration consists only of a renderer command")
                                if step.before_expression.strip() == step.after_expression.strip():
                                    fail(*qcontext, step_id, reason="teaching step has no visible mathematical state change")
                                if not step.working_expression or step.working_expression.strip() in {step.before_expression.strip(), step.after_expression.strip()}:
                                    fail(*qcontext, step_id, reason="mathematical operation has no distinct visible working state")
                                known = set(object_ids)
                                targets = {target for event in step.events for target in [*event.targets, event.from_target, event.to_target] if target}
                                if targets - known:
                                    fail(*qcontext, step_id, reason=f"missing event targets: {sorted(targets - known)}")
                                active_target = step.visualization_state.target if step.visualization_state else None
                                if not active_target or active_target not in known:
                                    fail(*qcontext, step_id, reason="teaching step has no real active semantic target")
                                focus_times = [event.at_ms for event in step.events if event.type == "focus" and active_target in event.targets]
                                operation_times = [event.at_ms for event in step.events if event.type == "show_operation"]
                                action_times = [event.at_ms for event in step.events if event.type in {
                                    "apply_both_sides", "substitute", "compare", "simplify",
                                    "evaluate_expression", "introduce_inverse", "apply_to_both_sides", "cancel_inverse_pair",
                                    "simplify_expression", "substitute_value", "replace_unknown",
                                    "reverse_equality", "compare_both_sides", "tilt_balance",
                                    "restore_balance", "mark_incorrect_step", "repair_incorrect_step",
                                    "verify_original", "show_conclusion",
                                }]
                                result_times = [event.at_ms for event in step.events if event.type in {"reveal", "replace", "simplify"} and "result" in event.targets]
                                if not focus_times:
                                    fail(*qcontext, step_id, reason="active mathematical target is never focused")
                                if not operation_times or not result_times:
                                    fail(*qcontext, step_id, reason="operation has no visible result event")
                                elif min(operation_times) >= min(result_times):
                                    fail(*qcontext, step_id, reason="result appears before its mathematical operation")
                                if question.id.startswith("g8-ae-l01-w") and (not action_times or (operation_times and result_times and not min(operation_times) < min(action_times) < min(result_times))):
                                    fail(*qcontext, step_id, reason="mathematical operation does not visibly act before its result")
                                if step.operation.action == "verify_solution":
                                    verification_events = [event for event in step.events if event.type == "verify" and "verification" in event.targets]
                                    if not verification_events or step.state_after.get("verification_link") != question.expected_evidence:
                                        fail(*qcontext, step_id, reason="verification is unrelated to the original question")
                        if question.id.startswith("g8-ae-l01-w"):
                            from app.curriculum.grade8.teaching_timelines import TERMINAL_CONTRACTS

                            contract = TERMINAL_CONTRACTS.get(question.id)
                            terminal_step = board.steps[-1]
                            terminal_id = terminal_step.id or str(terminal_step.step_number)
                            if contract is None:
                                fail(*qcontext, terminal_id, reason="terminal-answer contract is missing")
                                continue
                            if question.answer != contract["approved_answer"]:
                                fail(*qcontext, terminal_id, reason="explicit final answer disagrees with the approved answer")
                            states = [board.initial_expression]
                            for authored_step in board.steps:
                                states.extend([authored_step.working_expression or "", authored_step.after_expression])
                            answer_state = str(contract["answer_state"])
                            answer_steps = [
                                authored_step for authored_step in board.steps
                                if answer_state.casefold() in authored_step.after_expression.casefold()
                            ]
                            if not answer_steps:
                                fail(*qcontext, terminal_id, reason="timeline lacks an explicit final-answer state")
                            if answer_state.casefold() in board.initial_expression.casefold():
                                fail(*qcontext, terminal_id, reason="final answer appears in the initial state")
                            if "□" in board.problem and not any(re.search(r"(?:□\s*=\s*-?\d|\d\s*=\s*□)", step.after_expression) for step in board.steps):
                                fail(*qcontext, terminal_id, reason="requested box remains unresolved in the final-answer state")
                            ordered, missing_state = _contains_in_order(states, list(contract["required_states"]))
                            if not ordered:
                                fail(*qcontext, terminal_id, reason=f"timeline skips required simplification: {missing_state}")
                            if terminal_step.operation.action != "verify_solution" or terminal_step.state_after.get("verification_complete") is not True:
                                fail(*qcontext, terminal_id, reason="timeline lacks terminal verification against the original question")
                            verification_state = str(contract["verification_state"])
                            terminal_math = f"{terminal_step.working_expression} {terminal_step.after_expression}"
                            if verification_state.casefold() not in terminal_math.casefold():
                                fail(*qcontext, terminal_id, reason="verification does not use the derived answer")
                            if not _verification_is_true(verification_state):
                                fail(*qcontext, terminal_id, reason="terminal verification is mathematically false")
                            if question.id == "g8-ae-l01-w01" and not {"12 = 9 + 3", "12 = 12"}.issubset(set(states)):
                                fail(*qcontext, terminal_id, reason="true-or-false equality does not evaluate both sides")
                            if question.id in {"g8-ae-l01-w05", "g8-ae-l01-w10"}:
                                joined = " ".join(states)
                                required_repair = "8 − 3 = 8 − 3" if question.id.endswith("w05") else "3x = 15"
                                if required_repair not in joined:
                                    fail(*qcontext, terminal_id, reason="misconception is diagnosed without a repaired valid method")
    return failures
