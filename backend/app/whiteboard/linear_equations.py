"""Deterministic validation for the initial linear-equation operation set."""

import re
from fractions import Fraction

from app.curriculum.schemas import TeachingStep

LINEAR_SIDE = re.compile(r"^([+-]?\d*)x([+-]\d+(?:/\d+)?)?$")


def parse_side(value: str) -> tuple[Fraction, Fraction] | None:
    compact = value.replace(" ", "")
    if "x" not in compact:
        try:
            return Fraction(0), Fraction(compact)
        except (ValueError, ZeroDivisionError):
            return None
    match = LINEAR_SIDE.fullmatch(compact)
    if not match:
        return None
    coefficient_text, constant_text = match.groups()
    coefficient = Fraction(-1 if coefficient_text == "-" else coefficient_text or 1)
    return coefficient, Fraction((constant_text or "0").replace("+", ""))


def parse_equation(value: str) -> tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]] | None:
    if value.count("=") != 1:
        return None
    left, right = value.split("=")
    parsed_left, parsed_right = parse_side(left), parse_side(right)
    return (parsed_left, parsed_right) if parsed_left and parsed_right else None


def verify_linear_transition(step: TeachingStep) -> bool:
    before, after = parse_equation(step.before_expression), parse_equation(step.after_expression)
    if before is None or after is None:
        return False
    (left_a, left_b), (right_a, right_b) = before
    (after_left_a, after_left_b), (after_right_a, after_right_b) = after
    value = Fraction(str(step.operation.value))
    if step.operation.type == "subtract_both_sides":
        expected = ((left_a, left_b - value), (right_a, right_b - value))
    elif step.operation.type == "divide_both_sides" and value:
        expected = ((left_a / value, left_b / value), (right_a / value, right_b / value))
    else:
        return False
    return expected == after
