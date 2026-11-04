"""Static original Grade 9 exponents bank, compiled only at authoring time."""
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/curriculum/grade9/exponents'
OUT=ROOT/'backend/app/curriculum/grade9/generated'
ATP='https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2026%20ATPs/2026_ATP_Mathematics_Grade%209.pdf'
TITLES={1:'Powers and exponent laws',2:'Zero and negative exponents',
        3:'Scientific notation and small numbers',4:'Combined operations and parentheses',
        5:'Scientific notation in contexts',6:'Exponent error diagnosis and reassessment'}
SUP=str.maketrans('-0123456789','⁻⁰¹²³⁴⁵⁶⁷⁸⁹')
def powtext(base,n):return f'{base}{str(n).translate(SUP)}'
def frac(n,d):
    f=Fraction(n,d);return str(f.numerator) if f.denominator==1 else f'{f.numerator}/{f.denominator}'
def sci(value):
    x=Decimal(str(value));assert x>0
    exp=x.adjusted();co=x.scaleb(-exp).normalize()
    return f'{co} × 10{str(exp).translate(SUP)}',str(co),exp

REASONS={
 'base-times-exponent':['Multiplies base and exponent.','Adds base and exponent.','Counts one extra repeated factor.'],
 'product-law':['Multiplies exponents instead of adding them.','Adds the separate power values.','Omits one repeated base factor.'],
 'quotient-law':['Adds the exponents instead of subtracting.','Multiplies the exponents.','Reverses the exponent difference.'],
 'power-of-power':['Adds the exponents instead of multiplying.','Stops before repeating every factor.','Counts one repeated factor too many.'],
 'power-of-product':['Adds the powered factors.','Raises only one factor.','Raises the sum instead of the product.'],
 'zero-exponent':['Treats a nonzero base raised to zero as zero.','Keeps the base unchanged.','Applies a negative sign without justification.'],
 'negative-exponent':['Treats a negative exponent as a negative value.','Keeps the positive power rather than its reciprocal.','Uses one extra factor in the reciprocal denominator.'],
 'parenthesised-negative-base':['Drops the sign of the full negative base.','Adds the base and exponent.','Stops a repeated factor too early.'],
 'scientific-normalization':['Leaves the coefficient outside [1,10).','Moves the decimal in the wrong direction.','Moves one decimal place too far.'],
 'scientific-order':['Compares coefficients before powers of ten.','Assumes different powers are equal.','Claims order is indeterminate despite given values.'],
 'scientific-unit':['Loses a factor of ten when scaling the measured value.','Reverses the exponent direction.','Omits the stated multiplier.'],
 'combined-law':['Adds exponents where the quotient requires subtraction.','Omits the final divisor.','Subtracts one extra from the final exponent.'],
 'parentheses-first':['Powers the wrong scope of the negative base.','Treats a product as a sum.','Reverses the sign after a valid square.'],
 'first-error-product':['Keeps the learner’s exponent product.','Adds power values instead of exponents.','Omits the final repeated factor.'],
 'first-error-zero':['Keeps the learner’s zero result.','Keeps the original base.','Changes the sign of the identity value.'],
 'first-error-negative':['Keeps the learner’s negative power value.','Keeps the positive power without a reciprocal.','Uses an extra factor in the denominator.'],
 'first-error-scientific':['Keeps the non-normalized coefficient.','Reverses the exponent sign.','Moves the decimal one extra place.'],
 'first-error-parentheses':['Keeps the learner’s sign error.','Adds base and exponent.','Stops one factor too early.'],
}

def case(prompt,givens,steps,answer,wrong,visual,tag,check):
    answer=str(answer);wrong=list(map(str,wrong))
    assert tag in REASONS and len(steps)>=3 and len(wrong)==3 and len({answer,*wrong})==4,(prompt,answer,wrong)
    return dict(problem=prompt,givens=list(map(str,givens)),actions=[*steps,'Check: '+check],
        answer=answer,wrongs=wrong,wrong_methods=REASONS[tag],visual=visual,misconception=tag,check='Check: '+check)

