"""Original Grade 9 probability questions with exact rational keys."""
import json
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/curriculum/grade9/probability';OUT=ROOT/'backend/app/curriculum/grade9/generated'
ATP='https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2026%20ATPs/2026_ATP_Mathematics_Grade%209.pdf'
TITLES={1:'Sample spaces and equally likely outcomes',2:'Two-way tables and conditional counts',3:'Tree diagrams and compound events',4:'Experimental versus theoretical relative frequency',5:'Combined events, first-error diagnosis and reassessment'}
def case(n,i,variant=0):
 seed=i+(19 if variant==3 else 16 if variant==2 else 15 if variant else 0);v={'lesson':n}
 if n==1:
  N=6+seed;fav=N//3;prob=Fraction(fav,N);v.update(model='sample_grid',outcomes=list(range(1,N+1)),favourable=fav)
  problem=f'A fair spinner has equally sized sectors numbered 1 to {N}. List the sample space size and find P(a multiple of 3).'
  actions=[f'List all sectors 1, 2, …, {N}; there are {N} equally likely outcomes.',f'Mark multiples of 3: {", ".join(str(k) for k in range(1,N+1) if k%3==0)}.',f'Favourable outcomes = {fav}; possible outcomes = {N}.','Probability = '+f'{fav}/{N}'+(f' = {prob}' if str(prob)!=f'{fav}/{N}' else '')+'.',f'Check: 0 ≤ {prob} ≤ 1; only multiples of 3 are highlighted.']
  answer=f'sample space size = {N}; P(multiple of 3) = {prob}';wrong=[f'sample space size = {N}; P(multiple of 3) = {Fraction(fav+d,N)}' for d in (1,2,-1)]
 elif n==2:
  a=5+seed;b=3+seed%5;c=4+seed%4;d=7+seed%3;row=a+b;prob=Fraction(a,row)
  v.update(model='two_way',table=[[a,b],[c,d]],row_total=row,column_total=a+c,grand_total=a+b+c+d)
  problem=f'A survey records Grade 9 bus {a}, Grade 9 walk {b}, Grade 8 bus {c}, Grade 8 walk {d}. Find P(bus | Grade 9).'
  actions=[f'Write the table: Grade 9 bus {a}, walk {b}; Grade 8 bus {c}, walk {d}.',f'Grade 9 row total = {a} + {b} = {row}; the full survey has {a+b+c+d}.',f'Given Grade 9, restrict attention to the {row} Grade 9 learners.',f'Of these, {a} use the bus: P(bus | Grade 9) = {a}/{row}'+(f' = {prob}' if str(prob)!=f'{a}/{row}' else '')+'.',f'Check the condition: use the Grade 9 row denominator {row}, not the grand total {a+b+c+d}.']
  answer=f'P(bus | Grade 9) = {prob}';wrong=[f'P(bus | Grade 9) = {Fraction(a+dlt,row)}' for dlt in (1,2,-1)]
 elif n==3:
  red=3+seed;blue=2+seed%4;total=red+blue;prob=Fraction(red*(red-1),total*(total-1))
  v.update(model='tree',red=red,blue=blue,first_red_num=red,first_red_den=total,second_red_num=red-1,second_red_den=total-1,prob_num=prob.numerator,prob_den=prob.denominator)
  problem=f'A bag has {red} red and {blue} blue counters. Draw twice without replacement. Find P(red then red).'
  actions=[f'First draw: {red} red out of {total} counters, so P(R₁) = {red}/{total}.',f'After a red draw, {red-1} red counters remain among {total-1}.',f'Follow the red-to-red path: P(R₂ | R₁) = {red-1}/{total-1}.',f'Multiply along that path: ({red}/{total}) × ({red-1}/{total-1}) = {prob}.',f'Check the second denominator decreased by one because the first counter was not replaced.']
  answer=f'P(red then red) = {prob}';wrong=[f'P(red then red) = {Fraction(red*(red-1)+dlt,total*(total-1))}' for dlt in (1,2,-1)]
 elif n==4:
  trials=20+seed*2;heads=trials//2+3+seed%3;observed=Fraction(heads,trials);prediction=25
  v.update(model='relative_frequency',trials=trials,heads=heads,tails=trials-heads,predicted_heads=prediction)
  problem=f'A fair coin gave heads {heads} times in {trials} tosses. Find the experimental relative frequency of heads and the theoretical prediction for heads in 50 new tosses.'
  actions=[f'Observed heads = {heads}; observed tails = {trials-heads}; total = {trials}.',f'Experimental relative frequency of heads is {heads}/{trials}'+(f' = {observed}' if str(observed)!=f'{heads}/{trials}' else '')+'.',f'The fair-coin theoretical probability of heads is 1/2, which need not equal {observed}.',f'Theoretical prediction for 50 new tosses = 50 × 1/2 = {prediction}.',f'Check: observed {heads}/{trials} describes past trials; {prediction} is an expectation, not a guarantee.']
  answer=f'experimental frequency = {observed}; predicted heads in 50 = {prediction}';wrong=[f'experimental frequency = {Fraction(heads+dlt,trials)}; predicted heads in 50 = {prediction}' for dlt in (1,2,-1)]
 else:
  N=6+seed*2;fav=N//3;prob=Fraction(fav,2*N)
  v.update(model='joint_grid',sectors=N,multiples_of_three=fav,coin_outcomes=['H','T'],favourable_pairs=fav,total_pairs=2*N)
  problem=f'A fair spinner numbered 1 to {N} and a fair coin are used together. A learner adds P(multiple of 3) and P(heads) for “multiple of 3 AND heads.” Find the first error and the correct probability.'
  actions=[f'List spinner outcomes 1 to {N} and coin outcomes H, T; there are {2*N} equally likely pairs.',f'The spinner has {fav} multiples of 3, giving {fav} pairs with heads.',f'The first error is adding probabilities for an AND event; use the joint pairs or multiply independent probabilities.',f'P(multiple of 3 AND heads) = ({fav}/{N}) × (1/2) = {fav}/{2*N} = {prob}.',f'Check the {fav} highlighted favourable pairs among {2*N}; the result is between 0 and 1.']
  answer=f'first error: added for AND; correct probability = {prob}';wrong=[f'first error: added for AND; correct probability = {Fraction(fav+dlt,2*N)}' for dlt in (1,2,-1)]
 assert len(set([answer,*wrong]))==4,(n,i)
 return {'id':f'g9-prob-l{n:02}-w{i:02}' if not variant else f'g9-prob-l{n:02}-v{variant}-w{i:02}','problem':problem,'actions':actions,'answer':answer,'check':actions[-1],'wrong':wrong,'misconception':'Choose the correct sample space and denominator, then distinguish a path product from addition and observation from prediction.','visual':{'family':'probability','values':v},'lesson':n}
