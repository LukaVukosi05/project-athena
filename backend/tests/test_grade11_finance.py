"""Grade 11 finance content, arithmetic and public answer gates."""
import json
from decimal import Decimal, ROUND_HALF_UP
from hashlib import sha256
from pathlib import Path
from fastapi.testclient import TestClient
from app.curriculum.grade11 import GRADE_11
from app.curriculum.grade11.assessment_finance import BANKS
from app.curriculum.validation import validate_curriculum
from app.main import app
from app.practice.catalog import PRACTICE_BANKS

ROOT=Path(__file__).resolve().parents[2]
D=Decimal
R=lambda x:x.quantize(D('.01'),rounding=ROUND_HALF_UP)

def expected(v):
 mode=v['mode']
 if mode=='exchange':
  return D(v['quantity'])*D(v['new']) if v['direction']=='foreign_to_rand' else D(v['quantity'])/D(v['new'])
 p=D(v['principal']);r=D(v['rate']);n=v.get('years',1)
 if mode=='growth':return p*(1+r*n) if v['simple'] else p*(1+r)**n
 if mode=='hire':
  balance=p*(1-D(v['deposit_rate']))
  return (balance*(1+r*n))/v['months']
 if mode in ('inflation','population'):return p*(1+r)**n
 if mode=='decay':return p*(1-r*n) if v['simple'] else p*(1-r)**n
 if mode in ('effective','rate_diagnosis'):
  return ((1+r/v['periods'])**v['periods']-1)*100
 if mode=='growth_then_decay':return p*(1+r)**n*(1-D(v['decline']))
 if mode=='compare_methods':return p*(1+r)**n
 raise AssertionError(mode)

def test_finance_six_lessons_and_all_question_arithmetic():
 assert validate_curriculum([GRADE_11])==[]
 topic=GRADE_11.topics[9]
 assert (topic.id,topic.paper,topic.term)==('finance-growth-decay','Paper 1',3)
 assert len(topic.subtopics[0].lessons)==6
 modes=set()
 for n,lesson in enumerate(topic.subtopics[0].lessons,1):
  assert lesson.status.value=='teacher_review_required' and not lesson.release_approved
  assert len(lesson.whiteboard_questions)==len(PRACTICE_BANKS[lesson.id])==15
  assert tuple(map(len,BANKS[n][:3]))==(15,5,3)
  source=ROOT/'docs/curriculum/grade11/finance-growth-decay'/lesson.source_document
  assert sha256(source.read_bytes()).hexdigest()==lesson.source_sha256
  bank=json.loads((ROOT/f'backend/app/curriculum/grade11/generated/finance_{n:02}.json').read_text())
  assert len({q['problem'] for q in bank['worked']})==15
  for q in bank['worked']:
   v=q['visual']['values'];modes.add(v['mode']);answer=q['answer']
   assert len(q['actions'])==5 and answer in q['check']
   value=expected(v)
   rounded=str(R(value))
   if v['mode']=='population':rounded=str(value.quantize(D(1),rounding=ROUND_HALF_UP))
   if v['mode'] in ('effective','rate_diagnosis'):rounded=str(R(value))
   assert rounded in answer.replace(',',''),(q['id'],answer,rounded)
  for section,count in [('practice',15),('mastery',5),('reassessment',3)]:
   assert len(bank[section])==count
   for q in bank[section]:
    assert len(set(q['options']))==4 and q['options'][q['answer_index']] in q['memo']
 assert modes=={'growth','hire','inflation','population','exchange','decay','effective','growth_then_decay','compare_methods','rate_diagnosis'}

def test_finance_public_preview_reveal_and_practice(monkeypatch):
 monkeypatch.setattr('app.api.v1.lessons.enforce_lesson_access',lambda *a:None)
 with TestClient(app) as client:
  for n in range(1,7):
   response=client.get(f'/api/v1/lessons/g11-fin-{n:02}')
   assert response.status_code==200,response.text
   payload=response.json();assert payload['paper']=='Paper 1'
   for q in payload['whiteboard_questions']:
    assert q['solution_gated'] and q['total_step_count']==5
    assert len(q['whiteboard']['steps'])==1
    assert 'answer' not in q and 'full_memo' not in q
    scene=json.loads(q['whiteboard']['visualization']['parameters']['scene_json'])
    assert not any(key in scene for key in ('answer','actions','check'))
   qid=payload['whiteboard_questions'][0]['id']
   revealed=client.post(f'/api/v1/lessons/g11-fin-{n:02}/questions/{qid}/reveal')
   assert revealed.status_code==200,revealed.text
   assert len(revealed.json()['whiteboard']['steps'])==5
