"""Original, deterministic Grade 9 transformation geometry questions."""
import json
from pathlib import Path
from hashlib import sha256
ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/curriculum/grade9/transformation-geometry'
OUT=ROOT/'backend/app/curriculum/grade9/generated'
ATP='https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2026%20ATPs/2026_ATP_Mathematics_Grade%209.pdf'
TITLES={1:'Coordinates and translations across quadrants',2:'Reflections in the coordinate axes',3:'Reflection in the line y = x',4:'Quarter-turn rotations around a given centre',5:'Infer a transformation from image coordinates',6:'Enlargement, reduction, perimeter and area',7:'Combined transformations and first-error reassessment'}
def fmt(points):return ', '.join(f'{name}({x:g}, {y:g})' for name,(x,y) in zip('ABC',points))
def transform(pts,kind,dx=0,dy=0,c=(0,0),k=1):
 out=[]
 for x,y in pts:
  if kind=='translate':out.append((x+dx,y+dy))
  elif kind=='reflect_x':out.append((x,-y))
  elif kind=='reflect_y':out.append((-x,y))
  elif kind=='reflect_diag':out.append((y,x))
  elif kind=='rotate_ccw':out.append((c[0]-(y-c[1]),c[1]+(x-c[0])))
  elif kind=='rotate_cw':out.append((c[0]+(y-c[1]),c[1]-(x-c[0])))
  elif kind=='enlarge':out.append((c[0]+k*(x-c[0]),c[1]+k*(y-c[1])))
 return out

