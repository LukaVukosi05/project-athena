"""Measurement review: independent area and volume checks."""
import json,math
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
from fastapi.testclient import TestClient
from app.curriculum.grade11 import GRADE_11
from app.curriculum.grade11.assessment_measurement_review import BANKS
from app.curriculum.validation import validate_curriculum
from app.main import app
from app.practice.catalog import PRACTICE_BANKS
ROOT=Path(__file__).resolve().parents[2]

def expected(v):
 mode=v['mode']
 if mode=='prism':
  l,w,h=v['l'],v['w'],v['h'];return F(l*w*h),F(2*(l*w+l*h+w*h))
 if mode=='triangular_prism':
  a,b,hyp,length=v['a'],v['b'],v['hyp'],v['length']
  assert a*a+b*b==hyp*hyp
  base=F(a*b,2)
  return base*length,2*base+(a+b+hyp)*length
 if mode=='scale':
  l,w,h,k=v['l'],v['w'],v['h'],v['k']
  if v['all_dimensions']:l,w,h=l*k,w*k,h*k
  else:h*=k
  return F(l*w*h),F(2*(l*w+l*h+w*h))
 r=v['r']
 if mode=='cylinder':return F(r*r*v['h']),F(2*r*v['h']+2*r*r)
 if mode=='sphere':return F(4*r**3,3),F(4*r*r)
 if mode=='cone':
  h=v['h'];s=math.isqrt(r*r+h*h);assert s*s==r*r+h*h
  return F(r*r*h,3),F(r*(r+s))
 if mode=='hemisphere_cylinder':
  h=v['h'];return F(r*r*h)+F(2*r**3,3),F(2*r*h+3*r*r)
 if mode=='cone_cylinder':
  h,ch=v['h'],v['cone_h'];s=math.isqrt(r*r+ch*ch);assert s*s==r*r+ch*ch
  return F(r*r*h)+F(r*r*ch,3),F(2*r*h+r*r+r*s)
 raise AssertionError(mode)

def parse(answer):
 left,right=answer.split('; exposed SA = ')
 def value(raw,unit):
  raw=raw.split('=')[-1].strip().removesuffix(unit).strip()
  return F(raw.removesuffix('π').strip('()') or '1')
 return value(left,'cm³'),value(right,'cm²')

def test_measurement_review_content_arithmetic_and_sources():
 assert validate_curriculum([GRADE_11])==[]
 topic=GRADE_11.topics[11]
 assert (topic.id,topic.term,topic.paper,topic.official_caps_topic)==('measurement-revision',4,'Paper 2','Euclidean Geometry and Measurement')
 assert len(topic.subtopics[0].lessons)==4
 modes=set()
 for n,lesson in enumerate(topic.subtopics[0].lessons,1):
  assert lesson.status.value=='teacher_review_required' and not lesson.release_approved
  assert len(lesson.whiteboard_questions)==len(PRACTICE_BANKS[lesson.id])==15
  assert tuple(map(len,BANKS[n][:3]))==(15,5,3)
  source=ROOT/'docs/curriculum/grade11/measurement-revision'/lesson.source_document
  assert sha256(source.read_bytes()).hexdigest()==lesson.source_sha256
  bank=json.loads((ROOT/f'backend/app/curriculum/grade11/generated/measurement_{n:02}.json').read_text())
  assert len({q['problem'] for q in bank['worked']})==15
  for q in bank['worked']:
   v=q['visual']['values'];modes.add(v['mode'])
   assert len(q['actions'])==5 and q['answer'] in q['check']
   assert parse(q['answer'])==expected(v),(q['id'],q['answer'])
  for section,count in [('practice',15),('mastery',5),('reassessment',3)]:
   assert len(bank[section])==count
   for item in bank[section]:
    assert len(set(item['options']))==4 and item['options'][item['answer_index']] in item['memo']
 assert modes=={'prism','triangular_prism','cylinder','scale','sphere','cone','hemisphere_cylinder','cone_cylinder'}

def test_review_public_answer_gate_and_reveal(monkeypatch):
 monkeypatch.setattr('app.api.v1.lessons.enforce_lesson_access',lambda *a:None)
 with TestClient(app) as client:
  for n in range(1,5):
   response=client.get(f'/api/v1/lessons/g11-meas-{n:02}')
   assert response.status_code==200,response.text
   payload=response.json();assert payload['paper']=='Paper 2'
   for q in payload['whiteboard_questions']:
    assert q['solution_gated'] and q['total_step_count']==5 and len(q['whiteboard']['steps'])==1
    assert 'answer' not in q and 'full_memo' not in q
    scene=json.loads(q['whiteboard']['visualization']['parameters']['scene_json'])
    assert not any(key in scene for key in ('answer','actions','check'))
   qid=payload['whiteboard_questions'][0]['id']
   reveal=client.post(f'/api/v1/lessons/g11-meas-{n:02}/questions/{qid}/reveal')
   assert reveal.status_code==200,reveal.text
   assert len(reveal.json()['whiteboard']['steps'])==5
