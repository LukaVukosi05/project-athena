"""Author original Grade 11 analytical-geometry examples and assessment banks."""
from __future__ import annotations

import json
from fractions import Fraction
from hashlib import sha256
from math import gcd, isqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / 'docs/curriculum/grade11/analytical-geometry'
OUT = ROOT / 'backend/app/curriculum/grade11/generated'
ATP = 'https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2023%20ATPs/FET%20Content%20Subjects/Grade%2011/1.590%20ATP%202023-24%20Gr%2011%20Maths%20final.pdf'
TITLES = {
    1: 'Distance between two points',
    2: 'Gradient and direction of a line segment',
    3: 'Midpoints and missing endpoints',
    4: 'Equation of a line through two points',
    5: 'Parallel and perpendicular lines through a point',
    6: 'Inclination from exact gradients',
}
DIFFICULTIES = ['foundation']*2 + ['easy']*3 + ['standard']*4 + ['intermediate']*3 + ['exam']*3
TRIPLES = [(3,4,5),(5,12,13),(8,15,17)]

def fmt(value):
    f=Fraction(value)
    return str(f.numerator) if f.denominator==1 else f'{f.numerator}/{f.denominator}'

def coords(a):
    return f'({fmt(a[0])}, {fmt(a[1])})'

def line(slope,intercept):
    c=Fraction(intercept)
    return f'y = {fmt(slope)}x {"+" if c>=0 else "−"} {fmt(abs(c))}'

