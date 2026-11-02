"""Grade 8 graph-from-table whiteboard, authored from Athena's scene pack."""
import hashlib
import json
from pathlib import Path

from app.curriculum.schemas import (
    AccessLevel, ContentStatus, Lesson, LessonBlock, MathematicalOperation,
    SemanticObject, StepExplanation, TeachingStep, TimelineEvent,
    VisualizationInstruction, VisualizationState, WhiteboardBlock, WhiteboardQuestion,
)

ROOT = Path(__file__).resolve().parents[4]
SOURCE = ROOT / "docs/curriculum/grade8/graphs/lesson-02-tables-to-graphs.md"
SCENES = ROOT / "docs/curriculum/grade8/graphs/lesson-02-scenes.json"
LESSON_ID = "g8-graphs-02"
SCENE_DATA = json.loads(SCENES.read_text(encoding="utf-8"))["scenes"]


def _question(scene, number):
    qid = f"g8-graphs-l02-w{number:02}"
    if scene["id"] != qid or len(scene["actions"]) != 4:
        raise ValueError(f"{qid}: scene ID or teaching sequence invalid")
    pairs = [(row["x"], row["y"]) for row in scene["graph"]["table"]]
    if pairs != [(row["x"], row["y"]) for row in scene["graph"]["points"]]:
        raise ValueError(f"{qid}: graph disagrees with the source table")
    objects = [SemanticObject(id=key, type=kind, value=value, group=group) for key, kind, value, group in [
        ("problem", "label", scene["problem"][:160], "given"),
        ("model", "label", "Table and Cartesian plane", "visual"),
        ("operation", "operation", "Current graph action", "working"),
        ("result", "result", "Result of graph action", "working"),
        ("verification", "verification", "Check each table column and graph", "check"),
    ]]
    for idx, point in enumerate(scene["given"], 1):
        objects.append(SemanticObject(id=f"given-point-{idx}", type="position", value=point["label"], group="given"))
    for idx, point in enumerate(scene["derived"], 1):
        objects.append(SemanticObject(id=f"target-{idx}", type="position", value=point["label"], group="derived"))
    steps=[]
    before="Read the table and both labelled axes"
    for idx, action in enumerate(scene["actions"], 1):
        last=idx==4
        after=f"{idx}. {action}" if not last else f"Verified: {scene['memo']}"
        narration=action if not last else f"{action} Check the source table: {scene['memo']}"
        duration=max(4800,len(narration.split())*390)
        events=[TimelineEvent(at_ms=0,type="caption",text=narration), TimelineEvent(at_ms=0,type="narration",text=narration),
            TimelineEvent(at_ms=250,type="focus",targets=["model"]),
            TimelineEvent(at_ms=900,type="show_operation",targets=["operation"],label=action),
            TimelineEvent(at_ms=duration//2,type="reveal",targets=["result"],label=after[:240]),
            TimelineEvent(at_ms=duration-200,type="verify" if last else "complete",targets=["verification"] if last else ["result"]) ]
        steps.append(TeachingStep(id=f"{qid}-step-{idx:02}",step_number=idx-1,title="Check the table and graph" if last else action,
            before_expression=before,working_expression=action,
            operation=MathematicalOperation(type="coordinate_plot_step",value=action,
                action="verify_solution" if last else "transform_expression"),after_expression=after,
            explanation=StepExplanation(what=narration,why="Each plotted coordinate comes from one matched input-output column.",
                purpose=action,remember=scene["repair"]),common_mistake=scene["misconception"],
            animation_template="grade8_coordinate_plane",screen_reader_description=f"{before}. {narration} {after}.",
            visualization_state=VisualizationState(objects=[o.id for o in objects],highlights=["model"],annotations=[f"stage:{idx}"],target="model",before_state=before,working_state=action,after_state=after),
            instructional_goal=narration,duration_ms=duration,events=events,narration=narration,
            state_after={"stage":idx,"question_id":qid,"verification_complete":last,
                "verification_link":scene["memo"],"completion_state":after}))
        before=after
    board=WhiteboardBlock(id=f"{qid}-board",representation="visual",problem=scene["problem"],
        initial_expression="Read the table and both labelled axes",steps=steps,
        visualization=VisualizationInstruction(type="coordinate_geometry",template="grade8_coordinate_plane",
            parameters={"scene_json":json.dumps(scene,ensure_ascii=False),"question_id":qid,
                "prompt":scene["problem"],"total_steps":4}),semantic_objects=objects)
    level="foundation" if number==1 else "easy" if number<=3 else "standard" if number<=6 else "intermediate" if number<=9 else "exam" if number<=12 else "advanced"
    return WhiteboardQuestion(id=qid,order=number,difficulty=level,is_core_example=number==1,
        guidance_level="high" if number<=5 else "moderate" if number<=10 else "reduced",whiteboard=board,
        cognitive_level="knowledge" if number<=3 else "routine" if number<=6 else "complex" if number<=12 else "problem_solving",
        marks=scene["marks"],answer=scene["memo"],full_memo=[*scene["actions"],f"Verify: {scene['memo']}"],
        misconception_tags=[scene["misconception"]],expected_evidence=scene["memo"])


QUESTIONS=[_question(scene,n) for n,scene in enumerate(SCENE_DATA,1)]
LESSON=Lesson(id=LESSON_ID,order=2,title="Plotting graphs from tables",
    objective="Match input-output columns, plot ordered pairs at correct scales, draw a line when justified and read a table from a graph.",
    why_it_matters="A graph communicates how one quantity changes with another, provided each coordinate and connecting line is justified.",
    intuition="Keep each table column together. Place x first and y second. Check whether values between plotted inputs make sense before joining dots.",
    prerequisites=["g8-graphs-01","g8-functions-relationships-03"],estimated_minutes=85,
    difficulty="standard",access_level=AccessLevel.PREMIUM,status=ContentStatus.TEACHER_REVIEW_REQUIRED,
    blocks=[LessonBlock(type="concept",title="From a column to a plotted pair",content="Read one input-output column together, locate x then y, and retain that point before moving to the next column."),
        QUESTIONS[0].whiteboard,
        LessonBlock(type="mistake",title="When to connect dots",content="A straight line requires a straight relationship and meaningful intermediate inputs. Whole ticket counts remain separate points; unequal rises cannot all share one straight line."),
        LessonBlock(type="practice",title="Plot, read and decide",content="Complete the independent questions before revealing each solution.",data={"practice_bank_id":LESSON_ID}),
        LessonBlock(type="summary",title="Check the original table",content="Read every plotted point back against its table column, axis scale and domain.")],
    whiteboard_questions=QUESTIONS,mastery_threshold=.8,paper=None,
    source_document=SOURCE.name,source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),release_approved=False,
    assessment_contract={"worked_example_count":15,"practice_count":15,"mastery_question_count":5,
        "parallel_reassessment_count":3,"answer_hidden_before_submission":True,"progression_threshold":.8,
        "runtime_conversion":"graphs_lesson_2_teacher_review"})
