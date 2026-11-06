"""Compile original Grade 9 Functions and Relationships source questions."""
from pathlib import Path
from hashlib import sha256
import json

ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/curriculum/grade9/functions-relationships'
OUT=ROOT/'backend/app/curriculum/grade9/generated'
ATP='https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2026%20ATPs/2026_ATP_Mathematics_Grade%209.pdf'
TITLES={1:'Flow diagrams and output values',2:'Input-output tables and inverse lookup',
        3:'Formulae and equations',4:'Equivalent words, tables, formulae and graphs',
        5:'Mixed representations and first-error repair'}

def output(a,b,x,kind):return x*x+b if kind=='square' else a*x+b

def rule(a,b,kind):
    return f'y = x² {"+" if b>=0 else "−"} {abs(b)}' if kind=='square' else f'y = {a}x {"+" if b>=0 else "−"} {abs(b)}'

def words(a,b,kind):
    return f'square the input, then {"add" if b>=0 else "subtract"} {abs(b)}' if kind=='square' else f'multiply the input by {a}, then {"add" if b>=0 else "subtract"} {abs(b)}'

def case(lesson,a,b,target,kind='linear',advanced=False):
    known_x=[-1,0,1,2] if lesson==4 else [0,1,2,3]
    pairs=[[x,output(a,b,x,kind)] for x in known_x]
    calculated=output(a,b,target,kind)
    expression=rule(a,b,kind);procedure=words(a,b,kind)
    if lesson==1:
        prompt=f'A flow diagram says: {procedure}. What output follows input {target}?'
        answer=str(calculated);wrong=[str(calculated+a),str(calculated-a),str(target+b)]
        actions=[f'Place input {target} into the first box. The given rule says to {procedure}.',
                 f'{"Square" if kind=="square" else "Multiply"} the input: {target*target if kind=="square" else a*target}.',
                 f'Apply the final adjustment to obtain output {calculated}.',
                 f'Check: input {known_x[2]} follows the same boxes and gives {pairs[2][1]}, as expected.']
        family='flow'
    elif lesson==2:
        prompt=f'The table gives input-output pairs {pairs}. Which input gives output {calculated}?'
        answer=str(target);wrong=[str(target+1),str(target-1),str(target+2)]
        actions=[f'Read the table as input→output pairs; the target output is {calculated}.',
                 f'Use the rule {expression} and work backwards, checking possible inputs.',
                 f'Input {target} gives {calculated}; therefore the missing input is {target}.',
                 f'Check: input {known_x[1]} gives {pairs[1][1]}, matching the given table.']
        family='table'
    elif lesson==3:
        prompt=f'The formula is {expression}. Calculate y when x = {target}.'
        answer=str(calculated);wrong=[str(calculated+a),str(calculated-a),str(target+b)]
        actions=[f'Retain the given formula {expression} and substitute x = {target}.',
                 f'Calculate the product or square first: {target*target if kind=="square" else a*target}.',
                 f'Then apply {b:+d} to obtain y = {calculated}.',
                 f'Check: x={known_x[2]} in the original formula gives {pairs[2][1]}.']
        family='formula'
    elif lesson==4:
        prompt=(f'The table contains the points {pairs}. A graph plots these same points. '
                +('A learner uses the first point to choose an equation. Find a rule that also passes through the remaining three points, and justify it.'
                  if advanced else 'Which equation represents both?'))
        answer=expression;wrong=[rule(a,b+1,kind),rule(a+1,b,kind),rule(a,b-a,kind)]
        actions=[f'Align each input-output pair; the point (0, {b}) is on the graph.',
                 f'Plot the known points and compare their vertical changes; the multiplier is {a}.',
                 f'The words, table and plotted line agree with {expression}.',
                 f'Check: the equation gives {pairs[-1][1]} for x={known_x[-1]}, matching the last point.']
        family='graph'
    else:
        claim=rule(a,b+1,kind) if not advanced else rule(a+1,b,kind)
        first=0 if not advanced else 1
        claimed=output(a,b+1,first,kind) if not advanced else output(a+1,b,first,kind)
        prompt=f'A learner claims the pairs {pairs} follow {claim}. Find the first wrong output and repair the rule.'
        answer=expression;wrong=[claim,rule(a,b+2,kind),rule(a+2,b,kind)]
        actions=[f'Compare the claim with the given pair at x={first}: it predicts {claimed}, but the table says {output(a,b,first,kind)}.',
                 f'The first incorrect output is at x={first}; test the original multiplier and adjustment against another pair.',
                 f'The corrected equation is {expression}.',
                 f'Check: x={known_x[-1]} gives y={pairs[-1][1]} as in the original table.']
        family='diagnosis'
    if len({answer,*wrong})<4:
        if answer.lstrip('-').isdigit():wrong=[str(int(answer)+1),str(int(answer)+2),str(int(answer)+3)]
        else:wrong=[rule(a,b+1,kind),rule(a+1,b,kind),rule(a,b-1,kind)]
    assert len({answer,*wrong})==4,(lesson,prompt,answer,wrong)
    visual=dict(family=family,kind=kind,a=a,b=b,rule=expression,words=procedure,known_pairs=pairs,
                target_input=target,target_output=calculated,claim=claim if lesson==5 else None,
                first_error_input=first if lesson==5 else None)
    return dict(problem=prompt,givens=[str(p) for p in pairs] if lesson!=1 else [str(target),procedure],
        actions=actions,answer=answer,wrongs=wrong,
        wrong_methods=['Uses an incorrect adjustment or intercept.','Uses an incorrect multiplier or slope.','Substitutes the wrong input value.'],
        visual=visual,misconception='first-output-error' if lesson==5 else 'input-output-rule',check=actions[-1])

