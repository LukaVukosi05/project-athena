"""Original DBE-aligned Grade 9 3D geometry question sources; deterministic keys."""
import json
from hashlib import sha256
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/curriculum/grade9/geometry-of-3d-objects';OUT=ROOT/'backend/app/curriculum/grade9/generated'
ATP='https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2026%20ATPs/2026_ATP_Mathematics_Grade%209.pdf'
TITLES={1:'Platonic solids: faces, edges and vertices',2:'Spheres and cylinders: curved and flat surfaces',3:'Nets of cubes, prisms, pyramids and cylinders',4:'Identify a solid from its net and repair the first error'}
SOLIDS=[('tetrahedron',4,6,4,'triangles'),('cube',6,12,8,'squares'),('octahedron',8,12,6,'triangles'),('dodecahedron',12,30,20,'pentagons'),('icosahedron',20,30,12,'triangles')]
NETS=[('cube',6,6,0,0),('rectangular prism',6,0,0,0),('triangular prism',5,0,2,0),('square pyramid',5,1,4,0),('cylinder',3,0,0,2)]
# Fourth net field: squares; fifth triangles; sixth circular faces.
def net_parts(shape):
 if shape=='cube':return '6 equal squares'
 if shape=='rectangular prism':return '6 rectangles in three matching pairs'
 if shape=='triangular prism':return '3 rectangles and 2 matching triangles'
 if shape=='square pyramid':return '1 square and 4 matching triangles'
 return '1 rectangle and 2 matching circles'
