"""Compile original, deterministic Grade 9 pattern questions into reviewed source packs."""
from pathlib import Path
from hashlib import sha256
import json

ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/curriculum/grade9/numeric-geometric-patterns'
OUT=ROOT/'backend/app/curriculum/grade9/generated'
ATP='https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2026%20ATPs/2026_ATP_Mathematics_Grade%209.pdf'
TITLES={1:'Visual and numeric patterns',2:'Tables and position rules',3:'Changing differences and ratios',4:'General rules and unknown terms',5:'Justifying and diagnosing pattern rules'}

def term(kind,a,b,n):
    return {'linear':lambda:a*n+b,'geometric':lambda:a*b**(n-1),'square':lambda:a*n*n+b,
            'stair':lambda:a*n*(n+1)//2+b,'border':lambda:a*(2*n+1)+b}[kind]()

def rule(kind,a,b):
    return {'linear':f'{a}n {"+" if b>=0 else "−"} {abs(b)}',
            'geometric':f'{a} × {b}^(n−1)',
            'square':f'{a}n² {"+" if b>=0 else "−"} {abs(b)}',
            'stair':f'{a}n(n+1)/2 {"+" if b>=0 else "−"} {abs(b)}',
            'border':f'{a}(2n+1) {"+" if b>=0 else "−"} {abs(b)}'}[kind]

def row(values):return ', '.join(map(str,values))

def build_case(lesson,kind,a,b,target,mode='next',shape=None):
    known=[term(kind,a,b,n) for n in range(1,5 if lesson!=1 or not shape else 4)]
    result=term(kind,a,b,target);expression=rule(kind,a,b)
    diffs=[y-x for x,y in zip(known,known[1:])]
    if mode=='rule':
        answer=expression
        wrong=[rule(kind,a,b+1),rule(kind,a+1,b),rule(kind,a,b-a)]
        assert len({answer,*wrong})==4
    else:
        answer=str(result)
        wrong=[str(result+1),str(result+a*(target-1) if kind!='geometric' else result*b),str(result-a if a else result-2)]
        if len({answer,*wrong})<4:wrong=[str(result+1),str(result+2),str(result+3)]
    if mode=='diagnose':
        advanced=target>=9
        claim=f'{known[0]} + {known[1]-known[0]}(n−1)' if advanced else rule(kind,a,b+1)
        prompt=f'A learner claims the rule for positions 1–4 with terms {row(known)} is {claim}. Test the first incorrect value and give the correct general rule.'
        answer=expression;wrong=[claim,rule(kind,a+1,b),rule(kind,a,b-a)]
        first=3 if advanced else 2 if kind=='geometric' else 1
        claimed=known[0]+(known[1]-known[0])*(first-1) if advanced else term(kind,a,b+1,first)
        actions=[f'Test the claim at position {first}: it gives {claimed}, but the table gives {known[first-1]}.',
                 f'Inspect differences {row(diffs)} and the figure or table values; the claimed rule fails at position {first}.',
                 f'The corrected general rule is {expression}.',
                 f'Check: at position 2 the rule gives {known[1]}, matching the given second term.']
    elif mode=='rule':
        prompt=f'For positions 1–4 the terms are {row(known)}. Give an algebraic rule for term n.'
        actions=[f'Keep positions 1, 2, 3 and 4 aligned with terms {row(known)}.',
                 f'The successive changes are {row(diffs)}; compare their pattern with the term positions.',
                 f'A rule consistent with all given terms is {expression}.',
                 f'Check: position 4 gives {known[-1]}, as in the original pattern.']
    elif shape:
        prompt=f'Figures 1, 2 and 3 use {row(known)} square tiles respectively. The figures grow as {shape} shapes. How many tiles are in figure {target}?'
        actions=[f'Count the given figures at positions 1, 2 and 3: {row(known)} tiles.',
                 f'Compare how each {shape} grows; the general count is {expression}.',
                 f'At position {target}, substitute n={target} to obtain {result} tiles.',
                 f'Check: the rule gives {known[1]} tiles for figure 2, matching the original figure.']
    elif lesson==2:
        prompt=f'The table has positions 1, 2, 3, 4 and outputs {row(known)}. Find the output at position {target}.'
        actions=[f'Link each position to its output: 1→{known[0]}, 2→{known[1]}, 3→{known[2]}, 4→{known[3]}.',
                 f'The rule is {expression}; verify it against the given positions.',
                 f'At n={target}, the output is {result}.',
                 f'Check: at n=2 the rule gives {known[1]}, as in the original table.']
    else:
        prompt=f'The pattern begins {row(known)}. Find term {target}, showing the rule you used.'
        actions=[f'Label the given terms by positions 1 to {len(known)}: {row(known)}.',
                 f'First differences are {row(diffs)}; use the pattern of differences or ratios to identify {expression}.',
                 f'Substitute n={target}: term {target} is {result}.',
                 f'Check: the rule gives {known[1]} at position 2, matching the given pattern.']
    assert len({answer,*wrong})==4,(lesson,prompt,answer,wrong)
    return dict(problem=prompt,givens=list(map(str,known)),actions=actions,answer=answer,wrongs=wrong,
        wrong_methods=['Counts one extra tile or term.','Extends a constant difference where the pattern changes.','Uses the wrong position or rule parameter.'],
        misconception='first-error-rule' if mode=='diagnose' else 'pattern-relation',check=actions[-1],
        visual=dict(family='tiles' if shape else 'diagnosis' if mode=='diagnose' else 'rule' if mode=='rule' else 'table' if lesson==2 else 'differences',
                    kind=kind,shape=shape,known=known,positions=list(range(1,len(known)+1)),differences=diffs,
                    a=a,b=b,rule=expression,target=target,target_value=result,claim=claim if mode=='diagnose' else None))

def specs(lesson):
    if lesson==1:
        return [(kind,a,b,(9+i%3) if i>=12 else 4 if shape else 5,'next',shape) for i,(kind,a,b,shape) in enumerate([
            ('linear',3,2,None),('linear',5,-1,None),('geometric',2,2,None),('geometric',3,3,None),('square',1,0,'square'),
            ('stair',1,0,'staircase'),('border',1,0,'L'),('linear',7,3,None),('geometric',4,2,None),('square',2,1,'square'),
            ('stair',2,1,'staircase'),('border',2,1,'L'),('linear',4,6,None),('square',3,2,'square'),('stair',3,1,'staircase')])]
    if lesson==2:return [('linear',a,b,16+i%3 if i>=12 else 6+(i%4),'next',None) for i,(a,b) in enumerate([(3,2),(5,1),(2,-3),(7,-2),(4,5),(-2,20),(6,0),(8,-7),(3,9),(9,-3),(-3,25),(11,4),(5,-6),(12,-11),(7,8)])]
    if lesson==3:return [(kind,a,b,10+i%3 if i>=12 else 6+i%3,'next',None) for i,(kind,a,b) in enumerate([
        ('square',1,0),('square',2,1),('stair',1,0),('square',3,2),('stair',2,1),('geometric',2,2),
        ('square',1,4),('stair',3,0),('square',2,-1),('geometric',3,3),('square',4,1),('stair',1,5),
        ('square',3,-2),('geometric',5,2),('stair',2,4)])]
    if lesson==4:return [(kind,a,b,15+i%3 if i>=12 else 7+i%3,'rule' if i<9 else 'next',None) for i,(kind,a,b) in enumerate([
        ('linear',3,2),('linear',4,-1),('square',1,0),('stair',1,0),('geometric',2,3),('square',2,1),
        ('border',1,0),('stair',2,2),('linear',7,-3),('square',3,1),('geometric',3,2),('linear',5,4),
        ('stair',3,1),('border',2,0),('square',1,7)])]
    return [(kind,a,b,9 if i>=12 else 5,'diagnose',None) for i,(kind,a,b) in enumerate([
        ('linear',3,2),('square',1,0),('stair',1,0),('geometric',2,2),('border',1,0),
        ('linear',5,-2),('square',2,1),('stair',2,1),('geometric',3,3),('border',2,1),
        ('linear',7,4),('border',3,0),('stair',3,1),('geometric',4,2),('square',3,2)])]

def private(case,n,kind,index):
    choices=case['wrongs'][:];key=(index-1)%4;choices.insert(key,case['answer'])
    return dict(id=f'g9-pat-l{n:02}-{kind}{index:02}',prompt=case['problem'],options=choices,answer_index=key,
        memo=' '.join(case['actions']),misconception=case['misconception'],
        option_rationales={v:('Correct: '+case['check'] if v==case['answer'] else 'Incorrect: '+case['wrong_methods'][case['wrongs'].index(v)]) for v in choices})

def build(n):
    worked=[build_case(n,*x) for x in specs(n)];assert len(worked)==15
    other=[];used={c['problem'] for c in worked};seed=1
    while len(other)<23:
        for i,kind in enumerate(('linear','square','stair','geometric','border')):
            a=2+seed+i;b=2*seed+i
            mode='diagnose' if n==5 else 'rule' if n==4 and i%2 else 'next'
            candidate=build_case(n,kind,a,b,6+seed%3,mode)
            if candidate['problem'] not in used:other.append(candidate);used.add(candidate['problem'])
            if len(other)==23:break
        seed+=1;assert seed<30
    filename=f'lesson-{n:02}-'+TITLES[n].lower().replace(' ','-')+'.md'
    data=dict(source=filename,worked=[{**c,'id':f'g9-pat-l{n:02}-w{i:02}',
        'difficulty':'foundation' if i<=2 else 'easy' if i<=5 else 'standard' if i<=9 else 'exam' if i<=12 else 'advanced'} for i,c in enumerate(worked,1)],
        practice=[private(c,n,'p',i) for i,c in enumerate(other[:15],1)],
        mastery=[private(c,n,'m',i) for i,c in enumerate(other[15:20],1)],
        reassessment=[private(c,n,'r',i) for i,c in enumerate(other[20:],1)])
    lines=[f'# Grade 9 Topic 4 · Lesson {n}: {TITLES[n]}','',
        'Status: teacher and browser review required. Original Athena questions; not published.',
        'Scope: DBE 2026 Mathematics Grade 9 ATP, Term 1, Numeric and Geometric Patterns.',ATP,'',
        'Whiteboard: original figures and numbers remain visible; reveal one relationship and one operation at a time.',
        'Earlier results accumulate beside the visual; final result precedes an independent check.','', '## Worked examples']
    for c in data['worked']:
        lines+=['',f"### {c['id']} · {c['difficulty']}",f"Question: {c['problem']}",
          f"Givens: {'; '.join(c['givens'])}",f"Visual: {json.dumps(c['visual'],ensure_ascii=False)}",
          *[f'{i}. {action}' for i,action in enumerate(c['actions'],1)],
          f"Answer: {c['answer']}",f"Misconception: {c['misconception']}"]
    for kind in ('practice','mastery','reassessment'):
        lines+=['',f'## {kind.title()} · private keys and rationales']
        for c in data[kind]:
            lines+=['',f"### {c['id']}",f"Question: {c['prompt']}",
                *[f'{chr(65+i)}. {option}' for i,option in enumerate(c['options'])],
                f"Key: {chr(65+c['answer_index'])}",f"Memo: {c['memo']}",
                *[f'Distractor {v}: {reason}' for v,reason in c['option_rationales'].items() if reason.startswith('Incorrect:')]]
    DOC.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    (DOC/filename).write_text('\n'.join(lines)+'\n',encoding='utf-8')
    (OUT/f'patterns_{n:02}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return dict(lesson_id=f'g9-patterns-{n:02}',source=filename,
        source_sha256=sha256((DOC/filename).read_bytes()).hexdigest(),
        **{f'{kind}_ids':[c['id'] for c in data[kind]] for kind in ('worked','practice','mastery','reassessment')},
        **{f'{kind}_count':len(data[kind]) for kind in ('worked','practice','mastery','reassessment')},
        status='teacher_review_required',browser_accepted=False,teacher_approved=False)

if __name__=='__main__':
    rows=[build(n) for n in range(1,6)]
    (DOC/'topic4-acceptance-manifest.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Authored',len(rows),'lessons; worked',sum(x['worked_count'] for x in rows),'practice',sum(x['practice_count'] for x in rows))
