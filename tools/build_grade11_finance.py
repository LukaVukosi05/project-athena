"""Original Grade 11 finance questions with deterministic, checked money arithmetic."""
from __future__ import annotations

import json
from decimal import Decimal, ROUND_HALF_UP
from hashlib import sha256
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/curriculum/grade11/finance-growth-decay'
OUT=ROOT/'backend/app/curriculum/grade11/generated'
ATP='https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2023%20ATPs/FET%20Content%20Subjects/Grade%2011/1.590%20ATP%202023-24%20Gr%2011%20Maths%20final.pdf'
CAPS='https://www.education.gov.za/Portals/0/CD/National%20Curriculum%20Statements%20and%20Vocational/CAPS%20FET%20_%20MATHEMATICS%20_%20GR%2010-12%20_%20Web_1133.pdf'
TITLES={1:'Simple and compound growth',2:'Hire purchase, inflation and population',
        3:'Foreign exchange rates and conversion',4:'Straight-line and reducing-balance depreciation',
        5:'Nominal and effective interest rates',6:'Integrated growth, decay and finance diagnosis'}
DIFFICULTY=['foundation']*2+['easy']*3+['standard']*4+['intermediate']*3+['exam']*3
D=lambda x:Decimal(str(x))
CENT=D('0.01')
def money(x):return f'{x.quantize(CENT,rounding=ROUND_HALF_UP):,.2f}'
def rate(x):return f'{x.quantize(CENT,rounding=ROUND_HALF_UP):.2f}'
def whole(x):return str(x.quantize(D('1'),rounding=ROUND_HALF_UP))

