"""Author the complete Grade 9 integer topic as static, checked question banks.

The DBE ATP defines the skills; these original Athena questions are not copied exam items.
"""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/curriculum/grade9/integers'
OUT=ROOT/'backend/app/curriculum/grade9/generated'
TITLES={1:'Ordering and four operations',2:'Sign rules and integer properties',
        3:'Squares, cubes and integer roots',4:'Multi-operation integer contexts',
        5:'First-error diagnosis and reassessment'}
ATP='https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2026%20ATPs/2026_ATP_Mathematics_Grade%209.pdf'
WRONG_REASONS={
 'negative-order':['Reads the number line right to left.','Swaps the two smallest signed values.','Swaps the two greatest signed values.'],
 'negative-subtraction':['Reverses the sign of the calculated difference.','Adds the subtrahend instead of its opposite.','Makes an extra step after reaching the correct value.'],
 'sign-rule':['Attaches the opposite sign to a correct magnitude.','Changes the magnitude by one.','Changes the magnitude by two.'],
 'distributive-term':['Multiplies only the first bracket term.','Subtracts the second term after distribution.','Adds the three original values without multiplying.'],
 'additive-inverse':['Stops before adding the inverse.','Subtracts the inverse instead of adding it.','Discards the untouched starting term.'],
 'regroup-sign':['Changes the sign of the last term while regrouping.','Changes the sign of the middle term.','Omits the first term from the sum.'],
 'common-factor':['Subtracts one bracket term instead of adding.','Leaves the second term outside the common factor.','Adds the terms without the common multiplication.'],
 'negative-base-square':['Keeps a negative sign after multiplying two negative bases.','Multiplies the base by the exponent.','Reports only the base magnitude.'],
 'odd-power-sign':['Drops the negative sign after three negative factors.','Multiplies the base by three instead of cubing.','Stops after multiplying only two factors.'],
 'principal-root':['Chooses the negative root for the principal square root.','Doubles the candidate instead of squaring it.','Leaves the original square unchanged.'],
 'cube-root-sign':['Reverses the sign of the cube root.','Multiplies the root by three.','Returns the original cube instead of its root.'],
 'brackets-first':['Multiplies before completing the bracket.','Treats the plus sign in the bracket as a minus.','Reverses the sign of a correct product.'],
 'credit-debit':['Adds a payment instead of subtracting it.','Subtracts a receipt instead of adding it.','Stops after the receipt without the payment.'],
 'temperature-direction':['Moves up for a fall in temperature.','Moves down for the stated positive change.','Stops before the final fall.'],
 'game-order':['Adds the adjustment to each round before multiplying.','Applies the adjustment in the opposite direction.','Omits the final adjustment.'],
 'first-wrong-subtraction':['Keeps the original incorrect result.','Stops at the unchanged first value.','Reverses the sign of the repaired result.'],
 'first-wrong-product-sign':['Keeps the learner’s incorrect sign.','Adds the signed factors instead of multiplying.','Adds magnitudes instead of multiplying.'],
 'first-wrong-order':['Keeps the learner’s bracketed answer.','Stops before multiplication.','Reports the product without the added term.'],
 'first-wrong-square-sign':['Keeps the learner’s negative square.','Multiplies the negative base by two.','Keeps only the magnitude of the base.'],
}

def signed(n):return f'({n})' if n<0 else str(n)
def make(prompt,givens,steps,answer,visual,tag,wrong,check):
    answer=str(answer);wrong=[str(x) for x in wrong]
    assert len(steps)>=3 and len(set([answer,*wrong]))==4 and tag in WRONG_REASONS,(prompt,answer,wrong)
    return dict(problem=prompt,givens=[str(x) for x in givens],actions=[*steps,'Check: '+check],
                answer=answer,wrongs=wrong,wrong_methods=WRONG_REASONS[tag],
                visual=visual,misconception=tag,check='Check: '+check)

def compare(a,b,c):
    values=[a,b,c];ordered=sorted(values);answer=', '.join(map(str,ordered))
    return make(f'Arrange {a}, {b} and {c} in ascending order.',values,
        ['Mark zero as the reference on the signed number line.',
         'Place each value at its exact tick: '+', '.join(map(str,values))+'.',
         'Read the ticks from left to right: '+answer+'.'],answer,
        {'family':'line','values':values,'path':[ordered[0],ordered[1],ordered[2]],'labels':['first','second','third']},
        'negative-order',[', '.join(map(str,sorted(values,reverse=True))),', '.join(map(str,[ordered[1],ordered[0],ordered[2]])),', '.join(map(str,[ordered[0],ordered[2],ordered[1]]))],
        f'{ordered[0]} < {ordered[1]} < {ordered[2]}.')

