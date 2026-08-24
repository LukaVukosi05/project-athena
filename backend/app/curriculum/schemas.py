"""Typed curriculum, lesson-block and whiteboard contracts."""

from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator


class ContentStatus(StrEnum):
    DRAFT = "draft"
    AI_ASSISTED = "ai_assisted"
    TEACHER_REVIEW_REQUIRED = "teacher_review_required"
    REVIEWED = "reviewed"
    APPROVED = "approved"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class AccessLevel(StrEnum):
    FREE = "free"
    PREMIUM = "premium"


class StepExplanation(BaseModel):
    what: str = Field(min_length=1)
    why: str = Field(min_length=1)
    purpose: str = Field(min_length=1)
    remember: str = Field(min_length=1)


class MathematicalOperation(BaseModel):
    type: str = Field(pattern=r"^[a-z][a-z0-9_]*$")
    value: int | float | str | None = None


class VisualizationInstruction(BaseModel):
    type: Literal["geometry", "coordinate_geometry", "function_graph", "trigonometry", "statistics", "probability", "calculus", "sequences"]
    template: str = Field(pattern=r"^[a-z][a-z0-9_]*$")
    parameters: dict[str, int | float | str | bool | list[int | float | str | bool]] = Field(default_factory=dict)


class VisualizationState(BaseModel):
    objects: list[str] = Field(default_factory=list)
    highlights: list[str] = Field(default_factory=list)
    annotations: list[str] = Field(default_factory=list)


TimelineEventType = Literal[
    "focus", "dim", "reveal", "write", "replace", "substitute", "show_operation",
    "calculate_difference", "calculate_ratio",
    "draw_arrow", "apply_both_sides", "cancel", "move", "align",
    "compare", "group", "plot_point", "draw_curve", "draw_asymptote",
    "shade", "shade_region", "fill_area", "pause", "narration", "caption",
    "checkpoint", "verify",
]


class TimelineEvent(BaseModel):
    at_ms: int = Field(ge=0, le=120_000)
    type: TimelineEventType
    targets: list[str] = Field(default_factory=list, max_length=30)
    from_target: str | None = None
    to_target: str | None = None
    label: str | None = Field(default=None, max_length=240)
    text: str | None = Field(default=None, max_length=1_000)
    style: Literal["given", "target", "operation", "matching_pattern", "result", "verification", "muted"] | None = None
    checkpoint_type: Literal["predict_next_step", "select_operation", "calculate_value", "identify_pattern", "choose_graph", "spot_error", "explain_reason"] | None = None

    @model_validator(mode="after")
    def validate_shape(self):
        if self.type == "draw_arrow" and not (self.from_target and self.to_target):
            raise ValueError("draw_arrow requires from_target and to_target")
        if self.type in {"narration", "caption"} and not self.text:
            raise ValueError(f"{self.type} requires text")
        if self.type == "checkpoint" and not (self.text and self.checkpoint_type):
            raise ValueError("checkpoint requires text and checkpoint_type")
        if self.type == "apply_both_sides" and len(self.targets) < 2:
            raise ValueError("apply_both_sides requires targets on both equation sides")
        return self


class SemanticObject(BaseModel):
    id: str = Field(pattern=r"^[a-z][a-z0-9_-]*$")
    type: Literal["term", "position", "difference", "ratio", "token", "label", "operation", "result", "verification"]
    value: str = Field(min_length=1, max_length=160)
    group: str | None = Field(default=None, max_length=80)


class TeachingStep(BaseModel):
    step_number: int = Field(ge=0)
    title: str
    before_expression: str
    working_expression: str | None = None
    operation: MathematicalOperation
    after_expression: str
    explanation: StepExplanation
    common_mistake: str | None = None
    animation_template: str
    screen_reader_description: str
    visualization_state: VisualizationState | None = None
    id: str | None = Field(default=None, pattern=r"^[a-z][a-z0-9_-]*$")
    instructional_goal: str | None = Field(default=None, max_length=500)
    duration_ms: int = Field(default=0, ge=0, le=120_000)
    events: list[TimelineEvent] = Field(default_factory=list, max_length=80)
    narration: str | None = Field(default=None, max_length=2_000)
    narration_audio_url: str | None = Field(default=None, pattern=r"^/assets/narration/[a-z0-9/_-]+\.mp3$")
    state_after: dict[str, int | float | str | bool | list[int | float | str | bool]] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_timeline(self):
        times = [event.at_ms for event in self.events]
        if times != sorted(times):
            raise ValueError("Timeline events must be ordered by at_ms")
        if times and self.duration_ms < times[-1]:
            raise ValueError("Step duration must include its final timeline event")
        narration = " ".join(event.text for event in self.events if event.type == "narration" and event.text)
        captions = " ".join(event.text for event in self.events if event.type == "caption" and event.text)
        if narration and captions and narration != captions:
            raise ValueError("Timeline captions must match narration text")
        applied_targets: set[str] = set()
        for event in self.events:
            if event.type == "apply_both_sides":
                applied_targets.update(event.targets)
            if event.type == "cancel" and not set(event.targets).issubset(applied_targets):
                raise ValueError("Cancellation requires an earlier matching operation")
        return self