def case(n,i,variant=0):
    t=i+variant*15
    x=(t*3)%13-6
    y=(t*5)%13-6
    dx=2+(t%4)
    dy=(2+(t*2)%7)*(-1 if t%3==0 else 1)
    a=(x,y);b=(x+dx,y+dy)
    rise=dy;run=dx;m=Fraction(rise,run)
    if n==1:
        leg1,leg2,hyp=TRIPLES[(t-1)%3]
        if t%2: leg1,leg2=leg2,leg1
        scale=1+(t//9)
        b=(x+leg1*scale,y+leg2*scale)
        rise=b[1]-a[1];run=b[0]-a[0]
        length=hyp*scale
        problem=f'Find the distance between A{coords(a)} and B{coords(b)}.'
        answer=f'{length} units'
        steps=[f'Plot A{coords(a)} and B{coords(b)} on the same coordinate plane.',
               f'Draw the horizontal and vertical legs: Δx = {b[0]} − ({x}) = {run}; Δy = {b[1]} − ({y}) = {rise}.',
               f'Use Pythagoras: AB² = (Δx)² + (Δy)² = {run*run} + {rise*rise} = {length*length}.',
               f'Distance cannot be negative, so AB = √{length*length} = {length}.',
               f'Answer: AB = {length} units. Check: {run}² + {rise}² = {length}².']
        wrong=[f'{run+rise} units',f'{run} units',f'{length*length} units']
        visual={'mode':'distance','a':a,'b':b,'dx':run,'dy':rise,'length':length}
    elif n==2:
        problem=f'Calculate the gradient of line AB for A{coords(a)} and B{coords(b)}.'
        answer=f'm = {fmt(m)}'
        steps=[f'Plot A{coords(a)} and B{coords(b)}. Read x and y in the same point order.',
               f'Mark the horizontal run xB − xA = {b[0]} − ({x}) = {run}.',
               f'Mark the signed vertical rise yB − yA = {b[1]} − ({y}) = {rise}.',
               f'Divide rise by run: m = ({rise})/({run}) = {fmt(m)}.',
               f'Answer: m = {fmt(m)}. Check from A to B: run {run} and rise {rise}, so rise/run = {fmt(m)}.']
        wrong=[f'm = {fmt(-m)}',f'm = {fmt(Fraction(run,rise))}',f'm = {run+rise}']
        visual={'mode':'gradient','a':a,'b':b,'dx':run,'dy':rise,'m':fmt(m)}
    elif n==3:
        # Alternating direction requires either a midpoint or an endpoint.
        mid=(Fraction(a[0]+b[0],2),Fraction(a[1]+b[1],2))
        missing=t%2==0
        if missing:
            problem=f'A{coords(a)} and M{coords(mid)} are an endpoint and midpoint of AB. Find B.'
            answer=f'B{coords(b)}'
            steps=[f'Plot A{coords(a)} and midpoint M{coords(mid)}; leave B unknown.',
                   f'The midpoint formula gives Mx = (Ax + Bx)/2 and My = (Ay + By)/2.',
                   f'Solve Bx = 2({fmt(mid[0])}) − ({x}) = {b[0]}.',
                   f'Solve By = 2({fmt(mid[1])}) − ({y}) = {b[1]}.',
                   f'Answer: B{coords(b)}. Check: midpoint of A{coords(a)} and B{coords(b)} is M{coords(mid)}.']
            wrong=[f'B{coords(mid)}',f'B{coords((b[1],b[0]))}',f'B{coords((a[0]+b[0],a[1]+b[1]))}']
        else:
            problem=f'Find the midpoint M of A{coords(a)} and B{coords(b)}.'
            answer=f'M{coords(mid)}'
            steps=[f'Plot endpoints A{coords(a)} and B{coords(b)}.',
                   f'Add the x-coordinates: {x} + ({b[0]}) = {a[0]+b[0]}.',
                   f'Add the y-coordinates: {y} + ({b[1]}) = {a[1]+b[1]}.',
                   f'Divide each sum by 2: M = ({a[0]+b[0]}/2, {a[1]+b[1]}/2).',
                   f'Answer: M{coords(mid)}. Check: the horizontal and vertical offsets from A to M each equal those from M to B.']
            wrong=[f'M{coords((a[0]+b[0],a[1]+b[1]))}',f'M{coords((mid[1],mid[0]))}',f'M{coords(a)}']
        visual={'mode':'midpoint','a':a,'b':b,'mid':[fmt(z) for z in mid], 'missing':missing}
    elif n==4:
        c=Fraction(y)-m*x
        equation=line(m,c)
        problem=f'Determine the equation of line AB through A{coords(a)} and B{coords(b)} in y = mx + c form.'
        answer=equation
        steps=[f'Plot the two given points A{coords(a)} and B{coords(b)}.',
               f'Find the rise {rise} and run {run}; m = {rise}/{run} = {fmt(m)}.',
               f'Substitute A into y = mx + c: {y} = ({fmt(m)})({x}) + c.',
               f'Solve for c: c = {y} − ({fmt(m)})({x}) = {fmt(c)}.',
               f'Answer: {equation}. Check: replacing x with {b[0]} gives y = {b[1]}.']
        wrong=[line(-m,c),line(m,y),line(Fraction(run,rise),c)]
        visual={'mode':'equation','a':a,'b':b,'m':fmt(m),'c':fmt(c)}
    elif n==5:
        # Base slope has no zero case so the negative reciprocal is defined.
        target= m if t%2 else -1/m
        relation='parallel' if t%2 else 'perpendicular'
        p=(x+1,y-2)
        c=Fraction(p[1])-target*p[0]
        equation=line(target,c)
        problem=(f'Line AB through A{coords(a)} and B{coords(b)} has a {relation} line through P{coords(p)}. '
                 'Find the equation of the new line in y = mx + c form.')
        answer=equation
        steps=[f'Plot A{coords(a)}, B{coords(b)} and the new line point P{coords(p)}.',
               f'From A to B, rise = {rise} and run = {run}, so mAB = {fmt(m)}.',
               (f'Parallel lines have equal gradients: mnew = {fmt(target)}.' if relation=='parallel' else
                f'Perpendicular gradients multiply to −1: mnew = −1/({fmt(m)}) = {fmt(target)}.'),
               f'Substitute P into y = mnew x + c: c = {p[1]} − ({fmt(target)})({p[0]}) = {fmt(c)}.',
               f'Answer: {equation}. Check: P lies on the new line and its gradient is {fmt(target)}.']
        wrong=[line(m,c+1),line(-target,c),line(target,c+1)]
        visual={'mode':'parallel_perpendicular','a':a,'b':b,'p':p,'relation':relation,'base_m':fmt(m),'target_m':fmt(target),'c':fmt(c)}
    else:
        # Exact tan values are stored explicitly; only an upper-right or upper-left ray is drawn.
        angles=[30,45,60,120,135,150]
        slopes=['√3/3','1','√3','−√3','−1','−√3/3']
        theta=angles[(t-1)%6];symbol=slopes[(t-1)%6]
        p=(x,y)
        problem=(f'A line through P{coords(p)} has gradient m = {symbol}. '
                 'Determine its inclination θ, 0° ≤ θ < 180°.')
        answer=f'θ = {theta}°'
        steps=[f'Plot P{coords(p)} and a horizontal positive x-direction through it.',
               f'Inclination θ is measured anticlockwise from the positive x-direction, with 0° ≤ θ < 180°.',
               f'Use m = tan θ = {symbol}. The sign places the line in the {"obtuse" if theta>90 else "acute"} inclination sector.',
               f'The reference angle is {min(theta,180-theta)}°, giving θ = {theta}° in the required interval.',
               f'Answer: θ = {theta}°. Check: tan({theta}°) = {symbol} and the plotted line has the matching direction.']
        wrong=[f'θ = {180-theta}°',f'θ = {360-theta}°',f'θ = {90 if theta!=90 else 0}°']
        visual={'mode':'inclination','p':p,'theta':theta,'m':symbol}
    wrong=list(dict.fromkeys(w for w in wrong if w!=answer))
    offset=2
    while len(wrong)<3:
        if n==2:extra=f'm = {fmt(m+offset)}'
        elif n in (4,5):extra=line(m if n==4 else target,c+offset)
        elif n==3:extra=f'{"B" if missing else "M"}{coords((b[0]+offset,b[1]))}'
        elif n==6:extra=f'θ = {theta+offset}°'
        else:extra=f'{length+offset} units'
        if extra not in wrong and extra!=answer:wrong.append(extra)
        offset+=1
    assert len(steps)==5 and len({answer,*wrong[:3]})==4
    return {'id':f'g11-ag-l{n:02}-w{i:02}','lesson':n,'problem':problem,
            'answer':answer,'actions':steps,'check':steps[-1],
            'visual':{'family':'grade11_analytical','values':visual},'wrong':wrong[:3],
            'difficulty':DIFFICULTIES[i-1]}

def build():
    DOC.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    manifest=[]
    for n,title in TITLES.items():
        worked=[{k:v for k,v in case(n,i).items() if k!='wrong'} for i in range(1,16)]
        assert len({q['problem'] for q in worked})==15
        data={'source':f'grade11-ag-lesson-{n:02}.md','worked':worked}
        for section,amount,variant,prefix in (('practice',15,1,'p'),('mastery',5,2,'m'),('reassessment',3,3,'r')):
            items=[]
            for i in range(1,amount+1):
                item=case(n,i,variant)
                options=[item['answer'],*item['wrong']]
                shift=(i+variant)%4;options=options[shift:]+options[:shift]
                items.append({'id':f'g11-ag-l{n:02}-{prefix}{i:02}','prompt':item['problem'],
                    'options':options,'answer_index':options.index(item['answer']),
                    'actions':item['actions'],'memo':' '.join(item['actions'])})
            data[section]=items
        lines=[f'# Grade 11 Topic 5, Lesson {n}: {title}',
            f'Scope: [DBE Grade 11 Mathematics ATP, Term 2]({ATP}). Original Athena questions.',
            'Status: teacher review and live browser acceptance required. Plot the question coordinates before calculating.']
        for item in worked:
            lines.extend([f'## {item["id"]}: {item["problem"]}',
                f'Visual values: `{json.dumps(item["visual"],ensure_ascii=False)}`',
                *[f'{j}. {step}' for j,step in enumerate(item['actions'],1)],
                f'Answer: {item["answer"]}. Check: {item["check"]}'])
        for section in ('practice','mastery','reassessment'):
            lines.append(f'## {section.title()} answer key')
            for item in data[section]:
                lines.append(f'- {item["id"]}: {item["prompt"]} Options: {" | ".join(item["options"])}. '
                    f'Correct: {item["options"][item["answer_index"]]}. {item["memo"]}')
        source=DOC/data['source'];source.write_text('\n\n'.join(lines)+'\n',encoding='utf-8')
        (OUT/f'analytical_{n:02}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        manifest.append({'lesson_id':f'g11-ag-{n:02}','source':source.name,
            'source_sha256':sha256(source.read_bytes()).hexdigest(),
            'worked':15,'practice':15,'mastery':5,'reassessment':3,
            'status':'teacher_review_required','teacher_approved':False,'browser_accepted':False})
    (DOC/'topic5-acceptance-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':build()
