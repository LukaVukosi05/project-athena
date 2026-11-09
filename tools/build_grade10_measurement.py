"""Original Grade 10 measurement question bank: exact symbolic volumes and surfaces."""
from pathlib import Path
from hashlib import sha256
import json
ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/curriculum/grade10/measurement';OUT=ROOT/'backend/app/curriculum/grade10/generated'
ATP='https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2023%20ATPs/FET%20Content%20Subjects/Grade%2010/1.580%20ATP%202023-24%20Gr%2010%20Maths%20final.pdf'
TITLES={1:'Right prisms: volume and surface area',2:'Cylinders and exposed surfaces',3:'Scaling dimensions, surface and volume',4:'Spheres and hemispheres',5:'Right pyramids and cones',6:'Composite solids and first-error repair'}
def case(n,i,variant=0):
 s=i+variant*29
 if n==1:
  a=3+s%7;b=4+(s//2)%8;h=5+(s//3)%9;V=a*b*h;S=2*(a*b+a*h+b*h)
  problem=f'A sealed rectangular prism measures {a} cm by {b} cm by {h} cm. Calculate its volume and total surface area.'
  answer=f'volume {V} cm³; total surface area {S} cm²'
  actions=[f'Mark length {a} cm, width {b} cm and height {h} cm on the same prism.',f'The base has area {a}×{b}={a*b} cm².',f'Volume = base area × height = {a*b}×{h}={V} cm³.',f'Pairs of faces have areas {a*b}, {a*h} and {b*h} cm², so total surface area = 2({a*b}+{a*h}+{b*h})={S} cm².',f'Answer: {answer}. Confirm there are six outside faces.']
  wrong=[f'volume {S} cm³; total surface area {V} cm²',f'volume {V} cm³; total surface area {S//2} cm²',f'volume {a+b+h} cm³; total surface area {S} cm²']
  v={'shape':'prism','a':a,'b':b,'h':h,'volume':V,'surface':S}
 elif n==2:
  r=2+s%7;h=5+(s//2)%10;V=r*r*h;curved=2*r*h;top=r*r;S=curved+2*top;open_top=s%2==0;actual=curved+top if open_top else S
  problem=f'A right circular cylinder has radius {r} cm and height {h} cm. Its top is {"open" if open_top else "closed"} and its base is closed. Find its volume and exposed surface area in terms of π.'
  answer=f'volume {V}π cm³; exposed surface area {actual}π cm²'
  actions=[f'Label radius {r} cm and perpendicular height {h} cm; the base is a circle.',f'Base area = π×{r}²={top}π cm²; volume = {top}π×{h}={V}π cm³.',f'Unwrap the curved wall: circumference 2π×{r} multiplied by height {h} gives {curved}π cm².',f'Include the closed base ({top}π cm²)'+(' but exclude the open top.' if open_top else f' and the closed top (another {top}π cm²).'),f'Answer: {answer}. Surface counts only exposed faces.']
  wrong=[f'volume {V}π cm³; exposed surface area {S if open_top else curved+top}π cm²',f'volume {2*V}π cm³; exposed surface area {actual}π cm²',f'volume {V}π cm³; exposed surface area {V}π cm²']
  v={'shape':'cylinder','r':r,'h':h,'open_top':open_top,'volume':V,'surface':actual}
 elif n==3:
  a=3+s%6;b=4+(s//2)%6;h=5+(s//3)%6;k=2+s%3;one_dimension=s%2==0;oldV=a*b*h;oldS=2*(a*b+a*h+b*h)
  A=a*k;B=b if one_dimension else b*k;H=h if one_dimension else h*k;V=A*B*H;S=2*(A*B+A*H+B*H)
  change='only its length' if one_dimension else 'each of its three dimensions'
  problem=f'A {a} cm × {b} cm × {h} cm rectangular prism is enlarged by multiplying {change} by {k}. Find its new dimensions, volume and total surface area.'
  answer=f'{A} cm × {B} cm × {H} cm; volume {V} cm³; total surface area {S} cm²'
  actions=[f'Mark the original length {a}, width {b} and height {h} cm; record the scale instruction precisely.',f'Change {change} by factor {k}: new dimensions {A} cm × {B} cm × {H} cm.',f'New volume = {A}×{B}×{H}={V} cm³ (original {oldV} cm³).',f'New total surface area = 2({A*B}+{A*H}+{B*H})={S} cm² (original {oldS} cm²).',f'Answer: {answer}. {"Only one dimension changed, so do not apply k² or k³ to every measure." if one_dimension else "All dimensions changed: volume scales by k³ and surface by k²."}']
  wrong=[f'{A} cm × {B} cm × {H} cm; volume {oldV*k*k*k if one_dimension else oldV*k} cm³; total surface area {S} cm²',f'{A} cm × {B} cm × {H} cm; volume {V} cm³; total surface area {oldS*k*k if one_dimension else oldS*k} cm²',f'{a} cm × {b} cm × {h} cm; volume {oldV} cm³; total surface area {oldS} cm²']
  # Wrong candidates can coincide if formula happens to yield the right value; repair with unmistakably distinct numbers.
  for j,x in enumerate(wrong):
   if x==answer or x in wrong[:j]:wrong[j]=f'{A} cm × {B} cm × {H} cm; volume {V+j+1} cm³; total surface area {S} cm²'
  v={'shape':'prism','a':a,'b':b,'h':h,'scaled_a':A,'scaled_b':B,'scaled_h':H,'scale':k,'one_dimension':one_dimension,'volume':V,'surface':S}
 elif n==4:
  r=3*(1+s%9);hemi=s%2==0;V=2*r**3//3 if hemi else 4*r**3//3;S=3*r*r if hemi else 4*r*r
  problem=f'A {"solid hemisphere with its flat circular base exposed" if hemi else "solid sphere"} has radius {r} cm. Find its volume and total exposed surface area in terms of π.'
  answer=f'volume {V}π cm³; total exposed surface area {S}π cm²'
  curved=2*r*r if hemi else 4*r*r
  actions=[f'Mark the radius from centre to surface: {r} cm.',f'Choose the {"half-sphere" if hemi else "full-sphere"} volume formula: {"2/3" if hemi else "4/3"}πr³.',f'Volume = {"2/3" if hemi else "4/3"}π({r})³={V}π cm³.',f'{"Curved hemisphere area = 2πr² = "+str(curved)+"π cm²; add the exposed flat disc "+str(r*r)+"π cm²." if hemi else "Sphere area = 4πr² = "+str(S)+"π cm²; it has no flat base."}',f'Answer: {answer}. Compare squared area units with cubed volume units.']
  wrong=[f'volume {V}π cm³; total exposed surface area {curved if hemi else 2*r*r}π cm²',f'volume {V*2}π cm³; total exposed surface area {S}π cm²',f'volume {S}π cm³; total exposed surface area {V}π cm²']
  v={'shape':'hemisphere' if hemi else 'sphere','r':r,'volume':V,'surface':S}
 elif n==5:
  cone=s%2==0
  if cone:
   r,h,l=[(3,4,5),(5,12,13),(8,15,17)][s%3];m=1+(s//3)%6;r*=m;h*=m;l*=m;V=r*r*h//3;S=r*l+r*r
   problem=f'A closed right cone has radius {r} cm and perpendicular height {h} cm. Find its slant height, volume and total surface area in terms of π.'
   answer=f'slant height {l} cm; volume {V}π cm³; total surface area {S}π cm²'
   actions=[f'Mark radius {r} cm and perpendicular height {h} cm; the slant height runs down the side.',f'Use Pythagoras: l²={r}²+{h}²={l*l}, so l={l} cm.',f'Volume = 1/3πr²h = 1/3π×{r}²×{h}={V}π cm³.',f'Curved area = πrl={r*l}π cm²; add circular base {r*r}π cm² to get {S}π cm².',f'Answer: {answer}. Height and slant height have different roles.']
   wrong=[f'slant height {h} cm; volume {V}π cm³; total surface area {S}π cm²',f'slant height {l} cm; volume {r*r*l//3}π cm³; total surface area {S}π cm²',f'slant height {l} cm; volume {V}π cm³; total surface area {r*l}π cm²']
   v={'shape':'cone','r':r,'h':h,'slant':l,'volume':V,'surface':S}
  else:
   b,h,l=[(6,4,5),(8,3,5),(10,12,13)][s%3];m=1+(s//3)%6;b*=m;h*=m;l*=m;V=b*b*h//3;S=b*b+2*b*l
   problem=f'A closed right square pyramid has base side {b} cm and perpendicular height {h} cm. Find the slant height, volume and total surface area.'
   answer=f'slant height {l} cm; volume {V} cm³; total surface area {S} cm²'
   actions=[f'Mark square base side {b} cm and perpendicular height {h} cm.',f'From the centre to midpoint of a base side is {b//2} cm; l²={h}²+{b//2}²={l*l}, hence l={l} cm.',f'Volume = 1/3×{b*b}×{h}={V} cm³.',f'Four triangular faces total 4(1/2×{b}×{l})={2*b*l} cm²; add the base {b*b} cm² to get {S} cm².',f'Answer: {answer}. Use the slant height for triangle area, perpendicular height for volume.']
   wrong=[f'slant height {h} cm; volume {V} cm³; total surface area {S} cm²',f'slant height {l} cm; volume {b*b*l//3} cm³; total surface area {S} cm²',f'slant height {l} cm; volume {V} cm³; total surface area {2*b*l} cm²']
   v={'shape':'pyramid','b':b,'h':h,'slant':l,'volume':V,'surface':S}
 else:
  r=3*(1+s%4);h=4+s%9;cylinder=r*r*h;hemi=2*r**3//3;V=cylinder+hemi;S=2*r*h+3*r*r
  problem=f'A solid is a right cylinder of radius {r} cm and height {h} cm capped by a hemisphere of the same radius. Its bottom is exposed and its joining circle is internal. Find total volume and outside surface area in terms of π.'
  answer=f'volume {V}π cm³; outside surface area {S}π cm²'
  actions=[f'Mark common radius {r} cm and cylinder height {h} cm; locate the internal join.',f'Cylinder volume = π×{r}²×{h}={cylinder}π cm³.',f'Hemisphere volume = 2/3π×{r}³={hemi}π cm³; combined volume = {V}π cm³.',f'Outside area is cylinder wall {2*r*h}π plus exposed bottom disc {r*r}π plus curved hemisphere {2*r*r}π = {S}π cm².',f'Answer: {answer}. The joining disc is internal and must not be counted.']
  wrong=[f'volume {V}π cm³; outside surface area {S+r*r}π cm²',f'volume {cylinder}π cm³; outside surface area {S}π cm²',f'volume {V}π cm³; outside surface area {S-r*r}π cm²']
  v={'shape':'cylinder_hemisphere','r':r,'h':h,'cylinder_volume':cylinder,'hemisphere_volume':hemi,'volume':V,'surface':S}
 for j,x in enumerate(wrong):
  if x==answer or x in wrong[:j]:
   unit='π' if v['shape'] not in ('prism','pyramid') else ''
   wrong[j]=f'volume {v["volume"]+j+1}{unit} cm³; total surface area {v["surface"]}{unit} cm²'
 if n==6:
  claim=wrong[0];correct=answer
  problem+=f' A learner claims {claim}. Find the first error and give the correct measurements.'
  answer=f'first error: counted the internal joining circle as outside area; correct: {correct}'
  actions=[actions[0],f'Inspect the learner’s claim: {claim}. Mark the joining disc as internal.',
   f'First error: an internal circle of area {r*r}π cm² was added to the outside surface.',
   actions[3],f'Answer: {answer}. Count the cylinder wall, exposed bottom and curved hemisphere exactly once.']
  wrong=[f'No error; {claim}',f'first error: counted the internal joining circle as outside area; correct: {claim}',f'No error; {correct}']
 assert len(actions)==5 and len({answer,*wrong})==4,(n,i,answer,wrong)
 v['lesson']=n;v['answer']=answer
 return {'id':f'g10-meas-l{n:02}-w{i:02}','lesson':n,'problem':problem,'actions':actions,'answer':answer,'check':actions[-1],
   'visual':{'family':'grade10_measurement','values':v},'wrong':wrong,
   'misconception':'Distinguish perpendicular height from slant, exposed faces from internal joins, and area units from volume units.',
   'difficulty':'foundation' if i<=2 else 'easy' if i<=5 else 'standard' if i<=9 else 'intermediate' if i<=12 else 'exam'}
def item(n,i,variant,prefix):
 q=case(n,i,variant);position=i%4;opts=[q['answer'],*q['wrong']];opts=opts[-position:]+opts[:-position] if position else opts
 return {'id':f'g10-meas-l{n:02}-{prefix}{i:02}','prompt':q['problem'],'options':opts,'answer_index':position,'memo':' '.join(q['actions']),'source':f'grade10-meas-lesson-{n:02}.md'}
def build():
 DOC.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True);manifest=[]
 for n,title in TITLES.items():
  worked=[{k:v for k,v in case(n,i).items() if k!='wrong'} for i in range(1,16)]
  data={'source':f'grade10-meas-lesson-{n:02}.md','worked':worked,'practice':[item(n,i,1,'p') for i in range(1,16)],'mastery':[item(n,i+15,2,'m') for i in range(1,6)],'reassessment':[item(n,i+20,3,'r') for i in range(1,4)]}
  assert len({x['problem'] for x in worked})>=10,n
  lines=[f'# Grade 10 Topic 10 · Lesson {n}: {title}',f'Authority: [DBE Grade 10 ATP]({ATP}), Term 4 Measurement. Original Athena examples.','Status: teacher and browser review required. All dimensions and exposed surfaces are question-specific.']
  for q in worked:lines += [f'## {q["id"]}: {q["problem"]}',f'Visual contract: {json.dumps(q["visual"],ensure_ascii=False)}',*[f'{j}. {a}' for j,a in enumerate(q['actions'],1)],f'**Answer:** {q["answer"]}. **Misconception:** {q["misconception"]}']
  for label,key in [('Practice','practice'),('Mastery','mastery'),('Parallel reassessment','reassessment')]:
   lines.append(f'## {label} answer key')
   for q in data[key]:lines.append(f'- {q["id"]}: {q["prompt"]} Options: {" | ".join(q["options"])}. Correct: {q["options"][q["answer_index"]]}. {q["memo"]}')
  source=DOC/data['source'];source.write_text('\n\n'.join(lines)+'\n',encoding='utf-8')
  (OUT/f'measurement_{n:02}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  manifest.append({'lesson_id':f'g10-meas-{n:02}','source':source.name,'source_sha256':sha256(source.read_bytes()).hexdigest(),'worked':15,'practice':15,'mastery':5,'reassessment':3,'status':'teacher_review_required','teacher_approved':False,'browser_accepted':False})
 (DOC/'topic10-acceptance-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
 (DOC/'topic10-batch-acceptance.md').write_text(f'# Grade 10 Topic 10: Measurement\n\n[DBE Grade 10 ATP]({ATP}) Term 4 covers right prisms, cylinders, scaling dimensions, spheres, right pyramids, right cones and composite figures. Six authored lessons include 90 worked, 90 four-choice practice, 30 mastery and 18 reassessment questions. Teacher and browser acceptance pending.\n',encoding='utf-8')
if __name__=='__main__':build()
