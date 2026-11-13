"""Original measurement revision questions grounded in Grade 11 ATP review scope."""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/curriculum/grade11/measurement-revision'
OUT=ROOT/'backend/app/curriculum/grade11/generated'
ATP='https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2023%20ATPs/FET%20Content%20Subjects/Grade%2011/1.590%20ATP%202023-24%20Gr%2011%20Maths%20final.pdf'
CAPS='https://www.education.gov.za/Portals/0/CD/National%20Curriculum%20Statements%20and%20Vocational/CAPS%20FET%20_%20MATHEMATICS%20_%20GR%2010-12%20_%20Web_1133.pdf'
TITLES={1:'Review prisms and cylinders',2:'Scale dimensions, surface area and volume',3:'Spheres and right cones',4:'Composite solids and exposed surfaces'}
DIFFICULTY=['foundation']*2+['easy']*3+['standard']*4+['intermediate']*3+['exam']*3

def pi(x):
 x=F(x)
 return ('π' if x==1 else '−π' if x==-1 else f'{x.numerator}π' if x.denominator==1 else f'({x.numerator}/{x.denominator})π')
def area_volume(volume,surface,has_pi=True):
 fmt=pi if has_pi else str
 return f'V = {fmt(volume)} cm³; exposed SA = {fmt(surface)} cm²'

