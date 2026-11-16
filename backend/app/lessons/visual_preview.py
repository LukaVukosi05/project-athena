"""Public visual givens for Grades 9–11, excluding authored solution values.

Register family and hidden keys once; keep mode-specific exceptions explicit.
Unknown families intentionally expose only the existing generic givens marker.
"""

# (lesson prefix, public renderer family, private value keys)
VISUAL_PREVIEW_RULES = (
    ("g9-shapes-", "shapes", ("target", "each")),
    (
        "g10-algebra-",
        "grade10_expressions",
        (
            "answer",
            "coefficients",
            "decimal",
            "excluded",
            "lower",
            "upper",
            "first",
            "second",
            "a",
            "b",
            "c",
            "d",
            "t",
            "middle",
        ),
    ),
    ("g11-es-", "grade11_exponents_surds", ("root", "outside", "valid", "rejected")),
    ("g11-ei-", "grade11_equations", ("r", "s")),
    ("g11-meas-", "grade11_measurement", ()),
    ("g11-pat-", "grade11_patterns", ("target",)),
    ("g11-fin-", "grade11_finance", ()),
    ("g11-prob-", "grade11_probability", ()),
    (
        "g11-stat-",
        "grade11_statistics",
        (
            "mean",
            "sum",
            "weighted",
            "five",
            "iqr",
            "peak",
            "cumulative",
            "total",
            "median_class",
            "squares",
            "variance",
            "sd",
            "upper_fence",
            "model",
            "first_differences",
            "second_differences",
        ),
    ),
    ("g11-rules-", "grade11_triangle_rules", ("B1", "B2", "area")),
    (
        "g11-fn-",
        "grade11_functions",
        (
            "vertex",
            "vertical",
            "horizontal",
            "target_y",
            "y0",
            "y1",
            "slope",
            "result",
            "period",
            "shift",
        ),
    ),
    (
        "g11-ag-",
        "grade11_analytical",
        ("length", "m", "c", "target_m", "base_m", "theta", "dx", "dy"),
    ),
    ("g11-euc-", "grade11_euclidean", ("half", "tangent")),
    ("g11-tr-", "grade11_trigonometry", ("excluded",)),
    (
        "g10-eei-",
        "grade10_equations",
        (
            "result",
            "base",
            "target",
            "rhs",
            "r",
            "t",
            "coefficient",
            "constant",
            "x",
            "y",
            "u",
            "v",
            "total",
            "perimeter",
            "width",
            "bound",
            "closed",
            "direction",
        ),
    ),
    (
        "g10-meas-",
        "grade10_measurement",
        (
            "answer",
            "volume",
            "surface",
            "scaled_a",
            "scaled_b",
            "scaled_h",
            "slant",
            "cylinder_volume",
            "hemisphere_volume",
        ),
    ),
    (
        "g10-fin-",
        "grade10_finance",
        (
            "answer",
            "amount",
            "interest",
            "simple",
            "deposit",
            "balance",
            "instalment",
            "old_amount",
            "difference",
        ),
    ),
    ("g10-prob-", "grade10_probability", ("answer",)),
    (
        "g10-stat-",
        "grade10_statistics",
        (
            "answer",
            "summary",
            "other_summary",
            "q1",
            "q3",
            "median",
            "minimum",
            "maximum",
        ),
    ),
    ("g10-fn-", "grade10_functions", ("answer",)),
    ("g10-ag-", "grade10_analytical", ("answer", "solution_point")),
    (
        "g10-euc-",
        "grade10_euclidean",
        (
            "answer",
            "result",
            "a",
            "b",
            "c",
            "radicand",
            "solution_bc",
            "solution_de",
            "scale",
        ),
    ),
    (
        "g10-trig-",
        "grade10_trigonometry",
        (
            "answer",
            "hypotenuse",
            "numerator",
            "denominator",
            "reference",
            "quadrant",
            "angle",
            "radius",
            "sin",
            "cos",
            "tan",
            "ratio",
        ),
    ),
    ("g9-tg-", "transformation", ("image", "original_area", "rule")),
    (
        "g9-sv-",
        "surface_volume",
        (
            "surface_area",
            "volume",
            "volume_pi",
            "surface_area_pi",
            "triangle_area",
            "capacity_num",
            "capacity_den",
            "original",
            "new_volume",
            "factor",
            "litres_num",
            "litres_den",
            "correct_value",
        ),
    ),
    (
        "g9-solid-",
        "solids",
        ("target", "parts", "missing", "faces", "edges", "vertices"),
    ),
    (
        "g9-prob-",
        "probability",
        (
            "favourable",
            "row_total",
            "column_total",
            "grand_total",
            "first_red_num",
            "first_red_den",
            "second_red_num",
            "second_red_den",
            "prob_num",
            "prob_den",
            "predicted_heads",
            "multiples_of_three",
            "favourable_pairs",
            "total_pairs",
        ),
    ),
    (
        "g9-data-",
        "data",
        (
            "young_pick",
            "old_pick",
            "total",
            "mode",
            "median",
            "mean_rounded",
            "range",
            "outlier",
            "gain_a",
            "gain_b",
            "modal_interval",
            "walk_angle_num",
            "walk_angle_den",
            "prediction",
            "difference",
            "percent",
        ),
    ),
    (
        "g9-area-",
        "area",
        (
            "area",
            "perimeter",
            "diameter",
            "circumference_coefficient",
            "area_coefficient",
            "old_perimeter",
            "old_area",
            "new_perimeter",
            "new_area",
            "scaled_length",
            "scaled_width",
            "outer_length",
            "outer_width",
            "path_area",
            "fence",
        ),
    ),
)


