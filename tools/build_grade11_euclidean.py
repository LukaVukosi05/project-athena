"""Original Grade 11 circle-theorem application banks with measurable geometry."""
from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/"docs/curriculum/grade11/euclidean-geometry"
OUT=ROOT/"backend/app/curriculum/grade11/generated"
ATP="https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2023%20ATPs/FET%20Content%20Subjects/Grade%2011/1.590%20ATP%202023-24%20Gr%2011%20Maths%20final.pdf"
TITLES={
  1:"Perpendiculars and chord midpoints",
  2:"Centre angle and angle at the circumference",
  3:"Angles in the same segment",
  4:"Opposite angles of a cyclic quadrilateral",
  5:"Equal tangents and perpendicular radii",
  6:"Tangent–chord alternate-segment theorem",
  7:"Combine centre and cyclic angle theorems",
  8:"Diagnose a two-theorem tangent–chord rider",
}
DIFFICULTIES=["foundation"]*2+["easy"]*3+["standard"]*4+["intermediate"]*3+["exam"]*3
TRIPLES=((3,4,5),(5,12,13),(8,15,17))

def case(n:int,i:int,variant:int=0)->dict:
    t=((i-1+variant*7)%30)+1
    angle=36+4*t # central, under 180°
    gamma=30+2*t # tangent–chord, no more than 90°
    if n==1:
        half,d,r=TRIPLES[(t-1)%3]
        scale=1+(t-1)//3
        half*=scale;d*=scale;r*=scale
        length=2*half
        problem=(f"In a circle with centre O, OM ⟂ chord AB at M. "
                 f"If OA = {r} cm and OM = {d} cm, calculate AB.")
        answer=f"{length} cm"
        steps=[
            f"Mark OA = {r} cm as a radius. Because OM is perpendicular to chord AB, M bisects AB.",
            f"Triangle OMA is right-angled at M, with hypotenuse OA = {r} cm and side OM = {d} cm.",
            f"By Pythagoras, AM² = OA² − OM² = {r*r} − {d*d} = {half*half} cm².",
            f"The positive length AM = {half} cm, and the chord has equal halves AM and MB.",
            f"Answer: AB = 2({half}) = {length} cm. Check: {half}² + {d}² = {r}²."
        ]
        wrong=[f"{half} cm",f"{r} cm",f"{2*d} cm"]
        visual={"mode":"chord","half":half,"distance":d,"radius":r}
    elif n==2:
        central=angle
        inscribed=angle//2
        problem=f"Arc AB subtends ∠AOB = {central}° at centre O. C lies on the major arc AB. Find ∠ACB."
        answer=f"{inscribed}°"
        steps=[
            f"Trace arc AB and confirm that C is on the major arc; ∠AOB = {central}° subtends the minor arc AB.",
            f"Draw chords CA and CB. The angle at C and the angle at O stand on the same minor arc AB.",
            f"The angle at the centre is twice the angle at the circumference on that arc.",
            f"Therefore 2∠ACB = {central}°, so ∠ACB = {central}° ÷ 2.",
            f"Answer: ∠ACB = {inscribed}°. Check: 2({inscribed}°) = {central}°."
        ]
        wrong=[f"{central}°",f"{180-central}°",f"{180-inscribed}°"]
        visual={"mode":"centre","central":central,"target":"circumference"}
    elif n==3:
        inscribed=20+2*t
        central=2*inscribed
        problem=f"Points C and D lie on the same major arc AB. If ∠ACB = {inscribed}°, find ∠ADB."
        answer=f"{inscribed}°"
        steps=[
            f"Mark the given ∠ACB = {inscribed}° and identify its endpoints A and B.",
            f"∠ACB and ∠ADB both stand on chord AB, with C and D on the same side of AB.",
            f"Angles in the same segment of a circle are equal.",
            f"Transfer the {inscribed}° marking from C to D without changing the intercepted chord.",
            f"Answer: ∠ADB = {inscribed}°. The centre angle on the minor arc would be {central}°, twice either angle."
        ]
        wrong=[f"{central}°",f"{180-inscribed}°",f"{90-inscribed//2}°"]
        visual={"mode":"same_segment","inscribed":inscribed}
    elif n==4:
        given=40+3*t
        opposite=180-given
        problem=f"ABCD is a cyclic quadrilateral in order. If ∠BAD = {given}°, find its opposite angle ∠BCD."
        answer=f"{opposite}°"
        steps=[
            f"Locate ∠BAD = {given}° at vertex A and ∠BCD at the opposite vertex C.",
            f"Because all four vertices lie on one circle, the two opposite angles are supplementary.",
            f"Write ∠BAD + ∠BCD = 180°.",
            f"Subtract the known angle: ∠BCD = 180° − {given}°.",
            f"Answer: ∠BCD = {opposite}°. Check: {given}° + {opposite}° = 180°."
        ]
        wrong=[f"{given}°",f"{90-given if given<90 else given-90}°",f"{360-given}°"]
        visual={"mode":"cyclic","given":given}
    elif n==5:
        radius,tangent,hyp=TRIPLES[(t-1)%3]
        scale=1+(t-1)//3
        radius*=scale;tangent*=scale;hyp*=scale
        problem=(f"From external point P, tangents PA and PB touch a circle with centre O. "
                 f"If OP = {hyp} cm and OA = {radius} cm, calculate both tangent lengths.")
        answer=f"PA = PB = {tangent} cm"
        steps=[
            f"Join O to point of contact A. Radius OA = {radius} cm is perpendicular to tangent PA.",
            f"Right triangle OAP has hypotenuse OP = {hyp} cm and leg OA = {radius} cm.",
            f"Apply Pythagoras: PA² = OP² − OA² = {hyp*hyp} − {radius*radius} = {tangent*tangent} cm².",
            f"The positive tangent length PA = {tangent} cm. Tangents from the same external point are equal.",
            f"Answer: PA = PB = {tangent} cm. Check: {radius}² + {tangent}² = {hyp}²."
        ]
        wrong=[f"PA = PB = {radius} cm",f"PA = PB = {hyp} cm",f"PA = PB = {hyp+radius} cm"]
        visual={"mode":"tangents","radius":radius,"tangent":tangent,"external":hyp}
    elif n==6:
        inscribed=gamma
        problem=(f"A tangent at A forms an angle of {gamma}° with chord AB. "
                 f"C lies on the major arc AB. Find ∠ACB.")
        answer=f"{inscribed}°"
        steps=[
            f"Mark the {gamma}° angle between the tangent ray at A and chord AB.",
            f"Join C to A and B. Angle ACB subtends chord AB on the alternate side of the tangent.",
            f"By the tangent–chord theorem, the angle in the alternate segment equals the tangent–chord angle.",
            f"Thus ∠ACB has the same measure as the marked angle at A: {gamma}°.",
            f"Answer: ∠ACB = {inscribed}°. Its intercepted minor arc AB has centre angle {2*gamma}°."
        ]
        wrong=[f"{2*gamma}°",f"{180-gamma}°",f"{90-gamma}°"]
        visual={"mode":"tangent_chord","given":gamma}
    elif n==7:
        inscribed=angle//2
        opposite=180-inscribed
        problem=(f"Arc AB subtends ∠AOB = {angle}° at centre O. "
                 f"C is on the major arc AB and D on the minor arc AB. Find ∠ADB.")
        answer=f"{opposite}°"
        steps=[
            f"∠AOB = {angle}° subtends the minor arc AB; C stands on the major arc.",
            f"The centre angle is twice the angle at C, so ∠ACB = {angle}° ÷ 2 = {inscribed}°.",
            f"A, C, B, D lie on one circle; ∠ACB and ∠ADB are opposite cyclic angles.",
            f"Opposite cyclic angles sum to 180°, so ∠ADB = 180° − {inscribed}°.",
            f"Answer: ∠ADB = {opposite}°. Check: {inscribed}° + {opposite}° = 180°."
        ]
        wrong=[f"{inscribed}°",f"{angle}°",f"{180-angle}°"]
        visual={"mode":"centre_cyclic","central":angle}
    else:
        opposite=180-gamma
        problem=(f"A tangent at A makes {gamma}° with chord AB. C is on the major arc AB "
                 f"and D on the minor arc. A learner claims ∠ADB = {gamma}°. Find ∠ADB and identify the missed theorem.")
        answer=f"{opposite}°; opposite angles of a cyclic quadrilateral"
        steps=[
            f"Identify the marked tangent–chord angle at A as {gamma}°.",
            f"By the alternate-segment theorem, ∠ACB = {gamma}° because C lies on the major arc AB.",
            f"The learner transferred this value directly to D, but C and D are on opposite sides of chord AB.",
            f"∠ACB and ∠ADB are opposite cyclic angles, so ∠ADB = 180° − {gamma}°.",
            f"Answer: ∠ADB = {opposite}°; opposite angles of a cyclic quadrilateral. Check: {gamma}° + {opposite}° = 180°."
        ]
        wrong=[f"{gamma}°; angles in the same segment",
               f"{2*gamma}°; centre angle theorem",
               f"{opposite}°; angles in the same segment"]
        visual={"mode":"tangent_cyclic","given":gamma}
    wrong=list(dict.fromkeys(w for w in wrong if w!=answer))
    offset=1
    while len(wrong)<3:
        item=f"{angle+offset}°"
        if item not in wrong and item!=answer:wrong.append(item)
        offset+=1
    assert len(steps)==5 and len({answer,*wrong[:3]})==4
    return {"id":f"g11-euc-l{n:02}-w{i:02}","lesson":n,
            "problem":problem,"answer":answer,"actions":steps,"check":steps[-1],
            "visual":{"family":"grade11_euclidean","values":visual},"wrong":wrong[:3],
            "difficulty":DIFFICULTIES[min(i-1,14)]}

