"""Quadratic patterns: independent arithmetic and public answer gating."""
import json
from hashlib import sha256
from pathlib import Path
from fastapi.testclient import TestClient
from app.curriculum.grade11 import GRADE_11
from app.curriculum.grade11.assessment_patterns import BANKS
from app.curriculum.validation import validate_curriculum
from app.main import app
from app.practice.catalog import PRACTICE_BANKS
ROOT=Path(__file__).resolve().parents[2]

def test_authored_patterns_and_independent_arithmetic():
 assert validate_curriculum([GRADE_11])==[]
 topic=GRADE_11.topics[10]
 assert (topic.id,topic.term,topic.paper)==('quadratic-number-patterns',4,'Paper 1')
 assert len(topic.subtopics[0].lessons)==5
 modes=set()
 for n,lesson in enumerate(topic.subtopics[0].lessons,1):
  assert lesson.status.value=='teacher_review_required' and not lesson.release_approved
  assert len(lesson.whiteboard_questions)==len(PRACTICE_BANKS[lesson.id])==15
  assert tuple(map(len,BANKS[n][:3]))==(15,5,3)
  source=ROOT/'docs/curriculum/grade11/quadratic-number-patterns'/lesson.source_document
  assert sha256(source.read_bytes()).hexdigest()==lesson.source_sha256
  bank=json.loads((ROOT/f'backend/app/curriculum/grade11/generated/patterns_{n:02}.json').read_text())
  assert len({q['problem'] for q in bank['worked']})==15
  for q in bank['worked']:
   v=q['visual']['values'];mode=v['mode'];modes.add(mode)
   terms=v['terms'];first=[y-x for x,y in zip(terms,terms[1:])]
   second=[y-x for x,y in zip(first,first[1:])]
   assert len(set(second))==1 and second[0]!=0
   a=second[0]//2;b=first[0]-3*a;c=terms[0]-a-b
   assert [a*k*k+b*k+c for k in range(1,6)]==terms
   assert len(q['actions'])==5 and q['answer'] in q['check']
   target=v['target'];value=a*target*target+b*target+c
   if mode=='difference':assert q['answer']==f'Quadratic; T₆ = {a*36+b*6+c}'
   if mode=='figural':
    assert q['answer']==f'T{target} = {value} tiles'
    assert a==1 and b==v['columns_offset'] and c==v['extra']
   if mode=='diagnosis':assert q['answer']==f'T{target} = {value}'
   if mode=='position':
    assert q['answer']==f'n = {target}' and str(value) in q['problem']
    assert all(a*k*k+b*k+c!=value for k in range(1,target))
  for section,count in [('practice',15),('mastery',5),('reassessment',3)]:
   assert len(bank[section])==count
   for item in bank[section]:
    assert len(set(item['options']))==4
    assert item['options'][item['answer_index']] in item['memo']
 assert modes=={'difference','rule','position','figural','diagnosis'}

def test_pattern_public_preview_reveal(monkeypatch):
 monkeypatch.setattr('app.api.v1.lessons.enforce_lesson_access',lambda *a:None)
 with TestClient(app) as client:
  for n in range(1,6):
   response=client.get(f'/api/v1/lessons/g11-pat-{n:02}')
   assert response.status_code==200,response.text
   payload=response.json();assert payload['paper']=='Paper 1'
   for q in payload['whiteboard_questions']:
    assert q['solution_gated'] and q['total_step_count']==5
    assert len(q['whiteboard']['steps'])==1
    assert 'answer' not in q and 'full_memo' not in q
    scene=json.loads(q['whiteboard']['visualization']['parameters']['scene_json'])
    assert not any(key in scene for key in ('answer','actions','check'))
    assert 'target' not in scene['visual']['values']
   qid=payload['whiteboard_questions'][0]['id']
   revealed=client.post(f'/api/v1/lessons/g11-pat-{n:02}/questions/{qid}/reveal')
   assert revealed.status_code==200,revealed.text
   assert len(revealed.json()['whiteboard']['steps'])==5
