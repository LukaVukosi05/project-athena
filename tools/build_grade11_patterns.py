"""Original Grade 11 quadratic pattern examples and private MCQ banks."""
import json
from hashlib import sha256
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/curriculum/grade11/quadratic-number-patterns'
OUT=ROOT/'backend/app/curriculum/grade11/generated'
ATP='https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2023%20ATPs/FET%20Content%20Subjects/Grade%2011/1.590%20ATP%202023-24%20Gr%2011%20Maths%20final.pdf'
CAPS='https://www.education.gov.za/Portals/0/CD/National%20Curriculum%20Statements%20and%20Vocational/CAPS%20FET%20_%20MATHEMATICS%20_%20GR%2010-12%20_%20Web_1133.pdf'
TITLES={1:'Recognise a constant second difference',2:'Find the quadratic general term',3:'Find a term position from its value',4:'Quadratic figural patterns',5:'Integrated patterns and first-error diagnosis'}
DIFFICULTY=['foundation']*2+['easy']*3+['standard']*4+['intermediate']*3+['exam']*3

def poly(a,b,c,n):return a*n*n+b*n+c

def formula(a,b,c):
 def coeff(k,x,first=False):
  if not k:return ''
  sign='− ' if k<0 else '' if first else '+ '
  return f'{sign}{abs(k) if abs(k)!=1 else ""}{x}'
 return ' '.join(filter(None,[coeff(a,'n²',True),coeff(b,'n'),('− ' if c<0 else '+ ')+str(abs(c)) if c else ''])).strip()

def case(lesson,index,variant=0):
 t=index+15*variant
 a=(1+t%3)*(-1 if lesson in (1,2,5) and t%5==0 else 1)
 b=(-4+t%9) if lesson in (1,2,5) else 1+t%6
 c=12+t%11
 mode=('difference','rule','position','figural','diagnosis')[lesson-1]
 if mode=='figural':
  q=1+t%3;extra=t%3;a,b,c=1,q,extra
 terms=[poly(a,b,c,n) for n in range(1,6)]
 first=[terms[j+1]-terms[j] for j in range(4)]
 second=[first[j+1]-first[j] for j in range(3)]
 assert second==[2*a]*3
 seq=', '.join(map(str,terms))
 target=7+t%11
 actual=poly(a,b,c,target)
 rule=formula(a,b,c)
 if mode=='difference':
  answer=f'Quadratic; T₆ = {poly(a,b,c,6)}'
  prompt=f'Consider the sequence {seq}, … . Determine whether it is quadratic using differences, then find T₆.'
  steps=[f'Write T₁ to T₅: {seq}. Keep each term in its given position.',
         f'Subtract adjacent terms: first differences are {", ".join(map(str,first))}. They are not constant.',
         f'Subtract adjacent first differences: {", ".join(map(str,second))}. This is constant, so the pattern is quadratic.',
         f'Continue the first differences: {first[-1]} + {second[0]} = {first[-1]+second[0]}; then T₆ = {terms[-1]} + {first[-1]+second[0]} = {poly(a,b,c,6)}.',
         f'Answer: {answer}. Check the final first difference is {poly(a,b,c,6)-terms[-1]}, and every second difference is {2*a}.']
  wrong=[f'Quadratic; T₆ = {poly(a,b,c,6)+d}' for d in (first[-1],-2*a,2*a)]
 elif mode=='rule':
  answer=f'Tₙ = {rule}'
  prompt=f'Find the general term Tₙ = an² + bn + c for the sequence {seq}, … . Verify it at n = 4.'
  steps=[f'Write the five given terms in their positions: {seq}.',
         f'First differences: {", ".join(map(str,first))}; second differences: {", ".join(map(str,second))}.',
         f'For a quadratic rule, constant second difference = 2a. Thus 2a = {2*a}, so a = {a}.',
         f'T₂ − T₁ = 3a + b = {first[0]}; b = {first[0]} − 3({a}) = {b}. T₁ = a + b + c = {terms[0]}, so c = {terms[0]} − ({a}) − ({b}) = {c}.',
         f'Answer: {answer}. Check T₄ = {a}(4²) + ({b})(4) + ({c}) = {poly(a,b,c,4)}, matching the fourth given term.']
  wrong=[f'Tₙ = {formula(a+d,b,c)}' for d in (1,-1)] + [f'Tₙ = {formula(a,b+1,c)}']
 elif mode=='position':
  answer=f'n = {target}'
  prompt=f'The quadratic sequence begins {seq}, … . At which positive integer position does the value {actual} occur? Show that your position is valid.'
  steps=[f'Write T₁ to T₅: {seq}. Their first differences are {", ".join(map(str,first))}.',
         f'Second differences are {", ".join(map(str,second))}, so a = {second[0]}/2 = {a}.',
         f'Use T₂ − T₁ = 3a + b = {first[0]} to obtain b = {b}; then T₁ = a + b + c = {terms[0]} gives c = {c}. Thus Tₙ = {rule}.',
         f'Rearrange {a}n² + ({b})n + ({c}) = {actual}: (n − {target})({a}n + {b+a*target}) = 0. Thus n = {target} or n = −{b+a*target}/{a}; reject the negative position.',
         f'Answer: {answer}. For n ≥ 1, consecutive increments are positive; T₍{target-1}₎ = {poly(a,b,c,target-1)} < {actual}, so this is the only positive position.']
  wrong=[f'n = {target+d}' for d in (-2,-1,1)]
 elif mode=='figural':
  answer=f'T{target} = {actual} tiles'
  prompt=f'Figure n is an n-row rectangle with n + {b} tiles per row, plus {c} separate fixed tiles. Figures 1, 2 and 3 have {terms[0]}, {terms[1]} and {terms[2]} tiles. How many tiles are in Figure {target}?'
  steps=[f'Draw Figures 1–3: use n rows and n + {b} columns, then add the same {c} fixed tiles each time.',
         f'Count Figure 1 = {terms[0]}, Figure 2 = {terms[1]}, Figure 3 = {terms[2]}; extending gives {seq}.',
         f'The rectangle has n(n + {b}) tiles; with the fixed {c}, the rule is Tₙ = n² + {b}n + {c}. Its constant second difference is 2.',
         f'For Figure {target}, multiply {target} rows by {target+b} columns, then add {c}: {target}({target+b}) + {c} = {actual}.',
         f'Answer: {answer}. Check Figure 3 by the same construction: 3({3+b}) + {c} = {terms[2]}.']
  wrong=[f'T{target} = {actual+d} tiles' for d in (-b,-(b+c+3),target)]
 else:
  answer=f'T{target} = {actual}'
  naive=terms[0]+(target-1)*first[0]
  prompt=f'A learner sees {seq}, … and assumes the first difference stays at {first[0]}, predicting T{target} = {naive}. Locate the first error and calculate the correct T{target}.'
  steps=[f'Write adjacent differences from {seq}: {", ".join(map(str,first))}.',
         f'The first error is keeping {first[0]} constant: the first differences change by {second[0]} each time.',
         f'The second differences are {", ".join(map(str,second))}, so a = {a}. Using T₂ − T₁ = {first[0]} gives b = {b}, and T₁ = {terms[0]} gives c = {c}.',
         f'Use the corrected rule Tₙ = {rule}: T{target} = {a}({target}²) + ({b})({target}) + ({c}) = {actual}.',
         f'Answer: {answer}. The learner’s {naive} used a linear rule; check the corrected rule reproduces T₁ = {terms[0]} and T₅ = {terms[4]}.']
  wrong=[f'T{target} = {value}' for value in (naive,actual+2*a,actual-first[-1])]
 assert len(set([answer,*wrong]))==4,(lesson,index,answer,wrong)
 return dict(id=f'g11-pat-l{lesson:02}-w{index:02}',lesson=lesson,problem=prompt,answer=answer,actions=steps,
  check=steps[-1],visual=dict(family='grade11_patterns',values=dict(mode=mode,terms=terms,target=target,rows=3,columns_offset=b,extra=c) if mode=='figural' else dict(mode=mode,terms=terms,target=target)),
  difficulty=DIFFICULTY[index-1],wrong=wrong)

