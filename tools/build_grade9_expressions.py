"""Author original Grade 9 algebraic-expression banks with exact arithmetic."""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json
import math
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/curriculum/grade9/algebraic-expressions'
OUT=ROOT/'backend/app/curriculum/grade9/generated'
ATP='https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2026%20ATPs/2026_ATP_Mathematics_Grade%209.pdf'
TITLES={1:'Algebraic language and term classification',2:'Collecting like terms with fractions and decimals',
 3:'Distributing monomials across polynomials',4:'Products and squares of binomials',
 5:'Polynomial division and substitution',6:'Common-factor factorisation',
 7:'Difference of two squares',8:'Trinomials and algebraic fractions',
 9:'Mixed expressions and first-error repair'}
x=s.Symbol('x')

def fmt(value):
    return str(value).replace('**2','²').replace('**3','³').replace('*','×').replace('-', '−')

def same(a,b):return s.simplify(a-b)==0

def product(a,b):return fmt(s.Mul(a,b,evaluate=False))

def case(n,index):
    # Stable, distinct values; late examples use signed values, more terms and restrictions.
    a=2+(index%5);b=1+(index%7);c=2+(index%4);k=2+(index%3)
    sign=-1 if index%3==0 else 1
    advanced=index>=12
    if n==1:
        terms=[sign*a*x*x,b*x,sign*c]+([k*x] if advanced else [])
        expression=s.Add(*terms,evaluate=False)
        if index%3==0:
            prompt=f'In {fmt(expression)}, identify the coefficient of x².';answer=fmt(sign*a);wrong=[fmt(b),fmt(c),fmt(-sign*a)]
        elif index%3==1:
            prompt=f'How many written terms does {fmt(expression)} have before collecting like terms?';answer=str(len(terms));wrong=[str(len(terms)+1),str(len(terms)-1),str(len(terms)+2)]
        else:
            prompt=f'Identify the constant term in {fmt(expression)}.';answer=fmt(sign*c);wrong=[fmt(b),fmt(sign*a),fmt(-sign*c)]
        steps=[f'Keep the original expression {fmt(expression)} visible.',
               'Separate terms at each top-level plus or minus sign; the sign belongs to its term.',
               f'Identify the requested feature: {answer}.',
               f'Check the expression {fmt(expression)} against that classification. The answer is {answer}.']
        family='terms';givens=[fmt(t) for t in terms];restriction=''
    elif n==2:
        p=F(sign*a,2 if index%2 else 4);q=F(b,4 if index%2 else 2)
        r=F(c,2);h=F(k,4)
        shown=lambda value:format(float(value),'.2f').rstrip('0').rstrip('.') if index%4==0 else str(value)
        expression=f'{shown(p)}x + {shown(q)}x + {shown(r)} − {shown(h)}'
        result=p+q;constant=r-h
        prompt=f'Simplify {expression}, keeping exact fractions.'
        answer=f'{result}x {"+" if constant>=0 else "−"} {abs(constant)}'
        wrong=[f'{p-q}x + {r+h}',f'{p+q+r}x − {h}',f'{p+q}x + {r+h}']
        steps=[f'Underline like terms in {expression}: the x terms together and constants together.',
               f'Convert denominators when needed and collect the x coefficient: {shown(p)} + {shown(q)} = {result}.',
               f'Collect the constants separately: {shown(r)} − {shown(h)} = {constant}; so the result is {answer}.',
               f'Check at x = 2: both {expression} and {answer} equal {2*result+constant}.']
        family='like_terms';givens=[f'{shown(p)}x',f'{shown(q)}x',shown(r),f'−{shown(h)}'];restriction=''
    elif n==3:
        factor=sign*a*x if index%2 else sign*a
        inside=b*x+c if not advanced else b*x*x+c*x+k
        original=product(factor,inside);expanded=s.expand(factor*inside)
        prompt=f'Expand {original} and collect like terms.';answer=fmt(expanded)
        wrong=[fmt(s.expand(factor*b*x+c)),fmt(-expanded),fmt(s.expand(factor*(b*x-c)))]
        parts=list(s.Add.make_args(inside))
        steps=[f'Draw one distribution arrow from {fmt(factor)} to each of the {len(parts)} terms in {fmt(inside)}.',
               f'Multiply the factor into every term: '+', '.join(f'{product(factor,t)} = {fmt(s.expand(factor*t))}' for t in parts)+'.',
               f'Combine the products without dropping a sign: {answer}.',
               f'Check at x = 1: the original product and {answer} both give {expanded.subs(x,1)}.']
        family='distribution';givens=[fmt(factor)]+[fmt(t) for t in parts];restriction=''
    elif n==4:
        left=x+sign*a;right=x+(sign*a if index%4==0 else b)
        original=product(left,right);expanded=s.expand(left*right)
        prompt=f'Expand {original} using all four area-model cells.';answer=fmt(expanded)
        wrong=[fmt(s.expand(x*x+sign*a*b)),fmt(s.expand(x*x+(sign*a+b)*x)),fmt(s.expand((x+sign*a)*(x-b)))]
        steps=[f'Label the rectangle rows x and {sign*a}; columns x and {fmt(right-x)}.',
               f'Fill the four cells: x², {fmt((right-x)*x)}, {fmt(sign*a*x)}, {fmt(sign*a*(right-x))}.',
               f'Add the cell areas and collect like terms: {answer}.',
               f'Check at x = 1: the original brackets and {answer} both give {expanded.subs(x,1)}.']
        family='area';givens=['x',str(sign*a),'x',fmt(right-x)];restriction=''
    elif n==5:
        if index%2:
            numerator=sign*a*x*x+b*x;divisor=x
            prompt=f'Simplify ({fmt(numerator)}) ÷ x for x ≠ 0.';result=s.expand(numerator/divisor)
            answer=fmt(result);wrong=[fmt(numerator),fmt(sign*a*x+b*x),fmt(sign*a*x-b)]
            steps=[f'Show the numerator {fmt(numerator)} as two separate terms above the common divisor x.',
                   f'Divide the first term: {fmt(sign*a*x*x)} ÷ x = {fmt(sign*a*x)}.',
                   f'Divide the second term: {fmt(b*x)} ÷ x = {b}; combine to obtain {answer}.',
                   f'Check by multiplying {answer} by x to recover {fmt(numerator)}; x ≠ 0.']
            restriction='x ≠ 0';givens=[fmt(sign*a*x*x),fmt(b*x),'x'];family='division'
        elif index%4==0:
            divisor=k;numerator=k*(sign*a*x*x+b*x+c);result=s.expand(numerator/divisor)
            prompt=f'Simplify ({fmt(numerator)}) ÷ {divisor}.';answer=fmt(result)
            wrong=[fmt(numerator),fmt(result+c),fmt(result-b*x)]
            steps=[f'Copy every term of {fmt(numerator)} above the shared divisor {divisor}.',
                   f'Divide the squared term and the x term separately by {divisor}.',
                   f'Divide the constant too; the complete quotient is {answer}.',
                   f'Check: multiply {answer} by {divisor} to recover {fmt(numerator)}.']
            restriction='';givens=[fmt(t) for t in s.Add.make_args(numerator)]+[str(divisor)];family='division'
        else:
            expression=sign*a*x*x+b*x+c;v=(-2 if advanced else 2+index%3);result=expression.subs(x,v)
            prompt=f'Evaluate {fmt(expression)} when x = {v}.';answer=str(result)
            wrong=[str(result+2),str(result-2),str(-result)]
            steps=[f'Copy {fmt(expression)} and place x = {v} under every occurrence of x.',
                   f'Evaluate the square and signed products: {sign*a}×({v})² = {sign*a*v*v}, {b}×({v}) = {b*v}.',
                   f'Add the three terms: {sign*a*v*v} + ({b*v}) + {c} = {answer}.',
                   f'Check by substitution into the original {fmt(expression)}: {answer}.']
            restriction='';givens=[fmt(sign*a*x*x),fmt(b*x),str(c),str(v)];family='substitution'
    elif n==6:
        common=sign*k*x if index%2 else sign*k
        coefficient=c+1 if advanced and math.gcd(a,b,c)>1 else c
        inner=a*x+b if not advanced else a*x*x+b*x+coefficient
        divisor=math.gcd(a,b,coefficient) if advanced else math.gcd(a,b)
        if divisor>1:
            common*=divisor;inner/=divisor
        original=s.expand(common*inner)
        prompt=f'Factorise {fmt(original)} completely by taking out a common factor.'
        answer=product(common,inner)
        wrong=[product(common,inner+1),product(-common,inner),product(common,inner-b)]
        steps=[f'Mark each term in {fmt(original)} and find the largest shared numerical and variable factor.',
               f'Take out {fmt(common)}; divide each original term by it to form {fmt(inner)}.',
               f'Write the factored result {answer}, preserving every sign.',
               f'Check: distributing {fmt(common)} into {fmt(inner)} recovers {fmt(original)}.']
        family='common_factor';givens=[fmt(t) for t in s.Add.make_args(original)];restriction=''
    elif n==7:
        left=a*x;right=b
        original=left*left-right*right
        if advanced: original=k*original
        prompt=f'Factorise {fmt(original)} completely.'
        gcd=math.gcd(a,b);outer=(k if advanced else 1)*gcd*gcd
        reduced_left=(a//gcd)*x;reduced_right=b//gcd
        expression=(reduced_left-reduced_right)*(reduced_left+reduced_right)*outer
        answer=(f'{outer}×' if outer>1 else '')+product(reduced_left-reduced_right,reduced_left+reduced_right)
        wrong=[product(reduced_left-reduced_right,reduced_left-reduced_right),product(reduced_left+reduced_right,reduced_left+reduced_right),product(reduced_left-reduced_right,reduced_left+reduced_right+1)]
        steps=[f'Extract the greatest common numerical factor {outer} from {fmt(original)}.' if outer>1 else f'Identify {fmt(left*left)} − {right*right} as a difference of two squares.',
               f'The remaining square roots are {fmt(reduced_left)} and {reduced_right}; form the conjugates {fmt(reduced_left-reduced_right)} and {fmt(reduced_left+reduced_right)}.',
               f'Keep the extracted factor: {answer}.',
               f'Check by expanding the brackets: {fmt(s.expand(expression))}, the original expression.']
        family='difference_squares';givens=[fmt(left*left),str(right*right)]+([str(k)] if advanced else []);restriction=''
    elif n==8:
        p=sign*a;q=b;original=s.expand((x+p)*(x+q))
        if index%3:
            outer=k if advanced else 1
            original*=outer
            prompt=f'Factorise {fmt(original)}.'
            answer=(f'{outer}×' if outer>1 else '')+product(x+p,x+q)
            wrong=[product(x-p,x+q),product(x+p,x-q),product(x+p+1,x+q)]
            steps=[f'Write the trinomial {fmt(original)} in descending powers'+(f' and extract common factor {outer}' if outer>1 else f' and read its constant {p*q}')+'.',
                   f'Find numbers {p} and {q} whose product is {p*q} and sum is {p+q}.',
                   f'Place them in the two brackets: {answer}.',
                   f'Check by expanding: {answer} = {fmt(original)}.']
            family='trinomial';restriction='';givens=[fmt(original),str(p),str(q)]
        else:
            denominator=x+p
            prompt=f'Simplify ({fmt(original)})/({fmt(denominator)}), stating any restriction.'
            answer=f'{fmt(x+q)}; x ≠ {-p}'
            wrong=[f'{fmt(x+p)}; x ≠ {-p}',f'{fmt(x+q)}; x ≠ {-q}',f'{fmt(x+q)}; no restriction']
            steps=[f'Keep the original denominator {fmt(denominator)} visible: it is zero at x = {-p}, so x ≠ {-p}.',
                   f'Factor the numerator {fmt(original)} as {product(x+p,x+q)}.',
                   f'Cancel the shared factor {fmt(denominator)} only for x ≠ {-p}, leaving {fmt(x+q)}.',
                   f'Check at x = 1 unless excluded: the original fraction equals {fmt(x+q)}; retain x ≠ {-p}.']
            family='fraction';restriction=f'x ≠ {-p}';givens=[fmt(original),fmt(denominator)]
    else:
        left=x+sign*a;right=x+b;original=product(left,right);correct=s.expand(left*right)
        claimed=correct-sign*a*x
        prompt=f'A learner writes {original} = {fmt(claimed)}. Identify the first missing product and correct the expansion.'
        answer=fmt(correct)
        wrong=[fmt(claimed),fmt(correct-sign*a*b),fmt(correct+b*x)]
        steps=[f'Keep the learner’s claim {fmt(claimed)} next to the original {original}.',
               f'Fill the area cells: x², {fmt(b*x)}, {fmt(sign*a*x)}, {sign*a*b}. The first missing product is {fmt(sign*a*x)}.',
               f'Add all four cells to repair the result: {answer}.',
               f'Check at x = 1: {original} and {answer} both give {correct.subs(x,1)}.']
        family='diagnosis';givens=['x',str(sign*a),'x',str(b)];restriction=''
    # Use distinct distractors without silently accepting equivalent forms.
    if len({answer,*wrong})<4:
        wrong=[f'{answer} + {delta}' for delta in (1,2,3)]
    visual=dict(family=family,givens=givens,restriction=restriction,answer=answer,
                rows=[str(v) for v in givens[:2]],columns=[str(v) for v in givens[2:4]],
                factor=fmt(factor) if n==3 else fmt(common) if n==6 else None,
                conjugates=[fmt(reduced_left-reduced_right),fmt(reduced_left+reduced_right)] if n==7 else None,
                claim=fmt(claimed) if n==9 else None)
    return dict(problem=prompt,actions=steps,answer=answer,wrongs=wrong,
        wrong_methods=['A term or factor was omitted.','A sign or factor was changed.','The original restriction or operation was lost.'],
        visual=visual,misconception=f'expressions-{family}',check=steps[-1])

def private(c,n,kind,index):
    options=c['wrongs'][:];key=(index-1)%4;options.insert(key,c['answer'])
    return dict(id=f'g9-aex-l{n:02}-{kind}{index:02}',prompt=c['problem'],options=options,answer_index=key,
      memo=' '.join(c['actions']),misconception=c['misconception'],
      option_rationales={v:('Correct: '+c['check'] if v==c['answer'] else 'Incorrect: '+c['wrong_methods'][c['wrongs'].index(v)]) for v in options})

def build(n):
    worked=[case(n,i) for i in range(1,16)]
    # Disjoint problem bank; changed values and seeds beyond worked range.
    other=[];seen={c['problem'] for c in worked}
    for seed in range(16,150):
        candidate=case(n,seed)
        if candidate['problem'] not in seen:
            seen.add(candidate['problem']);other.append(candidate)
        if len(other)==23:break
    assert len({c['problem'] for c in [*worked,*other]})==38,(n,'duplicate prompts')
    filename=f'lesson-{n:02}-'+TITLES[n].lower().replace(',','').replace(' ','-')+'.md'
    data=dict(source=filename,worked=[{**c,'id':f'g9-aex-l{n:02}-w{i:02}',
        'difficulty':'foundation' if i<=2 else 'easy' if i<=5 else 'standard' if i<=9 else 'exam' if i<=12 else 'advanced'} for i,c in enumerate(worked,1)],
        practice=[private(c,n,'p',i) for i,c in enumerate(other[:15],1)],
        mastery=[private(c,n,'m',i) for i,c in enumerate(other[15:20],1)],
        reassessment=[private(c,n,'r',i) for i,c in enumerate(other[20:],1)])
    lines=[f'# Grade 9 Topic 6 · Lesson {n}: {TITLES[n]}','',
        'Status: authored preview awaiting teacher and live-browser review. Original Athena examples.','',
        'Scope: DBE 2026 Grade 9 Mathematics ATP, Terms 1–2.',ATP,'',
        'Whiteboard: preserve givens and prior written results; show one mathematical operation at a time.','',
        '## Worked examples']
    for c in data['worked']:
        lines+=['',f"### {c['id']} · {c['difficulty']}",f"Question: {c['problem']}",
          f"Visual: {json.dumps(c['visual'],ensure_ascii=False)}",
          *[f'{i}. {action}' for i,action in enumerate(c['actions'],1)],
          f"Answer: {c['answer']}",f"Misconception: {c['misconception']}"]
    for kind in ('practice','mastery','reassessment'):
        lines+=['',f'## {kind.title()} · private answer keys and rationales']
        for item in data[kind]:
            lines+=['',f"### {item['id']}",f"Question: {item['prompt']}",
              *[f'{chr(65+i)}. {option}' for i,option in enumerate(item['options'])],
              f"Key: {chr(65+item['answer_index'])}",f"Memo: {item['memo']}",
              *[f'Distractor {v}: {reason}' for v,reason in item['option_rationales'].items() if reason.startswith('Incorrect:')]]
    DOC.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    (DOC/filename).write_text('\n'.join(lines)+'\n',encoding='utf-8')
    (OUT/f'expressions_{n:02}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return dict(lesson_id=f'g9-expressions-{n:02}',source=filename,
      source_sha256=sha256((DOC/filename).read_bytes()).hexdigest(),
      **{f'{kind}_ids':[c['id'] for c in data[kind]] for kind in ('worked','practice','mastery','reassessment')},
      **{f'{kind}_count':len(data[kind]) for kind in ('worked','practice','mastery','reassessment')},
      status='teacher_review_required',browser_accepted=False,teacher_approved=False)

if __name__=='__main__':
    manifest=[build(n) for n in range(1,10)]
    (DOC/'topic6-acceptance-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Authored',len(manifest),'lessons:',sum(x['worked_count'] for x in manifest),'worked,',sum(x['practice_count'] for x in manifest),'practice')