def specs(n):
    seeds=[(2,3,4),(3,1,5),(4,-2,4),(5,2,6),(2,-4,7),(3,5,8),(6,1,6),(4,4,7),
           (7,-3,8),(5,-5,9),(8,2,7),(3,-2,9),(6,4,11),(9,-1,12),(7,3,13)]
    return [(a,b,target,'square' if n in (1,2,3) and i in (4,8,12) else 'linear',i>=12) for i,(a,b,target) in enumerate(seeds)]

def other_cases(n):
    used={case(n,*spec)['problem'] for spec in specs(n)};items=[];seed=1
    while len(items)<23:
        for i in range(5):
            a=2+seed+5*i;b=2*seed-i-4;target=5+seed+(i%3)
            c=case(n,a,b,target,'square' if n<=3 and i==4 else 'linear',seed>=4)
            if c['problem'] not in used:items.append(c);used.add(c['problem'])
            if len(items)==23:break
        seed+=1;assert seed<20
    return items

def private(c,n,kind,index):
    options=c['wrongs'][:];key=(index-1)%4;options.insert(key,c['answer'])
    return dict(id=f'g9-fn-l{n:02}-{kind}{index:02}',prompt=c['problem'],options=options,answer_index=key,
        memo=' '.join(c['actions']),misconception=c['misconception'],
        option_rationales={v:('Correct: '+c['check'] if v==c['answer'] else 'Incorrect: '+c['wrong_methods'][c['wrongs'].index(v)]) for v in options})

def build(n):
    worked=[case(n,*spec) for spec in specs(n)];assert len(worked)==15
    others=other_cases(n)
    filename=f'lesson-{n:02}-'+TITLES[n].lower().replace(',','').replace(' ','-')+'.md'
    data=dict(source=filename,worked=[{**c,'id':f'g9-fn-l{n:02}-w{i:02}',
        'difficulty':'foundation' if i<=2 else 'easy' if i<=5 else 'standard' if i<=9 else 'exam' if i<=12 else 'advanced'} for i,c in enumerate(worked,1)],
        practice=[private(c,n,'p',i) for i,c in enumerate(others[:15],1)],
        mastery=[private(c,n,'m',i) for i,c in enumerate(others[15:20],1)],
        reassessment=[private(c,n,'r',i) for i,c in enumerate(others[20:],1)])
    lines=[f'# Grade 9 Topic 5 · Lesson {n}: {TITLES[n]}','',
      'Status: authored preview awaiting browser and teacher sign-off; original Athena questions.',
      'Scope: DBE 2026 Mathematics Grade 9 ATP, Term 1, Functions and Relationships.',ATP,'',
      'Whiteboard: preserve givens and prior worked steps. Link the same input-output pair in the flow, table, formula and graph.','',
      '## Worked examples']
    for c in data['worked']:
        lines+=['',f"### {c['id']} · {c['difficulty']}",f"Question: {c['problem']}",
            f"Givens: {'; '.join(c['givens'])}",f"Visual: {json.dumps(c['visual'],ensure_ascii=False)}",
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
    (OUT/f'functions_{n:02}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return dict(lesson_id=f'g9-functions-{n:02}',source=filename,
        source_sha256=sha256((DOC/filename).read_bytes()).hexdigest(),
        **{f'{kind}_ids':[x['id'] for x in data[kind]] for kind in ('worked','practice','mastery','reassessment')},
        **{f'{kind}_count':len(data[kind]) for kind in ('worked','practice','mastery','reassessment')},
        status='teacher_review_required',browser_accepted=False,teacher_approved=False)

if __name__=='__main__':
    manifest=[build(n) for n in range(1,6)]
    (DOC/'topic5-acceptance-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Authored',len(manifest),'lessons:',sum(x['worked_count'] for x in manifest),'worked,',sum(x['practice_count'] for x in manifest),'practice')
