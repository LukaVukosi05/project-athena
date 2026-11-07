"""Original Grade 9 line geometry lessons with explicit angle sectors and answer keys."""
import json
from hashlib import sha256
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/curriculum/grade9/geometry-of-straight-lines'
OUT=ROOT/'backend/app/curriculum/grade9/generated'
ATP='https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2026%20ATPs/2026_ATP_Mathematics_Grade%209.pdf'
TITLES={1:'Intersecting and perpendicular angle relationships',2:'Parallel lines and a transversal',3:'Combined angle chains',4:'Algebraic unknowns in line geometry',5:'Proof, first-error diagnosis and reassessment'}

def case(lesson,index,variant=0):
    seed=index+23*variant
    theta=40+(seed*7)%45
    assert 40<=theta<=84
    visual={'kind':'intersection' if lesson==1 and seed%3!=2 else 'perpendicular' if lesson==1 else 'parallel',
            'theta':theta,'lesson':lesson}
    if lesson==1:
        relation=('vertical','linear','right')[seed%3]
        given=theta;target={'vertical':theta,'linear':180-theta,'right':90-theta}[relation]
        visual.update(relation=relation,given=given,target=target)
        statement={'vertical':'vertically opposite','linear':'adjacent on a straight line','right':'two parts of a right angle'}[relation]
        prompt=f'In the marked {"perpendicular" if relation=="right" else "intersecting"} lines, the shown angle is {given}°. Find the separate marked angle x and justify it.'
        equation=f'x = {given}°' if relation=='vertical' else f'x + {given}° = {90 if relation=="right" else 180}°'
        check=f'Check: the two marked angles are equal at {given}°.' if relation=='vertical' else f'Check: {given}° + {target}° = {90 if relation=="right" else 180}°.'
        actions=[f'Locate the distinct {given}° sector and the sector marked x; keep the line intersection fixed.',
                 f'Identify the relationship: the two sectors are {statement}.',
                 f'Write the relationship as {equation}.',
                 f'Calculate x = {target}°.',check]
        answer=f'x = {target}°';wrong=[f'x = {target+7}°',f'x = {target+14}°',f'x = {target-7}°']
    elif lesson==2:
        relation=('corresponding','alternate','cointerior')[seed%3]
        given=180-theta if relation=='cointerior' else theta;target=theta
        visual.update(relation=relation,given=given,target=target)
        prompt=f'The two marked lines are parallel and cut by a transversal. The labelled {relation.replace("cointerior","co-interior")} angle is {given}°. Find the target angle x and give the reason.'
        equation=f'x = {given}°' if relation!='cointerior' else f'x + {given}° = 180°'
        check=f'Check: the marked pair is equal at {target}°.' if relation!='cointerior' else f'Check: {given}° + {target}° = 180°.'
        actions=[f'Identify the two parallel marks and trace the single transversal.',
                 f'Locate the given {given}° sector and the target sector x at the other crossing.',
                 f'Use the {relation.replace("cointerior","co-interior")} angle theorem: {equation}.',
                 f'Calculate x = {target}°.',check]
        answer=f'x = {target}°';wrong=[f'x = {180-target}°',f'x = {target+10}°',f'x = {target-10}°']
    elif lesson==3:
        given=theta;target=180-theta
        visual.update(relation='chain',given=given,target=target,middle=theta)
        prompt=f'Two marked parallel lines are crossed by one transversal. The upper top-right angle is {given}°. Find the lower top-left angle x, naming each relationship.'
        actions=[f'Locate the upper top-right sector labelled {given}°.',
                 f'Mark the lower top-right sector as a corresponding angle to the given sector.',
                 f'Corresponding angles are equal: the lower top-right angle is {given}°.',
                 f'The lower top-right and top-left angles form a straight line: x + {given}° = 180°.',
                 f'Subtract {given}° to obtain x = {target}°.',
                 f'Check: {target}° + {given}° = 180° at the lower intersection.']
        answer=f'x = {target}°';wrong=[f'x = {given}°',f'x = {target+10}°',f'x = {target-10}°']
    elif lesson==4:
        x=2+seed%10;a=2+seed%4;target=180-theta;b=target-a*x
        visual.update(relation='algebra',given=theta,target=target,coefficient=a,constant=b,solution=x,middle=theta)
        prompt=f'Two marked parallel lines have an upper top-right angle of {theta}°. The lower top-left angle is labelled ({a}x + {b})°. Find x, then calculate the marked angle.'
        actions=[f'Mark the given upper top-right sector as {theta}°.',
                 f'Its lower top-right corresponding partner is also {theta}°.',
                 f'The lower top-left sector and that partner lie on a straight line, so its measure is 180° − {theta}° = {target}°.',
                 f'Equate its label to its measure: {a}x + {b} = {target}.',
                 f'Subtract {b} from both sides: {a}x = {target-b}.',
                 f'Divide both sides by {a}: x = {x}; the marked angle is {target}°.',
                 f'Check: {a}({x}) + {b} = {target}, and {target}° + {theta}° = 180°.']
        answer=f'x = {x}';wrong=[f'x = {x+1}',f'x = {x-1}',f'x = {target}']
    else:
        relation=('corresponding','alternate','cointerior')[seed%3]
        given=180-theta if relation=='cointerior' else theta;target=theta
        claimed=given if relation=='cointerior' else 180-given
        visual.update(relation=relation,given=given,target=target,claimed=claimed)
        prompt=f'At two marked parallel lines, a {relation.replace("cointerior","co-interior")} pair includes the given {given}° angle and target x. A learner writes x = {claimed}°. Locate the first incorrect reason and repair it.'
        theorem=f'co-interior angles sum to 180°: x + {given}° = 180°' if relation=='cointerior' else f'{relation} angles are equal: x = {given}°'
        actions=[f'Find the given {given}° sector and the separate target x, using the parallel marks.',
                 f'The learner wrote x = {claimed}°; identify which sectors were compared.',
                 f'Check the diagram: the pair is {relation.replace("cointerior","co-interior")}, so {theorem}.',
                 f'The learner used the wrong relationship at the previous step. Repair x = {target}°.',
                 f'Check: {given}° + {target}° = 180°.' if relation=='cointerior' else f'Check: both marked {relation} sectors equal {target}°.']
        answer=f'x = {target}°';wrong=[f'x = {claimed}°',f'x = {target+10}°',f'x = {target-10}°']
    assert len(set([answer,*wrong]))==4,(lesson,index,answer,wrong)
    return {'id':f'g9-lines-l{lesson:02}-w{index:02}' if not variant else f'g9-lines-l{lesson:02}-v{variant}-w{index:02}',
        'problem':prompt,'actions':actions,'answer':answer,'check':actions[-1],'wrong':wrong,
        'misconception':'Name the exact angle pair and its parallel or perpendicular markings; visual appearance alone is not proof.',
        'visual':{'family':'straight_lines','values':visual},'lesson':lesson}

