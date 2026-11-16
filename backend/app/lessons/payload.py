"""Build learner lesson documents without changing the source curriculum.

HTTP entitlement checks belong to the router. Preview/answer privacy belongs here.
"""

import json

from app.lessons.grade8_preview import gate_grade8_question
from app.lessons.visual_preview import public_visual


def lesson_payload(grade, topic, subtopic, lesson) -> dict:
    payload = lesson.model_dump()
    # Private assessment banks live outside the Lesson model. Worked-example
    # answers and memos are also omitted from the initial learner payload.
    for question in payload.get("whiteboard_questions", []):
        question.pop("answer", None)
        question.pop("full_memo", None)
        question.pop("expected_evidence", None)
        if grade.id == "grade-8":
            gate_grade8_question(question, lesson.id)
    if grade.id in {"grade-9", "grade-10", "grade-11"}:
        for question in payload.get("whiteboard_questions", []):
            question["total_step_count"] = len(question["whiteboard"]["steps"])
            question["solution_gated"] = True
            board = question["whiteboard"]
            preview = board["steps"][0]
            preview["working_expression"] = preview["before_expression"]
            preview["after_expression"] = preview["before_expression"]
            preview["events"] = []
            preview["narration"] = ""
            preview["common_mistake"] = None
            preview["state_after"] = {}
            preview["operation"]["value"] = "Read the original question"
            preview["title"] = "Read the original question"
            preview["explanation"] = {
                key: "Start with the complete question."
                for key in preview["explanation"]
            }
            preview["screen_reader_description"] = board["problem"]
            preview["instructional_goal"] = "Read the original question"
            preview["visualization_state"]["working_state"] = preview[
                "before_expression"
            ]
            preview["visualization_state"]["after_state"] = preview["before_expression"]
            board["steps"] = [preview]
            params = board["visualization"]["parameters"]
            scene = json.loads(params["scene_json"])
            for key in (
                "actions",
                "memo",
                "check",
                "answer",
                "wrongs",
                "wrong_methods",
                "option_rationales",
                "category",
                "secondary",
                "secondary_category",
                "primary_stage",
                "secondary_stage",
                "factors",
                "misconception",
            ):
                scene.pop(key, None)
            if scene.get("visual"):
                scene["visual"] = public_visual(lesson.id, scene["visual"])
            params["scene_json"] = json.dumps(scene, ensure_ascii=False)
            board["semantic_objects"] = [
                item
                for item in board["semantic_objects"]
                if item["id"] in {"problem", "model", "token", "factor-roots"}
            ]
    if grade.id in {"grade-8", "grade-9", "grade-10", "grade-11"}:
        previews = {
            item["whiteboard"]["id"]: item["whiteboard"]
            for item in payload.get("whiteboard_questions", [])
        }
        payload["blocks"] = [
            previews.get(block.get("id"), block) for block in payload.get("blocks", [])
        ]
    payload["assessment_contract"] = {
        key: value
        for key, value in payload.get("assessment_contract", {}).items()
        if key
        in {
            "worked_example_count",
            "practice_count",
            "mastery_question_count",
            "parallel_reassessment_count",
            "answer_hidden_before_submission",
            "progression_threshold",
        }
    }
    if lesson.id == "g12-sequences-series-01":
        # The practice API is authoritative. Legacy embedded questions and
        # answer keys must never be delivered with the lesson document.
        payload["blocks"] = [
            (
                {
                    **block,
                    "title": "Self-guided practice",
                    "content": "Solve, submit, then compare your method.",
                    "data": {"practice_bank_id": lesson.id},
                }
                if block.get("type") == "practice"
                else block
            )
            for block in payload["blocks"]
            if block.get("type") != "checkpoint"
        ]
    return {
        "grade_id": grade.id,
        "topic_id": topic.id,
        "topic_title": topic.title,
        "paper": topic.paper,
        "paper_number": topic.paper_number,
        "subtopic_id": subtopic.id,
        "subtopic_title": subtopic.title,
        "lesson_count": len(subtopic.lessons),
        **payload,
    }
