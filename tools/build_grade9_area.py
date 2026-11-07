"""Original Grade 9 area and perimeter bank, checked from dimensions."""
import json
import math
from hashlib import sha256
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/curriculum/grade9/area-and-perimeter'
OUT=ROOT/'backend/app/curriculum/grade9/generated'
ATP='https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2026%20ATPs/2026_ATP_Mathematics_Grade%209.pdf'
TITLES={1:'Polygons and SI units',2:'Composite polygon decomposition',3:'Circles and circumference',4:'Changing dimensions and scale',5:'Applied mixed cases and reassessment'}
def case(n,i,variant=0):
    seed=i+(17 if variant==3 else 15 if variant else 0)
    L=8+seed%41;W=4+(seed*3)%11
    v={'lesson':n,'length':L,'width':W}
    if n==1:
        mm=10*L;area=L*W;perimeter=2*(L+W)
        v.update(model='rectangle_units',length_mm=mm,area=area,perimeter=perimeter)
        problem=f'A rectangular tile is {mm} mm long and {W} cm wide. Find its perimeter in cm and area in cm².'
        actions=[f'Label the length {mm} mm and width {W} cm on the rectangle.',f'Convert {mm} mm ÷ 10 = {L} cm, so the two dimensions now share cm units.',f'Perimeter = 2({L} + {W}) = {perimeter} cm.',f'Area = {L} × {W} = {area} cm².',f'Check: opposite sides sum to {perimeter} cm; {L} columns of {W} square centimetres give {area} cm².']
        answer=f'P = {perimeter} cm; A = {area} cm²';wrong=[f'P = {perimeter+d} cm; A = {area} cm²' for d in (2,4,-2)]
    elif n==2:
        cut_w=2+seed%5;cut_h=1+seed%2
        assert cut_w<L and cut_h<W
        area=L*W-cut_w*cut_h;perimeter=2*(L+W)
        v.update(model='l_shape',cut_width=cut_w,cut_height=cut_h,area=area,perimeter=perimeter)
        problem=f'An L-shaped card is a {L} cm by {W} cm rectangle with a {cut_w} cm by {cut_h} cm corner removed. Find its area and outside perimeter.'
        actions=[f'Draw the outer {L} cm × {W} cm rectangle and mark the removed {cut_w} cm × {cut_h} cm corner.',f'Outer area = {L} × {W} = {L*W} cm²; removed area = {cut_w} × {cut_h} = {cut_w*cut_h} cm².',f'Subtract only the removed region: A = {L*W} − {cut_w*cut_h} = {area} cm².',f'Trace the six outside boundary segments; the two added notch edges replace the two lost corner edges, so P = 2({L} + {W}) = {perimeter} cm.',f'Check: ({L} − {cut_w}) + {cut_w} + ({W} − {cut_h}) + {cut_h} + {L} + {W} = {perimeter} cm.']
        answer=f'A = {area} cm²; P = {perimeter} cm';wrong=[f'A = {area+d} cm²; P = {perimeter} cm' for d in (cut_w*cut_h,2*cut_w*cut_h,-cut_w*cut_h)]
    elif n==3:
        r=3+seed%41;diameter=2*r
        v.update(model='circle',radius=r,diameter=diameter,circumference_coefficient=diameter,area_coefficient=r*r)
        problem=f'A circular sign has radius {r} cm. Give its diameter, circumference and area exactly in terms of π; also round C and A to two decimal places.'
        actions=[f'Mark the centre and radius r = {r} cm.',f'Diameter d = 2r = {diameter} cm.',f'Circumference C = 2πr = {diameter}π cm ≈ {math.pi*diameter:.2f} cm.',f'Area A = πr² = {r*r}π cm² ≈ {math.pi*r*r:.2f} cm².',f'Check: C = πd = {diameter}π cm and A = π({r})² = {r*r}π cm²; length uses cm, area uses cm².']
        answer=f'd = {diameter} cm; C = {diameter}π cm ≈ {math.pi*diameter:.2f} cm; A = {r*r}π cm² ≈ {math.pi*r*r:.2f} cm²'
        wrong=[f'd = {diameter} cm; C = {diameter+2*j}π cm ≈ {math.pi*(diameter+2*j):.2f} cm; A = {r*r}π cm² ≈ {math.pi*r*r:.2f} cm²' for j in (1,2,-1)]
    elif n==4:
        factor=2;mode=('both','length_only','width_only')[seed%3]
        new_l=L*(factor if mode in ('both','length_only') else 1);new_w=W*(factor if mode in ('both','width_only') else 1)
        old_p=2*(L+W);old_a=L*W;new_p=2*(new_l+new_w);new_a=new_l*new_w
        v.update(model='scaled_rectangle',mode=mode,factor=factor,scaled_length=new_l,scaled_width=new_w,old_perimeter=old_p,old_area=old_a,new_perimeter=new_p,new_area=new_a)
        phrase={'both':'both dimensions','length_only':'only the length','width_only':'only the width'}[mode]
        problem=f'A {L} cm by {W} cm rectangle is changed by doubling {phrase}. Find the new perimeter and area.'
        actions=[f'Mark the original dimensions {L} cm and {W} cm; double {phrase}.',f'The new dimensions are {new_l} cm and {new_w} cm.',f'Original perimeter = 2({L} + {W}) = {old_p} cm; new perimeter = 2({new_l} + {new_w}) = {new_p} cm.',f'Original area = {L} × {W} = {old_a} cm²; new area = {new_l} × {new_w} = {new_a} cm².',f'Check: area changes by {new_a//old_a} times; the boundary changes from {old_p} cm to {new_p} cm.']
        answer=f'P = {new_p} cm; A = {new_a} cm²';wrong=[f'P = {new_p+d} cm; A = {new_a} cm²' for d in (2,4,-2)]
    else:
        path=1+seed%4;outer_l=L+2*path;outer_w=W+2*path;path_area=outer_l*outer_w-L*W;fence=2*(outer_l+outer_w)
        v.update(model='garden_path',path=path,outer_length=outer_l,outer_width=outer_w,path_area=path_area,fence=fence)
        problem=f'A {L} m by {W} m garden has a uniform {path} m path outside all four sides. Find the path area and outer fence length.'
        actions=[f'Mark the inner {L} m × {W} m garden and a path width of {path} m on each side.',f'Outer dimensions are {L} + 2({path}) = {outer_l} m and {W} + 2({path}) = {outer_w} m.',f'Outer area = {outer_l} × {outer_w} = {outer_l*outer_w} m²; inner area = {L} × {W} = {L*W} m².',f'Path area = {outer_l*outer_w} − {L*W} = {path_area} m²; outer fence length = 2({outer_l} + {outer_w}) = {fence} m.',f'Check: the path area plus the garden area equals {outer_l*outer_w} m²; the outer four sides total {fence} m.']
        answer=f'path = {path_area} m²; fence = {fence} m';wrong=[f'path = {path_area+d} m²; fence = {fence} m' for d in (2*path,4*path,-2*path)]
    assert len(set([answer,*wrong]))==4,(n,i)
    return {'id':f'g9-area-l{n:02}-w{i:02}' if not variant else f'g9-area-l{n:02}-v{variant}-w{i:02}', 'problem':problem,'actions':actions,'answer':answer,'check':actions[-1], 'wrong':wrong,'misconception':'Keep the given lengths and units attached to the correct edges; perimeter counts boundary length, area counts square units.', 'visual':{'family':'area','values':v},'lesson':n}
