"""Author original Grade 11 triangle-rule proofs, applications and MCQ banks."""
from __future__ import annotations

import json
import math
from hashlib import sha256
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/curriculum/grade11/triangle-rules'
OUT=ROOT/'backend/app/curriculum/grade11/generated'
ATP='https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2023%20ATPs/FET%20Content%20Subjects/Grade%2011/1.590%20ATP%202023-24%20Gr%2011%20Maths%20final.pdf'
TITLES={1:'Derive and apply the sine rule',
        2:'Solve ambiguous sine-rule cases',
        3:'Derive and apply the cosine rule',
        4:'Find angles with the cosine rule',
        5:'Derive and apply the area rule'}
DIFF=['foundation']*2+['easy']*3+['standard']*4+['intermediate']*3+['exam']*3
def fmt(x):return f'{x:.2f}'
def sin(x):return math.sin(math.radians(x))
def cos(x):return math.cos(math.radians(x))

def case(n,i,variant=0):
    t=i+15*variant
    proof=variant==0 and i==1 and n in (1,3,5)
    if proof:
        if n==1:
            problem='In ΔABC, draw altitude CD to AB. Derive a/sin A = b/sin B using a = BC and b = AC.'
            answer='a/sin A = b/sin B'
            actions=['Draw CD perpendicular to AB; label CD = h, BC = a and AC = b.',
                     'In right triangle ACD, sin A = h/b, so h = b sin A.',
                     'In right triangle BCD, sin B = h/a, so h = a sin B.',
                     'Equate the two heights: b sin A = a sin B; divide by sin A sin B.',
                     'Answer: a/sin A = b/sin B. Check both ratios equal ab/h for nondegenerate triangles.']
            wrong=['a/sin B = b/sin A','a sin A = b sin B','a/b = sin A sin B']
            v={'mode':'proof_sine'}
        elif n==3:
            problem='In ΔABC, place A at the origin and AB = c on the horizontal axis. Derive a² = b² + c² − 2bc cos A.'
            answer='a² = b² + c² − 2bc cos A'
            actions=['Draw AC = b making angle A with AB = c; lower perpendicular CD to AB.',
                     'The horizontal projection AD = b cos A, so DB = c − b cos A.',
                     'The vertical height CD = b sin A. Use Pythagoras: a² = (c − b cos A)² + (b sin A)².',
                     'Expand and combine b²(cos² A + sin² A) = b².',
                     'Answer: a² = b² + c² − 2bc cos A. Check A = 90° reduces to Pythagoras.']
            wrong=['a² = b² + c² + 2bc cos A','a = b² + c² − 2bc cos A','a² = b² + c² − bc cos A']
            v={'mode':'proof_cosine'}
        else:
            problem='In ΔABC, AB = c and AC = b enclose angle A. Draw altitude CD and derive the area rule.'
            answer='Area = ½bc sin A'
            actions=['Draw altitude CD = h perpendicular to base AB = c.',
                     'The triangle has area = ½ × base × height = ½ch.',
                     'In right triangle ACD, sin A = h/b, hence h = b sin A.',
                     'Substitute the height: area = ½c(b sin A).',
                     'Answer: Area = ½bc sin A. Check that A = 90° gives ½bc.']
            wrong=['Area = bc sin A','Area = ½bc cos A','Area = ½(b+c) sin A']
            v={'mode':'proof_area'}
    elif n==1:
        A=[30,40,45,50,60][(t-1)%5];B=[35,45,55,65,70][(t*2)%5]
        a=6+(t%11);b=a*sin(B)/sin(A)
        problem=f'In ΔABC, A = {A}°, B = {B}° and a = {a} cm. Find b to two decimal places.'
        answer=f'b = {fmt(b)} cm'
        actions=[f'Label a = BC = {a} cm opposite A = {A}°, and b = AC opposite B = {B}°.',
                 f'Draw an altitude to see the sine rule a/sin A = b/sin B.',
                 f'Substitute: {a}/sin({A}°) = b/sin({B}°).',
                 f'Rearrange: b = {a} sin({B}°)/sin({A}°) = {fmt(b)} cm.',
                 f'Answer: {answer}. Check: b sin({A}°) and {a} sin({B}°) agree before rounding.']
        wrong=[f'b = {fmt(a*sin(A)/sin(B))} cm',f'b = {fmt(a*sin(B))} cm',f'b = {fmt(b+1)} cm']
        v={'mode':'sine_side','A':A,'B':B,'a':a,'b':b}
    elif n==2:
        A=[25,30,35,40][(t-1)%4];a=7+(t%13)
        ratio=[0.68,0.73,0.78,0.83,0.88][(t-1)%5]
        b=round(a*ratio/sin(A))
        ratio_actual=b*sin(A)/a
        assert sin(A)<ratio_actual<1,(A,a,b)
        B1=math.degrees(math.asin(ratio_actual));B2=180-B1
        assert A+B2<180
        problem=f'In ΔABC, A = {A}°, a = {a} cm and b = {b} cm. Find both possible B angles (two decimals).'
        answer=f'B = {fmt(B1)}° or {fmt(B2)}°'
        actions=[f'Label the known opposite pair A = {A}°, a = {a} cm and second side b = {b} cm.',
                 f'By the sine rule, sin B = b sin A/a = {b} sin({A}°)/{a} = {ratio_actual:.4f}.',
                 f'The acute branch is B₁ = arcsin({ratio_actual:.4f}) = {fmt(B1)}°.',
                 f'The supplementary branch is B₂ = 180° − {fmt(B1)}° = {fmt(B2)}°; both satisfy A + B < 180°.',
                 f'Answer: {answer}. Check both sine values match {ratio_actual:.4f} before rounding.']
        wrong=[f'B = {fmt(B1)}° only',f'B = {fmt(B2)}° only',f'B = {fmt(B1)}° or {fmt(180-A)}°']
        v={'mode':'ambiguous','A':A,'a':a,'b':b,'B1':B1,'B2':B2}
    elif n==3:
        b=5+(t%10);c=7+(t*2)%11;A=[45,60,75,100,120][(t-1)%5]
        a=math.sqrt(b*b+c*c-2*b*c*cos(A))
        problem=f'In ΔABC, b = {b} cm and c = {c} cm enclose angle A = {A}°. Find a to two decimals.'
        answer=f'a = {fmt(a)} cm'
        actions=[f'Label sides b = AC = {b} cm and c = AB = {c} cm with included angle A = {A}°.',
                 f'Drop a perpendicular from C to AB to see why the cosine rule uses the included angle.',
                 f'Write a² = b² + c² − 2bc cos A = {b*b} + {c*c} − {2*b*c} cos({A}°).',
                 f'Take the positive root: a = √({b*b+c*c} − {2*b*c} cos({A}°)) = {fmt(a)} cm.',
                 f'Answer: {answer}. Check the unrounded length is between |{b} − {c}| and {b+c}.']
        wrong=[f'a = {fmt(math.sqrt(b*b+c*c))} cm',f'a = {fmt(math.sqrt(b*b+c*c+2*b*c*cos(A)))} cm',f'a = {fmt(a+1)} cm']
        v={'mode':'cosine_side','A':A,'a':a,'b':b,'c':c}
    elif n==4:
        b=5+(t%10);c=6+(t*2)%11
        # Vary a within triangle inequality; avoid degenerate endpoints.
        lower=abs(b-c)+1;upper=b+c-1;a=lower+(t*7)%(upper-lower+1)
        value=(b*b+c*c-a*a)/(2*b*c);A=math.degrees(math.acos(value))
        problem=f'In ΔABC, a = {a} cm, b = {b} cm and c = {c} cm. Find angle A to two decimals.'
        answer=f'A = {fmt(A)}°'
        actions=[f'Plot the three sides, keeping a = {a} cm opposite unknown A.',
                 f'Write a² = b² + c² − 2bc cos A.',
                 f'Rearrange cos A = (b² + c² − a²)/(2bc) = ({b*b} + {c*c} − {a*a})/{2*b*c} = {value:.4f}.',
                 f'Use inverse cosine on the full-precision fraction: A = {fmt(A)}°.',
                 f'Answer: {answer}. Check substituting A into the cosine rule reproduces side a = {a} cm.']
        wrong=[f'A = {fmt(180-A)}°',f'A = {fmt(math.degrees(math.asin(value)) if -1<=value<=1 else 0)}°',f'A = {fmt(A+5)}°']
        v={'mode':'cosine_angle','A':A,'a':a,'b':b,'c':c}
    else:
        b=6+(t%12);c=7+(t*2)%13;A=[30,45,60,90,120][(t-1)%5]
        area=b*c*sin(A)/2
        problem=f'A triangular field has sides b = {b} m and c = {c} m enclosing angle A = {A}°. Find its area to two decimals.'
        answer=f'Area = {fmt(area)} m²'
        actions=[f'Draw triangle ABC and mark sides b = {b} m, c = {c} m and their included A = {A}°.',
                 f'Drop an altitude to base c; height h = b sin A = {b} sin({A}°).',
                 f'Use area = ½ × base × height = ½bc sin A.',
                 f'Substitute: area = ½({b})({c}) sin({A}°) = {fmt(area)} m².',
                 f'Answer: {answer}. Check the area is positive and no more than ½({b})({c}) m².']
        wrong=[f'Area = {fmt(b*c*sin(A))} m²',f'Area = {fmt(b*c*cos(A)/2)} m²',f'Area = {fmt(area+1)} m²']
        v={'mode':'area','A':A,'b':b,'c':c,'area':area}
    wrong=list(dict.fromkeys(x for x in wrong if x!=answer))
    offset=1
    while len(wrong)<3:
        if n==1:extra=f'b = {fmt(v.get("b",0)+offset)} cm' if not proof else f'a/sin A = b/sin B + {offset}'
        elif n==2:extra=f'B = {fmt(B1+offset)}° or {fmt(B2)}°'
        elif n==3:extra=f'a = {fmt(v.get("a",0)+offset)} cm' if not proof else f'a² = b² + c² − {offset}bc cos A'
        elif n==4:extra=f'A = {fmt(A+offset)}°'
        else:extra=f'Area = {fmt(v.get("area",0)+offset)} m²' if not proof else f'Area = {offset}bc sin A'
        if extra not in wrong and extra!=answer:wrong.append(extra)
        offset+=1
    assert len(actions)==5 and len({answer,*wrong[:3]})==4
    return {'id':f'g11-rules-l{n:02}-w{i:02}','lesson':n,'problem':problem,
            'answer':answer,'actions':actions,'check':actions[-1],
            'visual':{'family':'grade11_triangle_rules','values':v},'wrong':wrong[:3],
            'difficulty':DIFF[i-1]}

