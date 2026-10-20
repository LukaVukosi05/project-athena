import hashlib
import json
from pathlib import Path

from fastapi.testclient import TestClient

from app.curriculum.content_manifest import readiness_for
from app.curriculum.grade8.assessment import MASTERY_BANK, PRACTICE_BANK, QUESTION_VERIFICATIONS, REASSESSMENT_BANK, REPAIR_RULES
from app.curriculum.grade8.lesson1_runtime import LESSON_1, RENDERER_TEMPLATES, SEMANTIC_ANIMATION_OPERATIONS, SOURCE_DATA
from app.curriculum.grade8.teaching_timelines import COMMAND_WORDS, TEACHING_TIMELINES, TERMINAL_CONTRACTS
from app.curriculum.repository import curriculum_repository
from app.curriculum.validation import validate_curriculum
from app.curriculum.schemas import TimelineEvent
from app.main import app
from app.visualization.registry import CATALOGUE

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "docs/curriculum/grade8/algebraic-equations/Project_Athena_Grade8_Algebraic_Equations_Gold_Pack_v1_0.docx"
EXPECTED_HASH = "69b97ae1d9f85d0f9fb41aad170f6cbc777f2e39844dd6b8d6235bee6c093574"


def test_gold_pack_hash_and_exact_source_contract():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED_HASH
    assert SOURCE_DATA["id"] == "g8-algebraic-equations-01"
    banks = {
        "worked_examples": ("w", 15),
        "practice_questions": ("p", 15),
        "mastery_questions": ("m", 5),
        "reassessment_questions": ("r", 3),
    }
    all_ids = []
    for name, (kind, count) in banks.items():
        rows = SOURCE_DATA[name]
        ids = [item["id"] for item in rows]
        assert ids == [f"g8-ae-l01-{kind}{number:02}" for number in range(1, count + 1)]
        for current, following in zip(rows, rows[1:]):
            assert following["prompt"] not in current.get("solution", [])
        all_ids.extend(ids)
    assert len(all_ids) == len(set(all_ids))


def test_runtime_matches_source_and_release_gate():
    assert LESSON_1.title == SOURCE_DATA["title"]
    assert LESSON_1.objective == SOURCE_DATA["objective"]
    assert LESSON_1.why_it_matters == SOURCE_DATA["why_it_matters"]
    assert [item.id for item in LESSON_1.whiteboard_questions] == [item["id"] for item in SOURCE_DATA["worked_examples"]]
    assert [item.id for item in PRACTICE_BANK] == [item["id"] for item in SOURCE_DATA["practice_questions"]]
    assert [item.id for item in MASTERY_BANK] == [item["id"] for item in SOURCE_DATA["mastery_questions"]]
    assert [item.id for item in REASSESSMENT_BANK] == [item["id"] for item in SOURCE_DATA["reassessment_questions"]]
    assert LESSON_1.release_approved is True
    assert readiness_for(LESSON_1).value == "published"
    broken = LESSON_1.model_copy(update={"assessment_contract": {**LESSON_1.assessment_contract, "practice_count": 14}})
    assert readiness_for(broken).value == "authored"
    grade = curriculum_repository.get_grade("grade-8")
    lessons = grade.topics[0].subtopics[0].lessons
    assert len(lessons) == 10
    assert all(item.release_approved and item.status.value == "published" for item in lessons[:8])
    assert all(not item.release_approved and item.status.value == "coming_soon" for item in lessons[8:])
    assert not [failure for failure in validate_curriculum([grade]) if failure.lesson_id == LESSON_1.id]


def test_whiteboard_templates_targets_states_and_registry_parity():
    backend = {f"{kind}:{template}" for kind, template in CATALOGUE}
    frontend = set(json.loads((ROOT / "frontend/js/visualization/template-manifest.json").read_text(encoding="utf-8")))
    assert RENDERER_TEMPLATES == {
        "algebra:equality_balance", "algebra:additive_inverse", "algebra:multiplicative_inverse",
        "algebra:two_step_balance", "algebra:variables_both_sides", "algebra:context_to_equation",
        "algebra:distributive_equation",
    }
    assert RENDERER_TEMPLATES <= backend == frontend
    for question in LESSON_1.whiteboard_questions:
        board = question.whiteboard
        object_ids = {item.id for item in board.semantic_objects}
        assert board.steps[0].before_expression == board.initial_expression
        for step in board.steps:
            assert step.before_expression != step.after_expression
            assert [event.at_ms for event in step.events] == sorted(event.at_ms for event in step.events)
            targets = {target for event in step.events for target in event.targets}
            assert targets <= object_ids
            narration = " ".join(event.text for event in step.events if event.type == "narration")
            captions = " ".join(event.text for event in step.events if event.type == "caption")
            assert narration == captions