def public_visual(lesson_id: str, visual: dict) -> dict:
    for prefix, family, hidden in VISUAL_PREVIEW_RULES:
        if lesson_id.startswith(prefix):
            givens = dict(visual["values"])
            for key in hidden:
                givens.pop(key, None)
            _apply_mode_exceptions(lesson_id, givens)
            return {"family": family, "values": givens}
    return {"family": "givens"}


def _apply_mode_exceptions(lesson_id: str, givens: dict) -> None:
    if lesson_id.startswith("g11-rules-"):
        if givens.get("mode") == "sine_side":
            givens.pop("b", None)
        if givens.get("mode") == "cosine_side":
            givens.pop("a", None)
        if givens.get("mode") == "cosine_angle":
            givens.pop("A", None)
    elif lesson_id.startswith("g11-ag-"):
        if givens.get("mode") == "midpoint":
            givens.pop("b" if givens.get("missing") else "mid", None)
    elif lesson_id.startswith("g11-tr-"):
        if givens.get("mode") in {"general", "interval"}:
            givens.pop("reference", None)
    elif lesson_id.startswith("g10-eei-"):
        if givens.get("form") == "purchase":
            givens.pop("a", None)
    elif lesson_id.startswith("g10-prob-"):
        if lesson_id.startswith(("g10-prob-02", "g10-prob-05")):
            for hidden in ("a_only", "b_only", "neither", "union"):
                givens.pop(hidden, None)
    elif lesson_id.startswith("g10-fn-"):
        if lesson_id.startswith("g10-fn-01"):
            givens["given"] = givens.get("given", [])[:2]
        if lesson_id.startswith("g10-fn-06"):
            givens.pop("a", None)
            givens.pop("q", None)
        if lesson_id.startswith("g10-fn-07"):
            givens.pop("mode", None)
    elif lesson_id.startswith("g10-ag-"):
        if givens.get("model") in {"two_segments", "quadrilateral"}:
            givens.pop("mode", None)
    elif lesson_id.startswith("g10-euc-"):
        if givens.get("mode") == "diagnosis":
            givens.pop("de", None)
    elif lesson_id.startswith("g10-trig-"):
        if givens.get("model") == "solve":
            givens.pop("degree", None)
