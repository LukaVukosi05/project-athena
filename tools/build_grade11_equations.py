"""Original, deterministic Grade 11 equations and inequalities banks.

Parameters are chosen so every worked problem has an independently checkable
integer or exact radical answer. The source files are authored snapshots.
"""
from __future__ import annotations

import json
from hashlib import sha256
from math import isqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/curriculum/grade11/equations-inequalities"
OUT = ROOT / "backend/app/curriculum/grade11/generated"
ATP = "https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2023%20ATPs/FET%20Content%20Subjects/Grade%2011/1.590%20ATP%202023-24%20Gr%2011%20Maths%20final.pdf"
TITLES = {
    1: "Complete the square and read the turning point",
    2: "Solve quadratic equations by factorisation",
    3: "Use the quadratic formula for exact roots",
    4: "Solve quadratic inequalities on a graph",
    5: "Solve linear and quadratic equations simultaneously",
    6: "Use the discriminant to classify roots",
    7: "Choose and justify a quadratic method",
}
DIFFICULTIES = ["foundation"]*2 + ["easy"]*3 + ["standard"]*4 + ["intermediate"]*3 + ["exam"]*3

def polynomial(b: int, c: int) -> str:
    return "x²" + (f" + {b}x" if b > 0 else f" − {abs(b)}x" if b < 0 else "") + (f" + {c}" if c > 0 else f" − {abs(c)}" if c < 0 else "")

def signed(n: int) -> str:
    return f"+ {n}" if n >= 0 else f"− {abs(n)}"

def factor(r: int) -> str:
    return f"(x − {r})" if r >= 0 else f"(x + {abs(r)})"

def roots_text(r: int, s: int) -> str:
    return f"x = {r} or x = {s}" if r != s else f"x = {r}"

