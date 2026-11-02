"""Original, checked Grade 8 2D shape cases; numerical and visual data share one source."""
from dataclasses import dataclass
from math import sqrt, radians, cos, sin


@dataclass(frozen=True)
class ShapeCase:
    id: str
    lesson: int
    family: str
    given: tuple[int, ...]
    answer: str
    problem: str
    working: tuple[str, ...]
    check: str
    misconception: str
    scene: dict


def triangle_sides(n, sides):
    a,b,c = sides  # BC, AC, AB
    assert a+b>c and a+c>b and b+c>a
    category = 'equilateral' if a==b==c else 'isosceles' if len(set(sides))==2 else 'scalene'
    x=(b*b+c*c-a*a)/(2*c)
    y=sqrt(b*b-x*x)
    # The SVG uses a common scale for all three sides, preserving classification.
    scale=min(230/c,145/y)
    pts=[[55,185],[55+c*scale,185],[55+x*scale,185-y*scale]]
    return ShapeCase(f'g8-shapes-01-w{n:02}',1,'triangle_sides',sides,category,
        f'Triangle ABC has BC = {a} cm, AC = {b} cm and AB = {c} cm. Classify it by its side lengths and give a reason.',
        (f'Mark BC = {a} cm, AC = {b} cm and AB = {c} cm on different sides.',
         'Compare the three lengths; equal lengths receive matching tick marks.',
         f'{len(set(sides))} distinct side length(s) occur.',
         f'Therefore the side classification is {category}.'),
        f'Lengths {a}, {b}, {c} match the {category} definition.',
        'Classify by equal side lengths, not by the apparent shape or an unmarked right angle.',
        {'shape':'triangle','points':pts,'labels':{'AB':str(c),'AC':str(b),'BC':str(a)}})


def triangle_sum(n, A, B):
    C=180-A-B
    assert 15<=A<=145 and 15<=B<=145 and 15<=C<=145
    # Intersect rays from the ends of the base at the specified angles.
    import math
    t=math.tan(math.radians(A));u=math.tan(math.radians(B))
    x=250*u/(t+u);h=x*t;scale=min(1,140/h)
    pts=[[45,185],[45+250*scale,185],[45+x*scale,185-h*scale]]
    return ShapeCase(f'g8-shapes-02-w{n:02}',2,'triangle_sum',(A,B),f'{C}°',
        f'In triangle ABC, angle A = {A}° and angle B = {B}°. Find angle C and state the theorem.',
        (f'Highlight angle A = {A}° and angle B = {B}°.',
         'The three interior angles of any triangle add to 180°.',
         f'{A}° + {B}° + C = 180°.',f'C = 180° − {A}° − {B}° = {C}°.'),
        f'{A}° + {B}° + {C}° = 180°.',
        'Do not use 360° for a triangle or treat the exterior angle as an interior angle.',
        {'shape':'triangle','points':pts,'angles':{'A':f'{A}°','B':f'{B}°','C':'x'},'result_angle':'C'})


def equal_triangle(n, kind, known, target):
    assert kind in ('equilateral','isosceles')
    if kind=='equilateral':
        assert known==60 and target=='angle'; answer=60
        side=4+n
        problem=f'Triangle ABC has AB = BC = CA = {side} cm. Find angle C and justify its size.'
        working=('Mark all three sides equal.','Equal sides in an equilateral triangle give three equal angles.',
                 'A + B + C = 180° and A = B = C.','C = 180° ÷ 3 = 60°.')
        check='60° + 60° + 60° = 180°.'
        points=[[180,185-100*sqrt(3)],[80,185],[280,185]]
    else:
        assert 10<known<160 and target in ('base','vertex')
        if target=='base':
            answer=(180-known)//2;assert (180-known)%2==0
            problem=f'Triangle ABC has AB = AC and vertex angle A = {known}°. Find base angle B.'
            working=('Mark AB and AC with matching ticks.','Their opposite base angles B and C are equal.',
                     f'B + C = 180° − {known}° = {180-known}°.',f'B = C = {180-known}° ÷ 2 = {answer}°.')
            check=f'{known}° + {answer}° + {answer}° = 180°.'
        else:
            answer=180-2*known;assert answer>0
            problem=f'Triangle ABC has AB = AC and base angle B = {known}°. Find vertex angle A.'
            working=('Mark the two equal sides AB and AC.','Base angles B and C are opposite those equal sides, so C = B.',
                     f'B = C = {known}°.',f'A = 180° − {known}° − {known}° = {answer}°.')
            check=f'{answer}° + {known}° + {known}° = 180°.'
        points=[[170,52],[55,185],[285,185]]
    angles={'A':f'{known}°' if kind=='isosceles' and target=='base' else ('x' if kind=='isosceles' else '60°'),
            'B':f'{known}°' if kind=='isosceles' and target=='vertex' else ('x' if kind=='isosceles' else '60°'),
            'C':'x' if kind=='equilateral' else ''}
    return ShapeCase(f'g8-shapes-03-w{n:02}',3,'equal_triangle',(known,),f'{answer}°',problem,working,check,
        'Equal sides imply equal opposite angles; an isosceles triangle does not necessarily have three equal angles.',
        {'shape':'triangle','points':points,'angles':angles,'ticks':kind,'result_angle':'C' if kind=='equilateral' else target})