def basic(base,n):
    value=base**n;prompt=f'Calculate {powtext(base,n)}.'
    return case(prompt,[base,n],[f'The base is {base}; the exponent counts {n} factors.',
        f'Expand as '+(' × '.join([str(base)]*n))+'.',f'Multiply the factors: {value}.'],value,
        [base*n,base+n,base**(n+1)],{'family':'factors','base':base,'exponents':[n],'values':[base**i for i in range(n+1)]},
        'base-times-exponent',f'{powtext(base,n)} = {value}.')

def same_base(base,m,n,kind):
    if kind=='product':
        exponent=m+n;value=base**exponent;wrong=[base**(m*n),base**m+base**n,base**(exponent-1)]
        prompt=f'Calculate {powtext(base,m)} × {powtext(base,n)}.'
        steps=[f'The bases match: both are {base}.',f'For multiplication add the exponents: {m}+{n}={exponent}.',f'{powtext(base,exponent)} = {value}.'];tag='product-law'
    else:
        assert m>n;exponent=m-n;value=base**exponent;wrong=[base**(m+n),base**(m*n),frac(1,base**exponent)]
        prompt=f'Calculate {powtext(base,m)} ÷ {powtext(base,n)}.'
        steps=[f'The nonzero bases match: both are {base}.',f'For division subtract exponents: {m}−{n}={exponent}.',f'{powtext(base,exponent)} = {value}.'];tag='quotient-law'
    return case(prompt,[base,m,n],steps,value,wrong,
        {'family':'law','base':base,'exponents':[m,n,exponent],'values':[base**m,base**n,value],'operator':kind},tag,
        f'{base**m} {"×" if kind=="product" else "÷"} {base**n} = {value}.')

def nested(base,m,n):
    exponent=m*n;value=base**exponent;prompt=f'Calculate ({powtext(base,m)}){str(n).translate(SUP)}.'
    return case(prompt,[base,m,n],[f'The entire power {powtext(base,m)} is repeated {n} times.',
        f'Multiply exponents: {m}×{n}={exponent}.',f'Evaluate {powtext(base,exponent)} = {value}.'],value,
        [base**(m+n),base**(exponent-1 if exponent-1!=m+n else exponent-2),base**(exponent+1)],
        {'family':'law','base':base,'exponents':[m,n,exponent],'values':[base**m,value],'operator':'nested'},
        'power-of-power',f'({base**m}){str(n).translate(SUP)} = {value}.')

def product_power(a,b,n):
    value=(a*b)**n;prompt=f'Calculate ({a} × {b}){str(n).translate(SUP)}.'
    return case(prompt,[a,b,n],[f'The exponent applies to the whole product {a}×{b}.',
        f'Raise each factor: {powtext(a,n)} × {powtext(b,n)} = {a**n}×{b**n}.',f'Multiply to obtain {value}.'],value,
        [a**n+b**n,a*b**n,(a+b)**n],
        {'family':'law','base':a*b,'exponents':[n],'values':[a,b,a**n,b**n,value],'operator':'product_power'},
        'power-of-product',f'{a*b}{str(n).translate(SUP)} = {value}.')

def zero(base):
    prompt=f'Calculate ({base})⁰.'
    return case(prompt,[base,0],[f'The base {base} is nonzero.',
        'A nonzero base to exponent zero equals the multiplicative identity.',f'Therefore ({base})⁰ = 1.'],1,
        [0,base,-1],{'family':'reciprocal','base':base,'exponent':0,'denominator':1,'operator':'zero'},
        'zero-exponent',f'{base}³ ÷ {base}³ = 1 = {base}⁰.')

def negative(base,n):
    result=frac(1,base**n);prompt=f'Calculate {powtext(base,-n)} as a fraction.'
    return case(prompt,[base,-n],[f'A negative exponent indicates a reciprocal, not a negative value.',
        f'{powtext(base,-n)} = 1/{powtext(base,n)}.',f'{powtext(base,n)} = {base**n}, so the result is {result}.'],result,
        [-base**n,base**n,frac(1,base**(n+1))],
        {'family':'reciprocal','base':base,'exponent':-n,'denominator':base**n,'operator':'negative'},
        'negative-exponent',f'{result} × {base**n} = 1.')