def case(number: int, index: int, variant: int = 0) -> dict:
    t = index + 23*variant
    h = (2+t%5)*(-1 if t%4==0 else 1)
    k = (t%9)-4
    r = -4+t%7
    s = r+2+(t//3)%6
    if number == 7:
        number = (2,4,5)[t%3]
        integrated = True
    else:
        integrated = False
    if number == 1:
        c=h*h+k
        question=f"Complete the square for f(x) = {polynomial(2*h,c)} and state its turning point."
        answer=f"({-h}; {k})"
        steps=[
            f"Half the coefficient of x: {2*h} ÷ 2 = {h}. The square will use (x {signed(h)}).",
            f"Square the half-coefficient: ({h})² = {h*h}. Add and subtract this amount.",
            f"f(x) = (x {signed(h)})² {signed(c-h*h)}.",
            f"The square is smallest when x = {-h}, so the turning point is ({-h}; {k}).",
            f"Answer: {answer}. Expand (x {signed(h)})² {signed(k)} to recover {polynomial(2*h,c)}."
        ]
        wrong=[f"({h}; {k})",f"({-h}; {-k})",f"({h}; {-k})"]
        visual={"mode":"square","b":2*h,"c":c}
    elif number == 2:
        b=-(r+s);c=r*s
        question=f"Solve {polynomial(b,c)} = 0 by factorisation."
        answer=roots_text(r,s)
        steps=[
            f"Find two numbers whose sum is {b} and product is {c}. Here they are {-r} and {-s}.",
            f"Split the middle term: x² {signed(-r)}x {signed(-s)}x {signed(c)} = 0.",
            f"Factor: {factor(r)}{factor(s)} = 0.",
            f"Use the zero-product rule: x − ({r}) = 0 or x − ({s}) = 0.",
            f"Answer: {answer}. Substituting each value into {polynomial(b,c)} gives zero."
        ]
        wrong=[roots_text(-r,-s),f"x = {r+s}",f"x = {r*s}"]
        visual={"mode":"roots","b":b,"c":c}
    elif number == 3:
        # D = 4u; u is never a perfect square. Exact roots are -h ± √u.
        u=(2,3,5,6,7,8,10,11,13,14,15,17,18,19,20)[(t-1)%15]
        b=2*h;c=h*h-u;disc=b*b-4*c
        question=f"Solve {polynomial(b,c)} = 0 using the quadratic formula. Give exact roots."
        answer=f"x = {-h} ± √{u}"
        steps=[
            f"Identify a = 1, b = {b} and c = {c} in ax² + bx + c = 0.",
            f"Calculate b² − 4ac = ({b})² − 4(1)({c}) = {disc}.",
            f"Substitute: x = (−({b}) ± √{disc}) ÷ 2.",
            f"Since √{disc} = 2√{u}, divide both terms by 2 to get x = {-h} ± √{u}.",
            f"Answer: {answer}. Each candidate satisfies (x + {h})² = {u}, hence the original equation."
        ]
        wrong=[f"x = {h} ± √{u}",f"x = {-h} ± √{disc}",f"x = {-h} ± {u}"]
        visual={"mode":"formula","b":b,"c":c,"discriminant":disc}
    elif number == 4:
        b=-(r+s);c=r*s; below=t%2==0; inclusive=t%3==0
        sign="≤" if below and inclusive else "<" if below else "≥" if inclusive else ">"
        question=f"Solve {polynomial(b,c)} {sign} 0. Show the interval on a number line."
        answer=(f"{r} ≤ x ≤ {s}" if inclusive else f"{r} < x < {s}") if below else (
            f"x ≤ {r} or x ≥ {s}" if inclusive else f"x < {r} or x > {s}")
        steps=[
            f"Find the boundary roots: {factor(r)}{factor(s)} = 0 gives x = {r} or x = {s}.",
            f"Mark {r} and {s} on the number line. The parabola opens upwards.",
            f"Between the roots the product is negative; outside them it is positive.",
            f"Select the {'between' if below else 'outside'} region for {sign} 0. {'Include' if inclusive else 'Exclude'} both zero endpoints.",
            f"Answer: {answer}. A test value in each chosen interval has the requested sign."
        ]
        wrong=[(f"x < {r} or x > {s}" if inclusive else f"x ≤ {r} or x ≥ {s}") if below else (
            f"{r} < x < {s}" if inclusive else f"{r} ≤ x ≤ {s}"),
            f"x = {r} or x = {s}",
            (f"{r} ≤ x ≤ {s}" if inclusive else f"{r} < x < {s}") if not below else (
                f"x ≤ {r} or x ≥ {s}" if inclusive else f"x < {r} or x > {s}")]
        visual={"mode":"inequality","b":b,"c":c,"sign":sign,"r":r,"s":s}
    elif number == 5:
        m=(t%5)-2;d=1+t%3;b=m-r-s;c=r*s+d
        yr=m*r+d;ys=m*s+d
        question=f"Find both intersections of y = {polynomial(b,c)} and y = {m}x {signed(d)}."
        answer=f"({r}; {yr}) and ({s}; {ys})"
        steps=[
            f"At an intersection the y-values are equal: {polynomial(b,c)} = {m}x {signed(d)}.",
            f"Subtract the line from both sides to preserve equality: {polynomial(b-m,c-d)} = 0.",
            f"Factor {factor(r)}{factor(s)} = 0, so x = {r} or x = {s}.",
            f"Use the straight line y = {m}x {signed(d)}: y({r}) = {yr} and y({s}) = {ys}.",
            f"Answer: {answer}. Substitute both ordered pairs into BOTH original equations."
        ]
        wrong=[f"({r}; {ys}) and ({s}; {yr})",roots_text(r,s),f"({-r}; {yr}) and ({-s}; {ys})"]
        visual={"mode":"intersection","b":b,"c":c,"m":m,"d":d}
    else:
        a=1;b=2*h
        kind=t%3
        if kind==0:c=h*h;label="equal real roots"
        elif kind==1:c=h*h-(2+t%7);label="two distinct real roots"
        else:c=h*h+(2+t%7);label="no real roots"
        disc=b*b-4*c
        question=f"Determine the nature of the roots of {polynomial(b,c)} = 0 without solving it."
        answer=label
        steps=[
            f"Read a = {a}, b = {b}, c = {c} from ax² + bx + c = 0.",
            f"Use the discriminant Δ = b² − 4ac.",
            f"Substitute: Δ = ({b})² − 4({a})({c}) = {disc}.",
            f"Because Δ is {'positive' if disc>0 else 'zero' if disc==0 else 'negative'}, the graph {'crosses' if disc>0 else 'touches' if disc==0 else 'does not meet'} the x-axis.",
            f"Answer: {answer}. The sign of Δ = {disc} confirms the classification."
        ]
        wrong=[x for x in ("equal real roots","two distinct real roots","no real roots","one positive root") if x!=answer][:3]
        visual={"mode":"discriminant","b":b,"c":c}
    if integrated:
        question="Choose a method and justify it. "+question
        steps[0]="Select the appropriate quadratic method. "+steps[0]
    wrong=list(dict.fromkeys(w for w in wrong if w!=answer))
    extra=1
    while len(wrong)<3:
        candidate=answer+f" (incorrect {extra})"
        if candidate not in wrong:wrong.append(candidate)
        extra+=1
    assert len(steps)==5 and len({answer,*wrong[:3]})==4
    return {"lesson":(7 if integrated else number),"problem":question,"answer":answer,
            "actions":steps,"check":steps[-1],"wrong":wrong[:3],
            "difficulty":DIFFICULTIES[min(index-1,14)],
            "visual":{"family":"grade11_equations","values":visual}}

def build():
    DOC.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    manifest=[]
    for n,title in TITLES.items():
        worked=[]
        for i in range(1,16):
            scene=case(n,i);scene["id"]=f"g11-ei-l{n:02}-w{i:02}"
            worked.append({k:v for k,v in scene.items() if k!="wrong"})
        data={"source":f"grade11-ei-lesson-{n:02}.md","worked":worked}
        for key,amount,variant,prefix in (("practice",15,1,"p"),("mastery",5,2,"m"),("reassessment",3,3,"r")):
            items=[]
            for i in range(1,amount+1):
                scene=case(n,i,variant)
                choices=[scene["answer"],*scene["wrong"]]
                shift=(i+variant)%4
                choices=choices[shift:]+choices[:shift]
                items.append({"id":f"g11-ei-l{n:02}-{prefix}{i:02}",
                              "prompt":scene["problem"],"options":choices,
                              "answer_index":choices.index(scene["answer"]),
                              "actions":scene["actions"],"memo":" ".join(scene["actions"])})
            data[key]=items
        assert len({q["problem"] for q in worked})==15
        lines=[f"# Grade 11 Topic 2, Lesson {n}: {title}",
               f"Scope: [DBE Grade 11 Mathematics ATP, Term 1]({ATP}). Original Athena problems.",
               "Status: teacher review and live browser acceptance required. Work in a book before selecting an option."]
        for scene in worked:
            lines.extend([f"## {scene['id']} — {scene['problem']}",
                          f"Visual values: `{json.dumps(scene['visual'],ensure_ascii=False)}`",
                          *[f"{j}. {step}" for j,step in enumerate(scene["actions"],1)],
                          f"Answer: {scene['answer']}. Check: {scene['check']}"])
        for key in ("practice","mastery","reassessment"):
            lines.append(f"## {key.title()} answer key")
            for item in data[key]:
                lines.append(f"- {item['id']}: {item['prompt']} Options: {' | '.join(item['options'])}. Correct: {item['options'][item['answer_index']]}. {item['memo']}")
        source=DOC/data["source"]
        source.write_text("\n\n".join(lines)+"\n",encoding="utf-8")
        (OUT/f"equations_inequalities_{n:02}.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        manifest.append({"lesson_id":f"g11-ei-{n:02}","source":source.name,"source_sha256":sha256(source.read_bytes()).hexdigest(),
                         "worked":15,"practice":15,"mastery":5,"reassessment":3,
                         "status":"teacher_review_required","teacher_approved":False,"browser_accepted":False})
    (DOC/"topic2-acceptance-manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")

if __name__=="__main__":build()