def test_all_fifteen_protected_whiteboard_contracts_are_stable():
    """Freeze approved mathematics and narration before presentation changes."""
    expected = {
        "g8-ae-l01-w01": "28d9eb5dcf989cbe3706999a010f11dd75824399c87db4a08dd3a8c38a44bb12",
        "g8-ae-l01-w02": "beb7c572ee21410dfc1477a75e4cd18ba7fbe0fec7edd2a746d35b8b2fcb6388",
        "g8-ae-l01-w03": "3d5940171210e3ec20d8733eab9cf021c668872b7329c9b7f03091a810f89095",
        "g8-ae-l01-w04": "d6c8669b3c1c2983f8263639d03e3906d7ed93d420f04d3451b25a01f6c2f342",
        "g8-ae-l01-w05": "d6fbb5491a8806ed10bcf935fb0391a5aafb15809fc4dff15e235f5b4b10da97",
        "g8-ae-l01-w06": "63bf768487d1b663aa0d7efa10964a2574d6dd1837e8fc0a5601b7b3361ded22",
        "g8-ae-l01-w07": "015fd611eaece65100b5d6d49f9cbef75f9ed2cff095d2b1de4eeb5bc93ca639",
        "g8-ae-l01-w08": "0ddfa133ca4a793716c79c1ce328c8d56adade7e2ebb14c9260b1cd9e0718455",
        "g8-ae-l01-w09": "e61af46f0bb1da6da694cc915a119f19ffef46ea39b484e19e24036406bed692",
        "g8-ae-l01-w10": "3cf195127628892793cc73e3be187efdd67e36546d1c47ce189a0f79fe2577c8",
        "g8-ae-l01-w11": "b649a648107543b8efee5c2103007b20db5cf1930303b698485d310647ebf708",
        "g8-ae-l01-w12": "a2ca0dafe51773e2df61d1fe3fd3b81ab7424fd91694da089517a233c1b03614",
        "g8-ae-l01-w13": "5459d728b2a343cb296ebdd71d2a67c50d9b7ee985461a4342818bab2314c4dc",
        "g8-ae-l01-w14": "cc5fdc7f38f712467c57c2a84d1b0a524cf3a80664d8559c17c6028384ae78d5",
        "g8-ae-l01-w15": "faa926979852f47ee48f55c541330c58646b2d8714c6b6eff9ffdf12c0718c14",
    }
    baseline_semantic_ids = {
        "problem", "left-expression", "right-expression", "variable-slot",
        "balance-beam", "context", "operation", "result", "verification",
    }
    observed = {}
    for question in LESSON_1.whiteboard_questions:
        board = question.whiteboard
        assert baseline_semantic_ids <= {item.id for item in board.semantic_objects}
        payload = {
            "question_id": question.id,
            "renderer_family": board.visualization.template,
            "timeline_step_ids": [step.id for step in board.steps],
            "initial_dom_state": board.initial_expression,
            "states": [
                [step.before_expression, step.working_expression, step.after_expression]
                for step in board.steps
            ],
            "final_answer": question.answer,
            "verification_state": board.steps[-1].after_expression,
            "captions": [
                [event.text for event in step.events if event.type == "caption"]
                for step in board.steps
            ],
            "narration": [step.narration for step in board.steps],
        }
        canonical = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
        observed[question.id] = hashlib.sha256(canonical.encode()).hexdigest()
    assert observed == expected


