"""Original Grade 9 Term 4 surface area, volume and capacity content."""
import json
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/curriculum/grade9/surface-area-and-volume';OUT=ROOT/'backend/app/curriculum/grade9/generated'
ATP='https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2026%20ATPs/2026_ATP_Mathematics_Grade%209.pdf'
TITLES={1:'Cube and rectangular prism surface area from nets',2:'Rectangular prism volume and capacity',3:'Triangular prism surface area and volume',4:'Closed cylinders: surface area and volume',5:'SI conversions and effects of doubling dimensions',6:'Applied measurement, first-error repair and reassessment'}
def case(n,i,variant=0):
 seed=i+variant*15;v={'lesson':n};
 if n==1:
  cube=(i-1)%15<5;L=3+seed;W=L if cube else 2+seed%6;H=L if cube else 3+seed%5
  area=2*(L*W+L*H+W*H);v.update(model='box_net',shape='cube' if cube else 'rectangular prism',length=L,width=W,height=H,surface_area=area)
  problem=(f'A closed cube has edge {L} cm.' if cube else f'A closed rectangular prism has length {L} cm, width {W} cm and height {H} cm.')+' Draw its net and calculate its total surface area.'
  actions=[f'Label every edge: length {L} cm, width {W} cm, height {H} cm.',f'Two faces each have area {L} × {W} = {L*W} cm².',f'The other pairs have areas {L} × {H} = {L*H} cm² and {W} × {H} = {W*H} cm².',f'Total surface area = 2({L*W} + {L*H} + {W*H}) = {area} cm².',f'Check all six faces of the closed {v["shape"]} are counted once.']
  answer=f'surface area = {area} cm²';wrong=[f'surface area = {area+d} cm²' for d in (1,-1,2)]
 elif n==2:
  L=5+seed;W=4+seed%4;H=3+seed%5;vol=L*W*H;capacity=Fraction(vol,1000)
  v.update(model='box_layers',length=L,width=W,height=H,volume=vol,capacity_num=capacity.numerator,capacity_den=capacity.denominator)
  problem=f'A water tank is a rectangular prism with internal length {L} cm, width {W} cm and height {H} cm. Find its volume in cm³ and capacity in litres.'
  actions=[f'Mark the internal dimensions {L} cm by {W} cm by {H} cm.',f'One base layer covers {L} × {W} = {L*W} cm².',f'Stack {H} such 1 cm layers: {L*W} × {H} = {vol} cm³.',f'Use 1 000 cm³ = 1 L: capacity = {vol}/1000 = {capacity} L.',f'Check: {capacity} × 1000 = {vol} cm³; the units agree.']
  answer=f'volume = {vol} cm³; capacity = {capacity} L';wrong=[f'volume = {vol} cm³; capacity = {Fraction(vol,scale)} L' for scale in (100,10000,10)]
 elif n==3:
  k=1+seed;B=3*k;T=4*k;C=5*k;length=4+seed%8;base=B*T//2;vol=base*length;area=2*base+(B+T+C)*length
  v.update(model='tri_prism',base=B,altitude=T,hypotenuse=C,length=length,triangle_area=base,volume=vol,surface_area=area)
  problem=f'A right triangular prism has perpendicular triangle sides {B} cm and {T} cm, third side {C} cm, and prism length {length} cm. Find its volume and total surface area.'
  actions=[f'Confirm the triangle is right-angled: {B}² + {T}² = {C}².',f'One triangle has area ½ × {B} × {T} = {base} cm².',f'Volume = triangular base area × length = {base} × {length} = {vol} cm³.',f'Total surface area = 2({base}) + ({B} + {T} + {C}) × {length} = {area} cm².',f'Check: two triangular ends and three rectangles are counted; cm² differs from cm³.']
  answer=f'volume = {vol} cm³; surface area = {area} cm²';wrong=[f'volume = {wrong} cm³; surface area = {area} cm²' for wrong in (vol*2,vol+base,vol-base)]
 elif n==4:
  r=2+seed;h=5+seed%9;vol=r*r*h;area=2*r*(r+h)
  v.update(model='cylinder_net',radius=r,height=h,volume_pi=vol,surface_area_pi=area,diameter=2*r)
  problem=f'A closed cylinder has radius {r} cm and height {h} cm. Give its volume and total surface area exactly in terms of π.'
  actions=[f'Label the radius {r} cm, height {h} cm and two circular ends.',f'One circular base has area π × {r}² = {r*r}π cm².',f'Volume = base area × height = {r*r}π × {h} = {vol}π cm³.',f'The curved rectangle has area 2π × {r} × {h}; add two bases: total surface area = {area}π cm².',f'Check: both circular ends are included and radius, not diameter, is squared.']
  answer=f'volume = {vol}π cm³; surface area = {area}π cm²';wrong=[f'volume = {wrong}π cm³; surface area = {area}π cm²' for wrong in (2*vol,4*vol,vol+h)]
 elif n==5:
  kind=['one_axis','all_axes','litres'][((i-1)%15//5)];L=5+seed;W=3+seed%4;H=4+seed%5;original=L*W*H
  if kind=='one_axis':
   new=2*original;problem=f'A rectangular prism measures {L} cm × {W} cm × {H} cm. Only its length is doubled. Find the new volume and the factor of change.'
   actions=[f'Original dimensions: {L}, {W}, {H} cm.',f'Original volume = {L} × {W} × {H} = {original} cm³.',f'New length is {2*L} cm; width and height stay {W}, {H} cm.',f'New volume = {2*L} × {W} × {H} = {new} cm³.',f'Check: new/original = {new}/{original} = 2.']
   answer=f'new volume = {new} cm³; factor = 2';wrong=[f'new volume = {original*f} cm³; factor = {f}' for f in (4,8,3)]
  elif kind=='all_axes':
   new=8*original;problem=f'A rectangular prism measures {L} cm × {W} cm × {H} cm. Every dimension is doubled. Find the new volume and the factor of change.'
   actions=[f'Original dimensions: {L}, {W}, {H} cm.',f'Original volume = {L} × {W} × {H} = {original} cm³.',f'Each new dimension is doubled: {2*L}, {2*W}, {2*H} cm.',f'New volume = {2*L} × {2*W} × {2*H} = {new} cm³.',f'Check: 2 × 2 × 2 = 8; new/original = 8.']
   answer=f'new volume = {new} cm³; factor = 8';wrong=[f'new volume = {original*f} cm³; factor = {f}' for f in (2,4,6)]
  else:
   litres=Fraction(original,1000);problem=f'A rectangular tank measures {L} cm × {W} cm × {H} cm inside. Convert its capacity from cm³ to litres.'
   actions=[f'Mark internal length {L} cm, width {W} cm and height {H} cm.',f'Volume = {L} × {W} × {H} = {original} cm³.',f'Use the conversion 1 L = 1 000 cm³.',f'Capacity = {original}/1000 = {litres} L.',f'Check: {litres} L × 1000 = {original} cm³.']
   answer=f'capacity = {litres} L';wrong=[f'capacity = {Fraction(original,d)} L' for d in (10,100,10000)]
  v.update(model='scale_convert',kind=kind,length=L,width=W,height=H,original=original,new_volume=new if kind!='litres' else original,factor=2 if kind=='one_axis' else 8 if kind=='all_axes' else 1,litres_num=Fraction(original,1000).numerator,litres_den=Fraction(original,1000).denominator)
 else:
  kind=['open_box','triangle','cylinder','double_all','convert'][((i-1)%5)];L=5+seed;W=3+seed%4;H=4+seed%5
  if kind=='open_box':
   area=L*W+2*L*H+2*W*H;problem=f'An open-top rectangular box has length {L} cm, width {W} cm, height {H} cm. A learner includes a top face. Find the first error and the required material area.'
   actions=[f'Identify the base {L} cm × {W} cm; the top is open.',f'A closed prism has two bases, but this net has only one.',f'First error: the learner added a top face that does not exist.',f'Material area = {L*W} + 2({L*H}) + 2({W*H}) = {area} cm².',f'Check one base and four sides, no top; units are cm².']
   answer=f'first error: included a top; material area = {area} cm²';wrong=[f'first error: included a top; material area = {area+d} cm²' for d in (1,-1,2)]
  elif kind=='triangle':
   B=3*(1+seed);T=4*(1+seed);C=5*(1+seed);length=H;base=B*T//2;vol=base*length
   problem=f'A triangular prism has a right-triangle end with legs {B} cm and {T} cm, and length {length} cm. A learner omits ½. Find the first error and correct volume.'
   actions=[f'Triangle legs are {B} cm and {T} cm.',f'The learner used the area of a rectangle, omitting the half.',f'First error: triangle area is ½ × {B} × {T} = {base} cm².',f'Volume = {base} × {length} = {vol} cm³.',f'Check: half the enclosing rectangle gives the triangular cross-section.']
   answer=f'first error: omitted ½; volume = {vol} cm³';wrong=[f'first error: omitted ½; volume = {vol+d} cm³' for d in (vol,base,-base)]
   v.update(base=B,altitude=T,hypotenuse=C,length=length,triangle_area=base)
  elif kind=='cylinder':
   r=2+seed;h=H;vol=r*r*h;problem=f'A closed cylinder has diameter {2*r} cm and height {h} cm. A learner squares the diameter as the radius. Find the first error and correct volume in terms of π.'
   actions=[f'The given {2*r} cm is a diameter.',f'Radius = diameter ÷ 2 = {r} cm.',f'First error: squaring {2*r} instead of the radius {r}.',f'Volume = π × {r}² × {h} = {vol}π cm³.',f'Check: using the diameter would produce four times the correct volume.']
   answer=f'first error: used diameter; volume = {vol}π cm³';wrong=[f'first error: used diameter; volume = {vol+d}π cm³' for d in (vol,3*vol,-h)]
   v.update(radius=r,diameter=2*r,height=h)
  elif kind=='double_all':
   original=L*W*H;new=8*original;problem=f'A rectangular prism has dimensions {L} cm × {W} cm × {H} cm. A learner doubles its volume when all dimensions double. Find the first error and new volume.'
   actions=[f'Original volume = {L} × {W} × {H} = {original} cm³.',f'New dimensions are {2*L}, {2*W}, {2*H} cm.',f'First error: doubling all three dimensions multiplies volume by 8, not 2.',f'New volume = {2*L} × {2*W} × {2*H} = {new} cm³.',f'Check: {new}/{original} = 8.']
   answer=f'first error: used factor 2; new volume = {new} cm³';wrong=[f'first error: used factor 2; new volume = {original*f} cm³' for f in (2,4,6)]
  else:
   original=L*W*H;litres=Fraction(original,1000);problem=f'A rectangular container measures {L} cm × {W} cm × {H} cm inside. A learner divides cm³ by 100 to obtain litres. Find the first error and correct capacity.'
   actions=[f'Volume = {L} × {W} × {H} = {original} cm³.',f'The learner divided by 100, which converts square units rather than cubic capacity.',f'First error: 1 L = 1 000 cm³, so divide by 1000.',f'Correct capacity = {original}/1000 = {litres} L.',f'Check: {litres} × 1000 = {original} cm³.']
   answer=f'first error: divided by 100; capacity = {litres} L';wrong=[f'first error: divided by 100; capacity = {Fraction(original,d)} L' for d in (10,100,10000)]
  v.update(model='applied_error',kind=kind,length=H if kind=='triangle' else L if kind!='cylinder' else 0,width=W if kind!='cylinder' else 0,height=H,correct_value=area if kind=='open_box' else vol if kind in ('triangle','cylinder') else new if kind=='double_all' else original)
  if kind=='convert':v.update(litres_num=litres.numerator,litres_den=litres.denominator)
 assert len(set([answer,*wrong]))==4,(n,i,variant)
 return {'id':f'g9-sv-l{n:02}-w{i:02}' if not variant else f'g9-sv-l{n:02}-v{variant}-w{i:02}','problem':problem,'actions':actions,'answer':answer,'check':actions[-1],'visual':{'family':'surface_volume','values':v},'lesson':n,'misconception':'Distinguish length, square and cubic units; count each face once, then verify the given radius, height and conversion.','wrong':wrong}
def choice(n,i,variant,prefix):
 c=case(n,i,variant);opts=[c['answer'],*c['wrong']];pos=i%4;opts=opts[4-pos:]+opts[:4-pos] if pos else opts
 return {'id':f'g9-sv-l{n:02}-{prefix}{i:02}','prompt':c['problem'],'options':opts,'answer_index':pos,'memo':' '.join(c['actions']),'source':f'lesson-{n:02}.md'}
def build():
 DOC.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True);manifest=[]
 for n,title in TITLES.items():
  worked=[{k:v for k,v in case(n,i).items() if k!='wrong'}|{'difficulty':'foundation' if i<=2 else 'easy' if i<=5 else 'standard' if i<=9 else 'intermediate' if i<=12 else 'exam'} for i in range(1,16)]
  data={'source':f'lesson-{n:02}.md','worked':worked,'practice':[choice(n,i,1,'p') for i in range(1,16)],'mastery':[choice(n,i+15,2,'m') for i in range(1,6)],'reassessment':[choice(n,i+18,3,'r') for i in range(1,4)]}
  assert len({c['problem'] for c in worked})==15
  lines=[f'# Grade 9 Topic 15 · Lesson {n}: {title}',f'Authority: [DBE 2026 Grade 9 Mathematics ATP]({ATP}), Term 4. Original Athena questions.','Status: teacher and browser review required. Show the geometry and a cumulative written solution before revealing an answer.']
  for c in worked:lines.extend([f'## {c["id"]}: {c["problem"]}',f'Visual: {json.dumps(c["visual"],ensure_ascii=False)}',*[f'{j}. {step}' for j,step in enumerate(c['actions'],1)],f'**Answer:** {c["answer"]}. **Misconception:** {c["misconception"]}'])
  for label,key in [('Practice','practice'),('Mastery','mastery'),('Parallel reassessment','reassessment')]:
   lines.append(f'## {label} answer key')
   for c in data[key]:lines.append(f'- {c["id"]}: {c["prompt"]} Options: {" | ".join(c["options"])}. Correct: {c["options"][c["answer_index"]]}. {c["memo"]}')
  source=DOC/data['source'];source.write_text('\n\n'.join(lines)+'\n',encoding='utf-8');(OUT/f'surface_volume_{n:02}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  manifest.append({'lesson_id':f'g9-sv-{n:02}','source':source.name,'source_sha256':sha256(source.read_bytes()).hexdigest(),'worked':15,'practice':15,'mastery':5,'reassessment':3,'status':'teacher_review_required','teacher_approved':False,'browser_accepted':False})
 (DOC/'topic15-acceptance-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
 (DOC/'topic15-batch-acceptance.md').write_text(f'# Grade 9 Topic 15: Surface Area and Volume\n\n[DBE 2026 Grade 9 Mathematics ATP, Term 4]({ATP}) includes cubes, rectangular and triangular prisms, cylinders, SI capacity conversions and volume changes when dimensions double. Six Athena lessons contain 90 worked examples, 90 four-choice practice items, 30 mastery items and 18 reassessments. Teacher and browser acceptance remain required.\n',encoding='utf-8')
if __name__=='__main__':build()