def case(lesson,index,variant=0):
 t=index+15*variant
 h=4+t%9
 if lesson==1:
  if t%3==0:
   triples=[(3,4,5),(5,12,13),(8,15,17),(7,24,25),(9,12,15)]
   leg_a,leg_b,hyp=triples[(t//3-1)%5];length=5+t%8
   base=F(leg_a*leg_b,2);v=base*length
   sa=2*base+(leg_a+leg_b+hyp)*length
   prompt=f'A closed right triangular prism has a right-triangle cross-section with perpendicular sides {leg_a} cm and {leg_b} cm, and hypotenuse {hyp} cm. Its length is {length} cm. Find its volume and total exposed surface area.'
   steps=[f'Draw two congruent right-triangle ends with legs {leg_a} cm, {leg_b} cm, hypotenuse {hyp} cm; join corresponding vertices over length {length} cm.',
          f'Triangle area = (1/2)×{leg_a}×{leg_b} = {base} cm². There are two triangular ends and three rectangular side faces.',
          f'Volume = triangular base area × prism length = {base}×{length} = {v} cm³.',
          f'Exposed surface area = 2({base}) + ({leg_a} + {leg_b} + {hyp})({length}) = {sa} cm².',
          f'Answer: {area_volume(v,sa,False)}. Check both triangular ends and all three rectangles are included.']
   givens=dict(mode='triangular_prism',a=leg_a,b=leg_b,hyp=hyp,length=length)
   wrong_v,wrong_sa=base,sa-base
   has_pi=False
  elif t%3==1:
   l=3+t%7;w=2+t%6;v=l*w*h;sa=2*(l*w+l*h+w*h)
   prompt=f'A closed rectangular prism is {l} cm long, {w} cm wide and {h} cm high. Find its volume and total exposed surface area.'
   steps=[f'Draw a rectangular prism; mark length {l} cm, width {w} cm and height {h} cm.',
          f'There are two faces of each type: {l}×{w}, {l}×{h}, and {w}×{h} square centimetres.',
          f'Volume = {l}×{w}×{h} = {v} cm³.',
          f'Exposed surface area = 2({l}×{w} + {l}×{h} + {w}×{h}) = {sa} cm².',
          f'Answer: {area_volume(v,sa,False)}. Check volume is cubic and six faces, including the base, were counted.']
   givens=dict(mode='prism',l=l,w=w,h=h)
   wrong_v,wrong_sa=l*w,sa-l*w
   has_pi=False
  else:
   r=2+t%7;v=r*r*h;sa=2*r*h+2*r*r
   prompt=f'A closed right circular cylinder has radius {r} cm and height {h} cm. Give its volume and total exposed surface area in terms of π.'
   steps=[f'Draw the cylinder and mark radius {r} cm on both circular ends and perpendicular height {h} cm.',
          f'The two closed circular ends contribute 2π({r})²; the curved side contributes 2π({r})({h}).',
          f'Volume = π({r})²({h}) = {pi(v)} cm³.',
          f'Exposed surface area = 2π({r})² + 2π({r})({h}) = {pi(sa)} cm².',
          f'Answer: {area_volume(v,sa)}. Check that both circular ends and the curved side were included.']
   givens=dict(mode='cylinder',r=r,h=h)
   wrong_v,wrong_sa=r*h,sa-r*r
   has_pi=True
 elif lesson==2:
  l=3+t%6;w=2+t%5;h=4+t%7;k=2+t%3;all_dimensions=bool(t%2)
  new=(l*k,w*k,h*k) if all_dimensions else (l,w,h*k)
  v=new[0]*new[1]*new[2]
  sa=2*(new[0]*new[1]+new[0]*new[2]+new[1]*new[2])
  if all_dimensions:
   prompt=f'A rectangular prism measures {l} cm by {w} cm by {h} cm. Every dimension is multiplied by {k}. Find its new volume and exposed surface area. State the volume and area scale factors.'
   step2=f'Each dimension changes: {l}→{new[0]}, {w}→{new[1]}, {h}→{new[2]} cm. The volume factor is {k}³ = {k**3}, the area factor is {k}² = {k**2}.'
  else:
   prompt=f'A rectangular prism measures {l} cm by {w} cm by {h} cm. Only its height is multiplied by {k}; length and width stay fixed. Find its new volume and exposed surface area.'
   step2=f'Only height changes from {h} to {new[2]} cm. The top and bottom retain area {l}×{w}; the four side faces change.'
  steps=[f'Draw and label the original prism: {l} cm by {w} cm by {h} cm. Mark the changed dimensions only.',step2,
         f'New volume = {new[0]}×{new[1]}×{new[2]} = {v} cm³.',
         f'New exposed surface area = 2({new[0]}×{new[1]} + {new[0]}×{new[2]} + {new[1]}×{new[2]}) = {sa} cm².',
         f'Answer: {area_volume(v,sa,False)}. Check the volume factor is {v//(l*w*h)}; the area changes according to the actual new faces.']
  givens=dict(mode='scale',l=l,w=w,h=h,k=k,all_dimensions=all_dimensions)
  wrong_v,wrong_sa=l*w*h,2*(l*w+l*h+w*h)
  has_pi=False
 elif lesson==3:
  if t%2:
   r=2+t;v=F(4*r**3,3);sa=4*r*r
   prompt=f'A sphere has radius {r} cm. Find its volume and exposed surface area in terms of π.'
   steps=[f'Mark radius {r} cm from the centre of the sphere to its surface.',
          f'Use V = (4/3)πr³ and SA = 4πr². The surface is one continuous exposed boundary.',
          f'Volume = (4/3)π({r})³ = {pi(v)} cm³.',
          f'Exposed surface area = 4π({r})² = {pi(sa)} cm².',
          f'Answer: {area_volume(v,sa)}. Check the volume uses a cube and the surface area uses a square.']
   givens=dict(mode='sphere',r=r)
   wrong_v,wrong_sa=F(4*r*r,3),4*r**3
  else:
   pairs=[(3,4,5),(4,3,5),(5,12,13),(6,8,10),(8,15,17)]
   base_r,base_h,base_s=pairs[(t//2)%5];m=1+2*(t//10);r=base_r*m;h=base_h*m;s=base_s*m
   v=F(r*r*h,3);sa=r*(r+s)
   prompt=f'A closed right cone has radius {r} cm and perpendicular height {h} cm. Find its slant height, volume and total exposed surface area in terms of π.'
   steps=[f'Draw the right cone. Mark base radius {r} cm and perpendicular height {h} cm from apex to centre.',
          f'Use a right triangle to find the slant height: √({r}² + {h}²) = {s} cm. This is the curved-side length.',
          f'Volume = (1/3)π({r})²({h}) = {pi(v)} cm³.',
          f'Exposed surface area = π({r})({s}) + π({r})² = {pi(sa)} cm², including the closed base.',
          f'Answer: {area_volume(v,sa)}; slant height = {s} cm. Check the perpendicular height was used for volume.']
   givens=dict(mode='cone',r=r,h=h)
   wrong_v,wrong_sa=r*r*h,r*s
  has_pi=True
 else:
  if t%2:
   r=2+t%6;h=4+t%7
   v=F(r*r*h)+F(2*r**3,3);sa=2*r*h+3*r*r
   prompt=f'A hemisphere of radius {r} cm is fixed to the top of a cylinder with the same radius and height {h} cm. The bottom circular base is exposed and the joined circle is hidden. Find the total volume and exposed surface area in terms of π.'
   steps=[f'Draw a cylinder and hemispherical cap with radius {r} cm; label cylinder height {h} cm. Mark the joined circular face as hidden.',
          f'Total volume = cylinder πr²h plus hemisphere (2/3)πr³. Volumes add despite the hidden join.',
          f'Substitute V = π({r})²({h}) + (2/3)π({r})³ = {pi(v)} cm³.',
          f'Exposed area includes cylinder curved side 2πrh, bottom πr² and hemispherical curved surface 2πr²: {pi(sa)} cm².',
          f'Answer: {area_volume(v,sa)}. Verify the shared top circle is excluded exactly once from exposed area.']
   givens=dict(mode='hemisphere_cylinder',r=r,h=h)
   wrong_v,wrong_sa=r*r*h,2*r*h+r*r
  else:
   pairs=[(3,4,5),(4,3,5),(5,12,13),(6,8,10),(8,15,17)]
   br,bh,bs=pairs[(t//2)%5];m=1+2*(t//10);r=br*m;cone_h=bh*m;cyl_h=4+t%8;s=bs*m
   v=F(r*r*cyl_h)+F(r*r*cone_h,3)
   sa=2*r*cyl_h+r*r+r*s
   prompt=f'A closed-bottom cylinder of radius {r} cm and height {cyl_h} cm supports a right cone of the same radius and perpendicular height {cone_h} cm. Their joined circular face is hidden. Find the total volume and exposed surface area in terms of π.'
   steps=[f'Draw the stacked cylinder and cone: common radius {r} cm, cylinder height {cyl_h} cm, cone perpendicular height {cone_h} cm.',
          f'The cone slant height is √({r}² + {cone_h}²) = {s} cm. The common circular join is not exposed.',
          f'Volume = π({r})²({cyl_h}) + (1/3)π({r})²({cone_h}) = {pi(v)} cm³.',
          f'Exposed area = cylinder curve 2π({r})({cyl_h}) + bottom π({r})² + cone curve π({r})({s}) = {pi(sa)} cm².',
          f'Answer: {area_volume(v,sa)}. Check neither the cylinder top nor the cone base was added to exposed area.']
   givens=dict(mode='cone_cylinder',r=r,h=cyl_h,cone_h=cone_h)
   wrong_v,wrong_sa=r*r*cyl_h,2*r*cyl_h+r*r
  has_pi=True
 answer=area_volume(v,sa,has_pi)
 assert len(steps)==5 and answer in steps[-1]
 # Both wrong dimensions are independent plausible errors, yielding four distinct MCQ options.
 fmt=lambda x,y:area_volume(x,y,has_pi)
 wrong=[fmt(wrong_v,sa),fmt(v,wrong_sa),fmt(wrong_v,wrong_sa)]
 assert len(set([answer,*wrong]))==4
 return dict(id=f'g11-meas-l{lesson:02}-w{index:02}',lesson=lesson,problem=prompt,
   answer=answer,actions=steps,check=steps[-1],visual=dict(family='grade11_measurement',values=givens),
   difficulty=DIFFICULTY[index-1],wrong=wrong)

def build():
 DOC.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True);manifest=[]
 for n,title in TITLES.items():
  worked=[{k:v for k,v in case(n,i).items() if k!='wrong'} for i in range(1,16)]
  assert len({q['problem'] for q in worked})==15
  data=dict(source=f'grade11-meas-lesson-{n:02}.md',worked=worked)
  for section,count,variant,prefix in [('practice',15,1,'p'),('mastery',5,2,'m'),('reassessment',3,3,'r')]:
   bank=[]
   for i in range(1,count+1):
    q=case(n,i,variant);options=[q['answer'],*q['wrong']];shift=(i+variant)%4;options=options[shift:]+options[:shift]
    bank.append(dict(id=f'g11-meas-l{n:02}-{prefix}{i:02}',prompt=q['problem'],options=options,
                     answer_index=options.index(q['answer']),actions=q['actions'],memo=' '.join(q['actions'])))
   data[section]=bank
  lines=[f'# Grade 11 Measurement Revision, Lesson {n}: {title}',f'[DBE ATP]({ATP}) and [Mathematics CAPS]({CAPS}).',
    'This is an Athena revision path, not a separate newly prescribed CAPS topic. Original questions; teacher and live browser acceptance required.',
    'All dimensions are centimetres. Exact π answers are retained. Closed bases and hidden joins are labelled per question.']
  for q in worked:lines.extend([f'## {q["id"]}: {q["problem"]}',f'Question-specific visual givens: `{json.dumps(q["visual"],ensure_ascii=False)}`',
    *[f'{j}. {s}' for j,s in enumerate(q['actions'],1)],f'Answer: {q["answer"]}. Check: {q["check"]}'])
  for section in ('practice','mastery','reassessment'):
   lines.append(f'## {section.title()} key')
   for q in data[section]:lines.append(f'- {q["id"]}: {q["prompt"]} Options: {" | ".join(q["options"])}. Correct: {q["options"][q["answer_index"]]}. {q["memo"]}')
  source=DOC/data['source'];source.write_text('\n\n'.join(lines)+'\n',encoding='utf-8')
  (OUT/f'measurement_{n:02}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  manifest.append(dict(lesson_id=f'g11-meas-{n:02}',source=source.name,source_sha256=sha256(source.read_bytes()).hexdigest(),worked=15,practice=15,mastery=5,reassessment=3,status='teacher_review_required',teacher_approved=False,browser_accepted=False))
 (DOC/'topic12-acceptance-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':build()
