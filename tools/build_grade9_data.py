"""Original Grade 9 Data Handling questions with deterministic answer keys."""
import json
from hashlib import sha256
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/curriculum/grade9/data-handling'
OUT=ROOT/'backend/app/curriculum/grade9/generated'
ATP='https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2026%20ATPs/2026_ATP_Mathematics_Grade%209.pdf'
TITLES={1:'Investigation, population and sample',2:'Collection, representation and bias',3:'Frequency tables and grouped data',4:'Centre, spread and outliers',5:'Bar and broken-line comparisons',6:'Histograms and class intervals',7:'Pie charts and scatter plots',8:'Critical interpretation and written report'}
def case(n,i,variant=0):
    seed=i+(19 if variant==3 else 16 if variant==2 else 15 if variant else 0)
    v={'lesson':n}
    if n==1:
        population=90+seed*7;sample=12+seed
        v.update(model='survey',population=population,sample=sample)
        problem=f'A school has {population} Grade 9 learners. A researcher asks {sample} of them about travel to school. State the population and sample sizes.'
        actions=[f'Identify the question: travel for the {population} Grade 9 learners.',f'The population is everyone the research describes: {population} learners.',f'The sample is the smaller group actually asked: {sample} learners.',f'The {sample} replies must not be reported as {population} individual replies.',f'Check: {sample} < {population}; state both sizes and who belongs to each group.']
        answer=f'population = {population}; sample = {sample}'
        wrong=[f'population = {population}; sample = {sample+d}' for d in (1,2,-1)]
    elif n==2:
        young=3*(20+seed);old=20+seed;target=12;young_pick=9;old_pick=3
        v.update(model='stratified',young=young,old=old,young_pick=young_pick,old_pick=old_pick,convenience_young=12,convenience_old=0)
        problem=f'The school register lists {young} junior and {old} senior learners. Select 12 proportionally to survey travel. A volunteer only asks 12 juniors. Name a suitable source and collection method; give the fair group counts and the bias.'
        actions=[f'Use the school register as the source of group sizes: {young} junior and {old} senior learners.',f'The population ratio is {young}:{old} = 3:1.',f'Use a stratified survey: divide 12 places into four equal parts, 12 ÷ 4 = 3 per part.',f'Allocate 9 junior and 3 senior places; taking 12 juniors and 0 seniors excludes seniors.',f'Check: 9 + 3 = 12, and 9:3 = {young}:{old}; the convenience sample is biased.']
        answer='source: school register; stratified survey: 9 junior, 3 senior; volunteer sample biased'
        wrong=['source: school register; stratified survey: 8 junior, 4 senior; volunteer sample biased','source: school register; stratified survey: 6 junior, 6 senior; volunteer sample biased','source: school register; convenience survey: 12 junior, 0 senior; volunteer sample unbiased']
    elif n==3:
        a=3+seed;b=a+3;c=2+seed%3;total=a+b+c
        v.update(model='frequency',categories=['1','2','3'],counts=[a,b,c],total=total,mode='2')
        problem=f'A class records reading scores: score 1 occurs {a} times, score 2 occurs {b} times, score 3 occurs {c} times. Complete the frequency total and identify the modal score.'
        actions=[f'Enter score 1 with a tally of {a}.',f'Enter score 2 with {b} and score 3 with {c} tallies.',f'Total frequency = {a} + {b} + {c} = {total}.',f'Score 2 has the largest frequency, {b}; the mode is 2.',f'Check: all category counts add to {total}, and {b} is greater than both {a} and {c}.']
        answer=f'total = {total}; mode = 2'
        wrong=[f'total = {total+d}; mode = 2' for d in (1,2,-1)]
    elif n==4:
        base=8+seed;values=[base-4,base-2,base-1,base,base+1,base+2,base+12];total=sum(values);mean=total/7;span=values[-1]-values[0]
        v.update(model='dotplot',values=values,total=total,median=base,mean_rounded=f'{mean:.2f}',range=span,outlier=base+12)
        problem=f'The seven daily counts are {", ".join(map(str,values))}. Find the mean (two decimals), median, range and possible high outlier.'
        actions=[f'Arrange the seven counts in order: {", ".join(map(str,values))}.',f'Sum them: {" + ".join(map(str,values))} = {total}.',f'Mean = {total} ÷ 7 ≈ {mean:.2f}; the fourth value gives median {base}.',f'Range = {values[-1]} − {values[0]} = {span}; {base+12} lies well above the cluster and is a possible outlier.',f'Check the original seven values: the sum is {total}, the centre is {base}, and both extreme values give range {span}.']
        answer=f'mean ≈ {mean:.2f}; median = {base}; range = {span}; possible outlier = {base+12}'
        wrong=[f'mean ≈ {mean:.2f}; median = {base+d}; range = {span}; possible outlier = {base+12}' for d in (1,2,-1)]
    elif n==5:
        a=12+seed;b=8+seed;a2=a+6+seed%4;b2=b+2;da=a2-a;db=b2-b
        v.update(model='double_bar',categories=['week 1','week 2'],series_a=[a,a2],series_b=[b,b2],gain_a=da,gain_b=db)
        problem=f'Two clubs count members in two weeks: A has {a}, then {a2}; B has {b}, then {b2}. Which club gains more, and by how many more members?'
        actions=[f'Mark week 1 counts A = {a}, B = {b} against the shared zero baseline.',f'Mark week 2 counts A = {a2}, B = {b2} on the same scale.',f'Club A gains {a2} − {a} = {da}.',f'Club B gains {b2} − {b} = {db}; A gains {da-db} more.',f'Check the paired bars use the same axis: {da} > {db}.']
        answer=f'A gains {da-db} more members'
        wrong=[f'A gains {da-db+d} more members' for d in (1,2,-1)]
    elif n==6:
        a=3+seed;b=a+4;c=2+seed%3;total=a+b+c
        v.update(model='histogram',intervals=['0–9','10–19','20–29'],counts=[a,b,c],total=total,modal_interval='10–19')
        problem=f'Grouped travel times (minutes) have frequencies 0–9: {a}, 10–19: {b}, 20–29: {c}. Find total frequency and the modal interval.'
        actions=[f'Mark continuous time intervals 0–9, 10–19 and 20–29 on the horizontal axis.',f'Draw touching bars of heights {a}, {b}, {c} on a zero-based frequency axis.',f'Total frequency = {a} + {b} + {c} = {total}.',f'The tallest bar has frequency {b}, in interval 10–19 minutes.',f'Check: each journey contributes to one interval; the modal class is an interval, not an individual time.']
        answer=f'total = {total}; modal interval = 10–19 min'
        wrong=[f'total = {total+d}; modal interval = 10–19 min' for d in (1,2,-1)]
    elif n==7 and seed%2:
        a=4*(1+seed%5);b=4*(2+seed%4);c=4*(3+seed%3);total=a+b+c;angle=360*a//total
        # Keep the exact fraction because an angle may not be an integer.
        from fractions import Fraction
        fraction=Fraction(360*a,total)
        v.update(model='pie',counts=[a,b,c],labels=['walk','bus','car'],total=total,walk_angle_num=fraction.numerator,walk_angle_den=fraction.denominator)
        problem=f'A transport survey counts walk {a}, bus {b}, car {c}. Find the total and the exact pie-sector angle for walking.'
        actions=[f'Put walk {a}, bus {b}, car {c} in a frequency table.',f'Total responses = {a} + {b} + {c} = {total}.',f'Walking is {a}/{total} of a whole circle.',f'Walk sector = ({a}/{total}) × 360° = {fraction}°.',f'Check: each sector uses its count divided by {total}; all three sector angles must total 360°.']
        answer=f'total = {total}; walking angle = {fraction}°'
        wrong=[f'total = {total+d}; walking angle = {fraction}°' for d in (1,2,-1)]
    elif n==7:
        k=2+seed;points=[[x,2*x+k] for x in range(1,6)];pred=12+k
        v.update(model='scatter',points=points,prediction=pred)
        problem=f'Five paired (study hours, score) readings are {", ".join(str(tuple(p)) for p in points)}. Describe the association and predict the score at 6 hours using the pattern.'
        actions=[f'Label study hours on the horizontal axis and score on the vertical axis.',f'Plot each given pair: {", ".join(str(tuple(p)) for p in points)}.',f'Every increase of one hour pairs with a score increase of 2.',f'The points show a positive association; the line rule for these data is score = 2h + {k}.',f'Predict at 6 hours: 2(6) + {k} = {pred}; this is an extrapolation beyond the measured hours.']
        answer=f'positive association; predicted score at 6 h = {pred}'
        wrong=[f'positive association; predicted score at 6 h = {pred+d}' for d in (1,2,-1)]
    else:
        first=36+seed;second=first+6;growth=round(600/first,2);baseline=first-5
        v.update(model='misleading_bar',first=first,second=second,truncated_baseline=baseline,difference=6,percent=f'{growth:.2f}')
        problem=f'A chart shows {first} and {second} responses but begins its bar axis at {baseline}. State the true difference and percentage increase (two decimals), and describe why the chart misleads.'
        actions=[f'Read actual labels {first} and {second}, not just the visible bar lengths.',f'The axis starts at {baseline}, not zero, so the visible bars exaggerate the relative change.',f'Actual difference = {second} − {first} = 6 responses.',f'Percentage increase = 6 ÷ {first} × 100 ≈ {growth:.2f}%.',f'Report: increase is 6 responses ({growth:.2f}%); the truncated axis exaggerates its visual size.']
        answer=f'difference = 6; increase ≈ {growth:.2f}%; truncated axis exaggerates change'
        wrong=[f'difference = {6+d}; increase ≈ {growth:.2f}%; truncated axis exaggerates change' for d in (1,2,-1)]
    assert len(set([answer,*wrong]))==4
    return {'id':f'g9-data-l{n:02}-w{i:02}' if not variant else f'g9-data-l{n:02}-v{variant}-w{i:02}', 'problem':problem,'actions':actions,'answer':answer,'check':actions[-1],'wrong':wrong,'misconception':'Keep the source, count, denominator and axis scale tied to the original dataset.','visual':{'family':'data','values':v},'lesson':n}