def signed_base(base,n):
    assert base<0;value=base**n;prompt=f'Calculate ({base}){str(n).translate(SUP)}.'
    return case(prompt,[base,n],[f'Parentheses make {base} the entire base.',
        f'Expand '+(' × '.join([f'({base})']*n))+'.',f'Count negative factors and multiply: {value}.'],value,
        [-value,base+n,base**(n-1)],
        {'family':'factors','base':base,'exponents':[n],'values':[base**i for i in range(n+1)]},
        'parenthesised-negative-base',f'({base}){str(n).translate(SUP)} = {value}.')

def normalize(raw):
    answer,co,exp=sci(raw);x=Decimal(raw);wrong=[f'{Decimal(co)*10} × 10{str(exp-1).translate(SUP)}',
        f'{co} × 10{str(-exp).translate(SUP)}',f'{Decimal(co)/10} × 10{str(exp+2).translate(SUP)}']
    prompt=f'Write {raw} in normalized scientific notation.'
    return case(prompt,[raw],[f'The coefficient must be at least 1 and less than 10.',
        f'Move the decimal point to obtain {co}; count {abs(exp)} places.',
        f'{"A large number uses a positive" if exp>=0 else "A number below one uses a negative"} exponent: {answer}.'],
        answer,wrong,{'family':'scale','raw':str(x),'coefficient':co,'exponent':exp,'operator':'normalize'},
        'scientific-normalization',f'{answer} = {raw}.')

def compare_scientific(a,ea,b,eb):
    va=Decimal(str(a))*(Decimal(10)**ea);vb=Decimal(str(b))*(Decimal(10)**eb)
    answer='A is greater' if va>vb else 'B is greater' if vb>va else 'Equal';assert answer!='Equal'
    prompt=f'Which is greater: A = {a} × 10{str(ea).translate(SUP)} or B = {b} × 10{str(eb).translate(SUP)}?'
    return case(prompt,[a,ea,b,eb],[f'First inspect the powers of ten: {ea} and {eb}.',
        f'Convert to a common scale: A = {va}, B = {vb}.',f'Compare the aligned values: {answer}.'],answer,
        ['B is greater' if answer=='A is greater' else 'A is greater','Equal','Cannot tell'],
        {'family':'compare','a':[str(a),ea],'b':[str(b),eb],'values':[str(va),str(vb)]},
        'scientific-order',f'{va} {">" if va>vb else "<"} {vb}.')

def scientific_context(co,exp,mult,unit,scenario):
    amount=Decimal(str(co))*(Decimal(10)**exp)
    total=amount*mult;answer,final_co,final_exp=sci(total);given=f'{co} × 10{str(exp).translate(SUP)} {unit}'
    prompt=f'{scenario} Each unit measures {given}. What is the total for {mult} units in normalized scientific notation?'
    return case(prompt,[given,mult],[f'Multiply {mult} by the coefficient {co}, keeping 10{str(exp).translate(SUP)} and {unit}.',
        f'The unnormalized coefficient is {Decimal(str(co))*mult}.',f'Renormalize to {answer} {unit}.'],f'{answer} {unit}',
        [f'{Decimal(str(co))*mult} × 10{str(exp+1).translate(SUP)} {unit}',f'{final_co} × 10{str(-final_exp).translate(SUP)} {unit}',f'{co} × 10{str(exp).translate(SUP)} {unit}'],
        {'family':'context','coefficient':str(co),'exponent':exp,'multiplier':mult,'unit':unit,'result_coefficient':final_co,'result_exponent':final_exp},
        'scientific-unit',f'{given} × {mult} = {answer} {unit}.')

def combined(base,a,b,c):
    exponent=a+b-c;assert exponent>=1;value=base**exponent
    prompt=f'Calculate ({powtext(base,a)} × {powtext(base,b)}) ÷ {powtext(base,c)}.'
    return case(prompt,[base,a,b,c],[f'Combine the numerator with the product law: {a}+{b}={a+b}.',
        f'Divide equal nonzero bases: subtract exponent {c}, giving {a+b}−{c}={exponent}.',
        f'Evaluate {powtext(base,exponent)} = {value}.'],value,
        [base**(a+b+c),base**(a+b),base**(exponent-1)],
        {'family':'law','base':base,'exponents':[a,b,c,exponent],'values':[base**a,base**b,base**c,value],'operator':'combined'},
        'combined-law',f'{base**a}×{base**b}÷{base**c}={value}.')

