"""Authored Grade 8 Pythagoras cases. One numerical record drives mathematics and SVG."""
from dataclasses import dataclass
from math import isqrt


def root(n):
    assert isinstance(n, int) and n > 0
    factor = next(d for d in range(isqrt(n), 0, -1) if n % (d*d) == 0)
    remaining = n // (factor*factor)
    return str(factor) if remaining == 1 else f'{factor if factor > 1 else ""}√{remaining}'


@dataclass(frozen=True)
class Case:
    id: str
    lesson: int
    family: str
    a: int
    b: int
    c: int | None
    problem: str
    answer: str
    working: tuple[str, ...]
    check: str
    misconception: str
    context: str = ''


def make(lesson, index, a, b, c=None, context=''):
    assert (a == 0 if lesson == 3 else a > 0) and b > 0 and (c is None or c > 0)
    qid=f'g8-pyth-{lesson:02}-w{index:02}'
    if lesson == 1:
        assert c is None
        total=a*a+b*b
        problem=f'A right-angled triangle has perpendicular sides of {a} cm and {b} cm. Find the areas of the squares on the two shorter sides and the square on the longest side.'
        working=(f'The two given sides meet at the marked right angle: {a} cm and {b} cm.',
                 f'The first square has area {a} × {a} = {a*a} cm².',
                 f'The second square has area {b} × {b} = {b*b} cm².',
                 f'Add the two areas: {a*a} + {b*b} = {total} cm².',
                 f'The square on the hypotenuse has area {total} cm².')
        answer=f'{a*a} cm², {b*b} cm²; hypotenuse square {total} cm²'
        check=f'{a*a} + {b*b} = {total} cm²; areas, not side lengths, are added.'
        misconception='A side length is in cm; its square area is in cm². Do not add the side lengths.'
        family='square_areas'
    elif lesson == 2:
        assert c is None
        n=a*a+b*b; r=root(n)
        problem=f'Triangle ABC is right-angled at A. AB = {a} cm and AC = {b} cm. Calculate the length BC exactly.'
        working=('BC is opposite the marked right angle, so it is the hypotenuse.',
                 f'Write BC² = AB² + AC² = {a}² + {b}².',
                 f'Square separately: BC² = {a*a} + {b*b}.',
                 f'Add: BC² = {n}.',
                 f'Take the nonnegative square root because BC is a length: BC = √{n} = {r} cm.')
        answer=f'{r} cm';check=f'({r})² = {n} = {a*a} + {b*b}; BC is longer than both legs.'
        misconception='Take the square root after adding the squares, not before. The hypotenuse must be longest.'
        family='hypotenuse'
    elif lesson == 3:
        assert c is not None and c > b
        n=c*c-b*b; r=root(n)
        problem=f'Triangle ABC is right-angled at A. BC = {c} cm and AC = {b} cm. Calculate AB exactly.'
        working=(f'BC = {c} cm is opposite the right angle and is the longest side.',
                 f'Use AB² + AC² = BC², so AB² + {b}² = {c}².',
                 f'Square the numbers: AB² + {b*b} = {c*c}.',
                 f'Subtract the known square: AB² = {c*c} − {b*b} = {n}.',
                 f'AB is a positive length, so AB = √{n} = {r} cm.')
        answer=f'{r} cm';check=f'({r})² + {b*b} = {n} + {b*b} = {c*c} = {c}².'
        misconception='For a missing leg subtract the known leg squared from the hypotenuse squared; never reverse them.'
        family='missing_leg'
    elif lesson == 4:
        assert c is not None and all(x > 0 for x in (a,b,c))
        x,y,z=sorted((a,b,c));assert x+y>z
        left=x*x+y*y;right=z*z;is_right=left==right
        problem=f'A triangle has side lengths {a} cm, {b} cm and {c} cm. Decide whether it is right-angled, and justify with squares.'
        working=(f'Identify the longest side: {z} cm. The two others are {x} cm and {y} cm.',
                 f'Square and add the two shorter sides: {x}² + {y}² = {x*x} + {y*y} = {left}.',
                 f'Square the longest side: {z}² = {right}.',
                 f'Compare: {left} {"=" if is_right else "≠"} {right}.',
                 'The converse of Pythagoras confirms a right angle.' if is_right else 'The squared lengths do not match, so this triangle is not right-angled.')
        answer='right-angled' if is_right else 'not right-angled'
        check=f'{x}² + {y}² = {left} {"=" if is_right else "≠"} {right} = {z}².'
        misconception='Do not assume a triangle is right-angled from its appearance; compare the square of the longest side.'
        family='converse'
    else:
        assert lesson == 5 and c is None
        n=a*a+b*b;r=root(n)
        descriptions={
            'ladder':f'A ladder rests {a} m from a vertical wall and reaches {b} m up the wall. How long is the ladder? Give an exact answer.',
            'rectangle':f'A rectangular floor is {a} m long and {b} m wide. Find the diagonal length exactly.',
            'ramp':f'A ramp rises {b} m over a horizontal run of {a} m. Find the sloped length exactly.',
            'route':f'Walk {a} km east and then {b} km north. Find the straight-line distance back to the starting point exactly.',
            'screen':f'A rectangular display is {a} cm wide and {b} cm high. Find its diagonal exactly.',
        }
        assert context in descriptions
        problem=descriptions[context]
        working=(f'Mark the horizontal {a} {"cm" if context=="screen" else "m" if context!="route" else "km"} and vertical {b} with a right-angle corner.',
                 'The requested straight or sloping length is opposite the right angle; label it h.',
                 f'Use h² = {a}² + {b}².',f'Calculate the squares: h² = {a*a} + {b*b} = {n}.',
                 f'Take the positive root: h = √{n} = {r} {"cm" if context=="screen" else "km" if context=="route" else "m"}.')
        unit='cm' if context=='screen' else 'km' if context=='route' else 'm'
        answer=f'{r} {unit}';check=f'({r})² = {n} = {a*a} + {b*b}; the diagonal/sloping line is longest.'
        misconception='Draw the perpendicular sides first; do not add their lengths to get the diagonal.'
        family='application'
    return Case(qid,lesson,family,a,b,c,problem,answer,working,check,misconception,context)