def choice(n,i,variant,prefix):
    c=case(n,i,variant);opts=[c['answer'],*c['wrong']];pos=i%4;opts=opts[4-pos:]+opts[:4-pos] if pos else opts
    return {'id':f'g9-area-l{n:02}-{prefix}{i:02}','prompt':c['problem'],'options':opts,'answer_index':pos,'memo':' '.join(c['actions']),'source':f'lesson-{n:02}.md'}
def build():
    DOC.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True);manifest=[]
    for n,title in TITLES.items():
        worked=[{k:v for k,v in case(n,i).items() if k!='wrong'}|{'difficulty':'foundation' if i<=2 else 'easy' if i<=5 else 'standard' if i<=9 else 'intermediate' if i<=12 else 'exam'} for i in range(1,16)]
        data={'source':f'lesson-{n:02}.md','worked':worked,'practice':[choice(n,i,1,'p') for i in range(1,16)],'mastery':[choice(n,i+15,2,'m') for i in range(1,6)],'reassessment':[choice(n,i+18,3,'r') for i in range(1,4)]}
        assert len({c['problem'] for c in worked})==15
        lines=[f'# Grade 9 Topic 11 · Lesson {n}: {title}',f'Authority: [DBE 2026 Grade 9 Mathematics ATP]({ATP}), Term 3. Original Athena questions.','Status: teacher and browser review required. Preserve original dimensions; reveal conversion, construction, formula, calculation and check in order.']
        for c in worked:lines.extend([f'## {c["id"]}: {c["problem"]}',f'Visual: {json.dumps(c["visual"],ensure_ascii=False)}',*[f'{j}. {step}' for j,step in enumerate(c['actions'],1)],f'**Answer:** {c["answer"]}. **Misconception:** {c["misconception"]}'])
        for label,key in [('Practice','practice'),('Mastery','mastery'),('Changed-value reassessment','reassessment')]:
            lines.append(f'## {label} answer key')
            for c in data[key]:lines.append(f'- {c["id"]}: {c["prompt"]} Options: {" | ".join(c["options"])}. Correct: {c["options"][c["answer_index"]]}. {c["memo"]}')
        source=DOC/data['source'];source.write_text('\n\n'.join(lines)+'\n',encoding='utf-8')
        (OUT/f'area_{n:02}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        manifest.append({'lesson_id':f'g9-area-{n:02}','source':source.name,'source_sha256':sha256(source.read_bytes()).hexdigest(),'worked':15,'practice':15,'mastery':5,'reassessment':3,'status':'teacher_review_required','teacher_approved':False,'browser_accepted':False})
    (DOC/'topic11-acceptance-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    (DOC/'topic11-batch-acceptance.md').write_text(f'# Grade 9 Topic 11: Area and Perimeter\n\n[DBE 2026 Grade 9 Mathematics ATP, Term 3]({ATP}) requires SI conversions, perimeter and area of polygons and circles, and investigation of doubling dimensions. This five-lesson breakdown is Athena’s.\n\n75 worked examples, 75 four-choice practice items, 25 mastery items and 15 changed-value reassessments. Teacher mathematical review and real desktop/mobile browser acceptance remain required.\n',encoding='utf-8')
if __name__=='__main__':build()
