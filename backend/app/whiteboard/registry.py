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
registry.register("apply_both_sides_display", "equation_balance_display", verify_equivalent_transition)
registry.register("simplify_equation", "equation_simplification", verify_equivalent_transition)
registry.register("divide_both_sides_display", "equation_division_display", verify_equivalent_transition)
registry.register("verification_line", "equation_verification", lambda step: bool(step.after_expression.strip()))
registry.register("balance_focus_goal", "equation_focus", lambda step: step.before_expression == step.after_expression)
registry.register("balance_focus_constant", "equation_focus", lambda step: step.before_expression == step.after_expression)
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
for finance_operation in (
    "place_cashflow", "set_focal_date", "match_rate_period", "accumulate", "discount",
    "calculate", "verify_financial_sense", "label_period", "count_payments", "split_phase",
    "mark_payment", "highlight_remaining_payments", "compare_options",
):
    registry.register(finance_operation, "finance_timeline_reasoning", lambda step: bool(step.events and step.visualization_state))
for calculus_operation in (
    "plot_function", "place_curve_point", "show_change_triangle", "move_point",
    "differentiate_term", "substitute_derivative_value", "solve_derivative_zero",
    "test_derivative_sign", "classify_stationary", "shade_concavity", "mark_inflection",
    "build_objective", "mark_feasible_domain", "compare_boundaries",
    "verify_calculus_sense", "factor_common", "substitute", "cancel",
    "calculus_limit", "calculus_tangent",
):
    registry.register(calculus_operation, "calculus_timeline_reasoning", lambda step: bool(step.events and step.visualization_state))
for algebra_operation in (
    "algebra_orient", "algebra_inspect", "algebra_select", "algebra_transform",
    "algebra_validate", "algebra_verify", "algebra_summarize",
):
    registry.register(algebra_operation, "algebra_timeline_reasoning", lambda step: bool(step.events and step.visualization_state))
