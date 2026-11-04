"""Deterministic original Grade 9 Topic 1 bank; no questions are generated at request time.

Review the compiled Markdown and JSON before changing lesson readiness. All money uses
whole rand amounts so that the displayed options have one exact interpretation.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from math import gcd
from pathlib import Path
import json
import hashlib

ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/curriculum/grade9/whole-numbers'
OUT=ROOT/'backend/app/curriculum/grade9/generated'
TITLES={3:'Ratio and rate',4:'Direct and inverse proportion',5:'Percentages and transactions',6:'Budgets and accounts',7:'Loans and interest',8:'Exchange, commission and rentals'}

def money(x):return f'R{int(x):,}'.replace(',',' ')
WRONG_METHODS={
 'ratio-order-or-one-sided-scaling':['Reverses the stated order of the colours.','Leaves the ratio unreduced.','Uses a combined total instead of the blue part.'],
 'rate-units':['Multiplies distance by time instead of dividing.','Selects the time as the speed.','Reverses the units.'],
 'unmatched-units':['Chooses the dearer pack after comparing per kg.','Compares the total prices without matching masses.','Chooses the dearer pack and uses unmatched total prices.'],
 'direct-scale':['Multiplies total price by item count.','Adds a count to a currency amount.','Stops at one unit instead of the requested count.'],
 'direct-instead-of-inverse':['Scales time directly with worker count.','Reports total worker-days as calendar days.','Keeps the original time despite a change in workers.'],
 'ratio-share':['Finds the first group instead of the second.','Reports one part instead of the second group.','Reports the entire amount instead of a share.'],
 'wrong-percentage-base':['Reports the discount or VAT component instead of final price.','Adds a discount or subtracts VAT.','Treats the percent number as a rand amount.'],
 'wrong-vat-base':['Reports only VAT instead of total.','Subtracts VAT from the original price.','Adds 15 rand instead of 15 percent.'],
 'profit-sign':['Confuses profit with loss.','Adds cost and selling price.','Uses the wrong sign and sum.'],
 'sequential-base':['Assumes equal percentages cancel or uses the old base.','Stops after discount.','Adds VAT on the reduced price to the old price.'],
 'debit-credit':['Reports total expenses as balance.','Adds expenses to income.','Forgets other expenses.'],
 'budget-time-base':['Reverses the affordability decision.','Reports the remaining balance rather than a decision.','Reports the payment amount rather than a decision.'],
 'compound-instead-of-simple':['Reports interest without the principal.','Counts only one year.','Counts an extra year.'],
 'simple-instead-of-compound':['Uses simple interest on the initial principal.','Reports simple interest without the principal.','Uses only the first compound year.'],
 'forgot-deposit':['Omits the deposit.','Confuses cash and hire totals.','Counts only one instalment.'],
 'exchange-direction':['Omits the fee.','Multiplies by the quoted rand-per-unit rate.','Adds the fee instead of deducting it.'],
 'commission-base':['Reports commission without basic pay.','Adds the percent number as currency.','Reports sales plus basic pay.'],
 'ignored-fixed-fee':['Chooses the wrong total.','Uses an incorrect difference after choosing the right plan.','Uses an incorrect difference and the wrong plan.'],
 'budget-variance':['Reports the planned balance instead of actual.','Confuses expenses with remaining balance.','Adds actual expenses to income.'],
 'loan-total-cost':['Chooses the dearer offer.','Compares deposits only.','Omits the deposit when comparing total cost.'],
 'exchange-rental':['Chooses the dearer plan after converting.','Compares foreign units with rand.','Forgets the conversion or fixed charge.']
}
def case(prompt, givens, steps, answer, wrongs, visual, tag, verify):
    assert len(steps)>=3 and len(wrongs)==3 and len(set([answer,*wrongs]))==4,(prompt,answer,wrongs)
    assert all(isinstance(s,str) and s for s in steps) and tag in WRONG_METHODS
    return dict(problem=prompt,givens=givens,actions=[*steps, 'Check: '+verify],answer=answer,wrongs=wrongs,visual=visual,misconception=tag,wrong_methods=WRONG_METHODS[tag],check='Check: '+verify)

def ratio(a,b,unit='counters'):
    d=gcd(a,b);ans=f'{a//d}:{b//d}'
    return case(f'A box has {a} blue and {b} red {unit}. Write the blue:red ratio in simplest form.',
        [f'Blue {a}',f'Red {b}'],[f'Identify the ordered ratio blue:red as {a}:{b}.',f'The greatest common factor of {a} and {b} is {d}.',f'Divide both parts by {d}: {a}÷{d}:{b}÷{d} = {ans}.'],ans,
        [f'{b//d}:{a//d}',f'{a}:{b}',f'{a+b}:{b}'],{'family':'ratio','bars':[a,b],'labels':['blue','red']},'ratio-order-or-one-sided-scaling',f'{a//d}×{d}={a} and {b//d}×{d}={b}; the order remains blue:red.')

def rate(distance,time,unit='km'):
    v=distance//time;assert distance%time==0
    return case(f'A cyclist travels {distance} {unit} in {time} hours at a constant speed. Find the rate in {unit}/h.',
        [f'Distance {distance} {unit}',f'Time {time} h'],[f'Write speed as distance ÷ time = {distance} {unit} ÷ {time} h.',f'Divide {distance} by {time}: {v}.',f'Keep the quotient units: {v} {unit}/h.'],f'{v} {unit}/h',
        [f'{distance*time} {unit}/h',f'{time} {unit}/h',f'{v} h/{unit}'],{'family':'rate','table':[[distance,time],[v,1]],'units':[unit,'h']},'rate-units',f'{v} {unit}/h × {time} h = {distance} {unit}.')

def unit_rate(price,quantity,other_price,other_quantity):
    a=price//quantity;b=other_price//other_quantity;assert price%quantity==other_price%other_quantity==0 and a!=b
    chosen='A' if a<b else 'B';wrong='B' if a<b else 'A'
    return case(f'Pack A costs {money(price)} for {quantity} kg; pack B costs {money(other_price)} for {other_quantity} kg. Which costs less per kg, and by how much?',
        [f'A {money(price)} / {quantity} kg',f'B {money(other_price)} / {other_quantity} kg'],[f'Divide A price by its mass: {money(price)}÷{quantity} = {money(a)}/kg.',f'Divide B price by its mass: {money(other_price)}÷{other_quantity} = {money(b)}/kg.',f'Compare equal units: pack {chosen} costs {money(abs(a-b))}/kg less.'],f'{chosen}, {money(abs(a-b))}/kg',
        [f'{wrong}, {money(abs(a-b))}/kg',f'{chosen}, {money(abs(price-other_price))}/kg',f'{wrong}, {money(abs(price-other_price))}/kg'],{'family':'rate','table':[[price,quantity],[other_price,other_quantity]],'units':['R','kg']},'unmatched-units',f'{money(min(a,b))}/kg < {money(max(a,b))}/kg.')

def direct(q1,c1,q2,thing='notebooks'):
    per=c1//q1;assert c1%q1==0 and q2!=q1;value=per*q2
    return case(f'{q1} identical {thing} cost {money(c1)}. At the same price per item, what do {q2} cost?',
        [f'{q1} items',money(c1),f'{q2} items'],[f'Test the relationship: more {thing} means more cost at a fixed unit price.',f'One item costs {money(c1)}÷{q1} = {money(per)}.',f'Multiply the unit cost by {q2}: {money(per)}×{q2} = {money(value)}.'],money(value),
        [money(c1*q2),money(c1+q2),money(per)],{'family':'direct','table':[[q1,c1],[q2,value]],'units':['items','R']},'direct-scale',f'{value}÷{q2}={per} and {c1}÷{q1}={per} rand per item.')

def inverse(workers,days,new_workers,thing='painters'):
    total=workers*days;assert total%new_workers==0 and new_workers!=workers;result=total//new_workers
    return case(f'{workers} {thing} finish an equal-size job in {days} days. At the same individual rate, how many days will {new_workers} {thing} need?',
        [f'{workers} {thing}',f'{days} days',f'{new_workers} {thing}'],[f'Test the relationship: more {thing} need fewer days for the same job.',f'The fixed job needs {workers}×{days}={total} worker-days.',f'Divide by {new_workers} workers: {total}÷{new_workers}={result} days.'],f'{result} days',
        [f'{days*new_workers//workers} days',f'{total} days',f'{days} days'],{'family':'inverse','table':[[workers,days],[new_workers,result]],'units':['workers','days']},'direct-instead-of-inverse',f'{new_workers}×{result}={workers}×{days}={total} worker-days.')

def share(total,a,b,context='two clubs'):
    assert total%(a+b)==0;unit=total//(a+b);x=a*unit;y=b*unit
    return case(f'Share {money(total)} between {context} in the ratio {a}:{b}. How much does the second group receive?',
        [money(total),f'{a}:{b}'],[f'Total parts are {a}+{b}={a+b}.',f'One part is {money(total)}÷{a+b}={money(unit)}.',f'The second group has {b} parts: {b}×{money(unit)}={money(y)}.'],money(y),
        [money(x),money(unit),money(total)],{'family':'share','bars':[a,b],'labels':['first parts','second parts']},'ratio-share',f'{money(x)}+{money(y)}={money(total)}, and {x}:{y}={a}:{b}.')

def discount(price,pct):
    assert price*pct%100==0;delta=price*pct//100;out=price-delta
    return case(f'A jacket marked {money(price)} is discounted by {pct}%. What is its sale price?',
        [money(price),f'{pct}% discount'],[f'The percentage base is the marked price, {money(price)}.',f'The discount is {pct}% of {money(price)} = {money(delta)}.',f'Subtract the discount: {money(price)}−{money(delta)}={money(out)}.'],money(out),
        [money(delta),money(price+delta),money(price-pct)],{'family':'transaction','timeline':[price,delta,out],'labels':['marked','discount','sale']},'wrong-percentage-base',f'{money(out)}+{money(delta)}={money(price)}.')

def vat(price,pct=15):
    assert price*pct%100==0;delta=price*pct//100;out=price+delta
    return case(f'A service costs {money(price)} before {pct}% VAT. Calculate the VAT-inclusive price.',
        [money(price),f'{pct}% VAT'],[f'The VAT base is the before-tax price, {money(price)}.',f'VAT is {pct}% of {money(price)} = {money(delta)}.',f'Add VAT: {money(price)}+{money(delta)}={money(out)}.'],money(out),
        [money(delta),money(price-delta),money(price+pct)],{'family':'transaction','timeline':[price,delta,out],'labels':['before tax','VAT','total']},'wrong-vat-base',f'{money(out)}−{money(delta)}={money(price)}.')

def profit(cost,sell):
    assert sell!=cost;delta=abs(sell-cost);term='profit' if sell>cost else 'loss';wrong='loss' if term=='profit' else 'profit'
    return case(f'A shop buys a lamp for {money(cost)} and sells it for {money(sell)}. Was this a profit or a loss? Give the amount.',
        [f'Cost {money(cost)}',f'Selling price {money(sell)}'],[f'Compare selling price {money(sell)} with cost {money(cost)}.',f'The difference is {money(max(sell,cost))}−{money(min(sell,cost))}={money(delta)}.',f'Selling is {"higher" if sell>cost else "lower"} than cost, so it is a {term} of {money(delta)}.'],f'{term} {money(delta)}',
        [f'{wrong} {money(delta)}',f'{term} {money(sell+cost)}',f'{wrong} {money(sell+cost)}'],{'family':'transaction','timeline':[cost,sell,delta],'labels':['cost','sale','difference']},'profit-sign',f'{money(cost)} {"+" if sell>cost else "−"} {money(delta)} = {money(sell)}.')

def sequential(price,discount_pct,vat_pct=15):
    assert price*discount_pct%100==0;reduced=price*(100-discount_pct)//100;assert reduced*vat_pct%100==0
    vat_amount=reduced*vat_pct//100;end=reduced+vat_amount
    return case(f'A device priced {money(price)} gets {discount_pct}% off, then {vat_pct}% VAT on the reduced price. What is the final price?',
        [money(price),f'{discount_pct}% off',f'{vat_pct}% VAT'],[f'The discount base is {money(price)}; subtract {money(price*discount_pct//100)} to get {money(reduced)}.',f'VAT is on the new base {money(reduced)}: {vat_pct}% = {money(vat_amount)}.',f'Add VAT to the reduced price: {money(reduced)}+{money(vat_amount)}={money(end)}.'],money(end),
        [money(price),money(reduced),money(price+vat_amount)],{'family':'transaction','timeline':[price,reduced,end],'labels':['original','after discount','after VAT']},'sequential-base',f'{money(end)}−{money(vat_amount)}={money(reduced)}; the second base was not {money(price)}.')

def budget(income,expenses,extra=0):
    out=sum(expenses)+extra;balance=income-out;assert balance>0
    return case(f'A household receives {money(income)} monthly. Rent, food and transport are {money(expenses[0])}, {money(expenses[1])} and {money(expenses[2])}; other costs are {money(extra)}. What remains?',
        [f'Income {money(income)}',*[money(x) for x in expenses],f'Other {money(extra)}'],[f'Use a monthly ledger; start with income {money(income)}.',f'Add expenses: {" + ".join(money(x) for x in [*expenses,extra])} = {money(out)}.',f'Subtract total spending from income: {money(income)}−{money(out)}={money(balance)}.'],money(balance),
        [money(out),money(income+out),money(income-expenses[0])],{'family':'ledger','income':income,'expenses':[*expenses,extra],'balance':balance},'debit-credit',f'{money(balance)}+{money(out)}={money(income)}.')

def afford(income,expenses,plan):
    remaining=income-sum(expenses);assert remaining>0 and remaining!=plan
    yes=remaining>=plan;answer='Affordable' if yes else 'Not affordable';wrong='Not affordable' if yes else 'Affordable'
    return case(f'Monthly income is {money(income)} and fixed expenses are {", ".join(money(x) for x in expenses)}. Is a new monthly payment of {money(plan)} affordable without borrowing?',
        [f'Income {money(income)}',f'Payment {money(plan)}',*[money(x) for x in expenses]],[f'The expense base is the same month as income.',f'After fixed expenses, {money(income)}−{money(sum(expenses))}={money(remaining)} remains.',f'Compare {money(remaining)} with {money(plan)}: {answer.lower()}.'],answer,
        [wrong,money(remaining),money(plan)],{'family':'ledger','income':income,'expenses':expenses,'balance':remaining,'plan':plan},'budget-time-base',f'{money(remaining)} {"≥" if yes else "<"} {money(plan)}.')

def simple(principal,rate,years):
    assert principal*rate%100==0;annual=principal*rate//100;interest=annual*years;end=principal+interest
    return case(f'Invest {money(principal)} at {rate}% simple interest per year for {years} years. Find the final balance.',
        [money(principal),f'{rate}% p.a.',f'{years} years'],[f'With simple interest, every year uses the original {money(principal)} as base.',f'One year adds {rate}% of {money(principal)} = {money(annual)}; {years} years add {money(interest)}.',f'Final balance is {money(principal)}+{money(interest)}={money(end)}.'],money(end),
        [money(interest),money(principal+annual),money(principal+annual*(years+1))],{'family':'interest','balances':[principal,*[principal+annual*i for i in range(1,years+1)]],'kind':'simple'},'compound-instead-of-simple',f'{money(end)}−{money(principal)}={money(interest)}={years}×{money(annual)}.')

def compound(principal,rate,years):
    assert all(principal*(100+rate)**i%100**i==0 for i in range(1,years+1));balances=[principal*(100+rate)**i//100**i for i in range(years+1)];end=balances[-1]
    return case(f'Invest {money(principal)} at {rate}% compound interest per year for {years} years. Find the final balance.',
        [money(principal),f'{rate}% p.a.',f'{years} years'],[f'Each year uses the previous balance as the new percentage base.',*[f'Year {i}: {money(balances[i-1])}×{100+rate}/100 = {money(balances[i])}.' for i in range(1,years+1)],f'After {years} years the balance is {money(end)}.'],money(end),
        [money(principal+principal*rate*years//100),money(principal*rate*years//100),money(principal+principal*rate//100)],{'family':'interest','balances':balances,'kind':'compound'},'simple-instead-of-compound',f'{money(balances[-2])}×{100+rate}/100={money(end)}.')

def hire(cash,deposit,instalment,months):
    paid=deposit+instalment*months;assert paid>cash
    return case(f'A {money(cash)} appliance is offered on hire purchase: {money(deposit)} deposit and {months} payments of {money(instalment)}. What is the total paid?',
        [f'Cash {money(cash)}',f'Deposit {money(deposit)}',f'{months}×{money(instalment)}'],[f'Count every instalment: {months}×{money(instalment)} = {money(months*instalment)}.',f'Include the deposit of {money(deposit)}.',f'Total paid = {money(deposit)}+{money(months*instalment)}={money(paid)}.'],money(paid),
        [money(months*instalment),money(cash),money(deposit+instalment)],{'family':'interest','balances':[deposit,deposit+months*instalment],'kind':'hire'},'forgot-deposit',f'{money(paid)}−{money(cash)}={money(paid-cash)} above cash price.')

def exchange(rand,rate,fee):
    assert rand%rate==0;units=rand//rate;assert 0<fee<units;net=units-fee
    return case(f'At {money(rate)} per foreign unit, exchange {money(rand)}. The provider then charges {fee} foreign units. How many foreign units remain?',
        [f'{money(rand)}',f'{money(rate)}/unit',f'{fee} units fee'],[f'Check units: rand ÷ (rand per foreign unit) gives foreign units.',f'Convert: {money(rand)}÷{money(rate)} = {units} foreign units.',f'Deduct the foreign-currency fee: {units}−{fee}={net} foreign units.'],f'{net} foreign units',
        [f'{units} foreign units',f'{rand*rate-fee} foreign units',f'{units+fee} foreign units'],{'family':'exchange','source':rand,'rate':rate,'gross':units,'fee':fee,'net':net},'exchange-direction',f'{net}+{fee}={units}; {units}×{rate}={rand} rand.')

def commission(sales,pct,fixed):
    assert sales*pct%100==0;cut=sales*pct//100;total=cut+fixed
    return case(f'A salesperson earns {pct}% commission on {money(sales)} sales plus {money(fixed)} basic pay. Find total pay.',
        [f'Sales {money(sales)}',f'Rate {pct}%',f'Basic {money(fixed)}'],[f'Commission uses sales {money(sales)} as its base.',f'{pct}% of {money(sales)} is {money(cut)}.',f'Add basic pay: {money(cut)}+{money(fixed)}={money(total)}.'],money(total),
        [money(cut),money(sales*pct//100+fixed+pct),money(sales+fixed)],{'family':'commission','sales':sales,'rate':pct,'commission':cut,'basic':fixed,'total':total},'commission-base',f'{money(total)}−{money(fixed)}={money(cut)} commission.')

def rental(days,base_a,per_a,base_b,per_b):
    a=base_a+days*per_a;b=base_b+days*per_b;assert a!=b
    chosen='A' if a<b else 'B';wrong='B' if a<b else 'A'
    return case(f'Rent for {days} days. Plan A charges {money(base_a)} plus {money(per_a)}/day; Plan B charges {money(base_b)} plus {money(per_b)}/day. Which is cheaper and by how much?',
        [f'{days} days',f'A {money(base_a)}+{money(per_a)}/day',f'B {money(base_b)}+{money(per_b)}/day'],[f'Both plans include a fixed fee and a daily rate for {days} days.',f'A costs {money(base_a)}+{days}×{money(per_a)}={money(a)}; B costs {money(base_b)}+{days}×{money(per_b)}={money(b)}.',f'Compare totals, not daily rates: {chosen} is cheaper by {money(abs(a-b))}.'],f'{chosen} by {money(abs(a-b))}',
        [f'{wrong} by {money(abs(a-b))}',f'{chosen} by {money(abs(a-b)+base_a)}',f'{wrong} by {money(abs(a-b)+base_b)}'],{'family':'rental','days':days,'base':[base_a,base_b],'daily':[per_a,per_b],'totals':[a,b]},'ignored-fixed-fee',f'{money(max(a,b))}−{money(min(a,b))}={money(abs(a-b))}.')

def budget_variance(income,planned,actual):
    p=income-sum(planned);a=income-sum(actual);assert p>0 and a>0 and a!=p
    return case(f'A budget has monthly income {money(income)}. Planned rent, food and travel are {", ".join(money(x) for x in planned)}; actual amounts are {", ".join(money(x) for x in actual)}. How much remained after actual spending?',
      [f'Income {money(income)}',f'Planned {", ".join(money(x) for x in planned)}',f'Actual {", ".join(money(x) for x in actual)}'],
      [f'Keep planned and actual columns separate for the same month.',f'Actual spending totals {" + ".join(money(x) for x in actual)} = {money(sum(actual))}.',f'Subtract actual spending: {money(income)}−{money(sum(actual))}={money(a)}.'],money(a),
      [money(p),money(sum(actual)),money(income+sum(actual))],{'family':'ledger','income':income,'planned':planned,'expenses':actual,'balance':a},'budget-variance',f'{money(a)}+{money(sum(actual))}={money(income)}; planned balance was {money(p)}.')

def loan_choice(cash,deposit_a,monthly_a,deposit_b,monthly_b,months=12):
    a=deposit_a+months*monthly_a;b=deposit_b+months*monthly_b;assert a!=b
    choice='A' if a<b else 'B';other='B' if a<b else 'A'
    return case(f'A device costs {money(cash)} cash. Offer A: {money(deposit_a)} deposit plus {months}×{money(monthly_a)}. Offer B: {money(deposit_b)} deposit plus {months}×{money(monthly_b)}. Which offer costs less in total?',
      [f'Cash {money(cash)}',f'A deposit {money(deposit_a)}',f'B deposit {money(deposit_b)}',f'{months} monthly payments'],
      [f'Compare equal total time periods, not the monthly instalments alone.',f'A total: {money(deposit_a)}+{months}×{money(monthly_a)}={money(a)}; B total: {money(deposit_b)}+{months}×{money(monthly_b)}={money(b)}.',f'{choice} costs less by {money(abs(a-b))}.'],f'{choice} by {money(abs(a-b))}',
      [f'{other} by {money(abs(a-b))}',f'{choice} by {money(abs(deposit_a-deposit_b))}',f'{other} by {money(abs(deposit_a-deposit_b))}'],
      {'family':'interest','kind':'compare','balances':[a,b],'labels':['Offer A total','Offer B total'],'givens':[deposit_a,monthly_a,deposit_b,monthly_b,months]},'loan-total-cost',f'{money(max(a,b))}−{money(min(a,b))}={money(abs(a-b))}.')

def exchange_rental(days,foreign_base,foreign_daily,rate,fee,local_total):
    foreign=foreign_base+days*foreign_daily;rand=foreign*rate+fee;assert rand!=local_total
    choice='foreign' if rand<local_total else 'local';other='local' if choice=='foreign' else 'foreign';difference=abs(rand-local_total)
    return case(f'For {days} days, a foreign rental charges {foreign_base} foreign units plus {foreign_daily} units/day. At {money(rate)} per unit, add a {money(fee)} rand conversion fee. A local rental totals {money(local_total)}. Which costs less in rand, and by how much?',
      [f'{days} days',f'{foreign_base}+{foreign_daily}/day foreign units',f'{money(rate)}/unit',f'Fee {money(fee)}',f'Local {money(local_total)}'],
      [f'Foreign rental = {foreign_base}+{days}×{foreign_daily}={foreign} foreign units.',f'Convert and add fee: {foreign}×{money(rate)}+{money(fee)}={money(rand)}.',f'Compare {money(rand)} with local {money(local_total)}: {choice} saves {money(difference)}.'],f'{choice} by {money(difference)}',
      [f'{other} by {money(difference)}',f'{choice} by {money(abs(foreign-local_total))}',f'{other} by {money(abs(foreign-local_total))}'],
      {'family':'rental_exchange','days':days,'foreign_base':foreign_base,'foreign_daily':foreign_daily,'rate':rate,'fee':fee,'foreign':foreign,'rand_total':rand,'local_total':local_total},
      'exchange-rental',f'{money(max(rand,local_total))}−{money(min(rand,local_total))}={money(difference)}.')

BUILD={
 3:[*[ratio(*x) for x in [(18,30),(28,42),(45,60),(36,54),(72,96)]],*[rate(*x) for x in [(84,2),(135,3),(176,4),(245,5),(324,6)]],*[unit_rate(*x) for x in [(48,2,90,3),(75,3,112,4),(144,6,110,5),(96,4,135,5),(156,6,168,7)]]],
 4:[*[direct(*x) for x in [(3,45,7),(4,80,9),(5,125,8),(6,90,11),(8,144,13)]],*[inverse(*x) for x in [(4,12,6),(5,18,9),(6,20,8),(8,15,10),(9,16,12)]],*[share(*x) for x in [(420,2,5,'two sports clubs'),(720,3,5,'two charities'),(990,4,7,'two classes'),(1170,5,8,'two teams'),(1680,7,5,'two groups')]]],
 5:[*[discount(*x) for x in [(800,10),(1200,15),(1500,20),(2400,25),(3600,5)]],*[vat(x) for x in (600,1200,1800,2400,3200)],*[profit(*x) for x in [(240,300),(650,520),(800,1000),(1450,1160),(2500,3000)]],*[sequential(*x) for x in [(2000,20),(4000,10),(6000,25),(8000,15),(10000,30)]]][-15:],
 6:[*[budget(*x) for x in [(8000,[3000,1800,900],300),(9200,[3400,2100,800],400),(10500,[3900,2400,1100],600),(12000,[4500,2800,1250],750),(15000,[5600,3200,1400],1200)]],*[afford(*x) for x in [(9000,[3000,2100,1200],800),(11000,[4500,2400,1600],3000),(12500,[4600,2700,1500],2500),(14000,[5200,3400,1800],4000),(16500,[6000,4200,1600],3200)]],*[budget(*x) for x in [(11800,[4200,2700,1400],1500),(13400,[5200,2800,1700],1600),(15600,[5700,3400,1850],2100),(18000,[6400,4200,2250],2500),(21000,[7600,4800,2750],3100)]]],
 7:[*[simple(*x) for x in [(2000,5,2),(3000,8,3),(5000,6,4),(8000,10,3),(12000,5,5)]],*[compound(*x) for x in [(2000,10,2),(4000,10,3),(8000,5,2),(16000,5,3),(25000,4,2)]],*[hire(*x) for x in [(3000,600,240,12),(5000,1000,380,12),(8000,1600,620,12),(12000,2400,950,12),(15000,3000,1200,12)]]],
 8:[*[exchange(*x) for x in [(1800,20,5),(3600,20,8),(5250,21,10),(6300,21,15),(8400,24,20)]],*[commission(*x) for x in [(3000,5,200),(5000,8,300),(7500,4,450),(9000,10,500),(12000,6,650)]],*[rental(*x) for x in [(3,100,90,200,70),(4,250,60,100,110),(5,150,130,400,75),(7,500,80,200,130),(10,100,140,600,95)]]]
}
# Final rows require applying earlier skills in a new context.
BUILD[6][-2:]=[budget_variance(18500,[6500,3900,2000],[6500,4500,2400]),budget_variance(22000,[7500,4800,2600],[7800,5200,2900])]
BUILD[7][-2:]=[loan_choice(9000,1800,760,2700,690),loan_choice(16000,3200,1300,4800,1170)]
BUILD[8][-3:]=[exchange_rental(3,20,8,20,60,960),exchange_rental(5,15,9,22,55,1350),exchange_rental(7,18,10,21,70,2300)]


# Keep all five price skills in Lesson 5: early examples include both base and final price;
# the last five explicitly show distinct sequential bases.
BUILD[5]=[*[discount(*x) for x in [(800,10),(1200,15),(1500,20)]],*[vat(x) for x in (600,1200,1800)],*[profit(*x) for x in [(240,300),(650,520),(800,1000),(1450,1160)]],*[sequential(*x) for x in [(2000,20),(4000,10),(6000,25),(8000,15),(10000,30)]]]

# The independent banks are deliberately different numerical cases. Their answer
# positions rotate A/B/C/D and each non-key option is an explicit wrong method.
PRACTICE={
3:[*[ratio(*x) for x in [(24,40),(30,45),(64,80),(56,84),(81,108)]],*[rate(*x) for x in [(96,2),(150,3),(216,4),(275,5),(390,6)]],*[unit_rate(*x) for x in [(60,2,81,3),(90,3,116,4),(180,6,125,5),(120,4,140,5),(180,6,192,8)]]],
4:[*[direct(*x) for x in [(3,60,7),(4,100,9),(5,150,8),(6,120,11),(8,160,13)]],*[inverse(*x) for x in [(4,18,6),(5,24,10),(6,18,9),(8,21,12),(9,20,12)]],*[share(*x) for x in [(490,2,5,'two clubs'),(800,3,5,'two charities'),(880,4,7,'two classes'),(1560,5,8,'two teams'),(1800,7,5,'two groups')]]],
5:[*[discount(*x) for x in [(900,10),(1400,15),(1800,20)]],*[vat(x) for x in (800,1600,2600)],*[profit(*x) for x in [(350,420),(750,600),(900,1100),(1800,1440)]],*[sequential(*x) for x in [(3000,20),(5000,10),(7000,20),(10000,15),(12000,30)]]],
6:[*[budget(*x) for x in [(9500,[3200,2200,1100],500),(10800,[3600,2500,1200],800),(13000,[4900,2900,1550],700),(14500,[5500,3200,1750],850),(17000,[6200,3700,1800],1100)]],*[afford(*x) for x in [(10000,[3500,2300,1300],900),(12000,[4800,2500,1400],3500),(13500,[5200,3100,1700],2600),(15000,[5700,3900,1900],3900),(18500,[6800,4500,1800],4000)]],*[budget(*x) for x in [(12500,[4500,2800,1500],1100),(14300,[5400,3100,1900],1300),(16800,[6200,3900,1900],1700),(19500,[7200,4600,2100],2300),(23000,[8200,5600,3200],2600)]]],
7:[*[simple(*x) for x in [(2500,4,2),(4000,6,3),(6000,5,4),(9000,8,3),(14000,5,5)]],*[compound(*x) for x in [(3000,10,2),(5000,10,3),(12000,5,2),(40000,5,3),(30000,4,2)]],*[hire(*x) for x in [(4000,800,320,12),(6000,1200,460,12),(10000,2000,780,12),(14000,2800,1100,12),(18000,3600,1450,12)]]],
8:[*[exchange(*x) for x in [(2400,20,6),(4800,20,9),(6300,21,11),(7350,21,16),(9600,24,21)]],*[commission(*x) for x in [(4000,5,250),(6000,8,350),(8500,4,500),(10000,10,550),(15000,6,750)]],*[rental(*x) for x in [(3,130,100,250,75),(4,275,65,120,115),(5,180,145,450,85),(7,520,90,260,140),(10,140,150,650,100)]]]
}

PRACTICE[6][-2:]=[budget_variance(20000,[7200,4100,2500],[7300,4600,2700]),budget_variance(25000,[8500,5500,3000],[8900,6100,3200])]
PRACTICE[7][-2:]=[loan_choice(11000,2200,920,3300,830),loan_choice(19000,3800,1540,5700,1400)]
PRACTICE[8][-3:]=[exchange_rental(4,25,7,20,80,1200),exchange_rental(6,12,11,23,60,1900),exchange_rental(8,22,9,24,90,2800)]

MASTER_AND_REASSESS={
 3:[ratio(70,105),rate(288,4),unit_rate(84,3,125,5),ratio(96,144),rate(420,6),
    ratio(66,99),unit_rate(100,4,174,6),rate(392,7)],
 4:[direct(7,175,12),inverse(6,24,8),share(1320,5,6,'two clubs'),direct(9,270,14),inverse(10,18,15),
    share(1260,2,7,'two charities'),direct(7,210,11),inverse(8,24,12)],
 5:[discount(2500,20),vat(2800),profit(1700,1360),sequential(12000,25),sequential(16000,10),
    discount(2700,10),vat(3600),sequential(14000,20)],
 6:[budget(17500,[6200,3900,2100],1400),afford(13000,[5000,3200,1600],1800),budget(19500,[7300,4500,2300],900),afford(16000,[5500,3700,1900],5200),budget(22000,[8000,5100,2700],1700),
    afford(17000,[6200,3800,1800],4200),budget(24500,[8900,5700,3400],1900),afford(20000,[7500,4300,2200],6500)],
 7:[simple(7000,6,3),compound(6000,10,2),hire(7000,1400,550,12),compound(24000,5,3),simple(18000,5,4),
    hire(11000,2200,880,12),compound(35000,4,2),simple(13000,8,3)],
 8:[exchange(5400,20,7),commission(8000,5,500),rental(6,300,80,100,130),exchange(9240,21,13),rental(8,400,95,150,130),
    commission(11000,8,700),exchange(10800,24,18),rental(9,500,100,200,145)]
}

MASTER_AND_REASSESS[6][4]=budget_variance(21000,[7400,4400,2400],[7500,4800,2900])
MASTER_AND_REASSESS[7][4]=loan_choice(13000,2600,1100,3900,1000)
MASTER_AND_REASSESS[8][4]=exchange_rental(4,30,8,21,75,1500)
MASTER_AND_REASSESS[8][7]=exchange_rental(6,15,12,22,65,2200)

def extra(number,offset):
    return MASTER_AND_REASSESS[number][:5] if offset==1 else MASTER_AND_REASSESS[number][5:]

def as_item(item,number,prefix,index):
    answer=item['answer'];wrong=item['wrongs'];shift=(index-1)%4
    options=wrong.copy();options.insert(shift,answer)
    return dict(id=f'g9-whole-l{number:02}-{prefix}{index:02}',prompt=item['problem'],
                options=options,answer_index=shift,memo=f"{answer}. {' '.join(item['actions'])}",
                misconception=item['misconception'],option_rationales={v:('Correct: '+item['check'] if v==answer else 'Incorrect: '+item['wrong_methods'][wrong.index(v)]) for v in options})

def build(n):
    worked=BUILD[n];practice=PRACTICE[n];assert len(worked)==len(practice)==15,(n,len(worked),len(practice))
    # Exclude prompt collisions between practice and worked, even for the same model.
    assert not {x['problem'] for x in worked}&{x['problem'] for x in practice}
    mastery=extra(n,1);reassessment=extra(n,2)
    for bank in (worked,practice,mastery,reassessment):
        assert len({x['problem'] for x in bank})==len(bank),(n,'duplicate prompts')
    result={'source':f'lesson-{n:02}-'+TITLES[n].lower().replace(',','').replace(' ','-')+'.md',
        'worked':[{**c,'id':f'g9-whole-l{n:02}-w{i:02}',
           'difficulty':'foundation' if i<=2 else 'easy' if i<=5 else 'standard' if i<=9 else 'exam' if i<=12 else 'advanced'} for i,c in enumerate(worked,1)],
        'practice':[as_item(c,n,'p',i) for i,c in enumerate(practice,1)],
        'mastery':[as_item(c,n,'m',i) for i,c in enumerate(mastery,1)],
        'reassessment':[as_item(c,n,'r',i) for i,c in enumerate(reassessment,1)]}
    lines=[f'# Grade 9 Topic 1 · Lesson {n}: {TITLES[n]}',
      '', 'Status: authored source for mathematics and browser review; not published.',
      'Scope: DBE 2026 Grade 9 Mathematics ATP Term 1, Whole Numbers. Questions are original Athena variants.',
      'https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2026%20ATPs/2026_ATP_Mathematics_Grade%209.pdf',
      '', 'Each worked example carries exact givens, one mathematical action per step, a check, a misconception tag and a question-specific visual data contract.',
      'Learners should work practice and mastery questions independently in a book before choosing one option.', '', '## Worked examples']
    for c in result['worked']:
        lines += ['',f"### {c['id']} · {c['difficulty']}",f"Question: {c['problem']}",f"Givens: {'; '.join(c['givens'])}",
                  f"Visual: {c['visual']['family']} · {json.dumps(c['visual'],ensure_ascii=False)}",
                  *[f"{i}. {step}" for i,step in enumerate(c['actions'],1)],f"Answer: {c['answer']}",f"Misconception: {c['misconception']}"]
    for name in ('practice','mastery','reassessment'):
        lines += ['',f"## {name.title()} · private key and rationale"]
        for c in result[name]:
            lines += ['',f"### {c['id']}",f"Question: {c['prompt']}",
                *[f"{chr(65+i)}. {option}" for i,option in enumerate(c['options'])],
                f"Key: {chr(65+c['answer_index'])}",f"Memo: {c['memo']}",
                *[f"Distractor {option}: {reason}" for option,reason in c['option_rationales'].items() if not reason.startswith('Correct:')]]
    doc=DOC/result['source'];doc.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    out=OUT/f'whole_numbers_{n:02}.json';out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(n,doc.relative_to(ROOT),out.relative_to(ROOT))

if __name__=='__main__':
    DOC.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    for number in range(3,9):build(number)
    manifest=[]
    for number in range(1,9):
        generated=OUT/f'whole_numbers_{number:02}.json'
        data=json.loads(generated.read_text(encoding='utf-8'))
        source=DOC/data['source']
        manifest.append({'lesson_id':f'g9-whole-numbers-{number:02}',
          'source':data['source'],'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
          'worked_ids':[q['id'] for q in data['worked']],
          'practice_ids':[q['id'] for q in data['practice']],
          'mastery_ids':[q['id'] for q in data['mastery']],
          'reassessment_ids':[q['id'] for q in data['reassessment']],
          'worked_count':15,'practice_count':15,'mastery_count':5,'reassessment_count':3,
          'status':'teacher_review_required','browser_accepted':False,'teacher_approved':False})
    target=DOC/'topic1-acceptance-manifest.json'
    target.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(target.relative_to(ROOT))
