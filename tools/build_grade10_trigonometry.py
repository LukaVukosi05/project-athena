"""Original Grade 10 trigonometry examples aligned to DBE Term 1 ATP."""
import json
import math
from hashlib import sha256
from pathlib import Path
from fractions import Fraction

ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/curriculum/grade10/trigonometry'
OUT=ROOT/'backend/app/curriculum/grade10/generated'
ATP='https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2023%20ATPs/FET%20Content%20Subjects/Grade%2010/1.580%20ATP%202023-24%20Gr%2010%20Maths%20final.pdf'
TITLES={1:'Opposite, adjacent and hypotenuse: sine, cosine and tangent',
 2:'Quadrants and reference angles from 0° to 360°',
 3:'Reciprocal ratios cosec, sec and cot',
 4:'Exact ratios at 0°, 30°, 45°, 60° and 90°',
 5:'Two-dimensional right-triangle applications',
 6:'Solve acute-angle trigonometric equations',
 7:'Coordinate diagrams and signed ratios through 360°'}
TRIPLES=[(3,4,5),(5,12,13),(8,15,17),(7,24,25),(20,21,29)]
SPECIAL={0:('0','1','0'),30:('1/2','√3/2','√3/3'),45:('√2/2','√2/2','1'),
 60:('√3/2','1/2','√3'),90:('1','0','undefined')}
def frac(a,b):return str(Fraction(a,b))
def sign_text(value,negative):return value if value in ('0','undefined') or not negative else '−'+value
def special_angle(deg,fn):
 if deg%90==0:
  table={0:('0','1','0'),90:('1','0','undefined'),180:('0','−1','0'),270:('−1','0','undefined')}
  return table[deg][{'sin':0,'cos':1,'tan':2}[fn]]
 ref=deg%180;ref=ref if ref<=90 else 180-ref
 val=SPECIAL[ref][{'sin':0,'cos':1,'tan':2}[fn]]
 return sign_text(val,((deg>180) if fn=='sin' else (90<deg<270) if fn=='cos' else 90<deg<180 or 270<deg<360))