for grade8_template in (
    "expression_tiles", "signed_terms", "grouped_terms", "fraction_bar",
    "square_comparison", "like_term_sort", "unlike_term_sort", "receipt", "rectangle", "bracket_negation", "grouped_polynomials", "factor_array", "sign_grid", "area_product", "power_stack", "area_comparison",
    "distribute_strip", "signed_distribute", "trinomial_branches", "area_distribute", "compare_paths",
    "equal_share", "signed_quotient", "factor_cancel", "term_share", "three_term_share", "exponent_lanes", "context_packs", "error_division", "two_quotients", "square_grid", "signed_square", "cube_stack", "signed_cube", "sign_scope", "power_factor_stack", "root_pairs", "absolute_root", "cube_root", "fraction_cube", "error_root", "compare_powers", "compare_roots", "value_machine", "signed_slot", "exponent_scope", "compare_scope", "two_input", "bracket_input", "layered_order", "fraction_gate", "equivalent_value_paths", "error_substitution", "context_measure", "term_bins", "distribute_collect", "signed_distribution_collect", "quotient_collect", "dual_distribution_collect", "negative_bracket", "variable_quotient_collect", "power_bins", "distribution_error", "perimeter_mixed", "equivalent_mixed", "layered_mixed", "layered_quotient_mixed", "unit_receipt", "fixed_variable_receipt", "flow_rule", "input_table", "fare_table", "decrease_timeline", "packs_plus_loose", "context_perimeter", "plan_comparison", "fee_error", "equivalence_models", "general_table", "split_area_context", "parallel_flows", "fundraiser_audit", "diagnostic_term_sort", "diagnostic_signed_terms", "diagnostic_factor_array", "diagnostic_distribution_paths", "diagnostic_signed_distribution", "diagnostic_quotient_lanes", "diagnostic_exponent_scope", "diagnostic_root_pairs", "diagnostic_parallel_paths", "diagnostic_mixed_trace", "diagnostic_restricted_quotient", "diagnostic_context_receipt", "diagnostic_area_split", "diagnostic_parallel_flows", "diagnostic_integrated_trace", "function_flow", "function_table", "function_reverse", "function_context", "function_compare", "equivalence_translation", "equivalence_flow_table", "equivalence_counterexample", "equivalence_context", "equivalence_domain", "equivalence_algebra", "rule_difference", "rule_zero", "rule_signed", "rule_nonlinear", "rule_context", "rule_choice", "formula_rectangle", "relationship_match", "relationship_repair",
    "equality_balance", "additive_inverse", "multiplicative_inverse",
    "two_step_balance", "variables_both_sides", "context_to_equation",
    "distributive_equation", "inspection_fact_family", "inspection_number_line",
    "inspection_substitution_table", "inspection_context",
    "additive_balance", "additive_number_line", "additive_context",
    "equal_groups", "fraction_scale", "multiplicative_balance", "multiplicative_context",
    "two_step_balance_native", "operation_machine", "two_step_number_line",
    "two_step_fraction_scale", "two_step_context", "variables_both_sides_native", "expression_comparison",
    "identity_contradiction", "dual_rate_timeline", "equal_sides_triangle",
    "bracket_balance_native", "bracket_distribution_native", "bracket_paths_native", "bracket_area_native", "bracket_rectangle_native",
    "fraction_bar_balance_native", "fraction_equivalence_native", "fraction_lcd_native", "fraction_error_native", "fraction_context_native",
            "context_translation_strip_native", "number_relationship_native", "money_model_native", "perimeter_model_native", "sharing_bar_model_native", "age_timeline_native", "rate_table_native", "error_diagnosis_context_native",
            "diagnosis_first_error_replay_native", "diagnosis_balance_equation_native", "diagnosis_signed_balance_native", "diagnosis_bracket_distribution_native", "diagnosis_denominator_lcm_native", "diagnosis_error_diagnosis_context_native", "diagnosis_perimeter_model_native", "diagnosis_identity_contradiction_native", "diagnosis_rate_table_native", "diagnosis_mastery_map_native",
):
    registry.register(
        f"{grade8_template}_step",
        grade8_template,
        lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression),
    )
