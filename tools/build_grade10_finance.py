"""Original Grade 10 finance questions with auditable Decimal arithmetic."""
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from hashlib import sha256
import json
ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/curriculum/grade10/finance-and-growth'
OUT=ROOT/'backend/app/curriculum/grade10/generated'
ATP='https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2023%20ATPs/FET%20Content%20Subjects/Grade%2010/1.580%20ATP%202023-24%20Gr%2010%20Maths%20final.pdf'
TITLES={1:'Simple interest and period conversion',2:'Compound growth and comparison',3:'Inflation, depreciation and population',4:'Hire purchase and instalments',5:'Exchange rates and rate changes',6:'Mixed finance methods and first-error repair'}
D=Decimal
def money(x):return D(x).quantize(D('.01'),rounding=ROUND_HALF_UP)
def rand(x):return f'R{money(x):,.2f}'
def case(n,i,variant=0):
 s=i+variant*27;p=D(1000+250*(s%17));rate=D(4+(s%10))/100;years=2+(s%5)
 months=years*12;ratepct=int(rate*100)
 mode=n if n!=6 else (s%5)+1
 v={'family':'grade10_finance','values':{'lesson':n,'mode':mode,'principal':str(p),'rate':str(rate),'years':years}}
 if mode==1:
  if s%3==0:months=12*(1+s%4)+6;years=D(months)/12
  interest=money(p*rate*D(years));total=money(p+interest)
  problem=f'{rand(p)} is invested at {ratepct}% simple interest per year for {months} months. Find the interest and final amount.'
  answer=f'interest {rand(interest)}; amount {rand(total)}'
  actions=[f'Identify P={rand(p)}, i={ratepct}%={rate}, and t={months}/12={years} years.',
   f'Use simple interest I=Pit because the same original principal earns interest each year.',
   f'I={rand(p)} × {rate} × {years}={rand(interest)}.',
   f'Add interest to principal: A={rand(p)}+{rand(interest)}={rand(total)}.',
   f'Answer: {answer}. Check A=P(1+it)={rand(total)}.']
  bad=[f'interest {rand(p*rate)}; amount {rand(p+p*rate)}',f'interest {rand(p*rate*months)}; amount {rand(p+p*rate*months)}',f'interest {rand(total)}; amount {rand(interest)}']
  v['values'].update(years=str(years),periods=months,unit='months',interest=str(interest),amount=str(total))
 elif mode==2:
  amount=money(p*(1+rate)**years);interest=money(amount-p);simple=money(p*(1+rate*years))
  problem=f'A savings account starts with {rand(p)} at {ratepct}% compound interest per year for {years} years. Find its final amount and compare it with simple interest at the same rate.'
  answer=f'compound {rand(amount)}; simple {rand(simple)}; difference {rand(amount-simple)}'
  actions=[f'Identify principal {rand(p)}, annual rate {rate}, and {years} compounding periods.',
   f'Compound interest multiplies the updated balance each year: A=P(1+i)^n.',
   f'A={rand(p)}(1+{rate})^{years}={rand(amount)}; compound interest is {rand(interest)}.',
   f'Simple growth on the original principal: {rand(p)}(1+{rate}×{years})={rand(simple)}.',
   f'Answer: {answer}. The extra growth comes from interest on earlier interest.']
  bad=[f'compound {rand(simple)}; simple {rand(simple)}; difference R0.00',f'compound {rand(amount)}; simple {rand(simple)}; difference {rand(interest)}',f'compound {rand(p*(1+rate)**(years-1))}; simple {rand(simple)}; difference R0.00']
  v['values'].update(amount=str(amount),simple=str(simple),interest=str(interest))
 elif mode==3 and s%5==0:
  population=D(10000+500*(s%13));annual=D(2+s%6)/100;final=(population*(1+annual)**years).quantize(D('1'),rounding=ROUND_HALF_UP)
  problem=f'A town has {int(population):,} residents. Its population grows by {int(annual*100)}% per year for {years} years. Estimate the population after {years} years, rounding once to a whole person.'
  answer=f'{int(final):,} residents'
  actions=[f'Start with {int(population):,} residents, annual rate {int(annual*100)}%, and {years} years.',
   f'Annual growth multiplier = 1+{annual}={1+annual}; keep the growing base.',
   f'Model P={int(population):,}({1+annual})^{years}; population is a count, not rand.',
   f'Evaluate the power before rounding: {int(population):,}×({1+annual})^{years}≈{int(final):,}.',
   f'Answer: {answer}. Round only after the final multiplication.']
  bad=[f'{int((population*(1+annual*years)).quantize(D('1'))):,} residents',f'{int((population*(1-annual)**years).quantize(D('1'))):,} residents',f'{int((population*(1+annual)**(years-1)).quantize(D('1'))):,} residents']
  v['values'].update(principal=str(population),rate=str(annual),amount=str(final),direction='up',unit='people')
 elif mode==3:
  decline=s%2==0;change=1-rate if decline else 1+rate
  amount=money(p*change**years);direction='depreciates' if decline else 'rises with inflation';sign='−' if decline else '＋'
  problem=f'An item valued at {rand(p)} {direction} by {ratepct}% each year for {years} years. Estimate its value after {years} years, rounding only at the end.'
  answer=rand(amount)
  actions=[f'Identify the starting value {rand(p)}, rate {ratepct}%, and {years} successive years.',
   f'Use one annual multiplier {change}; each year acts on the previous value.',
   f'Write A={rand(p)}(1 {sign} {rate})^{years}, without rounding the intermediate balance.',
   f'Calculate {rand(p)} × {change}^{years}={rand(amount)}.',
   f'Answer: {answer}. A multiplier below 1 gives a lower value; above 1 gives a higher value.']
  bad=[rand(p*(1-rate*years if decline else 1+rate*years)),rand(p*(1+rate if decline else 1-rate)**years),rand(p*change**(years-1))]
  v['values'].update(amount=str(amount),direction='down' if decline else 'up')
 elif mode==4:
  cash=p+D(3000);deposit=money(cash*D('0.2'));balance=cash-deposit;term=2+(s%3);int_rate=D(6+(s%7))/100;interest=money(balance*int_rate*term);instalment=money((balance+interest)/(term*12));total=money(deposit+balance+interest)
  problem=f'A laptop costs {rand(cash)} cash. A buyer pays a 20% deposit and finances the balance at {int(int_rate*100)}% simple interest per year over {term} years, with no fees. Find the deposit, financed balance and monthly instalment.'
  answer=f'deposit {rand(deposit)}; balance {rand(balance)}; monthly {rand(instalment)}'
  actions=[f'Calculate deposit: 20% of {rand(cash)}={rand(deposit)}.',
   f'Financed balance is cash price minus deposit: {rand(cash)}−{rand(deposit)}={rand(balance)}.',
   f'Interest on the financed balance: {rand(balance)}×{int(int_rate*100)}%×{term}={rand(interest)}.',
   f'The financed amount plus interest is {rand(balance+interest)} over {term*12} equal months.',
   f'Answer: {answer}. Divide {rand(balance+interest)} by {term*12}; fees are excluded.']
  bad=[f'deposit {rand(deposit)}; balance {rand(balance)}; monthly {rand((cash+interest)/(term*12))}',f'deposit {rand(deposit)}; balance {rand(cash)}; monthly {rand(instalment)}',f'deposit {rand(cash*D('.1'))}; balance {rand(balance)}; monthly {rand(instalment)}']
  v['values'].update(principal=str(cash),rate=str(int_rate),years=term,deposit=str(deposit),balance=str(balance),interest=str(interest),amount=str(balance+interest),months=term*12,instalment=str(instalment))
 elif mode==5 and s%3==0:
  exchange=D(15+s%6)+D('.50');new_rate=exchange+D('.75');foreign=D(50+10*(s%17));old=money(foreign*exchange);new=money(foreign*new_rate);increase=money(new-old)
  problem=f'One US dollar costs R{exchange:.2f}, then the rate rises to R{new_rate:.2f} per US dollar. How much more does a US${foreign:.2f} purchase cost in rand? Ignore fees.'
  answer=f'{rand(increase)} more'
  actions=[f'The old and new quotes are both rand per US dollar: R{exchange:.2f} and R{new_rate:.2f}.',
   f'Hold the same foreign purchase of US${foreign:.2f} for both conversions.',
   f'Old rand cost = {foreign}×{exchange}={rand(old)}.',
   f'New rand cost = {foreign}×{new_rate}={rand(new)}; subtract old from new.',
   f'Answer: {answer}. Check {rand(new)}−{rand(old)}={rand(increase)}.']
  bad=[f'{rand(new)} more',f'{rand(old)} more',f'{rand(foreign)} more']
  v['values'].update(principal=str(foreign),rate=str(exchange),new_rate=str(new_rate),amount=str(new),old_amount=str(old),difference=str(increase),direction='compare',unit='ZAR')
 elif mode==5:
  exchange=D(15+(s%8))+D('0.50');foreign=D(35+5*(s%14));rands=money(exchange*foreign);reverse=s%2==0
  problem=(f'A travel budget is {rand(rands)}. At R{exchange:.2f} per US dollar, how many US dollars can be bought? Ignore fees.' if reverse else f'A hotel charges US${foreign:.2f}. At R{exchange:.2f} per US dollar, calculate the cost in rand. Ignore fees.')
  answer=f'US${money(rands/exchange):,.2f}' if reverse else rand(rands)
  actions=[f'Read the unit: one US dollar costs R{exchange:.2f}.',f'Identify the starting amount: {rand(rands)}.' if reverse else f'Identify the starting amount: US${foreign:.2f}.',
   'To obtain dollars from rand, divide by rand per dollar.' if reverse else 'To obtain rand from dollars, multiply by rand per dollar.',
   f'Calculate {rand(rands)} ÷ {exchange} = {answer} (rounded to cents).' if reverse else f'Calculate {foreign} × {exchange} = {answer}.',
   f'Answer: {answer}. Check that reversing the conversion restores the starting value within rounding.']
  bad=[rand(rands*exchange) if reverse else f'US${foreign:.2f}',f'US${money(rands):,.2f}' if reverse else rand(foreign/exchange),rand(exchange) if reverse else rand(foreign)]
  v['values'].update(principal=str(rands if reverse else foreign),rate=str(exchange),amount=str(money(rands/exchange) if reverse else rands),direction='divide' if reverse else 'multiply',unit='USD' if reverse else 'ZAR')
 if n==6:
  reasons={1:'The time in months was not converted to years.',2:'Simple interest was used where annual compounding is required.',3:'The wrong annual multiplier or number of years was used.',4:'The deposit was included in the financed principal.',5:'The quoted rand-per-dollar rate was used in the wrong conversion or treated as the total cost.'}
  reason=reasons[mode];claim=bad[0];correct=answer
  problem+=f' A learner instead claims {claim}. Identify the first error and give the correct result.'
  actions=[actions[0],f'Inspect the learner’s claim: {claim}. Keep the original quantities and their units visible.',
   f'First error: {reason} Return to the original rate, base and period.',actions[3],
   f'Answer: first error is {reason} Correct result: {correct}. Check it against the original question.']
  answer=f'first error is {reason} Correct result: {correct}'
  bad=[f'No error; {claim}',f'first error: {reason} correct: {claim}',f'No error; {correct}']
 assert len(set([answer,*bad]))==4,(n,i,answer,bad)
 v['values']['answer']=answer
 return {'id':f'g10-fin-l{n:02}-w{i:02}','problem':problem,'actions':actions,'answer':answer,'check':actions[-1], 'visual':v,'lesson':n,'wrong':bad,'misconception':'Choose the correct base, multiplier and period; keep the stated units until the last rounding.', 'difficulty':'foundation' if i<=2 else 'easy' if i<=5 else 'standard' if i<=9 else 'intermediate' if i<=12 else 'exam'}
