"""Deterministic validation for the initial linear-equation operation set."""

import ast
import re
from fractions import Fraction

from app.curriculum.schemas import TeachingStep

LINEAR_SIDE = re.compile(r"^([+-]?\d*)x([+-]\d+(?:/\d+)?)?$")


def _linear_expression(value: str) -> tuple[Fraction, Fraction]:
    """Parse the small, safe linear-expression grammar used by curriculum."""
    source = re.sub(r"(?<=\d)x", "*x", value.replace(" ", ""))
    source = re.sub(r"(?<=\d)\(", "*(", source)

    def visit(node: ast.AST) -> tuple[Fraction, Fraction]:
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if isinstance(node, ast.Name) and node.id == "x":
            return Fraction(1), Fraction(0)
        if isinstance(node, ast.Constant) and isinstance(node.value, int):
            return Fraction(0), Fraction(node.value)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
            a, b = visit(node.operand)
            return (-a, -b) if isinstance(node.op, ast.USub) else (a, b)
        if isinstance(node, ast.BinOp):
            left, right = visit(node.left), visit(node.right)
            if isinstance(node.op, ast.Add):
                return left[0] + right[0], left[1] + right[1]
            if isinstance(node.op, ast.Sub):
                return left[0] - right[0], left[1] - right[1]
            if isinstance(node.op, ast.Mult):
                if left[0] and right[0]:
                    raise ValueError("Non-linear expression")
                return left[0] * right[1] + right[0] * left[1], left[1] * right[1]
            if isinstance(node.op, ast.Div) and right[0] == 0 and right[1] != 0:
                return left[0] / right[1], left[1] / right[1]
        raise ValueError("Unsupported expression")

    return visit(ast.parse(source, mode="eval"))


def solve_linear_equation(value: str) -> Fraction | None:
    """Return a unique solution without evaluating arbitrary source text."""
    if value.count("=") != 1:
        return None
    try:
        left, right = (_linear_expression(side) for side in value.split("="))
        coefficient = left[0] - right[0]
        return (right[1] - left[1]) / coefficient if coefficient else None
    except (SyntaxError, ValueError, ZeroDivisionError):
        return None


def verify_equivalent_transition(step: TeachingStep) -> bool:
    before = solve_linear_equation(step.before_expression)
    return before is not None and before == solve_linear_equation(step.after_expression)


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