# Cases 11–15 intentionally mix unfamiliar values and longer reasoning, including exact surds.
DATA={
 1:[(3,4),(5,12),(6,8),(7,24),(8,15),(9,12),(10,24),(12,16),(15,20),(11,13),(13,17),(14,19),(16,21),(18,23),(19,27)],
 2:[(3,4),(5,12),(6,8),(8,15),(7,24),(2,3),(4,7),(10,11),(9,20),(12,13),(15,22),(17,25),(18,29),(21,32),(23,34)],
 3:[(0,4,5),(0,5,13),(0,8,10),(0,12,13),(0,15,17),(0,3,6),(0,7,12),(0,9,15),(0,11,18),(0,13,20),(0,14,25),(0,16,29),(0,19,35),(0,22,41),(0,25,46)],
 4:[(3,4,5),(5,12,13),(6,8,10),(8,15,17),(7,24,25),(4,5,6),(6,7,10),(8,9,13),(10,10,14),(13,14,20),(9,12,16),(16,30,34),(15,20,26),(20,21,29),(18,24,31)],
 5:[(3,4,'ladder'),(5,12,'rectangle'),(6,8,'ramp'),(8,15,'route'),(7,24,'screen'),(4,7,'ladder'),(9,10,'rectangle'),(11,13,'ramp'),(12,16,'route'),(14,19,'screen'),(17,23,'ladder'),(18,29,'rectangle'),(21,32,'ramp'),(24,35,'route'),(28,39,'screen')],
}
LESSONS={n:[make(n,i,values[0],values[1],context=values[2]) if n==5 else make(n,i,*values) if n==4 else make(n,i,values[0],values[1],values[2]) if n==3 else make(n,i,*values) for i,values in enumerate(items,1)] for n,items in DATA.items()}

def variant(case,shift):
    if case.lesson==3:return make(3,int(case.id[-2:]),0,case.b+shift,case.c+2*shift)
    if case.lesson==4:
        # Preserve right status for right triangles; alter all three sides by scaling.
        if case.answer=='right-angled':return make(4,int(case.id[-2:]),case.a*(shift+1),case.b*(shift+1),case.c*(shift+1))
        return make(4,int(case.id[-2:]),case.a+shift,case.b+shift,case.c+shift)
    return make(case.lesson,int(case.id[-2:]),case.a+shift,case.b+shift,context=case.context)
