"""Allow-listed operation-to-animation registry."""

from collections.abc import Callable
from app.curriculum.schemas import TeachingStep, WhiteboardBlock
from app.whiteboard.linear_equations import verify_equivalent_transition, verify_linear_transition

StepValidator = Callable[[TeachingStep], bool]


class AnimationRegistry:
    def __init__(self):
        self._operations: dict[str, tuple[str, StepValidator]] = {}

    def register(self, operation: str, template: str, validator: StepValidator) -> None:
        if operation in self._operations:
            raise ValueError(f"Operation already registered: {operation}")
        self._operations[operation] = (template, validator)

    def validate(self, plan: WhiteboardBlock) -> None:
        for step in plan.steps:
            registered = self._operations.get(step.operation.type)
            if registered is None:
                raise ValueError(f"Unknown whiteboard operation: {step.operation.type}")
            template, validator = registered
            if template != step.animation_template:
                raise ValueError(f"Template mismatch for {step.operation.type}")
            if not validator(step):
                raise ValueError(f"Invalid transition at step {step.step_number}")


registry = AnimationRegistry()
registry.register("identify_objective", "identify_unknown", lambda step: step.before_expression == step.after_expression)
registry.register("subtract_both_sides", "equation_balance_subtraction", verify_linear_transition)
registry.register("divide_both_sides", "equation_balance_division", verify_linear_transition)
registry.register("equivalent_transform", "equation_transformation", verify_equivalent_transition)
registry.register("present_expression", "expression_presentation", lambda step: step.before_expression == step.after_expression)
registry.register("identity_recognition", "identity_highlight", lambda step: bool(step.operation.value) and step.after_expression == step.operation.value)
registry.register("state_simplified_result", "simplified_result", lambda step: step.after_expression.startswith("∴ "))
registry.register("build_geometry_scene", "geometry_scene", lambda step: step.before_expression == step.after_expression)
registry.register("highlight_geometry", "geometry_highlight", lambda step: bool(step.visualization_state and step.visualization_state.highlights))
registry.register("apply_geometry_theorem", "geometry_theorem", lambda step: bool(step.after_expression))
registry.register("solve_geometry", "geometry_solution", lambda step: bool(step.after_expression and step.visualization_state and "solution" in step.visualization_state.annotations))
registry.register("complete_geometry", "geometry_complete", lambda step: bool(step.after_expression and step.visualization_state and "answer" in step.visualization_state.annotations))
registry.register("substitute_value", "substitution_verification", lambda step: "✓" in step.after_expression)
registry.register("identify_interval", "rate_change_setup", lambda step: step.before_expression == step.after_expression)
registry.register("substitute_function_value", "function_substitution", lambda step: step.operation.value is not None)
registry.register("calculate_average_rate", "average_rate_quotient", lambda step: "per" in step.after_expression)
registry.register("interpret_rate", "rate_interpretation", lambda step: bool(step.after_expression))
registry.register("read_problem", "problem_annotation", lambda step: bool(step.after_expression))
registry.register("timeline_orient", "semantic_timeline", lambda step: bool(step.events and step.instructional_goal))
registry.register("timeline_inspect", "semantic_timeline", lambda step: bool(step.events and any(event.type in {"focus", "draw_arrow", "compare"} for event in step.events)))
registry.register("timeline_select", "semantic_timeline", lambda step: bool(step.events and step.state_after))
registry.register("timeline_verify", "semantic_timeline", lambda step: bool(step.events and any(event.type == "verify" for event in step.events)))
registry.register("timeline_summarize", "semantic_timeline", lambda step: bool(step.events and step.after_expression))
registry.register("select_method", "method_selection", lambda step: bool(step.after_expression))
registry.register("show_working", "progressive_working", lambda step: "∴" in step.after_expression)
registry.register("verify_result", "result_verification", lambda step: "✓" in step.after_expression)
registry.register("draw_secant", "secant_line", lambda step: step.before_expression == step.after_expression)
registry.register("calculate_secant_gradient", "secant_gradient", lambda step: "h≠0" in step.after_expression)
registry.register("approach_limit", "secant_approaches_tangent", lambda step: "→" in step.after_expression)
registry.register("draw_tangent", "tangent_at_point", lambda step: "f′" in step.after_expression)