def test_all_fifteen_examples_have_supported_semantic_animation_sequences():
    frontend_controller = (ROOT / "frontend/js/whiteboard/timeline-controller.js").read_text(encoding="utf-8")
    event_types = {
        event.type
        for question in LESSON_1.whiteboard_questions
        for step in question.whiteboard.steps
        for event in step.events
    }
    used_semantic_operations = event_types & SEMANTIC_ANIMATION_OPERATIONS
    assert {
        "focus_object", "evaluate_expression", "introduce_inverse",
        "apply_to_both_sides", "cancel_inverse_pair", "substitute_value",
        "replace_unknown", "reverse_equality", "compare_both_sides",
        "tilt_balance", "restore_balance", "mark_incorrect_step",
        "repair_incorrect_step", "verify_original", "show_conclusion",
    } <= used_semantic_operations
    for operation in used_semantic_operations:
        assert f'event.type==="{operation}"' in frontend_controller or operation in {"focus_object"}
    for question in LESSON_1.whiteboard_questions:
        for step in question.whiteboard.steps:
            types = [event.type for event in step.events]
            assert "focus_object" in types
            assert types.index("show_operation") < types.index("reveal")
            assert any(event in used_semantic_operations for event in types)


def test_example_two_semantic_animation_matches_the_approved_reasoning_order():
    question = next(item for item in LESSON_1.whiteboard_questions if item.id == "g8-ae-l01-w02")
    operations = [[event.type for event in step.events] for step in question.whiteboard.steps]
    assert "evaluate_expression" in operations[0]
    assert all(name in operations[1] for name in ("introduce_inverse", "apply_to_both_sides", "cancel_inverse_pair"))
    assert "reverse_equality" in operations[2]
    assert all(name in operations[3] for name in ("substitute_value", "replace_unknown"))
    assert all(name in operations[4] for name in ("compare_both_sides", "restore_balance"))
    assert all(name in operations[5] for name in ("verify_original", "show_conclusion"))
    assert question.whiteboard.steps[-1].after_expression == "Checked: 13 = 13; therefore □ = 8"


def test_misconception_animation_breaks_then_repairs_the_balance():
    question = next(item for item in LESSON_1.whiteboard_questions if item.id == "g8-ae-l01-w05")
    event_types = [[event.type for event in step.events] for step in question.whiteboard.steps]
    assert "mark_incorrect_step" in event_types[0] and "tilt_balance" in event_types[0]
    assert "restore_balance" in event_types[1]
    assert "repair_incorrect_step" in event_types[2] and "apply_to_both_sides" in event_types[2]
    assert "verify_original" in event_types[-1]


def test_all_fifteen_examples_satisfy_learner_teaching_contract():
    number_words = {"2":"two", "3":"three", "4":"four", "5":"five", "6":"six", "6.5":"six comma five", "7":"seven", "8":"eight", "9":"nine", "10":"ten", "11":"eleven", "12":"twelve", "13":"thirteen", "18":"eighteen", "19":"nineteen", "21":"twenty-one", "28":"twenty-eight", "45":"forty-five"}
    assert set(TEACHING_TIMELINES) == {item["id"] for item in SOURCE_DATA["worked_examples"]}
    all_narration = []
    for source, question in zip(SOURCE_DATA["worked_examples"], LESSON_1.whiteboard_questions, strict=True):
        board = question.whiteboard
        assert len(board.steps) >= 5
        assert question.answer.casefold() not in board.initial_expression.casefold()
        source_numbers = set(__import__("re").findall(r"\d+(?:\.\d+)?", source["prompt"]))
        question_narration = " ".join(step.narration or "" for step in board.steps)
        assert any(value in question_narration or number_words.get(value, "") in question_narration.casefold() for value in source_numbers)
        for step in board.steps:
            assert step.internal_instruction
            assert step.internal_instruction not in (step.narration or "")
            assert step.internal_instruction not in " ".join(event.text or "" for event in step.events if event.type == "caption")
            assert "internal_instruction" not in step.model_dump()
            assert step.operation.action
            assert step.visualization_state.target in {item.id for item in board.semantic_objects}
            assert step.visualization_state.before_state == step.before_expression
            assert step.visualization_state.working_state == step.working_expression
            assert step.visualization_state.after_state == step.after_expression
            assert step.before_expression != step.after_expression
            assert step.working_expression not in {step.before_expression, step.after_expression}
            captions = [event.text for event in step.events if event.type == "caption"]
            narrations = [event.text for event in step.events if event.type == "narration"]
            assert captions == narrations == [step.narration]
            assert not any((step.narration or "").casefold().startswith(f"{word} ") for word in COMMAND_WORDS)
            operation_at = min(event.at_ms for event in step.events if event.type == "show_operation")
            action_at = min(event.at_ms for event in step.events if event.type in {"apply_both_sides", "substitute", "compare", "simplify"})
            result_at = min(event.at_ms for event in step.events if event.type == "reveal" and "result" in event.targets)
            assert operation_at < action_at < result_at <= step.duration_ms
            assert step.duration_ms >= len((step.narration or "").split()) * 350
            all_narration.append(step.narration)
        final = board.steps[-1]
        assert final.operation.action == "verify_solution"
        assert final.state_after["verification_link"] == source["verification"]
        assert any(event.type == "verify" and "verification" in event.targets for event in final.events)
    assert len(all_narration) == len(set(all_narration)), "narration must be question- and step-specific"


