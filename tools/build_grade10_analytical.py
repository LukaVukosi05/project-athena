"""Original Grade 10 Analytical Geometry source with exact coordinate arithmetic."""
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import json
import math

ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/curriculum/grade10/analytical-geometry'
OUT=ROOT/'backend/app/curriculum/grade10/generated'
ATP='https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2023%20ATPs/FET%20Content%20Subjects/Grade%2010/1.580%20ATP%202023-24%20Gr%2010%20Maths%20final.pdf'
TITLES={1:'Distance between two points and the right-triangle construction',
 2:'Midpoint and the missing endpoint',3:'Gradient as rise over run',
 4:'Parallel and perpendicular gradients',5:'Classify quadrilaterals from coordinates',
 6:'Mixed coordinate proofs and first-error repair'}
def f(v):return str(v.numerator) if isinstance(v,Fraction) and v.denominator==1 else str(v)
def case(n,i,variant=0):
 s=i+15*variant;x=-7+(s*3)%13;y=-6+(s*5)%11;sign=-1 if s%2 else 1
 values={'lesson':n,'model':'segment','points':[],'mode':''}
 if n==1:
  dx,dy,h=[(3,4,5),(5,12,13),(8,15,17)][(s-1)%3];scale=1+(s//4)%2 if (s-1)%3==0 else 1
  dx*=scale;dy*=scale;h*=scale;dy*=sign
  A=[x,y];B=[x+dx,y+dy]
  problem=f'On a Cartesian plane A({x}; {y}) and B({B[0]}; {B[1]}). Find the exact distance AB.'
  answer=f'AB = {h} units'
  actions=[f'Plot A({x}; {y}) and B({B[0]}; {B[1]}) on the same axes.',f'Draw horizontal run Δx={dx} and vertical rise Δy={dy}.',f'Use AB²=(Δx)²+(Δy)²={dx}²+({dy})²={h*h}.',f'Take the positive root: AB=√{h*h}={h} units.',f'Answer: {answer}. Check by squaring: {h}²={dx*dx}+{dy*dy}.']
  wrong=[f'AB = {abs(dx)+abs(dy)} units',f'AB = {h*h} units',f'AB = {h+1} units']
  values.update(points=[A,B],mode='distance',dx=dx,dy=dy)
 elif n==2:
  dx=2*(2+s%6);dy=2*sign*(1+(s//2)%5);A=[x,y];B=[x+dx,y+dy];M=[x+dx//2,y+dy//2]
  if s%3==0:
   problem=f'A({x}; {y}) and midpoint M({M[0]}; {M[1]}) are given. Find the other endpoint B.'
   answer=f'B({B[0]}; {B[1]})'
   actions=[f'Plot A({x}; {y}) and midpoint M({M[0]}; {M[1]}).','A→M is half the full directed displacement A→B.',f'The vector A→M is ({M[0]-x}; {M[1]-y}); repeat it from M.',f'B=2M−A=({2*M[0]}−({x}); {2*M[1]}−({y}))=({B[0]}; {B[1]}).',f'Answer: {answer}. Check that averaging A and B returns M.']
   wrong=[f'B({M[0]}; {M[1]})',f'B({B[0]+1}; {B[1]})',f'B({B[0]}; {B[1]+1})']
   values.update(points=[A,M],mode='reverse_midpoint',solution_point=B)
  else:
   problem=f'Find the midpoint of A({x}; {y}) and B({B[0]}; {B[1]}).'
   answer=f'M({M[0]}; {M[1]})'
   actions=[f'Plot A({x}; {y}) and B({B[0]}; {B[1]}).','The midpoint is halfway along the horizontal and vertical displacements.',f'Average x: ({x}+{B[0]})/2={M[0]}.',f'Average y: ({y}+{B[1]})/2={M[1]}.',f'Answer: {answer}. Check AM and MB have the same directed displacement.']
   wrong=[f'M({B[0]}; {B[1]})',f'M({M[0]+1}; {M[1]})',f'M({M[0]}; {M[1]+1})']
   values.update(points=[A,B],mode='midpoint',solution_point=M)
 elif n==3:
  dx=2+s%6;dy=sign*(1+(s//2)%6);A=[x,y];B=[x+dx,y+dy];slope=Fraction(dy,dx)
  problem=f'Find the gradient of the segment joining A({x}; {y}) to B({B[0]}; {B[1]}).'
  answer=f'm = {f(slope)}'
  actions=[f'Plot A({x}; {y}) and B({B[0]}; {B[1]}).',f'Move horizontally from A by Δx={dx}; keep the x-axis scale fixed.',f'Move vertically by Δy={dy}; down gives a negative rise.',f'Gradient m=Δy/Δx={dy}/{dx}={f(slope)}.',f'Answer: {answer}. Reverse both differences and the quotient is unchanged.']
  wrong=[f'm = {f(Fraction(dx,dy))}',f'm = {f(-slope)}',f'm = {f(slope+1)}']
  values.update(points=[A,B],mode='gradient',dx=dx,dy=dy)
 elif n==4:
  p=2+s%4;q=1+(s//3)%4;A=[x,y];B=[x+p,y+q];C=[x+2,y+7];relation='parallel' if s%2 else 'perpendicular'
  D=[C[0]+p,C[1]+q] if relation=='parallel' else [C[0]+q,C[1]-p]
  m1=Fraction(q,p);m2=Fraction(D[1]-C[1],D[0]-C[0])
  problem=f'AB joins A({x}; {y}) to B({B[0]}; {B[1]}). CD joins C({C[0]}; {C[1]}) to D({D[0]}; {D[1]}). Are AB and CD parallel or perpendicular? Justify with gradients.'
  answer=f'AB ⟂ CD' if relation=='perpendicular' else 'AB ∥ CD'
  actions=[f'Plot the four supplied points and draw the two segments.',f'Find mAB=({B[1]}−({y}))/({B[0]}−({x}))={f(m1)}.',f'Find mCD=({D[1]}−({C[1]}))/({D[0]}−({C[0]}))={f(m2)}.',f'The gradient product is −1, so the segments are perpendicular.' if relation=='perpendicular' else 'The gradients are equal, so the segments are parallel.',f'Answer: {answer}. Compare the slopes, not the picture alone.']
  wrong=[('AB ∥ CD' if relation=='perpendicular' else 'AB ⟂ CD'),'Neither parallel nor perpendicular','The gradients are undefined']
  values.update(model='two_segments',points=[A,B,C,D],mode=relation)
 elif n==5:
  shape=['parallelogram','rectangle','rhombus','square','trapezium'][(s-1)%5];a=3+s%4;b=2+(s//3)%4
  if shape=='parallelogram':U=(a,0);V=(1,b)
  elif shape=='rectangle':U=(a,0);V=(0,a+1)
  elif shape=='rhombus':
   if a==b:b+=1
   U=(a,b);V=(a,-b)
  elif shape=='square':U=(a,0);V=(0,a)
  else:U=(a+3,0);V=(1,b)
  A=[x,y];B=[x+U[0],y+U[1]];D=[x+V[0],y+V[1]]
  C=[B[0]+V[0],B[1]+V[1]] if shape!='trapezium' else [D[0]+a,D[1]]
  problem=f'Classify ABCD using its coordinates: A({x}; {y}), B({B[0]}; {B[1]}), C({C[0]}; {C[1]}), D({D[0]}; {D[1]}).'
  answer=f'ABCD is a {shape}'
  if shape=='trapezium':reason='AB ∥ CD (both horizontal), while AD and BC have different gradients; exactly one opposite pair is parallel.'
  elif shape=='square':reason='All four sides are equal and adjacent horizontal and vertical sides meet at right angles.'
  elif shape=='rhombus':reason='All four side lengths are equal; adjacent side dot product is nonzero, so it is not a square.'
  elif shape=='rectangle':reason='Opposite sides are parallel and adjacent horizontal and vertical sides meet at right angles; adjacent lengths differ.'
  else:reason='Both pairs of opposite sides have equal direction vectors; adjacent vectors are neither perpendicular nor equal in length.'
  actions=[f'Plot A, B, C and D at their stated coordinates.',f'Draw AB, BC, CD and DA in that order.','Compute the horizontal and vertical changes for opposite sides.',reason,f'Answer: {answer}. A sketch alone is not a proof.']
  wrong=[f'ABCD is a {x}' for x in ['parallelogram','rectangle','rhombus','square','trapezium'] if x!=shape][:3]
  values.update(model='quadrilateral',points=[A,B,C,D],mode=shape)
 else:
  mode=['distance_check','midpoint_check','gradient_check'][(s-1)%3]
  A=[x,y]
  if mode=='distance_check':
   dx=3*(1+s%3);dy=4*(1+s%3)*sign;B=[x+dx,y+dy];correct=5*(1+s%3)
   problem=f'A learner adds the run and rise for A({x}; {y}), B({B[0]}; {B[1]}) and reports AB={abs(dx)+abs(dy)}. Identify the first error and find AB.'
   answer=f'Use Pythagoras, not a sum; AB = {correct} units'
   actions=[f'Plot A({x}; {y}) and B({B[0]}; {B[1]}).',f'Build the right triangle with run {dx} and rise {dy}.','The first error is adding the legs to get a diagonal. Use Pythagoras.',f'AB=√({dx}²+({dy})²)={correct} units.',f'Answer: {answer}. Square the diagonal to check.']
   wrong=[f'AB = {abs(dx)+abs(dy)} units',f'AB = {correct*correct} units',f'AB = {correct+1} units'];values.update(points=[A,B],mode=mode,dx=dx,dy=dy)
  elif mode=='midpoint_check':
   dx=2*(2+s%5);dy=2*sign*(1+(s//2)%3);B=[x+dx,y+dy];M=[x+dx//2,y+dy//2]
   problem=f'A learner calls B({B[0]}; {B[1]}) the midpoint of A({x}; {y}) and B({B[0]}; {B[1]}). Find the first error and correct midpoint.'
   answer=f'The endpoint is not the midpoint; M({M[0]}; {M[1]})'
   actions=[f'Plot A({x}; {y}) and B({B[0]}; {B[1]}).','The learner selected an endpoint, not the half-way position.',f'Average x: ({x}+{B[0]})/2={M[0]}.',f'Average y: ({y}+{B[1]})/2={M[1]}.',f'Answer: {answer}. AM and MB have equal directed changes.']
   wrong=[f'M({B[0]}; {B[1]})',f'M({M[0]+1}; {M[1]})',f'M({M[0]}; {M[1]+1})'];values.update(points=[A,B],mode=mode,solution_point=M)
  else:
   dx=3+s%5;dy=sign*(2+(s//2)%5);B=[x+dx,y+dy];slope=Fraction(dy,dx)
   problem=f'A learner uses run/rise for A({x}; {y}), B({B[0]}; {B[1]}). Identify the first error and give the gradient.'
   answer=f'Use rise/run; m = {f(slope)}'
   actions=[f'Plot the two points A({x}; {y}) and B({B[0]}; {B[1]}).',f'Mark the run Δx={dx} and signed rise Δy={dy}.','The first error is reversing the fraction: the denominator is the run.',f'm=({dy})/{dx}={f(slope)}.',f'Answer: {answer}. Reversing both coordinate differences preserves it.']
   wrong=[f'm = {f(Fraction(dx,dy))}',f'm = {f(-slope)}',f'm = {f(slope+1)}'];values.update(points=[A,B],mode=mode,dx=dx,dy=dy)
 wrong=list(dict.fromkeys(w for w in wrong if w!=answer))
 for w in ('Not enough information','The sketch alone proves it','The result is twice the stated value'):
  if w!=answer and w not in wrong:wrong.append(w)
 wrong=wrong[:3]
 assert len(actions)==5 and len(wrong)==3 and len({answer,*wrong})==4,(n,i,answer,wrong)
 values['answer']=answer
 return {'id':f'g10-ag-l{n:02}-w{i:02}','problem':problem,'actions':actions,'answer':answer,'check':actions[-1],
  'visual':{'family':'grade10_analytical','values':values},'lesson':n,'wrong':wrong,
  'misconception':'Keep the coordinates and axis scales visible; derive each conclusion from exact differences.',
  'difficulty':'foundation' if i<=2 else 'easy' if i<=5 else 'standard' if i<=9 else 'intermediate' if i<=12 else 'exam'}
def option(n,i,variant,prefix):
 q=case(n,i,variant);opts=[q['answer'],*q['wrong']];pos=i%4;opts=opts[-pos:]+opts[:-pos] if pos else opts
 return {'id':f'g10-ag-l{n:02}-{prefix}{i:02}','prompt':q['problem'],'options':opts,'answer_index':pos,
  'memo':' '.join(q['actions']),'source':f'grade10-ag-lesson-{n:02}.md'}
def build():
 DOC.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True);manifest=[]
 for n,title in TITLES.items():
  worked=[{k:v for k,v in case(n,i).items() if k!='wrong'} for i in range(1,16)]
  data={'source':f'grade10-ag-lesson-{n:02}.md','worked':worked,
   'practice':[option(n,i,1,'p') for i in range(1,16)],
   'mastery':[option(n,i+15,2,'m') for i in range(1,6)],
   'reassessment':[option(n,i+20,3,'r') for i in range(1,4)]}
  assert len({q['problem'] for q in worked})==15
  lines=[f'# Grade 10 Topic 5 · Lesson {n}: {title}',f'Authority: [DBE Grade 10 Mathematics ATP]({ATP}), Term 2 Analytical Geometry. Original Athena examples.',
   'Status: teacher and browser review required. Plot the given points on the actual axis scale, retain earlier constructions and justify every coordinate deduction.']
  for q in worked:
   lines += [f'## {q["id"]}: {q["problem"]}',f'Visual contract: {json.dumps(q["visual"],ensure_ascii=False)}',
    *[f'{j}. {a}' for j,a in enumerate(q['actions'],1)],f'**Answer:** {q["answer"]}. **Misconception:** {q["misconception"]}']
  for label,key in [('Practice','practice'),('Mastery','mastery'),('Parallel reassessment','reassessment')]:
   lines.append(f'## {label} answer key')
   for q in data[key]:lines.append(f'- {q["id"]}: {q["prompt"]} Options: {" | ".join(q["options"])}. Correct: {q["options"][q["answer_index"]]}. {q["memo"]}')
  source=DOC/data['source'];source.write_text('\n\n'.join(lines)+'\n',encoding='utf-8')
  (OUT/f'analytical_{n:02}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  manifest.append({'lesson_id':f'g10-ag-{n:02}','source':source.name,'source_sha256':sha256(source.read_bytes()).hexdigest(),
   'worked':15,'practice':15,'mastery':5,'reassessment':3,'status':'teacher_review_required','teacher_approved':False,'browser_accepted':False})
 (DOC/'topic05-acceptance-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
 (DOC/'topic05-batch-acceptance.md').write_text(f'# Grade 10 Topic 5: Analytical Geometry\n\n[DBE Grade 10 Mathematics ATP]({ATP}) Term 2: Cartesian figures, distance, gradient, parallel/perpendicular and midpoint. Six lessons contain 90 worked, 90 four-choice practice, 30 mastery and 18 reassessments. Teacher and live browser acceptance remain pending.\n',encoding='utf-8')
if __name__=='__main__':build()
