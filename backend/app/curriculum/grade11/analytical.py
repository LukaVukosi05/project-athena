"""Original Grade 11 Topic 5 lessons, held for teacher review."""
from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path

from app.curriculum.schemas import (
    AccessLevel, ContentStatus, GradeCurriculum, Lesson, LessonBlock, MathematicalOperation,
    SemanticObject, StepExplanation, Subtopic, TeachingStep, TimelineEvent, Topic,
    VisualizationInstruction, VisualizationState, WhiteboardBlock, WhiteboardQuestion,
)

ROOT = Path(__file__).resolve().parents[4]
SOURCE = ROOT / "docs/curriculum/grade11/analytical-geometry"
DATA = Path(__file__).with_name("generated")
TITLES = (
    "Distance between two points",
    "Gradient and direction of a line segment",
    "Midpoints and missing endpoints",
    "Equation of a line through two points",
    "Parallel and perpendicular lines through a point",
    "Inclination from exact gradients",
)


def build_lesson(number: int) -> tuple[Lesson, dict]:
    data = json.loads((DATA / f"analytical_{number:02}.json").read_text(encoding="utf-8"))
    source = SOURCE / data["source"]
    lesson_id = f"g11-ag-{number:02}"
    questions = []
    for order, scene in enumerate(data["worked"], 1):
        qid = scene["id"]
        actions = scene["actions"]
        ids = ["problem", "model", "operation", "result", "verification"]
        objects = [SemanticObject(id=identifier, type="verification" if identifier == "verification" else
                                  "result" if identifier == "result" else "operation" if identifier == "operation" else "label",
                                  value=identifier) for identifier in ids]
        steps = []
        previous = "Read the original question"
        for index, action in enumerate(actions, 1):
            after = f"{index}. {action}"
            narration = action
            duration = max(5500, min(22000, len(narration.split()) * 550))
            final = index == len(actions)
            steps.append(TeachingStep(
                id=f"{qid}-step-{index:02}", step_number=index - 1, title=action,
                before_expression=previous, working_expression=action,
                operation=MathematicalOperation(type=f"grade11_ag_{number}_step",
                    action="verify_solution" if final else "transform_expression", value=action),
                after_expression=after, explanation=StepExplanation(
                    what=action, why="Use the actual plotted coordinates and name the relevant coordinate formula.",
                    purpose=action, remember="Check both original points, signs and the final equation."),
                animation_template=f"grade11_ag_{number}", screen_reader_description=narration,
                visualization_state=VisualizationState(objects=ids, highlights=["model"],
                    annotations=[f"stage:{index}"], target="model", before_state=previous,
                    working_state=action, after_state=after),
                instructional_goal=action, duration_ms=duration,
                events=[TimelineEvent(at_ms=0, type="caption", text=narration),
                        TimelineEvent(at_ms=0, type="narration", text=narration),
                        TimelineEvent(at_ms=350, type="focus", targets=["model"]),
                        TimelineEvent(at_ms=1100, type="show_operation", targets=["operation"], label=action[:200]),
                        TimelineEvent(at_ms=duration - 600, type="reveal", targets=["result"], label=after[:200]),
                        TimelineEvent(at_ms=duration - 120, type="verify" if final else "complete",
                                      targets=["verification" if final else "result"])],
                narration=narration, state_after={"stage":index, "question_id":qid,
                    "verification_complete":final, "verification_link":scene["check"] if final else "",
                    "completion_state":after},
            ))
            previous = after
        board = WhiteboardBlock(id=f"{qid}-board", representation="visual", problem=scene["problem"],
            initial_expression="Read the original question", steps=steps, semantic_objects=objects,
            visualization=VisualizationInstruction(type="coordinate_geometry", template=f"grade11_ag_{number}",
                parameters={"scene_json":json.dumps(scene, ensure_ascii=False), "question_id":qid,
                            "prompt":scene["problem"], "total_steps":len(actions)}))
        questions.append(WhiteboardQuestion(id=qid, order=order, difficulty=scene["difficulty"],
            is_core_example=order == 1, guidance_level="high" if order <= 5 else "reduced",
            cognitive_level="knowledge" if order <= 3 else "routine" if order <= 8 else "complex",
            marks=2 if order <= 3 else 4 if order <= 10 else 6, whiteboard=board,
            answer=scene["answer"], full_memo=actions,
            misconception_tags=["grade11-analytical-geometry"], expected_evidence=scene["check"]))
    lesson = Lesson(id=lesson_id, order=number, title=TITLES[number-1], estimated_minutes=75,
        objective=f"Explain and verify {TITLES[number-1].lower()} with exact mathematical steps.",
        why_it_matters="Coordinate proofs support Grade 11 analytical geometry and later NSC examinations.",
        intuition="Keep the original points, plotted segment and cumulative calculation visible together.",
        prerequisites=[] if number == 1 else [f"g11-ag-{number-1:02}"],
        difficulty="foundation" if number == 1 else "standard",
        access_level=AccessLevel.FREE if number == 1 else AccessLevel.PREMIUM,
        status=ContentStatus.TEACHER_REVIEW_REQUIRED, release_approved=False,
        blocks=[LessonBlock(type="concept", title=TITLES[number-1],
                            content="Plot the original points, predict one construction, then check its reason."),
                questions[0].whiteboard,
                LessonBlock(type="practice", title="Work in your book, then choose",
                            content="Choose one of four answers after working independently.",
                            data={"practice_bank_id":lesson_id}),
                LessonBlock(type="summary", title="Verify", content="Check in the original expression.")],
        whiteboard_questions=questions, mastery_threshold=.8, paper="Paper 2",
        source_document=source.name, source_sha256=sha256(source.read_bytes()).hexdigest(),
        assessment_contract={"worked_example_count":15, "practice_count":15,
            "mastery_question_count":5, "parallel_reassessment_count":3,
            "answer_hidden_before_submission":True, "progression_threshold":.8})
    return lesson, data


LESSONS = {number:build_lesson(number) for number in range(1, 7)}
TOPIC = Topic(id="analytical-geometry", product_order=5, title="Analytical Geometry",
        official_caps_topic="Analytical Geometry", caps_sequence=5, term=2, paper="Paper 2",
        caps_reference="DBE Grade 11 Mathematics ATP, Term 2",
        expected_duration="Six authored lessons awaiting teacher and browser review",
        exam_relevance="Grade 11 Paper 2 analytical geometry and formal assessment",
        status=ContentStatus.TEACHER_REVIEW_REQUIRED,
        subtopics=[Subtopic(id="analytical-geometry-learning-path", order=1,
            title="Distance, gradient, midpoint, line equations and inclination",
            lessons=[LESSONS[number][0] for number in range(1, 7)])])
