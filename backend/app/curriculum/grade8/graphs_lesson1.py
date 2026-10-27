"""Grade 8 Cartesian coordinates, authored from the reviewed-in-repository draft.

The source remains a teacher-review draft. Each worked example carries its own
coordinate scene and a deterministic sequence of mathematical actions.
"""
import hashlib
import json
import re
from pathlib import Path

from app.curriculum.schemas import (
    AccessLevel, ContentStatus, Lesson, LessonBlock, MathematicalOperation,
    SemanticObject, StepExplanation, TeachingStep, TimelineEvent,
    VisualizationInstruction, VisualizationState, WhiteboardBlock, WhiteboardQuestion,
)

ROOT = Path(__file__).resolve().parents[4]
SOURCE = ROOT / "docs/curriculum/grade8/graphs/lesson-01-cartesian-plane-draft.md"
SCENES = ROOT / "docs/curriculum/grade8/graphs/lesson-01-scenes.json"
LESSON_ID = "g8-graphs-01"


def _source_sections():
    source = SOURCE.read_text(encoding="utf-8")
    sections = re.findall(r"^### (\d\d) (.*?)(?=^### |^## Independent practice)", source, re.M | re.S)
    if len(sections) != 15:
        raise ValueError("g8-graphs-01 source must contain 15 worked examples")
    result = []
    for number, section in sections:
        question = re.search(r"\*\*Question \((\d+) marks\):\*\* (.*?)\n", section)
        memo = re.search(r"\*\*Memo:\*\* (.*?) \*\*Misconception:\*\* (.*?) \*\*Repair:\*\* (.*)", section, re.S)
        if not question or not memo:
            raise ValueError(f"g8-graphs-01 example {number} lacks question or memo")
        result.append((int(number), int(question[1]), question[2].strip(), *[v.strip() for v in memo.groups()]))
    return result


# One action at a time. These are question-specific; the scene controls the
# plotted values and reveal timing while these lines control the spoken proof.
ACTION_LINES = [
    ["Read the ordered pair A(2, 3)", "Move two units right from the origin", "Move three units up", "Plot A at (2, 3)"],
    ["Find the given dot B", "Project B to x = 3", "Project B to y = 1", "Read B as (3, 1)"],
    ["Read C(4, 0)", "Move four units right", "Zero means no vertical movement", "Plot C on the x-axis"],
    ["D stays on the vertical axis", "No horizontal movement gives x = 0", "Move five units down to y = −5", "Read D as (0, −5)"],
    ["Read E(−3, 2)", "Move three units left", "Move two units up", "Plot E in Quadrant II"],
    ["Read F(−2, −4)", "Move two units left", "Move four units down", "Plot F in Quadrant III"],
    ["Plot G: right three", "Plot G: down two to (3, −2)", "Start H from the origin and move left two", "Move H up three to (−2, 3)"],
    ["Read the x scale: two per interval", "Six means three intervals right", "Read the y scale: five per interval", "Ten means two intervals up; plot J"],
    ["Read both scales: two per interval", "−4 is two intervals left", "6 is three intervals up", "Plot K in Quadrant II"],
    ["Project P to x = −1", "Read P at y = 4", "Project Q: x = 0, y = −3", "Project R: x = 4, y = 0"],
    ["Compare the learner dot with (−3, 1)", "The first coordinate requires moving left three", "The second requires moving up one", "Plot the corrected M and retain the error"],
    ["Read axis units: minutes and kilometres", "Four minutes is two horizontal intervals", "Six kilometres is two vertical intervals", "Plot and interpret the single observation"],
    ["Locate given A at (−2, 3)", "Keep x fixed at −2", "Subtract three from y: 3 − 3 = 0", "Place B at (−2, 0)"],
    ["Locate the given point (0, −1)", "Stay on x = 0", "Move four units up: −1 + 4 = 3", "Place T at (0, 3)"],
    ["Keep A and B at their given positions", "Check the y scale: two per interval", "Learner C two squares down is at y = −4", "Correct C is one square down at (2, −2)"],
]