def case(n,i,variant=0):
 k=i-1+variant*15;v={'lesson':n};wrong=[]
 if n==1:
  shape,F,E,V,face=SOLIDS[k%5];task=(k//5)%3
  target=['edges','vertices','faces'][task];result=[E,V,F][task]
  given=[f'{F} faces and {V} vertices',f'{F} faces and {E} edges',f'{V} vertices and {E} edges'][task]
  problem=f'A regular {shape} has {given}; all its faces are {face}. Find the number of {target} and verify using Euler’s relationship.'
  actions=[f'Identify the {shape}; its faces are congruent regular {face}.',f'Label the givens: {given}.',f'Use Euler’s relationship F + V = E + 2 with F = {F}, E = {E}, V = {V}.',f'Therefore the missing number of {target} is {result}.',f'Check: {F} + {V} = {E} + 2 = {F+V}.']
  answer=f'{target} = {result}';wrong=[f'{target} = {result+d}' for d in (-2,-1,1)]
  v.update(model='platonic',shape=shape,faces=F,edges=E,vertices=V,face_shape=face,target=target)
 elif n==2:
  kind=['sphere','cylinder','compare'][k%3];context=({'sphere':['a ball','a marble','a globe','a bead','a spherical tank'],'cylinder':['a tin','a drum','a closed pipe','a food can','a sealed container'],'compare':['a can','a drum','a closed pipe','a food tin','a container']}[kind])[k//3%5]
  if kind=='sphere':
   problem=f'For {context} modelled as a sphere, count its flat faces, curved surfaces, edges and vertices. Explain how it can roll.'
   actions=['Identify one continuous curved surface.','Check for flat faces: there are none.','Trace boundaries: there are no edges or vertices.','A sphere rolls in every direction because its whole surface curves.','Check: 0 flat faces, 1 curved surface, 0 edges, 0 vertices.']
   answer='sphere: 0 flat faces, 1 curved surface, 0 edges, 0 vertices'
   wrong=['sphere: 1 flat face, 1 curved surface, 0 edges, 0 vertices','sphere: 0 flat faces, 1 curved surface, 1 edge, 0 vertices','sphere: 0 flat faces, 1 curved surface, 0 edges, 1 vertex']
  elif kind=='cylinder':
   problem=f'For {context} modelled as a closed cylinder, count its flat circular faces, curved surfaces, curved edges and vertices.'
   actions=['Identify the top circular base.','Identify the matching bottom circular base.','Trace the lateral curved surface and its two circular boundary edges.','The two round boundaries are curved edges, not vertices.','Check: 2 flat circular faces, 1 curved surface, 2 curved edges, 0 vertices.']
   answer='cylinder: 2 flat circular faces, 1 curved surface, 2 curved edges, 0 vertices'
   wrong=['cylinder: 1 flat circular face, 1 curved surface, 2 curved edges, 0 vertices','cylinder: 2 flat circular faces, 1 curved surface, 1 curved edge, 0 vertices','cylinder: 2 flat circular faces, 1 curved surface, 2 curved edges, 2 vertices']
  else:
   problem=f'Compare a closed cylindrical {context} with a spherical model: which has circular flat faces, and which has no edges at all?'
   actions=['Place the sphere and closed cylinder side by side.','Mark the cylinder’s two flat circular bases.','Trace its two curved boundary edges.','The sphere has one uninterrupted curved surface with no edges.','Check: cylinder has flat circles; sphere has no edges.']
   answer='cylinder: circular flat faces; sphere: no edges'
   wrong=['sphere: circular flat faces; cylinder: no edges','both: circular flat faces; neither: edges','neither: circular flat faces; both: no edges']
  v.update(model=kind,context=context)
 elif n==3:
  shape,F,_,_,_=NETS[k%5];size=2+k//5;parts=net_parts(shape)
  problem=f'A {shape} is built from a net with one labelled edge of {size} cm. Name every face piece needed for the complete net before folding.'
  actions=[f'Identify the solid as a {shape}.',f'Find the base pieces; match each shared edge to the corresponding side.',f'Arrange side pieces beside their matching base edges. The net needs {parts}.',f'Count the complete net: {F} face pieces; fold adjacent matching edges.',f'Check that the folded net closes with {F} faces and no gap or overlap.']
  answer=f'{shape} net: {parts}';wrong=[f'{shape} net: {p}' for p in ({'cube':['5 equal squares','6 triangles','4 equal squares'],'rectangular prism':['5 rectangles','6 identical squares','4 rectangles'],'triangular prism':['3 rectangles and 1 triangle','2 rectangles and 2 triangles','3 rectangles and 3 triangles'],'square pyramid':['1 square and 3 triangles','2 squares and 4 triangles','1 triangle and 4 squares'],'cylinder':['1 rectangle and 1 circle','2 rectangles and 2 circles','1 rectangle and 3 circles']}[shape])]
  v.update(model='net',shape=shape,faces=F,scale=size,parts=parts,missing=False)
 else:
  shape,F,_,_,_=NETS[k%5];size=2+k//5;parts=net_parts(shape)
  observed={'cube':'5 equal squares','rectangular prism':'5 rectangles','triangular prism':'3 rectangles and 1 triangle','square pyramid':'1 square and 3 triangles','cylinder':'1 rectangle and 1 circle'}[shape]
  missing={'cube':'one matching square','rectangular prism':'one matching rectangle','triangular prism':'one matching triangle','square pyramid':'one matching triangle','cylinder':'one matching circle'}[shape]
  problem=f'A learner draws a net for a {shape} with one edge labelled {size} cm with {observed}. Find the first missing face and repair the net.'
  actions=[f'Check the learner’s proposed {shape} net: {observed}.',f'Compare the net with the solid: it should have {F} face pieces.',f'The first error is that {missing} is absent; the net cannot close.',f'Add {missing} on a matching free edge; a complete net has {parts}.',f'Check the repaired net closes as a {shape} with {F} face pieces.']
  answer=f'missing {missing}; complete net: {parts}'
  wrong=[f'missing {x}; complete net: {parts}' for x in ('a vertex','one curved edge','two extra faces')]
  v.update(model='net_error',shape=shape,faces=F,scale=size,parts=parts,observed=observed,missing=missing)
 assert len(set([answer,*wrong]))==4,(n,i,variant)
 return {'id':f'g9-solid-l{n:02}-w{i:02}' if not variant else f'g9-solid-l{n:02}-v{variant}-w{i:02}','problem':problem,'actions':actions,'answer':answer,'check':actions[-1],'visual':{'family':'solids','values':v},'lesson':n,'misconception':'Count actual face pieces and their joining edges; keep curved surfaces distinct from flat faces.' ,'wrong':wrong}
def choice(n,i,variant,prefix):
 c=case(n,i,variant);opts=[c['answer'],*c['wrong']];pos=i%4;opts=opts[4-pos:]+opts[:4-pos] if pos else opts
 return {'id':f'g9-solid-l{n:02}-{prefix}{i:02}','prompt':c['problem'],'options':opts,'answer_index':pos,'memo':' '.join(c['actions']),'source':f'lesson-{n:02}.md'}
def build():
 DOC.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True);manifest=[]
 for n,title in TITLES.items():
  worked=[{k:v for k,v in case(n,i).items() if k!='wrong'}|{'difficulty':'foundation' if i<=2 else 'easy' if i<=5 else 'standard' if i<=9 else 'intermediate' if i<=12 else 'exam'} for i in range(1,16)]
  data={'source':f'lesson-{n:02}.md','worked':worked,'practice':[choice(n,i,1,'p') for i in range(1,16)],'mastery':[choice(n,i+15,2,'m') for i in range(1,6)],'reassessment':[choice(n,i+18,3,'r') for i in range(1,4)]}
  lines=[f'# Grade 9 Topic 14 · Lesson {n}: {title}',f'Authority: [DBE 2026 Grade 9 Mathematics ATP]({ATP}), Term 4. Original Athena questions.','Status: teacher and browser review required. Each operation updates the net/solid and a cumulative written solution.']
  for c in worked:lines.extend([f'## {c["id"]}: {c["problem"]}',f'Visual: {json.dumps(c["visual"],ensure_ascii=False)}',*[f'{j}. {step}' for j,step in enumerate(c['actions'],1)],f'**Answer:** {c["answer"]}. **Misconception:** {c["misconception"]}'])
  for label,key in [('Practice','practice'),('Mastery','mastery'),('Parallel reassessment','reassessment')]:
   lines.append(f'## {label} answer key')
   for c in data[key]:lines.append(f'- {c["id"]}: {c["prompt"]} Options: {" | ".join(c["options"])}. Correct: {c["options"][c["answer_index"]]}. {c["memo"]}')
  source=DOC/data['source'];source.write_text('\n\n'.join(lines)+'\n',encoding='utf-8');(OUT/f'geometry_3d_{n:02}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  manifest.append({'lesson_id':f'g9-solid-{n:02}','source':source.name,'source_sha256':sha256(source.read_bytes()).hexdigest(),'worked':15,'practice':15,'mastery':5,'reassessment':3,'status':'teacher_review_required','teacher_approved':False,'browser_accepted':False})
 (DOC/'topic14-acceptance-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
 (DOC/'topic14-batch-acceptance.md').write_text(f'# Grade 9 Topic 14: Geometry of 3D Objects\n\n[DBE 2026 Grade 9 Mathematics ATP, Term 4]({ATP}) covers Platonic solids, spheres, cylinders and nets of cubes, prisms, pyramids and cylinders. Four Athena lessons contain 60 worked examples, 60 practice items, 20 mastery items and 12 reassessments. Teacher and browser acceptance remain required.\n',encoding='utf-8')
if __name__=='__main__':build()