def bracket_power(base,a,b):
    assert base<0;value=(base**a)*(base**b);prompt=f'Calculate ({powtext(base,a)} × {powtext(base,b)}).'
    return case(prompt,[base,a,b],[f'Parentheses keep {base} as the signed base of both powers.',
        f'Add exponents for a product of the same base: {a}+{b}={a+b}.',
        f'{powtext(f"({base})",a+b)} = {value}.'],value,
        [-value,base**a+base**b,base**(a+b-1)],
        {'family':'factors','base':base,'exponents':[a,b,a+b],'values':[base**a,base**b,value]},
        'parentheses-first',f'{base**a}×{base**b}={value}.')

def diagnose(base,a,b,kind):
    if kind=='product':
        value=base**(a+b);claim=base**(a*b)
        prompt=f'A learner says {powtext(base,a)} × {powtext(base,b)} = {claim} because the exponents multiply. Find the first error and corrected result.'
        steps=[f'The bases match: {base}.',f'The first error is multiplying exponents {a}×{b}; a product of powers adds them.',f'Use {a}+{b}={a+b}; {powtext(base,a+b)} = {value}.'];tag='first-error-product'
        wrong=[claim,base**a+base**b,base**(a+b-1)]
    elif kind=='zero':
        value=1;claim=0;prompt=f'A learner says ({base})⁰ = 0. Find the first error and corrected result.'
        steps=[f'Confirm the base {base} is nonzero.',f'The first error is treating exponent zero as a zero value.',f'The multiplicative identity gives ({base})⁰ = 1.'];tag='first-error-zero';wrong=[0,base,-1]
    elif kind=='negative':
        value=frac(1,base**a);claim=-base**a;prompt=f'A learner says {powtext(base,-a)} = {claim}. Find the first error and corrected fraction.'
        steps=[f'The base {base} is positive.',f'The first error is reading a negative exponent as a negative result.',f'Reciprocate the positive power: 1/{base**a} = {value}.'];tag='first-error-negative'
        wrong=[claim,base**a,frac(1,base**(a+1))]
    elif kind=='parentheses':
        assert base<0;value=base**a;claim=-abs(value);assert value>0
        prompt=f'A learner writes ({base}){str(a).translate(SUP)} = {claim}. Find the first error and corrected result.'
        steps=[f'Keep the parentheses: {base} is the whole base.',f'The first error is keeping a negative sign after an even number of negative factors.',f'Calculate {powtext(f"({base})",a)} = {value}.'];tag='first-error-parentheses'
        wrong=[claim,base+a,base**(a-1)]
    else:
        raw=Decimal(str(base));value,co,exp=sci(raw);claim=f'{Decimal(co)*10} × 10{str(exp-1).translate(SUP)}'
        prompt=f'A learner writes {raw} as {claim} in scientific notation. Find the first error and normalize it.'
        steps=['A normalized coefficient must be at least 1 and below 10.',f'The first error is leaving coefficient {Decimal(co)*10} outside that range.',f'Rewrite it as {value}.'];tag='first-error-scientific'
        wrong=[claim,f'{co} × 10{str(-exp).translate(SUP)}',f'{co} × 10{str(exp+1).translate(SUP)}']
    return case(prompt,[base,a,b],[*steps],value,wrong,
        {'family':'diagnosis','kind':kind,'base':str(base),'exponents':[a,b],'claim':str(claim),'correction':str(value)},
        tag,f'The corrected expression evaluates to {value}, not {claim}.')

