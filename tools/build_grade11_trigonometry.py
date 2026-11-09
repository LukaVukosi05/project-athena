"""Authored Grade 11 Term 1 trigonometry banks with exact special-angle values."""
from __future__ import annotations

import json
from hashlib import sha256
from math import gcd
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/"docs/curriculum/grade11/trigonometry-reduction"
OUT=ROOT/"backend/app/curriculum/grade11/generated"
ATP="https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2023%20ATPs/FET%20Content%20Subjects/Grade%2011/1.590%20ATP%202023-24%20Gr%2011%20Maths%20final.pdf"
TITLES={
  1:"Derive tangent and the Pythagorean identity",
  2:"Reduce angles around 90 degrees",
  3:"Reduce angles around 180 degrees",
  4:"Reduce 360-degree and negative angles",
  5:"Determine where an identity is defined",
  6:"Write general solutions of trigonometric equations",
  7:"Solve trigonometric equations in an interval",
}
DIFFICULTIES=["foundation"]*2+["easy"]*3+["standard"]*4+["intermediate"]*3+["exam"]*3
EXACT={
  30:{"sin":"1/2","cos":"√3/2","tan":"√3/3","cot":"√3"},
  45:{"sin":"√2/2","cos":"√2/2","tan":"1","cot":"1"},
  60:{"sin":"√3/2","cos":"1/2","tan":"√3","cot":"√3/3"},
}
PERIOD={"sin":360,"cos":360,"tan":180}
FUNCTIONS=("sin","cos","tan")
REFS=(30,45,60)

def negative(value:str)->str:
    return "-"+value if value!="0" else "0"

def fmt_angle(angle:int)->str:
    return f"{angle}°"

def values(fn:str,alpha:int,sign:int)->str:
    value=EXACT[alpha][fn]
    return value if sign>0 else negative(value)

def cycle(index:int,variant:int,size:int)->int:
    return (index-1+variant*7)%size

