"""Typed curriculum, lesson-block and whiteboard contracts."""

from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator


class ContentStatus(StrEnum):
    COMING_SOON = "coming_soon"
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
    action: Literal[
        "show_object", "highlight_expression", "evaluate_expression", "transform_expression",
        "add_to_both_sides", "remove_from_both_sides", "divide_both_sides",
        "substitute_value", "compare_values", "balance_scale", "verify_solution",
        "form_equation", "diagnose_error", "group_equal_terms",
    ] | None = None


class VisualizationInstruction(BaseModel):
    type: Literal["geometry", "coordinate_geometry", "function_graph", "trigonometry", "statistics", "probability", "calculus", "sequences", "finance", "algebra"]
    template: str = Field(pattern=r"^[a-z][a-z0-9_]*$")
    parameters: dict[str, int | float | str | bool | list[int | float | str | bool]] = Field(default_factory=dict)


class VisualizationState(BaseModel):
    objects: list[str] = Field(default_factory=list)
    highlights: list[str] = Field(default_factory=list)
    annotations: list[str] = Field(default_factory=list)
    target: str | None = None
    before_state: str | None = None
    working_state: str | None = None
    after_state: str | None = None


TimelineEventType = Literal[
    "show_question", "set_goal", "focus", "dim", "reveal", "write", "replace", "simplify", "substitute", "show_operation",
    "calculate_difference", "calculate_ratio",
    "draw_arrow", "apply_both_sides", "cancel", "move", "align",
    "compare", "group", "plot_point", "draw_curve", "draw_asymptote",
    "shade", "shade_region", "fill_area", "pause", "narration", "caption",
    "checkpoint", "verify", "complete",
    "place_cashflow", "set_focal_date", "label_period", "match_rate_period",
    "count_payments", "accumulate", "discount", "split_phase", "mark_payment",
    "highlight_remaining_payments", "calculate", "compare_options", "verify_financial_sense",
    "plot_function", "place_curve_point", "draw_secant", "show_change_triangle",
    "move_point", "approach_limit", "draw_tangent", "differentiate_term",
    "substitute_derivative_value", "solve_derivative_zero", "test_derivative_sign",
    "classify_stationary", "shade_concavity", "mark_inflection", "build_objective",
    "mark_feasible_domain", "compare_boundaries", "verify_calculus_sense", "factor_common",
    "factor", "mark_restriction", "branch_zero_product", "highlight_discriminant",
    "draw_number_line", "mark_endpoint", "back_substitute", "verify_original",
    "factor_expression", "split_zero_product", "calculate_discriminant",
    "branch_roots", "mark_number_line", "shade_interval", "reject_candidate",
    "pair_solutions", "preserve_restriction",
    "focus_object", "evaluate_expression", "introduce_inverse", "apply_to_both_sides",
    "cancel_inverse_pair", "simplify_expression", "substitute_value",
    "replace_unknown", "reverse_equality", "compare_both_sides",
    "tilt_balance", "restore_balance", "mark_incorrect_step",
    "repair_incorrect_step", "show_conclusion",
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
    internal_instruction: str | None = Field(default=None, exclude=True, repr=False)

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
        factored_targets: set[str] = set()
        for event in self.events:
            if event.type == "apply_both_sides":
                applied_targets.update(event.targets)
            if event.type == "factor_common":
                factored_targets.update(event.targets)
            if event.type == "cancel" and not set(event.targets).issubset(applied_targets | factored_targets):
                raise ValueError("Cancellation requires an earlier matching operation or common factor")
        return self


class FormulaUnderstanding(BaseModel):
    meaning: str = Field(min_length=1, max_length=1_000)
    origin: str = Field(min_length=1, max_length=1_500)
    formula: str = Field(min_length=1, max_length=500)
    symbol_anatomy: list[str] = Field(min_length=1, max_length=20)
    why_it_works: str = Field(min_length=1, max_length=1_500)
    validity_conditions: list[str] = Field(min_length=1, max_length=12)
    selection_reason: str = Field(min_length=1, max_length=1_000)
    wrong_use_cases: list[str] = Field(min_length=1, max_length=12)
    visual_model: dict[str, str] = Field(min_length=1, max_length=12)
    verification: dict[str, str] = Field(min_length=1, max_length=12)


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
    formula_understanding: FormulaUnderstanding | None = None

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
    operation_signature: list[str] = Field(default_factory=list)
    expected_evidence: str | None = None
    answer_tolerance: float | None = Field(default=None, ge=0)
    approximate_answer: bool = False


class PresentationSemanticObject(BaseModel):
    id: str = Field(pattern=r"^[a-z][a-z0-9_-]*$")
    type: str = Field(pattern=r"^[a-z][a-z0-9_]*$")
    accessible_label: str = Field(min_length=1)


class PresentationEvent(BaseModel):
    event_id: str = Field(pattern=r"^[a-z][a-z0-9_-]*$")
    sequence: int = Field(ge=1)
    event_type: str = Field(pattern=r"^[a-z][a-z0-9_]*$")
    visual_instruction: str = Field(min_length=1)
    semantic_object_ids: list[str] = Field(default_factory=list)
    hold_after: bool = False


class VoiceCue(BaseModel):
    cue_id: str = Field(pattern=r"^[a-z][a-z0-9_-]*$")
    start_event: str
    end_event: str
    spoken_text: str = Field(min_length=1)
    caption_text: str = Field(min_length=1)
    pronunciation_hints: list[str] = Field(default_factory=list)
    interruptible: bool = True
    wait_for_user: bool = False
    silence_during_motion: bool = True


class PresentationContract(BaseModel):
    paper: Literal["Paper 2"]
    canvas_family: str = Field(pattern=r"^[a-z][a-z0-9_]*$")
    semantic_objects: list[PresentationSemanticObject] = Field(min_length=1)
    events: list[PresentationEvent] = Field(min_length=1)
    voice_cues: list[VoiceCue] = Field(min_length=1)
    reduced_motion_sequence: list[str] = Field(min_length=1)
    animation_choreography: str = Field(min_length=1)
    voice_direction: str = Field(min_length=1)
    prohibited_fallback: str = Field(min_length=1)
    question_first: bool = True
    future_engine_status: Literal["specified_not_activated"] = "specified_not_activated"

    @model_validator(mode="after")
    def validate_references(self):
        object_ids = {item.id for item in self.semantic_objects}
        event_ids = {item.event_id for item in self.events}
        if len(object_ids) != len(self.semantic_objects) or len(event_ids) != len(self.events):
            raise ValueError("Presentation object and event IDs must be unique")
        for event in self.events:
            missing = set(event.semantic_object_ids) - object_ids
            if missing:
                raise ValueError(f"Presentation event targets do not exist: {sorted(missing)}")
        for cue in self.voice_cues:
            missing = {cue.start_event, cue.end_event} - event_ids
            if missing:
                raise ValueError(f"Voice cue events do not exist: {sorted(missing)}")
            if cue.spoken_text != cue.caption_text:
                raise ValueError("Future voice captions must match spoken text")
        return self


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
    paper: Literal["Paper 1", "Paper 2"] | None = None
    presentation_contract: PresentationContract | None = None
    source_document: str | None = None
    source_sha256: str | None = Field(default=None, pattern=r"^[a-f0-9]{64}$")
    assessment_contract: dict[str, Any] = Field(default_factory=dict)
    release_approved: bool = False

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
    paper: Literal["Paper 1", "Paper 2", "Both", "Readiness"] | None = None
    paper_number: Literal[1, 2] | None = None
    grade: int | None = Field(default=None, ge=8, le=12)
    subject: Literal["Mathematics"] | None = None
    official_weighting: int | None = Field(default=None, ge=0, le=150)
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