WORKED={
 1:[*[basic(*x) for x in [(2,3),(3,3),(4,3)]],
    *[same_base(*x,'product') for x in [(2,3,4),(3,2,3),(4,2,3)]],
    *[same_base(*x,'quotient') for x in [(2,6,2),(3,5,2),(5,4,2)]],
    *[nested(*x) for x in [(2,3,2),(3,2,3),(5,2,3)]],
    *[product_power(*x) for x in [(2,3,2),(3,4,2),(2,5,3)]]],
 2:[*[zero(x) for x in (2,-3,7,10)],
    *[negative(*x) for x in [(2,3),(3,2),(5,2),(2,5),(4,3),(7,2)]],
    *[signed_base(*x) for x in [(-2,2),(-2,3),(-3,2),(-3,3),(-4,2)]]],
 3:[*[normalize(x) for x in ['4200','63000','7800000','0.0045','0.00072','0.0000036','0.000084','125000','0.0000091']],
    *[compare_scientific(*x) for x in [(4.2,3,3.9,3),(6.1,-4,8.2,-5),(2.5,6,9.1,5),(3.4,-6,7.0,-7),(5.2,4,5.19,4),(1.8,-3,9.3,-4)]]],
 4:[*[combined(*x) for x in [(2,4,3,2),(3,3,2,1),(4,2,3,2),(5,2,2,1),(2,5,2,3),(3,4,2,3),(2,6,3,4),(4,3,2,3)]],
    *[bracket_power(*x) for x in [(-2,2,2),(-3,3,2),(-4,2,2),(-2,3,3),(-3,2,4),(-5,2,2),(-2,4,3)]]],
 5:[*[scientific_context(*x) for x in [
     ('3.2',-4,5,'m','A laboratory cuts identical fibres.'),('4.5',-6,20,'g','A scale weighs identical grains.'),
     ('2.8',3,6,'m','A survey records equal trail segments.'),('7.5',-5,12,'L','A sensor measures repeated droplets.'),
     ('1.6',4,8,'cells','A culture contains equal samples.'),('6.4',-7,25,'m','An instrument measures equal films.'),
     ('5.1',5,7,'bytes','A storage test transfers equal blocks.'),('3.6',-3,15,'g','A lab mixes equal samples.'),
     ('8.2',2,9,'m','A map records identical sections.'),('1.25',-4,16,'L','A dispenser releases equal drops.'),
     ('2.4',6,5,'units','A counter records equal batches.'),('6.8',-8,30,'m','A microscope records identical lengths.'),
     ('4.2',3,25,'units','A warehouse counts equal pallets.'),('9.6',-5,125,'g','A lab combines equal samples.'),
     ('7.2',4,75,'m','A survey combines identical intervals.')]]],
 6:[*[diagnose(*x,'product') for x in [(2,2,3),(3,2,4),(5,2,3)]],
    *[diagnose(x,0,0,'zero') for x in (4,-7,9)],
    *[diagnose(*x,'negative') for x in [(2,3,0),(3,2,0),(5,2,0)]],
    *[diagnose(*x,'parentheses') for x in [(-2,2,0),(-3,2,0),(-4,2,0)]],
    *[diagnose(x,0,0,'scientific') for x in ('0.00064','48000','0.0000035')]]
}

def candidates(n,seed):
    if n==1:return [basic(2+seed,3),same_base(2,3+seed,2,'product'),same_base(3,5+seed,2,'quotient'),nested(2,2+seed,2),product_power(2,3+seed,2)]
    if n==2:return [zero(12+seed),negative(2+seed,2),negative(3,2+seed),signed_base(-3-seed,2),signed_base(-2,3+seed)]
    if n==3:return [normalize(str(Decimal(11+seed)*1000)),normalize(str(Decimal(12+seed)/Decimal(100000))),compare_scientific(2+seed,3,4+seed,2),compare_scientific(3+seed,-4,5+seed,-5)]
    if n==4:return [combined(2,3+seed,2,1),combined(3,3+seed,2,2),bracket_power(-2-seed,2,2),bracket_power(-3,3,2+seed)]
    if n==5:return [scientific_context(str(Decimal(11+seed)/10),-4,5+seed,'m','A sensor records identical segments.'),
        scientific_context(str(Decimal(12+seed)/10),3,4+seed,'units','A counter records equal groups.'),
        scientific_context(str(Decimal(13+seed)/10),-6,6+seed,'g','A lab weighs identical samples.')]
    return [diagnose(2,3+seed,2,'product'),diagnose(10+seed,0,0,'zero'),diagnose(2+seed,2,0,'negative'),
        diagnose(-2-seed,2,0,'parentheses'),diagnose(str(Decimal(12+seed)/100000),0,0,'scientific')]