def build():
    DOC.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    manifest=[]
    for n,title in TITLES.items():
        worked=[{key:value for key,value in case(n,i).items() if key!="wrong"} for i in range(1,16)]
        assert len({x["problem"] for x in worked})==15
        data={"source":f"grade11-euc-lesson-{n:02}.md","worked":worked}
        for section,amount,variant,prefix in (("practice",15,1,"p"),("mastery",5,2,"m"),("reassessment",3,3,"r")):
            items=[]
            for i in range(1,amount+1):
                scene=case(n,i,variant);choices=[scene["answer"],*scene["wrong"]]
                shift=(i+variant)%4;choices=choices[shift:]+choices[:shift]
                items.append({"id":f"g11-euc-l{n:02}-{prefix}{i:02}","prompt":scene["problem"],
                              "options":choices,"answer_index":choices.index(scene["answer"]),
                              "actions":scene["actions"],"memo":" ".join(scene["actions"])})
            data[section]=items
        lines=[f"# Grade 11 Topic 4, Lesson {n}: {title}",
               f"Scope: [DBE Grade 11 Mathematics ATP, Term 2]({ATP}). Original Athena diagrams and questions.",
               "Status: teacher review and live browser acceptance required. Give the theorem reason before calculating."]
        for item in worked:
            lines.extend([f"## {item['id']}: {item['problem']}",
                          f"Visual values: `{json.dumps(item['visual'],ensure_ascii=False)}`",
                          *[f"{j}. {step}" for j,step in enumerate(item["actions"],1)],
                          f"Answer: {item['answer']}. Check: {item['check']}"])
        for section in ("practice","mastery","reassessment"):
            lines.append(f"## {section.title()} answer key")
            for item in data[section]:
                lines.append(f"- {item['id']}: {item['prompt']} Options: {' | '.join(item['options'])}. Correct: {item['options'][item['answer_index']]}. {item['memo']}")
        source=DOC/data["source"];source.write_text("\n\n".join(lines)+"\n",encoding="utf-8")
        (OUT/f"euclidean_{n:02}.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        manifest.append({"lesson_id":f"g11-euc-{n:02}","source":source.name,
                         "source_sha256":sha256(source.read_bytes()).hexdigest(),
                         "worked":15,"practice":15,"mastery":5,"reassessment":3,
                         "status":"teacher_review_required","teacher_approved":False,"browser_accepted":False})
    (DOC/"topic4-acceptance-manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")

if __name__=="__main__":build()
