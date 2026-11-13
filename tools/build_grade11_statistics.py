"""Original Grade 11 Statistics examples, answers and review keys."""
from __future__ import annotations

import json
import math
from hashlib import sha256
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/curriculum/grade11/statistics'
OUT=ROOT/'backend/app/curriculum/grade11/generated'
ATP='https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2023%20ATPs/FET%20Content%20Subjects/Grade%2011/1.590%20ATP%202023-24%20Gr%2011%20Maths%20final.pdf'
CAPS='https://www.education.gov.za/Portals/0/CD/National%20Curriculum%20Statements%20and%20Vocational/CAPS%20FET%20_%20MATHEMATICS%20_%20GR%2010-12%20_%20Web_1133.pdf'
TITLES={1:'Mean and central tendency in grouped and ungrouped data',
        2:'Quartiles, five-number summaries and box plots',
        3:'Histograms and frequency polygons',
        4:'Cumulative frequency curves and ogives',
        5:'Variance and standard deviation of ungrouped data',
        6:'Skewness, spread and outlier decisions',
        7:'Scatterplots and suitable models'}
DIFF=['foundation']*2+['easy']*3+['standard']*4+['intermediate']*3+['exam']*3
def avg(xs):return sum(xs)/len(xs)
def quartiles(xs):
    x=sorted(xs);assert len(x)%2==1
    h=len(x)//2
    return x[0],(x[(h-1)//2]+x[h//2])/2,x[h],(x[h+1+(h-1)//2]+x[h+1+h//2])/2,x[-1]
def fmt(x):return f'{x:.2f}'
def choose(answer,wrong):
    seen=[]
    for candidate in wrong:
        if candidate!=answer and candidate not in seen:seen.append(candidate)
    assert len(seen)>=3,(answer,wrong)
    return seen[:3]

def case(n,i,variant=0):
    t=i+15*variant
    if n==1:
        if i<=3 and variant==0:
            x=[8+t,11+t,11+t,15+t,18+t,20+t,23+t]
            mean=avg(x);answer=f'Mean = {fmt(mean)}'
            problem=f'The seven daily study times (minutes) are {", ".join(map(str,x))}. Find the mean to two decimals.'
            steps=[f'Arrange the seven given times and count n = {len(x)}.',
                   f'Add every value: Σx = {sum(x)} minutes.',
                   f'Use mean = Σx/n = {sum(x)}/{len(x)}.',
                   f'Divide: mean = {fmt(mean)} minutes.',
                   f'Answer: {answer}. Check the mean lies between {min(x)} and {max(x)} minutes.']
            wrong=[f'Mean = {fmt(sum(x)/6)}',f'Mean = {fmt(x[len(x)//2])}',f'Mean = {fmt(mean+1)}']
            v={'mode':'ungrouped','data':x,'sum':sum(x),'mean':mean}
        else:
            start=10+5*(t%5);width=10;freq=[3+t%3,5+(t*2)%4,8+(t*3)%5,6+(t*5)%4,2+(t*7)%4]
            mids=[start+5+width*j for j in range(5)]
            total=sum(freq);weighted=sum(a*b for a,b in zip(mids,freq));mean=weighted/total
            answer=f'Estimated mean = {fmt(mean)}'
            label='travel times' if t%2 else 'test scores'
            problem=f'A frequency table for {label} has intervals '
            problem+=', '.join(f'{start+width*j}≤x<{start+width*(j+1)}: {f}' for j,f in enumerate(freq))
            problem+='. Estimate the mean to two decimals using class midpoints.'
            steps=[f'Copy the five {width}-wide classes and their frequencies {freq}; total N = {total}.',
                   f'Mark each class midpoint: {mids}.',
                   f'Multiply midpoint × frequency in each class and sum: Σ(fm) = {weighted}.',
                   f'Estimate x̄ = Σ(fm)/Σf = {weighted}/{total} = {fmt(mean)}.',
                   f'Answer: {answer}. The result lies within the interval {start} to {start+50}; grouped values give an estimate.']
            wrong=[f'Estimated mean = {fmt(mean+1.5)}',f'Estimated mean = {fmt(weighted/(total+5))}',f'Estimated mean = {fmt(mean+width/2)}']
            v={'mode':'grouped','start':start,'width':width,'frequencies':freq,'midpoints':mids,'total':total,'weighted':weighted,'mean':mean}
    elif n==2:
        base=4+(t%13);delta=[2+(t%3),3+(t*2)%4,2+(t*3)%3,3+(t*5)%4,
               3+(t*7)%5,2+(t*11)%3,3+(t*13)%5,2+(t*17)%4]
        x=[base]
        for d in delta:x.append(x[-1]+d)
        minimum,q1,med,q3,maximum=quartiles(x);iqr=q3-q1
        answer=f'Five-number summary = ({minimum}, {q1:g}, {med}, {q3:g}, {maximum}); IQR = {iqr:g}'
        problem=f'The nine ordered measurements are {", ".join(map(str,x))}. Give the five-number summary and IQR.'
        steps=[f'Plot the nine observations in order: {x}.',
               f'Mark the median, fifth value = {med}; split the remaining values into lower and upper halves.',
               f'Lower half {x[:4]} gives Q1 = {q1:g}; upper half {x[5:]} gives Q3 = {q3:g}.',
               f'Mark whiskers at {minimum} and {maximum}, box from {q1:g} to {q3:g}, median line at {med}.',
               f'Answer: {answer}. Check IQR = Q3 − Q1 = {q3:g} − {q1:g} = {iqr:g}.']
        wrong=[f'Five-number summary = ({minimum}, {x[2]}, {med}, {x[6]}, {maximum}); IQR = {x[6]-x[2]}',
               f'Five-number summary = ({minimum}, {q1:g}, {med}, {q3:g}, {maximum}); IQR = {maximum-minimum}',
               f'Five-number summary = ({minimum}, {q1:g}, {med}, {q3:g}, {maximum}); IQR = {iqr+1:g}']
        v={'mode':'box','data':x,'five':[minimum,q1,med,q3,maximum],'iqr':iqr}
    elif n==3:
        start=5*(t%6);width=10;freq=[3+t%4,5+(t*2)%5,10+(t*3)%6,6+(t*5)%4,2+(t*7)%4]
        upper=start+50;peak=max(freq);index=freq.index(peak);lo=start+width*index;hi=lo+width
        answer=f'Modal interval = {lo}≤x<{hi}'
        problem=f'A grouped survey uses equal-width intervals from {start}≤x<{start+10} through {upper-10}≤x<{upper}. Frequencies in order: {freq}. Draw a histogram and frequency polygon; identify the modal interval.'
        steps=[f'The class boundaries {list(range(start,upper+1,width))} define the horizontal positions; each frequency determines a bar height.',
               f'Draw five touching histogram bars of width {width}, heights {freq}.',
               f'Mark the midpoint of each bar top at {[start+5+j*width for j in range(5)]}.',
               f'Join the midpoint points to form the frequency polygon; the largest frequency is {peak}.',
               f'Answer: {answer}, because its bar and polygon peak have frequency {peak}.']
        wrong=[f'Modal interval = {start}≤x<{start+10}',f'Modal interval = {lo+width}≤x<{hi+width}',
               f'Modal interval = {start+width*(index-1)}≤x<{lo}']
        v={'mode':'histogram','start':start,'width':width,'frequencies':freq,'peak':index}
    elif n==4:
        start=10*(t%4);width=10;freq=[2+t%4,4+(t*2)%5,7+(t*3)%6,6+(t*5)%5,3+(t*7)%4]
        if sum(freq)%2==0:freq[-1]+=1  # An unambiguous middle observation for every teaching example.
        cumsum=[0]
        for count in freq:cumsum.append(cumsum[-1]+count)
        N=cumsum[-1];threshold=(N+1)//2;idx=next(j for j in range(5) if cumsum[j]<threshold<=cumsum[j+1]);lo=start+idx*width
        answer=f'Median class = {lo}≤x<{lo+width}'
        problem=f'A grouped distribution has class boundaries {list(range(start,start+51,10))} and frequencies {freq}. Draw its less-than ogive and find the class containing the median observation.'
        steps=[f'Start cumulative count 0 at the first lower boundary {start}.',
               f'Add the frequencies successively: cumulative counts {cumsum}.',
               f'Plot cumulative count against upper boundaries {list(range(start,start+51,10))}, then join adjacent points.',
               f'N = {N}; the median observation is at position {threshold}, between cumulative counts {cumsum[idx]} and {cumsum[idx+1]}.',
               f'Answer: {answer}. Read the upper boundary at each cumulative value, not the midpoint.']
        wrong=[f'Median class = {start}≤x<{start+10}',f'Median class = {lo+width}≤x<{lo+2*width}',
               f'Median class = {start+10*((idx-1)%5)}≤x<{start+10*((idx-1)%5)+10}']
        v={'mode':'ogive','start':start,'width':width,'frequencies':freq,'cumulative':cumsum,'total':N,'median_class':idx}
    elif n==5:
        base=5+t%9;offset=[0,2+(t%3),4+(t*2)%4,6+(t*3)%5,8+(t*5)%5,11+(t*7)%4]
        x=[base+d for d in offset];mean=avg(x);squares=sum((a-mean)**2 for a in x);var=squares/len(x);sd=math.sqrt(var)
        answer=f'Population variance = {fmt(var)}; standard deviation = {fmt(sd)}'
        problem=f'For the complete set of six recorded values {x}, calculate the population variance and standard deviation to two decimals.'
        steps=[f'Keep all six values {x}; the population size is N = {len(x)}.',
               f'Calculate the unrounded mean: x̄ = {sum(x)}/{len(x)} = {mean:g}.',
               f'Subtract the mean and square each deviation; Σ(x − x̄)² = {squares:.4f}.',
               f'Use population variance σ² = Σ(x − x̄)²/N = {squares:.4f}/{len(x)} = {fmt(var)}.',
               f'Answer: {answer}. Check σ = √({var:.4f}) = {fmt(sd)}; no N−1 sample correction.']
        wrong=[f'Population variance = {fmt(squares/(len(x)-1))}; standard deviation = {fmt(math.sqrt(squares/(len(x)-1)))}',
               f'Population variance = {fmt(var)}; standard deviation = {fmt(var)}',
               f'Population variance = {fmt(sd)}; standard deviation = {fmt(var)}']
        v={'mode':'deviation','data':x,'mean':mean,'squares':squares,'variance':var,'sd':sd}
    elif n==6:
        base=8+t%7;x=[base,base+1,base+2,base+3,base+4,base+6,base+7,base+8,base+26+(t%9)]
        minimum,q1,med,q3,maximum=quartiles(x);iqr=q3-q1;fence=q3+1.5*iqr
        assert maximum>fence and x[-2]<=fence
        answer=f'Upper outlier = {maximum}; right-skewed'
        problem=f'The ordered waiting times are {x}. Use the 1.5×IQR rule to identify outliers and describe the likely skew.'
        steps=[f'Sort the waiting times (already ordered) and mark minimum {minimum}, median {med}, maximum {maximum}.',
               f'Find Q1 = {q1:g}, Q3 = {q3:g}, IQR = {iqr:g}.',
               f'Calculate the upper fence Q3 + 1.5×IQR = {fence:g}; the lower fence is {q1-1.5*iqr:g}.',
               f'The value {maximum} exceeds {fence:g}; the other observations lie inside the fences. The long tail points right.',
               f'Answer: {answer}. Check {maximum} is above the upper fence; do not call every maximum an outlier.']
        wrong=[f'Upper outlier = {maximum}; left-skewed',f'No outlier; right-skewed',f'Upper outlier = {x[-2]}; right-skewed']
        v={'mode':'outlier','data':x,'five':[minimum,q1,med,q3,maximum],'iqr':iqr,'upper_fence':fence}
    else:
        model=['linear','quadratic','exponential'][(t-1)%3];x=list(range(1,7));k=2+(t%3);c=1+t%5
        y=[k*a+c if model=='linear' else a*a+k*a+c if model=='quadratic' else k**a+c for a in x]
        answer=f'Model = {model}'
        problem=f'Scatterplot data, ordered by x: {list(zip(x,y))}. Plot the six points and choose a linear, quadratic or exponential model.'
        differences=[y[j+1]-y[j] for j in range(5)]
        second=[differences[j+1]-differences[j] for j in range(4)]
        evidence=('constant first differences' if model=='linear' else 'constant second differences' if model=='quadratic' else 'a multiplying growth pattern after removing the constant offset')
        steps=[f'The first two ordered pairs {list(zip(x,y))[:2]} anchor the scale; keep the given data table visible.',
               f'The remaining four plotted points make the change between successive y-values visible: {differences}.',
               f'Compute second differences: {second}; compare additive versus multiplicative growth.',
               f'The points show {evidence}; the plotted trend is {model}.',
               f'Answer: {answer}. Check against all six points; extrapolation beyond these values is uncertain.']
        wrong=[f'Model = {name}' for name in ('linear','quadratic','exponential','constant') if name!=model]
        v={'mode':'scatter','x':x,'y':y,'model':model,'first_differences':differences,'second_differences':second}
    wrong=choose(answer,wrong)
    assert len(steps)==5 and answer in steps[-1]
    return {'id':f'g11-stat-l{n:02}-w{i:02}','lesson':n,'problem':problem,'answer':answer,
            'actions':steps,'check':steps[-1],
            'visual':{'family':'grade11_statistics','values':v},'wrong':wrong,'difficulty':DIFF[i-1]}

def build():
    DOC.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True);manifest=[]
    for n,title in TITLES.items():
        worked=[{k:v for k,v in case(n,i).items() if k!='wrong'} for i in range(1,16)]
        assert len({q['problem'] for q in worked})==15
        data={'source':f'grade11-stat-lesson-{n:02}.md','worked':worked}
        for section,count,variant,prefix in [('practice',15,1,'p'),('mastery',5,2,'m'),('reassessment',3,3,'r')]:
            bank=[]
            for i in range(1,count+1):
                c=case(n,i,variant);options=[c['answer'],*c['wrong']];shift=(i+variant)%4
                options=options[shift:]+options[:shift]
                bank.append({'id':f'g11-stat-l{n:02}-{prefix}{i:02}','prompt':c['problem'],
                             'options':options,'answer_index':options.index(c['answer']),
                             'actions':c['actions'],'memo':' '.join(c['actions'])})
            data[section]=bank
        lines=[f'# Grade 11 Topic 8, Lesson {n}: {title}',
               f'Scope: [DBE Grade 11 ATP, Term 3]({ATP}). Scatterplots additionally follow [Mathematics CAPS]({CAPS}).',
               'Original Athena questions; teacher review and live browser acceptance are still required.',
               'Convention: quartiles use medians of the lower/upper halves, excluding the median of an odd-sized set. Variance uses population N (the complete observed set). Grouped mean is an estimate from class midpoints.']
        for q in worked:
            lines.extend([f'## {q["id"]}: {q["problem"]}',
                          f'Visual values: `{json.dumps(q["visual"],ensure_ascii=False)}`',
                          *[f'{j}. {step}' for j,step in enumerate(q['actions'],1)],
                          f'Answer: {q["answer"]}. Check: {q["check"]}'])
        for section in ('practice','mastery','reassessment'):
            lines.append(f'## {section.title()} answer key')
            for item in data[section]:
                lines.append(f'- {item["id"]}: {item["prompt"]} Options: {" | ".join(item["options"])}. '
                             f'Correct: {item["options"][item["answer_index"]]}. {item["memo"]}')
        source=DOC/data['source'];source.write_text('\n\n'.join(lines)+'\n',encoding='utf-8')
        (OUT/f'statistics_{n:02}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        manifest.append({'lesson_id':f'g11-stat-{n:02}','source':source.name,
                         'source_sha256':sha256(source.read_bytes()).hexdigest(),
                         'worked':15,'practice':15,'mastery':5,'reassessment':3,
                         'status':'teacher_review_required','teacher_approved':False,'browser_accepted':False})
    (DOC/'topic8-acceptance-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':build()