def choice(n,i,variant,prefix):
 c=case(n,i,variant);opts=[c['answer'],*c['wrong']];pos=i%4;opts=opts[4-pos:]+opts[:4-pos] if pos else opts
 return {'id':f'g9-prob-l{n:02}-{prefix}{i:02}','prompt':c['problem'],'options':opts,'answer_index':pos,'memo':' '.join(c['actions']),'source':f'lesson-{n:02}.md'}
def build():
 DOC.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True);manifest=[]
 for n,title in TITLES.items():
  worked=[{k:v for k,v in case(n,i).items() if k!='wrong'}|{'difficulty':'foundation' if i<=2 else 'easy' if i<=5 else 'standard' if i<=9 else 'intermediate' if i<=12 else 'exam'} for i in range(1,16)]
  data={'source':f'lesson-{n:02}.md','worked':worked,'practice':[choice(n,i,1,'p') for i in range(1,16)],'mastery':[choice(n,i+15,2,'m') for i in range(1,6)],'reassessment':[choice(n,i+18,3,'r') for i in range(1,4)]}
  assert len({c['problem'] for c in worked})==15
  lines=[f'# Grade 9 Topic 13 · Lesson {n}: {title}',f'Authority: [DBE 2026 Grade 9 Mathematics ATP]({ATP}), Term 3. Original Athena questions.','Status: teacher and browser review required. Show the sample space, denominators, branches or trials before the result.']
  for c in worked:lines.extend([f'## {c["id"]}: {c["problem"]}',f'Visual: {json.dumps(c["visual"],ensure_ascii=False)}',*[f'{j}. {step}' for j,step in enumerate(c['actions'],1)],f'**Answer:** {c["answer"]}. **Misconception:** {c["misconception"]}'])
  for label,key in [('Practice','practice'),('Mastery','mastery'),('Changed-value reassessment','reassessment')]:
   lines.append(f'## {label} answer key')
   for c in data[key]:lines.append(f'- {c["id"]}: {c["prompt"]} Options: {" | ".join(c["options"])}. Correct: {c["options"][c["answer_index"]]}. {c["memo"]}')
  source=DOC/data['source'];source.write_text('\n\n'.join(lines)+'\n',encoding='utf-8');(OUT/f'probability_{n:02}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  manifest.append({'lesson_id':f'g9-prob-{n:02}','source':source.name,'source_sha256':sha256(source.read_bytes()).hexdigest(),'worked':15,'practice':15,'mastery':5,'reassessment':3,'status':'teacher_review_required','teacher_approved':False,'browser_accepted':False})
 (DOC/'topic13-acceptance-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
 (DOC/'topic13-batch-acceptance.md').write_text(f'# Grade 9 Topic 13: Probability\n\n[DBE 2026 Grade 9 Mathematics ATP, Term 3]({ATP}) includes two-way tables, tree diagrams and experimental relative frequency. Five Athena lessons contain 75 worked examples, 75 four-choice practice items, 25 mastery items and 15 changed-value reassessments. Teacher and browser acceptance remain required.\n',encoding='utf-8')
if __name__=='__main__':build()
