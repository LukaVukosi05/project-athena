"""Original DBE ATP aligned Grade 9 graph questions, diagrams and independent MCQs."""
import json
from hashlib import sha256
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/curriculum/grade9/graphs'
OUT=ROOT/'backend/app/curriculum/grade9/generated'
ATP='https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2026%20ATPs/2026_ATP_Mathematics_Grade%209.pdf'
TITLES={1:'Global graph features in context',2:'Ordered pairs and Cartesian plotting',3:'Gradient as rise over run',4:'Intercepts of straight lines',5:'Draw a line from its equation',6:'Find an equation from a graph',7:'Integrated graph interpretation and first-error repair'}

def rule(m,b):
    return f'y = {m}x {"+" if b>=0 else "−"} {abs(b)}'

def case(lesson,index,variant=0):
    assert 1<=lesson<=7 and 1<=index<=23 and 0<=variant<=3
    seed=index+23*variant
    m=(2+seed%4)*(-1 if seed%3==0 else 1)
    b=(2+seed%5+7*(seed//15))*(-1 if seed%4==0 else 1)
    values={'m':m,'b':b}; family=('global','ordered','gradient','intercepts','line','infer','diagnosis')[lesson-1]
    if lesson==1:
        start=seed;peak=start+3+seed%5;end=start+seed%3
        points=[[0,start],[2,peak],[4,peak],[6,end]]
        values={'points':points,'peak':peak}
        problem=f'A water tank reading (litres) changes at hours 0, 2, 4 and 6: {start}, {peak}, {peak}, {end}. Join the readings with straight segments. Describe each interval and give the maximum reading.'
        actions=[f'Plot the original reading (0, {start}) on the labelled axes.',
                 f'Plot (2, {peak}); from 0 to 2 hours the reading increases.',
                 f'Plot (4, {peak}); from 2 to 4 hours the reading is constant.',
                 f'Plot (6, {end}); from 4 to 6 hours the reading decreases.',
                 f'The highest plotted level is {peak} litres, held from hour 2 to hour 4.',
                 f'Check: {peak} is at least as large as all four readings {start}, {peak}, {peak}, {end}.']
        answer=f'maximum = {peak} litres';wrong=[f'maximum = {start} litres',f'maximum = {end} litres',f'maximum = {peak+2} litres']
        if start==end:wrong[1]=f'maximum = {peak-1} litres'
    elif lesson==2:
        points=[[x,m*x+b] for x in (-1,0,1,2)]
        values.update(points=points)
        problem=f'Complete the table for {rule(m,b)} at x = −1, 0, 1 and 2. Plot each ordered pair. What is the point at x = 2?'
        actions=[f'For x = −1, y = {m}(−1) {"+" if b>=0 else "−"} {abs(b)} = {points[0][1]}; plot (−1, {points[0][1]}).',
                 f'For x = 0, y = {b}; plot (0, {b}) on the vertical axis.',
                 f'For x = 1, y = {m+b}; plot (1, {m+b}).',
                 f'For x = 2, y = {2*m+b}; plot (2, {2*m+b}).',
                 f'Check: substituting 2 in {rule(m,b)} gives y = {2*m+b}.']
        answer=f'(2, {2*m+b})';wrong=[f'({2*m+b}, 2)',f'(2, {m+b})',f'(2, {2*m-b})']
        if len(set([answer,*wrong]))<4:wrong[-1]=f'(2, {2*m+b+2})'
    elif lesson==3:
        x1=-(seed%3);run=2+seed%2;y1=m*x1+b;x2=x1+run;y2=y1+m*run
        values.update(points=[[x1,y1],[x2,y2]],run=run,rise=y2-y1)
        problem=f'Find the gradient of the straight line through A({x1}, {y1}) and B({x2}, {y2}). Draw and label a rise/run triangle.'
        actions=[f'Plot A({x1}, {y1}) and B({x2}, {y2}) on the same axes.',
                 f'From A to B the horizontal run is {x2} − ({x1}) = {run}.',
                 f'The vertical rise is {y2} − ({y1}) = {m*run}.',
                 f'Gradient = rise ÷ run = {m*run} ÷ {run} = {m}.',
                 f'Check: moving {run} units right changes y by {m*run}, so the gradient is {m}.']
        answer=f'gradient = {m}';wrong=[f'gradient = {m*run}',f'gradient = {-m}',f'gradient = {m+1}']
    elif lesson==4:
        b=m*(2+seed%13+5*(seed//60));x0=-b//m;values.update(b=b,x_intercept=x0,points=[[x0,0],[0,b]])
        problem=f'Find and plot both axis intercepts of {rule(m,b)}. State them as ordered pairs.'
        actions=[f'At the y-axis x = 0, so y = {m}(0) {"+" if b>=0 else "−"} {abs(b)} = {b}.',
                 f'Plot the y-intercept (0, {b}).',
                 f'At the x-axis y = 0: 0 = {m}x {"+" if b>=0 else "−"} {abs(b)}.',
                 f'Solve for x: {m}x = {-b}, so x = {x0}; plot ({x0}, 0).',
                 f'Check: {m}({x0}) + ({b}) = 0, and x=0 gives y={b}.']
        answer=f'({x0}, 0) and (0, {b})';wrong=[f'(0, {x0}) and ({b}, 0)',f'({-x0}, 0) and (0, {b})',f'({x0}, 0) and (0, {-b})']
    elif lesson==5:
        points=[[x,m*x+b] for x in (-1,0,1,2)];values.update(points=points)
        problem=f'Draw the graph of {rule(m,b)} for −1 ≤ x ≤ 2 using a table. State two points that fix the line.'
        actions=[f'Choose x = −1, 0, 1, 2; keep each input beside its calculated output.',
                 f'At x = −1, y = {b-m}; mark (−1, {b-m}).',
                 f'At x = 0, y = {b}; mark (0, {b}).',
                 f'At x = 1, y = {b+m}; mark (1, {b+m}).',
                 f'At x = 2, y = {b+2*m}; mark (2, {b+2*m}).',
                 f'Join the four plotted points with one straight line.',
                 f'Check: the line includes (0, {b}) and (1, {b+m}), a change of {m} for a run of 1.']
        answer=f'(0, {b}) and (1, {b+m})';wrong=[f'(0, {b+2}) and (1, {b+m})',f'(0, {b}) and (1, {b-m})',f'(0, {b+1}) and (1, {b+m+1})']
    elif lesson==6:
        points=[[0,b],[1,b+m],[2,b+2*m]];values.update(points=points)
        problem=f'A straight line passes through (0, {b}), (1, {b+m}) and (2, {b+2*m}). Find its equation in the form y = mx + c.'
        actions=[f'Plot the first given point (0, {b}).',
                 f'Plot the next given point (1, {b+m}).',
                 f'Plot (2, {b+2*m}); the three points align.',
                 f'The y-intercept is (0, {b}), so c = {b}.',
                 f'From (0, {b}) to (1, {b+m}), rise = {m} and run = 1.',
                 f'The gradient is m = {m} ÷ 1 = {m}; the rule is {rule(m,b)}.',
                 f'Check: at x=2 the rule gives {m}(2)+({b}) = {2*m+b}, matching (2, {2*m+b}).']
        answer=rule(m,b);wrong=[rule(-m,b),rule(m,-b),rule(m+1,b)]
    else:
        points=[[0,b],[1,b+m],[2,b+2*m]];wrong_m=m+1;values.update(points=points,claimed_gradient=wrong_m)
        problem=f'A line passes through (0, {b}), (1, {b+m}), (2, {b+2*m}). A learner claims its gradient is {wrong_m}, so its equation is {rule(wrong_m,b)}. Identify the first error and give the correct equation.'
        actions=[f'Plot the original point (0, {b}).',
                 f'Plot the original point (1, {b+m}).',
                 f'Plot the original point (2, {b+2*m}); retain both earlier points.',
                 f'Test the learner claim at x=1: {wrong_m}(1)+({b}) = {wrong_m+b}, but the given y is {m+b}.',
                 f'The first error is the gradient: the actual rise from x=0 to x=1 is {m+b} − ({b}) = {m}.',
                 f'The run is 1, so the correct gradient is {m}; the y-intercept remains {b}.',
                 f'Repair the equation to {rule(m,b)}.',
                 f'Check: at x=2, {m}(2)+({b}) = {2*m+b}, the given output.']
        answer=rule(m,b);wrong=[rule(wrong_m,b),rule(-m,b),rule(m,-b)]
    assert len(set([answer,*wrong]))==4,(lesson,index,answer,wrong)
    return {'id':f'g9-gr-l{lesson:02}-w{index:02}' if not variant else f'g9-gr-l{lesson:02}-v{variant}-w{index:02}',
      'problem':problem,'actions':actions,'answer':answer,'check':actions[-1],
      'misconception':('Keep axes and ordered-pair positions fixed; reveal each calculated point before joining a line.' if lesson!=1 else 'A flat interval is constant, and the maximum is a y-value, not the hour.'),
      'visual':{'family':family,'values':values},'wrong':wrong,'lesson':lesson}

def choice(lesson,index,variant,prefix):
    item=case(lesson,index,variant);answer=item['answer'];wrong=item['wrong'];correct=index%4
    options=[answer,*wrong];options=options[4-correct:]+options[:4-correct] if correct else options
    return {'id':f'g9-gr-l{lesson:02}-{prefix}{index:02}','prompt':item['problem'],'options':options,
      'answer_index':correct,'memo':' '.join(item['actions']),'source':f'lesson-{lesson:02}.md'}

def build():
    DOC.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True);manifest=[]
    for number,title in TITLES.items():
        worked=[{k:v for k,v in case(number,index).items() if k!='wrong'}|{'difficulty':'foundation' if index<=2 else 'easy' if index<=5 else 'standard' if index<=9 else 'intermediate' if index<=12 else 'exam'} for index in range(1,16)]
        data={'source':f'lesson-{number:02}.md','worked':worked,'practice':[choice(number,i,1,'p') for i in range(1,16)],
              'mastery':[choice(number,i+15,2,'m') for i in range(1,6)],'reassessment':[choice(number,i+18,3,'r') for i in range(1,4)]}
        assert len({s['problem'] for s in worked})==15
        lines=[f'# Grade 9 Topic 8 · Lesson {number}: {title}',f'Authority: [DBE 2026 Grade 9 Mathematics ATP]({ATP}), Term 2. All questions are original Athena variants.',
               'Status: teacher and browser review required. Use a scaled coordinate plane; retain axes, givens and prior written steps. Each action reveals only its own point, triangle or line.']
        for item in worked:
            lines.extend([f'## {item["id"]}: {item["problem"]}',f'Visual: {json.dumps(item["visual"],ensure_ascii=False)}',*[f'{j}. {a}' for j,a in enumerate(item['actions'],1)],f'**Answer:** {item["answer"]}. **Misconception:** {item["misconception"]}'])
        for label,key in [('Practice','practice'),('Mastery','mastery'),('Changed-value reassessment','reassessment')]:
            lines.append(f'## {label} answer key')
            for item in data[key]:lines.append(f'- {item["id"]}: {item["prompt"]} Options: {" | ".join(item["options"])}. Correct: {item["options"][item["answer_index"]]}. {item["memo"]}')
        source=DOC/data['source'];source.write_text('\n\n'.join(lines)+'\n',encoding='utf-8')
        (OUT/f'graphs_{number:02}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        manifest.append({'lesson_id':f'g9-graphs-{number:02}','source':data['source'],'source_sha256':sha256(source.read_bytes()).hexdigest(),
           'worked':15,'practice':15,'mastery':5,'reassessment':3,'status':'teacher_review_required','teacher_approved':False,'browser_accepted':False})
    (DOC/'topic8-acceptance-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    (DOC/'topic8-batch-acceptance.md').write_text(f'''# Grade 9 Topic 8: Graphs\n\n[DBE 2026 Grade 9 Mathematics ATP, Term 2]({ATP}) covers global features, linear gradient and intercepts, ordered pairs, drawing from equations and equations from graphs. Seven lessons are Athena's product breakdown.\n\nEach lesson includes 15 original worked examples, 15 separate four-option practice questions, five mastery and three changed-value reassessments. The renderer should plot each question's points incrementally on a persistent coordinate plane and keep a cumulative written record.\n\nTeacher review and real desktop/mobile browser acceptance remain required before release. Structural and arithmetic tests do not establish learning outcomes.\n''',encoding='utf-8')
if __name__=='__main__':build()