def case(n,i,variant=0):
    t=i+15*variant
    p=D(1000+175*t)
    percent=4+t%9;r=D(percent)/100
    years=2+t%4
    if n==1:
        simple=t%2==1
        value=p*(1+r*years) if simple else p*(1+r)**years
        factor=f'1 + {r} × {years}' if simple else f'(1 + {r})^{years}'
        kind='simple interest' if simple else 'compound interest annually'
        problem=f'R{money(p)} is invested at {percent}% per year for {years} years using {kind}. Find the accumulated amount to the nearest cent.'
        steps=[f'Principal P = R{money(p)}, annual rate i = {r}, number of years n = {years}.',
               f'{"Simple" if simple else "Compound"} growth uses A = {"P(1 + in)" if simple else "P(1 + i)^n"}; distinguish it from the other method.',
               f'Substitute A = {money(p)} × {factor}.',
               f'Calculate A = R{money(value)}; only round at the final money amount.',
               f'Answer: R{money(value)}. Check that growth is positive and A exceeds the original R{money(p)}.']
        v=dict(mode='growth',principal=str(p),rate=str(r),years=years,simple=simple)
        label='Accumulated amount'
    elif n==2:
        mode=['hire','inflation','population'][t%3]
        if mode=='hire':
            deposit_rate=D(10+5*(t%4))/100
            cash=D(2000+125*t);deposit=cash*deposit_rate;balance=cash-deposit
            hp_rate=D(7+t%7)/100;term=1+t%3;months=12*term
            interest=balance*hp_rate*term;value=(balance+interest)/months
            problem=f'A device has a cash price of R{money(cash)}. Pay {deposit_rate*100:g}% deposit, then simple interest of {hp_rate*100:g}% per year on the outstanding balance for {term} years. Find the monthly instalment over {months} equal months, excluding fees.'
            steps=[f'Deposit = {money(cash)} × {deposit_rate} = R{money(deposit)}.',
                   f'The financed balance is {money(cash)} − {money(deposit)} = R{money(balance)}; interest is charged on this balance.',
                   f'Simple interest on the balance = {money(balance)} × {hp_rate} × {term} = R{money(interest)}.',
                   f'Repay R{money(balance+interest)} over {months} months: {money(balance+interest)}/{months} = R{money(value)} per month.',
                   f'Answer: R{money(value)} per month. Check the deposit is excluded from the instalment total.']
            v=dict(mode=mode,principal=str(cash),deposit_rate=str(deposit_rate),rate=str(hp_rate),years=term,months=months)
            label='Monthly instalment'
        elif mode=='inflation':
            price=D(1000+125*t);value=price*(1+r)**years
            problem=f'A basket costs R{money(price)} today. If its price rises by {percent}% each year for {years} years, estimate its price then to the nearest cent.'
            steps=[f'Initial price P = R{money(price)}; annual inflation i = {r}; n = {years} years.',
                   f'Repeated inflation compounds, so use A = P(1 + i)^n.',
                   f'Substitute A = {money(price)} × (1 + {r})^{years}.',
                   f'Evaluate the full power before rounding: A = R{money(value)}.',
                   f'Answer: R{money(value)}. Check the price rises above R{money(price)}.']
            v=dict(mode=mode,principal=str(price),rate=str(r),years=years)
            label='Future price'
        else:
            people=D(5000+375*t);value=people*(1+r)**years
            problem=f'A town has {whole(people)} people. Estimate its population after {years} years at {percent}% annual compound growth, rounding only the final population to a whole person.'
            steps=[f'Initial population P = {whole(people)}, annual growth rate i = {r}, n = {years}.',
                   f'Population grows on the new total each year: A = P(1 + i)^n.',
                   f'Substitute A = {whole(people)} × (1 + {r})^{years}.',
                   f'The unrounded result is {value:.3f}; round to {whole(value)} people at the end.',
                   f'Answer: {whole(value)} people. Check that the result exceeds {whole(people)}.']
            v=dict(mode=mode,principal=str(people),rate=str(r),years=years)
            label='Population';value=value.quantize(D('1'),rounding=ROUND_HALF_UP)
    elif n==3:
        # A quote is explicitly in rand for one foreign unit; the conversion direction matters.
        foreign=['USD','EUR','GBP'][t%3];old=D(12)+D(t%8)+D('0.40');new=old+D(t%5-2)*D('0.35')
        units=D(80+7*t);rand=units*new
        mode='foreign_to_rand' if t%2 else 'rand_to_foreign'
        if mode=='foreign_to_rand':
            value=rand
            problem=f'An exchange board quotes R{money(old)} and later R{money(new)} for one {foreign}. Convert {whole(units)} {foreign} at the later quote into rand, and explain the change in rand cost.'
            steps=[f'The quote is rand per one {foreign}; use the later rate R{money(new)} per {foreign}.',
                   f'For {whole(units)} {foreign}, multiply foreign units by rand per unit.',
                   f'Calculate {whole(units)} × {money(new)} = R{money(value)}.',
                   f'The earlier cost would be {whole(units)} × {money(old)} = R{money(units*old)}; compare the two.',
                   f'Answer: R{money(value)}. A higher rand-per-{foreign} quote makes this foreign purchase cost more rand.']
            label='Rand received'
        else:
            budget=D(1500+75*t);value=budget/new
            problem=f'An exchange board quotes R{money(old)} and later R{money(new)} per one {foreign}. With a R{money(budget)} budget, how many {foreign} units can be bought at the later quote? Ignore fees; round units to two decimals.'
            steps=[f'The quote is R{money(new)} for one {foreign}; rand ÷ rand-per-{foreign} gives {foreign} units.',
                   f'Use the later quote, rather than the earlier R{money(old)} rate.',
                   f'Calculate {money(budget)} ÷ {money(new)} = {money(value)} {foreign}.',
                   f'At the earlier quote the same budget would buy {money(budget/old)} {foreign}; compare direction.',
                   f'Answer: {money(value)} {foreign}. Multiply the unrounded units by R{money(new)} to recover the budget.']
            label=f'{foreign} bought'
        v=dict(mode='exchange',direction=mode,currency=foreign,old=str(old),new=str(new),quantity=str(units) if mode=='foreign_to_rand' else str(budget))
    elif n==4:
        purchase=D(6000+350*t);simple=t%2==1
        value=purchase*(1-r*years) if simple else purchase*(1-r)**years
        kind='straight-line depreciation on original cost' if simple else 'reducing-balance depreciation'
        formula='P(1 − in)' if simple else 'P(1 − i)^n'
        problem=f'A machine costs R{money(purchase)} and depreciates by {percent}% annually for {years} years using {kind}. Find its book value to the nearest cent.'
        steps=[f'Original cost P = R{money(purchase)}, depreciation rate i = {r}, n = {years}.',
               f'{"Straight-line" if simple else "Reducing-balance"} depreciation uses A = {formula}.',
               f'Substitute A = {money(purchase)} × {"(1 − " + str(r) + " × " + str(years) + ")" if simple else "(1 − " + str(r) + ")^" + str(years)}.',
               f'Calculate A = R{money(value)}; this is the book value, not the total loss.',
               f'Answer: R{money(value)}. Check 0 < A < the original R{money(purchase)}.']
        v=dict(mode='decay',principal=str(purchase),rate=str(r),years=years,simple=simple)
        label='Book value'
    elif n==5:
        principal=D(2000+125*t);nominal=D(6+t%10)/100;m=[2,4,12][t%3]
        value=((1+nominal/m)**m-1)*100
        accumulated=principal*(1+nominal/m)**(m*years)
        problem=f'R{money(principal)} earns {nominal*100:g}% nominal interest compounded {m} times per year. Find the effective annual rate to two decimal places, and identify the compounding period.'
        steps=[f'Nominal annual rate j = {nominal}; {m} compounding periods per year.',
               f'The rate per period is j/m = {nominal}/{m} = {(nominal/m):.6f}.',
               f'Effective annual rate = (1 + j/m)^m − 1 = (1 + {nominal}/{m})^{m} − 1.',
               f'This is {rate(value)}% per year; after {years} years the principal would grow to R{money(accumulated)} without intermediate rounding.',
               f'Answer: {rate(value)}% effective annually. The period is {12//m} month(s), and the effective rate exceeds the positive nominal rate.']
        v=dict(mode='effective',principal=str(principal),rate=str(nominal),periods=m,years=years)
        label='Effective annual rate'
    else:
        mode=['growth_then_decay','compare_methods','rate_diagnosis'][t%3]
        principal=D(3000+165*t);annual=D(5+t%8)/100;term=2+t%3
        if mode=='growth_then_decay':
            drop=D(3+t%6)/100
            risen=principal*(1+annual)**term;value=risen*(1-drop)
            problem=f'A price of R{money(principal)} rises {annual*100:g}% each year for {term} years, then falls {drop*100:g}% once. Find its final price; explain why the percentages cannot simply be subtracted.'
            steps=[f'The first growth applies {term} times to the changing balance: R{money(principal)} × (1 + {annual})^{term}.',
                   f'The price after growth is approximately R{money(risen)}; retain the unrounded balance.',
                   f'The final fall applies to the unrounded new price: {money(principal)} × (1 + {annual})^{term} × (1 − {drop}).',
                   f'This gives R{money(value)}. The two percentage changes use different bases.',
                   f'Answer: R{money(value)}. Check by multiplying the two factors, not subtracting their percentages.']
            v=dict(mode=mode,principal=str(principal),rate=str(annual),decline=str(drop),years=term)
            label='Final price'
        elif mode=='compare_methods':
            simple=principal*(1+annual*term);value=principal*(1+annual)**term
            problem=f'R{money(principal)} earns {annual*100:g}% annually for {term} years. Compare simple interest with annual compound interest; find the compound amount and identify which is larger.'
            steps=[f'Simple interest gives Aₛ = {money(principal)} × (1 + {annual} × {term}) = R{money(simple)}.',
                   f'Compound interest gives A꜀ = {money(principal)} × (1 + {annual})^{term}.',
                   f'Evaluate the compound power before rounding: A꜀ = R{money(value)}.',
                   f'Compare R{money(value)} with R{money(simple)}; compound growth is larger for this positive rate and multiple years.',
                   f'Answer: R{money(value)} compound amount. The difference is R{money(value-simple)}.']
            v=dict(mode=mode,principal=str(principal),rate=str(annual),years=term)
            label='Compound amount'
        else:
            periods=4;value=((1+annual/periods)**periods-1)*100
            problem=f'A bank advertises {annual*100:g}% nominal interest compounded quarterly. A learner calls {annual*100:g}% the effective annual rate. Locate the first error and give the effective annual rate to two decimal places.'
            steps=[f'The quoted {annual*100:g}% is nominal, with {periods} compounding periods per year.',
                   f'The learner ignored compounding: first divide the nominal rate by {periods} to get {annual/periods:.6f} per quarter.',
                   f'Then compound four periods: (1 + {annual}/{periods})^{periods} − 1.',
                   f'The effective annual rate is {rate(value)}%; it differs from the advertised nominal rate.',
                   f'Answer: {rate(value)}% effective annually. The first error was equating nominal and effective rates.']
            v=dict(mode=mode,principal=str(principal),rate=str(annual),periods=periods,years=1)
            label='Effective annual rate'
    numeric=value
    formatted=rate(numeric) if 'rate' in label.lower() else whole(numeric) if label=='Population' else money(numeric)
    unit='%' if 'rate' in label.lower() else ' people' if label=='Population' else f' {v["currency"]}' if v.get('direction')=='rand_to_foreign' else ''
    prefix='' if unit else 'R'
    answer=f'{label} = {prefix}{formatted}{unit}'
    steps[-1]=steps[-1].replace('Answer:',f'Answer: {label} =',1)
    # Three distinct, numerically plausible but wrong outcomes; no textual fake answers.
    width=D('0.25') if 'rate' in label.lower() else D('1') if label=='Population' else max(D('0.50'),abs(numeric)*D('0.03'))
    wrong=[]
    for shift in (1,-1,2,-2,3):
        trial=numeric+width*shift
        if trial<=0:continue
        text=rate(trial) if 'rate' in label.lower() else whole(trial) if label=='Population' else money(trial)
        option=f'{label} = {prefix}{text}{unit}'
        if option!=answer and option not in wrong:wrong.append(option)
        if len(wrong)==3:break
    assert len(wrong)==3 and len(steps)==5
    # Exact-answer label in the final narration, including units and context.
    assert answer in steps[-1],(n,i,answer)
    return dict(id=f'g11-fin-l{n:02}-w{i:02}',lesson=n,problem=problem,
                answer=answer,actions=steps,check=steps[-1],
                visual=dict(family='grade11_finance',values=v),difficulty=DIFFICULTY[i-1],wrong=wrong)