def build():
 DOC.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True);manifest=[]
 for n,title in TITLES.items():
  worked=[{k:v for k,v in case(n,i).items() if k!='wrong'} for i in range(1,16)]
  assert len({q['problem'] for q in worked})==15
  data=dict(source=f'grade11-pat-lesson-{n:02}.md',worked=worked)
  for section,count,variant,prefix in [('practice',15,1,'p'),('mastery',5,2,'m'),('reassessment',3,3,'r')]:
   bank=[]
   for i in range(1,count+1):
    q=case(n,i,variant);opts=[q['answer'],*q['wrong']];offset=(i+variant)%4;opts=opts[offset:]+opts[:offset]
    bank.append(dict(id=f'g11-pat-l{n:02}-{prefix}{i:02}',prompt=q['problem'],options=opts,
       answer_index=opts.index(q['answer']),actions=q['actions'],memo=' '.join(q['actions'])))
   data[section]=bank
  lines=[f'# Grade 11 Topic 11, Lesson {n}: {title}',f'[DBE ATP]({ATP}) and [Mathematics CAPS]({CAPS}).',
   'Original Athena questions. Teacher and live browser review required. Term positions begin at n = 1.']
  for q in worked:lines.extend([f'## {q["id"]}: {q["problem"]}',f'Visual givens: `{json.dumps(q["visual"],ensure_ascii=False)}`',
    *[f'{j}. {s}' for j,s in enumerate(q['actions'],1)],f'Answer: {q["answer"]}. Check: {q["check"]}'])
  for section in ('practice','mastery','reassessment'):
   lines.append(f'## {section.title()} key')
   for q in data[section]:lines.append(f'- {q["id"]}: {q["prompt"]} Options: {" | ".join(q["options"])}. Correct: {q["options"][q["answer_index"]]}. {q["memo"]}')
  source=DOC/data['source'];source.write_text('\n\n'.join(lines)+'\n',encoding='utf-8')
  (OUT/f'patterns_{n:02}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  manifest.append(dict(lesson_id=f'g11-pat-{n:02}',source=source.name,source_sha256=sha256(source.read_bytes()).hexdigest(),worked=15,practice=15,mastery=5,reassessment=3,status='teacher_review_required',teacher_approved=False,browser_accepted=False))
 (DOC/'topic11-acceptance-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':build()