def test_all_fifteen_examples_have_approved_answer_and_true_terminal_verification():
    assert set(TERMINAL_CONTRACTS) == {question.id for question in LESSON_1.whiteboard_questions}
    for question in LESSON_1.whiteboard_questions:
        contract = TERMINAL_CONTRACTS[question.id]
        steps = question.whiteboard.steps
        stages = [question.whiteboard.initial_expression, *[value for step in steps for value in (step.working_expression, step.after_expression)]]
        assert question.answer == contract["approved_answer"]
        assert any(str(contract["answer_state"]).casefold() in step.after_expression.casefold() for step in steps)
        assert contract["verification_state"] in f"{steps[-1].working_expression} {steps[-1].after_expression}"
        assert steps[-1].operation.action == "verify_solution"
        assert steps[-1].state_after["verification_complete"] is True
        cursor = 0
        for required in contract["required_states"]:
            cursor = next(index + 1 for index in range(cursor, len(stages)) if required.casefold() in stages[index].casefold())


def test_confirmed_incomplete_examples_reach_required_terminal_mathematics():
    by_id = {question.id: question.whiteboard for question in LESSON_1.whiteboard_questions}
    assert "12 = 12" in by_id["g8-ae-l01-w01"].steps[-1].after_expression
    assert any("□ = 8" in step.after_expression for step in by_id["g8-ae-l01-w02"].steps)
    assert "13 = 13" in by_id["g8-ae-l01-w02"].steps[-1].after_expression
    assert any("□ = 7" in step.after_expression for step in by_id["g8-ae-l01-w03"].steps)
    assert "10 = 10" in by_id["g8-ae-l01-w03"].steps[-1].after_expression
    repair_states = " ".join(step.after_expression for step in by_id["g8-ae-l01-w05"].steps)
    assert "5 ≠ 8" in repair_states and "8 − 3 = 8 − 3" in repair_states and "5 = 5" in repair_states


def test_every_question_surface_has_a_complete_answer_and_original_question_check():
    assert len(LESSON_1.whiteboard_questions) == 15
    assert len(PRACTICE_BANK) == 15
    assert len(MASTERY_BANK) == 5
    assert len(REASSESSMENT_BANK) == 3
    assert len(REPAIR_RULES) == 6
    all_assessment_ids = {item.id for item in [*PRACTICE_BANK, *MASTERY_BANK, *REASSESSMENT_BANK]}
    assert all_assessment_ids == set(QUESTION_VERIFICATIONS)
    for question in PRACTICE_BANK:
        assert question.accepted_answers
        assert question.worked_solution[-1].verification == QUESTION_VERIFICATIONS[question.id]
        assert "=" in question.verification["original_question_check"]
        assert all(answer.casefold() not in " ".join(question.hints).casefold() for answer in question.accepted_answers if answer.replace(".", "").isdigit())
    for question in [*MASTERY_BANK, *REASSESSMENT_BANK]:
        assert question.solution and question.answer
        assert question.verification == QUESTION_VERIFICATIONS[question.id]
        assert "=" in question.verification