def choice(lesson,index,variant,prefix):
    c=case(lesson,index,variant);right=c['answer'];options=[right,*c['wrong']];correct=index%4
    options=options[4-correct:]+options[:4-correct] if correct else options
    return {'id':f'g9-lines-l{lesson:02}-{prefix}{index:02}','prompt':c['problem'],'options':options,
        'answer_index':correct,'memo':' '.join(c['actions']),'source':f'lesson-{lesson:02}.md'}

def build():
    DOC.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True);manifest=[]
    for n,title in TITLES.items():
        worked=[{key:value for key,value in case(n,i).items() if key!='wrong'}|{'difficulty':'foundation' if i<=2 else 'easy' if i<=5 else 'standard' if i<=9 else 'intermediate' if i<=12 else 'exam'} for i in range(1,16)]
        data={'source':f'lesson-{n:02}.md','worked':worked,
              'practice':[choice(n,i,1,'p') for i in range(1,16)],
              'mastery':[choice(n,i+15,2,'m') for i in range(1,6)],
              'reassessment':[choice(n,i+18,3,'r') for i in range(1,4)]}
        assert len({c['problem'] for c in worked})==15
        lines=[f'# Grade 9 Topic 9 · Lesson {n}: {title}',f'Authority: [DBE 2026 Grade 9 Mathematics ATP]({ATP}), Term 2. Original Athena questions.',
               'Status: teacher and browser review required. The diagram has distinct labelled sectors. Reveal the actual theorem and value in order; preserve previous work.']
        for c in worked:lines.extend([f'## {c["id"]}: {c["problem"]}',f'Visual: {json.dumps(c["visual"],ensure_ascii=False)}',*[f'{j}. {action}' for j,action in enumerate(c['actions'],1)],f'**Answer:** {c["answer"]}. **Misconception:** {c["misconception"]}'])
        for label,key in [('Practice','practice'),('Mastery','mastery'),('Changed-value reassessment','reassessment')]:
            lines.append(f'## {label} answer key')
            for c in data[key]:lines.append(f'- {c["id"]}: {c["prompt"]} Options: {" | ".join(c["options"])}. Correct: {c["options"][c["answer_index"]]}. {c["memo"]}')
        source=DOC/data['source'];source.write_text('\n\n'.join(lines)+'\n',encoding='utf-8')
        (OUT/f'straight_lines_{n:02}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        manifest.append({'lesson_id':f'g9-straight-lines-{n:02}','source':source.name,'source_sha256':sha256(source.read_bytes()).hexdigest(),
            'worked':15,'practice':15,'mastery':5,'reassessment':3,'status':'teacher_review_required','teacher_approved':False,'browser_accepted':False})
    (DOC/'topic9-acceptance-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    (DOC/'topic9-batch-acceptance.md').write_text(f'''# Grade 9 Topic 9: Geometry of Straight Lines\n\n[DBE 2026 Grade 9 Mathematics ATP, Term 2]({ATP}) requires angle relationships formed by perpendicular, intersecting and parallel lines, then problems with reasons. Athena's five-lesson breakdown is a product decision.\n\nEvery lesson has 15 worked examples, 15 four-choice practice items, five mastery and three changed-value reassessments. Teacher mathematical and accessibility review plus real desktop/mobile browser acceptance remain required.\n''',encoding='utf-8')
if __name__=='__main__':build()