def item(n,i,variant,prefix):
 q=case(n,i,variant);position=i%4;opts=[q['answer'],*q['wrong']];opts=opts[-position:]+opts[:-position] if position else opts
 assert opts[position]==q['answer']
 return {'id':f'g10-fin-l{n:02}-{prefix}{i:02}','prompt':q['problem'],'options':opts,'answer_index':position,'memo':' '.join(q['actions']),'source':f'grade10-fin-lesson-{n:02}.md'}
def build():
 DOC.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True);manifest=[]
 for n,title in TITLES.items():
  worked=[{k:v for k,v in case(n,i).items() if k!='wrong'} for i in range(1,16)]
  data={'source':f'grade10-fin-lesson-{n:02}.md','worked':worked,'practice':[item(n,i,1,'p') for i in range(1,16)],'mastery':[item(n,i+15,2,'m') for i in range(1,6)],'reassessment':[item(n,i+20,3,'r') for i in range(1,4)]}
  assert len({x['problem'] for x in worked})>=10
  lines=[f'# Grade 10 Topic 9 · Lesson {n}: {title}',f'Authority: [DBE Grade 10 ATP]({ATP}), Term 3 Finance and Growth. Original Athena examples.','Status: teacher and browser review required. Currency is rounded to cents at the final step.']
  for q in worked:lines += [f'## {q["id"]}: {q["problem"]}',f'Visual contract: {json.dumps(q["visual"],ensure_ascii=False)}',*[f'{j}. {a}' for j,a in enumerate(q['actions'],1)],f'**Answer:** {q["answer"]}. **Misconception:** {q["misconception"]}']
  for label,key in [('Practice','practice'),('Mastery','mastery'),('Parallel reassessment','reassessment')]:
   lines.append(f'## {label} answer key')
   for q in data[key]:lines.append(f'- {q["id"]}: {q["prompt"]} Options: {" | ".join(q["options"])}. Correct: {q["options"][q["answer_index"]]}. {q["memo"]}')
  source=DOC/data['source'];source.write_text('\n\n'.join(lines)+'\n',encoding='utf-8')
  (OUT/f'finance_{n:02}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  manifest.append({'lesson_id':f'g10-fin-{n:02}','source':source.name,'source_sha256':sha256(source.read_bytes()).hexdigest(),'worked':15,'practice':15,'mastery':5,'reassessment':3,'status':'teacher_review_required','teacher_approved':False,'browser_accepted':False})
 (DOC/'topic09-acceptance-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
 (DOC/'topic09-batch-acceptance.md').write_text(f'# Grade 10 Topic 9: Finance and Growth\n\n[DBE Grade 10 ATP]({ATP}) covers simple and compound growth, hire purchase, inflation, population and exchange rates. Six authored lessons include 90 worked, 90 four-choice practice, 30 mastery and 18 reassessment questions. Teacher and browser acceptance pending.\n',encoding='utf-8')
if __name__=='__main__':build()