def test_terminal_validation_reports_answer_verification_and_skipped_simplification_failures():
    grade = curriculum_repository.get_grade("grade-8")
    topic, subtopic = grade.topics[0], grade.topics[0].subtopics[0]
    question = LESSON_1.whiteboard_questions[2]
    broken_steps = list(question.whiteboard.steps[:-1])
    broken_board = question.whiteboard.model_copy(update={"steps": broken_steps})
    broken_question = question.model_copy(update={"answer": "99", "whiteboard": broken_board})
    bad_lesson = LESSON_1.model_copy(update={"whiteboard_questions": [*LESSON_1.whiteboard_questions[:2], broken_question, *LESSON_1.whiteboard_questions[3:]]})
    bad_subtopic = subtopic.model_copy(update={"lessons": [bad_lesson, *subtopic.lessons[1:]]})
    bad_topic = topic.model_copy(update={"subtopics": [bad_subtopic, *topic.subtopics[1:]]})
    bad_grade = grade.model_copy(update={"topics": [bad_topic, *grade.topics[1:]]})
    reasons = {failure.failure_reason for failure in validate_curriculum([bad_grade]) if failure.question_id == question.id}
    assert "explicit final answer disagrees with the approved answer" in reasons
    assert "timeline lacks terminal verification against the original question" in reasons
    assert any(reason.startswith("timeline skips required simplification") for reason in reasons)


def test_first_example_teaches_comparison_not_renderer_commands():
    question = LESSON_1.whiteboard_questions[0]
    narration = " ".join(step.narration or "" for step in question.whiteboard.steps).casefold()
    assert "same value" in narration and "both sides" in narration and "twelve" in narration
    for command in ("reveal the complete equation", "highlight the left", "place 12", "show the beam"):
        assert command not in narration


def test_published_timeline_validation_reports_all_teaching_failures():
    grade = curriculum_repository.get_grade("grade-8")
    topic, subtopic = grade.topics[0], grade.topics[0].subtopics[0]
    question = LESSON_1.whiteboard_questions[0]
    original = question.whiteboard.steps[0]
    command = "Reveal the complete equation."
    broken = original.model_copy(update={
        "before_expression": question.whiteboard.initial_expression,
        "working_expression": question.whiteboard.initial_expression,
        "after_expression": question.whiteboard.initial_expression,
        "narration": command,
        "internal_instruction": command,
        "visualization_state": original.visualization_state.model_copy(update={"target": "missing-target"}),
        "events": [
            TimelineEvent(at_ms=0, type="caption", text=command),
            TimelineEvent(at_ms=0, type="narration", text=command),
            TimelineEvent(at_ms=350, type="focus", targets=["left-expression"]),
            TimelineEvent(at_ms=500, type="reveal", targets=["result"], style="result"),
            TimelineEvent(at_ms=1000, type="show_operation", targets=["operation"], label="7 + 5 → 12", style="operation"),
        ],
    })
    board = question.whiteboard.model_copy(update={"steps": [broken]})
    bad_question = question.model_copy(update={"whiteboard": board})
    bad_lesson = LESSON_1.model_copy(update={"whiteboard_questions": [bad_question, *LESSON_1.whiteboard_questions[1:]]})
    bad_subtopic = subtopic.model_copy(update={"lessons": [bad_lesson, *subtopic.lessons[1:]]})
    bad_topic = topic.model_copy(update={"subtopics": [bad_subtopic, *topic.subtopics[1:]]})
    bad_grade = grade.model_copy(update={"topics": [bad_topic, *grade.topics[1:]]})
    failures = [item for item in validate_curriculum([bad_grade]) if item.question_id == question.id and item.step_id == broken.id]
    reasons = {item.failure_reason for item in failures}
    assert "learner narration duplicates the internal authoring instruction" in reasons
    assert "learner narration consists only of a renderer command" in reasons
    assert "teaching step has no visible mathematical state change" in reasons
    assert "mathematical operation has no distinct visible working state" in reasons
    assert "teaching step has no real active semantic target" in reasons
    assert "result appears before its mathematical operation" in reasons
    assert all(item.grade_id == "grade-8" and item.topic_id == "algebraic-equations" and item.lesson_id == LESSON_1.id for item in failures)


