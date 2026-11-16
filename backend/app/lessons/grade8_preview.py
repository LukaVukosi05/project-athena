"""Grade 8 initial-preview privacy rules; preserve authored lesson exceptions."""

import json


def gate_grade8_question(question: dict, lesson_id: str) -> None:
    question["total_step_count"] = len(question["whiteboard"]["steps"])
    question["solution_gated"] = True
    if lesson_id in {"g8-algebraic-equations-10", "g8-algebraic-expressions-10"}:
        question["diagnostic_submission_required"] = True
    question["whiteboard"]["steps"] = question["whiteboard"]["steps"][:1]
    if lesson_id == "g8-algebraic-equations-02":
        preview = question["whiteboard"]["steps"][0]
        preview["working_expression"] = preview["before_expression"]
        preview["after_expression"] = preview["before_expression"]
        preview["narration"] = ""
        preview["events"] = []
        preview["internal_instruction"] = None
        preview["explanation"] = {
            key: "Start with the complete question." for key in preview["explanation"]
        }
        preview["operation"]["value"] = "Inspect the original relationship"
        preview["instructional_goal"] = "Inspect the original relationship"
        preview["screen_reader_description"] = question["whiteboard"]["problem"]
        preview["state_after"] = {}
        preview["visualization_state"]["working_state"] = preview["before_expression"]
        preview["visualization_state"]["after_state"] = preview["before_expression"]
        visual = question["whiteboard"].get("visualization")
        if visual:
            source_data = visual["parameters"].get("source_data", "")
            concealed = {
                "candidate",
                "candidates",
                "outputs",
                "left outputs",
                "right outputs",
                "smaller",
                "larger",
                "candidate cm",
                "intermediate",
                "group value",
            }
            visual["parameters"]["source_data"] = "; ".join(
                field
                for field in source_data.split("; ")
                if field.partition("=")[0].strip() not in concealed
            )
    if lesson_id in {
        "g8-graphs-01",
        "g8-graphs-02",
        "g8-graphs-03",
        "g8-graphs-04",
        "g8-graphs-05",
        "g8-graphs-06",
        "g8-patterns-01",
        "g8-patterns-02",
        "g8-patterns-03",
        "g8-patterns-04",
        "g8-patterns-05",
        "g8-patterns-06",
        "g8-whole-numbers-01",
        "g8-whole-numbers-02",
        "g8-integers-01",
        "g8-integers-02",
        "g8-integers-03",
        "g8-integers-04",
        "g8-integers-05",
        "g8-integers-06",
        "g8-common-fractions-01",
        "g8-common-fractions-02",
        "g8-common-fractions-03",
        "g8-common-fractions-04",
        "g8-common-fractions-05",
        "g8-common-fractions-06",
        "g8-common-fractions-07",
        "g8-common-fractions-08",
        "g8-decimal-fractions-01",
        "g8-decimal-fractions-02",
        "g8-decimal-fractions-03",
        "g8-decimal-fractions-04",
        "g8-decimal-fractions-05",
        "g8-decimal-fractions-06",
        "g8-exponents-01",
        "g8-exponents-02",
        "g8-exponents-03",
        "g8-exponents-04",
        "g8-exponents-05",
        "g8-exponents-06",
        "g8-straight-lines-01",
        "g8-straight-lines-02",
        "g8-shapes-01",
        "g8-shapes-02",
        "g8-shapes-03",
        "g8-shapes-04",
        "g8-shapes-05",
        "g8-pythagoras-01",
        "g8-pythagoras-02",
        "g8-pythagoras-03",
        "g8-pythagoras-04",
        "g8-pythagoras-05",
        "g8-algebraic-expressions-01",
        "g8-algebraic-expressions-02",
        "g8-algebraic-expressions-03",
        "g8-algebraic-expressions-04",
        "g8-algebraic-expressions-05",
        "g8-algebraic-expressions-06",
        "g8-algebraic-expressions-07",
        "g8-algebraic-expressions-08",
        "g8-algebraic-expressions-09",
        "g8-algebraic-expressions-10",
        "g8-functions-relationships-01",
        "g8-functions-relationships-02",
        "g8-functions-relationships-03",
        "g8-functions-relationships-04",
        "g8-functions-relationships-05",
        "g8-functions-relationships-06",
        "g8-algebraic-equations-03",
        "g8-algebraic-equations-04",
        "g8-algebraic-equations-05",
        "g8-algebraic-equations-06",
        "g8-algebraic-equations-07",
        "g8-algebraic-equations-08",
        "g8-algebraic-equations-09",
        "g8-algebraic-equations-10",
    }:
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
        preview["explanation"] = {
            key: "Start with the complete question." for key in preview["explanation"]
        }
        preview["visualization_state"]["working_state"] = preview["before_expression"]
        preview["visualization_state"]["after_state"] = preview["before_expression"]
        source = question["whiteboard"]["visualization"]["parameters"].get(
            "source_data", ""
        )
        question["whiteboard"]["visualization"]["parameters"]["source_data"] = (
            "; ".join(
                field
                for field in source.split("; ")
                if not field.partition("=")[0]
                .strip()
                .replace("_", " ")
                .startswith(
                    (
                        "solution",
                        "equation",
                        "correct",
                        "first error",
                        "reduced statement",
                        "final prices",
                        "dimensions",
                        "equal cost",
                        "unit value",
                        "whole litres",
                        "landing",
                        "intermediate",
                        "reverse operations",
                        "reverse rule",
                        "signed distance",
                        "difference",
                        "condition",
                        "break even input",
                        "meeting week",
                        "common length",
                        "classification",
                        "learner conclusion",
                        "repair",
                        "meeting amount",
                        "test values",
                        "expanded",
                        "divide first state",
                        "partial products",
                        "restriction",
                        "lcd",
                        "scaled terms",
                        "cleared equation",
                    )
                )
            )
        )
    if lesson_id in {
        "g8-common-fractions-01",
        "g8-common-fractions-02",
        "g8-common-fractions-03",
        "g8-common-fractions-04",
        "g8-common-fractions-05",
        "g8-common-fractions-06",
        "g8-common-fractions-07",
        "g8-common-fractions-08",
        "g8-decimal-fractions-01",
        "g8-decimal-fractions-02",
        "g8-decimal-fractions-03",
        "g8-decimal-fractions-04",
        "g8-decimal-fractions-05",
        "g8-decimal-fractions-06",
        "g8-exponents-01",
        "g8-exponents-02",
        "g8-exponents-03",
        "g8-exponents-04",
        "g8-exponents-05",
        "g8-exponents-06",
    }:
        params = question["whiteboard"]["visualization"]["parameters"]
        scene = json.loads(params["scene_json"])
        for key in ("answer", "memo", "rows", "misconception"):
            scene.pop(key, None)
        params["scene_json"] = json.dumps(scene, ensure_ascii=False)
    if lesson_id in {
        "g8-integers-03",
        "g8-integers-04",
        "g8-integers-05",
        "g8-integers-06",
    }:
        params = question["whiteboard"]["visualization"]["parameters"]
        scene = json.loads(params["scene_json"])
        for key in (
            "answer",
            "memo",
            "actions",
            "rows",
            "misconception",
            "left_value",
            "claim_true",
        ):
            scene.pop(key, None)
        params["scene_json"] = json.dumps(scene, ensure_ascii=False)
    if lesson_id in {"g8-integers-01", "g8-integers-02"}:
        params = question["whiteboard"]["visualization"]["parameters"]
        scene = json.loads(params["scene_json"])
        for key in ("answer", "memo", "actions", "path"):
            scene.pop(key, None)
        params["scene_json"] = json.dumps(scene, ensure_ascii=False)
    if lesson_id in {"g8-whole-numbers-01", "g8-whole-numbers-02"}:
        params = question["whiteboard"]["visualization"]["parameters"]
        scene = json.loads(params["scene_json"])
        for key in ("answer", "memo", "actions", "factors", "property"):
            scene.pop(key, None)
        params["scene_json"] = json.dumps(scene, ensure_ascii=False)
    if lesson_id in {
        "g8-graphs-03",
        "g8-graphs-04",
        "g8-graphs-05",
        "g8-graphs-06",
        "g8-patterns-01",
        "g8-patterns-02",
        "g8-patterns-03",
        "g8-patterns-04",
        "g8-patterns-05",
        "g8-patterns-06",
        "g8-whole-numbers-01",
        "g8-whole-numbers-02",
        "g8-integers-01",
        "g8-integers-02",
    }:
        params = question["whiteboard"]["visualization"]["parameters"]
        scene = json.loads(params["scene_json"])
        for private_key in (
            ("answer", "memo", "actions", "repair", "misconception", "rule", "a", "b")
            if lesson_id == "g8-patterns-03"
            else (
                (
                    "answer",
                    "memo",
                    "actions",
                    "repair",
                    "misconception",
                    "correct_label",
                    "wrong_index",
                    "rule",
                    "a",
                    "b",
                    "family",
                )
                if lesson_id
                in {
                    "g8-patterns-05",
                    "g8-patterns-06",
                    "g8-whole-numbers-01",
                    "g8-whole-numbers-02",
                    "g8-integers-01",
                    "g8-integers-02",
                }
                else ("answer", "memo", "actions", "repair", "misconception")
            )
        ):
            scene.pop(private_key, None)
        params["scene_json"] = json.dumps(scene, ensure_ascii=False)
    if lesson_id in {"g8-functions-relationships-05", "g8-functions-relationships-06"}:
        visual = question["whiteboard"]["visualization"]
        params = visual["parameters"]
        params["derived_objects"] = ["?" for _ in params["derived_objects"]]
        scene = json.loads(params["scene_json"])
        scene.pop("chosen", None)
        for path in scene["candidates"]:
            path.pop("value", None)
            if scene["mode"] == "repair" and path is scene["candidates"][1]:
                path["label"] = "Repair path"
        params["scene_json"] = json.dumps(scene, ensure_ascii=False)
    question["whiteboard"]["semantic_objects"] = [
        item
        for item in question["whiteboard"]["semantic_objects"]
        if item["id"] in {"problem", "stage-01"}
    ]
