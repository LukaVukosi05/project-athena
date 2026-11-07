"""Author original Grade 9 equations examples and independent changed-value MCQs."""
import json
from hashlib import sha256
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/curriculum/grade9/algebraic-equations'
OUT=ROOT/'backend/app/curriculum/grade9/generated'
ATP='https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2026%20ATPs/2026_ATP_Mathematics_Grade%209.pdf'
TITLES={1:'Translate situations into equations',2:'Solve using inverse operations',
        3:'Brackets and unknowns on both sides',4:'Solve equations using exponent laws',
        5:'Factorisation and the zero-product property',6:'Substitution tables and first-error repair'}

def signed(n):return f'+ {n}' if n>=0 else f'− {-n}'
def roots(a,b):return f'x = {a} or x = {b}' if a!=b else f'x = {a}'

def case(number,index,variant=0):
    assert 1<=number<=6 and 1<=index<=23 and 0<=variant<=3
    seed=index+23*variant
    solution=2+seed%13 if number==1 or seed%4 else -(2+seed%8)
    multiplier=2+seed%5
    offset=3+seed%9
    name=('A school club','A taxi group','A study group','A library')[seed%4]
    if number==1:
        total=multiplier*solution+offset
        prompt=f'{name} has {multiplier} equal groups of learners and {offset} helpers, {total} people altogether. Let x be the number in each group. Form an equation and find x.'
        actions=[f'Draw {multiplier} equal group boxes labelled x and a separate box of {offset} helpers.',
                 f'The total gives {multiplier}x + {offset} = {total}.',
                 f'Subtract {offset} from both sides: {multiplier}x = {total-offset}.',
                 f'Divide both sides by {multiplier}: x = {solution}.',
                 f'Check: {multiplier}({solution}) + {offset} = {total}.']
        answer=f'x = {solution} learners per group';givens=[str(multiplier),str(offset),str(total)];family='groups'
        values={'multiplier':multiplier,'offset':offset,'total':total,'solution':solution}
        misconception='Keep helpers outside the equal groups; the unknown counts one group.'
    elif number==2:
        total=multiplier*solution+offset
        prompt=f'Solve {multiplier}x {signed(offset)} = {total}, showing the same inverse operation on both sides.'
        actions=[f'Start with {multiplier}x + {offset} = {total}; locate the term containing x.',
                 f'Subtract {offset} from both sides: {multiplier}x = {total-offset}.',
                 f'Divide both sides by {multiplier}: x = {solution}.',
                 f'Check: {multiplier}({solution}) + {offset} = {total}.']
        answer=f'x = {solution}';givens=[f'{multiplier}x',f'+ {offset}',str(total)];family='balance'
        values={'multiplier':multiplier,'offset':offset,'total':total,'solution':solution}
        misconception='Change both sides when removing an added term; divide the entire remaining side.'
    elif number==3:
        other=multiplier+1+seed%3
        right=multiplier*(solution+offset)-other*solution
        prompt=f'Solve {multiplier}(x + {offset}) = {other}x {signed(right)}.'
        actions=[f'Expand the left bracket: {multiplier}x + {multiplier*offset} = {other}x {signed(right)}.',
                 f'Subtract {multiplier}x from both sides: {multiplier*offset} = {other-multiplier}x {signed(right)}.',
                 f'Subtract {right} from both sides: {multiplier*offset-right} = {other-multiplier}x.',
                 f'Divide by {other-multiplier}: x = {solution}.',
                 f'Check: {multiplier}({solution}+{offset}) = {multiplier*(solution+offset)} and {other}({solution}) {signed(right)} = {multiplier*(solution+offset)}.']
        answer=f'x = {solution}';givens=[f'{multiplier}(x+{offset})',f'{other}x {signed(right)}'];family='brackets'
        values={'multiplier':multiplier,'offset':offset,'other':other,'right':right,'solution':solution}
        misconception='Distribute to every bracket term; moving an x term means changing both sides.'
    elif number==4:
        base=2+seed%4;left=2+seed%5;power=left+2+seed//5
        solution=power-left
        prompt=f'Solve {base}^(x + {left}) = {base}^{power} using equal bases. Verify the exponent.'
        actions=[f'Both sides have the same positive base {base}, which is not 1.',
                 f'Equate exponents: x + {left} = {power}.',
                 f'Subtract {left} on both sides: x = {power-left}.',
                 f'Check: {base}^({solution}+{left}) = {base}^{power}.']
        answer=f'x = {solution}';givens=[str(base),f'x+{left}',str(power)];family='powers'
        values={'base':base,'left':left,'power':power,'solution':solution}
        misconception='Equal bases permit comparing exponents; do not equate an exponent with the whole power.'
    elif number==5:
        first=1+seed;second=-(2+seed%7)
        if first==second:second-=1
        expanded=index>=8 and variant==0
        middle=-second-first;constant=first*second
        expression=f'x² {signed(middle)}x {signed(constant)} = 0'
        prompt=(f'Factorise and solve {expression}. Give every solution.' if expanded else
            f'Solve (x − {first})(x + {-second}) = 0. Give every solution and check the zero-product rule.')
        actions=([f'Find two integers with product {constant} and sum {middle}: {-first} and {-second}.',
                  f'Factorise: {expression} becomes (x − {first})(x + {-second}) = 0.'] if expanded else [])+[
                 f'The product is zero, so at least one factor must equal zero.',
                 f'First factor: x − {first} = 0, therefore x = {first}.',
                 f'Second factor: x + {-second} = 0, therefore x = {second}.',
                 f'Check: ({first} − {first})({first} + {-second}) = 0 and ({second} − {first})({second} + {-second}) = 0.']
        answer=roots(first,second);givens=[f'x − {first}',f'x + {-second}','0'];family='zero_product'
        values={'first':first,'second':second,'expanded':expanded,'middle':middle,'constant':constant}
        misconception='Set each factor equal to zero; do not divide by a possibly zero factor or omit a root.'
    else:
        input_one=1+seed%4;input_two=input_one+2
        out_one=multiplier*input_one+offset;out_two=multiplier*input_two+offset
        requested=solution
        target=multiplier*requested+offset
        prompt=f'The rule is y = {multiplier}x + {offset}. Complete the outputs for x = {input_one} and x = {input_two}, then find x when y = {target}.'
        diagnostic=index>=11 and variant==0
        if diagnostic:
            prompt+=f' A learner pairs ({input_one}, {out_two}); identify the first error before solving.'
        actions=[f'Keep the ordered-pair columns aligned: inputs {input_one}, {input_two} and the unknown input.',
                 f'For x = {input_one}, y = {multiplier}({input_one}) + {offset} = {out_one}; write ({input_one}, {out_one}).',
                 f'For x = {input_two}, y = {multiplier}({input_two}) + {offset} = {out_two}; write ({input_two}, {out_two}).',
                 f'For y = {target}, solve {multiplier}x + {offset} = {target}: x = {requested}.',
                 f'Check: {multiplier}({requested}) + {offset} = {target}; the ordered pair is ({requested}, {target}).']
        if diagnostic:
            actions.insert(1,f'The claimed pair ({input_one}, {out_two}) uses the output for x = {input_two}; its first error is mismatching the input row.')
        answer=f'x = {requested}';givens=[f'y = {multiplier}x + {offset}',str(input_one),str(input_two),str(target)];family='table'
        values={'multiplier':multiplier,'offset':offset,'input_one':input_one,'input_two':input_two,
                'out_one':out_one,'out_two':out_two,'target':target,'solution':requested,'diagnostic':diagnostic}
        misconception='The ordered pair is (input, output); inverse lookup must undo the addition before division.'
    check=actions[-1]
    return {'id':f'g9-eq-l{number:02}-w{index:02}' if variant==0 else f'g9-eq-l{number:02}-v{variant}-w{index:02}',
            'problem':prompt,'actions':actions,'answer':answer,'check':check,'misconception':misconception,
            'visual':{'family':family,'givens':givens,'values':values},'lesson':number}