def case(n,i,variant=0):
 s=i+15*variant
 x,y,h=TRIPLES[(s-1)%5];scale=1+(s-1)//5;x*=scale;y*=scale;h*=scale
 v={'lesson':n,'family':'grade10_trigonometry','opposite':x,'adjacent':y,'hypotenuse':h,'orientation':'opposite-vertical' if s%2 else 'opposite-horizontal'}
 if n==1:
  fn=['sin','cos','tan'][(s-1)%3];num=y if fn=='cos' else x;den=h if fn!='tan' else y
  problem=f'In right triangle ABC, ∠B=90°, the side opposite ∠A is {x} cm and adjacent is {y} cm. Find {fn} A exactly.'
  value=frac(num,den);ans=f'{fn} A = {value}'
  actions=[f'Mark ∠B=90° and identify ∠A as the reference angle.',f'Label the side opposite A {x} cm and the adjacent side {y} cm.',f'Find the hypotenuse: √({x}²+{y}²) = {h} cm.',f'Use {fn} A = {"opposite/hypotenuse" if fn=="sin" else "adjacent/hypotenuse" if fn=="cos" else "opposite/adjacent"} = {num}/{den}.',f'Answer: {ans}. Check {x}²+{y}²={h}².']
  wrong=[f'{fn} A = {frac(y,h)}',f'{fn} A = {frac(x,h)}',f'{fn} A = {frac(h,num)}']
  v.update(model='triangle',fn=fn,numerator=num,denominator=den)
 elif n==2:
  angles=[30,45,60,120,135,150,210,225,240,300,315,330,0,90,180]
  deg=angles[(s-1)%15];fn=['sin','cos','tan'][(s-1+variant)%3]
  if deg in (90,270) and fn=='tan':fn='sin'
  val=special_angle(deg,fn);ans=f'{fn} {deg}° = {val}'
  problem=f'Use the unit circle to find the exact value of {fn} {deg}° and identify its quadrant or axis.'
  quadrant='positive x-axis' if deg==0 else 'positive y-axis' if deg==90 else 'negative x-axis' if deg==180 else f'quadrant {1+deg//90}'
  ref=min(deg%180,180-deg%180)
  actions=[f'Draw coordinate axes and turn counterclockwise from the positive x-axis to {deg}°.',f'Mark the terminal side in {quadrant}.',f'The reference angle is {ref}°; use its special-angle ratio.',f'Apply the sign of {fn} in {quadrant}: {val}.',f'Answer: {ans}. Confirm the sign on the coordinate axes.']
  wrong=[f'{fn} {deg}° = {other}' for other in ('1/2','−1/2','0','1','−1','√3/2','−√3/2','√2/2','−√2/2','undefined') if other!=val][:3]
  v.update(model='circle',degree=deg,fn=fn,quadrant=quadrant,reference=ref)
 elif n==3:
  fn=['cosec','sec','cot'][(s-1)%3];num=h if fn in ('cosec','sec') else y;den=x if fn=='cosec' else y if fn=='sec' else x
  val=frac(num,den);ans=f'{fn} A = {val}'
  problem=f'Right triangle ABC has opposite side {x} cm, adjacent side {y} cm and angle A acute. Find {fn} A exactly.'
  base='sin' if fn=='cosec' else 'cos' if fn=='sec' else 'tan'
  actions=[f'Mark the angle A and label opposite {x} cm and adjacent {y} cm.',f'Calculate the hypotenuse √({x}²+{y}²)={h} cm.',f'Write {base} A as a ratio of the labelled sides.',f'Invert that ratio: {fn} A = {num}/{den}.',f'Answer: {ans}. Multiply {fn} A by {base} A to obtain 1.']
  wrong=[f'{fn} A = {frac(x,h)}',f'{fn} A = {frac(y,h)}',f'{fn} A = {frac(den,num)}']
  v.update(model='triangle',fn=fn,numerator=num,denominator=den)
 elif n==4:
  deg=[0,30,45,60,90][(s-1)%5];fn=['sin','cos','tan'][((s-1)//5+variant)%3]
  val=SPECIAL[deg][['sin','cos','tan'].index(fn)]
  problem=f'Derive {fn} {deg}° exactly without a calculator; explain the special triangle or axis.'
  ans=f'{fn} {deg}° = {val}'
  reference='unit-circle axis' if deg in (0,90) else '45°-45°-90° triangle with sides 1, 1, √2' if deg==45 else '30°-60°-90° triangle with sides 1, √3, 2'
  actions=[f'Draw the {reference}.',f'Mark {deg}° at the appropriate vertex or axis.',f'Label opposite, adjacent and hypotenuse relative to {deg}°.',f'Use {fn} = {"opposite/hypotenuse" if fn=="sin" else "adjacent/hypotenuse" if fn=="cos" else "opposite/adjacent"}; here the value is {val}.',f'Answer: {ans}. Check against the labelled special triangle or unit-circle point.']
  wrong=[f'{fn} {deg}° = {other}' for other in ('0','1','1/2','√2/2','√3/2','√3','undefined') if other!=val][:3]
  v.update(model='special',degree=deg,fn=fn,reference=reference)
 elif n==5:
  context=['ladder leaning against a wall','ramp rising to a platform','guy rope attached to a pole','viewing line to a tower','support cable to a mast'][(s-1)%5]
  angle=math.degrees(math.atan2(x,y));rounded=f'{angle:.1f}';ans=f'θ ≈ {rounded}°'
  problem=f'A {context} forms a right triangle: vertical rise {x} m and horizontal run {y} m. Find the angle θ to the ground to one decimal place.'
  actions=[f'Draw and label the rise {x} m, run {y} m and ground angle θ.',f'Check the hypotenuse: √({x}²+{y}²)={h} m.',f'The rise is opposite θ and the run adjacent: tan θ={x}/{y}.',f'Apply inverse tangent: θ=arctan({x}/{y})≈{angle:.4f}°.',f'Answer: {ans}. The angle is acute and the given rise/run ratio matches tan θ.']
  wrong=[f'θ ≈ {math.degrees(math.atan2(y,x)):.1f}°',f'θ ≈ {angle+10:.1f}°',f'θ ≈ {angle-10:.1f}°']
  v.update(model='application',angle=float(rounded),context=context)
 elif n==6:
  deg=[30,45,60][(s-1)%3];fn=['sin','cos','tan'][((s-1)//3+variant)%3]
  k=1+(s-1)//9
  base=SPECIAL[deg][['sin','cos','tan'].index(fn)]
  mul={'1/2':str(k)+'/2' if k>1 else '1/2','√3/2':f'{k}√3/2' if k>1 else '√3/2','√2/2':f'{k}√2/2' if k>1 else '√2/2','√3/3':f'{k}√3/3' if k>1 else '√3/3','1':str(k),'√3':f'{k}√3' if k>1 else '√3'}
  rhs=mul[base]
  problem=f'Solve {k}{fn} θ = {rhs} for 0° ≤ θ ≤ 90°; give the angle exactly.'
  ans=f'θ = {deg}°'
  actions=[f'Identify the unknown acute or endpoint angle θ in {k}{fn} θ = {rhs}.',f'Divide both sides by {k}: {fn} θ = {base}.',f'Compare with the exact special-angle ratios.',f'The unique angle in 0° to 90° matching {fn} θ={base} is {deg}°.',f'Answer: {ans}. Substitute θ={deg}°: {k}×{base}={rhs}.']
  wrong=[f'θ = {other}°' for other in (0,30,45,60,90) if other!=deg][:3]
  v.update(model='solve',degree=deg,fn=fn,multiplier=k,ratio=base)
 else:
  sx=-1 if s%2 else 1;sy=-1 if s%3==0 else 1
  px=sx*y;py=sy*x;rad=h
  sin=frac(py,rad);cos=frac(px,rad);tan=frac(py,px)
  problem=f'A terminal side passes through P({px}, {py}). Determine sin θ, cos θ and tan θ exactly, where 0° ≤ θ < 360°.'
  ans=f'sin θ = {sin}; cos θ = {cos}; tan θ = {tan}'
  actions=[f'Plot P({px}, {py}) on fixed Cartesian axes and join it to O(0,0).',f'Construct the reference right triangle with horizontal {abs(px)} and vertical {abs(py)}.',f'Calculate r=√({px}²+{py}²)={rad}.',f'Use signed coordinates: sin θ={py}/{rad}, cos θ={px}/{rad}, tan θ={py}/{px}.',f'Answer: {ans}. Verify tan θ = sin θ / cos θ.']
  wrong=[f'sin θ = {frac(-py,rad)}; cos θ = {cos}; tan θ = {tan}',f'sin θ = {sin}; cos θ = {frac(-px,rad)}; tan θ = {tan}',f'sin θ = {sin}; cos θ = {cos}; tan θ = {frac(-py,px)}']
  v.update(model='coordinate',point=[px,py],radius=rad,sin=sin,cos=cos,tan=tan)
 # Preserve four distinguishable answer options even for coincident distractors.
 wrong=list(dict.fromkeys(value for value in wrong if value!=ans))
 for alt in ([f'{fn} A = {value}' for value in (frac(x,y),frac(y,x),frac(h,y),frac(h,x),'0','1')] if n in (1,3)
             else [f'θ = {angle}°' for angle in (0,30,45,60,90)] if n==6
             else [f'{ans} (wrong unit)',f'{ans} (opposite sign)',f'{ans} (missing branch)']):
  if len(wrong)>=3:break
  if alt!=ans and alt not in wrong:wrong.append(alt)
 assert len(actions)==5 and len({ans,*wrong[:3]})==4,(n,i,wrong)
 v['answer']=ans
 return {'id':f'g10-trig-l{n:02}-w{i:02}' if not variant else f'g10-trig-l{n:02}-v{variant}-w{i:02}',
  'problem':problem,'actions':actions,'answer':ans,'check':actions[-1],
  'visual':{'family':'grade10_trigonometry','values':v},'lesson':n,
  'misconception':'Identify the marked reference angle, keep coordinate signs and test the original condition.',
  'wrong':wrong[:3],'difficulty':'foundation' if i<=2 else 'easy' if i<=5 else 'standard' if i<=9 else 'intermediate' if i<=12 else 'exam'}
def choice(n,i,variant,prefix):
 q=case(n,i,variant);options=[q['answer'],*q['wrong']];pos=i%4
 options=options[-pos:]+options[:-pos] if pos else options
 return {'id':f'g10-trig-l{n:02}-{prefix}{i:02}','prompt':q['problem'],
  'options':options,'answer_index':pos,'memo':' '.join(q['actions']),
  'source':f'grade10-trig-lesson-{n:02}.md'}
def build():
 DOC.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True);manifest=[]
 for n,title in TITLES.items():
  worked=[{k:v for k,v in case(n,i).items() if k!='wrong'} for i in range(1,16)]
  data={'source':f'grade10-trig-lesson-{n:02}.md','worked':worked,
   'practice':[choice(n,i,1,'p') for i in range(1,16)],
   'mastery':[choice(n,i+15,2,'m') for i in range(1,6)],
   'reassessment':[choice(n,i+20,3,'r') for i in range(1,4)]}
  assert len({q['problem'] for q in worked})>=10,n
  lines=[f'# Grade 10 Topic 3 · Lesson {n}: {title}',
   f'Authority: [DBE Grade 10 Mathematics ATP]({ATP}), Term 1. Original Athena questions.',
   'Status: teacher and live browser review required. Retain the same angle, side labels, axes and written record through every stage.']
  for q in worked:lines += [f'## {q["id"]}: {q["problem"]}',f'Visual contract: {json.dumps(q["visual"],ensure_ascii=False)}',
   *[f'{j}. {a}' for j,a in enumerate(q['actions'],1)],f'**Answer:** {q["answer"]}. **Misconception:** {q["misconception"]}']
  for label,key in [('Practice','practice'),('Mastery','mastery'),('Parallel reassessment','reassessment')]:
   lines.append(f'## {label} answer key')
   for q in data[key]:lines.append(f'- {q["id"]}: {q["prompt"]} Options: {" | ".join(q["options"])}. Correct: {q["options"][q["answer_index"]]}. {q["memo"]}')
  source=DOC/data['source'];source.write_text('\n\n'.join(lines)+'\n',encoding='utf-8')
  (OUT/f'trig_{n:02}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  manifest.append({'lesson_id':f'g10-trig-{n:02}','source':source.name,'source_sha256':sha256(source.read_bytes()).hexdigest(),
   'worked':15,'practice':15,'mastery':5,'reassessment':3,'status':'teacher_review_required','teacher_approved':False,'browser_accepted':False})
 (DOC/'topic03-acceptance-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
 (DOC/'topic03-batch-acceptance.md').write_text(f'# Grade 10 Topic 3: Trigonometry\n\n[DBE Grade 10 Mathematics ATP]({ATP}) Term 1 lists right-triangle ratios, signed values through 360°, reciprocals, exact special angles, two-dimensional applications, acute-angle equations, and diagram-based values. Seven authored lessons contain 105 worked, 105 four-choice practice, 35 mastery and 21 reassessment questions. These are source-backed previews; mathematical teacher review and live browser acceptance remain pending.\n',encoding='utf-8')
if __name__=='__main__':build()
