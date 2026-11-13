"""Original Grade 11 function-graph source banks, including trig graph transformations."""
from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/curriculum/grade11/functions-graphs'
OUT=ROOT/'backend/app/curriculum/grade11/generated'
ATP='https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2023%20ATPs/FET%20Content%20Subjects/Grade%2011/1.590%20ATP%202023-24%20Gr%2011%20Maths%20final.pdf'
TITLES={1:'Quadratic graph translations and turning points',
        2:'Hyperbola asymptotes and translations',
        3:'Exponential graph shifts and plotted values',
        4:'Average gradient between two points on a curve',
        5:'Point-by-point sine, cosine and tangent graphs',
        6:'Frequency parameter and period of trigonometric graphs',
        7:'Horizontal shifts of trigonometric graphs',
        8:'Two-parameter trigonometric sketch reasoning'}
DIFF=['foundation']*2+['easy']*3+['standard']*4+['intermediate']*3+['exam']*3
def sign(x):return f'+ {x}' if x>=0 else f'− {abs(x)}'

def case(n,i,variant=0):
    t=i+variant*15
    if n==1:
        a=[1,-1,2,-2][(t-1)%4];p=(t*3)%9-4;q=(t*5)%11-5
        # Avoid identical points across the 15 questions; the tuple varies with t.
        ans=f'({-p}, {q})'
        problem=f'For f(x) = {a}(x {sign(p)})² {sign(q)}, find the turning point and identify its graph.'
        actions=[f'Start with the parent parabola y = x² and mark its turning point (0, 0).',
                 f'The bracket x {sign(p)} moves the graph {abs(p)} units {"left" if p>0 else "right" if p<0 else "horizontally by zero"}.',
                 f'The {sign(q)} term shifts the graph vertically to the turning point ({-p}, {q}).',
                 f'The coefficient {a} makes the parabola open {"up" if a>0 else "down"}; plot points one unit to either side of x = {-p}.',
                 f'Answer: turning point {ans}. Check: f({-p}) = {q}, with symmetric points at x = {-p-1} and x = {-p+1}.']
        wrong=[f'({p}, {q})',f'({-p}, {-q})',f'({p}, {-q})']
        values={'mode':'quadratic','a':a,'p':p,'q':q,'vertex':[-p,q]}
    elif n==2:
        a=[2,-2,3,-3][(t-1)%4];p=(t*2)%9-4;q=(t*3)%9-4
        problem=f'For f(x) = {a}/(x {sign(p)}) {sign(q)}, state both asymptotes.'
        ans=f'x = {-p}; y = {q}'
        actions=[f'Start with y = {a}/x, which is undefined at x = 0 and approaches y = 0.',
                 f'Set the denominator to zero: x {sign(p)} = 0, so x = {-p} is excluded.',
                 f'Draw the vertical asymptote x = {-p}; translate the two branches around it.',
                 f'The vertical shift {sign(q)} moves the horizontal asymptote to y = {q}.',
                 f'Answer: {ans}. Check: the denominator vanishes at x = {-p} and f(x) approaches {q} for large |x|.']
        wrong=[f'x = {p}; y = {q}',f'x = {-p}; y = {-q}',f'x = {p}; y = {-q}']
        values={'mode':'hyperbola','a':a,'p':p,'q':q,'vertical':-p,'horizontal':q}
    elif n==3:
        a=[1,2,-1][(t-1)%3];b=2+(t%4);p=(t*3)%9-4;q=(t*5)%7-3
        x=1-p;y=a*b+q
        problem=f'On f(x) = {a}·{b}^(x {sign(p)}) {sign(q)}, find the point where x = {x}.'
        ans=f'({x}, {y})'
        actions=[f'Start with b^x for base b = {b} > 0, b ≠ 1; mark its value 1 at x = 0.',
                 f'For x = {x}, calculate the exponent: x {sign(p)} = 1.',
                 f'The exponential value is {b}¹ = {b}; multiply by {a} to obtain {a*b}.',
                 f'Apply the vertical shift {sign(q)}: f({x}) = {a*b} {sign(q)} = {y}.',
                 f'Answer: {ans}. Check: substituting x = {x} into the original function gives {y}.']
        wrong=[f'({x}, {a+q})',f'({x}, {a*b-q})',f'({-x}, {y})']
        values={'mode':'exponential','a':a,'b':b,'p':p,'q':q,'target_x':x,'target_y':y}
    elif n==4:
        a=[1,2,-1,-2][(t-1)%4];p=(t*2)%7-3;q=(t*3)%7-3;x0=(t*5)%9-4;h=1+(t%4);x1=x0+h
        f=lambda x:a*(x+p)**2+q
        y0,y1=f(x0),f(x1);slope=(y1-y0)//h
        problem=f'For f(x) = {a}(x {sign(p)})² {sign(q)}, find the average gradient from x = {x0} to x = {x1}.'
        ans=f'm = {slope}'
        actions=[f'Plot the first point A = ({x0}, f({x0})) on the parabola.',
                 f'Calculate f({x0}) = {y0} and f({x1}) = {y1}, then plot B = ({x1}, {y1}).',
                 f'Draw the secant AB; its horizontal run is {x1} − ({x0}) = {h}.',
                 f'Its signed rise is {y1} − ({y0}) = {y1-y0}; average gradient = ({y1-y0})/{h} = {slope}.',
                 f'Answer: {ans}. Check: {slope} × {h} = {y1-y0}, the actual change in f.']
        wrong=[f'm = {-slope}',f'm = {y1-y0}',f'm = {h}']
        values={'mode':'secant','a':a,'p':p,'q':q,'x0':x0,'x1':x1,'y0':y0,'y1':y1,'slope':slope}
    elif n==5:
        # Exact values for 30°, 45°, 60°, 90°, 180° and their signed/translated angles.
        sine={0:'0',30:'1/2',45:'√2/2',60:'√3/2',90:'1',120:'√3/2',135:'√2/2',150:'1/2',180:'0',210:'−1/2',225:'−√2/2',240:'−√3/2',270:'−1',300:'−√3/2',315:'−√2/2',330:'−1/2'}
        cosine={0:'1',30:'√3/2',45:'√2/2',60:'1/2',90:'0',120:'−1/2',135:'−√2/2',150:'−√3/2',180:'−1',210:'−√3/2',225:'−√2/2',240:'−1/2',270:'0',300:'1/2',315:'√2/2',330:'√3/2'}
        tangent={0:'0',30:'√3/3',45:'1',60:'√3',120:'−√3',135:'−1',150:'−√3/3',180:'0',210:'√3/3',225:'1',240:'√3',300:'−√3',315:'−1',330:'−√3/3'}
        fn=['sin','cos','tan'][(t-1)%3]
        theta=[-330,-300,-270,-240,-225,-210,-180,-150,-135,-120,-90,-60,-45,-30,0,30,45,60,90,120,135,150,180,210,225,240,270,300,315,330][(t*7)%30]
        if fn=='tan' and theta%180==90:theta+=30
        reduced=theta%360
        table={'sin':sine,'cos':cosine,'tan':tangent}[fn]
        assert reduced in table,(fn,theta)
        result=table[reduced];problem=f'Use a point-by-point sketch of y = {fn} θ to find {fn}({theta}°).'
        ans=f'{fn}({theta}°) = {result}'
        actions=[f'Mark the horizontal angle axis from −360° to 360° and the parent {fn} curve.',
                 f'Locate θ = {theta}° on the axis; a full 360° turn gives equivalent angle {reduced}°.',
                 f'Trace vertically to the {fn} curve, respecting its sign and any undefined tangent positions.',
                 f'Read the ordinate from the exact special angle: {fn}({theta}°) = {result}.',
                 f'Answer: {ans}. Check the quadrant sign and the periodic value at {reduced}°.']
        wrong=[f'{fn}({theta}°) = 0' if result!='0' else f'{fn}({theta}°) = 1',
               f'{fn}({theta}°) = −{result}' if not result.startswith('−') else f'{fn}({theta}°) = {result[1:]}',
               f'{fn}({theta}°) = 1/2' if result!='1/2' else f'{fn}({theta}°) = √3/2']
        values={'mode':'trig_point','fn':fn,'theta':theta,'result':result}
    elif n==6:
        fn=['sin','cos','tan'][(t-1)%3];k=1+(t-1)//3%5
        base=180 if fn=='tan' else 360;period=base//k
        problem=f'For y = {fn}({k}x), determine the period in degrees.'
        ans=f'period = {period}°'
        actions=[f'Start with the parent y = {fn} x; its period is {base}°.',
                 f'The factor k = {k} changes how rapidly the input angle is traversed.',
                 f'Plot the parent and transformed graphs together over −360° to 360°.',
                 f'One cycle of y = {fn}({k}x) takes {base}° ÷ {k} = {period}°.',
                 f'Answer: {ans}. Check the transformed graph repeats after a horizontal shift of {period}°.']
        wrong=[f'period = {base*k}°',f'period = {base}°' if k!=1 else f'period = {base//2}°',f'period = {period+30}°']
        values={'mode':'trig_frequency','fn':fn,'k':k,'period':period}
    elif n==7:
        fn=['sin','cos','tan'][(t-1)%3];p=((t*7)%17-8)*30
        if p==0:p=270
        direction='left' if p>0 else 'right'
        problem=f'For y = {fn}(x {sign(p)}°), describe the horizontal translation of the parent graph.'
        ans=f'{abs(p)}° {direction}'
        actions=[f'Sketch the parent {fn} curve on axes covering −360° to 360°.',
                 f'Find the input that replaces parent x = 0: x {sign(p)}° = 0.',
                 f'Therefore the reference point moves from x = 0° to x = {-p}°.',
                 f'Translate every corresponding point {abs(p)}° {direction}; keep amplitude and period unchanged.',
                 f'Answer: {ans}. Check the shifted input equals zero at x = {-p}°.']
        wrong=[f'{abs(p)}° {"right" if direction=="left" else "left"}',f'{abs(p)+30}° {direction}',f'{abs(p)} units up']
        values={'mode':'trig_shift','fn':fn,'p':p,'shift':-p}
    else:
        fn=['sin','cos','tan'][(t-1)%3];a=[-3,-2,-1,2,3][(t-1)//3%5];k=1+(t%3)
        base=180 if fn=='tan' else 360;period=base//k
        # Tan has no bounded amplitude. Ask for vertical scale there.
        property_name='vertical scale' if fn=='tan' else 'amplitude'
        problem=f'For y = {a}{fn}({k}x), find its {property_name} and period in degrees.'
        ans=f'{property_name} = {abs(a)}; period = {period}°'
        actions=[f'Start with y = {fn} x and mark its original cycle {base}°.',
                 f'The factor {k} inside the function divides the cycle width by {k}.',
                 f'The coefficient {a} outside multiplies each ordinate by {a}, including a reflection if negative.',
                 f'The {property_name} is {abs(a)} and the cycle width is {base}/{k} = {period}°.',
                 f'Answer: {ans}. Check consecutive corresponding features are {period}° apart.']
        wrong=[f'{property_name} = {abs(a)}; period = {base*k}°',
               f'{property_name} = {k}; period = {period}°',
               f'{property_name} = {abs(a)+1}; period = {period}°']
        values={'mode':'trig_two','fn':fn,'a':a,'k':k,'period':period}
    wrong=list(dict.fromkeys(w for w in wrong if w!=ans))
    offset=1
    while len(wrong)<3:
        if n==1:extra=f'({-p}, {q+offset})'
        elif n==2:extra=f'x = {-p+offset}; y = {q}'
        elif n==3:extra=f'({x}, {y+offset})'
        elif n==4:extra=f'm = {slope+offset}'
        elif n==5:
            other=['0','1/2','−1/2','√2/2','−√2/2','√3/2','−√3/2','1','−1','√3','−√3'][(offset-1)%11]
            extra=f'{fn}({theta}°) = {other}'
        elif n==6:extra=f'period = {period+30*offset}°'
        elif n==7:extra=f'{abs(p)+30*offset}° {direction}'
        else:extra=f'{property_name} = {abs(a)+offset}; period = {period}°'
        if extra not in wrong and extra!=ans:wrong.append(extra)
        offset+=1
    assert len(actions)==5 and len({ans,*wrong[:3]})==4
    return {'id':f'g11-fn-l{n:02}-w{i:02}','lesson':n,'problem':problem,
            'answer':ans,'actions':actions,'check':actions[-1],
            'visual':{'family':'grade11_functions','values':values},'wrong':wrong[:3],
            'difficulty':DIFF[i-1]}

def build():
    DOC.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True);manifest=[]
    for n,title in TITLES.items():
        worked=[{k:v for k,v in case(n,i).items() if k!='wrong'} for i in range(1,16)]
        assert len({x['problem'] for x in worked})==15,(n,'duplicate')
        data={'source':f'grade11-fn-lesson-{n:02}.md','worked':worked}
        for section,amount,variant,prefix in [('practice',15,1,'p'),('mastery',5,2,'m'),('reassessment',3,3,'r')]:
            items=[]
            for i in range(1,amount+1):
                c=case(n,i,variant);options=[c['answer'],*c['wrong']];shift=(i+variant)%4
                options=options[shift:]+options[:shift]
                items.append({'id':f'g11-fn-l{n:02}-{prefix}{i:02}','prompt':c['problem'],
                    'options':options,'answer_index':options.index(c['answer']),
                    'actions':c['actions'],'memo':' '.join(c['actions'])})
            data[section]=items
        lines=[f'# Grade 11 Topic 6, Lesson {n}: {title}',
               f'Scope: [DBE Grade 11 Mathematics ATP, Term 2]({ATP}). Original Athena questions.',
               f'Paper: {"Paper 1" if n<=4 else "Paper 2"}. Status: teacher review and live browser acceptance required.']
        for item in worked:
            lines.extend([f'## {item["id"]}: {item["problem"]}',
                          f'Visual values: `{json.dumps(item["visual"],ensure_ascii=False)}`',
                          *[f'{j}. {step}' for j,step in enumerate(item['actions'],1)],
                          f'Answer: {item["answer"]}. Check: {item["check"]}'])
        for section in ['practice','mastery','reassessment']:
            lines.append(f'## {section.title()} answer key')
            for item in data[section]:
                lines.append(f'- {item["id"]}: {item["prompt"]} Options: {" | ".join(item["options"])}. '
                             f'Correct: {item["options"][item["answer_index"]]}. {item["memo"]}')
        source=DOC/data['source'];source.write_text('\n\n'.join(lines)+'\n',encoding='utf-8')
        (OUT/f'functions_{n:02}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        manifest.append({'lesson_id':f'g11-fn-{n:02}','paper':'Paper 1' if n<=4 else 'Paper 2',
                         'source':source.name,'source_sha256':sha256(source.read_bytes()).hexdigest(),
                         'worked':15,'practice':15,'mastery':5,'reassessment':3,
                         'status':'teacher_review_required','teacher_approved':False,'browser_accepted':False})
    (DOC/'topic6-acceptance-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':build()
