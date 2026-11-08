"""Original Grade 10 probability questions derived from explicit event regions."""
from pathlib import Path
from fractions import Fraction
from hashlib import sha256
import json
ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/curriculum/grade10/probability'
OUT=ROOT/'backend/app/curriculum/grade10/generated'
ATP='https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2023%20ATPs/FET%20Content%20Subjects/Grade%2010/1.580%20ATP%202023-24%20Gr%2010%20Maths%20final.pdf'
TITLES={1:'Relative frequency and theoretical probability',2:'Venn regions and two-event counts',3:'Union and intersection of two events',4:'Mutually exclusive and complementary events',5:'Mixed probability reasoning and first-error repair'}

def case(n,i,variant=0):
 s=i+variant*19
 ao=2+s%6;bo=3+(s//2)%6;both=(s//3)%5;neither=1+(s//4)%6
 if n==4 and s%2:both=0;neither=0 # complement: A and B partition S
 if n==4 and not s%2:both=0;neither=2+(s//4)%5 # exclusive but not complementary
 N=ao+bo+both+neither; A=ao+both;B=bo+both;union=ao+bo+both
 v={'lesson':n,'model':'venn','a_only':ao,'b_only':bo,'both':both,'neither':neither,'total':N,'a':A,'b':B,'union':union}
 if n==1:
  faces=6 if s%2 else 4; favourable=3 if faces==6 else 1;trial=24+(s%7)*6;hits=max(1,min(trial-1,trial*favourable//faces+(s%5)-2));theory=Fraction(favourable,faces);relative=Fraction(hits,trial)
  v={'lesson':n,'model':'frequency','trials':trial,'hits':hits,'faces':faces,'favourable':favourable,'event':'even on a fair die' if faces==6 else 'heads in a sequence of four equally likely coin-toss outcomes'}
  # Four equiprobable outcomes correspond to two tosses, one HH outcome.
  if faces==4:v['event']='two heads in two fair coin tosses'
  question=f'A learner records {hits} occurrences of {v["event"]} in {trial} independent trials. The theoretical model has {favourable} favourable outcomes out of {faces}. Find the observed relative frequency and compare it with the theoretical probability.'
  relation='higher than' if relative>theory else 'lower than' if relative<theory else 'equal to'
  answer=f'relative frequency {relative}; theoretical probability {theory}; observed is {relation} theoretical'
  steps=[f'Write the observed count {hits} and number of trials {trial} as separate quantities.',f'Divide the observed count by trials: relative frequency={hits}/{trial}={relative}.',
         f'From {faces} equally likely outcomes, {favourable} satisfy the event; theoretical probability={favourable}/{faces}={theory}.',
         f'Compare {relative} and {theory}: the observed relative frequency is {relation} the theoretical value. A finite experiment may differ from theory.',f'Answer: {answer}. Observed frequency uses the experimental denominator {trial}.']
  wrong=[f'relative frequency {Fraction(trial,hits)}; theoretical probability {theory}',f'relative frequency {theory}; theoretical probability {relative}',f'relative frequency {Fraction(hits,faces)}; theoretical probability {theory}']
 elif n==2:
  task=('A only','B only','both A and B','neither A nor B')[(s-1)%4]
  answer=str({'A only':ao,'B only':bo,'both A and B':both,'neither A nor B':neither}[task])
  question=f'In a class of {N}, {A} choose activity A, {B} choose B and {both} choose both. How many choose {task}?'
  steps=[f'Draw the universal set with two overlapping circles A and B for {N} learners.',f'Put {both} into the overlap first.',f'Subtract the overlap: A-only={A}−{both}={ao}, B-only={B}−{both}={bo}.',
         f'Outside both={N}−({ao}+{both}+{bo})={neither}; check all four regions total {N}.',f'Answer: {task} = {answer}. Every learner is counted exactly once.']
  wrong=[str(A),str(B),str(union),str(neither+1),str(ao+1)]
 elif n==3:
  task=('A or B','A and B','not A or B')[(s-1)%3]
  # The third task is explicitly the complement of A-or-B to avoid ambiguous negation.
  if task=='not A or B':task='neither A nor B'
  value=union if task=='A or B' else both if task=='A and B' else neither
  answer=str(Fraction(value,N))
  question=f'A sample space has {N} outcomes: A-only {ao}, B-only {bo}, both {both}, neither {neither}. Find P({task}).'
  steps=[f'Mark the four disjoint regions A-only={ao}, overlap={both}, B-only={bo}, outside={neither}.',f'Calculate |A|={A} and |B|={B}; use the common denominator |S|={N}.',
         f'|A∪B|={A}+{B}−{both}={union}; the overlap was counted twice in |A|+|B|.',
         f'The requested favourable count for {task} is {value}; divide by {N}.',f'Answer: P({task}) = {answer}. All four disjoint regions add to {N}.']
  wrong=[str(Fraction(A+B,N)),str(Fraction(A,N)),str(Fraction(B,N)),str(Fraction(N-value,N))]
 elif n==4:
  complementary=neither==0
  task='Are A and B complementary?' if complementary else 'Are A and B mutually exclusive but not complementary?'
  answer='Yes; disjoint and exhaustive' if complementary else 'Yes; disjoint but not exhaustive'
  question=f'Events A and B have A-only={ao}, B-only={bo}, intersection={both}, outside both={neither}, in S of size {N}. {task}'
  steps=[f'Place {ao} in A-only and {bo} in B-only; draw the full universe S={N}.',f'The intersection has {both} outcomes, so A and B are mutually exclusive.',
         f'The union has {union} outcomes. Compare it with S={N}; the outside region contains {neither}.',
         'A and B are complementary because they are disjoint and exhaust S.' if complementary else 'They are not complementary: the outside region is nonempty.',
         f'Answer: {answer}. Check both disjointness and the entire sample space.']
  wrong=['Yes; disjoint but not exhaustive' if complementary else 'Yes; disjoint and exhaustive','No; the overlap is nonzero','No; every event has probability zero']
 else:
  # Deliberately incorrect addition rule, with a nonzero overlap.
  both=max(1,both);N=ao+bo+both+neither;A=ao+both;B=bo+both;union=ao+bo+both
  v.update(both=both,total=N,a=A,b=B,union=union)
  wrong_claim=Fraction(A+B,N);correct=Fraction(union,N)
  question=f'In S of {N} outcomes, |A|={A}, |B|={B} and |A∩B|={both}. A learner claims P(A or B)={wrong_claim} by adding P(A)+P(B). Find the first error and correct probability.'
  answer=f'Overlap counted twice; P(A or B)={correct}'
  steps=[f'Draw the two events and put the shared {both} outcomes in their overlap.',f'Calculate the claimed numerator |A|+|B|={A+B}; it includes the overlap twice.',
         f'Correct the first error by subtracting |A∩B|={both} once.',f'|A∪B|={A}+{B}−{both}={union}; divide by |S|={N}.',
         f'Answer: {answer}. The union count cannot exceed the sample space.']
  wrong=[f'Overlap counted twice; P(A or B)={wrong_claim}',f'Events are complementary; P(A or B)=1',f'No error; P(A or B)={wrong_claim}']
 wrong=list(dict.fromkeys(str(x) for x in wrong if str(x)!=answer))
 for filler in ('Cannot determine','0','1','All outcomes are impossible'):
  if filler not in wrong and filler!=answer:wrong.append(filler)
 assert len(steps)==5 and len({answer,*wrong[:3]})==4,(n,i,answer,wrong)
 v['answer']=answer
 return {'id':f'g10-prob-l{n:02}-w{i:02}','problem':question,'actions':steps,'answer':answer,'check':steps[-1],
   'visual':{'family':'grade10_probability','values':v},'lesson':n,'wrong':wrong[:3],
   'misconception':'The overlap is counted once in a union; complement requires both disjointness and exhaustive coverage.',
   'difficulty':'foundation' if i<=2 else 'easy' if i<=5 else 'standard' if i<=9 else 'intermediate' if i<=12 else 'exam'}

def option(n,i,variant,prefix):
 q=case(n,i,variant);opts=[q['answer'],*q['wrong']];position=i%4
 opts=opts[-position:]+opts[:-position] if position else opts
 return {'id':f'g10-prob-l{n:02}-{prefix}{i:02}','prompt':q['problem'],'options':opts,'answer_index':position,
   'memo':' '.join(q['actions']),'source':f'grade10-prob-lesson-{n:02}.md'}

def build():
 DOC.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True);manifest=[]
 for n,title in TITLES.items():
  worked=[{k:v for k,v in case(n,i).items() if k!='wrong'} for i in range(1,16)]
  data={'source':f'grade10-prob-lesson-{n:02}.md','worked':worked,'practice':[option(n,i,1,'p') for i in range(1,16)],
    'mastery':[option(n,i+15,2,'m') for i in range(1,6)],'reassessment':[option(n,i+20,3,'r') for i in range(1,4)]}
  assert len({x['problem'] for x in worked})>=10,n
  lines=[f'# Grade 10 Topic 8 · Lesson {n}: {title}',f'Authority: [DBE Grade 10 ATP]({ATP}), Term 3 Probability. Original Athena examples.',
         'Status: teacher and browser review required. Sample-space counts and Venn regions must match the current question.']
  for q in worked:lines += [f'## {q["id"]}: {q["problem"]}',f'Visual contract: {json.dumps(q["visual"],ensure_ascii=False)}',
    *[f'{j}. {a}' for j,a in enumerate(q['actions'],1)],f'**Answer:** {q["answer"]}. **Misconception:** {q["misconception"]}']
  for label,key in [('Practice','practice'),('Mastery','mastery'),('Parallel reassessment','reassessment')]:
   lines.append(f'## {label} answer key')
   for q in data[key]:lines.append(f'- {q["id"]}: {q["prompt"]} Options: {" | ".join(q["options"])}. Correct: {q["options"][q["answer_index"]]}. {q["memo"]}')
  source=DOC/data['source'];source.write_text('\n\n'.join(lines)+'\n',encoding='utf-8')
  (OUT/f'probability_{n:02}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  manifest.append({'lesson_id':f'g10-prob-{n:02}','source':source.name,'source_sha256':sha256(source.read_bytes()).hexdigest(),
    'worked':15,'practice':15,'mastery':5,'reassessment':3,'status':'teacher_review_required','teacher_approved':False,'browser_accepted':False})
 (DOC/'topic08-acceptance-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
 (DOC/'topic08-batch-acceptance.md').write_text(f'# Grade 10 Topic 8: Probability\n\n[DBE Grade 10 ATP]({ATP}) Term 3 covers relative versus theoretical frequency, Venn diagrams, the two-event union rule, exclusive and complementary events. Five authored lessons include 75 worked, 75 four-choice practice, 25 mastery and 15 reassessment questions. Teacher and browser acceptance pending.\n',encoding='utf-8')
if __name__=='__main__':build()
