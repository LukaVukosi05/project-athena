"""Original, checked Grade 9 geometry of 2D shapes question bank."""
import json
from hashlib import sha256
from pathlib import Path
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/curriculum/grade9/geometry-of-2d-shapes'
OUT=ROOT/'backend/app/curriculum/grade9/generated'
ATP='https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2026%20ATPs/2026_ATP_Mathematics_Grade%209.pdf'
TITLES={1:'Triangle classes and angle sum',2:'Exterior angle of a triangle',3:'Quadrilateral properties',4:'Diagonals and polygon interior angles',5:'Congruent triangle conditions',6:'Similar triangles and scale',7:'Unknown sides and angles with reasons',8:'Integrated proof and first-error reassessment'}

def case(n,i,variant=0):
    seed=i+(17 if variant==3 else 15 if variant else 0)
    a=20+seed%14*4
    v={'kind':('triangle' if n in (1,2,7) else 'quadrilateral' if n==3 else 'polygon' if n==4 else 'pair'), 'lesson':n}
    if n==1:
        model=('isosceles','equilateral','right')[seed%3]
        if model=='isosceles':
            apex=30+seed%61*2;target=(180-apex)//2
            v.update(model=model,apex=apex,target=target)
            problem=f'Isosceles triangle ABC has AB = AC and apex angle A = {apex}°. Find base angle B, with a reason.'
            acts=[f'Mark equal sides AB and AC, and read ∠A = {apex}°.', 'Equal sides face equal base angles, so ∠B = ∠C = x.',f'Use the triangle angle sum: {apex}° + x + x = 180°.',f'Subtract {apex}°: 2x = {180-apex}°; divide by 2: x = {target}°.',f'Check: {apex}° + {target}° + {target}° = 180°.']
            result=f'∠B = {target}°'
        elif model=='equilateral':
            side=3+seed%41;target=60
            v.update(model=model,side=side,target=target)
            problem=f'Equilateral triangle ABC has AB = BC = CA = {side} cm. Find angle B and give a reason.'
            acts=[f'Mark all three equal sides, each {side} cm.','All three angles opposite these sides are equal: ∠A = ∠B = ∠C = x.', 'Triangle angle sum: x + x + x = 180°.', 'Divide 180° by 3: x = 60°.', 'Check: 60° + 60° + 60° = 180°.']
            result='∠B = 60°'
        else:
            given=22+2*(seed%23);side=3+seed%41;target=90-given
            v.update(model=model,given=given,side=side,target=target)
            problem=f'Right triangle ABC has ∠B = 90°, ∠A = {given}° and BC = {side} cm. Find ∠C.'
            acts=[f'Mark the right angle at B and ∠A = {given}°.', 'The three interior angles of a triangle total 180°.',f'Write {given}° + 90° + ∠C = 180°.',f'Calculate ∠C = 180° − 90° − {given}° = {target}°.',f'Check: {given}° + 90° + {target}° = 180°.']
            result=f'∠C = {target}°'
        wrong=[result.replace(f'{target}°',f'{target+d}°') for d in (4,8,-4)]
    elif n==2:
        left=20+seed%41*2; right=25+seed%17*2; target=left+right
        v.update(left=left,right=right,target=target,model='exterior')
        problem=f'In triangle ABC, ∠A = {left}° and ∠B = {right}°. Extend BC past C to D. Find exterior ∠ACD.'
        acts=[f'Locate remote interior angles ∠A = {left}° and ∠B = {right}°.',f'The interior angle at C is 180° − {left}° − {right}° = {180-target}°.', '∠ACB and ∠ACD form a straight line.',f'Calculate ∠ACD = 180° − {180-target}° = {target}°.',f'Check: the exterior angle also equals {left}° + {right}° = {target}°.']
        result=f'∠ACD = {target}°';wrong=[f'∠ACD = {target+d}°' for d in (4,8,-4)]
    elif n==3:
        model=('parallelogram','rectangle','rhombus','trapezium','square','kite')[seed%6]
        given=40+seed%41*3 if model in ('parallelogram','rhombus','trapezium') else 3+seed%41
        target=180-given if model in ('parallelogram','rhombus','trapezium') else given
        v.update(model=model,given=given,target=target)
        if model in ('parallelogram','rhombus'):
            problem=f'ABCD is a {model}. ∠A = {given}°. Find adjacent ∠B, naming the property.'
            reason='adjacent angles in a parallelogram are supplementary' if model=='parallelogram' else 'a rhombus is a parallelogram, so adjacent angles are supplementary'
            acts=[f'Locate ∠A = {given}° and adjacent ∠B.',f'Use the property: {reason}.',f'Write {given}° + ∠B = 180°.',f'Calculate ∠B = 180° − {given}° = {target}°.',f'Check: {given}° + {target}° = 180°.']
            result=f'∠B = {target}°'
        elif model=='trapezium':
            problem=f'Trapezium ABCD has AB ∥ CD. ∠A = {given}°. Find ∠D on the same transversal AD.'
            acts=[f'Mark the one parallel pair AB ∥ CD and the transversal AD; ∠A = {given}°.', '∠A and ∠D are co-interior angles.',f'Co-interior angles sum to 180°: {given}° + ∠D = 180°.',f'Calculate ∠D = {target}°.',f'Check: {given}° + {target}° = 180°.']
            result=f'∠D = {target}°'
        else:
            prompt={'rectangle':f'Rectangle ABCD has side AB = {given} cm. Find opposite side CD.', 'square':f'Square ABCD has side AB = {given} cm. Find side BC.', 'kite':f'Kite ABCD has its adjacent sides AB and AD marked equal. If AB = {given} cm, find AD.'}[model]
            problem=prompt
            reason={'rectangle':'Opposite sides of a rectangle are equal.', 'square':'All four sides of a square are equal.', 'kite':'The given adjacent pair AB and AD is equal by the kite markings.'}[model]
            side={'rectangle':'CD','square':'BC','kite':'AD'}[model]
            acts=[f'Locate the given side AB = {given} cm and the requested side {side}.',f'{reason}',f'Write {side} = AB.',f'Calculate {side} = {given} cm.',f'Check the marked corresponding or equal sides both measure {given} cm.']
            result=f'{side} = {target} cm'
        wrong=[result.replace(f'{target}',f'{target+d}') for d in (1,2,-1)]
    elif n==4:
        if seed%2:
            sides=4+seed%41;target=(sides-2)*180;each=str(Fraction(target,sides))
            v.update(model='regular_polygon',sides=sides,target=target,each=each)
            problem=f'A regular {sides}-sided polygon is drawn. Find its total interior angle sum and the size of each interior angle.'
            acts=[f'Count {sides} vertices; choose one vertex for diagonals.',f'Draw diagonals from that vertex, forming {sides-2} non-overlapping triangles.',f'Each triangle contributes 180°: total = ({sides} − 2) × 180° = {target}°.',f'Regularity makes all {sides} interior angles equal: each = {target}° ÷ {sides} = {each}°.',f'Check: {sides} × {each}° = {target}°.']
            result=f'sum = {target}°; each = {each}°';wrong=[f'sum = {target+d}°; each = {each}°' for d in (180,-180,360)]
        else:
            shape=('rectangle','square','parallelogram','rhombus','kite')[seed%5];given=6+seed%41;target=given
            v.update(model='diagonals',shape=shape,given=given,target=target)
            if shape in ('rectangle','square'):
                problem=f'ABCD is a {shape}. Diagonal AC = {given} cm. Find diagonal BD and state the property.'
                reason=f'Diagonals of a {shape} are equal in length.';equation=f'BD = AC = {given} cm';result=f'BD = {target} cm'
            elif shape in ('parallelogram','rhombus'):
                problem=f'Diagonals AC and BD of a {shape} ABCD meet at E. If AE = {given} cm, find EC.'
                reason=f'Diagonals of a {shape} bisect each other.';equation=f'EC = AE = {given} cm';result=f'EC = {target} cm'
            else:
                problem=f'Kite ABCD has AB = AD and CB = CD. Its symmetry diagonal AC meets BD at E. If BE = {given} cm, find ED.'
                reason='The symmetry diagonal AC of this kite bisects BD.';equation=f'ED = BE = {given} cm';result=f'ED = {target} cm'
            acts=[f'Locate the two actual diagonals and the given segment of {given} cm.',f'State the property: {reason}',f'Pair the requested segment with the given: {equation}.',f'Calculate {result}.',f'Check that both segments stated equal by the {shape} property are {given} cm.']
            wrong=[result.replace(f'{target}',f'{target+d}') for d in (1,2,-1)]
    elif n==5:
        first=4+seed%41;second=5+(seed*3)%9;third=first+second-2
        criterion=('SAS','SSS','ASA')[seed%3]
        v.update(model='congruent',sides=[first,second,third],target=third,criterion=criterion)
        if criterion=='SAS':
            problem=f'Triangles ABC and DEF have AB = DE = {first} cm, AC = DF = {second} cm and BC = {third} cm. Their included angles ∠A and ∠D are marked equal. Find EF and justify correspondence.'
            acts=[f'Pair AB with DE ({first} cm) and AC with DF ({second} cm).', 'The included angles ∠A and ∠D are marked equal.', 'Two side pairs and their included angle establish SAS congruence: △ABC ≅ △DEF.',f'The order A↔D, B↔E, C↔F pairs BC with EF: EF = {third} cm.',f'Check: BC and EF are corresponding sides, both {third} cm.']
            result=f'EF = {third} cm';wrong=[f'EF = {third+d} cm' for d in (1,2,-1)]
        elif criterion=='SSS':
            problem=f'AB = DE = {first} cm, AC = DF = {second} cm, and BC = EF = {third} cm. Which condition proves △ABC ≅ △DEF?'
            acts=[f'Mark AB = DE = {first} cm.',f'Mark AC = DF = {second} cm and BC = EF = {third} cm.', 'All three corresponding side pairs are equal.', 'Therefore △ABC ≅ △DEF by SSS.', 'Check the vertex order A↔D, B↔E, C↔F and all three side pairs.']
            result='△ABC ≅ △DEF (SSS)';wrong=['△ABC ≅ △DEF (SAS)','△ABC ≅ △DEF (ASA)','insufficient evidence']
        else:
            problem=f'∠A = ∠D and ∠B = ∠E are marked equal. AB = DE = {first} cm lies between them. Which condition proves △ABC ≅ △DEF?'
            acts=['Mark ∠A = ∠D.', 'Mark ∠B = ∠E.',f'The included corresponding sides AB and DE both measure {first} cm.', 'Therefore △ABC ≅ △DEF by ASA.', 'Check that the equal side lies between the two marked angles in each triangle.']
            result='△ABC ≅ △DEF (ASA)';wrong=['△ABC ≅ △DEF (SAS)','△ABC ≅ △DEF (SSS)','insufficient evidence']
    elif n==6:
        small=3+seed%41;scale=2+seed%3;target=(small+2)*scale
        criterion=('given','AA','SAS','SSS')[seed%4]
        v.update(model='similar',small=small,scale=scale,target=target,criterion=criterion)
        if criterion=='given':
            problem=f'△ABC ∼ △DEF in the stated order. AB = {small} cm, DE = {small*scale} cm and BC = {small+2} cm. Find EF.'
            acts=[f'Pair AB with DE and BC with EF in △ABC ∼ △DEF.',f'The scale factor from ABC to DEF is DE ÷ AB = {small*scale} ÷ {small} = {scale}.',f'Write EF ÷ BC = {scale}, so EF = {scale} × {small+2}.',f'Calculate EF = {target} cm.',f'Check: EF ÷ BC = {target} ÷ {small+2} = {scale}.']
            result=f'EF = {target} cm';wrong=[f'EF = {target+d} cm' for d in (scale,2*scale,-scale)]
        elif criterion=='AA':
            problem=f'∠A = ∠D and ∠B = ∠E are marked equal. AB = {small} cm, DE = {small*scale} cm and BC = {small+2} cm. Show the similarity condition and find EF.'
            acts=['Locate the two corresponding equal angle pairs A↔D and B↔E.', 'Two equal angle pairs establish △ABC ∼ △DEF by AA.',f'Pair AB with DE: scale factor = {small*scale} ÷ {small} = {scale}.',f'EF corresponds to BC, so EF = {scale} × {small+2} = {target} cm.',f'Check: EF ÷ BC = {target} ÷ {small+2} = {scale}, and the two angle pairs match.']
            result=f'EF = {target} cm';wrong=[f'EF = {target+d} cm' for d in (scale,2*scale,-scale)]
        elif criterion=='SAS':
            problem=f'AB = {small} cm, AC = {small+1} cm, DE = {small*scale} cm and DF = {(small+1)*scale} cm. Included angles ∠A and ∠D are marked equal. If BC = {small+2} cm, find EF.'
            acts=[f'AB:DE = {small}:{small*scale} and AC:DF = {small+1}:{(small+1)*scale}; the two ratios match.', 'The included angles ∠A = ∠D are marked equal.', 'Proportional adjacent sides and their included angle establish SAS similarity.',f'Scale factor = {scale}; EF corresponds to BC, so EF = {scale} × {small+2} = {target} cm.',f'Check: AB:DE = AC:DF = BC:EF = 1:{scale}.']
            result=f'EF = {target} cm';wrong=[f'EF = {target+d} cm' for d in (scale,2*scale,-scale)]
        else:
            problem=f'AB = {small}, AC = {small+1}, BC = {small+2} cm; DE = {small*scale}, DF = {(small+1)*scale}, EF = {target} cm. Give the condition proving △ABC ∼ △DEF.'
            acts=[f'Pair AB:DE = {small}:{small*scale} = 1:{scale}.',f'Pair AC:DF = {small+1}:{(small+1)*scale} = 1:{scale}.',f'Pair BC:EF = {small+2}:{target} = 1:{scale}.','All three corresponding side pairs are in the same ratio; △ABC ∼ △DEF by SSS similarity.',f'Check: every large side is {scale} times its corresponding small side.']
            result='△ABC ∼ △DEF (SSS similarity)';wrong=['△ABC ≅ △DEF (SSS congruence)','△ABC ∼ △DEF (AA)','insufficient evidence']
    elif n==7:
        given=30+seed%61*2;target=(180-given)//2
        v.update(model='isosceles',apex=given,target=target)
        problem=f'AB = AC in triangle ABC. ∠A = {given}° and ∠B = x. Find x, giving each geometric reason.'
        acts=[f'Observe AB = AC and the given apex angle ∠A = {given}°.', 'Equal sides imply ∠B = ∠C = x, since base angles of an isosceles triangle are equal.',f'Triangle angle sum gives {given}° + x + x = 180°.',f'2x = {180-given}°, hence x = {target}°.',f'Check: {given}° + 2({target}°) = 180°.']
        result=f'x = {target}°';wrong=[f'x = {target+d}°' for d in (3,6,-3)]
    else:
        given=30+seed%61*2;target=(180-given)//2;claimed=180-given
        v.update(model='diagnosis',apex=given,target=target,claimed=claimed)
        problem=f'In isosceles △ABC, AB = AC and ∠A = {given}°. A learner writes ∠B = 180° − {given}° = {claimed}°. Identify the first error and find ∠B.'
        acts=[f'Keep AB = AC and the apex angle {given}° visible.',f'The learner assigned all {claimed}° remaining to one base angle.', 'This is the first error: equal sides require two equal base angles, not one.',f'Split the remaining angle equally: ∠B = ∠C = ({180-given}°) ÷ 2 = {target}°.',f'Check: {given}° + {target}° + {target}° = 180°.']
        result=f'∠B = {target}°';wrong=[f'∠B = {claimed}°',f'∠B = {target+3}°',f'∠B = {target-3}°']
    assert len(set([result,*wrong]))==4
    return {'id':f'g9-shapes-l{n:02}-w{i:02}' if not variant else f'g9-shapes-l{n:02}-v{variant}-w{i:02}', 'problem':problem,'actions':acts,'answer':result,'check':acts[-1],'wrong':wrong,'misconception':'A diagram alone does not prove a property; mark the given equality and state the applicable reason.', 'visual':{'family':'shapes','values':v},'lesson':n}

