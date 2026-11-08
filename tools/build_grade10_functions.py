"""Original Grade 10 Functions and Graphs examples grounded in the DBE ATP."""
from hashlib import sha256
from pathlib import Path
from fractions import Fraction
import json

ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/curriculum/grade10/functions-and-graphs'
OUT=ROOT/'backend/app/curriculum/grade10/generated'
ATP='https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2023%20ATPs/FET%20Content%20Subjects/Grade%2010/1.580%20ATP%202023-24%20Gr%2010%20Maths%20final.pdf'
TITLES={1:'Function rules, tables and plotted input-output pairs',2:'Parent graphs, intercepts, turning points and asymptotes',
 3:'Effects of a and q on algebraic graphs',4:'Sine, cosine and tangent from 0° to 360°',
 5:'Amplitude, reflection and vertical shifts in trigonometric graphs',6:'Infer algebraic equations from graph features',
 7:'Mixed graph interpretation and first-error repair'}
FAMILIES=('linear','parabola','hyperbola','exponential')
ANGLES=(0,30,45,60,90,120,135,150,180,210,225,240,270,300,315,330,360)
SIN=('0','1/2','√2/2','√3/2','1','√3/2','√2/2','1/2','0','−1/2','−√2/2','−√3/2','−1','−√3/2','−√2/2','−1/2','0')
COS=('1','√3/2','√2/2','1/2','0','−1/2','−√2/2','−√3/2','−1','−√3/2','−√2/2','−1/2','0','1/2','√2/2','√3/2','1')
TAN=('0','√3/3','1','√3','undefined','−√3','−1','−√3/3','0','√3/3','1','√3','undefined','−√3','−1','−√3/3','0')
def expr(f,a,q,b=2):
 core={'linear':'x','parabola':'x²','hyperbola':'1/x','exponential':f'{b}ˣ','sine':'sin θ','cosine':'cos θ','tangent':'tan θ'}[f]
 return f'y = {a}·{core} {"+" if q>=0 else "−"} {abs(q)}'
