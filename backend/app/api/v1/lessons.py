"""Lesson content endpoint with server-side entitlement enforcement."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.core.security import get_optional_user
from app.curriculum.repository import curriculum_repository as repository
from app.db.models.user import User
from app.lessons.access import enforce_lesson_access

router = APIRouter()


def _lesson_context(lesson_id: str):
    result = repository.get_lesson_context(lesson_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return result


@router.get("/{lesson_id}")
def get_lesson(lesson_id: str, user: User | None = Depends(get_optional_user)) -> dict:
    result = _lesson_context(lesson_id)
    grade, topic, subtopic, lesson = result
    if lesson.status.value == "coming_soon":
        raise HTTPException(status_code=409, detail="This lesson is coming soon")
    enforce_lesson_access(lesson, user)
    payload = lesson.model_dump()
    # Private assessment banks live outside the Lesson model. Worked-example
    # answers and memos are also omitted from the initial learner payload.
    for question in payload.get("whiteboard_questions", []):
        question.pop("answer", None)
        question.pop("full_memo", None)
        question.pop("expected_evidence", None)
        if grade.id == "grade-8":
            question["total_step_count"] = len(question["whiteboard"]["steps"])
            question["solution_gated"] = True
            if lesson.id in {"g8-algebraic-equations-10", "g8-algebraic-expressions-10"}:
                question["diagnostic_submission_required"] = True
            question["whiteboard"]["steps"] = question["whiteboard"]["steps"][:1]
            if lesson.id == "g8-algebraic-equations-02":
                preview = question["whiteboard"]["steps"][0]
                preview["working_expression"] = preview["before_expression"]
                preview["after_expression"] = preview["before_expression"]
                preview["narration"] = ""
                preview["events"] = []
                preview["internal_instruction"] = None
                preview["explanation"] = {key: "Start with the complete question."
                                          for key in preview["explanation"]}
                preview["operation"]["value"] = "Inspect the original relationship"
                preview["instructional_goal"] = "Inspect the original relationship"
                preview["screen_reader_description"] = question["whiteboard"]["problem"]
                preview["state_after"] = {}
                preview["visualization_state"]["working_state"] = preview["before_expression"]
                preview["visualization_state"]["after_state"] = preview["before_expression"]
                visual = question["whiteboard"].get("visualization")
                if visual:
                    source_data = visual["parameters"].get("source_data", "")
                    concealed = {"candidate", "candidates", "outputs", "left outputs", "right outputs",
                                 "smaller", "larger", "candidate cm", "intermediate", "group value"}
                    visual["parameters"]["source_data"] = "; ".join(
                        field for field in source_data.split("; ")
                        if field.partition("=")[0].strip() not in concealed
                    )
            if lesson.id in {"g8-graphs-01", "g8-graphs-02", "g8-graphs-03", "g8-graphs-04", "g8-graphs-05", "g8-graphs-06", "g8-patterns-01", "g8-patterns-02", "g8-patterns-03", "g8-patterns-04", "g8-patterns-05", "g8-patterns-06", "g8-whole-numbers-01", "g8-whole-numbers-02", "g8-integers-01", "g8-integers-02", "g8-integers-03", "g8-integers-04", "g8-integers-05", "g8-integers-06", "g8-common-fractions-01", "g8-common-fractions-02", "g8-common-fractions-03", "g8-common-fractions-04", "g8-common-fractions-05", "g8-common-fractions-06", "g8-common-fractions-07", "g8-common-fractions-08", "g8-decimal-fractions-01", "g8-decimal-fractions-02", "g8-decimal-fractions-03", "g8-decimal-fractions-04", "g8-decimal-fractions-05", "g8-decimal-fractions-06", "g8-exponents-01", "g8-exponents-02", "g8-exponents-03", "g8-exponents-04", "g8-exponents-05", "g8-exponents-06", "g8-straight-lines-01", "g8-straight-lines-02", "g8-shapes-01", "g8-shapes-02", "g8-shapes-03", "g8-shapes-04", "g8-shapes-05", "g8-pythagoras-01", "g8-pythagoras-02", "g8-pythagoras-03", "g8-pythagoras-04", "g8-pythagoras-05", "g8-algebraic-expressions-01", "g8-algebraic-expressions-02", "g8-algebraic-expressions-03", "g8-algebraic-expressions-04", "g8-algebraic-expressions-05", "g8-algebraic-expressions-06", "g8-algebraic-expressions-07", "g8-algebraic-expressions-08", "g8-algebraic-expressions-09", "g8-algebraic-expressions-10", "g8-functions-relationships-01", "g8-functions-relationships-02", "g8-functions-relationships-03", "g8-functions-relationships-04", "g8-functions-relationships-05", "g8-functions-relationships-06", "g8-algebraic-equations-03", "g8-algebraic-equations-04", "g8-algebraic-equations-05", "g8-algebraic-equations-06", "g8-algebraic-equations-07", "g8-algebraic-equations-08", "g8-algebraic-equations-09", "g8-algebraic-equations-10"}:
                preview = question["whiteboard"]["steps"][0]
                preview["working_expression"] = preview["before_expression"]
                preview["after_expression"] = preview["before_expression"]
                preview["events"] = []
                preview["narration"] = ""
                preview["internal_instruction"] = None
                preview["state_after"] = {}
                preview["operation"]["value"] = "Read the original question"
                preview["instructional_goal"] = "Read the original question"
                preview["screen_reader_description"] = question["whiteboard"]["problem"]
                preview["explanation"] = {key:"Start with the complete question." for key in preview["explanation"]}
                preview["visualization_state"]["working_state"] = preview["before_expression"]
                preview["visualization_state"]["after_state"] = preview["before_expression"]
                source = question["whiteboard"]["visualization"]["parameters"].get("source_data", "")
                question["whiteboard"]["visualization"]["parameters"]["source_data"] = "; ".join(
                    field for field in source.split("; ")
                    if not field.partition("=")[0].strip().replace("_", " ").startswith(("solution", "equation", "correct", "first error", "reduced statement", "final prices", "dimensions", "equal cost", "unit value", "whole litres", "landing", "intermediate", "reverse operations", "reverse rule", "signed distance", "difference", "condition", "break even input", "meeting week", "common length", "classification", "learner conclusion", "repair", "meeting amount", "test values", "expanded", "divide first state", "partial products", "restriction", "lcd", "scaled terms", "cleared equation"))
                )
            if lesson.id in {"g8-common-fractions-01", "g8-common-fractions-02", "g8-common-fractions-03", "g8-common-fractions-04", "g8-common-fractions-05", "g8-common-fractions-06", "g8-common-fractions-07", "g8-common-fractions-08", "g8-decimal-fractions-01", "g8-decimal-fractions-02", "g8-decimal-fractions-03", "g8-decimal-fractions-04", "g8-decimal-fractions-05", "g8-decimal-fractions-06", "g8-exponents-01", "g8-exponents-02", "g8-exponents-03", "g8-exponents-04", "g8-exponents-05", "g8-exponents-06"}:
                import json
                params=question["whiteboard"]["visualization"]["parameters"]
                scene=json.loads(params["scene_json"])
                for key in ("answer","memo","rows","misconception"):
                    scene.pop(key,None)
                params["scene_json"]=json.dumps(scene,ensure_ascii=False)
            if lesson.id in {"g8-integers-03", "g8-integers-04", "g8-integers-05", "g8-integers-06"}:
                import json
                params=question["whiteboard"]["visualization"]["parameters"]
                scene=json.loads(params["scene_json"])
                for key in ("answer","memo","actions","rows","misconception","left_value","claim_true"):
                    scene.pop(key,None)
                params["scene_json"]=json.dumps(scene,ensure_ascii=False)
            if lesson.id in {"g8-integers-01", "g8-integers-02"}:
                import json
                params=question["whiteboard"]["visualization"]["parameters"]
                scene=json.loads(params["scene_json"])
                for key in ("answer","memo","actions","path"):
                    scene.pop(key,None)
                params["scene_json"]=json.dumps(scene,ensure_ascii=False)
            if lesson.id in {"g8-whole-numbers-01", "g8-whole-numbers-02"}:
                import json
                params=question["whiteboard"]["visualization"]["parameters"]
                scene=json.loads(params["scene_json"])
                for key in ("answer","memo","actions","factors","property"):
                    scene.pop(key,None)
                params["scene_json"]=json.dumps(scene,ensure_ascii=False)
            if lesson.id in {"g8-graphs-03", "g8-graphs-04", "g8-graphs-05", "g8-graphs-06", "g8-patterns-01", "g8-patterns-02", "g8-patterns-03", "g8-patterns-04", "g8-patterns-05", "g8-patterns-06", "g8-whole-numbers-01", "g8-whole-numbers-02", "g8-integers-01", "g8-integers-02"}:
                import json
                params = question["whiteboard"]["visualization"]["parameters"]
                scene = json.loads(params["scene_json"])
                for private_key in (("answer", "memo", "actions", "repair", "misconception", "rule", "a", "b")
                                    if lesson.id == "g8-patterns-03" else
                                    ("answer", "memo", "actions", "repair", "misconception", "correct_label", "wrong_index", "rule", "a", "b", "family")
                                    if lesson.id in {"g8-patterns-05", "g8-patterns-06", "g8-whole-numbers-01", "g8-whole-numbers-02", "g8-integers-01", "g8-integers-02"} else
                                    ("answer", "memo", "actions", "repair", "misconception")):
                    scene.pop(private_key, None)
                params["scene_json"] = json.dumps(scene, ensure_ascii=False)
            if lesson.id in {"g8-functions-relationships-05", "g8-functions-relationships-06"}:
                import json
                visual=question["whiteboard"]["visualization"]
                params=visual["parameters"]
                params["derived_objects"]=["?" for _ in params["derived_objects"]]
                scene=json.loads(params["scene_json"])
                scene.pop("chosen",None)
                for path in scene["candidates"]:
                    path.pop("value",None)
                    if scene["mode"]=="repair" and path is scene["candidates"][1]:
                        path["label"]="Repair path"
                params["scene_json"]=json.dumps(scene,ensure_ascii=False)
            question["whiteboard"]["semantic_objects"] = [
                item for item in question["whiteboard"]["semantic_objects"]
                if item["id"] in {"problem", "stage-01"}
            ]
    if grade.id == "grade-9":
        import json
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
            preview["explanation"] = {key: "Start with the complete question." for key in preview["explanation"]}
            preview["screen_reader_description"] = board["problem"]
            preview["instructional_goal"] = "Read the original question"
            preview["visualization_state"]["working_state"] = preview["before_expression"]
            preview["visualization_state"]["after_state"] = preview["before_expression"]
            board["steps"] = [preview]
            params = board["visualization"]["parameters"]
            scene = json.loads(params["scene_json"])
            for key in ("actions", "memo", "check", "answer", "wrongs", "wrong_methods", "option_rationales", "category",
                        "secondary", "secondary_category", "primary_stage", "secondary_stage", "factors", "misconception"):
                scene.pop(key, None)
            if scene.get("visual"):
                scene["visual"] = {"family":"givens"}
            params["scene_json"] = json.dumps(scene, ensure_ascii=False)
            board["semantic_objects"] = [item for item in board["semantic_objects"] if item["id"] in {"problem", "model", "token", "factor-roots"}]
        previews = {item["whiteboard"]["id"]:item["whiteboard"] for item in payload.get("whiteboard_questions", [])}
        payload["blocks"] = [previews.get(block.get("id"), block) for block in payload.get("blocks", [])]
    if grade.id == "grade-8":
        previews = {item["whiteboard"]["id"]:item["whiteboard"] for item in payload.get("whiteboard_questions", [])}
        payload["blocks"] = [previews.get(block.get("id"),block) for block in payload.get("blocks", [])]
    payload["assessment_contract"] = {
        key: value for key, value in payload.get("assessment_contract", {}).items()
        if key in {"worked_example_count", "practice_count", "mastery_question_count", "parallel_reassessment_count", "answer_hidden_before_submission", "progression_threshold"}
    }
    if lesson.id == "g12-sequences-series-01":
        # The practice API is authoritative. Legacy embedded questions and
        # answer keys must never be delivered with the lesson document.
        payload["blocks"] = [
            ({**block, "title": "Self-guided practice",
              "content": "Solve, submit, then compare your method.",
              "data": {"practice_bank_id": lesson.id}}
             if block.get("type") == "practice" else block)
            for block in payload["blocks"] if block.get("type") != "checkpoint"
        ]
    return {"grade_id": grade.id, "topic_id": topic.id,
            "topic_title": topic.title, "paper": topic.paper,
            "paper_number": topic.paper_number, "subtopic_id": subtopic.id,
            "subtopic_title": subtopic.title,
            "lesson_count": len(subtopic.lessons), **payload}


@router.post("/{lesson_id}/questions/{question_id}/reveal")
def reveal_worked_example(lesson_id: str, question_id: str, user: User | None = Depends(get_optional_user)) -> dict:
    grade, _, _, lesson = _lesson_context(lesson_id)
    if grade.id not in {"grade-8", "grade-9"}:
        raise HTTPException(status_code=404, detail="Worked example not found")
    enforce_lesson_access(lesson, user)
    if lesson.id in {"g8-algebraic-equations-10", "g8-algebraic-expressions-10"}:
        raise HTTPException(status_code=409, detail="Submit your first-error diagnosis before viewing the worked repair")
    question = next((item for item in lesson.whiteboard_questions if item.id == question_id), None)
    if question is None:
        raise HTTPException(status_code=404, detail="Worked example not found")
    # This explicit learner action is the solution gate. It returns only the
    # requested worked example and never exposes assessment answer keys.
    return question.model_dump()


class DiagnosticAttempt(BaseModel):
    first_error_and_repair: str = Field(min_length=3, max_length=500)


@router.post("/{lesson_id}/questions/{question_id}/diagnose")
def diagnose_worked_example(lesson_id: str, question_id: str, attempt: DiagnosticAttempt,
                            user: User | None = Depends(get_optional_user)) -> dict:
    grade, _, _, lesson = _lesson_context(lesson_id)
    if grade.id != "grade-8" or lesson.id not in {"g8-algebraic-equations-10", "g8-algebraic-expressions-10"}:
        raise HTTPException(status_code=404, detail="Diagnostic case not found")
    enforce_lesson_access(lesson, user)
    if not attempt.first_error_and_repair.strip():
        raise HTTPException(status_code=422, detail="Describe the first error and your repair")
    question = next((item for item in lesson.whiteboard_questions if item.id == question_id), None)
    if question is None:
        raise HTTPException(status_code=404, detail="Diagnostic case not found")
    # Submission precedes the authored explanation; this is an attempt gate,
    # not automated grading of mathematical prose.
    return question.model_dump()
