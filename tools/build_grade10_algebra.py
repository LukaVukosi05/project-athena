"""Original Grade 10 Algebraic Expressions questions grounded in DBE Term 1 ATP."""
from pathlib import Path
from hashlib import sha256
import json, math
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/curriculum/grade10/algebraic-expressions';OUT=ROOT/'backend/app/curriculum/grade10/generated'
ATP='https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2023%20ATPs/FET%20Content%20Subjects/Grade%2010/1.580%20ATP%202023-24%20Gr%2010%20Maths%20final.pdf'
TITLES={1:'Rational and irrational real numbers',2:'Surds, integer bounds and appropriate rounding',3:'Multiply a binomial by a trinomial',4:'Factorise trinomials and group in pairs',5:'Factorise sums and differences of cubes',6:'Simplify and combine algebraic fractions with cubic denominators'}
def poly(coefs):
 out=''
 for power,v in sorted(coefs.items(),reverse=True):
  if v==0:continue
  core=('x' if abs(v)==1 and power else str(abs(v)))+('²' if power==2 else '³' if power==3 else 'x' if power==1 and abs(v)!=1 else '')
  if power==1 and abs(v)==1:core='x'
  if power==0:core=str(abs(v))
  out+=((' + ' if v>0 else ' − ') if out else ('−' if v<0 else ''))+core
 return out or '0'