QUADS={
 'parallelogram':([[80,175],[260,175],[305,55],[125,55]],'both pairs of opposite sides parallel, with no right-angle or four-equal-side marking'),
 'rectangle':([[65,175],[295,175],[295,65],[65,65]],'four right angles and unequal adjacent side lengths'),
 'square':([[90,180],[250,180],[250,20],[90,20]],'four right angles and four equal sides'),
 'rhombus':([[65,105],[170,25],[275,105],[170,185]],'four equal sides, with no right angle'),
 'trapezium':([[65,175],[295,175],[245,65],[100,65]],'exactly one pair of opposite sides parallel'),
 'kite':([[60,125],[170,20],[280,125],[170,190]],'two pairs of equal adjacent sides, with no opposite parallel pair')}

def classify_quad(n,kind):
    points,properties=QUADS[kind]
    return ShapeCase(f'g8-shapes-04-w{n:02}',4,'quad_classify',(n,),kind,
        f'Quadrilateral ABCD has {properties}; AB is marked {n+3} cm. Give its most specific name and justify it.',
        ('Locate every parallel mark, equal-side tick and right-angle square.',
         f'The given markings establish: {properties}.',
         'Compare this evidence with the definitions of square, rectangle, rhombus, parallelogram, trapezium and kite.',
         f'The most specific matching name is {kind}.'),
        f'{kind} satisfies the explicitly stated side and angle markings.',
        'Do not decide from a slanted drawing alone; use the stated markings and the most specific definition.',
        {'shape':'quadrilateral','points':points,'properties':properties})


def _normalise_polygon(points):
    xs,ys=zip(*points)
    scale=min(260/(max(xs)-min(xs)),140/(max(ys)-min(ys)))
    return [[45+(x-min(xs))*scale,185-(y-min(ys))*scale] for x,y in points]


def _sum_polygon(A,B,C):
    """Intersect the last edge with the ray from A; all four angles follow."""
    heading_b=radians(180-B)
    heading_c=radians(360-B-C)
    a=(0.,0.);b=(180.,0.)
    c=(b[0]+100*cos(heading_b),100*sin(heading_b))
    v=(cos(heading_c),sin(heading_c));w=(cos(radians(A)),sin(radians(A)))
    cross=lambda u,v:u[0]*v[1]-u[1]*v[0]
    denominator=cross(v,w)
    if abs(denominator)<1e-8:raise ValueError('Degenerate quadrilateral')
    t=cross((-c[0],-c[1]),w)/denominator
    s=cross((-c[0],-c[1]),v)/denominator
    if min(t,s)<=0:raise ValueError('Quadrilateral edges must meet in front of the vertices')
    return _normalise_polygon((a,b,c,(s*w[0],s*w[1])))


def _parallelogram(A):
    offset=(100*cos(radians(A)),100*sin(radians(A)))
    return _normalise_polygon(((0,0),(180,0),(180+offset[0],offset[1]),offset))


def quad_angle(n,kind,angles):
    assert kind in ('sum','parallelogram_opposite','parallelogram_adjacent')
    if kind=='sum':
        A,B,C=angles;D=360-A-B-C;assert 15<D<180
        problem=f'Quadrilateral ABCD has angles A = {A}°, B = {B}° and C = {C}°. Find angle D.'
        working=(f'Mark A = {A}°, B = {B}° and C = {C}°.',
                 'Draw a diagonal: two triangles give 180° + 180° = 360°.',
                 f'{A}° + {B}° + {C}° + D = 360°.',
                 f'D = 360° − {A}° − {B}° − {C}° = {D}°.')
        check=f'{A}° + {B}° + {C}° + {D}° = 360°.'
        scene={'shape':'quadrilateral','points':_sum_polygon(A,B,C),'angles':{'A':f'{A}°','B':f'{B}°','C':f'{C}°','D':'x'},'kind':kind}
    else:
        (A,)=angles;assert 20<A<160
        if kind=='parallelogram_opposite':
            D=A;problem=f'ABCD is a parallelogram and angle A = {A}°. Find opposite angle C.'
            working=('Mark both pairs of opposite sides parallel.',f'Angle A = {A}°.',
                     'Opposite angles in a parallelogram are equal.',f'Angle C = {A}°.')
            check=f'Opposite angles A and C both equal {A}°.'
        else:
            D=180-A;problem=f'ABCD is a parallelogram and angle A = {A}°. Find adjacent angle B.'
            working=('Mark the opposite sides parallel.',f'Angle A = {A}°.',
                     'Adjacent angles on a side between parallel lines sum to 180°.',f'Angle B = 180° − {A}° = {D}°.')
            check=f'{A}° + {D}° = 180°.'
        scene={'shape':'quadrilateral','points':_parallelogram(A),'angles':{'A':f'{A}°','C':'x' if kind.endswith('opposite') else '', 'B':'x' if kind.endswith('adjacent') else ''},'kind':kind}
    return ShapeCase(f'g8-shapes-05-w{n:02}',5,'quad_angle',angles,f'{D}°',problem,working,check,
        'The interior angle sum for a quadrilateral is 360°; parallelograms also have equal opposite and supplementary adjacent angles.',scene)