def test_public_payload_gates_answers_and_direct_urls_restore():
    with TestClient(app) as client:
        payload = client.get("/api/v1/lessons/g8-algebraic-equations-01").json()
        topic_payload = client.get("/api/v1/curriculum/grades/grade-8/topics/algebraic-equations").json()
        blocked = client.get("/api/v1/lessons/g8-algebraic-equations-07")
        revealed = client.post("/api/v1/lessons/g8-algebraic-equations-01/questions/g8-ae-l01-w01/reveal")
    assert payload["grade_id"] == "grade-8"
    assert payload["topic_id"] == "algebraic-equations"
    assert payload["paper"] is None
    assert all("answer" not in item and "full_memo" not in item for item in payload["whiteboard_questions"])
    assert all(item["solution_gated"] and len(item["whiteboard"]["steps"]) == 1 for item in payload["whiteboard_questions"])
    assert "whiteboard_questions" not in topic_payload["subtopics"][0]["lessons"][0]
    assert "assessment_contract" not in topic_payload["subtopics"][0]["lessons"][0]
    assert blocked.status_code == 401
    assert revealed.status_code == 200
    assert revealed.json()["id"] == "g8-ae-l01-w01"
    assert "internal_instruction" not in json.dumps(revealed.json())
    assert "Reveal the complete equation" not in json.dumps(revealed.json())


def test_server_authoritative_practice_mastery_repair_and_reassessment():
    with TestClient(app) as client:
        public = client.get(f"/api/v1/practice/{LESSON_1.id}").json()
        assert len(public["questions"]) == 15
        assert "accepted_answers" not in json.dumps(public)
        session = client.post(f"/api/v1/practice/{LESSON_1.id}/sessions").json()["session_id"]
        cross = client.post(f"/api/v1/practice/g12-sequences-series-01/sessions/{session}/questions/g12-seq-l01-p01/submit", json={"answer": "x"})
        assert cross.status_code == 404
        mastery_public = client.get(f"/api/v1/practice/{LESSON_1.id}/mastery").json()
        assert len(mastery_public["questions"]) == 5 and "answer" not in json.dumps(mastery_public)
        fail_answers = {item.id: "definitely incorrect" for item in MASTERY_BANK}
        failed = client.post(f"/api/v1/practice/{LESSON_1.id}/sessions/{session}/mastery", json={"answers": fail_answers}).json()
        assert failed["mastered"] is False and failed["readiness_decision"] == "targeted_repair_required"
        assert failed["repair_routes"]
        assert client.post(f"/api/v1/practice/{LESSON_1.id}/sessions/{session}/repair/complete").json()["reassessment_unlocked"]
        reassessment = client.get(f"/api/v1/practice/{LESSON_1.id}/sessions/{session}/reassessment").json()
        assert len(reassessment["questions"]) == 3 and "answer" not in json.dumps(reassessment)
        reassessment_answers = {item.id: item.answer for item in REASSESSMENT_BANK}
        ready = client.post(f"/api/v1/practice/{LESSON_1.id}/sessions/{session}/reassessment", json={"answers": reassessment_answers}).json()
        assert ready["ready"] is True and ready["readiness_decision"] == "ready"
        second = client.post(f"/api/v1/practice/{LESSON_1.id}/sessions").json()["session_id"]
        pass_answers = {item.id: item.answer for item in MASTERY_BANK}
        passed = client.post(f"/api/v1/practice/{LESSON_1.id}/sessions/{second}/mastery", json={"answers": pass_answers}).json()
        assert passed["questions_correct"] == 5 and passed["mastered"] is True


def test_hint_endpoint_advances_one_hint_and_never_repeats_the_last_hint():
    with TestClient(app) as client:
        session = client.post(f"/api/v1/practice/{LESSON_1.id}/sessions").json()["session_id"]
        path = f"/api/v1/practice/{LESSON_1.id}/sessions/{session}/questions/g8-ae-l01-p03/hint"
        first = client.post(f"{path}?hint_index=0")
        second = client.post(f"{path}?hint_index=1")
        exhausted = client.post(f"{path}?hint_index=2")
        reset = client.post(f"{path}?hint_index=0")
    assert first.status_code == second.status_code == reset.status_code == 200
    assert first.json()["hint_index"] == 0 and first.json()["hints_remaining"] == 1
    assert second.json()["hint_index"] == 1 and second.json()["hint_complete"] is True
    assert first.json()["hint"] != second.json()["hint"]
    assert exhausted.status_code == 409
    assert reset.json()["hint"] == first.json()["hint"]
