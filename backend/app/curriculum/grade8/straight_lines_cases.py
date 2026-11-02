"""Original Grade 8 straight-line geometry cases for teacher review.

Every case describes the diagram, the theorem, the mathematical steps and a
check against the complete given.  These data are deliberately kept separate
from the current lesson catalogue until a native diagram renderer is ready.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class AngleCase:
    id: str
    diagram: str
    relationship: str
    given: tuple[int, ...]
    answer: int
    problem: str
    working: tuple[str, ...]
    check: str
    misconception: str


def _single(number: int, diagram: str, relationship: str, given: int) -> AngleCase:
    total = 180 if relationship in {"linear_pair", "cointerior"} else 90 if relationship == "right_angle" else 360 if relationship == "around_point" else None
    answer = given if total is None else total - given
    phrase = {"linear_pair": "adjacent angles on a straight line", "right_angle": "two parts of a right angle", "vertical": "vertically opposite angles", "around_point": "angles around one point", "corresponding": "corresponding angles on parallel lines", "alternate": "alternate interior angles on parallel lines", "cointerior": "co-interior angles on parallel lines"}[relationship]
    prompt = f"In the labelled diagram, {phrase} include a {given}° angle. Find the marked angle x. Give a reason."
    equation = f"x + {given}° = {total}°" if total is not None else f"x = {given}°"
    calculation = f"x = {total}° − {given}° = {answer}°" if total is not None else f"x = {answer}°"
    check = f"{answer}° + {given}° = {total}°" if total is not None else f"Both marked angles measure {answer}°."
    return AngleCase(f"g8-lines-{'02' if diagram == 'transversal' else '01'}-w{number:02}", diagram, relationship, (given,), answer, prompt,
                     (f"Locate the given {given}° angle and the separate marked angle x.", f"Identify the {phrase} relationship.", equation, calculation), check,
                     "Do not assume two angles are equal merely because they look alike; name the line or parallel-line relationship.")


def _expression(number: int, diagram: str, relationship: str, a: int, b: int, c: int, d: int) -> AngleCase:
    """For x-angle ax+b and given angle cx+d; choose integral x cases."""
    def term(coefficient: int, constant: int) -> str:
        if not coefficient:
            return str(constant)
        variable = "x" if coefficient == 1 else f"{coefficient}x"
        return variable if not constant else f"{variable} {'+' if constant > 0 else '−'} {abs(constant)}"
    total = 180 if relationship in {"linear_pair", "cointerior"} else 360 if relationship == "around_point" else None
    numerator = (total - b - d) if total is not None else d - b
    denominator = (a + c) if total is not None else a - c
    if denominator == 0 or numerator % denominator:
        raise ValueError(f"Case {number}: non-integral or undefined x")
    x = numerator // denominator
    left, right = a*x+b, c*x+d
    if x <= 0 or not 0 < left < 180 or not 0 < right < 180:
        raise ValueError(f"Case {number}: angle outside geometric range")
    if total == 360 and left+right != 360:
        raise ValueError(f"Case {number}: invalid around-point diagram")
    if total == 360:
        raise ValueError("A two-angle 360° case requires a reflex angle; use a separate diagram contract")
    phrase = {"linear_pair": "form a straight line", "vertical": "are vertically opposite", "corresponding": "are corresponding on parallel lines", "alternate": "are alternate interior on parallel lines", "cointerior": "are co-interior on parallel lines"}[relationship]
    operation = "+" if total is not None else "="
    equation = f"({term(a,b)}) {operation} ({term(c,d)})" + (f" = {total}" if total is not None else "")
    simplified = f"({a+c})x + ({b+d}) = {total}" if total is not None else f"({a-c})x = {d-b}"
    check = f"{left}° + {right}° = {total}°" if total is not None else f"Both expressions give {left}°."
    prompt = f"In the diagram, angles ({term(a,b)})° and ({term(c,d)})° {phrase}. Find x."
    return AngleCase(f"g8-lines-{'02' if diagram == 'transversal' else '01'}-w{number:02}", diagram, relationship,
                     (a,b,c,d), x, prompt, ("Mark the two distinct angle regions before writing an equation.", f"Use the fact that these angles {phrase}.", equation, simplified, f"Solve to obtain x = {x}.", f"Substitute: {term(a,b)} at x = {x} gives {left}°."), check,
                     "The unknown is x, not the angle size; substitute the solved x into the labelled expression.")


LESSON_1 = (
    _single(1,"perpendicular","right_angle",34),
    _single(2,"intersection","linear_pair",68),
    _single(3,"intersection","vertical",47),
    _single(4,"intersection","linear_pair",123),
    _single(5,"perpendicular","right_angle",57),
    _expression(6,"intersection","linear_pair",2,18,0,20),
    _expression(7,"intersection","vertical",3,12,2,47),
    _single(8,"intersection","vertical",116),
    _expression(9,"intersection","linear_pair",3,24,0,30),
    _single(10,"perpendicular","right_angle",19),
    _expression(11,"intersection","vertical",4,-14,2,50),
    _expression(12,"intersection","linear_pair",4,20,1,10),
    _single(13,"intersection","linear_pair",147),
    _expression(14,"intersection","vertical",5,9,3,75),
    _expression(15,"intersection","linear_pair",5,-30,1,0),
)

LESSON_2 = (
    _single(1,"transversal","corresponding",48),
    _single(2,"transversal","alternate",67),
    _single(3,"transversal","cointerior",112),
    _single(4,"transversal","cointerior",73),
    _expression(5,"transversal","corresponding",1,14,0,72),
    _expression(6,"transversal","alternate",2,9,0,83),
    _expression(7,"transversal","cointerior",3,24,2,11),
    _single(8,"transversal","corresponding",126),
    _single(9,"transversal","alternate",119),
    _single(10,"transversal","cointerior",98),
    _expression(11,"transversal","cointerior",4,-6,1,36),
    _expression(12,"transversal","corresponding",3,-20,0,100),
    _expression(13,"transversal","alternate",5,15,0,140),
    _expression(14,"transversal","cointerior",2,45,3,-20),
    _expression(15,"transversal","alternate",2,20,5,-40),
)

def validate_all():
    cases = LESSON_1 + LESSON_2
    assert len(cases) == 30 and len({case.id for case in cases}) == 30
    for case in cases:
        assert case.check and len(case.working) >= 4
        if len(case.given) == 1:
            other = case.given[0]
            if case.relationship in {"linear_pair", "cointerior"}: assert case.answer + other == 180
            elif case.relationship == "right_angle": assert case.answer + other == 90
            else: assert case.answer == other
        else:
            a,b,c,d = case.given
            left,right = a*case.answer+b,c*case.answer+d
            if case.relationship in {"linear_pair", "cointerior"}: assert left+right == 180
            else: assert left == right
    return True


def parallel_variant(case: AngleCase, shift: int) -> AngleCase:
    """Create an unseen parallel item with changed geometry values, not a copied memo."""
    if not 1 <= shift <= 6:
        raise ValueError('Shift must be a small positive integer')
    if len(case.given) == 1:
        original = case.given[0]
        cap = 90 if case.relationship == 'right_angle' else 180
        changed = original + 4*shift
        if changed >= cap: changed = original - 4*shift
        if not 0 < changed < cap: raise ValueError('Variant angle out of range')
        result = _single(int(case.id[-2:]),case.diagram,case.relationship,changed)
    else:
        a,b,c,d = case.given
        for candidate_x in (case.answer+shift,case.answer-shift):
            candidate_d = (180-(a+c)*candidate_x-b if case.relationship in {'linear_pair','cointerior'}
                           else (a-c)*candidate_x+b)
            try:
                result = _expression(int(case.id[-2:]),case.diagram,case.relationship,a,b,c,candidate_d)
                break
            except ValueError:
                continue
        else: raise ValueError('No legal parallel variant')
    if result.problem == case.problem:
        raise ValueError('Parallel problem must differ from worked example')
    return result

validate_all()