def operation(a,b,op):
    result={'+':a+b,'−':a-b,'×':a*b,'÷':a//b}[op]
    if op=='÷':assert b and a%b==0
    expression=f'{signed(a)} {op} {signed(b)}';tag='negative-subtraction' if op=='−' else 'sign-rule'
    if op=='+':
        steps=[f'Start at {a} on the number line.',f'{"Move right" if b>=0 else "Move left"} {abs(b)} units for adding {b}.',f'Land on {result}: {expression} = {result}.']
        path=[a,result]
    elif op=='−':
        steps=[f'Start with {a} and keep the subtraction sign.',f'Rewrite subtracting {signed(b)} as adding its opposite, {signed(-b)}.',f'Calculate {a} + {signed(-b)} = {result}.']
        path=[a,result]
    else:
        steps=[f'Read the two signed factors in {expression}.',f'{"Equal" if (a<0)==(b<0) else "Different"} signs give a {"positive" if result>=0 else "negative"} answer.',f'Calculate magnitudes {abs(a)} {op} {abs(b)} = {abs(result)}, then attach the sign: {result}.']
        path=[0,result]
    return make(f'Calculate {expression}.',[a,b,op],steps,result,
        {'family':'line' if op in '+−' else 'tiles','values':[a,b],'path':path,'operator':op,'magnitude':abs(result)},tag,
        [abs(result) if result<0 else -result, a+b if op=='−' else result+(1 if result<0 else -1),a-b if op=='+' else result+(-2 if result<0 else 2)],
        f'{expression} = {result}.')

def property_case(a,b,c,kind):
    if kind=='distributive':
        result=a*(b+c);partial=[a*b,a*c]
        prompt=f'Expand and evaluate {signed(a)} × ({signed(b)} + {signed(c)}).'
        steps=[f'The bracket contains two terms: {b} and {c}.',f'Distribute {a} to both: {a}×{signed(b)} + {a}×{signed(c)} = {partial[0]} + {signed(partial[1])}.',f'Add the signed products: {result}.']
        wrong=[a*b+c,a*(b-c),a+b+c];tag='distributive-term';values=[a,b,c]
    elif kind=='inverse':
        result=a;prompt=f'Evaluate {signed(a)} + {signed(b)} + {signed(-b)}.'
        steps=[f'Find the opposite pair {b} and {-b}.',f'Add the inverses: {b} + {signed(-b)} = 0.',f'Adding zero leaves {a}.']
        wrong=[a+b,a-b,0];tag='additive-inverse';values=[a,b,-b]
    elif kind=='associative':
        result=a+b+c;prompt=f'Evaluate ({signed(a)} + {signed(b)}) + {signed(c)} by regrouping.'
        steps=[f'Keep every signed term: {a}, {b}, {c}.',f'Regroup as {a} + ({signed(b)} + {signed(c)}) without changing term signs.',f'{b} + {signed(c)} = {b+c}; then {a} + {signed(b+c)} = {result}.']
        wrong=[a+b-c,a-b+c,b+c];tag='regroup-sign';values=[a,b,c]
    else:
        result=a*b+a*c;prompt=f'Use a property to calculate {signed(a)}×{signed(b)} + {signed(a)}×{signed(c)}.'
        steps=[f'Both terms contain a factor of {a}.',f'Factor the shared integer: {a}×({signed(b)}+{signed(c)}).',f'Add inside the bracket, then multiply: {a}×{signed(b+c)} = {result}.']
        wrong=[a*(b-c),a*b+c,a+b+c];tag='common-factor';values=[a,b,c]
    return make(prompt,values,steps,result,{'family':'tiles','values':values,'operator':kind,'path':[0,result]},tag,wrong,
        f'Substituting the original signed values also gives {result}.')

def power_root(n,kind,offset=0):
    if kind=='square':
        result=n*n;prompt=f'Calculate ({n})².';steps=[f'The base is the entire signed number ({n}).',f'Expand as ({n})×({n}).',f'Two negative factors have a positive product: {result}.']
        wrong=[-result,2*n,abs(n)];tag='negative-base-square';visual={'family':'tiles','values':[n,n],'operator':'square','path':[n,result]}
    elif kind=='cube':
        result=n**3;prompt=f'Calculate ({n})³.';steps=[f'The base {n} is repeated three times.',f'Expand ({n})×({n})×({n}).',f'The first pair gives {n*n}; multiply by {n} to obtain {result}.']
        wrong=[-result,3*n,n*n];tag='odd-power-sign';visual={'family':'tiles','values':[n,n,n],'operator':'cube','path':[n,n*n,result]}
    elif kind=='root':
        result=abs(n);square=n*n;prompt=f'Find the principal square root of {square}.'
        steps=[f'Find a nonnegative number whose square is {square}.',f'{result}×{result} = {square}.',f'The principal square root is {result}, not a pair of solutions.']
        wrong=[-result,2*result,square];tag='principal-root';visual={'family':'root','values':[square,result],'operator':'square_root','path':[square,result]}
    else:
        result=n;cube=n**3;prompt=f'Calculate ∛({cube}).'
        steps=[f'A cube root is the number repeated as a product of three equal factors.',f'{n}×{n}×{n} = {cube}.',f'Therefore ∛({cube}) = {n}.']
        wrong=[-n,3*n,cube];tag='cube-root-sign';visual={'family':'root','values':[cube,n],'operator':'cube_root','path':[cube,n]}
    return make(prompt,visual['values'],steps,result,visual,tag,wrong,
        f'{result}×{result} = {n*n}.' if kind=='root' else f'{result}³ = {n**3}.' if kind=='cube_root' else f'The original expression evaluates to {result}.')

def mixed(a,b,c,kind):
    if kind=='brackets':
        first=a+b;result=first*c;prompt=f'Calculate ({signed(a)} + {signed(b)}) × {signed(c)}.'
        steps=[f'Evaluate the bracket first: {a} + {signed(b)} = {first}.',f'The expression becomes {signed(first)}×{signed(c)}.',f'Apply the sign rule and multiply magnitudes: {result}.']
        wrong=[a+b*c,(a-b)*c,abs(result) if result<0 else -result];tag='brackets-first'
    elif kind=='debt':
        first=a+b;result=first-c;prompt=f'An account starts with a debt of R{abs(a)}, receives R{b}, then pays R{c}. What is the signed balance in rand?'
        steps=[f'Write the balance change as {a} + {signed(b)} − {signed(c)}.',f'After the receipt the balance is {first}.',f'After paying {c}, the balance is {result}.']
        wrong=[a+b+c,a-b-c,first];tag='credit-debit'
    elif kind=='temperature':
        first=a+b;result=first-c;prompt=f'The temperature is {a}°C. It changes by {b}°C, then falls by {c}°C. Find the final temperature.'
        steps=[f'Start at {a}°C on the number line.',f'Change by {b}°C to reach {first}°C.',f'Fall by {c}°C: {first} − {c} = {result}°C.']
        wrong=[a+b+c,a-b-c,first];tag='temperature-direction'
    else:
        first=a*b;result=first+c;prompt=f'A game awards {a} points per round for {b} rounds, then applies a {c:+d}-point adjustment. Find the total.'
        steps=[f'Multiply the per-round points: {a}×{b} = {first}.',f'Keep the adjustment sign: {signed(first)} + {signed(c)}.',f'Combine to get {result} points.']
        wrong=[a*(b+c),first-c,first];tag='game-order'
    assert len(set([result,*wrong]))==4,(prompt,result,wrong)
    unit='°C' if kind=='temperature' else ' points' if kind=='game' else ' rand' if kind=='debt' else ''
    answer=f'{result}{unit}'
    return make(prompt,[a,b,c],steps,answer,{'family':'context','values':[a,b,c],'operator':kind,'path':[a,first,result],'unit':unit},tag,
        [f'{w}{unit}' for w in wrong],f'Replaying both changes from {a} gives {result}{unit}.')

def diagnose(a,b,claim,kind):
    third=claim
    if kind=='subtraction':
        correct=a-b;wrong=a+b;claim=f'{a} − ({b}) = {wrong}'
        steps=[f'Read the learner claim: {claim}.',f'The first error is treating subtraction of {b} as addition of {b}; add the opposite {signed(-b)}.',f'Calculate {a} + {signed(-b)} = {correct}; compare with the claim.']
        tag='first-wrong-subtraction';wrong_options=[str(wrong),str(a),str(-correct)]
    elif kind=='product':
        correct=a*b;wrong=-correct;claim=f'{signed(a)}×{signed(b)} = {wrong}'
        steps=[f'Read the two signed factors in {claim}.',f'The first error is the claimed product sign: {"same" if (a<0)==(b<0) else "different"} signs give {"positive" if correct>=0 else "negative"}.',f'Multiply magnitudes and attach that sign: {correct}.']
        tag='first-wrong-product-sign';wrong_options=[str(wrong),str(a+b),str(abs(a)+abs(b))]
    elif kind=='order':
        correct=a+b*claim;wrong=(a+b)*claim
        steps=[f'Read {a} + {signed(b)}×{signed(claim)}.',f'The learner added first; multiplication comes before addition.',f'{b}×{signed(claim)} = {b*claim}; then {a} + {signed(b*claim)} = {correct}.']
        tag='first-wrong-order';wrong_options=[str(wrong),str(a+b),str(b*claim)]
        claim=f'{a} + {signed(b)}×{signed(claim)} = {wrong}'
    else:
        correct=a*a;wrong=-correct;claim=f'({a})² = {wrong}'
        steps=[f'Locate the parentheses in {claim}.',f'The learner kept a negative sign after squaring the whole negative base.',f'Expand ({a})×({a}) = {correct}.']
        tag='first-wrong-square-sign';wrong_options=[str(wrong),str(2*a),str(abs(a))]
    assert len(set([str(correct),*wrong_options]))==4,(claim,correct,wrong_options)
    return make(f'A learner wrote {claim}. Find the first incorrect operation and give the corrected result.',[claim],steps,str(correct),
        {'family':'diagnosis','values':[a,b,third] if kind=='order' else [a,b],'operator':kind,'path':[wrong,correct],'learner_claim':claim},tag,wrong_options,
        f'The corrected calculation evaluates to {correct}, while the learner claim gives {wrong}.')

WORKED={
 1:[compare(-8,3,-2),compare(-12,-5,0),compare(-17,7,-9),
    operation(-7,12,'+'),operation(6,-14,'+'),operation(-10,-9,'+'),
    operation(4,-7,'−'),operation(-8,-3,'−'),operation(-11,6,'−'),
    operation(-6,7,'×'),operation(-9,-4,'×'),operation(12,-8,'×'),
    operation(-42,6,'÷'),operation(72,-9,'÷'),operation(-96,-12,'÷')],
 2:[property_case(-6,9,-9,'inverse'),property_case(7,-13,13,'inverse'),property_case(-17,-5,5,'inverse'),
    property_case(-5,7,-3,'distributive'),property_case(-8,-4,6,'distributive'),property_case(9,-5,-4,'distributive'),
    property_case(-12,9,-4,'associative'),property_case(14,-8,-11,'associative'),property_case(-18,-7,15,'associative'),
    property_case(-3,-8,5,'common'),property_case(6,-9,-4,'common'),property_case(-7,12,-5,'common'),
    property_case(-11,4,-9,'distributive'),property_case(13,-12,5,'associative'),property_case(-14,8,-3,'common')],
 3:[power_root(n,'square') for n in (-3,-5,-8,-11)]+[power_root(n,'cube') for n in (-2,-3,-4,-6)]+
   [power_root(n,'root') for n in (-4,-7,-9,-12)]+[power_root(n,'cube_root') for n in (-3,-5,-7)],
 4:[mixed(*x,'brackets') for x in [(-8,3,-2),(7,-12,3),(-11,-5,4),(12,-7,-3)]]+
   [mixed(*x,'temperature') for x in [(-4,-6,3),(-9,5,7),(2,-11,8),(7,-15,6)]]+
   [mixed(*x,'debt') for x in [(-80,35,60),(-120,90,45),(-50,85,110)]]+
   [mixed(*x,'game') for x in [(-3,7,5),(8,5,-15),(-6,9,14),(12,4,-19)]],
 5:[diagnose(*x,'subtraction') for x in [(7,-4,0),(-8,-3,0),(12,-9,0),(5,-11,0)]]+
   [diagnose(*x,'product') for x in [(-6,-7,0),(-9,4,0),(8,-5,0),(-12,-3,0)]]+
   [diagnose(*x,'order') for x in [(8,-3,4),(-7,5,-2),(11,-4,-3),(15,-6,2)]]+
   [diagnose(-4,0,0,'square'),diagnose(-7,0,0,'square'),diagnose(-9,0,0,'square')]
}

def candidates(n,seed):
    if n==1:return [operation(-5-seed,seed+9,'+'),operation(seed+5,-seed-11,'−'),operation(-6-seed,seed+4,'×'),operation(-42-7*seed,7,'÷')]
    if n==2:return [property_case(-4-seed,7+seed,-3,'distributive'),property_case(-9-seed,4+seed,-4-seed,'inverse'),property_case(-8-seed,6,-3,'associative'),property_case(-3-seed,8,-5,'common')]
    if n==3:return [power_root(-4-seed,'square'),power_root(-2-seed,'cube'),power_root(-6-seed,'root'),power_root(-3-seed,'cube_root')]
    if n==4:return [mixed(-5-seed,4,-2,'brackets'),mixed(-8-seed,5,3,'temperature'),mixed(-70-10*seed,40+5*seed,35,'debt'),mixed(-3-seed,6,5,'game')]
    return [diagnose(8+seed,-4-seed,0,'subtraction'),diagnose(-5-seed,-3,0,'product'),diagnose(9+seed,-3,4,'order'),diagnose(-4-seed,0,0,'square')]

def item(case,n,prefix,index):
    options=case['wrongs'].copy();position=(index-1)%4;options.insert(position,case['answer'])
    return {'id':f'g9-int-l{n:02}-{prefix}{index:02}','prompt':case['problem'],'options':options,'answer_index':position,
        'memo':case['answer']+'. '+' '.join(case['actions']),'misconception':case['misconception'],
        'option_rationales':{value:('Correct: '+case['check'] if value==case['answer'] else
            'Incorrect: '+case['wrong_methods'][case['wrongs'].index(value)]) for value in options}}

def build(n):
    worked=WORKED[n];assert len(worked)==15
    other=[];seed=1
    while len(other)<23:
        for case in candidates(n,seed):
            if case['problem'] not in {c['problem'] for c in [*worked,*other]}:other.append(case)
            if len(other)==23:break
        seed+=1
    banks={'practice':[item(c,n,'p',i) for i,c in enumerate(other[:15],1)],
           'mastery':[item(c,n,'m',i) for i,c in enumerate(other[15:20],1)],
           'reassessment':[item(c,n,'r',i) for i,c in enumerate(other[20:],1)]}
    name=f'lesson-{n:02}-'+TITLES[n].lower().replace(',','').replace(' ','-')+'.md'
    data={'source':name,'worked':[{**c,'id':f'g9-int-l{n:02}-w{i:02}',
        'difficulty':'foundation' if i<=2 else 'easy' if i<=5 else 'standard' if i<=9 else 'exam' if i<=12 else 'advanced'}
        for i,c in enumerate(worked,1)],**banks}
    lines=[f'# Grade 9 Topic 2 · Lesson {n}: {TITLES[n]}','',
           'Status: authored source requiring mathematics and live browser review; not published.',
           'Authority: DBE 2026 Grade 9 Mathematics ATP, Term 1, Integers. Original Athena variants.',ATP,'',
           'Each visual must reveal exactly one action at a time and retain previous written results.','',
           '## Worked examples']
    for c in data['worked']:
        lines += ['',f"### {c['id']} · {c['difficulty']}",f"Question: {c['problem']}",
            f"Givens: {'; '.join(c['givens'])}",f"Visual: {json.dumps(c['visual'],ensure_ascii=False)}",
            *[f'{i}. {step}' for i,step in enumerate(c['actions'],1)],
            f"Answer: {c['answer']}",f"Misconception: {c['misconception']}"]
    for bank in ('practice','mastery','reassessment'):
        lines += ['',f'## {bank.title()} · private key and rationale']
        for c in data[bank]:
            lines += ['',f"### {c['id']}",f"Question: {c['prompt']}",
              *[f'{chr(65+i)}. {value}' for i,value in enumerate(c['options'])],
              f"Key: {chr(65+c['answer_index'])}",f"Memo: {c['memo']}",
              *[f'Distractor {value}: {reason}' for value,reason in c['option_rationales'].items() if reason.startswith('Incorrect:')]]
    (DOC/name).write_text('\n'.join(lines)+'\n',encoding='utf-8')
    (OUT/f'integers_{n:02}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return {'lesson_id':f'g9-integers-{n:02}','source':name,'source_sha256':hashlib.sha256((DOC/name).read_bytes()).hexdigest(),
            **{f'{bank}_ids':[x['id'] for x in cases] for bank,cases in data.items() if isinstance(cases,list)},
            **{f'{bank}_count':len(cases) for bank,cases in data.items() if isinstance(cases,list)},
            'status':'teacher_review_required','browser_accepted':False,'teacher_approved':False}

if __name__=='__main__':
    DOC.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    manifest=[build(n) for n in range(1,6)]
    (DOC/'topic2-acceptance-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Authored',len(manifest),'lessons:',sum(x['worked_count'] for x in manifest),'worked,',sum(x['practice_count'] for x in manifest),'practice')
