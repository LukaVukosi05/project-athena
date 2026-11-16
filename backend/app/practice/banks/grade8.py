"""Grade 8 lesson banks: practice, mastery, reassessment, repairs and rules."""

from app.curriculum.grade8 import (
    assessment_lesson2,
    assessment_lesson3,
    assessment_lesson4,
    assessment_lesson5,
    assessment_lesson6,
    assessment_lesson7,
    assessment_lesson8,
    assessment_lesson9,
    assessment_lesson10,
)
from app.curriculum.grade8 import (
    assessment_functions_lesson1,
    assessment_functions_lesson2,
    assessment_functions_lesson3,
)
from app.curriculum.grade8 import (
    assessment_functions_lesson4,
    assessment_functions_lesson5,
    assessment_functions_lesson6,
)
from app.curriculum.grade8 import (
    assessment_patterns,
    assessment_patterns_34,
    assessment_patterns_56,
    assessment_whole_numbers,
    assessment_integers,
    assessment_integers_advanced,
    assessment_integers_reasoning,
    assessment_fractions,
    assessment_fractions_operations,
    assessment_fractions_56,
    assessment_fractions_78,
    assessment_decimals,
    assessment_decimals_operations,
    assessment_decimals_powers,
    assessment_exponents,
)
from app.curriculum.grade8 import (
    assessment_straight_lines,
    assessment_shapes,
    assessment_pythagoras,
)
from app.curriculum.grade8 import assessment_straight_lines_chain
from app.curriculum.grade8 import (
    assessment_graphs_lesson1,
    assessment_graphs_lesson2,
    assessment_graphs_lesson3,
    assessment_graphs_lesson4,
    assessment_graphs_lesson5,
    assessment_graphs_lesson6,
)
from app.curriculum.grade8 import (
    assessment_expressions,
    assessment_expressions_lesson2,
    assessment_expressions_lesson3,
    assessment_expressions_lesson4,
    assessment_expressions_lesson5,
    assessment_expressions_lesson6,
    assessment_expressions_lesson7,
    assessment_expressions_lesson8,
    assessment_expressions_lesson9,
    assessment_expressions_lesson10,
)
from app.curriculum.grade8 import assessment as assessment_equations1
from app.practice.banks.common import module_bank

LESSON_BANKS = {
    **{f"g8-pythagoras-{n:02}": assessment_pythagoras.banks(n) for n in range(1, 6)},
    **{f"g8-shapes-{n:02}": assessment_shapes.banks(n) for n in range(1, 6)},
    **{f"g8-straight-lines-{n:02}": assessment_straight_lines.banks(n) for n in (1, 2)},
    **{
        f"g8-straight-lines-{n:02}": assessment_straight_lines_chain.banks(n)
        for n in (3, 4, 5)
    },
    **{f"g8-patterns-{n:02}": assessment_patterns_34.banks(n) for n in (3, 4)},
    **{f"g8-patterns-{n:02}": assessment_patterns_56.banks(n) for n in (5, 6)},
    **{f"g8-whole-numbers-{n:02}": assessment_whole_numbers.banks(n) for n in (1, 2)},
    **{f"g8-integers-{n:02}": assessment_integers.banks(n) for n in (1, 2)},
    **{f"g8-integers-{n:02}": assessment_integers_advanced.banks(n) for n in (3, 4)},
    **{f"g8-integers-{n:02}": assessment_integers_reasoning.banks(n) for n in (5, 6)},
    **{f"g8-common-fractions-{n:02}": assessment_fractions.banks(n) for n in (1, 2)},
    **{
        f"g8-common-fractions-{n:02}": assessment_fractions_operations.banks(n)
        for n in (3, 4)
    },
    **{f"g8-common-fractions-{n:02}": assessment_fractions_56.banks(n) for n in (5, 6)},
    **{f"g8-common-fractions-{n:02}": assessment_fractions_78.banks(n) for n in (7, 8)},
    **{f"g8-decimal-fractions-{n:02}": assessment_decimals.banks(n) for n in (1, 2)},
    **{
        f"g8-decimal-fractions-{n:02}": assessment_decimals_operations.banks(n)
        for n in (3, 4)
    },
    **{
        f"g8-decimal-fractions-{n:02}": assessment_decimals_powers.banks(n)
        for n in (5, 6)
    },
    **{
        f"g8-exponents-{n:02}": assessment_exponents.banks(n)
        for n in (1, 2, 3, 4, 5, 6)
    },
    **{
        f"g8-patterns-{n:02}": (
            bank[0],
            bank[1],
            bank[2],
            bank[3],
            {
                "pattern-rule-from-too-few-terms": "Retry a new pattern with changed starting values."
            },
        )
        for n, bank in (
            (1, assessment_patterns.banks(1)),
            (2, assessment_patterns.banks(2)),
        )
    },
    **{
        f"g8-graphs-{n:02}": module_bank(bank)
        for n, bank in (
            (3, assessment_graphs_lesson3),
            (4, assessment_graphs_lesson4),
            (5, assessment_graphs_lesson5),
            (6, assessment_graphs_lesson6),
        )
    },
    **{
        f"g8-functions-relationships-{n:02}": module_bank(bank)
        for n, bank in (
            (5, assessment_functions_lesson5),
            (6, assessment_functions_lesson6),
        )
    },
    "g8-functions-relationships-04": module_bank(assessment_functions_lesson4),
    "g8-graphs-01": module_bank(assessment_graphs_lesson1),
    "g8-graphs-02": module_bank(assessment_graphs_lesson2),
    "g8-algebraic-expressions-01": module_bank(assessment_expressions),
    "g8-algebraic-expressions-02": module_bank(assessment_expressions_lesson2),
    "g8-algebraic-expressions-03": module_bank(assessment_expressions_lesson3),
    "g8-algebraic-expressions-04": module_bank(assessment_expressions_lesson4),
    "g8-algebraic-expressions-05": module_bank(assessment_expressions_lesson5),
    "g8-algebraic-expressions-06": module_bank(assessment_expressions_lesson6),
    "g8-algebraic-expressions-07": module_bank(assessment_expressions_lesson7),
    "g8-algebraic-expressions-08": module_bank(assessment_expressions_lesson8),
    "g8-algebraic-expressions-09": module_bank(assessment_expressions_lesson9),
    "g8-algebraic-expressions-10": module_bank(assessment_expressions_lesson10),
    "g8-functions-relationships-01": module_bank(assessment_functions_lesson1),
    "g8-functions-relationships-02": module_bank(assessment_functions_lesson2),
    "g8-functions-relationships-03": module_bank(assessment_functions_lesson3),
    "g8-algebraic-equations-01": module_bank(assessment_equations1),
    "g8-algebraic-equations-02": module_bank(assessment_lesson2),
    "g8-algebraic-equations-03": module_bank(assessment_lesson3),
    "g8-algebraic-equations-04": module_bank(assessment_lesson4),
    "g8-algebraic-equations-05": module_bank(assessment_lesson5),
    "g8-algebraic-equations-06": module_bank(assessment_lesson6),
    "g8-algebraic-equations-07": module_bank(assessment_lesson7),
    "g8-algebraic-equations-08": module_bank(assessment_lesson8),
    "g8-algebraic-equations-09": module_bank(assessment_lesson9),
    "g8-algebraic-equations-10": module_bank(assessment_lesson10),
}
