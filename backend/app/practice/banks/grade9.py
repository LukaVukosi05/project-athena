"""Grade 9 lesson banks: practice, mastery, reassessment, repairs and rules."""

from app.curriculum.grade9 import assessment_whole_numbers as grade9_whole

LESSON_BANKS = {
    "g9-whole-numbers-01": (
        grade9_whole.PRACTICE_1,
        grade9_whole.MASTERY_1,
        grade9_whole.REASSESSMENT_1,
        grade9_whole.REPAIRS_1,
        grade9_whole.RULES_1,
    ),
    "g9-whole-numbers-02": (
        grade9_whole.PRACTICE_2,
        grade9_whole.MASTERY_2,
        grade9_whole.REASSESSMENT_2,
        grade9_whole.REPAIRS_2,
        grade9_whole.RULES_2,
    ),
    **{
        f"g9-whole-numbers-{number:02}": grade9_whole.EXTENDED_BANKS[number]
        for number in range(3, 9)
    },
    **{
        f"g9-integers-{number:02}": grade9_whole.INTEGER_BANKS[number]
        for number in range(1, 6)
    },
    **{
        f"g9-exponents-{number:02}": grade9_whole.EXPONENT_BANKS[number]
        for number in range(1, 7)
    },
    **{
        f"g9-patterns-{number:02}": grade9_whole.PATTERN_BANKS[number]
        for number in range(1, 6)
    },
    **{
        f"g9-functions-{number:02}": grade9_whole.FUNCTION_BANKS[number]
        for number in range(1, 6)
    },
    **{
        f"g9-expressions-{number:02}": grade9_whole.EXPRESSION_BANKS[number]
        for number in range(1, 10)
    },
    **{
        f"g9-equations-{number:02}": grade9_whole.EQUATION_BANKS[number]
        for number in range(1, 7)
    },
    **{
        f"g9-graphs-{number:02}": grade9_whole.GRAPH_BANKS[number]
        for number in range(1, 8)
    },
    **{
        f"g9-straight-lines-{number:02}": grade9_whole.LINE_BANKS[number]
        for number in range(1, 6)
    },
    **{
        f"g9-shapes-{number:02}": grade9_whole.SHAPE_BANKS[number]
        for number in range(1, 9)
    },
    **{
        f"g9-area-{number:02}": grade9_whole.AREA_BANKS[number]
        for number in range(1, 6)
    },
    **{
        f"g9-data-{number:02}": grade9_whole.DATA_BANKS[number]
        for number in range(1, 9)
    },
    **{
        f"g9-prob-{number:02}": grade9_whole.PROB_BANKS[number]
        for number in range(1, 6)
    },
    **{
        f"g9-solid-{number:02}": grade9_whole.SOLID_BANKS[number]
        for number in range(1, 5)
    },
    **{
        f"g9-tg-{number:02}": grade9_whole.TRANSFORM_BANKS[number]
        for number in range(1, 8)
    },
    **{
        f"g9-sv-{number:02}": grade9_whole.SURFACE_BANKS[number]
        for number in range(1, 7)
    },
}
