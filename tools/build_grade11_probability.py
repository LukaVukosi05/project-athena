"""Author original Grade 11 Probability questions and their independent keys."""
from __future__ import annotations

import json
from fractions import Fraction
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / 'docs/curriculum/grade11/probability'
OUT = ROOT / 'backend/app/curriculum/grade11/generated'
ATP = 'https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2023%20ATPs/FET%20Content%20Subjects/Grade%2011/1.590%20ATP%202023-24%20Gr%2011%20Maths%20final.pdf'
CAPS = 'https://www.education.gov.za/Portals/0/CD/National%20Curriculum%20Statements%20and%20Vocational/CAPS%20FET%20_%20MATHEMATICS%20_%20GR%2010-12%20_%20Web_1133.pdf'
TITLES = {
    1: 'Relative frequency and theoretical probability',
    2: 'Two-event Venn diagrams, unions and complements',
    3: 'Independent and dependent events',
    4: 'Three-event Venn diagrams and inclusion-exclusion',
    5: 'Tree diagrams with and without replacement',
    6: 'Contingency tables and conditional comparisons',
    7: 'Mixed probability problems and first-error diagnosis',
}
DIFFICULTY = ['foundation']*2 + ['easy']*3 + ['standard']*4 + ['intermediate']*3 + ['exam']*3


def ratio(a, b):
    value = Fraction(a, b)
    return f'{value.numerator}/{value.denominator}' if value.denominator != 1 else str(value.numerator)