def choice(n,i,variant,prefix):
    c=case(n,i,variant);right=c['answer'];opts=[right,*c['wrong']];position=i%4
    opts=opts[4-position:]+opts[:4-position] if position else opts
    return {'id':f'g9-shapes-l{n:02}-{prefix}{i:02}','prompt':c['problem'],'options':opts,'answer_index':position,'memo':' '.join(c['actions']),'source':f'lesson-{n:02}.md'}

def build():
    DOC.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True);manifest=[]
    for n,title in TITLES.items():
        worked=[{k:v for k,v in case(n,i).items() if k!='wrong'}|{'difficulty':'foundation' if i<=2 else 'easy' if i<=5 else 'standard' if i<=9 else 'intermediate' if i<=12 else 'exam'} for i in range(1,16)]
        data={'source':f'lesson-{n:02}.md','worked':worked,'practice':[choice(n,i,1,'p') for i in range(1,16)],'mastery':[choice(n,i+15,2,'m') for i in range(1,6)],'reassessment':[choice(n,i+18,3,'r') for i in range(1,4)]}
        assert len({c['problem'] for c in worked})==15,(n,'duplicate')
        lines=[f'# Grade 9 Topic 10 · Lesson {n}: {title}',f'Authority: [DBE 2026 Grade 9 Mathematics ATP]({ATP}), geometry of 2D shapes. Original Athena questions.','Status: teacher and browser review required. Reveal the marked givens, relevant theorem, calculation and check in order; retain previous written work.']
        for c in worked:lines.extend([f'## {c["id"]}: {c["problem"]}',f'Visual: {json.dumps(c["visual"],ensure_ascii=False)}',*[f'{j}. {step}' for j,step in enumerate(c['actions'],1)],f'**Answer:** {c["answer"]}. **Misconception:** {c["misconception"]}'])
        for label,key in [('Practice','practice'),('Mastery','mastery'),('Changed-value reassessment','reassessment')]:
            lines.append(f'## {label} answer key')
            for c in data[key]:lines.append(f'- {c["id"]}: {c["prompt"]} Options: {" | ".join(c["options"])}. Correct: {c["options"][c["answer_index"]]}. {c["memo"]}')
        source=DOC/data['source'];source.write_text('\n\n'.join(lines)+'\n',encoding='utf-8')
        (OUT/f'shapes_{n:02}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        manifest.append({'lesson_id':f'g9-shapes-{n:02}','source':source.name,'source_sha256':sha256(source.read_bytes()).hexdigest(),'worked':15,'practice':15,'mastery':5,'reassessment':3,'status':'teacher_review_required','teacher_approved':False,'browser_accepted':False})
    (DOC/'topic10-acceptance-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    (DOC/'topic10-batch-acceptance.md').write_text(f'# Grade 9 Topic 10: Geometry of 2D Shapes\n\n[DBE 2026 Grade 9 Mathematics ATP]({ATP}) covers properties of triangles and quadrilaterals, polygon angles, congruency, similarity and geometric reasoning. This eight-lesson breakdown is Athena’s own.\n\n120 worked examples, 120 four-option practice items, 40 mastery items and 24 changed-value reassessments. Teacher mathematical review and real desktop/mobile browser acceptance remain required.\n',encoding='utf-8')
if __name__=='__main__':build()