def build():
    DOC.mkdir(parents=True,exist_ok=True);manifest=[]
    for n,title in TITLES.items():
        worked=[{k:v for k,v in case(n,i).items() if k!='wrong'} for i in range(1,16)]
        assert len({q['problem'] for q in worked})==15
        data=dict(source=f'grade11-fin-lesson-{n:02}.md',worked=worked)
        for section,count,variant,prefix in [('practice',15,1,'p'),('mastery',5,2,'m'),('reassessment',3,3,'r')]:
            bank=[]
            for i in range(1,count+1):
                q=case(n,i,variant);options=[q['answer'],*q['wrong']];shift=(i+variant)%4;options=options[shift:]+options[:shift]
                assert len(set(options))==4
                bank.append(dict(id=f'g11-fin-l{n:02}-{prefix}{i:02}',prompt=q['problem'],
                                 options=options,answer_index=options.index(q['answer']),
                                 actions=q['actions'],memo=' '.join(q['actions'])))
            data[section]=bank
        lines=[f'# Grade 11 Topic 10, Lesson {n}: {title}',
               f'Curriculum: [DBE Grade 11 ATP]({ATP}) and [Mathematics CAPS]({CAPS}).',
               'Original Athena questions, not past-paper transcriptions. Teacher review and live browser acceptance required.',
               'Calculation convention: use Decimal arithmetic; retain full precision until the last rounding to cents, two-decimal rates or whole people. Exchange quote is rand per foreign unit; fees excluded.']
        for q in worked:
            lines.extend([f'## {q["id"]}: {q["problem"]}',f'Question-specific visual values: `{json.dumps(q["visual"],ensure_ascii=False)}`',
                          *[f'{j}. {step}' for j,step in enumerate(q['actions'],1)],f'Answer: {q["answer"]}. Check: {q["check"]}'])
        for section in ('practice','mastery','reassessment'):
            lines.append(f'## {section.title()} key')
            for q in data[section]:lines.append(f'- {q["id"]}: {q["prompt"]} Options: {" | ".join(q["options"])}. Correct: {q["options"][q["answer_index"]]}. {q["memo"]}')
        source=DOC/data['source'];source.write_text('\n\n'.join(lines)+'\n',encoding='utf-8')
        (OUT/f'finance_{n:02}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        manifest.append(dict(lesson_id=f'g11-fin-{n:02}',source=source.name,source_sha256=sha256(source.read_bytes()).hexdigest(),
                             worked=15,practice=15,mastery=5,reassessment=3,status='teacher_review_required',teacher_approved=False,browser_accepted=False))
    (DOC/'topic10-acceptance-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':build()