def choice_bank(number,index,variant,prefix):
    item=case(number,index,variant)
    answer=item['answer'];v=item['visual']['values']
    if number==5:
        wrong=[f'x = {v["first"]}',f'x = {v["second"]}',roots(-v['first'],-v['second'])]
    else:
        n=v['solution'];wrong=[f'x = {n+1}',f'x = {n-1}',f'x = {-n if n else n+2}']
        if number==1:wrong=[f'x = {n+1} learners per group',f'x = {n-1} learners per group',f'x = {-n} learners per group']
    options=[answer,*wrong]
    if len(set(options))!=4:
        wrong[-1]=f'x = {v.get("solution",v.get("first"))+9}' + (' learners per group' if number==1 else '')
        options=[answer,*wrong]
    assert len(set(options))==4,(number,index,options)
    correct=index%4
    options=options[4-correct:]+options[:4-correct] if correct else options
    assert options.index(answer)==correct
    return {'id':f'g9-eq-l{number:02}-{prefix}{index:02}','prompt':item['problem'],'options':options,
            'answer_index':correct,'memo':'. '.join(item['actions']),'source':f'lesson-{number:02}.md'}

def build():
    DOC.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    manifest=[]
    for number,title in TITLES.items():
        worked=[{**case(number,index),'difficulty':'foundation' if index<=2 else 'easy' if index<=5 else 'standard' if index<=9 else 'intermediate' if index<=12 else 'exam'} for index in range(1,16)]
        assert len({w['problem'] for w in worked})==15
        data={'source':f'lesson-{number:02}.md','worked':worked,
              'practice':[choice_bank(number,i,1,'p') for i in range(1,16)],
              'mastery':[choice_bank(number,i+15,2,'m') for i in range(1,6)],
              'reassessment':[choice_bank(number,i+18,3,'r') for i in range(1,4)]}
        lines=[f'# Grade 9 Topic 7 · Lesson {number}: {title}',f'Authority: [DBE 2026 Mathematics Grade 9 ATP]({ATP}), Term 2. Questions and scenarios are original Athena content.',
               'Status: teacher and browser review required. Worked examples show each intermediate equality and a substitution check. Practice is independent and four-option.']
        for item in worked:
            lines.extend([f'## {item["id"]}: {item["problem"]}',*[f'{j}. {a}' for j,a in enumerate(item['actions'],1)],
                          f'**Answer:** {item["answer"]}. **Misconception:** {item["misconception"]}'])
        for label,key in [('Practice','practice'),('Mastery','mastery'),('Changed-value reassessment','reassessment')]:
            lines.append(f'## {label} answer key')
            for item in data[key]:lines.append(f'- {item["id"]}: {item["prompt"]} Options: {" | ".join(item["options"])}. Correct: {item["options"][item["answer_index"]]}. {item["memo"]}')
        (DOC/f'lesson-{number:02}.md').write_text('\n\n'.join(lines)+'\n',encoding='utf-8')
        (OUT/f'equations_{number:02}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        manifest.append({'lesson_id':f'g9-equations-{number:02}','source':data['source'],
            'source_sha256':sha256((DOC/data['source']).read_bytes()).hexdigest(),
            'worked':15,'practice':15,'mastery':5,'reassessment':3,
            'status':'teacher_review_required','teacher_approved':False,'browser_accepted':False})
    (DOC/'topic7-acceptance-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    (DOC/'topic7-batch-acceptance.md').write_text('''# Grade 9 Topic 7: Algebraic Equations

Authority: [DBE 2026 Grade 9 Mathematics ATP, Term 2]('''+ATP+'''). Athena's six-lesson breakdown and examples are original product decisions.

| Lesson | Focus | Question-owned visual |
|---|---|---|
| 1 | Situations to equations | Equal group boxes and separate helpers |
| 2 | Inverse operations | Both sides of an equality |
| 3 | Brackets and unknowns on both sides | Expansion and equivalent sides |
| 4 | Exponent equations | Matching bases and exponent equality |
| 5 | Factorisation and zero product | Factor branches, with later expanded quadratics |
| 6 | Substitution tables and diagnosis | Ordered input/output rows and first mismatch |

Each lesson has 15 worked examples, 15 distinct four-choice practice items, five mastery items and three changed-value reassessments. The scene data drives each diagram and stages the intermediate equalities. Previews hide the answer, actions and visual solution data; full steps load through the reveal endpoint.

**Status:** authored preview, `release_approved=false`. Backend arithmetic and API tests and frontend renderer tests are required. A Grade 9 Mathematics teacher must review the language, factorisation scope, item difficulty and distractors. Desktop and mobile browser acceptance must check at least four examples per lesson, every step, written solution persistence, replay, navigation, MCQ gates, and clipping before learner release. Do not claim learning outcomes from structural tests.
''',encoding='utf-8')

if __name__=='__main__':build()