def case(n,i,variant=0):
 s=i+15*variant;a=(-1 if s%2 else 1)*(1+s%3);q=-3+(s*2)%7;u=-2+(s%5);b=2+(s%2)
 v={'lesson':n,'model':'function_graph','a':a,'q':q,'base':b,'given':[]}
 if n==1:
  a=1+s%4;q=-4+(s//2)%7;u=-2+(s*3)%7;value=a*u+q;v.update(family='linear',a=a,q=q,mode='table',given=[[0,q],[1,a+q],[u,value]],target_x=u)
  problem=f'The rule is {expr("linear",a,q)}. Complete the table value at x={u} and plot the pair.'
  answer=f'({u}; {value})'
  steps=[f'Keep the rule {expr("linear",a,q)} visible and mark input x={u}.',f'Substitute the input: y={a}×({u}) {"+" if q>=0 else "−"} {abs(q)}.',f'Calculate y={value}; add it to the table beside x={u}.',f'Plot ({u}; {value}) using the x-axis and y-axis scales.',f'Answer: {answer}. Check with another given row such as x=0 → y={q}.']
  wrong=[f'({value}; {u})',f'({u}; {value+a})',f'({u}; {value-1})']
 elif n==2:
  family=FAMILIES[(s-1)%4];v.update(family=family,a=1,q=0,mode='parent')
  sample_x=(-2,-1,1,2)[(s//4)%4]
  sample_y={'linear':sample_x,'parabola':sample_x**2,'hyperbola':Fraction(1,sample_x),'exponential':Fraction(b**sample_x) if sample_x>=0 else Fraction(1,b**(-sample_x))}[family]
  v['given']=[[sample_x,str(sample_y)]]
  if family=='linear':feature='y-intercept';answer='(0; 0)';why='At x=0 the line passes through the origin.'
  elif family=='parabola':feature='turning point';answer='(0; 0)';why='The parabola is symmetric about x=0 and its minimum is at the origin.'
  elif family=='hyperbola':feature='vertical asymptote';answer='x = 0';why='Division by zero is undefined, so the curve never crosses x=0.'
  else:feature='horizontal asymptote';answer='y = 0';why=f'As x decreases, {b}ˣ approaches zero but remains positive.'
  v['base']=b
  problem=f'For the parent graph {expr(family,1,0,b)}, plot its value at x={sample_x} and identify its {feature}.'
  steps=[f'Set up axes and identify the {family} family from the formula.',f'Substitute x={sample_x}, giving y={sample_y}, and plot ({sample_x}; {sample_y}).',f'Trace the shape without joining points across an undefined input.',why,f'Answer: {answer} is the {feature}. The plotted point ({sample_x}; {sample_y}) verifies the original rule.']
  wrong=[('x = 1' if answer.startswith('x') else 'y = 1' if answer.startswith('y') else '(0; 1)'),('x = −1' if answer.startswith('x') else 'y = −1' if answer.startswith('y') else '(1; 0)'),('no asymptote' if 'asymptote' in feature else '(1; 1)')]
 elif n==3:
  family=FAMILIES[(s-1)%4];a=(-1 if s%2 else 1)*(1+s%3);q=-3+(s//2)%7
  v.update(family=family,a=a,q=q,mode='transform')
  formula=expr(family,a,q,b)
  if family=='linear':feature='y-intercept';answer=f'(0; {q})';reason='At x=0 the x term vanishes.'
  elif family=='parabola':feature='turning point';answer=f'(0; {q})';reason='The axis of symmetry is x=0; a changes the opening and q moves the vertex.'
  elif family=='hyperbola':feature='horizontal asymptote';answer=f'y = {q}';reason='The term a/x tends to zero as |x| grows; x=0 stays excluded.'
  else:feature='horizontal asymptote';answer=f'y = {q}';reason=f'The term a·{b}ˣ tends to zero as x decreases; q sets the asymptote.'
  problem=f'For {formula}, give the {feature} and explain the effect of q.'
  steps=[f'Draw the parent {family} shape and mark its original axes or asymptotes.',f'Apply factor a={a}; a negative value reflects the parent in the x-axis.',f'Shift the graph vertically by q={q}, retaining the original as a comparison.',reason,f'Answer: {answer} ({feature}). Check it against {formula}.']
  wrong=[f'y = {q+1}' if 'asymptote' in feature else f'(0; {q+1})',f'y = {-q}' if 'asymptote' in feature else f'(0; {-q})',f'x = {q}' if 'asymptote' in feature else f'({q}; 0)']
 elif n==4:
  family=('sine','cosine','tangent')[(s-1)%3];theta=ANGLES[(s*5)%len(ANGLES)];idx=ANGLES.index(theta);value={'sine':SIN,'cosine':COS,'tangent':TAN}[family][idx]
  v.update(family=family,a=1,q=0,mode='trig_parent',angle=theta)
  problem=f'From the graph y={family.replace("sine","sin").replace("cosine","cos").replace("tangent","tan")} θ for 0°≤θ≤360°, determine y at θ={theta}°.'
  answer=f'y({theta}°) = {value}'
  steps=[f'Draw axes for θ from 0° to 360° and recognise the {family} graph.',f'Mark θ={theta}° on the horizontal axis and its quadrant.',f'Use the unit-circle reference angle to determine the magnitude and sign; tan is undefined at 90° and 270°.',f'Read the {family} value at {theta}°: {value}.',f'Answer: {answer}. Check the sign or undefined point against the graph.']
  wrong=[f'y({theta}°) = {"0" if value!="0" else "1"}',f'y({theta}°) = {"undefined" if value!="undefined" else "0"}',f'y({theta}°) = {"1" if value!="1" else "−1"}']
 elif n==5:
  family=('sine','cosine','tangent')[(s-1)%3];a=(-1 if s%2 else 1)*(1+s%4);q=-3+(s//2)%7;at0=a+q if family=='cosine' else q
  v.update(family=family,a=a,q=q,mode='trig_transform',angle=0)
  formula=expr(family,a,q)
  problem=f'For {formula}, give the midline and the value when θ=0°. Explain how a affects the graph.'
  answer=f'midline y = {q}; y(0°) = {at0}'
  steps=[f'Start with the parent {family} curve on 0°≤θ≤360°.',f'Multiply each defined parent y-value by a={a}; negative a reflects across the x-axis.',f'Shift the multiplied graph by q={q}, so the centre line is y={q}.',f'At θ=0°, {family} is {1 if family=="cosine" else 0}; hence y(0°)={at0}.',f'Answer: {answer}. Tangent has no amplitude; |a| scales it vertically.']
  wrong=[f'midline y = 0; y(0°) = {at0}',f'midline y = {q}; y(0°) = {q if family=="cosine" else a+q}',f'midline y = {-q}; y(0°) = {at0}']
 elif n==6:
  family=FAMILIES[(s-1)%4];a=(-1 if s%2 else 1)*(1+s%3);q=-3+(s//3)%7;v.update(family=family,a=a,q=q,mode='infer')
  if family=='linear':givens=f'y-intercept (0; {q}) and point (1; {a+q})';why=f'Slope=({a+q}−{q})/(1−0)={a}.'
  elif family=='parabola':givens=f'vertex (0; {q}) and point (1; {a+q})';why=f'Substituting (1; {a+q}) into y=ax²+{q} gives a={a}.'
  elif family=='hyperbola':givens=f'asymptotes x=0 and y={q}, and point (1; {a+q})';why=f'Substituting x=1 into y=a/x+{q} gives a={a}.'
  else:givens=f'asymptote y={q} and point (0; {a+q}), with base {b}';why=f'At x=0, {b}ˣ=1; hence a=({a+q})−({q})={a}.'
  v['given']=givens
  v['given_points']=[[0,q],[1,a+q]] if family in ('linear','parabola') else [[1,a+q]] if family=='hyperbola' else [[0,a+q]]
  v['given_asymptotes']=['x=0',f'y={q}'] if family=='hyperbola' else [f'y={q}'] if family=='exponential' else []
  formula=expr(family,a,q,b)
  problem=f'A {family} graph has {givens}. Find its equation.'
  answer=formula
  steps=[f'Mark the given point and intercept, vertex or asymptotes on the same axes.',f'Choose the {family} model with unknown a and q; the marked feature fixes q={q}.',why,f'Insert a={a} and q={q}; sketch the curve through the supplied point.',f'Answer: {answer}. Check every stated feature in the equation.']
  wrong=[expr(family,a+1,q,b),expr(family,a,q+1,b),expr(family,-a,q,b)]
 else:
  kind=(s-1)%3
  if kind==1:
   family='parabola' if s%2 else 'linear';a=(-1 if s%4 else 1);q=-2+(s//5)%5
   y1=a+q;y2=(4*a+q) if family=='parabola' else (2*a+q);slope=y2-y1
   v.update(family=family,a=a,q=q,mode='secant',given=[[1,y1],[2,y2]])
   problem=f'For {expr(family,a,q)}, find the average gradient from x=1 to x=2 using a secant.'
   answer=f'average gradient = {slope}'
   steps=[f'Plot the curve and mark x=1 and x=2.',f'Calculate f(1)={y1} and f(2)={y2}; plot (1; {y1}) and (2; {y2}).',f'Draw the secant joining those two points; its horizontal change is 2−1=1.',f'The average gradient is (f(2)−f(1))/(2−1)=({y2}−({y1}))/1={slope}.',f'Answer: {answer}. This is one secant gradient, not the average of two instantaneous gradients.']
   wrong=[f'average gradient = {y1+y2}',f'average gradient = {-slope}',f'average gradient = {slope+1}']
  elif kind==2:
   discrete=(s//3)%2==0;rate=1+(s//3)%2;context=['tickets sold','boxes packed','chairs rented','learners registered','items delivered'][(s//3)%5] if discrete else ['water filling','time elapsed','fuel transferred','distance travelled','liquid drained'][(s//3)%5]
   v.update(family='linear',a=rate,q=0,mode='discrete' if discrete else 'continuous',given=[[0,0],[1,rate],[2,2*rate]])
   problem=(f'A service handles {context} at R{rate} each. Let x be the number handled, 0≤x≤2. Is total cost versus x discrete or continuous?'
    if discrete else f'For {context}, a measured amount changes at {rate} units per minute. Let x be elapsed minutes, 0≤x≤2. Is amount versus x discrete or continuous?')
   answer='Discrete; only whole counts of x are valid' if discrete else 'Continuous; x may take any real value in the interval'
   steps=[f'Identify x as the number or measure for {context}.',f'Calculate the values at x=0, 1 and 2: y=0, {rate}, {2*rate}.',
    'A fraction of a counted item is not a valid input in this situation.' if discrete else 'The measured quantity can pass through values between whole-number inputs.',
    'Plot isolated points at whole x-values; do not connect them.' if discrete else 'Plot the points and join them on the stated continuous interval.',f'Answer: {answer}. The context decides the domain, not the appearance of the line formula.']
   wrong=['Continuous; every real x is valid' if discrete else 'Discrete; only x=0,1,2 are valid','No graph can be drawn','The domain is all negative integers']
  else:
    family=FAMILIES[(s-1)%4] if s%5 else 'sine';a=(-1 if s%2 else 1)*(1+s%3);q=(-3,-2,-1,1,2,3)[(s//3)%6]
    if family=='linear' and q==a:q=-q
    v.update(family=family,a=a,q=q,mode='diagnosis')
    if family=='linear':claim=f'the y-intercept of {expr(family,a,q)} is (0; {a})';answer=f'first error: using a as the intercept; (0; {q})';reason=f'At x=0, y={q}, not {a}.'
    elif family=='parabola':claim=f'the turning point of {expr(family,a,q)} is (0; 0)';answer=f'first error: ignoring q; turning point (0; {q})';reason=f'The vertex moves from (0; 0) to (0; {q}).'
    elif family=='hyperbola':claim=f'{expr(family,a,q)} is defined at x=0';answer=f'first error: division by zero; domain x ≠ 0';reason='The 1/x term has no value at x=0 regardless of q.'
    elif family=='sine':claim=f'{expr(family,a,q)} has midline y=0';answer=f'first error: ignoring q; midline y = {q}';reason=f'The vertical shift moves the midline to y={q}.'
    else:claim=f'{expr(family,a,q)} has horizontal asymptote y=0';answer=f'first error: ignoring q; asymptote y = {q}';reason=f'The vertical shift moves the horizontal asymptote to y={q}.'
    problem=f'A learner claims {claim}. Identify the first error and correct it.'
    steps=[f'Draw or mark the parent {family} graph and read the learner claim.',f'Identify the relevant intercept, turning point, domain or asymptote from the formula.',f'The first error is in the claimed feature, before any later graph interpretation. {reason}',f'Replace only that feature with the corrected mathematical fact.',f'Answer: {answer}. Verify it in the original equation.']
    wrong=[f'learner correct: {claim}',f'first error: change the input axis; {claim}',f'first error: reverse the entire curve; {claim}']
 wrong=list(dict.fromkeys(w for w in wrong if w!=answer))
 for filler in ('Cannot be determined','All points lie on the x-axis','The curve is undefined everywhere'):
  if filler not in wrong and filler!=answer:wrong.append(filler)
 wrong=wrong[:3]
 assert len(steps)==5 and len({answer,*wrong})==4,(n,i,answer,wrong)
 v['answer']=answer
 return {'id':f'g10-fn-l{n:02}-w{i:02}','problem':problem,'actions':steps,'answer':answer,'check':steps[-1],
  'visual':{'family':'grade10_functions','values':v},'lesson':n,'wrong':wrong,
  'misconception':'Keep domain restrictions, original points and the meaning of a and q visible through every graph step.',
  'difficulty':'foundation' if i<=2 else 'easy' if i<=5 else 'standard' if i<=9 else 'intermediate' if i<=12 else 'exam'}
def option(n,i,variant,prefix):
 scene=case(n,i,variant);choices=[scene['answer'],*scene['wrong']];position=i%4
 choices=choices[-position:]+choices[:-position] if position else choices
 return {'id':f'g10-fn-l{n:02}-{prefix}{i:02}','prompt':scene['problem'],'options':choices,'answer_index':position,
  'memo':' '.join(scene['actions']),'source':f'grade10-fn-lesson-{n:02}.md'}
def build():
 DOC.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True);manifest=[]
 for n,title in TITLES.items():
  worked=[{k:v for k,v in case(n,i).items() if k!='wrong'} for i in range(1,16)]
  data={'source':f'grade10-fn-lesson-{n:02}.md','worked':worked,
   'practice':[option(n,i,1,'p') for i in range(1,16)],
   'mastery':[option(n,i+15,2,'m') for i in range(1,6)],
   'reassessment':[option(n,i+20,3,'r') for i in range(1,4)]}
  assert len({q['problem'] for q in worked})>=10,n
  lines=[f'# Grade 10 Topic 6 · Lesson {n}: {title}',f'Authority: [DBE Grade 10 Mathematics ATP]({ATP}), Term 2 Functions and Graphs. Original Athena examples.',
   'Status: teacher and browser review required. Retain original axes and earlier plotted points; draw no curve across a discontinuity.']
  for scene in worked:lines += [f'## {scene["id"]}: {scene["problem"]}',f'Visual contract: {json.dumps(scene["visual"],ensure_ascii=False)}',
   *[f'{j}. {a}' for j,a in enumerate(scene['actions'],1)],f'**Answer:** {scene["answer"]}. **Misconception:** {scene["misconception"]}']
  for label,key in [('Practice','practice'),('Mastery','mastery'),('Parallel reassessment','reassessment')]:
   lines.append(f'## {label} answer key')
   for item in data[key]:lines.append(f'- {item["id"]}: {item["prompt"]} Options: {" | ".join(item["options"])}. Correct: {item["options"][item["answer_index"]]}. {item["memo"]}')
  source=DOC/data['source'];source.write_text('\n\n'.join(lines)+'\n',encoding='utf-8')
  (OUT/f'functions_{n:02}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  manifest.append({'lesson_id':f'g10-fn-{n:02}','source':source.name,'source_sha256':sha256(source.read_bytes()).hexdigest(),
   'worked':15,'practice':15,'mastery':5,'reassessment':3,'status':'teacher_review_required','teacher_approved':False,'browser_accepted':False})
 (DOC/'topic06-acceptance-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
 (DOC/'topic06-batch-acceptance.md').write_text(f'# Grade 10 Topic 6: Functions and Graphs\n\n[DBE Grade 10 Mathematics ATP]({ATP}) Term 2: representations, parent algebraic graphs, a and q effects, trigonometric graphs through 360°, sketching and inference. Seven lessons contain 105 worked, 105 four-choice practice, 35 mastery and 21 reassessments. Teacher and live browser acceptance remain pending.\n',encoding='utf-8')
if __name__=='__main__':build()
