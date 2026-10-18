"""Aggregate, lossless-content checks for the coordinated Paper 2 batch."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from fastapi.testclient import TestClient

from app.curriculum.grade12 import GRADE_12
from app.curriculum.grade12.lessons.paper2_topics import (
    ANALYTICAL_GEOMETRY_CANVAS_FAMILIES, ANALYTICAL_GEOMETRY_PACK,
    ANALYTICAL_GEOMETRY_PRACTICE_BANKS, STATISTICS_CANVAS_FAMILIES,
    STATISTICS_PACK, STATISTICS_PRACTICE_BANKS,
)
from app.main import app


ROOT = Path(__file__).parents[2]


def topic(topic_id):
    return next(item for item in GRADE_12.topics if item.id == topic_id)


def collect_failures():
    failures = []

    def check(condition, topic_id, lesson_id="-", item_id="-", field="-", reason="invalid"):
        if not condition:
            failures.append(f"{topic_id} / {lesson_id} / {item_id} / {field} / {reason}")

    specifications = [
        ("statistics-regression", 8, 20, 18, 180, 216, STATISTICS_PACK, STATISTICS_PRACTICE_BANKS, STATISTICS_CANVAS_FAMILIES, "G12-STAT"),
        ("analytical-geometry", 9, 40, 16, 160, 192, ANALYTICAL_GEOMETRY_PACK, ANALYTICAL_GEOMETRY_PRACTICE_BANKS, ANALYTICAL_GEOMETRY_CANVAS_FAMILIES, "G12-AG"),
    ]
    all_ids = []
    for topic_id, order, marks, lesson_count, guided_count, practice_count, pack, banks, families, prefix in specifications:
        current = topic(topic_id)
        lessons = current.subtopics[0].lessons
        check(current.product_order == order, topic_id, field="product_order", reason=f"expected {order}")
        check((current.paper, current.paper_number, current.grade, current.subject) == ("Paper 2", 2, 12, "Mathematics"), topic_id, field="paper_identity", reason="Paper 2 identity contract incomplete")
        check(current.official_weighting == marks, topic_id, field="official_weighting", reason=f"expected {marks}")
        check(len(lessons) == lesson_count, topic_id, field="lessons", reason=f"expected {lesson_count}")
        check(sum(len(item.whiteboard_questions) for item in lessons) == guided_count, topic_id, field="guided_examples", reason=f"expected {guided_count}")
        check(sum(len(bank) for bank in banks.values()) == practice_count, topic_id, field="practice_questions", reason=f"expected {practice_count}")
        check([item.id for item in lessons] == [row["id"] for row in pack["lessons"]], topic_id, field="lesson_order", reason="DOCX order or stable IDs changed")
        for lesson, raw, family in zip(lessons, pack["lessons"], families):
            check(lesson.title == raw["title"], topic_id, lesson.id, field="title", reason="approved title changed")
            check(lesson.source_sha256 == pack["source_sha256"], topic_id, lesson.id, field="source_sha256", reason="source traceability missing")
            check(lesson.paper == "Paper 2", topic_id, lesson.id, field="paper", reason="lesson is not machine-readable Paper 2")
            contract = lesson.presentation_contract
            check(contract is not None, topic_id, lesson.id, field="presentation_contract", reason="missing")
            if contract:
                check(contract.canvas_family == family, topic_id, lesson.id, field="canvas_family", reason=f"expected {family}")
                object_ids = {item.id for item in contract.semantic_objects}
                event_ids = {item.event_id for item in contract.events}
                check(bool(object_ids), topic_id, lesson.id, field="semantic_objects", reason="empty")
                check([event.sequence for event in contract.events] == list(range(1, 7)), topic_id, lesson.id, field="events", reason="six ordered source beats required")
                for event in contract.events:
                    check(set(event.semantic_object_ids) <= object_ids, topic_id, lesson.id, event.event_id, "semantic_object_ids", "missing target")
                for cue in contract.voice_cues:
                    check(cue.start_event in event_ids and cue.end_event in event_ids, topic_id, lesson.id, cue.cue_id, "event_reference", "missing event")
                    check(cue.caption_text == cue.spoken_text, topic_id, lesson.id, cue.cue_id, "caption_text", "caption differs from narration")
                    check(cue.silence_during_motion, topic_id, lesson.id, cue.cue_id, "silence_during_motion", "must remain true")
                check(any(cue.wait_for_user for cue in contract.voice_cues), topic_id, lesson.id, field="voice_cues", reason="prediction wait missing")
                check(contract.future_engine_status == "specified_not_activated", topic_id, lesson.id, field="future_engine_status", reason="engine must remain inactive")
            raw_guided = {item["ID"]: item for item in raw["guided_examples"]}
            check(len(raw_guided) == 10, topic_id, lesson.id, field="guided_source", reason="source item count changed")
            signatures = {tuple(item.operation_signature) for item in lesson.whiteboard_questions}
            check(len(signatures) > 1, topic_id, lesson.id, field="operation_signature", reason="all ten examples share one operation signature")
            for item in lesson.whiteboard_questions:
                all_ids.append(item.id)
                source = raw_guided[item.id]
                check(item.id == f"{prefix}-L{lesson.order:02}-W{item.order:02}", topic_id, lesson.id, item.id, "id", "non-deterministic ID")
                check(item.whiteboard.problem == source["Problem"], topic_id, lesson.id, item.id, "problem", "approved wording changed")
                check(item.answer == source["Worked evidence / memo"] and bool(item.answer), topic_id, lesson.id, item.id, "answer", "approved memo missing or changed")
                if item.order >= 9:
                    check(len(item.operation_signature) > 1 and "evaluate_and_justify" in item.operation_signature, topic_id, lesson.id, item.id, "operation_signature", "exam item reducible to substitution")
                if item.approximate_answer:
                    check(item.answer_tolerance is not None and "approx" in f"{item.whiteboard.problem} {item.answer}".casefold(), topic_id, lesson.id, item.id, "answer_tolerance", "approximate read-off lacks tolerance/language")
            raw_practice = {item["ID"]: item for item in raw["practice_questions"]}
            bank = banks[lesson.id]
            check(len(bank) == 12, topic_id, lesson.id, field="practice_bank", reason="expected 12")
            expected_cognitive = ["knowledge"] * 2 + ["routine"] * 3 + ["complex"] * 4 + ["problem_solving"] * 3
            check([item.cognitive_level for item in bank] == expected_cognitive, topic_id, lesson.id, field="difficulty_progression", reason="foundation/routine/complex/exam structure changed")
            for item in bank:
                all_ids.append(item.id)
                source = raw_practice[item.id]
                check(item.prompt == source["Independent problem"], topic_id, lesson.id, item.id, "problem", "approved wording changed")
                check(item.feedback_route == source["Answer / feedback route"] and bool(item.accepted_answers), topic_id, lesson.id, item.id, "answer", "approved answer/rubric missing or changed")
                check(item.answer_hidden_before_submission, topic_id, lesson.id, item.id, "answer_hidden_before_submission", "must be true")
                if item.question_number >= 10:
                    check("evaluate_and_justify" in item.reasoning_demands, topic_id, lesson.id, item.id, "reasoning_demands", "exam practice lacks genuine decision/justification")
                if item.approximate_answer:
                    check(item.answer_tolerance is not None and "approx" in f"{item.prompt} {item.feedback_route}".casefold(), topic_id, lesson.id, item.id, "answer_tolerance", "approximate read-off lacks tolerance/language")
        source_path = ROOT / pack["source"]
        check(source_path.is_file(), topic_id, field="source_document", reason="authoritative DOCX missing")
        if source_path.is_file():
            check(hashlib.sha256(source_path.read_bytes()).hexdigest() == pack["source_sha256"], topic_id, field="source_sha256", reason="generated content is stale")
    check(len(all_ids) == 748, "paper2", field="item_count", reason=f"expected 748, got {len(all_ids)}")
    check(len(set(all_ids)) == 748, "paper2", field="item_ids", reason="IDs are not globally unique")
    return failures


def test_paper2_content_contract_collects_all_failures():
    failures = collect_failures()
    assert not failures, "\n" + "\n".join(failures)


def test_scope_exclusions_and_required_conventions():
    content = " ".join(
        [question.whiteboard.problem + " " + (question.answer or "") for topic_id in ("statistics-regression", "analytical-geometry") for lesson in topic(topic_id).subtopics[0].lessons for question in lesson.whiteboard_questions]
    ).casefold()
    assert "normal distribution" not in content
    assert "correlation proves causation" not in content
    assert "correlation alone does not prove" in content
    assert "concurrency" not in content
    assert "degree mode" in content and "0 degrees <= theta <= 180 degrees" in content
    assert "median-excluded-halves convention" in content
    assert "population variance" in content and "population standard deviation" in content
    assert "diagram alone is insufficient" in content


def test_assessments_are_original_question_first_and_marked():
    for topic_id, marks in (("statistics-regression", 20), ("analytical-geometry", 40)):
        lesson = topic(topic_id).subtopics[0].lessons[-1]
        assert lesson.assessment_contract["question_first"] is True
        assert lesson.assessment_contract["timed"] is True
        assert lesson.assessment_contract["worked_content_locked_until_submission"] is True
        assert lesson.assessment_contract["marks"] == marks


def test_api_exposes_paper2_and_never_leaks_independent_answers():
    with TestClient(app) as client:
        grade = client.get("/api/v1/curriculum/grades/grade-12").json()
        stats = client.get("/api/v1/curriculum/grades/grade-12/topics/statistics-regression").json()
        geometry = client.get("/api/v1/curriculum/grades/grade-12/topics/analytical-geometry").json()
        practice = client.get("/api/v1/practice/g12-statistics-01").json()
    summary = {item["id"]: item for item in grade["topics"]}
    assert summary["statistics-regression"]["paper"] == summary["analytical-geometry"]["paper"] == "Paper 2"
    assert stats["paper_number"] == geometry["paper_number"] == 2
    assert all(item["paper"] == "Paper 2" for item in stats["subtopics"][0]["lessons"])
    assert all("answer" not in item and "accepted_answers" not in item and "feedback_route" not in item for item in practice["questions"])


def test_existing_paper1_topics_remain_ahead_of_paper2():
    assert [(item.product_order, item.paper) for item in GRADE_12.topics[:5]] == [(1, "Paper 1"), (2, "Paper 1"), (3, "Paper 1"), (4, "Paper 1"), (5, "Paper 1")]
    assert [(item.product_order, item.paper) for item in GRADE_12.topics[-2:]] == [(8, "Paper 2"), (9, "Paper 2")]
