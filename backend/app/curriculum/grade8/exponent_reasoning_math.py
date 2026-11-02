"""Exact bounded Grade 8 exponent misconception and integrated-context tasks."""
from math import isqrt

SUP = str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹')


def power(b, e):
    return f'{b}{str(e).translate(SUP)}'


def square(n):
    r = isqrt(n)
    if not 2 <= r <= 20 or r*r != n:
        raise ValueError('Expected bounded exact square')
    return r


def cube(n):
    r = next((k for k in range(2, 11) if k**3 == n), None)
    if r is None:
        raise ValueError('Expected bounded exact cube')
    return r


def solve(kind, values):
    if not isinstance(values, list) or not all(type(x) is str and x.isdigit() and 1 <= len(x) <= 4 for x in values):
        raise ValueError('Expected bounded whole-number values')
    v = list(map(int, values))
    if kind == 'sign_audit' and len(v) == 2:
        b, e = v
        if not 2 <= b <= 12 or e not in (2, 4):
            raise ValueError('Signed scope inputs out of range')
        result = b**e
        prompt = f'A learner says (−{b}){str(e).translate(SUP)} = −{result}. Locate the first sign error and find the correct value.'
        rows = [f'The brackets include −{b} in every one of the {e} factors.',
                f'Expand (−{b}){str(e).translate(SUP)} into {" × ".join([f"(−{b})"]*e)}.',
                f'Pair the {e} negative signs: every pair produces a positive sign.',
                f'Multiply the magnitudes: {power(b,e)} = {result}.',
                f'The first error is treating a bracketed negative base as an outside minus; the correct value is {result}.']
        return str(result), rows, prompt, f'{" × ".join([f"(−{b})"]*e)} = {result}; the learner’s −{result} is not equal.'
    if kind == 'root_audit' and len(v) == 1:
        n, = v; r = square(n)
        prompt = f'A learner claims √{n} gives both a positive and a negative answer. What single value does √{n} represent?'
        rows = [f'The symbol √{n} means the principal, nonnegative square root.',
                f'Draw {n} unit squares as a {r} by {r} square.',
                f'{r}² = {n}; this verifies the side length {r}.',
                f'Although (−{r})² = {n}, the symbol √ chooses the nonnegative value.',
                f'So √{n} = {r}, not a two-value answer.']
        return str(r), rows, prompt, f'{r}² = {n} and {r} ≥ 0; √{n} = {r}.'
    if kind == 'quotient_audit' and len(v) == 3:
        b, m, n = v
        if not 2 <= b <= 9 or not 2 <= n < m <= 5:
            raise ValueError('Quotient inputs out of range')
        result = b**(m-n)
        prompt = f'A learner uses addition of exponents for {power(b,m)} ÷ {power(b,n)}. Show the first incorrect law and give the correct value.'
        rows = [f'Identify the nonzero common base {b} and the division sign.',
                f'Write {m} factors of {b} in the numerator and {n} in the denominator.',
                f'Cancel {n} equal nonzero pairs, leaving {m-n} numerator factors.',
                f'Division requires subtracting exponents: {m} − {n} = {m-n}.',
                f'Evaluate {power(b,m-n)} = {result}; adding exponents was the first wrong law.']
        return str(result), rows, prompt, f'{b**m} ÷ {b**n} = {result}; direct division confirms the quotient.'
    if kind == 'root_sum_audit' and len(v) == 2:
        a, b = v; x, y = square(a), square(b)
        result = x+y
        prompt = f'A learner replaces √{a} + √{b} with √({a} + {b}). Find the first incorrect step and evaluate the original expression.'
        rows = [f'A plus sign separates two roots. Keep √{a} and √{b} as separate terms.',
                f'Build a square from {a} tiles: √{a} = {x}.',
                f'Build a second square from {b} tiles: √{b} = {y}.',
                f'Now add their side values: {x} + {y} = {result}.',
                f'The first error was moving addition inside one square root; the original expression equals {result}.']
        return str(result), rows, prompt, f'{x}² = {a}, {y}² = {b}, and {x} + {y} = {result}.'
    if kind == 'mixed_audit' and len(v) == 4:
        b,m,n,rad=v
        if not 2 <= b <= 7 or not 2 <= m <= 4 or not 2 <= n <= 3 or m+n>6:
            raise ValueError('Mixed inputs out of range')
        r=square(rad);result=b**(m+n)+r
        prompt=f'A learner multiplies the exponents in {power(b,m)} × {power(b,n)} + √{rad}. Locate the first error and evaluate the expression.'
        rows=[f'Keep the multiplication of the two powers separate from the added root.',
              f'The powers have common base {b}: write {m} factors and another {n} factors.',
              f'Count {m}+{n}={m+n} equal factors, so the product is {power(b,m+n)}.',
              f'Evaluate {power(b,m+n)} = {b**(m+n)}.',
              f'Evaluate √{rad} = {r}, because {r}² = {rad}.',
              f'Add {b**(m+n)} + {r} = {result}. Multiplying the exponents was the first error.']
        return str(result),rows,prompt,f'({b**m} × {b**n}) + {r} = {result}; direct values agree.'
    if kind == 'square_perimeter_gap' and len(v)==2:
        a,b=v;x,y=square(a),square(b)
        if a>=b:raise ValueError('Areas must increase')
        gap=4*(y-x)
        prompt=f'Two square picture frames have areas {a} cm² and {b} cm². How many centimetres longer is the larger perimeter?'
        rows=[f'Each area is the side multiplied by itself: s₁²={a}, s₂²={b}.',
              f'Find the first side: √{a}={x} cm; a {x} by {x} square has area {a}.',
              f'Find the second side: √{b}={y} cm; a {y} by {y} square has area {b}.',
              f'The first perimeter is 4 × {x} = {4*x} cm.',
              f'The second perimeter is 4 × {y} = {4*y} cm.',
              f'Subtract perimeters: {4*y} − {4*x} = {gap} cm.']
        return f'{gap} cm',rows,prompt,f'{x}²={a}, {y}²={b}, and {4*y}−{4*x}={gap} cm.'
    if kind=='cube_edge_gap' and len(v)==2:
        a,b=v;x,y=cube(a),cube(b)
        if a>=b:raise ValueError('Volumes must increase')
        gap=y-x
        prompt=f'Two cubic boxes have volumes {a} cm³ and {b} cm³. How much longer is one edge of the larger box?'
        rows=[f'A cube has three equal edges; V=s³.',
              f'Take ∛{a}={x} cm, because {x} × {x} × {x} = {a}.',
              f'Take ∛{b}={y} cm, because {y} × {y} × {y} = {b}.',
              f'Compare edge lengths rather than subtracting volumes.',
              f'Subtract {y} − {x} = {gap} cm.']
        return f'{gap} cm',rows,prompt,f'{x}³={a}, {y}³={b}; the edge difference is {gap} cm.'
    if kind=='side_area_gap' and len(v)==3:
        base,exponent,area=v
        if not 2<=base<=5 or not 2<=exponent<=4:raise ValueError('Power side out of range')
        small=base**exponent;other=square(area)
        if small==other:raise ValueError('Sides must differ')
        gap=abs(small**2-area)
        prompt=f'One square display has side {power(base,exponent)} cm; another has area {area} cm². Find the difference between their areas.'
        rows=[f'First evaluate the given side: {power(base,exponent)}={small} cm.',
              f'Square that side to get the first area: {small} × {small}={small*small} cm².',
              f'The other display already has area {area} cm².',
              f'Its side would be √{area}={other} cm; check {other}²={area}.',
              f'Subtract the smaller area from the larger: {max(small*small,area)}−{min(small*small,area)}={gap} cm².']
        return f'{gap} cm²',rows,prompt,f'{power(base,exponent)}={small}; {small}²={small*small}, and |{small*small}−{area}|={gap} cm².'
    if kind=='root_power_compare' and len(v)==4:
        base,exponent,rad,volume=v
        if not 2<=base<=7 or not 2<=exponent<=4:raise ValueError('Power out of range')
        r,c=square(rad),cube(volume);p=base**exponent;right=r*c;gap=abs(p-right)
        prompt=f'Compare {power(base,exponent)} with √{rad} × ∛{volume}. By how much do the two values differ?'
        rows=[f'Keep the power on the left and product of roots on the right.',
              f'Evaluate the left: {power(base,exponent)} = {p}.',
              f'Evaluate √{rad} = {r}; {r}² = {rad}.',
              f'Evaluate ∛{volume} = {c}; {c}³ = {volume}.',
              f'Multiply the right: {r} × {c} = {right}.',
              f'Compare {p} and {right}; difference = {max(p,right)} − {min(p,right)} = {gap}.']
        return str(gap),rows,prompt,f'{p} and {r} × {c} = {right}; the absolute difference is {gap}.'
    if kind=='combined_perimeter' and len(v)==3:
        area1,area2,volume=v;x,y,c=square(area1),square(area2),cube(volume)
        result=4*x+4*y+c
        prompt=f'Two square garden beds have areas {area1} m² and {area2} m². A cubic planter has volume {volume} m³. Find the sum of both bed perimeters and one planter edge, in metres.'
        rows=[f'Label the first bed side √{area1} and the second √{area2}.',
              f'Find √{area1} = {x} m, since {x}² = {area1}.',
              f'Find √{area2} = {y} m, since {y}² = {area2}.',
              f'Find the planter edge ∛{volume} = {c} m, since {c}³ = {volume}.',
              f'The bed perimeters are 4 × {x} = {4*x} m and 4 × {y} = {4*y} m.',
              f'Add lengths only: {4*x} + {4*y} + {c} = {result} m.']
        return f'{result} m',rows,prompt,f'{x}²={area1}, {y}²={area2}, {c}³={volume}; {4*x}+{4*y}+{c}={result} m.'
    raise ValueError('Unsupported exponent reasoning task')