def case(n,i,variant=0):
 s=i+variant*15;a=(s%5)-2;b=(s%4)-2;w=2+s%3;h=2+(s//3)%3
 pts=[(a,b),(a+w,b),(a,b+h)]
 if n==1:kind='translate';dx=2+s%3;dy=-(2+(s//2)%3);rule=f'translation by ({dx}, {dy})';c=(0,0);k=1
 elif n==2:kind='reflect_x' if s%2 else 'reflect_y';dx=dy=0;rule=f'reflection in the {"x" if kind=="reflect_x" else "y"}-axis';c=(0,0);k=1
 elif n==3:kind='reflect_diag';dx=dy=0;rule='reflection in y = x';c=(0,0);k=1
 elif n==4:kind='rotate_ccw' if s%2 else 'rotate_cw';dx=dy=0;c=((s%3)-1,((s//3)%3)-1);k=1;rule=f'90° {"anticlockwise" if kind=="rotate_ccw" else "clockwise"} rotation around {c}'
 elif n==5:
  kind=['translate','reflect_x','reflect_y','reflect_diag','rotate_ccw'][(s-1)%5];dx=2+s%2 if kind=='translate' else 0;dy=-2 if kind=='translate' else 0;c=(0,0);k=1;rule={'translate':f'translation by ({dx}, {dy})','reflect_x':'reflection in the x-axis','reflect_y':'reflection in the y-axis','reflect_diag':'reflection in y = x','rotate_ccw':'90° anticlockwise rotation about the origin'}[kind]
 elif n==6:kind='enlarge';dx=dy=0;c=((s%3)-1,((s//3)%3)-1);k=2 if s%2 else 0.5;rule=f'enlargement with centre {c} and scale factor {k:g}'
 else:
  kind=['reflect_x','translate','enlarge','rotate_cw','reflect_diag'][(s-1)%5];dx=3 if kind=='translate' else 0;dy=-2 if kind=='translate' else 0;c=(0,0) if kind!='enlarge' else (1,-1);k=2 if kind=='enlarge' else 1
  rule={'reflect_x':'reflection in the x-axis','translate':f'translation by ({dx}, {dy})','enlarge':f'enlargement with centre {c} and scale factor 2','rotate_cw':'90° clockwise rotation about the origin','reflect_diag':'reflection in y = x'}[kind]
 image=transform(pts,kind,dx,dy,c,k)
 def pf(q):return f'({q[0]:g}, {q[1]:g})'
 original=fmt(pts);im=fmt(image).replace('A(','A′(').replace('B(','B′(').replace('C(','C′(')
 if n==5:problem=f'Triangle {original} has image {im}. Identify the single transformation and verify it on all vertices.'
 elif n==7:problem=f'A learner transforms triangle {original} by {rule} but changes only the x-coordinate of B. Identify the first error and give the correct image.'
 else:problem=f'Triangle {original} is transformed by {rule}. Plot the image and give its vertex coordinates.'
 if kind=='translate':mapping=f'Add {dx} to x and {dy} to y at every vertex.'
 elif kind=='reflect_x':mapping='Keep x; reverse the sign of y for every vertex.'
 elif kind=='reflect_y':mapping='Reverse the sign of x; keep y for every vertex.'
 elif kind=='reflect_diag':mapping='Swap x and y for every vertex; the line y = x stays fixed.'
 elif kind=='rotate_ccw':mapping=f'Subtract centre {c}, turn each relative (x, y) into (−y, x), then add the centre.'
 elif kind=='rotate_cw':mapping=f'Subtract centre {c}, turn each relative (x, y) into (y, −x), then add the centre.'
 else:mapping=f'From centre {c}, multiply both coordinate offsets by {k:g}; then add the centre.'
 actions=[f'Plot and label the original vertices {original} on one fixed set of axes.',f'Mark the {rule}; {mapping}',f'Map A {pf(pts[0])} to A′{pf(image[0])}; retain A and A′.',f'Map B {pf(pts[1])} to B′{pf(image[1])} and C {pf(pts[2])} to C′{pf(image[2])}; join A′B′C′.',f'Check the coordinate rule on all three vertices; image {im}.']
 if n==5:actions[1]=f'Compare A and A′, then B and B′: the rule is {rule}. {mapping}'
 if n==7:actions[1]=f'First error: changing only B’s x-coordinate does not apply {rule} to every vertex. {mapping}'
 if n==6:
  perimeter=2*(w+h+(w*w+h*h)**.5);area=w*h/2
  actions[-1]=f'Perimeter changes by factor {k:g} and area by factor {k*k:g}; original area {area:g} square units, image area {area*k*k:g} square units. Image {im}.'
  answer=f'{im}; perimeter factor {k:g}; area factor {k*k:g}'
 else:answer=f'{rule}; {im}' if n in (5,7) else im
 wrong=[]
 for shift in (1,2,-1):
  altered=[(x+shift,y) for x,y in image];base=fmt(altered).replace('A(','A′(').replace('B(','B′(').replace('C(','C′(')
  wrong.append(f'{base}; perimeter factor {k:g}; area factor {k*k:g}' if n==6 else f'{rule}; {base}' if n in (5,7) else base)
 assert len({answer,*wrong})==4
 values={'lesson':n,'kind':kind,'original':pts,'image':image,'dx':dx,'dy':dy,'centre':c,'factor':k,'rule':rule,'model':'coordinate_transform','original_area':w*h/2 if n==6 else None}
 return {'id':f'g9-tg-l{n:02}-w{i:02}' if not variant else f'g9-tg-l{n:02}-v{variant}-w{i:02}','problem':problem,'actions':actions,'answer':answer,'check':actions[-1],'visual':{'family':'transformation','values':values},'lesson':n,'misconception':'Apply the same rule to both coordinates of every vertex; check the centre, axis and scale.','wrong':wrong}
def choice(n,i,variant,prefix):
 q=case(n,i,variant);opts=[q['answer'],*q['wrong']];p=i%4;opts=opts[4-p:]+opts[:4-p] if p else opts
 return {'id':f'g9-tg-l{n:02}-{prefix}{i:02}','prompt':q['problem'],'options':opts,'answer_index':p,'memo':' '.join(q['actions']),'source':f'lesson-{n:02}.md'}
def build():
 DOC.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True);manifest=[]
 for n,title in TITLES.items():
  worked=[{key:val for key,val in case(n,i).items() if key!='wrong'}|{'difficulty':'foundation' if i<=2 else 'easy' if i<=5 else 'standard' if i<=9 else 'intermediate' if i<=12 else 'exam'} for i in range(1,16)]
  data={'source':f'lesson-{n:02}.md','worked':worked,'practice':[choice(n,i,1,'p') for i in range(1,16)],'mastery':[choice(n,i+15,2,'m') for i in range(1,6)],'reassessment':[choice(n,i+18,3,'r') for i in range(1,4)]}
  lines=[f'# Grade 9 Topic 16 · Lesson {n}: {title}',f'Authority: [DBE 2026 Grade 9 Mathematics ATP]({ATP}), Term 4. Original Athena questions.','Status: teacher and browser review required. Plot each original and image vertex on stable axes; never display the final image initially.']
  for q in worked:lines.extend([f'## {q["id"]}: {q["problem"]}',f'Visual: {json.dumps(q["visual"],ensure_ascii=False)}',*[f'{j}. {a}' for j,a in enumerate(q['actions'],1)],f'**Answer:** {q["answer"]}. **Misconception:** {q["misconception"]}'])
  for label,key in [('Practice','practice'),('Mastery','mastery'),('Parallel reassessment','reassessment')]:
   lines.append(f'## {label} answer key')
   for q in data[key]:lines.append(f'- {q["id"]}: {q["prompt"]} Options: {" | ".join(q["options"])}. Correct: {q["options"][q["answer_index"]]}. {q["memo"]}')
  source=DOC/data['source'];source.write_text('\n\n'.join(lines)+'\n',encoding='utf-8');(OUT/f'transformation_{n:02}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  manifest.append({'lesson_id':f'g9-tg-{n:02}','source':source.name,'source_sha256':sha256(source.read_bytes()).hexdigest(),'worked':15,'practice':15,'mastery':5,'reassessment':3,'status':'teacher_review_required','teacher_approved':False,'browser_accepted':False})
 (DOC/'topic16-acceptance-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
 (DOC/'topic16-batch-acceptance.md').write_text(f'# Grade 9 Topic 16: Transformation Geometry\n\n[DBE 2026 Grade 9 Mathematics ATP, Term 4]({ATP}) includes translation across quadrants, reflection in coordinate axes and y=x, rotation around a given centre, identifying an image transformation, and enlargement/reduction with perimeter and area effects. Seven authored lessons contain 105 worked examples, 105 four-choice practice, 35 mastery and 21 reassessments. Teacher mathematical review and desktop/mobile browser acceptance remain required.\n',encoding='utf-8')
if __name__=='__main__':build()
