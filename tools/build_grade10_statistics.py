"""Original Grade 10 statistics worked examples; arithmetic generated from each dataset."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
from fractions import Fraction
import json

ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/curriculum/grade10/statistics'
OUT=ROOT/'backend/app/curriculum/grade10/generated'
ATP='https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2023%20ATPs/FET%20Content%20Subjects/Grade%2010/1.580%20ATP%202023-24%20Gr%2010%20Maths%20final.pdf'
TITLES={1:'Mean, median and mode in ungrouped data',2:'Grouped frequency tables and estimated mean',3:'Quartiles, percentiles, range and interquartile range',4:'Five-number summaries and box-and-whisker plots',5:'Histograms and frequency comparisons',6:'Compare distributions and diagnose misleading claims'}

def fmt(x):
    return str(x.numerator) if isinstance(x,Fraction) and x.denominator==1 else str(x)

def median(a):
    n=len(a)
    return Fraction(a[n//2]) if n%2 else Fraction(a[n//2-1]+a[n//2],2)

def case(n,i,variant=0):
    s=i+variant*17;shift=s%13;scale=1+s%3
    base=[1,2,2,3,4,4,5,6,7,8] if s%2 else [1,1,2,3,3,4,5,5,6,8]
    data=[shift+scale*x for x in base]
    total=sum(data);mean=Fraction(total,len(data));med=median(data);counts=Counter(data)
    modes=sorted(x for x,c in counts.items() if c==max(counts.values()))
    steps=[];v={'lesson':n,'model':'statistics','data':data,'shift':shift,'scale':scale}
    if n==1:
        task=('mean','median','mode')[(s-1)%3];answer={'mean':fmt(mean),'median':fmt(med),'mode':', '.join(map(str,modes))}[task]
        problem=f'The ten daily results are {", ".join(map(str,data))}. Calculate the {task}.'
        steps=[f'Write down all ten results and identify the requested {task}.',f'Order the data: {", ".join(map(str,data))}.',
            f'For the mean, total={total} and count=10. For the median, the middle pair is {data[4]} and {data[5]}.',
            f'Mean={fmt(mean)}; median=({data[4]}+{data[5]})/2={fmt(med)}; highest frequency={max(counts.values())}, mode={", ".join(map(str,modes))}.',
            f'Answer: {task} = {answer}. Check the answer against the original ten observations.']
        wrong=[fmt(mean+1),fmt(med+1),str(max(data)+1),str(min(data)-1)]
    elif n==2:
        mid=[5+shift,15+shift,25+shift,35+shift];freq=[2+s%3,3+(s//2)%3,4+(s//3)%3,2+(s//4)%3]
        lower=[x-5 for x in mid];upper=[x+5 for x in mid];weighted=sum(m*f for m,f in zip(mid,freq));N=sum(freq);estimate=Fraction(weighted,N)
        v.update(midpoints=mid,frequencies=freq,lower=lower,upper=upper)
        task=('estimated mean','modal interval','median interval')[(s-1)%3]
        cumulative=[];c=0
        for f in freq:c+=f;cumulative.append(c)
        modal_index=max(range(4),key=lambda j:freq[j]);median_index=next(j for j,c in enumerate(cumulative) if c>=Fraction(N,2))
        answer=fmt(estimate) if task=='estimated mean' else f'{lower[modal_index]}–{upper[modal_index]}' if task=='modal interval' else f'{lower[median_index]}–{upper[median_index]}'
        problem=f'A grouped distribution has equal-width intervals {", ".join(f"{a}–{b}" for a,b in zip(lower,upper))} with respective frequencies {freq}. Find the {task}.'
        steps=[f'Copy each class interval with its frequency; there are {N} observations in total.',f'Use class midpoints {mid} and cumulative frequencies {cumulative}.',
            f'Multiply each midpoint by its frequency: {[m*f for m,f in zip(mid,freq)]}; sum={weighted}.',
            f'Estimated mean={weighted}/{N}={fmt(estimate)}; modal interval has frequency {freq[modal_index]}; median lies where cumulative frequency reaches {N}/2.',
            f'Answer: {task} = {answer}. This is an estimate when using class midpoints; no precise raw-data mean is known.']
        wrong=[fmt(estimate+1),fmt(Fraction(sum(mid),4)),f'{lower[(modal_index+1)%4]}–{upper[(modal_index+1)%4]}',f'{lower[(median_index+1)%4]}–{upper[(median_index+1)%4]}']
    elif n in (3,4):
        # Ten values: Q1 is the median of the lower five, Q3 of the upper five.
        lo,hi=data[2],data[7];iqr=hi-lo;range_=data[-1]-data[0]
        v.update(summary=[data[0],lo,fmt(med),hi,data[-1]],q1=lo,q3=hi,median=fmt(med),minimum=data[0],maximum=data[-1])
        if n==3:
            task=('Q1','Q3','IQR','range','25th percentile','75th percentile')[(s-1)%6]
            answer=str(lo) if task in ('Q1','25th percentile') else str(hi) if task in ('Q3','75th percentile') else str(iqr) if task=='IQR' else str(range_)
            problem=f'For the ordered data {data}, find the {task}. Use the median-of-halves convention for quartiles.'
        else:
            task=('five-number summary','interquartile range')[(s-1)%2]
            answer=f'({data[0]}, {lo}, {fmt(med)}, {hi}, {data[-1]})' if task=='five-number summary' else str(iqr)
            problem=f'Construct a box-and-whisker plot for {data}, then give its {task}. Use the median-of-halves convention.'
        steps=[f'Keep the ten original values in ascending order: {data}.',f'Median is the average of positions 5 and 6: ({data[4]}+{data[5]})/2={fmt(med)}.',
            f'Lower half={data[:5]}; its middle is Q1={lo}. Upper half={data[5:]}; its middle is Q3={hi}.',
            f'Minimum={data[0]}, maximum={data[-1]}; range={range_}; IQR={hi}−{lo}={iqr}. Draw whiskers and the box at those actual scale values.',
            f'Answer: {task} = {answer}. The box covers the middle 50% of the ordered observations.']
        wrong=[str(hi),str(iqr+1),str(range_+1),str(lo-1),f'({data[0]}, {lo}, {fmt(med)}, {hi}, {data[-1]+1})']
    elif n==5:
        freq=[2+s%3,3+(s//2)%4,4+(s//3)%4,2+(s//4)%3];start=shift*2
        lower=[start+10*j for j in range(4)];upper=[x+10 for x in lower];idx=max(range(4),key=lambda j:freq[j]);N=sum(freq)
        v.update(frequencies=freq,lower=lower,upper=upper)
        task=('modal interval','total frequency')[(s-1)%2]
        answer=f'{lower[idx]}–{upper[idx]}' if task=='modal interval' else str(N)
        problem=f'Equal-width continuous intervals {list(zip(lower,upper))} have frequencies {freq}. Draw a histogram and find the {task}.'
        steps=[f'Label the horizontal axis with the touching class boundaries {lower+[upper[-1]]}.',f'Mark frequency increments on the vertical axis up to {max(freq)}.',
            f'Draw touching bars, each width 10, with successive heights {freq}.',f'Compare the bar heights: the largest is {freq[idx]} in {lower[idx]}–{upper[idx]}; total frequency={N}.',
            f'Answer: {task} = {answer}. With equal class widths, the tallest bar identifies the modal interval.']
        wrong=[str(N+1),f'{lower[(idx+1)%4]}–{upper[(idx+1)%4]}',str(max(freq)),str(sum(lower))]
    else:
        # Two ordered groups: compare their medians and IQRs from actual data.
        other=[x+(scale if j>=5 else 0) for j,x in enumerate(data)];ma=med;mb=median(other);q1b=other[2];q3b=other[7]
        v.update(other=other,summary=[data[0],data[2],fmt(ma),data[7],data[-1]],other_summary=[other[0],q1b,fmt(mb),q3b,other[-1]])
        answer=f'Group B has a higher median ({fmt(mb)} versus {fmt(ma)})' if s%2 else f'Group A has smaller IQR ({data[7]-data[2]} versus {q3b-q1b})'
        problem=f'Group A has ordered results {data}; group B has {other}. Compare the {"median" if s%2 else "IQR"} and support your conclusion.'
        steps=[f'Plot both groups on the same labelled number axis; do not compare raw maxima only.',f'Group A median={fmt(ma)}, Q1={data[2]}, Q3={data[7]}.',
            f'Group B median={fmt(mb)}, Q1={q1b}, Q3={q3b}.',f'Group A IQR={data[7]-data[2]}; group B IQR={q3b-q1b}. Compare the requested statistic.',
            f'Answer: {answer}. The other statistic measures a different feature of the distributions.']
        wrong=[f'Group A has a higher median ({fmt(ma)} versus {fmt(mb)})',f'Group B has smaller IQR ({q3b-q1b} versus {data[7]-data[2]})','Both groups have identical spread','The maximum alone proves the claim']
    wrong=list(dict.fromkeys(x for x in wrong if x!=answer))
    for filler in ('No answer can be calculated','The minimum is the mean','All observations are equal'):
        if filler not in wrong and filler!=answer:wrong.append(filler)
    assert len(steps)==5 and len({answer,*wrong[:3]})==4,(n,i)
    v['answer']=answer
    return {'id':f'g10-stat-l{n:02}-w{i:02}','problem':problem,'actions':steps,'answer':answer,'check':steps[-1],
      'visual':{'family':'grade10_statistics','values':v},'lesson':n,'wrong':wrong[:3],
      'misconception':'Keep the original observations, axis scale and denominators visible; distinguish estimates from exact values.',
      'difficulty':'foundation' if i<=2 else 'easy' if i<=5 else 'standard' if i<=9 else 'intermediate' if i<=12 else 'exam'}

def option(n,i,variant,prefix):
    scene=case(n,i,variant);choices=[scene['answer'],*scene['wrong']];position=i%4
    choices=choices[-position:]+choices[:-position] if position else choices
    return {'id':f'g10-stat-l{n:02}-{prefix}{i:02}','prompt':scene['problem'],'options':choices,'answer_index':position,
      'memo':' '.join(scene['actions']),'source':f'grade10-stat-lesson-{n:02}.md'}

def build():
    DOC.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True);manifest=[]
    for n,title in TITLES.items():
        worked=[{k:v for k,v in case(n,i).items() if k!='wrong'} for i in range(1,16)]
        data={'source':f'grade10-stat-lesson-{n:02}.md','worked':worked,'practice':[option(n,i,1,'p') for i in range(1,16)],
              'mastery':[option(n,i+15,2,'m') for i in range(1,6)],'reassessment':[option(n,i+20,3,'r') for i in range(1,4)]}
        assert len({q['problem'] for q in worked})>=10
        lines=[f'# Grade 10 Topic 7 · Lesson {n}: {title}',f'Authority: [DBE Grade 10 Mathematics ATP]({ATP}), Term 3 Statistics. All questions are original Athena examples.',
               'Status: teacher and live browser review required. Quartiles use the median-of-halves convention.']
        for scene in worked:lines += [f'## {scene["id"]}: {scene["problem"]}',f'Visual contract: {json.dumps(scene["visual"],ensure_ascii=False)}',
           *[f'{j}. {a}' for j,a in enumerate(scene['actions'],1)],f'**Answer:** {scene["answer"]}. **Misconception:** {scene["misconception"]}']
        for label,key in [('Practice','practice'),('Mastery','mastery'),('Parallel reassessment','reassessment')]:
            lines.append(f'## {label} answer key')
            for item in data[key]:lines.append(f'- {item["id"]}: {item["prompt"]} Options: {" | ".join(item["options"])}. Correct: {item["options"][item["answer_index"]]}. {item["memo"]}')
        source=DOC/data['source'];source.write_text('\n\n'.join(lines)+'\n',encoding='utf-8')
        (OUT/f'statistics_{n:02}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        manifest.append({'lesson_id':f'g10-stat-{n:02}','source':source.name,'source_sha256':sha256(source.read_bytes()).hexdigest(),
           'worked':15,'practice':15,'mastery':5,'reassessment':3,'status':'teacher_review_required','teacher_approved':False,'browser_accepted':False})
    (DOC/'topic07-acceptance-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    (DOC/'topic07-batch-acceptance.md').write_text(f'# Grade 10 Topic 7: Statistics\n\n[DBE Grade 10 ATP]({ATP}) Term 3: centre of raw and grouped data, quartiles, five-number summaries, box plots, histograms and contextual comparisons. The ATP also schedules a short 2D trigonometry block before Statistics, already represented by Topic 3 Lesson 5; revisit its depth in teacher review. Six lessons have 90 worked, 90 four-choice practice, 30 mastery and 18 reassessment questions. Teacher and browser acceptance pending.\n',encoding='utf-8')
if __name__=='__main__':build()
