"""Capture and classify every active whiteboard visual from the live curriculum API."""
from __future__ import annotations
import hashlib,json,urllib.request
from pathlib import Path

BASE="http://127.0.0.1:8010/api/v1"
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"artifacts"/"visualization-audit"
GENERIC={
 "statistics:balance_and_rank","statistics:spread_number_line",
}
def get(path):
 with urllib.request.urlopen(BASE+path) as response:return json.load(response)
def main():
 rows=[];grade=get("/curriculum/grades/grade-12")
 for topic in grade["topics"]:
  detail=get(f"/curriculum/grades/grade-12/topics/{topic['id']}")
  for subtopic in detail["subtopics"]:
   for summary in subtopic["lessons"]:
    if summary["status"]=="coming_soon":continue
    lesson=get(f"/lessons/{summary['id']}")
    for question in lesson.get("whiteboard_questions",[]):
     board=question["whiteboard"];visual=board.get("visualization");steps=board.get("steps",[])
     semantic={item["id"] for item in board.get("semantic_objects",[])}
     targets={target for step in steps for event in step.get("events",[]) for target in event.get("targets",[])}
     states=[step.get("visualization_state") for step in steps]
     key=f"{visual['type']}:{visual['template']}" if visual else "missing"
     params=visual.get("parameters",{}) if visual else {}
     reasons=[]
     if not visual:reasons.append("missing")
     if key in GENERIC:reasons.append("generic shared renderer")
     if params and set(params)<= {"prompt","answer","method","family","objects"}:reasons.append("not linked to numerical question values")
     if not targets<=semantic:reasons.append("event targets missing semantic objects")
     if not steps or any(not step.get("events") for step in steps):reasons.append("not animated")
     if len({json.dumps(state,sort_keys=True) for state in states})<=1 and len(states)>1:reasons.append("visualization_state reused across steps")
     if all(step.get("before_expression")==step.get("after_expression") for step in steps):reasons.append("visually identical operation states")
     rows.append({
      "topic_id":topic["id"],"lesson_id":lesson["id"],"question_id":question["id"],"problem":board.get("problem",question.get("problem","")),
      "whiteboard_id":board["id"],"visualization.type":visual.get("type") if visual else None,
      "visualization.template":visual.get("template") if visual else None,
      "visualization.parameters":params,"visualization_state":states,
      "semantic_objects":board.get("semantic_objects",[]),
      "timeline_events":[event for step in steps for event in step.get("events",[])],
      "audit_reasons":reasons,
     })
 fingerprints={}
 for row in rows:
  fingerprint=hashlib.sha256(json.dumps(row["visualization.parameters"],sort_keys=True).encode()).hexdigest()
  fingerprints.setdefault((row["visualization.type"],row["visualization.template"],fingerprint),[]).append(row)
 for group in fingerprints.values():
  prompts={row["problem"] for row in group}
  if len(group)>1 and len(prompts)>1:
   for row in group:row["audit_reasons"].append(f"visual parameters reused by {len(group)} questions")
 OUT.mkdir(parents=True,exist_ok=True)
 (OUT/"whiteboard-payloads.json").write_text(json.dumps(rows,indent=2),encoding="utf-8")
 lines=["| topic_id | lesson_id | question_id | template | audit |","|---|---|---|---|---|"]
 for row in rows:
  lines.append("| "+ " | ".join([row["topic_id"],row["lesson_id"],row["question_id"],f"{row['visualization.type']}:{row['visualization.template']}",", ".join(row["audit_reasons"]) or "pass"])+" |")
 (OUT/"whiteboard-audit.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
 summary={}
 for row in rows:
  status="pass" if not row["audit_reasons"] else "flagged"
  summary[status]=summary.get(status,0)+1
 print(json.dumps({"examples":len(rows),**summary,"output":str(OUT)},indent=2))
if __name__=="__main__":main()
