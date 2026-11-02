"""Bounded exact arithmetic for Grade 8 roots and exponent applications."""
from math import isqrt


def superscript(n):
    return str(n).translate(str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹'))


def solve(kind, values):
    """Return answer, individually teachable rows, problem and independent check."""
    if not isinstance(values, list) or not all(type(v) is str and v.isdigit() and 1 <= len(v) <= 4 for v in values):
        raise ValueError('Roots require bounded whole-number inputs')
    v = list(map(int, values))
    if kind == 'square_root' and len(v) == 1:
        n, = v
        if not 4 <= n <= 400 or isqrt(n) ** 2 != n:
            raise ValueError('Use a bounded perfect square')
        root = isqrt(n)
        problem = f'Find √{n}. Show why your answer is the principal square root.'
        rows = [f'Read √{n} as the nonnegative number whose square is {n}.',
                f'Build a square with {n} equal unit tiles.',
                f'Arrange the tiles into {root} rows of {root} tiles.',
                f'The side count is {root}; {root} × {root} = {n}.',
                f'Therefore √{n} = {root}; the √ sign asks for the nonnegative root.']
        check = f'{root}² = {n}; this reconstructs the original number.'
        return str(root), rows, problem, check
    if kind == 'cube_root' and len(v) == 1:
        n, = v
        root = next((k for k in range(2, 11) if k ** 3 == n), None)
        if root is None:
            raise ValueError('Use a bounded perfect cube')
        problem = f'Find ∛{n}. Show the three equal dimensions.'
        rows = [f'Read ∛{n} as the number that gives {n} when cubed.',
                f'Build a cube from {n} equal unit cubes.',
                f'Count {root} unit cubes along each of the three edges.',
                f'Check {root} × {root} × {root} = {n}.',
                f'Therefore ∛{n} = {root}.']
        check = f'{root}³ = {n}; this restores the original cube.'
        return str(root), rows, problem, check
    if kind == 'root_pair' and len(v) == 2:
        a, b = v
        s = isqrt(a)
        c = next((k for k in range(2, 11) if k**3 == b), None)
        if not 4 <= a <= 400 or s*s != a or c is None:
            raise ValueError('Both radicands must be exact')
        problem = f'Evaluate √{a} + ∛{b}. Show the two roots separately.'
        rows = [f'Keep √{a} and ∛{b} separate: their indices describe different shapes.',
                f'Arrange {a} tiles into a {s} by {s} square, so √{a} = {s}.',
                f'Arrange {b} cubes into a {c} by {c} by {c} cube, so ∛{b} = {c}.',
                f'Substitute the two root values: {s} + {c}.',
                f'Add to obtain {s+c}.']
        check = f'{s}² = {a} and {c}³ = {b}; {s} + {c} = {s+c}.'
        return str(s+c), rows, problem, check
    if kind == 'square_area' and len(v) == 1:
        area, = v
        side = isqrt(area)
        if not 16 <= area <= 400 or side*side != area:
            raise ValueError('Area must be a perfect square')
        problem = f'A square has area {area} cm². Find its side length and perimeter.'
        rows = [f'Label the equal sides s. Area = s × s = {area} cm².',
                f'Take the nonnegative square root: s = √{area}.',
                f'Arrange {area} square centimetres in a {side} by {side} square.',
                f'So the side length is {side} cm.',
                f'The perimeter is four sides: 4 × {side} = {4*side} cm.']
        check = f'{side} × {side} = {area} cm², and four sides total {4*side} cm.'
        return f'{side} cm; {4*side} cm', rows, problem, check
    if kind == 'cube_volume' and len(v) == 1:
        volume, = v
        side = next((k for k in range(2, 11) if k**3 == volume), None)
        if side is None:
            raise ValueError('Volume must be a perfect cube')
        problem = f'A cube has volume {volume} cm³. Find one edge length.'
        rows = [f'Label all three equal edges s; volume = s × s × s.',
                f'Therefore s³ = {volume} cm³.',
                f'Take the cube root: s = ∛{volume}.',
                f'Build {side} equal layers, each {side} by {side} unit cubes.',
                f'The edge is {side} cm.']
        check = f'{side} × {side} × {side} = {volume} cm³; the volume is restored.'
        return f'{side} cm', rows, problem, check
    if kind == 'mixed' and len(v) == 4:
        base, exponent, square, cube = v
        sr = isqrt(square)
        cr = next((k for k in range(2, 11) if k**3 == cube), None)
        if not 2 <= base <= 12 or not 2 <= exponent <= 4 or sr*sr != square or cr is None:
            raise ValueError('Bounded powers and exact roots required')
        power = base**exponent
        result = power + sr*cr
        problem = f'Evaluate {base}{superscript(exponent)} + √{square} × ∛{cube}. Show the order of operations.'
        rows = [f'Identify the power {base}{superscript(exponent)} and the two roots before multiplying or adding.',
                f'Evaluate the power: {base}{superscript(exponent)} = {power}.',
                f'Evaluate the square root: √{square} = {sr} because {sr}² = {square}.',
                f'Evaluate the cube root: ∛{cube} = {cr} because {cr}³ = {cube}.',
                f'Multiply before adding: {sr} × {cr} = {sr*cr}.',
                f'Add the two terms: {power} + {sr*cr} = {result}.']
        check = f'{base**exponent} + {sr} × {cr} = {result}; both roots recover {square} and {cube}.'
        return str(result), rows, problem, check
    raise ValueError('Unsupported Grade 8 roots task')