def _make_question(source, scene):
    number, marks, problem, memo, misconception, repair = source
    if scene["id"] != f"g8-graphs-l01-w{number:02}":
        raise ValueError(f"g8-graphs-01 scene mismatch at example {number}")
    actions = ACTION_LINES[number - 1]
    objects = [SemanticObject(id=key, type=kind, value=value, group=group) for key, kind, value, group in [
        ("problem", "label", problem[:160], "given"), ("model", "label", "Coordinate plane", "visual"),
        ("operation", "operation", "Current coordinate action", "working"),
        ("result", "result", "Current coordinate result", "working"),
        ("verification", "verification", "Read back the original question", "check"),
    ]]
    for idx, point in enumerate(scene["given"], 1):
        objects.append(SemanticObject(id=f"given-point-{idx}", type="position", value=point["label"], group="given"))
    for idx, point in enumerate(scene["derived"], 1):
        objects.append(SemanticObject(id=f"target-{idx}", type="position", value=point["label"], group="derived"))
    steps = []
    before = "Read the question and labelled axes"
    for idx, action in enumerate(actions, 1):
        last = idx == len(actions)
        after = f"{idx}. {action}" if not last else f"Verified: {memo}"
        narration = f"{action}. Read the axis labels and count the correct intervals before accepting this position." if not last else f"Check against the original question. {memo}"
        duration = max(4800, len(narration.split()) * 390)
        target = "result"
        events = [TimelineEvent(at_ms=0, type="caption", text=narration),
                  TimelineEvent(at_ms=0, type="narration", text=narration),
                  TimelineEvent(at_ms=250, type="focus", targets=["model"]),
                  TimelineEvent(at_ms=900, type="show_operation", targets=["operation"], label=action),
                  TimelineEvent(at_ms=duration // 2, type="reveal", targets=[target], label=after[:240]),
                  TimelineEvent(at_ms=duration - 200, type="verify" if last else "complete", targets=["verification"] if last else [target])]
        steps.append(TeachingStep(id=f"{scene['id']}-step-{idx:02}", step_number=idx-1,
            title="Check coordinates" if last else action, before_expression=before,
            working_expression=action,
            operation=MathematicalOperation(type="coordinate_plot_step", value=action,
                action="verify_solution" if last else "transform_expression"),
            after_expression=after,
            explanation=StepExplanation(what=narration, why="The axis labels and scales determine the position.",
                purpose=action, remember=repair), common_mistake=misconception,
            animation_template="grade8_coordinate_plane", screen_reader_description=f"{before}. {narration} {after}.",
            visualization_state=VisualizationState(objects=[o.id for o in objects], highlights=["model"],
                annotations=[f"stage:{idx}"], target="model", before_state=before,
                working_state=action, after_state=after),
            instructional_goal=narration, duration_ms=duration, events=events, narration=narration,
            state_after={"stage": idx, "question_id": scene["id"], "verification_complete": last,
                "verification_link": memo, "completion_state": after}))
        before = after
    board = WhiteboardBlock(id=f"{scene['id']}-board", representation="visual",
        problem=problem, initial_expression="Read the question and labelled axes", steps=steps,
        visualization=VisualizationInstruction(type="coordinate_geometry", template="grade8_coordinate_plane",
            parameters={"scene_json": json.dumps(scene, ensure_ascii=False), "question_id": scene["id"],
                "prompt": problem, "total_steps": len(steps)}),
        semantic_objects=objects)
    level = "foundation" if number == 1 else "easy" if number <= 3 else "standard" if number <= 6 else "intermediate" if number <= 9 else "exam" if number <= 12 else "advanced"
    return WhiteboardQuestion(id=scene["id"], order=number, difficulty=level,
        is_core_example=number == 1, guidance_level="high" if number <= 5 else "moderate" if number <= 10 else "reduced",
        whiteboard=board, cognitive_level="knowledge" if number <= 3 else "routine" if number <= 6 else "complex" if number <= 12 else "problem_solving",
        marks=marks, answer=memo, full_memo=[*actions, f"Verify: {memo}"],
        misconception_tags=[misconception], expected_evidence=memo)


SCENE_DATA = json.loads(SCENES.read_text(encoding="utf-8"))["scenes"]
QUESTIONS = [_make_question(source, scene) for source, scene in zip(_source_sections(), SCENE_DATA, strict=True)]
LESSON = Lesson(id=LESSON_ID, order=1, title="Cartesian coordinates and ordered pairs",
    objective="Read, plot and check ordered pairs on labelled Cartesian axes, including signed values, non-unit scales and context units.",
    why_it_matters="An incorrect coordinate or scale spoils every graph even when the underlying rule is correct.",
    intuition="Start at the origin. Move horizontally by x, then vertically by y. Read both tick scales and check against the original pair.",
    prerequisites=["integer number lines", "input-output tables"], estimated_minutes=80,
    difficulty="foundation", access_level=AccessLevel.FREE, status=ContentStatus.TEACHER_REVIEW_REQUIRED,
    blocks=[LessonBlock(type="concept", title="Across first, then up or down",
        content="The first coordinate gives the horizontal displacement; the second gives the vertical displacement. Read the axis labels and tick scale before plotting."),
        QUESTIONS[0].whiteboard,
        LessonBlock(type="mistake", title="Repair a misplaced point",
            content="Identify the first swapped coordinate, wrong sign or wrong tick interval; replot from the origin."),
        LessonBlock(type="practice", title="Plot and read independently",
            content="Try each fresh pair before requesting a hint or solution.", data={"practice_bank_id": LESSON_ID}),
        LessonBlock(type="summary", title="Check every plotted point",
            content="Project back to both labelled axes and verify the ordered pair, signs, scale and units.")],
    whiteboard_questions=QUESTIONS, mastery_threshold=.8, paper=None,
    source_document=SOURCE.name, source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    release_approved=False, assessment_contract={"worked_example_count": 15, "practice_count": 15,
        "mastery_question_count": 5, "parallel_reassessment_count": 3,
        "answer_hidden_before_submission": True, "progression_threshold": .8,
        "runtime_conversion": "graphs_lesson_1_teacher_review"})