def question(n: int, i: int, variant: int = 0) -> dict:
    t = i + 15*variant
    if n == 1:
        # A bag is sampled with replacement: compare observed frequency to the fixed model.
        red, blue = 2 + t%6, 3 + (2*t)%7
        trials = 40 + 10*(t%4)
        observed = max(1, min(trials-1, round(trials*red/(red+blue)) + (t%5-2)))
        answer = f'Theoretical P(red) = {ratio(red, red+blue)}'
        problem = f'A bag contains {red} red and {blue} blue counters. A counter is drawn, replaced and the bag mixed {trials} times; red occurs {observed} times. Give theoretical P(red) and compare it with relative frequency.'
        steps = [f'The bag has {red} + {blue} = {red+blue} equally likely counters.',
                 f'There are {red} favourable red counters, so theoretical P(red) = {red}/{red+blue}.',
                 f'Simplify the theoretical fraction to {ratio(red,red+blue)}.',
                 f'Experimental relative frequency is {observed}/{trials} = {observed/trials:.3f}; replacement keeps the theoretical ratio fixed.',
                 f'Answer: {answer}. Compare {red/(red+blue):.3f} with {observed/trials:.3f}; experimental values can differ in a finite sample.']
        wrong = [f'Theoretical P(red) = {ratio(blue,red+blue)}',f'Theoretical P(red) = {ratio(red,trials)}',f'Theoretical P(red) = {ratio(observed,trials)}']
        v = dict(mode='frequency',red=red,blue=blue,trials=trials,observed=observed)
    elif n == 2:
        both, aonly, bonly, neither = 2+t%6, 6+t%8, 4+(2*t)%7, 3+(3*t)%6
        total = both+aonly+bonly+neither
        target = ['union','complement','intersection'][t%3]
        count = {'union':aonly+both+bonly,'complement':bonly+neither,'intersection':both}[target]
        label = {'union':'A or B','complement':'not A','intersection':'A and B'}[target]
        answer = f'P({label}) = {ratio(count,total)}'
        problem = f'In a group of {total}, {aonly} belong to A only, {both} to both A and B, {bonly} to B only and {neither} to neither. Find P({label}).'
        steps = [f'Draw a rectangle with {total} outcomes and two intersecting circles A and B.',
                 f'Put {both} in the overlap, then {aonly} and {bonly} in the outer circle regions; {neither} stays outside.',
                 f'Check {aonly} + {both} + {bonly} + {neither} = {total}.',
                 f'The target {label} contains {count} outcomes; do not double-count the overlap.',
                 f'Answer: {answer}. Check the selected regions total {count} out of {total}.']
        wrong = [f'P({label}) = {ratio(aonly,total)}',f'P({label}) = {ratio(neither,total)}',f'P({label}) = {ratio(total-count,total)}']
        v = dict(mode='venn2',aonly=aonly,both=both,bonly=bonly,neither=neither,target=target)
    elif n == 3:
        # The joint count is independent on alternating questions and altered on the others.
        n_total = 100*(1+t//10)
        a = n_total*(2+t%5)//10;b=n_total*(2+(2*t+1)%5)//10
        expected=a*b//n_total
        joint = expected if t%2 else expected + min(4,a-expected,b-expected)
        assert joint <= min(a,b)
        independent = joint == Fraction(a*b,n_total)
        answer = 'Independent' if independent else 'Dependent'
        problem = f'Among {n_total} equally likely outcomes, {a} are in A, {b} in B and {joint} in both. Decide whether A and B are independent.'
        steps = [f'Use the same sample space of {n_total}; P(A) = {a}/{n_total}, P(B) = {b}/{n_total}.',
                 f'If independent, the product rule requires P(A and B) = {a}/{n_total} × {b}/{n_total} = {ratio(a*b,n_total*n_total)}.',
                 f'The actual overlap is P(A and B) = {joint}/{n_total} = {ratio(joint,n_total)}.',
                 f'Compare the actual joint probability to the product: {ratio(joint,n_total)} {"=" if independent else "≠"} {ratio(a*b,n_total*n_total)}.',
                 f'Answer: {answer}. The product rule {"holds" if independent else "does not hold"}; overlap alone does not imply independence.']
        wrong = ['Independent because the events overlap','Mutually exclusive because they overlap','Dependent because both events are possible'] if independent else ['Independent because the events overlap','Mutually exclusive because the joint count is nonzero','Independent because P(A) and P(B) are known']
        v = dict(mode='independence',total=n_total,a=a,b=b,both=joint)
    elif n == 4:
        abc=1+t%4;ab=2+(2*t)%5;ac=1+(3*t)%5;bc=2+(5*t)%5
        aonly=3+t%7;bonly=4+(2*t)%6;conly=3+(3*t)%6;outside=2+t%6
        parts = [aonly,bonly,conly,ab,ac,bc,abc,outside]
        total=sum(parts);target=['exactly one','at least two','A or B or C'][t%3]
        count={'exactly one':aonly+bonly+conly,'at least two':ab+ac+bc+abc,'A or B or C':total-outside}[target]
        answer=f'P({target}) = {ratio(count,total)}'
        problem=f'A three-set survey has regions A only {aonly}, B only {bonly}, C only {conly}, AB only {ab}, AC only {ac}, BC only {bc}, ABC {abc} and neither {outside}. Find P({target}).'
        steps=[f'Draw three labelled intersecting sets and put {abc} in the triple overlap first.',
               f'Fill the pair-only regions AB={ab}, AC={ac}, BC={bc}; keep these separate from the triple overlap.',
               f'Fill single-only regions A={aonly}, B={bonly}, C={conly}, then put {outside} outside all sets.',
               f'Add all eight disjoint regions to get {total}; the regions for {target} total {count}.',
               f'Answer: {answer}. Each counted outcome occupies exactly one disjoint region.']
        wrong=[f'P({target}) = {ratio(count+abc,total)}',f'P({target}) = {ratio(total-count,total)}',f'P({target}) = {ratio(count-abc,total)}']
        v=dict(mode='venn3',aonly=aonly,bonly=bonly,conly=conly,ab=ab,ac=ac,bc=bc,abc=abc,outside=outside,target=target)
    elif n == 5:
        red,blue=3+t%6+6*(t//6),4+(2*t)%6
        replacement=t%4==0
        target=['two red','one of each','at least one red'][t%3]
        den2=red+blue if replacement else red+blue-1
        rr=Fraction(red,red+blue)*Fraction(red if replacement else red-1,den2)
        rb=Fraction(red,red+blue)*Fraction(blue,den2)
        br=Fraction(blue,red+blue)*Fraction(red,den2)
        result={'two red':rr,'one of each':rb+br,'at least one red':rr+rb+br}[target]
        answer=f'P({target}) = {ratio(result.numerator,result.denominator)}'
        method='with replacement' if replacement else 'without replacement'
        problem=f'A bag holds {red} red and {blue} blue counters. Draw two {method}. Find the probability of {target}.'
        steps=[f'The first branches are red {red}/{red+blue} and blue {blue}/{red+blue}.',
               f'After a red first: P(red second) = {red if replacement else red-1}/{den2}; P(blue second) = {blue}/{den2}.',
               f'After a blue first: P(red second) = {red}/{den2}; P(blue second) = {blue if replacement else blue-1}/{den2}.',
               f'Multiply each required branch: RR={ratio(rr.numerator,rr.denominator)}, RB={ratio(rb.numerator,rb.denominator)}, BR={ratio(br.numerator,br.denominator)}.',
               f'Answer: {answer}. {"Replacement restores the starting total" if replacement else "The second draw has one fewer counter"}; add disjoint branches only.']
        wrong=[f'P({target}) = {ratio(rr.numerator,rr.denominator)}',f'P({target}) = {ratio(rb.numerator,rb.denominator)}',f'P({target}) = {ratio(br.numerator,br.denominator)}']
        v=dict(mode='tree',red=red,blue=blue,replacement=replacement,target=target)
    elif n == 6:
        a1,b1,a2,b2=4+t%8,3+(2*t)%6,5+(3*t)%8,2+(5*t)%7
        target=['A and X','first row given second column','first column given first row'][t%3]
        if target=='A and X':count,den=a1,a1+b1+a2+b2
        elif target=='first row given second column':count,den=b1,b1+b2
        else:count,den=a1,a1+b1
        answer=f'P({target}) = {ratio(count,den)}'
        problem=f'A two-way table counts {a1} in row A/column X, {b1} in A/Y, {a2} in B/X and {b2} in B/Y. Find P({target}).'
        steps=[f'Build the two-by-two table with the four cells {a1}, {b1}, {a2}, {b2}.',
               f'Row totals are {a1+b1} and {a2+b2}; column totals are {a1+a2} and {b1+b2}.',
               f'The grand total is {a1+b1+a2+b2}; the specified group has {den} outcomes.',
               f'The favourable cell contains {count}; use denominator {den}, so P = {count}/{den}.',
               f'Answer: {answer}. Check the denominator belongs to the given group, not automatically the whole table.']
        wrong=[f'P({target}) = {ratio(count,a1+b1+a2+b2)}',f'P({target}) = {ratio(count+1,den)}',f'P({target}) = {ratio(den-count,den)}']
        v=dict(mode='table',cells=[a1,b1,a2,b2],target=target)
    else:
        # Mixed review, with different representations and explicitly checked first errors.
        family=['venn','tree','table'][t%3]
        if family=='venn':
            aonly,both,bonly,neither=3+t%5,2+t%4,4+t%6,2+t%3
            total=aonly+both+bonly+neither;correct=aonly+both+bonly;incorrect=aonly+bonly+2*both
            answer=f'P(A or B) = {ratio(correct,total)}'
            problem=f'A={aonly+both}, B={bonly+both}, both={both}, neither={neither} in a group of {total}. A learner claims P(A or B)={incorrect}/{total}. Find and repair the first error.'
            steps=[f'Draw the overlap {both} once, with A only {aonly} and B only {bonly}.',
                   f'The learner added A and B and counted their shared {both} twice.',
                   f'Subtract the overlap: |A or B| = {aonly+both} + {bonly+both} − {both} = {correct}.',
                   f'Check {correct} + neither {neither} = {total}.',f'Answer: {answer}. The first error was double-counting the overlap.']
            wrong=[f'P(A or B) = {ratio(incorrect,total)}',f'P(A or B) = {ratio(aonly+bonly,total)}',f'P(A or B) = {ratio(total-correct,total)}']
            v=dict(mode='venn2',aonly=aonly,both=both,bonly=bonly,neither=neither,target='union')
        elif family=='tree':
            red,blue=3+t%5,4+(2*t)%5;total=red+blue
            result=Fraction(red,total)*Fraction(red-1,total-1)
            answer=f'P(two red) = {ratio(result.numerator,result.denominator)}'
            problem=f'A bag has {red} red and {blue} blue counters. Two are drawn without replacement. A learner uses ({red}/{total}) × ({red}/{total}) for two red. Find the first error and the correct result.'
            steps=[f'The first red branch has probability {red}/{total}.',
                   f'The learner wrongly reused the original bag after removing a red counter.',
                   f'The second red branch is ({red}-1)/({total}-1) = {red-1}/{total-1}.',
                   f'Multiply {red}/{total} × {red-1}/{total-1} = {answer.split(" = ")[1]}.',
                   f'Answer: {answer}. Check the second draw has {total-1} counters.']
            wrong=[f'P(two red) = {ratio(red*red,total*total)}',f'P(two red) = {ratio(red-1,total-1)}',f'P(two red) = {ratio(red*blue,total*(total-1))}']
            v=dict(mode='tree',red=red,blue=blue,replacement=False,target='two red')
        else:
            a1,b1,a2,b2=4+t%7,3+t%5,5+t%6,2+t%4;total=a1+b1+a2+b2
            answer=f'P(A given Y) = {ratio(b1,b1+b2)}'
            problem=f'A survey table has A/X={a1}, A/Y={b1}, B/X={a2}, B/Y={b2}. A learner claims P(A among Y)={b1}/{total}. Find the first error and correct probability.'
            steps=[f'Locate the Y column: A/Y={b1} and B/Y={b2}.',
                   f'The learner used the grand total {total} even though the selection is restricted to Y.',
                   f'The appropriate denominator is the Y column: {b1}+{b2}={b1+b2}.',
                   f'The favourable cell is {b1} of those {b1+b2} Y outcomes.',
                   f'Answer: {answer}. The first error was using the wrong denominator.']
            wrong=[f'P(A given Y) = {ratio(b1,total)}',f'P(A given Y) = {ratio(a1,a1+a2)}',f'P(A given Y) = {ratio(b2,b1+b2)}']
            v=dict(mode='table',cells=[a1,b1,a2,b2],target='first row given second column')
    # Reject mathematical distractors that accidentally simplify to the right answer.
    unique=[]
    for candidate in wrong:
        if candidate != answer and candidate not in unique: unique.append(candidate)
    for offset in range(1,8):
        if len(unique)>=3:break
        label, result = answer.split(' = ',1)
        value = Fraction(result)
        for candidate_value in (value+Fraction(offset,40),value-Fraction(offset,40)):
            if not 0<=candidate_value<=1:continue
            fallback=f'{label} = {ratio(candidate_value.numerator,candidate_value.denominator)}'
            if fallback!=answer and fallback not in unique:unique.append(fallback)
            if len(unique)>=3:break
    assert len(steps)==5 and len(unique)>=3
    return dict(id=f'g11-prob-l{n:02}-w{i:02}',lesson=n,problem=problem,answer=answer,
                actions=steps,check=steps[-1],visual=dict(family='grade11_probability',values=v),
                difficulty=DIFFICULTY[i-1],wrong=unique[:3])


def build():
    DOC.mkdir(parents=True,exist_ok=True)
    manifest=[]
    for n,title in TITLES.items():
        worked=[{k:v for k,v in question(n,i).items() if k!='wrong'} for i in range(1,16)]
        assert len({q['problem'] for q in worked})==15
        data=dict(source=f'grade11-prob-lesson-{n:02}.md',worked=worked)
        for section,count,variant,prefix in [('practice',15,1,'p'),('mastery',5,2,'m'),('reassessment',3,3,'r')]:
            bank=[]
            for i in range(1,count+1):
                scene=question(n,i,variant)
                options=[scene['answer'],*scene['wrong']]
                offset=(i+variant)%4;options=options[offset:]+options[:offset]
                assert len(set(options))==4
                bank.append(dict(id=f'g11-prob-l{n:02}-{prefix}{i:02}',prompt=scene['problem'],
                                 options=options,answer_index=options.index(scene['answer']),
                                 actions=scene['actions'],memo=' '.join(scene['actions'])))
            data[section]=bank
        lines=[f'# Grade 11 Topic 9, Lesson {n}: {title}',
               f'Curriculum: [DBE Grade 11 ATP]({ATP}) and [Mathematics CAPS]({CAPS}).',
               'Original Athena questions and worked steps; teacher review and live browser acceptance required.',
               'Fraction probabilities are exact and simplified. The tree distinguishes replacement from no replacement.']
        for scene in worked:
            lines.extend([f'## {scene["id"]}: {scene["problem"]}',
                          f'Question-specific visual values: `{json.dumps(scene["visual"],ensure_ascii=False)}`',
                          *[f'{j}. {step}' for j,step in enumerate(scene['actions'],1)],
                          f'Answer: {scene["answer"]}. Check: {scene["check"]}'])
        for section in ('practice','mastery','reassessment'):
            lines.append(f'## {section.title()} key')
            for item in data[section]:
                lines.append(f'- {item["id"]}: {item["prompt"]} Options: {" | ".join(item["options"])}. '
                             f'Correct: {item["options"][item["answer_index"]]}. {item["memo"]}')
        source=DOC/data['source'];source.write_text('\n\n'.join(lines)+'\n',encoding='utf-8')
        (OUT/f'probability_{n:02}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        manifest.append(dict(lesson_id=f'g11-prob-{n:02}',source=source.name,
                             source_sha256=sha256(source.read_bytes()).hexdigest(),worked=15,practice=15,
                             mastery=5,reassessment=3,status='teacher_review_required',
                             teacher_approved=False,browser_accepted=False))
    (DOC/'topic9-acceptance-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':build()
