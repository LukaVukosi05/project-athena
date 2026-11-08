"""Build original, source-backed Grade 10 Term 1 exponent/equation lessons."""
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/curriculum/grade10/exponents-equations-inequalities'
OUT=ROOT/'backend/app/curriculum/grade10/generated'
ATP='https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2023%20ATPs/FET%20Content%20Subjects/Grade%2010/1.580%20ATP%202023-24%20Gr%2010%20Maths%20final.pdf'
TITLES={
 1:'Exponent laws and zero or negative powers',
 2:'Fractional exponents and exponential equations',
 3:'Linear equations with brackets and fractions',
 4:'Quadratic equations by factorisation',
 5:'Simultaneous linear equations',
 6:'Word problems: translate, solve and interpret',
 7:'Literal equations and changing the subject',
 8:'Linear inequalities and interval notation',
 9:'Mixed methods, first-error diagnosis and reassessment',
}
def signed(n):return f'+ {n}' if n>=0 else f'− {-n}'
def case(n,i,variant=0):
 s=i+15*variant
 a=2+s%6;b=1+(s//2)%5;c=2+(s//3)%5;d=1+s%4
 kind=''
 if n==9:
  kind=['exponent','quadratic','simultaneous','literal','inequality'][s%5]
 else:kind=['','exponent','rational','linear','quadratic','simultaneous','word','literal','inequality'][n]
 visual={'family':'grade10_equations','values':{'lesson':n,'kind':kind,'a':a,'b':b,'c':c,'d':d}}
 if kind=='exponent':
  m=2+s%4;k=1+s%3
  if s%3==0:
   problem=f'Simplify (x^{m} · x^{k})/x^{m+k+1} for x ≠ 0.'
   result='1/x';actions=[f'Identify the same base x in both numerator factors.',f'Add numerator exponents: x^{m} · x^{k} = x^{m+k}.',f'Divide like bases: x^{m+k}/x^{m+k+1} = x^−1.', 'Rewrite the negative power using x^−1 = 1/x (x ≠ 0).','Answer: 1/x, x ≠ 0. Multiplying by x gives 1.']
   wrong=['x','0','1'];visual['values'].update(m=m,k=k,form='quotient')
  elif s%3==1:
   problem=f'Simplify (x^{m}y^{k})^2/(x^{2*m}y^{2*k-1}) for x,y ≠ 0.'
   result='y';actions=[f'Square each factor: (x^{m}y^{k})² = x^{2*m}y^{2*k}.',f'Split the quotient into x^{2*m}/x^{2*m} and y^{2*k}/y^{2*k-1}.','Subtract exponents on like bases: x⁰y¹.','Use x⁰ = 1 because x ≠ 0.','Answer: y. Substitute x = y = 2 to check both sides.']
   wrong=['x','xy','1/y'];visual['values'].update(m=m,k=k,form='product')
  else:
   problem=f'Simplify {a}x⁰ + x^−2 for x ≠ 0.'
   result=f'{a} + 1/x²';actions=['The zero exponent applies to x alone and x ≠ 0.',f'Write x⁰ = 1, so {a}x⁰ = {a}.','Rewrite x^−2 = 1/x².','Add the two terms without combining unlike powers.',f'Answer: {a} + 1/x²; x ≠ 0. At x = 1 both forms equal {a+1}.']
   wrong=[f'{a+1}/x²',f'{a} + x²',f'{a+1}'];visual['values'].update(form='zero')
 elif kind=='rational':
  a=2+s%19;visual['values']['a']=a
  base=a*a
  if s%2:
   problem=f'Solve x^(1/2) = {a} for real x.'
   result=f'x = {base}';actions=['The left side denotes the nonnegative square root of x.',f'Square both sides: (√x)² = {a}².',f'Therefore x = {base}.','Check x is nonnegative, as required for a real square root.',f'Answer: x = {base}; √{base} = {a}.']
   wrong=[f'x = {a}',f'x = −{base}',f'x = {base+1}'];visual['values'].update(form='root',base=base)
  else:
   power=3;cube=a**3
   problem=f'Solve x^(1/3) = {a} for real x.'
   result=f'x = {cube}';actions=['A one-third exponent is a cube root.',f'Cube both sides: (∛x)³ = {a}³.',f'Therefore x = {cube}.','Substitute the candidate into the original cube-root equation.',f'Answer: x = {cube}; ∛{cube} = {a}.']
   wrong=[f'x = {a}',f'x = {a*a}',f'x = −{cube}'];visual['values'].update(form='cube_root',base=cube)
 elif kind=='linear':
  target=a+2;left=a*(target+b);rhs=left+c
  problem=f'Solve {a}(x + {b}) + {c} = {rhs}.'
  result=f'x = {target}';actions=[f'Expand the left bracket: {a}x + {a*b} + {c} = {rhs}.',f'Combine constants: {a}x + {a*b+c} = {rhs}.',f'Subtract {a*b+c} from both sides: {a}x = {a*target}.',f'Divide both sides by {a}: x = {target}.',f'Answer: x = {target}. Substitute: {a}({target}+{b})+{c} = {rhs}.']
  wrong=[f'x = {target+1}',f'x = {target-1}',f'x = {target+2}'];visual['values'].update(target=target,rhs=rhs,form='balance')
 elif kind=='quadratic':
  r=a; t=-(b+1) if s%2 else b+1
  if t==r:t+=2
  coefficient=-(r+t);constant=r*t
  problem=f'Solve x² {signed(coefficient)}x {signed(constant)} = 0.'
  result=f'x = {r} or x = {t}'
  actions=[f'Find two numbers with sum {coefficient} and product {constant}: {-r} and {-t}.',f'Factor: (x − {r})(x {signed(-t)}) = 0.','A product is zero when at least one factor is zero.',f'Solve both branches: x = {r} or x = {t}.',f'Answer: {result}. Substitute each value into the original quadratic to obtain zero.']
  wrong=[f'x = {r} only',f'x = {t} only',f'x = −{r} or x = {t}'];visual['values'].update(r=r,t=t,coefficient=coefficient,constant=constant,form='two_roots')
 elif kind=='simultaneous':
  x=a;y=b;u=x+y;v=x-y
  problem=f'Solve simultaneously: x + y = {u} and x − y = {v}.'
  result=f'x = {x}, y = {y}'
  actions=[f'Write both equations in aligned columns: x+y={u} and x−y={v}.',f'Add the equations: 2x = {u+v}.',f'Divide by 2: x = {x}.',f'Substitute into x+y={u}: y={u}−{x}={y}.',f'Answer: {result}. Check x−y={x}−{y}={v}.']
  wrong=[f'x = {x+1}, y = {y-1}',f'x = {u}, y = {v}',f'x = {x}, y = −{y}'];visual['values'].update(x=x,y=y,u=u,v=v,form='elimination')
 elif kind=='word':
  sub=s%3
  if sub==0:
   total=2*a+b
   problem=f'Two identical notebooks plus a R{b} fee cost R{total} altogether. Write an equation for the notebook price p and solve.'
   result=f'p = R{a}';actions=[f'The two notebook prices and fee form 2p+{b}={total}.',f'Subtract the fee: 2p={total-b}.',f'Divide by two: p={a}.',f'Attach the unit: each notebook costs R{a}.',f'Answer: {result}; 2({a})+{b}={total}.']
   wrong=[f'p = R{total}',f'p = R{total-b}',f'p = R{a+1}'];visual['values'].update(form='purchase',total=total)
  elif sub==1:
   area=a*b;perim=2*(a+b)
   problem=f'A rectangle has perimeter {perim} cm. Its length is {a} cm. Find its width w.'
   result=f'w = {b} cm';actions=[f'Use perimeter P=2(length+width): {perim}=2({a}+w).',f'Divide by 2: {perim//2}={a}+w.',f'Subtract {a}: w={b}.',f'Check width is positive and the units are centimetres.',f'Answer: {result}; 2({a}+{b})={perim}.']
   wrong=[f'w = {perim} cm',f'w = {perim//2} cm',f'w = {b+1} cm'];visual['values'].update(form='rectangle',perimeter=perim)
  else:
   p=a+b;q=b;cost=2*p+q
   problem=f'Two adult tickets and one child ticket cost R{cost}. An adult ticket costs R{a} more than a child ticket. Find both prices.'
   result=f'adult R{p}, child R{q}'
   actions=[f'Let adult price A and child price C. Write 2A+C={cost} and A−C={a}.',f'From A−C={a}, substitute A=C+{a} into the first equation.',f'2(C+{a})+C={cost}, hence 3C={3*q}.',f'C={q}; then A=C+{a}={p}.',f'Answer: {result}. Check 2({p})+{q}={cost}.']
   wrong=[f'adult R{q}, child R{p}',f'adult R{cost}, child R{q}',f'adult R{p+1}, child R{q}'];visual['values'].update(form='tickets',total=cost)
 elif kind=='literal':
  if s%2:
   width=a+b
   problem=f'A trapezium has parallel sides {a} cm and {b} cm. Its area is A cm². Make the height h the subject of A = ½({a}+{b})h.'
   result=f'h = 2A/{width}'
   actions=[f'Start with A = ½({a}+{b})h.',f'Add the parallel sides: A = ({width}/2)h.',f'Multiply both sides by 2: 2A = {width}h.',f'Divide both sides by {width}: h = 2A/{width}.',f'Answer: {result}. Substituting into ½({width})h recovers A.']
   wrong=[f'h = A/(2·{width})',f'h = A/{width}',f'h = {width}A/2'];visual['values'].update(form='trapezium',width=width)
  else:
   a=2+s%19;visual['values']['a']=a
   problem=f'In v = u + {a}t, make t the subject.'
   result=f't = (v − u)/{a}'
   actions=[f'Start with v = u + {a}t.','Subtract u from both sides: v − u = '+f'{a}t.',f'The coefficient of t is {a}.',f'Divide both sides by {a}.',f'Answer: {result}; u + {a}((v − u)/{a}) = v.']
   wrong=[f't = (v + u)/{a}',f't = {a}(v − u)',f't = (u − v)/{a}'];visual['values'].update(form='motion')
 elif kind=='inequality':
  bound=a+1;neg=s%2==0
  if neg:
   k=2+s%3;offset=b;rhs=offset-k*bound
   problem=f'Solve {offset} − {k}x ≥ {rhs}. Give interval notation and show the solution on a number line.'
   result=f'x ≤ {bound}; (−∞, {bound}]'
   actions=[f'Subtract {offset} from both sides: −{k}x ≥ −{k*bound}.',f'Divide by −{k}; reverse ≥ to ≤: x ≤ {bound}.',f'Mark a filled circle at {bound} because equality is allowed.',f'Shade left and write the interval (−∞, {bound}].',f'Answer: {result}. Test x={bound} in the original and x={bound+1} outside.']
   wrong=[f'x ≥ {bound}; [{bound}, ∞)',f'x < {bound}; (−∞, {bound})',f'x ≤ {bound}; [{bound}, ∞)'];visual['values'].update(bound=bound,closed=True,direction='left',form='negative_divisor',k=k,offset=offset,rhs=rhs)
  else:
   k=2+s%3;offset=b;rhs=k*bound+offset
   problem=f'Solve {k}x + {offset} > {rhs}. Give interval notation and show the solution on a number line.'
   result=f'x > {bound}; ({bound}, ∞)'
   actions=[f'Subtract {offset} from both sides: {k}x > {k*bound}.',f'Divide by positive {k}, preserving >: x > {bound}.',f'Mark an open circle at {bound} because equality is excluded.',f'Shade right and write the interval ({bound}, ∞).',f'Answer: {result}. Test x={bound+1} inside and x={bound} outside.']
   wrong=[f'x ≥ {bound}; [{bound}, ∞)',f'x < {bound}; (−∞, {bound})',f'x > {bound}; [{bound}, ∞)'];visual['values'].update(bound=bound,closed=False,direction='right',form='positive_divisor',k=k,offset=offset,rhs=rhs)
 else:raise AssertionError(kind)
 assert len(actions)==5 and len({result,*wrong})==4,(n,i,result,wrong)
 visual['values']['result']=result
 return {'id':f'g10-eei-l{n:02}-w{i:02}' if not variant else f'g10-eei-l{n:02}-v{variant}-w{i:02}',
 'problem':problem,'actions':actions,'answer':result,'check':actions[-1],
 'visual':visual,'lesson':n,'misconception':'Check the first sign, branch, equation, unit or domain restriction against the original question.',
 'wrong':wrong,'difficulty':'foundation' if i<=2 else 'easy' if i<=5 else 'standard' if i<=9 else 'intermediate' if i<=12 else 'exam'}
def choice(n,i,variant,label):
 q=case(n,i,variant);choices=[q['answer'],*q['wrong']];pos=i%4
 choices=choices[-pos:]+choices[:-pos] if pos else choices
 return {'id':f'g10-eei-l{n:02}-{label}{i:02}','prompt':q['problem'],
 'options':choices,'answer_index':pos,'memo':' '.join(q['actions']),
 'source':f'grade10-eei-lesson-{n:02}.md'}
def build():
 DOC.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True);manifest=[]
 for n,title in TITLES.items():
  worked=[{k:v for k,v in case(n,i).items() if k!='wrong'} for i in range(1,16)]
  data={'source':f'grade10-eei-lesson-{n:02}.md','worked':worked,
   'practice':[choice(n,i,1,'p') for i in range(1,16)],
   'mastery':[choice(n,i+15,2,'m') for i in range(1,6)],
   'reassessment':[choice(n,i+20,3,'r') for i in range(1,4)]}
  # Some literal formulae recur with changed numbers; all authored examples must vary.
  assert len({q['problem'] for q in worked})>=10,n
  lines=[f'# Grade 10 Topic 2 · Lesson {n}: {title}',
    f'Authority: [DBE Grade 10 Mathematics ATP]({ATP}), Term 1.',
    'Original Athena examples. Teacher and browser review required. Show one stage at a time and retain the cumulative record.']
  for q in worked:
   lines += [f'## {q["id"]}: {q["problem"]}',f'Visual contract: {json.dumps(q["visual"],ensure_ascii=False)}',
    *[f'{j}. {a}' for j,a in enumerate(q['actions'],1)],f'**Answer:** {q["answer"]}. **Misconception:** {q["misconception"]}']
  for label,key in [('Practice','practice'),('Mastery','mastery'),('Parallel reassessment','reassessment')]:
   lines.append(f'## {label} answer key')
   for q in data[key]:
    lines.append(f'- {q["id"]}: {q["prompt"]} Options: {" | ".join(q["options"])}. Correct: {q["options"][q["answer_index"]]}. {q["memo"]}')
  path=DOC/data['source'];path.write_text('\n\n'.join(lines)+'\n',encoding='utf-8')
  (OUT/f'eei_{n:02}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  manifest.append({'lesson_id':f'g10-eei-{n:02}','source':path.name,'source_sha256':sha256(path.read_bytes()).hexdigest(),'worked':15,'practice':15,'mastery':5,'reassessment':3,'status':'teacher_review_required','teacher_approved':False,'browser_accepted':False})
 (DOC/'topic02-acceptance-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
 (DOC/'topic02-batch-acceptance.md').write_text(f'# Grade 10 Topic 2: Exponents, Equations and Inequalities\n\n[DBE Grade 10 Mathematics ATP]({ATP}) Term 1 covers integer and rational exponent laws; linear, quadratic, simultaneous and literal equations; applied problems; inequalities, number lines and interval notation. Nine authored lessons contain 135 worked examples, 135 four-choice practice, 45 mastery and 27 reassessments. Source implementation awaits teacher and live browser acceptance. Formula rearrangement is a reusable algebraic procedure illustrated by two formulas; it needs broader teacher review.\n',encoding='utf-8')
if __name__=='__main__':build()