def steps_and_visual(n:int,i:int,variant:int):
    t=cycle(i,variant,36)
    alpha=REFS[t%3]
    fn=FUNCTIONS[(t//3)%3]
    sign=1 if (t//9)%2==0 else -1
    if n==1:
        triples=((3,4,5),(5,12,13),(8,15,17))
        opp,adj,hyp=triples[(i-1+variant)%3]
        scale=1+(i-1+variant)//3
        opp*=scale;adj*=scale;hyp*=scale
        mode=("tan","cos","identity")[(i-1+variant)%3]
        if mode=="tan":
            problem=f"A right triangle has opposite side {opp}, adjacent side {adj} and hypotenuse {hyp}. Find tan θ from sin θ ÷ cos θ."
            common=gcd(opp,adj);answer=f"{opp//common}/{adj//common}"
            actions=[f"Use the given triangle to read sin θ = {opp}/{hyp}.",
                     f"The same triangle gives cos θ = {adj}/{hyp}.",
                     f"Because cos θ is nonzero, tan θ = sin θ ÷ cos θ.",
                     f"Divide the fractions: ({opp}/{hyp}) ÷ ({adj}/{hyp}) = {opp}/{adj}.",
                     f"Answer: tan θ = {answer}. The opposite-to-adjacent ratio {opp}:{adj} confirms it."]
            wrong=[f"{adj//common}/{opp//common}",f"{opp}/{hyp}",f"{adj}/{hyp}"]
        elif mode=="cos":
            problem=f"A right triangle has opposite side {opp}, adjacent side {adj} and hypotenuse {hyp}. Find cos θ and verify sin² θ + cos² θ = 1."
            common=gcd(adj,hyp);answer=f"{adj//common}/{hyp//common}"
            actions=[f"Mark the side adjacent to θ as {adj} and the hypotenuse as {hyp}.",
                     f"The cosine ratio is adjacent ÷ hypotenuse = {adj}/{hyp}.",
                     f"The sine ratio is opposite ÷ hypotenuse = {opp}/{hyp}.",
                     f"Square both ratios and add: {opp*opp}/{hyp*hyp} + {adj*adj}/{hyp*hyp} = {(opp*opp+adj*adj)}/{hyp*hyp}.",
                     f"Answer: cos θ = {answer}. Since {opp*opp} + {adj*adj} = {hyp*hyp}, sin² θ + cos² θ = 1."]
            wrong=[f"{opp}/{hyp}",f"{adj}/{opp}",f"{hyp}/{adj}"]
        else:
            problem=f"A right triangle has opposite side {opp}, adjacent side {adj} and hypotenuse {hyp}. Evaluate sin² θ + cos² θ exactly."
            answer="1"
            actions=[f"Write sin θ = {opp}/{hyp} from the opposite and hypotenuse.",
                     f"Write cos θ = {adj}/{hyp} from the adjacent and hypotenuse.",
                     f"Square each ratio: sin² θ = {opp*opp}/{hyp*hyp}, cos² θ = {adj*adj}/{hyp*hyp}.",
                     f"Add the numerators: ({opp*opp} + {adj*adj})/{hyp*hyp} = {opp*opp+adj*adj}/{hyp*hyp}.",
                     f"Answer: 1. Pythagoras gives {opp*opp} + {adj*adj} = {hyp*hyp}."]
            wrong=["0","2",f"{opp+adj}/{hyp}"]
        visual={"mode":"triangle","opposite":opp,"adjacent":adj,"hypotenuse":hyp,"task":mode}
    elif n in (2,3,4):
        forms={2:(("90 −",lambda a:90-a),("90 +",lambda a:90+a)),
               3:(("180 −",lambda a:180-a),("180 +",lambda a:180+a)),
               4:(("360 −",lambda a:360-a),("360 +",lambda a:360+a),("−",lambda a:-a))}
        options=forms[n]
        tag,theta_fn=options[(i-1+variant*3)//9%len(options)]
        theta=theta_fn(alpha)
        # Rotate function as well as reference to yield 15 distinct authored prompts.
        fn=FUNCTIONS[((i-1+variant*4)//3)%3]
        quadrant=((theta%360)//90)+1
        if theta%90==0:raise AssertionError("Special reference angle must not land on an axis")
        sign=(-1 if (fn=="sin" and quadrant in (3,4)) or
                     (fn=="cos" and quadrant in (2,3)) or
                     (fn=="tan" and quadrant in (2,4)) else 1)
        cofn={"sin":"cos","cos":"sin","tan":"cot"}[fn] if n==2 else fn
        magnitude=EXACT[alpha][cofn]
        value=magnitude if sign>0 else negative(magnitude)
        problem=f"Find the exact value of {fn}({tag} {alpha}°)."
        answer=value
        actions=[f"Read the angle in degrees: {tag} {alpha}° = {theta}°. Reduce it modulo 360° if necessary.",
                 f"Its terminal arm lies in quadrant {quadrant}. The acute reference angle is {alpha}°.",
                 f"The {fn} ratio is {'positive' if sign>0 else 'negative'} in quadrant {quadrant}.",
                 f"The reference magnitude is {cofn}({alpha}°) = {magnitude}; apply the quadrant sign.",
                 f"Answer: {fn}({tag} {alpha}°) = {value}. Its exact sign and reference ratio agree with the unit circle."]
        wrong=[negative(value) if sign>0 else value[1:],
               values(fn,REFS[(REFS.index(alpha)+1)%3],sign),
               negative(EXACT[alpha][cofn]) if sign>0 else EXACT[alpha][cofn]]
        visual={"mode":"reduction","theta":theta,"reference":alpha,"function":fn,"quadrant":quadrant}
    elif n==5:
        sets=((0,90,120,180),(30,90,180,270),(0,60,180,270),
              (90,150,210,270),(0,45,180,225))
        angles=sets[(i-1+variant)%5]
        family=(i-1)//5
        identities=("tan θ = sin θ / cos θ",
                    "sin² θ / (1 + cos θ) = 1 − cos θ",
                    "(1 − cos² θ) / sin θ = sin θ")
        invalid=({90,270},{180},{0,180})[family]
        valid=[a for a in angles if a not in invalid]
        answer=", ".join(map(fmt_angle,valid)) if valid else "none"
        list_text=", ".join(map(fmt_angle,angles))
        problem=f"At which of θ = {list_text} is {identities[family]} defined and true?"
        denominator=("cos θ","1 + cos θ","sin θ")[family]
        reason=("cos θ is zero at 90° and 270°",
                "1 + cos θ is zero at 180°",
                "sin θ is zero at 0° and 180°")[family]
        excluded=sorted(set(angles)&invalid)
        actions=[f"Read the proposed angles: {list_text}. This equality contains a denominator {denominator}.",
                 f"Only angles with a nonzero denominator can be tested; {reason}.",
                 f"Exclude {', '.join(map(fmt_angle,excluded)) if excluded else 'no candidates'} from the given list.",
                 f"At the remaining angles the identity follows from sin² θ + cos² θ = 1 and the denominator is nonzero.",
                 f"Answer: {answer}. Each included angle makes both original sides equal and defined."]
        wrong=[list_text,
               ", ".join(map(fmt_angle,excluded)) if excluded else "none",
               ", ".join(map(fmt_angle,angles[:-1]))]
        visual={"mode":"domain","angles":angles,"excluded":excluded,"family":family}
    else:
        # Exact nonzero special-angle targets. General solutions are given in degrees.
        fn=FUNCTIONS[((i-1+variant*2)//3)%3]
        alpha=REFS[(i-1+variant)%3]
        sign=1 if ((i-1+variant)//9)%2==0 else -1
        target=values(fn,alpha,sign)
        if fn=="sin":
            roots=(alpha,180-alpha) if sign>0 else (180+alpha,360-alpha)
        elif fn=="cos":
            roots=(alpha,360-alpha) if sign>0 else (180-alpha,180+alpha)
        else:
            roots=(alpha,180+alpha) if sign>0 else (180-alpha,360-alpha)
        roots=tuple(sorted(roots))
        period=PERIOD[fn]
        if n==6:
            # Tangent has one branch in a 180° period.
            general=(f"θ = {roots[0]}° + 180°k" if fn=="tan" else
                     f"θ = {roots[0]}° + 360°k or θ = {roots[1]}° + 360°k")
            answer=general+", k ∈ ℤ"
            problem=f"Give the general solution in degrees of {fn} θ = {target}."
            actions=[f"The target magnitude {target.lstrip('-')} has reference angle {alpha}°.",
                     f"{fn} is {'positive' if sign>0 else 'negative'} in the required quadrants; mark the solutions {roots[0]}° and {roots[1]}° in one revolution.",
                     f"The period of {fn} is {period}°; translating a solution by one period preserves its value.",
                     f"Write the complete branch{'es' if fn!='tan' else ''}: {general}.",
                     f"Answer: {answer}. Substitution gives {fn} θ = {target} on every branch."]
            wrong=[general.replace(f"{period}°k",f"{360 if period==180 else 180}°k")+", k ∈ ℤ",
                   f"θ = {alpha}° + 360°k, k ∈ ℤ",
                   f"θ = {roots[0]}°, k ∈ ℤ"]
        else:
            upper=720 if (i+variant)%4==0 else 360
            solutions=sorted(set(x+360*j for j in range(upper//360) for x in roots))
            answer=", ".join(map(fmt_angle,solutions))
            problem=f"Solve {fn} θ = {target} for 0° ≤ θ < {upper}°."
            actions=[f"The exact target {target} has acute reference angle {alpha}°.",
                     f"Use the unit-circle signs to identify the first-revolution candidates {roots[0]}° and {roots[1]}°.",
                     f"The period of {fn} is {period}°; list equivalent angles before applying the interval.",
                     f"Keep only values with 0° ≤ θ < {upper}°. The retained angles are {answer}.",
                     f"Answer: {answer}. Substitute every retained angle and check both interval endpoints."]
            wrong=[", ".join(map(fmt_angle,solutions[:-1])),
                   ", ".join(map(fmt_angle,solutions+[upper])),
                   ", ".join(map(fmt_angle,[alpha]))]
        visual={"mode":"general" if n==6 else "interval","reference":alpha,
                "function":fn,"target":target,"sign":sign,
                "upper":upper if n==7 else None}
    # Preserve three distinct misconception choices; avoid options identical to answer.
    wrong=list(dict.fromkeys(x for x in wrong if x!=answer))
    candidate=1
    while len(wrong)<3:
        distractor=f"{candidate*15}°" if n in (5,7) else f"{candidate}/2" if n<=4 else f"θ = {candidate*30}°, k ∈ ℤ"
        if distractor!=answer and distractor not in wrong:wrong.append(distractor)
        candidate+=1
    return problem,answer,actions,visual,wrong[:3]

def case(n:int,i:int,variant:int=0)->dict:
    problem,answer,actions,visual,wrong=steps_and_visual(n,i,variant)
    assert len(actions)==5 and len({answer,*wrong})==4
    return {"id":f"g11-tr-l{n:02}-w{i:02}","lesson":n,"problem":problem,
            "answer":answer,"actions":actions,"check":actions[-1],
            "visual":{"family":"grade11_trigonometry","values":visual},"wrong":wrong,
            "difficulty":DIFFICULTIES[min(i-1,14)]}

def build():
    DOC.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    manifest=[]
    for n,title in TITLES.items():
        worked=[{key:value for key,value in case(n,i).items() if key!="wrong"} for i in range(1,16)]
        assert len({scene["problem"] for scene in worked})==15,(n,"duplicate worked prompts")
        data={"source":f"grade11-tr-lesson-{n:02}.md","worked":worked}
        for section,amount,variant,prefix in (("practice",15,1,"p"),("mastery",5,2,"m"),("reassessment",3,3,"r")):
            rows=[]
            for i in range(1,amount+1):
                scene=case(n,i,variant)
                choices=[scene["answer"],*scene["wrong"]]
                shift=(i+variant)%4;choices=choices[shift:]+choices[:shift]
                rows.append({"id":f"g11-tr-l{n:02}-{prefix}{i:02}","prompt":scene["problem"],
                             "options":choices,"answer_index":choices.index(scene["answer"]),
                             "memo":" ".join(scene["actions"]),"actions":scene["actions"]})
            data[section]=rows
        lines=[f"# Grade 11 Topic 3, Lesson {n}: {title}",
               f"Scope: [DBE Grade 11 Mathematics ATP, Term 1]({ATP}). All problems and worked solutions authored for Athena.",
               "Status: teacher review and live browser acceptance required. Angles in degrees; work before choosing."]
        for scene in worked:
            lines += [f"## {scene['id']}: {scene['problem']}",
                      f"Whiteboard values: `{json.dumps(scene['visual'],ensure_ascii=False)}`",
                      *[f"{j}. {action}" for j,action in enumerate(scene["actions"],1)],
                      f"Answer: {scene['answer']}. Verification: {scene['check']}"]
        for section in ("practice","mastery","reassessment"):
            lines.append(f"## {section.title()} answer key")
            for item in data[section]:
                lines.append(f"- {item['id']}: {item['prompt']} Options: {' | '.join(item['options'])}. Correct: {item['options'][item['answer_index']]}. {item['memo']}")
        source=DOC/data["source"]
        source.write_text("\n\n".join(lines)+"\n",encoding="utf-8")
        (OUT/f"trigonometry_{n:02}.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        manifest.append({"lesson_id":f"g11-tr-{n:02}","source":source.name,"source_sha256":sha256(source.read_bytes()).hexdigest(),
                         "worked":15,"practice":15,"mastery":5,"reassessment":3,
                         "status":"teacher_review_required","teacher_approved":False,"browser_accepted":False})
    (DOC/"topic3-acceptance-manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")

if __name__=="__main__":build()
