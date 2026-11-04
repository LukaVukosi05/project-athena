"""Compile approved Grade 9 Topic 1 source tables into deterministic runtime data."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/curriculum/grade9/whole-numbers"
DEST = ROOT / "backend/app/curriculum/grade9/generated"

# Render data is deliberately separate from prose: changing an answer or the
# mathematical objects requires review of the source and the contract below.
CLASSIFICATION = [
    ("6", "N"), ("0", "W"), ("−7", "Z"), ("3/4", "Q"),
    ("−2.5", "Q"), ("0.333…", "Q"), ("√49", "N"),
    ("√2", "I"), ("−√81", "Z"), ("π and 22/7", "I"),
    ("−√16/2", "Z"), ("2/0", "outside"),
    ("0.101001000100001…", "I"), ("√50/√2", "N"),
    ("√(−9)", "outside"),
]
FACTOR_ROOTS = [
    [21], [36], [18,24], [12,18], [20,30], [72,108],
    [8,12,15], [35,48], [12,18], [84,126], [24,36],
    [8,12,20], [18,30,4], [54,24,36,45,72], [96,144],
]
FACTOR_KIND = [
    "prime", "prime", "hcf", "lcm", "both", "hcf", "lcm", "hcf",
    "lcm_clock", "hcf_ribbon", "error_hcf", "lcm_clock", "lcm", "candidate_hcf", "hcf_pack",
]


def clean(value):
    return value.strip().replace("`", "").replace("**", "")


def table_rows(text, prefix):
    return [list(map(clean, line.split("|")[1:-1]))
            for line in text.splitlines() if re.match(rf"^\| {prefix}\d{{2}}(?:\s|\|)", line)]


def primes(value):
    factors=[]; divisor=2
    while divisor*divisor<=value:
        while value%divisor==0:
            factors.append(divisor);value//=divisor
        divisor+=1
    if value>1:factors.append(value)
    return factors


def build(number):
    source = SOURCE / ("lesson-01-number-systems.md" if number==1 else "lesson-02-prime-factors-hcf-lcm.md")
    text=source.read_text(encoding="utf-8")
    worked=[]
    for index,row in enumerate(table_rows(text,"W"),1):
        assert len(row)==4 and row[0].startswith(f"W{index:02} "), row
        _,difficulty=row[0].split(" ",1)
        actions=[clean(part) for part in row[2].split("; ") if clean(part)]
        # The check is a final state, never an annotation on a still-incomplete step.
        check="Check: "+row[3].split(" Error:")[0].split(" First error:")[0]
        actions.append(check)
        assert len(actions)>=3 and len(set(actions))==len(actions), row[0]
        scene={"id":f"g9-whole-l{number:02}-w{index:02}","problem":row[1],
               "difficulty":difficulty,"actions":actions,"misconception":row[3],
               "memo":row[2],"check":check}
        if number==1:
            scene.update(token=CLASSIFICATION[index-1][0],category=CLASSIFICATION[index-1][1])
            if index in (8,10,15):
                second={8:("√4 = 2","N"),10:("22/7","Q"),15:("−√9 = −3","Z")}[index]
                scene['token']={8:'√2',10:'π',15:'√(−9)'}[index]
                scene.update(secondary=second[0],secondary_input={8:'√4',10:'22/7',15:'−√9'}[index],
                             secondary_category=second[1],primary_stage={8:3,10:1,15:2}[index],
                             secondary_stage={8:1,10:3,15:3}[index])
        else:
            numbers=FACTOR_ROOTS[index-1]
            scene.update(numbers=numbers,kind=FACTOR_KIND[index-1],factors=[primes(n) for n in numbers])
        worked.append(scene)
    banks={}
    for prefix in ("P","M","R"):
        rows=table_rows(text,prefix)
        bank=[]
        for index,row in enumerate(rows,1):
            assert row[0]==f"{prefix}{index:02}", row
            if prefix=="P":
                assert len(row)==7,row
                options=row[2:6];explanation=row[6]
            else:
                assert len(row)==4,row
                options=[clean(v) for v in row[2].split(";")];explanation=row[3]
            assert len(options)==len(set(options))==4, row
            match=re.search(r"^([ABCD])\.",explanation)
            assert match,row
            bank.append({"id":f"g9-whole-l{number:02}-{prefix.lower()}{index:02}",
                         "prompt":row[1],"options":options,"answer_index":"ABCD".index(match[1]),
                         "memo":explanation})
        banks[prefix.lower()]=bank
    assert len(worked)==len(banks["p"])==15 and len(banks["m"])==5 and len(banks["r"])==3
    return {"source":source.name,"worked":worked,"practice":banks["p"],"mastery":banks["m"],"reassessment":banks["r"]}


if __name__=="__main__":
    DEST.mkdir(parents=True,exist_ok=True)
    for n in (1,2):
        target=DEST/f"whole_numbers_{n:02}.json"
        target.write_text(json.dumps(build(n),ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        print(target.relative_to(ROOT))