def binomial(a):return f'(x {"+" if a>=0 else "−"} {abs(a)})'
def fmtfrac(a,b):return str(Fraction(a,b))
def case(n,i,variant=0):
 s=i+15*variant; a=2+s%7;b=1+(s//2)%6;c=1+(s//3)%5;sign=-1 if s%2 else 1
 v={'lesson':n,'model':['number_sets','surd_line','area_expansion','factor_groups','cube_identity','fraction_factors'][n-1], 'a':a,'b':b,'c':c,'sign':sign};wrong=[]
 if n==1:
  a=s+1;rad=a*a if s%3==0 else a*a+1;lower=a;upper=a+1
  if s%3==0:
   problem=f'Classify √{rad} as rational or irrational and locate its exact value on a number line.'
   actions=[f'Locate the two adjacent integers {a} and {a+1} on the real-number line.',f'Test {a}² = {rad}.',f'Therefore √{rad} = {a} exactly.',f'{a} = {a}/1, a ratio of integers; it is rational.',f'Answer: √{rad} = {a} is rational. Check {a} × {a} = {rad}.']
   answer=f'rational; √{rad} = {a}';wrong=[f'irrational; √{rad} = {a}',f'rational; √{rad} = {a+1}',f'rational; √{rad} = {a-1}'];v.update(kind='rational')
  else:
   problem=f'Classify √{rad} as rational or irrational, and place it between consecutive integers.'
   actions=[f'Place √{rad} on the real-number line.',f'Compare neighbouring squares: {lower}² = {lower*lower} < {rad} < {upper*upper} = {upper*upper}.',f'Therefore {lower} < √{rad} < {upper}.',f'{rad} is not a perfect square, so √{rad} cannot be expressed as a ratio of integers.',f'Answer: √{rad} is irrational and lies strictly between {lower} and {upper}; squaring both bounds checks the interval.']
   answer=f'irrational; {lower} < √{rad} < {upper}';wrong=[f'rational; {lower} < √{rad} < {upper}',f'irrational; {lower-1} < √{rad} < {lower}',f'irrational; {upper} < √{rad} < {upper+1}'];v.update(kind='irrational')
  v.update(radicand=rad,lower=lower,upper=upper)
 elif n==2:
  a=s+1;rad=a*a+1;precision=1 if s%2 else 2;value=math.sqrt(rad);rounded=f'{value:.{precision}f}'
  # Use Decimal-style half-up only where required; sqrt(integer-square+1) never lands at a decimal tie.
  problem=f'Estimate √{rad} to {precision} decimal place{"s" if precision>1 else ""} and justify the integer interval before rounding.'
  actions=[f'Write the adjacent square numbers {a*a} and {(a+1)**2}.',f'Since {a*a} < {rad} < {(a+1)**2}, the value lies between {a} and {a+1}.',f'Use a decimal approximation √{rad} ≈ {value:.5f}.',f'Keep {precision} decimal place{"s" if precision>1 else ""}: √{rad} ≈ {rounded}.',f'Check: {rounded} lies between {a} and {a+1}, and its square is close to {rad}.']
  answer=f'√{rad} ≈ {rounded}';wrong=[f'√{rad} ≈ {value+d:.{precision}f}' for d in (0.1,-0.1,0.2)];v.update(radicand=rad,lower=a,upper=a+1,decimal=rounded,precision=precision)
 elif n==3:
  d=sign*b; t=sign*c; co={3:1,2:a+d,1:t+a*d,0:a*t};problem=f'Expand and simplify {binomial(a)}(x² {"+" if d>0 else "−"} {abs(d)}x {"+" if t>0 else "−"} {abs(t)}).'
  actions=[f'Show the two rows x(x² {"+" if d>0 else "−"} {abs(d)}x {"+" if t>0 else "−"} {abs(t)}) and {a}(x² {"+" if d>0 else "−"} {abs(d)}x {"+" if t>0 else "−"} {abs(t)}).',f'First row: x³ {"+" if d>0 else "−"} {abs(d)}x² {"+" if t>0 else "−"} {abs(t)}x.',f'Second row: {a}x² {"+" if a*d>0 else "−"} {abs(a*d)}x {"+" if a*t>0 else "−"} {abs(a*t)}.',f'Collect like powers: x³ coefficient 1, x² coefficient {co[2]}, x coefficient {co[1]}, constant {co[0]}.',f'Answer: {poly(co)}. Check by substituting x = 0 in the product and expanded expression: both give {co[0]}.']
  answer=poly(co);wrong=[poly(co|{1:co[1]+shift}) for shift in (1,-1,2)];v.update(d=d,t=t,coefficients=co)
 elif n==4:
  if s%2:
   d=sign*b;co={2:1,1:a+d,0:a*d};problem=f'Factorise {poly(co)} fully.'
   actions=[f'Write the given trinomial {poly(co)}.',f'Find two integers with sum {co[1]} and product {co[0]}: {a} and {d}.',f'Split the middle term as {a}x + ({d})x.',f'Group and take common factors to obtain {binomial(a)}{binomial(d)}.',f'Answer: {binomial(a)}{binomial(d)}. Expand to recover {poly(co)}.']
   answer=f'{binomial(a)}{binomial(d)}';wrong=[f'{binomial(a+delta)}{binomial(d)}' for delta in (1,-1,2)];v.update(kind='trinomial',d=d,coefficients=co)
  else:
   d=sign*b;problem=f'Factorise x² + {a}x {"+" if d>=0 else "−"} {abs(d)}x {"+" if a*d>=0 else "−"} {abs(a*d)} by grouping in pairs.'
   actions=[f'Group (x² + {a}x) + ({d}x {"+" if a*d>=0 else "−"} {abs(a*d)}).',f'Take x out of the first pair: x(x + {a}).',f'Take {d} out of the second pair: {d}(x + {a}).',f'The repeated binomial is (x + {a}), so the result is {binomial(a)}{binomial(d)}.',f'Answer: {binomial(a)}{binomial(d)}. Multiply back to recover the four original terms.']
   answer=f'{binomial(a)}{binomial(d)}';wrong=[f'{binomial(a)}{binomial(d+delta)}' for delta in (1,-1,2)];v.update(kind='grouping',d=d,coefficients={2:1,1:a+d,0:a*d})
 elif n==5:
  b=2+((s-1)%15)//2+variant*8;v["b"]=b;cube=b**3;minus=sign<0;middle=b if minus else -b;co={2:1,1:middle,0:b*b};problem=f'Factorise x³ {"−" if minus else "+"} {cube} completely.'
  first=f'(x {"−" if minus else "+"} {b})';second=f'(x² {"+" if minus else "−"} {b}x + {b*b})'
  actions=[f'Write {cube} = {b}³; identify a difference of cubes.' if minus else f'Write {cube} = {b}³; identify a sum of cubes.',f'Use u³ {"−" if minus else "+"} v³ = (u {"−" if minus else "+"} v)(u² {"+" if minus else "−"} uv + v²).',f'Substitute u = x, v = {b}: {first}{second}.',f'Check the cross terms cancel after multiplying: the x² and x terms sum to zero.',f'Answer: {first}{second}. Multiply out to recover x³ {"−" if minus else "+"} {cube}.']
  answer=first+second;wrong=[first+f'(x² {"+" if minus else "−"} {b+shift}x + {b*b})' for shift in (1,-1,2)];v.update(cube=cube,kind='difference' if minus else 'sum',middle=middle)
 else:
  b=2+((s-1)%15)//2+variant*8;v["b"]=b;cube=b**3;minus=sign<0;denom=f'(x³ {"−" if minus else "+"} {cube})';first=f'(x {"−" if minus else "+"} {b})';second=f'(x² {"+" if minus else "−"} {b}x + {b*b})'
  if s%2:
   problem=f'Simplify {second}/{denom} and state the excluded real value of x.'
   actions=[f'Factor the denominator: {denom} = {first}{second}.',f'Keep the restriction from the original denominator: x ≠ {b if minus else -b}.',f'Cancel the common factor {second} only where it is nonzero.',f'Remaining expression: 1/{first}.',f'Answer: 1/{first}, x ≠ {b if minus else -b}. Check by multiplying the simplified form by the original denominator.']
   answer=f'1/{first}; x ≠ {b if minus else -b}';wrong=[f'1/{first}; x ≠ {b+shift if minus else -b+shift}' for shift in (1,-1,2)];v.update(kind='simplify')
  else:
   op='−' if s%4==0 else '+';coefficient=1-a if op=='−' else 1+a
   problem=f'Simplify {second}/{denom} {op} {a}{second}/{denom}; state the excluded real x.'
   actions=[f'The fractions share the denominator {denom}; combine the numerators.',f'Numerator = (1 {op} {a}){second} = {coefficient}{second}.',f'Factor the denominator: {denom} = {first}{second}.',f'Cancel {second}, retaining x ≠ {b if minus else -b} from the original denominator.',f'Answer: {coefficient}/{first}, x ≠ {b if minus else -b}. Multiply back to verify the common denominator.']
   answer=f'{coefficient}/{first}; x ≠ {b if minus else -b}';wrong=[f'{coefficient+shift}/{first}; x ≠ {b if minus else -b}' for shift in (1,-1,2)];v.update(kind='combine',operator=op)
  v.update(cube=cube,denominator=denom,first=first,second=second,excluded=b if minus else -b)
 assert len({answer,*wrong})==4,(n,i)
 return {'id':f'g10-aex-l{n:02}-w{i:02}' if not variant else f'g10-aex-l{n:02}-v{variant}-w{i:02}', 'problem':problem,'actions':actions,'answer':answer,'check':actions[-1], 'visual':{'family':'grade10_expressions','values':v},'lesson':n,'misconception':'Preserve every sign, factor, restriction and original expression; check the final result by reversing the operation.', 'wrong':wrong,'difficulty':'foundation' if i<=2 else 'easy' if i<=5 else 'standard' if i<=9 else 'intermediate' if i<=12 else 'exam'}
def choice(n,i,variant,prefix):
 q=case(n,i,variant);options=[q['answer'],*q['wrong']];pos=i%4;options=options[4-pos:]+options[:4-pos] if pos else options
 return {'id':f'g10-aex-l{n:02}-{prefix}{i:02}','prompt':q['problem'],'options':options,'answer_index':pos,'memo':' '.join(q['actions']),'source':f'grade10-algebra-lesson-{n:02}.md'}
def build():
 DOC.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True);manifest=[]
 for n,title in TITLES.items():
  worked=[{k:v for k,v in case(n,i).items() if k!='wrong'} for i in range(1,16)]
  data={'source':f'grade10-algebra-lesson-{n:02}.md','worked':worked,'practice':[choice(n,i,1,'p') for i in range(1,16)],'mastery':[choice(n,i+15,2,'m') for i in range(1,6)],'reassessment':[choice(n,i+18,3,'r') for i in range(1,4)]}
  assert len({q['problem'] for q in worked})==15
  lines=[f'# Grade 10 Topic 1 · Lesson {n}: {title}',f'Authority: [DBE Grade 10 Mathematics ATP]({ATP}), Term 1 Algebraic Expressions. Original Athena questions, not copied exercises.','Status: teacher and browser review required. Reveal one mathematical step at a time and preserve the cumulative written record.']
  for q in worked:lines.extend([f'## {q["id"]}: {q["problem"]}',f'Visual contract: {json.dumps(q["visual"],ensure_ascii=False)}',*[f'{j}. {step}' for j,step in enumerate(q['actions'],1)],f'**Answer:** {q["answer"]}. **Misconception:** {q["misconception"]}'])
  for label,key in [('Practice','practice'),('Mastery','mastery'),('Parallel reassessment','reassessment')]:
   lines.append(f'## {label} answer key')
   for q in data[key]:lines.append(f'- {q["id"]}: {q["prompt"]} Options: {" | ".join(q["options"])}. Correct: {q["options"][q["answer_index"]]}. {q["memo"]}')
  source=DOC/data['source'];source.write_text('\n\n'.join(lines)+'\n',encoding='utf-8');(OUT/f'algebra_{n:02}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  manifest.append({'lesson_id':f'g10-algebra-{n:02}','source':source.name,'source_sha256':sha256(source.read_bytes()).hexdigest(),'worked':15,'practice':15,'mastery':5,'reassessment':3,'status':'teacher_review_required','teacher_approved':False,'browser_accepted':False})
 (DOC/'topic01-acceptance-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
 (DOC/'topic01-batch-acceptance.md').write_text(f'# Grade 10 Topic 1: Algebraic Expressions\n\n[DBE Grade 10 Mathematics ATP]({ATP}) Term 1 specifies real numbers, surds, rounding, binomial by trinomial, factorisation (trinomials, grouping, cubes) and algebraic fractions with cubic denominators. Six authored lessons contain 90 worked, 90 four-choice practice, 30 mastery and 18 reassessments. Grade 10 other topics remain unregistered. Teacher and browser acceptance pending.\n',encoding='utf-8')
if __name__=='__main__':build()