def build():
    DOC.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True);manifest=[]
    for n,title in TITLES.items():
        worked=[{k:v for k,v in case(n,i).items() if k!='wrong'} for i in range(1,16)]
        assert len({q['problem'] for q in worked})==15
        data={'source':f'grade11-rules-lesson-{n:02}.md','worked':worked}
        for section,amount,variant,prefix in [('practice',15,1,'p'),('mastery',5,2,'m'),('reassessment',3,3,'r')]:
            items=[]
            for i in range(1,amount+1):
                c=case(n,i,variant);options=[c['answer'],*c['wrong']];shift=(i+variant)%4
                options=options[shift:]+options[:shift]
                items.append({'id':f'g11-rules-l{n:02}-{prefix}{i:02}','prompt':c['problem'],
                    'options':options,'answer_index':options.index(c['answer']),
                    'actions':c['actions'],'memo':' '.join(c['actions'])})
            data[section]=items
        lines=[f'# Grade 11 Topic 7, Lesson {n}: {title}',
               f'Scope: [DBE Grade 11 Mathematics ATP, Term 3]({ATP}). Original Athena questions.',
               'Status: teacher review and live browser acceptance required. Do not round until the final answer.']
        for q in worked:
            lines.extend([f'## {q["id"]}: {q["problem"]}',
                f'Visual values: `{json.dumps(q["visual"],ensure_ascii=False)}`',
                *[f'{j}. {step}' for j,step in enumerate(q['actions'],1)],
                f'Answer: {q["answer"]}. Check: {q["check"]}'])
        for section in ['practice','mastery','reassessment']:
            lines.append(f'## {section.title()} answer key')
            for q in data[section]:
                lines.append(f'- {q["id"]}: {q["prompt"]} Options: {" | ".join(q["options"])}. Correct: '
                             f'{q["options"][q["answer_index"]]}. {q["memo"]}')
        source=DOC/data['source'];source.write_text('\n\n'.join(lines)+'\n',encoding='utf-8')
        (OUT/f'triangle_rules_{n:02}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        manifest.append({'lesson_id':f'g11-rules-{n:02}','source':source.name,
                         'source_sha256':sha256(source.read_bytes()).hexdigest(),
                         'worked':15,'practice':15,'mastery':5,'reassessment':3,
                         'status':'teacher_review_required','teacher_approved':False,'browser_accepted':False})
    (DOC/'topic7-acceptance-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':build()