class WhiteboardBlock(BaseModel):
    type: Literal["whiteboard"] = "whiteboard"
    id: str
    representation: Literal["symbolic", "visual"] = "symbolic"
    problem: str
    initial_expression: str
    steps: list[TeachingStep] = Field(min_length=1)
    graph_spec: dict[str, Any] | None = None
    visualization: VisualizationInstruction | None = None
    semantic_objects: list[SemanticObject] = Field(default_factory=list, max_length=200)

    @model_validator(mode="after")
    def validate_state_chain(self):
        if self.representation == "visual" and self.visualization is None:
            raise ValueError("VISUALIZATION_REQUIRED_BUT_MISSING")
        expected = list(range(len(self.steps)))
        if [step.step_number for step in self.steps] != expected:
            raise ValueError("Whiteboard step numbers must be contiguous from zero")
        if self.steps[0].before_expression != self.initial_expression:
            raise ValueError("First step must begin at the initial expression")
        for previous, current in zip(self.steps, self.steps[1:]):
            if previous.after_expression != current.before_expression:
                raise ValueError("Whiteboard states must form a deterministic chain")
        object_ids = {item.id for item in self.semantic_objects}
        if len(object_ids) != len(self.semantic_objects):
            raise ValueError("Semantic object IDs must be unique")
        for step in self.steps:
            for event in step.events:
                referenced = [*event.targets, event.from_target, event.to_target]
                missing = {target for target in referenced if target and target not in object_ids}
                if missing:
                    raise ValueError(f"Timeline event targets do not exist: {sorted(missing)}")
        return self


class WhiteboardQuestion(BaseModel):
    id: str
    order: int = Field(ge=1)
    difficulty: Literal["foundation", "easy", "standard", "intermediate", "exam", "advanced", "expert"]
    estimated_minutes: int = Field(default=4, ge=1, le=20)
    is_core_example: bool = False
    guidance_level: Literal["high", "moderate", "reduced", "minimal"] = "high"
    whiteboard: WhiteboardBlock
    cognitive_level: Literal["knowledge", "routine", "complex", "problem_solving"] = "routine"
    marks: int = Field(default=2, ge=1, le=20)
    answer: str | None = None
    full_memo: list[str] = Field(default_factory=list)
    misconception_tags: list[str] = Field(default_factory=list)
    calculator_allowed: bool = False


class LessonBlock(BaseModel):
    type: Literal["concept", "checkpoint", "practice", "mistake", "memory_tip", "summary", "past_paper_question"]
    title: str
    content: str
    data: dict[str, Any] = Field(default_factory=dict)


class Lesson(BaseModel):
    id: str
    order: int = Field(ge=1)
    title: str
    objective: str
    why_it_matters: str
    intuition: str
    prerequisites: list[str] = Field(default_factory=list)
    estimated_minutes: int | None = Field(default=None, ge=1)
    difficulty: Literal["foundation", "standard", "exam", "challenge"]
    access_level: AccessLevel
    status: ContentStatus
    blocks: list[LessonBlock | WhiteboardBlock]
    whiteboard_questions: list[WhiteboardQuestion] = Field(default_factory=list, max_length=15)
    mastery_threshold: float = Field(default=0.7, ge=0, le=1)

    @model_validator(mode="after")
    def validate_whiteboard_question_set(self):
        if self.whiteboard_questions:
            orders = [question.order for question in self.whiteboard_questions]
            if orders != list(range(1, len(orders) + 1)):
                raise ValueError("Whiteboard question order must be contiguous from one")
            if sum(question.is_core_example for question in self.whiteboard_questions) != 1:
                raise ValueError("A whiteboard question set must have exactly one core example")
        return self


class Subtopic(BaseModel):
    id: str
    order: int = Field(ge=1)
    title: str
    prerequisites: list[str] = Field(default_factory=list)
    lessons: list[Lesson] = Field(default_factory=list)


class Topic(BaseModel):
    id: str
    product_order: int = Field(ge=0)
    title: str
    official_caps_topic: str | None = None
    caps_sequence: int | None = None
    term: int | None = Field(default=None, ge=1, le=4)
    expected_duration: str | None = None
    paper: Literal["Paper 1", "Paper 2", "Both", "Readiness"]
    caps_reference: str | None = None
    curriculum: Literal["CAPS"] = "CAPS"
    ieb_relevant: bool = True
    ieb_notes: str | None = None
    ieb_assessment_tags: list[str] = Field(default_factory=list)
    exam_relevance: str | None = None
    status: ContentStatus
    subtopics: list[Subtopic]


class GradeCurriculum(BaseModel):
    id: str
    grade: int = Field(ge=8, le=12)
    subject: Literal["Mathematics"] = "Mathematics"
    status: ContentStatus
    topics: list[Topic]