def choice(n,i,variant,prefix):
    c=case(n,i,variant);opts=[c['answer'],*c['wrong']];position=i%4
    opts=opts[4-position:]+opts[:4-position] if position else opts
    return {'id':f'g9-data-l{n:02}-{prefix}{i:02}','prompt':c['problem'],'options':opts,'answer_index':position,'memo':' '.join(c['actions']),'source':f'lesson-{n:02}.md'}
def build():
    DOC.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True);manifest=[]
    for n,title in TITLES.items():
        worked=[{k:v for k,v in case(n,i).items() if k!='wrong'}|{'difficulty':'foundation' if i<=2 else 'easy' if i<=5 else 'standard' if i<=9 else 'intermediate' if i<=12 else 'exam'} for i in range(1,16)]
        data={'source':f'lesson-{n:02}.md','worked':worked,'practice':[choice(n,i,1,'p') for i in range(1,16)],'mastery':[choice(n,i+15,2,'m') for i in range(1,6)],'reassessment':[choice(n,i+18,3,'r') for i in range(1,4)]}
        assert len({c['problem'] for c in worked})==15
        lines=[f'# Grade 9 Topic 12 · Lesson {n}: {title}',f'Authority: [DBE 2026 Grade 9 Mathematics ATP]({ATP}), Term 3. Original Athena questions.','Status: teacher and browser review required. Keep the dataset visible; reveal each count, calculation and inference in order.']
        for c in worked:lines.extend([f'## {c["id"]}: {c["problem"]}',f'Visual: {json.dumps(c["visual"],ensure_ascii=False)}',*[f'{j}. {step}' for j,step in enumerate(c['actions'],1)],f'**Answer:** {c["answer"]}. **Misconception:** {c["misconception"]}'])
        for label,key in [('Practice','practice'),('Mastery','mastery'),('Changed-value reassessment','reassessment')]:
            lines.append(f'## {label} answer key')
            for c in data[key]:lines.append(f'- {c["id"]}: {c["prompt"]} Options: {" | ".join(c["options"])}. Correct: {c["options"][c["answer_index"]]}. {c["memo"]}')
        source=DOC/data['source'];source.write_text('\n\n'.join(lines)+'\n',encoding='utf-8')
        (OUT/f'data_{n:02}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        manifest.append({'lesson_id':f'g9-data-{n:02}','source':source.name,'source_sha256':sha256(source.read_bytes()).hexdigest(),'worked':15,'practice':15,'mastery':5,'reassessment':3,'status':'teacher_review_required','teacher_approved':False,'browser_accepted':False})
    (DOC/'topic12-acceptance-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    (DOC/'topic12-batch-acceptance.md').write_text(f'# Grade 9 Topic 12: Data Handling\n\n[DBE 2026 Grade 9 Mathematics ATP, Term 3]({ATP}) covers data collection, representation, comparison, interpretation and reporting. Athena splits this into eight lessons with 120 worked examples, 120 four-choice practice items, 40 mastery items and 24 changed-value reassessments. Teacher review and desktop/mobile browser acceptance remain required.\n',encoding='utf-8')
if __name__=='__main__':build()
