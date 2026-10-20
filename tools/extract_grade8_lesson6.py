"""Compile Grade 8 variables-on-both-sides content from the approved pack."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from extract_grade8_lesson3 import SOURCE, EXPECTED_HASH, lines_from_docx, after, value, between, inline

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "backend/app/curriculum/grade8/generated/lesson_06.json"


def bank(section: list[str], kind: str, expected: int) -> list[dict]:
    positions = [(i, re.search(rf"g8-ae-l06-{kind}\d{{2}}", line).group()) for i, line in enumerate(section)
                 if re.search(rf"g8-ae-l06-{kind}\d{{2}}", line)]
    if len(positions) != expected:
        raise ValueError(f"Expected {expected} {kind} questions, found {len(positions)}")
    result = []
    for n, (pos, stable_id) in enumerate(positions, 1):
        end = positions[n][0] - 1 if n < len(positions) else len(section)
        chunk = section[pos + 1:end]
        prompt = next(re.match(rf"^{n}\. (.+)", line).group(1) for line in reversed(section[:pos])
                      if re.match(rf"^{n}\. (.+)", line))
        start_solution = chunk.index("Complete solution") + 1
        end_solution = next((i for i in range(start_solution, len(chunk)) if chunk[i].startswith("Misconception tags:")), len(chunk))
        result.append({"id":stable_id,"number":n,"prompt":prompt,"marks":int(value(chunk,"Marks")),
                       "answer":inline(chunk,"Answer"),"solution":chunk[start_solution:end_solution],
                       "misconception_tags":[s.strip() for s in next((line.split(":",1)[1] for line in chunk if line.startswith("Misconception tags:")), "").split(",") if s.strip()]})
    return result


def worked(section: list[str]) -> list[dict]:
    starts = [i for i, line in enumerate(section) if re.match(r"Worked example \d+: ", line)]
    if len(starts) != 15:
        raise ValueError(f"Expected 15 worked examples, found {len(starts)}")
    result = []
    for n, pos in enumerate(starts, 1):
        chunk = section[pos:starts[n] if n < len(starts) else len(section)]
        prompt = re.match(rf"Worked example {n}: (.+)", chunk[0]).group(1)
        stable_id = next(line for line in chunk if re.fullmatch(r"g8-ae-l06-w\d{2}", line))
        id_pos = chunk.index(stable_id)
        memo_start, sequence_start = chunk.index("Complete memo")+1, chunk.index("Deterministic teaching sequence")+1
        memo_end = next(i for i in range(memo_start,len(chunk)) if chunk[i].startswith("Misconception tags:"))
        sequence_end = next(i for i in range(sequence_start,len(chunk)) if chunk[i].startswith("Verification:"))
        result.append({"id":stable_id,"number":n,"prompt":prompt,"difficulty":chunk[id_pos+1].casefold(),
                       "cognitive_level":chunk[id_pos+2].casefold().replace(" ","_"),"marks":int(chunk[id_pos+3]),
                       "answer":inline(chunk,"Learner-facing answer"),"memo":chunk[memo_start:memo_end],
                       "misconception_tags":[s.strip() for s in inline(chunk,"Misconception tags").split(",")],
                       "renderer":inline(chunk,"Renderer"),"question_data":inline(chunk,"Question data"),
                       "initial_state":inline(chunk,"Initial state"),"teaching_sequence":chunk[sequence_start:sequence_end],
                       "verification":chunk[sequence_end].split(":",1)[1].strip(),"runtime_rule":inline(chunk,"Runtime rule")})
    return result


def compile_lesson() -> dict:
    digest = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    if digest != EXPECTED_HASH:
        raise ValueError(f"Gold Pack hash mismatch: {digest}")
    all_lines = lines_from_docx(SOURCE)
    lines = all_lines[all_lines.index("Lesson 6 Variables on both sides"):all_lines.index("Lesson 7 Bracket equations")]
    vocabulary = between(lines,"Vocabulary","Concept teaching")[2:]
    diagnoses = between(lines,"Misconception diagnosis and repair","Worked example bank")[3:]
    diagnostic = between(lines,"Entry diagnostic","Misconception diagnosis and repair")
    result = {"source_document":SOURCE.name,"source_sha256":digest,"id":value(lines,"Stable lesson ID"),
              "title":lines[0].removeprefix("Lesson 6 "),
              "estimated_minutes":int(re.search(r"\d+",value(lines,"Estimated time")).group()),
              "mastery_threshold":int(value(lines,"Mastery threshold").rstrip("%"))/100,
              "objective":after(lines,"Learning objective"),"why_it_matters":after(lines,"Why it matters"),
              "prerequisites":between(lines,"Prerequisites","Vocabulary"),
              "vocabulary":[{"term":vocabulary[i],"meaning":vocabulary[i+1]} for i in range(0,len(vocabulary),2)],
              "concept_teaching":between(lines,"Concept teaching","Entry diagnostic"),
              "entry_diagnostic":{k.casefold().replace(" ","_"):value(diagnostic,k) for k in ("Prompt","Answer","Failure route")},
              "misconceptions":[{"tag":diagnoses[i],"diagnosis":diagnoses[i+1],"repair":diagnoses[i+2]}
                                for i in range(0,len(diagnoses),3)],
              "worked_examples":worked(between(lines,"Worked example bank","Independent practice")),
              "practice_questions":bank(between(lines,"Independent practice","Mastery assessment"),"p",15),
              "mastery_questions":bank(between(lines,"Mastery assessment","Reteaching rules"),"m",5),
              "repair_rules":between(lines,"Reteaching rules","Parallel reassessment"),
              "reassessment_questions":bank(between(lines,"Parallel reassessment","Lesson summary"),"r",3),
              "summary":between(lines,"Lesson summary","Implementation acceptance checklist")}
    ids = [q["id"] for name in ("worked_examples","practice_questions","mastery_questions","reassessment_questions") for q in result[name]]
    if len(ids)!=38 or len(set(ids))!=38:
        raise ValueError("Lesson 6 needs 38 unique question IDs")
    return result


if __name__ == "__main__":
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    OUTPUT.write_text(json.dumps(compile_lesson(),ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(OUTPUT)