registry.register("pattern_step", "grade8_pattern_board", lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
registry.register("whole_number_step", "grade8_whole_number_board", lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
registry.register("grade9_set_step", "grade9_number_sets", lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
registry.register("grade9_factor_step", "grade9_prime_factors", lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
registry.register("grade9_3_step", "grade9_ratio_rate", lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
registry.register("grade9_4_step", "grade9_proportion", lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
registry.register("grade9_5_step", "grade9_transaction", lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
registry.register("grade9_6_step", "grade9_ledger", lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
registry.register("grade9_7_step", "grade9_interest", lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
registry.register("grade9_8_step", "grade9_decision", lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
for _grade9_integer_number in range(1,6):
    registry.register(f"grade9_integer_{_grade9_integer_number}_step", f"grade9_integer_{_grade9_integer_number}",
        lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
for _grade9_exponent_number in range(1,7):
    registry.register(f"grade9_exponent_{_grade9_exponent_number}_step", f"grade9_exponent_{_grade9_exponent_number}",
        lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
for _grade9_pattern_number in range(1,6):
    registry.register(f"grade9_pattern_{_grade9_pattern_number}_step", f"grade9_pattern_{_grade9_pattern_number}",
        lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
for _grade9_function_number in range(1,6):
    registry.register(f"grade9_function_{_grade9_function_number}_step", f"grade9_function_{_grade9_function_number}",
        lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
for _grade9_expression_number in range(1,10):
    registry.register(f"grade9_expression_{_grade9_expression_number}_step", f"grade9_expression_{_grade9_expression_number}",
        lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
for _grade10_algebra_number in range(1,7):
    registry.register(f'grade10_algebra_{_grade10_algebra_number}_step', f'grade10_algebra_{_grade10_algebra_number}',
        lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
for _grade10_eei_number in range(1,10):
    registry.register(f'grade10_eei_{_grade10_eei_number}_step', f'grade10_eei_{_grade10_eei_number}',
        lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
for _grade10_fn_number in range(1,8):
    registry.register(f'grade10_fn_{_grade10_fn_number}_step', f'grade10_fn_{_grade10_fn_number}',
        lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
for _grade10_stat_number in range(1,7):
    registry.register(f'grade10_stat_{_grade10_stat_number}_step', f'grade10_stat_{_grade10_stat_number}',
        lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
for _grade10_meas_number in range(1,7):
    registry.register(f'grade10_meas_{_grade10_meas_number}_step', f'grade10_meas_{_grade10_meas_number}',
        lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
for _grade11_es_number in range(1,7):
    registry.register(f'grade11_es_{_grade11_es_number}_step', f'grade11_es_{_grade11_es_number}',
        lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
for _grade11_ei_number in range(1,8):
    registry.register(f'grade11_ei_{_grade11_ei_number}_step', f'grade11_ei_{_grade11_ei_number}',
        lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
for _grade11_tr_number in range(1,8):
    registry.register(f'grade11_tr_{_grade11_tr_number}_step', f'grade11_tr_{_grade11_tr_number}',
        lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
for _grade10_fin_number in range(1,7):
    registry.register(f'grade10_fin_{_grade10_fin_number}_step', f'grade10_fin_{_grade10_fin_number}',
        lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
for _grade10_prob_number in range(1,6):
    registry.register(f'grade10_prob_{_grade10_prob_number}_step', f'grade10_prob_{_grade10_prob_number}',
        lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
for _grade10_ag_number in range(1,7):
    registry.register(f'grade10_ag_{_grade10_ag_number}_step', f'grade10_ag_{_grade10_ag_number}',
        lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
for _grade10_euc_number in range(1,7):
    registry.register(f'grade10_euc_{_grade10_euc_number}_step', f'grade10_euc_{_grade10_euc_number}',
        lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
for _grade10_trig_number in range(1,8):
    registry.register(f'grade10_trig_{_grade10_trig_number}_step', f'grade10_trig_{_grade10_trig_number}',
        lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
for _grade9_transform_number in range(1,8):
    registry.register(f'grade9_transform_{_grade9_transform_number}_step', f'grade9_transform_{_grade9_transform_number}',
        lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
for _grade9_surface_number in range(1,7):
    registry.register(f'grade9_surface_{_grade9_surface_number}_step', f'grade9_surface_{_grade9_surface_number}',
        lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
for _grade9_solid_number in range(1,5):
    registry.register(f'grade9_solid_{_grade9_solid_number}_step', f'grade9_solid_{_grade9_solid_number}',
        lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
for _grade9_probability_number in range(1,6):
    registry.register(f'grade9_probability_{_grade9_probability_number}_step', f'grade9_probability_{_grade9_probability_number}',
        lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
for _grade9_data_number in range(1,9):
    registry.register(f'grade9_data_{_grade9_data_number}_step', f'grade9_data_{_grade9_data_number}',
        lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
for _grade9_area_number in range(1,6):
    registry.register(f'grade9_area_{_grade9_area_number}_step', f'grade9_area_{_grade9_area_number}',
        lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
for _grade9_shapes_number in range(1,9):
    registry.register(f'grade9_shapes_{_grade9_shapes_number}_step', f'grade9_shapes_{_grade9_shapes_number}',
        lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
for _grade9_lines_number in range(1,6):
    registry.register(f'grade9_lines_{_grade9_lines_number}_step', f'grade9_lines_{_grade9_lines_number}',
        lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
for _grade9_graph_number in range(1,8):
    registry.register(f'grade9_graph_{_grade9_graph_number}_step', f'grade9_graph_{_grade9_graph_number}',
        lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
for _grade9_equation_number in range(1,7):
    registry.register(f"grade9_equation_{_grade9_equation_number}_step", f"grade9_equation_{_grade9_equation_number}",
        lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
registry.register("fraction_stage", "grade8_fraction_strips", lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
registry.register("fraction_operation_stage", "grade8_fraction_operations", lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
registry.register("fraction_model_stage", "grade8_fraction_powers_context", lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
registry.register("integer_reasoning_stage", "grade8_integer_reasoning", lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
registry.register("integer_operation_stage", "grade8_integer_operations", lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
registry.register("integer_step", "grade8_integer_board", lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
registry.register("global_graph_step", "grade8_global_story",
                  lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
registry.register("coordinate_plot_step", "grade8_coordinate_plane",
                  lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
registry.register("select_method", "method_selection", lambda step: bool(step.after_expression))
registry.register("show_working", "progressive_working", lambda step: "∴" in step.after_expression)
registry.register("verify_result", "result_verification", lambda step: "✓" in step.after_expression)
registry.register("draw_secant", "secant_line", lambda step: step.before_expression == step.after_expression)
registry.register("calculate_secant_gradient", "secant_gradient", lambda step: "h≠0" in step.after_expression)
registry.register("approach_limit", "secant_approaches_tangent", lambda step: "→" in step.after_expression)
registry.register("draw_tangent", "tangent_at_point", lambda step: "f′" in step.after_expression)

registry.register("percentage_stage", "grade8_percentage_grid", lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))

registry.register("decimal_column_stage", "grade8_decimal_columns", lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
registry.register("decimal_round_stage", "grade8_decimal_rounding", lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))

registry.register("decimal_product_stage", "grade8_decimal_product", lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
registry.register("decimal_quotient_stage", "grade8_decimal_quotient", lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
registry.register("decimal_power_stage", "grade8_decimal_power", lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
registry.register("decimal_root_stage", "grade8_decimal_root", lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
registry.register("exponent_representation_stage", "grade8_exponent_representation", lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
registry.register("exponent_laws_stage", "grade8_exponent_laws", lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
registry.register("exponent_roots_stage", "grade8_exponent_roots", lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
registry.register("exponent_applications_stage", "grade8_exponent_applications", lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
registry.register("exponent_error_stage", "grade8_exponent_error_trace", lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
registry.register("exponent_integrated_stage", "grade8_exponent_integrated", lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
registry.register("grade8_angle_stage", "grade8_intersecting_angles", lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
registry.register("grade8_parallel_angle_stage", "grade8_parallel_angles", lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
for _number,_template in (("chain","grade8_angle_chain"),("equation","grade8_angle_equation"),("error","grade8_angle_error")):
    registry.register(f"grade8_angle_{_number}_stage",_template,lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
for _shape_template in ("triangle_sides","triangle_sum","equal_triangle","quad_classify","quad_angle"):
    registry.register(f"grade8_{_shape_template}_stage", f"grade8_{_shape_template}", lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))

for _pyth_family in ("square_areas","hypotenuse","missing_leg","converse","application"):
    registry.register(f"grade8_{_pyth_family}_stage", f"grade8_pythagoras_{_pyth_family}", lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))

for _grade11_euc_number in range(1,9):
    registry.register(f"grade11_euc_{_grade11_euc_number}_step", f"grade11_euc_{_grade11_euc_number}",
        lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))

for _grade11_ag_number in range(1,7):
    registry.register(f"grade11_ag_{_grade11_ag_number}_step", f"grade11_ag_{_grade11_ag_number}",
        lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))

for _grade11_rules_number in range(1,6):
    registry.register(f"grade11_rules_{_grade11_rules_number}_step", f"grade11_rules_{_grade11_rules_number}",
        lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))

for _grade11_fn_number in range(1,9):
    registry.register(f"grade11_fn_{_grade11_fn_number}_step", f"grade11_fn_{_grade11_fn_number}",
        lambda step: bool(step.events and step.visualization_state and step.before_expression != step.after_expression))
