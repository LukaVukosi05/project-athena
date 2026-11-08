"""Original Grade 10 Euclidean Geometry examples grounded in the DBE Term 2 ATP."""
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import json
import math

ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/curriculum/grade10/euclidean-geometry'
OUT=ROOT/'backend/app/curriculum/grade10/generated'
ATP='https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2023%20ATPs/FET%20Content%20Subjects/Grade%2010/1.580%20ATP%202023-24%20Gr%2010%20Maths%20final.pdf'
TITLES={1:'Intersecting and parallel line angle reasons',
 2:'Congruent and similar triangles with matching vertices',
 3:'Properties of kites, parallelograms and trapeziums',
 4:'Rectangle, rhombus and square diagonals and areas',
 5:'The midpoint theorem in triangles',
 6:'Mixed geometric riders and first-error repair'}
def fmt(x):return str(x) if not isinstance(x,Fraction) or x.denominator==1 else f'{x.numerator}/{x.denominator}'
def case(n,i,variant=0):
 s=i+15*variant;a=2+s%13;b=3+(s//2)%11;c=4+(s//3)%9
 v={'lesson':n,'a':a,'b':b,'c':c}
 if n==1:
  theta=25+(s*11)%135;model='intersect' if s%2 else 'parallel'
  if model=='intersect':
   target='vertically opposite' if s%4==1 else 'adjacent on a straight line'
   value=theta if target=='vertically opposite' else 180-theta
   problem=f'Two straight lines AB and CD intersect at O. ∠AOC={theta}°. Find x, the {target} angle, and give a reason.'
   actions=[f'Locate ∠AOC={theta}° and the marked x at intersection O.',
    f'The relevant relationship is {target}.',
    f'Write x={theta}°.' if target=='vertically opposite' else f'Write x+{theta}°=180° because adjacent angles form a straight line.',
    f'Solve: x={value}°.',f'Answer: x={value}° ({target} angles). Check the full turn around O is 360°.']
  else:
   target='alternate interior' if s%4==0 else 'co-interior'
   value=theta if target=='alternate interior' else 180-theta
   problem=f'Parallel lines p ∥ q are cut by transversal t. A marked interior angle is {theta}°. Find x, its {target} partner, with a reason.'
   actions=[f'Mark p ∥ q and locate the angle {theta}° at the first crossing.',
    f'Trace the transversal to the marked {target} partner at the second crossing.',
    f'Use alternate angles on parallels: x={theta}°.' if target=='alternate interior' else f'Use co-interior angles on parallels: x+{theta}°=180°.',
    f'Solve: x={value}°.',f'Answer: x={value}° ({target}, p ∥ q).']
  ans=f'x = {value}°';wrong=[f'x = {180-value}°',f'x = {value+10}°',f'x = {value-10}°']
  v.update(model=model,given_angle=theta,target=target,result=value)
 elif n==2:
  mode=['sss','sas','asa','aa','similar_sas'][(s-1)%5];k=2+(s//5)%5
  if mode=='sss':
   p,q,r=3*k,4*k,5*k
   v.update(side_ab=p,side_ac=r,side_bc=q,side_de=p,side_df=r,side_ef=q)
   problem=f'In ΔABC and ΔDEF, AB=DE={p} cm, BC=EF={q} cm and AC=DF={r} cm. State the congruence criterion and the corresponding side to AC.'
   ans=f'SSS; DF = {r} cm'
   actions=['Draw both triangles with A↔D, B↔E, C↔F.',f'Mark AB=DE={p} and BC=EF={q}.',f'Mark AC=DF={r}: all three corresponding sides match.','Conclude ΔABC ≅ ΔDEF by SSS.',f'Answer: {ans}. Correspondence AC↔DF follows from A↔D and C↔F.']
   wrong=[f'SAS; DF = {r} cm',f'SSS; EF = {r} cm',f'SSS; DF = {q} cm']
  elif mode=='sas':
   angle=35+5*(s%10);p,q=a+2,b+3
   v.update(side_ab=p,side_ac=q,side_de=p,side_df=q)
   problem=f'In ΔABC and ΔDEF, AB=DE={p} cm, AC=DF={q} cm, and included ∠A=∠D={angle}°. State the congruence criterion and matching angle.'
   ans=f'SAS; ∠A corresponds to ∠D ({angle}°)'
   actions=['Draw the two triangles with A↔D, B↔E and C↔F.',f'Mark AB=DE={p} and AC=DF={q}.',f'Mark the INCLUDED ∠A=∠D={angle}° between those pairs of sides.','Conclude ΔABC ≅ ΔDEF by SAS.',f'Answer: {ans}. The marked angle lies between the two marked sides.']
   wrong=[f'SSA; ∠A corresponds to ∠D ({angle}°)',f'SAS; ∠A corresponds to ∠E ({angle}°)',f'AA; ∠A corresponds to ∠D ({angle}°)']
   v.update(angle=angle)
  elif mode=='asa':
   x=35+5*(s%7);y=50+5*(s%6);p=a+4
   v.update(side_ab=p,side_de=p)
   problem=f'In ΔABC and ΔDEF, ∠A=∠D={x}°, ∠B=∠E={y}°, and included AB=DE={p} cm. State the congruence criterion.'
   ans='ASA congruence'
   actions=['Draw the triangles in the correspondence A↔D, B↔E, C↔F.',f'Mark equal angles {x}° at A,D and {y}° at B,E.',f'Mark the side AB=DE={p} between those angles.','Two angles and the included side agree: ASA.',f'Answer: {ans}. This establishes the entire triangles, not merely similarity.']
   wrong=['AA similarity','SSA congruence','SSS congruence'];v.update(angle=x,second_angle=y)
  elif mode=='aa':
   x=30+5*(s%8);y=40+5*(s%6)
   problem=f'In ΔABC and ΔDEF, ∠A=∠D={x}° and ∠B=∠E={y}°. State whether similarity or congruence follows, and give the criterion.'
   ans='Similar by AA; congruence is not established'
   actions=['Mark the A↔D and B↔E angle correspondences.',f'The third angle in each triangle is 180°−{x}°−{y}°={180-x-y}°.', 'Two corresponding angles are equal, giving the same shape.','No equal side lengths have been supplied, so size equality is unproved.',f'Answer: {ans}. Check the third-angle sum in both triangles.']
   wrong=['Congruent by AA','Congruent by SAS','Not similar'];v.update(angle=x,second_angle=y)
  else:
   p=a+3;q=b+2;scale=2+s%3
   v.update(side_ab=p,side_ac=q,side_de=p*scale,side_df=q*scale)
   problem=f'ΔABC and ΔDEF have ∠A=∠D={35+5*(s%8)}°, AB={p}, AC={q}, DE={p*scale}, DF={q*scale}. Find the enlargement factor ABC→DEF and the similarity reason.'
   ans=f'scale factor {scale}; SAS similarity'
   actions=['Mark the included angles at A and D equal.',f'Compute DE/AB={p*scale}/{p}={scale}.',f'Compute DF/AC={q*scale}/{q}={scale}.','Two corresponding sides have the same scale with equal included angle: SAS similarity.',f'Answer: {ans}. Correspondence A↔D, B↔E, C↔F.']
   wrong=[f'scale factor {scale+1}; SAS similarity',f'scale factor {scale}; SSS congruence',f'scale factor 1/{scale}; SAS similarity']
   v.update(angle=35+5*(s%8),scale=scale)
  v.update(model='paired_triangles',mode=mode)
 elif n in (3,4):
  # Marked properties are chosen by the actual type of quadrilateral.
  shapes=['kite','parallelogram','trapezium'] if n==3 else ['rectangle','rhombus','square']
  shape=shapes[(s-1)%3];v.update(model='quadrilateral',shape=shape)
  if shape=='kite':
   p=2*a;q=2*b;area=Fraction(p*q,2)
   if s%2:
    problem=f'Kite ABCD has perpendicular diagonals AC={p} cm and BD={q} cm. Find its area.'
    ans=f'area = {fmt(area)} cm²';actions=['Draw kite ABCD and its diagonals AC and BD.',f'Mark AC={p} cm, BD={q} cm and the right angle where they cross.',f'Use area=½×AC×BD=½×{p}×{q}.',f'Calculate {fmt(area)} cm².',f'Answer: {ans}. Both diagonal lengths were used once.']
    wrong=[f'area = {p*q} cm²',f'area = {fmt(area+q)} cm²',f'area = {fmt(Fraction(p*q,4))} cm²']
   else:
    problem=f'In kite ABCD, diagonal AC is the symmetry axis and BD={q} cm. The diagonals meet at O. Find BO.'
    ans=f'BO = {b} cm';actions=['Draw the kite with AC as its marked symmetry diagonal.',f'Mark BD={q} cm and intersection O.','The symmetry diagonal AC bisects BD: BO=OD.',f'BO=BD/2={q}/2={b} cm.',f'Answer: {ans}. Check BO+OD={q} cm.']
    wrong=[f'BO = {q} cm',f'BO = {a} cm',f'BO = {b+1} cm']
   v.update(diagonal_ac=p,diagonal_bd=q)
  elif shape=='parallelogram':
   base=a+3;height=b+2;area=base*height
   v.update(operation='area' if s%2 else 'diagonal')
   if s%2:
    problem=f'Parallelogram ABCD has base AB={base} cm and perpendicular height {height} cm. Find its area.'
    ans=f'area = {area} cm²';actions=['Draw ABCD with AB∥DC and AD∥BC.',f'Mark AB={base} cm and the perpendicular height {height} cm.','Move the end triangle across: the parallelogram has the area of a rectangle of the same base and height.',f'Area={base}×{height}={area} cm².',f'Answer: {ans}. A slanted side is not the perpendicular height.']
    wrong=[f'area = {2*area} cm²',f'area = {area+base} cm²',f'area = {Fraction(area,2)} cm²']
   else:
    problem=f'In parallelogram ABCD, opposite side AB={base} cm and diagonals meet at O with AO={height} cm. Find DC and OC.'
    ans=f'DC = {base} cm; OC = {height} cm';actions=['Mark both pairs of opposite sides parallel in ABCD.',f'Opposite sides of a parallelogram are equal: DC=AB={base} cm.',f'Mark intersection O and AO={height} cm.','The diagonals bisect each other: OC=AO.',f'Answer: {ans}. Do not claim that the two whole diagonals are equal.']
    wrong=[f'DC = {base} cm; OC = {2*height} cm',f'DC = {2*base} cm; OC = {height} cm',f'DC = {base} cm; OC = {height+1} cm']
   v.update(base=base,height=height)
  elif shape=='trapezium':
   top=a+2;bottom=top+b;h=c;area=Fraction((top+bottom)*h,2)
   problem=f'Trapezium ABCD has AB∥DC, bases AB={bottom} cm and DC={top} cm, and perpendicular height {h} cm. Find its area.'
   ans=f'area = {fmt(area)} cm²';actions=['Draw a trapezium with exactly the marked parallel bases AB and DC.',f'Label bases {bottom} cm and {top} cm, and perpendicular height {h} cm.','Use area=½(sum of parallel bases)×perpendicular height.',f'Area=½({bottom}+{top})×{h}={fmt(area)} cm².',f'Answer: {ans}. The non-parallel side is not the height.']
   wrong=[f'area = {bottom*h} cm²',f'area = {top*h} cm²',f'area = {fmt(area+top)} cm²'];v.update(base=bottom,top=top,height=h)
  elif shape=='rectangle':
   width=a+3;height=b+2
   problem=f'Rectangle ABCD has AB={width} cm and BC={height} cm. Find AC and state why BD has the same length.'
   rad=width*width+height*height
   ans=f'AC = BD = √{rad} cm'
   actions=['Draw the four right angles of rectangle ABCD.',f'Label AB={width} cm and BC={height} cm.',f'In right triangle ABC, AC²={width}²+{height}²={rad}.',f'AC=√{rad} cm; the diagonals of a rectangle are equal.',f'Answer: {ans}. Square the diagonal to check the two side squares.']
   wrong=[f'AC = BD = {width+height} cm',f'AC = BD = √{rad+1} cm',f'AC = √{rad} cm; BD = {height} cm'];v.update(width=width,height=height,radicand=rad)
  elif shape=='rhombus':
   d1=2*a;d2=2*b;area=Fraction(d1*d2,2)
   problem=f'Rhombus ABCD has diagonals AC={d1} cm and BD={d2} cm. Find its area and name the diagonal angle.'
   ans=f'area = {fmt(area)} cm²; diagonals perpendicular'
   actions=['Draw a rhombus and mark all four sides equal.',f'Label diagonals AC={d1} cm and BD={d2} cm.','Rhombus diagonals bisect at right angles, forming four right triangles.',f'Area=½×{d1}×{d2}={fmt(area)} cm².',f'Answer: {ans}. Their lengths need not be equal.']
   wrong=[f'area = {d1*d2} cm²; diagonals perpendicular',f'area = {fmt(area)} cm²; diagonals parallel',f'area = {fmt(area+1)} cm²; diagonals perpendicular']
   v.update(diagonal_ac=d1,diagonal_bd=d2)
  else:
   side=a+3;area=side*side
   problem=f'Square ABCD has side AB={side} cm. Find its area and state one diagonal property.'
   ans=f'area = {area} cm²; diagonals equal and perpendicular'
   actions=['Draw a square with four equal sides and four right angles.',f'Label each side {side} cm.',f'Area=side×side={side}×{side}.',f'The diagonals are equal and meet at right angles.',f'Answer: {ans}. This square has both rectangle and rhombus diagonal properties.']
   wrong=[f'area = {2*area} cm²; diagonals equal and perpendicular',f'area = {area} cm²; diagonals parallel',f'area = {area+side} cm²; diagonals equal and perpendicular'];v.update(side=side)
 elif n==5:
  scale=1+(s-1)//5;ab=6*scale;ac=8*scale;bc=10*scale;de=bc//2;mode=['half','reverse','parallel'][(s-1)%3]
  if mode=='half':
   problem=f'In ΔABC, D is the midpoint of AB and E of AC. BC={bc} cm. Find DE and justify the result.'
   ans=f'DE = {de} cm'
   actions=['Draw triangle ABC and mark AD=DB and AE=EC.',f'Label BC={bc} cm.','Apply the midpoint theorem: DE∥BC and DE=½BC.',f'DE=½×{bc}={de} cm.',f'Answer: {ans}. The short segment has half the corresponding base length.']
   wrong=[f'DE = {bc} cm',f'DE = {bc*2} cm',f'DE = {de+1} cm']
  elif mode=='reverse':
   problem=f'In ΔABC, D and E are the midpoints of AB and AC. DE={de} cm. Find BC.'
   ans=f'BC = {bc} cm'
   actions=['Mark the equal halves on AB and AC, establishing both midpoints.',f'Label DE={de} cm.','The midpoint theorem gives DE=½BC.',f'BC=2×DE=2×{de}={bc} cm.',f'Answer: {ans}. Check DE is half of BC.']
   wrong=[f'BC = {de} cm',f'BC = {bc+1} cm',f'BC = {bc//2} cm']
  else:
   angle=35+5*(s%8)
   problem=f'In ΔABC, D and E are midpoints of AB and AC, and ∠ABC={angle}°. Find ∠ADE with a reason.'
   ans=f'∠ADE = {angle}°'
   actions=['Draw ΔABC with D halfway along AB and E halfway along AC.',f'Mark ∠ABC={angle}°.','The midpoint theorem implies DE∥BC.','Corresponding angles ∠ADE and ∠ABC are equal.',f'Answer: {ans} (DE∥BC, corresponding angles).']
   wrong=[f'∠ADE = {180-angle}°',f'∠ADE = {angle+10}°',f'∠ADE = {angle-10}°'];v.update(angle=angle)
  v.update(model='midpoint',mode=mode,ab=ab,ac=ac)
  if mode=='reverse':v.update(de=de,solution_bc=bc)
  elif mode=='half':v.update(bc=bc,solution_de=de)
 else:
  mode=['midpoint_angle','parallel_angle','diagnosis'][(s-1)%3];angle=35+5*(s%16);base=2*a
  if mode=='midpoint_angle':
   problem=f'In ΔABC, D and E are midpoints of AB and AC. ∠ABC={angle}°. Find ∠ADE and give a complete reason.'
   ans=f'∠ADE = {angle}° (midpoint theorem, corresponding angles)'
   actions=['Mark AD=DB and AE=EC in triangle ABC.',f'Mark given ∠ABC={angle}°.','The midpoint theorem makes DE∥BC.','Because AB is a transversal, ∠ADE corresponds to ∠ABC.',f'Answer: {ans}. Mark the equal angle sectors on the diagram.']
   wrong=[f'∠ADE = {180-angle}° (co-interior)',f'∠ADE = {angle}° (vertical angles)',f'∠ADE = {angle+5}° (midpoint theorem)'];v.update(model='midpoint',angle=angle)
  elif mode=='parallel_angle':
   problem=f'ABCD is a parallelogram, diagonal AC is drawn, and ∠DAC={angle}°. Find ∠ACB and name the angle relationship.'
   ans=f'∠ACB = {angle}° (alternate interior, AD∥BC)'
   actions=['Draw ABCD and mark AD∥BC.',f'Draw diagonal AC as the transversal and mark ∠DAC={angle}°.','∠DAC and ∠ACB are alternate interior angles.','Alternate interior angles are equal on parallel lines.',f'Answer: {ans}. The two angles lie on opposite sides of AC.']
   wrong=[f'∠ACB = {180-angle}° (co-interior)',f'∠ACB = {angle}° (vertical angles)',f'∠ACB = {angle+10}° (alternate interior)'];v.update(model='quadrilateral',shape='parallelogram',angle=angle)
  else:
   problem=f'In ΔABC, D and E are midpoints of AB and AC. BC={base} cm. A learner claims DE={base} cm. Find the first error and correct DE.'
   ans=f'First error: DE=BC; correct DE={a} cm'
   actions=['Draw the original triangle and mark AD=DB, AE=EC.',f'Mark BC={base} cm and the learner claim DE={base} cm.','The first error is treating the mid-segment as the full base: DE must be HALF of BC.',f'Replace the wrong step: DE=½×{base}={a} cm.',f'Answer: {ans}. Check 2DE=BC.']
   wrong=[f'DE={base} cm (learner correct)',f'First error: DE∥BC; correct DE={base} cm',f'First error: DE=BC; correct DE={2*base} cm'];v.update(model='midpoint',bc=base,de=a)
  v.update(mode=mode)
 wrong=list(dict.fromkeys(x for x in wrong if x!=ans))
 if n==1:
  for delta in (20,30,40,50):
   candidate=f'x = {value+delta}°'
   if candidate!=ans and candidate not in wrong:wrong.append(candidate)
 for candidate in ('Not enough information to determine the result','The marked lengths must be added','The conclusion follows from vertically opposite angles','The result is twice the marked length'):
  if candidate!=ans and candidate not in wrong:wrong.append(candidate)
 wrong=wrong[:3]
 assert len(actions)==5 and len({ans,*wrong})==4,(n,i,ans,wrong)
 v['answer']=ans
 return {'id':f'g10-euc-l{n:02}-w{i:02}' if not variant else f'g10-euc-l{n:02}-v{variant}-w{i:02}',
 'problem':problem,'actions':actions,'answer':ans,'check':actions[-1],
 'visual':{'family':'grade10_euclidean','values':v},'lesson':n,
 'misconception':'Use only marked geometric facts, state the theorem, and keep corresponding vertices in order.',
 'wrong':wrong,'difficulty':'foundation' if i<=2 else 'easy' if i<=5 else 'standard' if i<=9 else 'intermediate' if i<=12 else 'exam'}
def choice(n,i,variant,prefix):
 q=case(n,i,variant);options=[q['answer'],*q['wrong']];pos=i%4
 options=options[-pos:]+options[:-pos] if pos else options
 return {'id':f'g10-euc-l{n:02}-{prefix}{i:02}','prompt':q['problem'],'options':options,
 'answer_index':pos,'memo':' '.join(q['actions']),'source':f'grade10-euc-lesson-{n:02}.md'}
def build():
 DOC.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True);manifest=[]
 for n,title in TITLES.items():
  worked=[{k:v for k,v in case(n,i).items() if k!='wrong'} for i in range(1,16)]
  data={'source':f'grade10-euc-lesson-{n:02}.md','worked':worked,
   'practice':[choice(n,i,1,'p') for i in range(1,16)],
   'mastery':[choice(n,i+15,2,'m') for i in range(1,6)],
   'reassessment':[choice(n,i+20,3,'r') for i in range(1,4)]}
  assert len({q['problem'] for q in worked})>=10,n
  lines=[f'# Grade 10 Topic 4 · Lesson {n}: {title}',
   f'Authority: [DBE Grade 10 Mathematics ATP]({ATP}), Term 2 Euclidean Geometry. Original Athena examples.',
   'Status: teacher and browser review required. Keep marked facts and every previous justified step on the board.']
  for q in worked:lines += [f'## {q["id"]}: {q["problem"]}',f'Visual contract: {json.dumps(q["visual"],ensure_ascii=False)}',
   *[f'{j}. {a}' for j,a in enumerate(q['actions'],1)],f'**Answer:** {q["answer"]}. **Misconception:** {q["misconception"]}']
  for label,key in [('Practice','practice'),('Mastery','mastery'),('Parallel reassessment','reassessment')]:
   lines.append(f'## {label} answer key')
   for q in data[key]:lines.append(f'- {q["id"]}: {q["prompt"]} Options: {" | ".join(q["options"])}. Correct: {q["options"][q["answer_index"]]}. {q["memo"]}')
  source=DOC/data['source'];source.write_text('\n\n'.join(lines)+'\n',encoding='utf-8')
  (OUT/f'euclidean_{n:02}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  manifest.append({'lesson_id':f'g10-euc-{n:02}','source':source.name,'source_sha256':sha256(source.read_bytes()).hexdigest(),
   'worked':15,'practice':15,'mastery':5,'reassessment':3,'status':'teacher_review_required','teacher_approved':False,'browser_accepted':False})
 (DOC/'topic04-acceptance-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
 (DOC/'topic04-batch-acceptance.md').write_text(f'# Grade 10 Topic 4: Euclidean Geometry\n\n[DBE Grade 10 Mathematics ATP]({ATP}) Term 2 covers prior angle and triangle facts, congruence and similarity, kite/parallelogram/rectangle/rhombus/square/trapezium properties, triangle mid-segment and mixed riders. Six authored lessons contain 90 worked, 90 four-choice practice, 30 mastery and 18 reassessments. Teacher and live browser acceptance remain pending.\n',encoding='utf-8')
if __name__=='__main__':build()