LESSONS={
 1:tuple(triangle_sides(i,s) for i,s in enumerate(((5,5,5),(5,5,8),(3,4,5),(7,7,10),(6,6,6),(5,6,7),(6,8,10),(9,9,12),(4,4,7),(8,9,10),(11,11,11),(7,8,9),(10,10,16),(12,13,17),(13,14,15)),1)),
 2:tuple(triangle_sum(i,a,b) for i,(a,b) in enumerate(((50,60),(35,75),(90,40),(65,65),(42,78),(25,95),(70,45),(80,30),(55,85),(46,64),(30,100),(75,55),(62,38),(105,35),(44,86)),1)),
 3:tuple(equal_triangle(i,*row) for i,row in enumerate((('equilateral',60,'angle'),('isosceles',40,'base'),('isosceles',55,'vertex'),('isosceles',70,'base'),('isosceles',35,'vertex'),('equilateral',60,'angle'),('isosceles',100,'base'),('isosceles',48,'vertex'),('isosceles',32,'base'),('isosceles',68,'vertex'),('equilateral',60,'angle'),('isosceles',116,'base'),('isosceles',73,'vertex'),('isosceles',24,'base'),('isosceles',81,'vertex')),1)),
 4:tuple(classify_quad(i,k) for i,k in enumerate(('square','rectangle','rhombus','parallelogram','trapezium','kite','rectangle','square','kite','rhombus','parallelogram','trapezium','square','rectangle','rhombus'),1)),
 5:tuple(quad_angle(i,k,v) for i,(k,v) in enumerate((('sum',(80,105,95)),('parallelogram_opposite',(68,)),('parallelogram_adjacent',(112,)),('sum',(75,85,110)),('parallelogram_adjacent',(74,)),('sum',(105,80,100)),('parallelogram_opposite',(123,)),('sum',(95,78,92)),('parallelogram_adjacent',(57,)),('sum',(112,79,84)),('parallelogram_opposite',(79,)),('sum',(70,110,85)),('parallelogram_adjacent',(129,)),('sum',(83,117,75)),('parallelogram_opposite',(46,))),1))}


def variant(case,shift):
    assert 1<=shift<=4
    n=int(case.id[-2:]);family=case.family
    if family=='triangle_sides':
        return triangle_sides(n,tuple(v+shift for v in case.given))
    if family=='triangle_sum':
        a,b=case.given;return triangle_sum(n,a+shift,b+shift)
    if family=='equal_triangle':
        kind=case.scene['ticks'];known=case.given[0]
        # Equilateral angles cannot change: change labelled side lengths and ask the same invariant.
        if kind=='equilateral':
            c=equal_triangle(n,kind,60,'angle')
            from dataclasses import replace
            side=5+shift+n
            return replace(c,problem=f'Triangle ABC has AB = BC = CA = {side} cm. Find angle C and justify its size.',given=(side,))
        target=case.scene['result_angle'];return equal_triangle(n,kind,known+2*shift,target)
    if family=='quad_classify':
        c=classify_quad(n,case.answer)
        from dataclasses import replace
        # New given drawing orientation is an independent instance of the same class.
        return replace(c,problem=f'A new quadrilateral EFGH has {QUADS[case.answer][1]}. Name its most specific class and justify it.',
                       scene={**c.scene,'rotation':shift*7,'vertices':'EFGH'})
    k=case.scene['kind'];base=case.given
    return quad_angle(n,k,tuple(v+shift for v in base))


def validate_all():
    assert len(LESSONS)==5
    for num,cases in LESSONS.items():
        assert len(cases)==15 and len({c.id for c in cases})==15
        assert all(c.lesson==num and len(c.working)>=4 and c.check and c.answer for c in cases)
        assert len({c.problem for c in cases})==15
        for c in cases:
            for shift in (1,2,3):
                other=variant(c,shift)
                assert other.problem!=c.problem
    return True

validate_all()