def private_item(c,n,kind,index):
    options=c['wrongs'].copy();key=(index-1)%4;options.insert(key,c['answer'])
    return dict(id=f'g9-exp-l{n:02}-{kind}{index:02}',prompt=c['problem'],options=options,answer_index=key,
        memo=c['answer']+'. '+' '.join(c['actions']),misconception=c['misconception'],
        option_rationales={v:('Correct: '+c['check'] if v==c['answer'] else 'Incorrect: '+c['wrong_methods'][c['wrongs'].index(v)]) for v in options})

def build(n):
    worked=WORKED[n];assert len(worked)==15,(n,len(worked))
    other=[];used={c['problem'] for c in worked};seed=1
    while len(other)<23:
        for c in candidates(n,seed):
            if c['problem'] not in used:other.append(c);used.add(c['problem'])
            if len(other)==23:break
        seed+=1
        assert seed<30,(n,len(other))
    name=f'lesson-{n:02}-'+TITLES[n].lower().replace(',','').replace(' ','-')+'.md'
    data=dict(source=name,worked=[{**c,'id':f'g9-exp-l{n:02}-w{i:02}',
        'difficulty':'foundation' if i<=2 else 'easy' if i<=5 else 'standard' if i<=9 else 'exam' if i<=12 else 'advanced'} for i,c in enumerate(worked,1)],
        practice=[private_item(c,n,'p',i) for i,c in enumerate(other[:15],1)],
        mastery=[private_item(c,n,'m',i) for i,c in enumerate(other[15:20],1)],
        reassessment=[private_item(c,n,'r',i) for i,c in enumerate(other[20:],1)])
    lines=[f'# Grade 9 Topic 3 · Lesson {n}: {TITLES[n]}','',
        'Status: authored runtime source for mathematics and browser review; not published.',
        'Scope: DBE 2026 Grade 9 Mathematics ATP, Term 1, Exponents. Original Athena questions.',ATP,'',
        'Whiteboard: show the original expression, one legal operation at a time, cumulative written results and final verification.',
        '', '## Worked examples']
    for c in data['worked']:
        lines += ['',f"### {c['id']} · {c['difficulty']}",f"Question: {c['problem']}",f"Givens: {'; '.join(c['givens'])}",
          f"Visual: {json.dumps(c['visual'],ensure_ascii=False)}",*[f'{i}. {action}' for i,action in enumerate(c['actions'],1)],
          f"Answer: {c['answer']}",f"Misconception: {c['misconception']}"]
    for kind in ('practice','mastery','reassessment'):
        lines += ['',f'## {kind.title()} · private keys and rationales']
        for c in data[kind]:
            lines += ['',f"### {c['id']}",f"Question: {c['prompt']}",
                *[f'{chr(65+i)}. {option}' for i,option in enumerate(c['options'])],
                f"Key: {chr(65+c['answer_index'])}",f"Memo: {c['memo']}",
                *[f'Distractor {value}: {reason}' for value,reason in c['option_rationales'].items() if reason.startswith('Incorrect:')]]
    DOC.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    (DOC/name).write_text('\n'.join(lines)+'\n',encoding='utf-8')
    (OUT/f'exponents_{n:02}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return dict(lesson_id=f'g9-exponents-{n:02}',source=name,
       source_sha256=hashlib.sha256((DOC/name).read_bytes()).hexdigest(),
       **{f'{kind}_ids':[c['id'] for c in data[kind]] for kind in ('worked','practice','mastery','reassessment')},
       **{f'{kind}_count':len(data[kind]) for kind in ('worked','practice','mastery','reassessment')},
       status='teacher_review_required',browser_accepted=False,teacher_approved=False)

if __name__=='__main__':
    manifest=[build(n) for n in range(1,7)]
    (DOC/'topic3-acceptance-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Authored',len(manifest),'lessons:',sum(x['worked_count'] for x in manifest),'worked,',sum(x['practice_count'] for x in manifest),'practice')
