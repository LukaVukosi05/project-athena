"""Source integrity, decimal calculations and public answer gating."""
import copy,json
from decimal import Decimal,ROUND_HALF_UP
from hashlib import sha256
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.curriculum.grade10.algebra import GRADE_10,FIN_LESSONS
from app.curriculum.grade10.assessment import FIN_BANKS
from app.curriculum.validation import validate_curriculum
from app.visualization.registry import _grade10_fin_board
ROOT=Path(__file__).resolve().parents[2]
def test_finance_bank_and_calculations():
 assert (GRADE_10.topics[8].id,GRADE_10.topics[8].paper)==('finance-and-growth','Paper 1')
 assert not [e for e in validate_curriculum([GRADE_10]) if e.grade_id=='grade-10']
 manifest=json.loads((ROOT/'docs/curriculum/grade10/finance-and-growth/topic09-acceptance-manifest.json').read_text())
 for n,(lesson,data) in FIN_LESSONS.items():
  practice,mastery,reassessment,_,_=FIN_BANKS[n]
  assert (len(lesson.whiteboard_questions),len(practice),len(mastery),len(reassessment))==(15,15,5,3)
  assert all(len(q.whiteboard.steps)==5 for q in lesson.whiteboard_questions)
  assert all(q.type=='multiple_choice' and len(set(q.options))==4 for q in practice)
  assert sha256((ROOT/'docs/curriculum/grade10/finance-and-growth'/data['source']).read_bytes()).hexdigest()==manifest[n-1]['source_sha256']
  for q in data['worked']:
   p={'scene_json':json.dumps(q),'question_id':q['id'],'prompt':q['problem'],'total_steps':5};_grade10_fin_board(p,n)
   bad=copy.deepcopy(q);bad['visual']['values']['principal']='1';p['scene_json']=json.dumps(bad)
   with pytest.raises(ValueError):_grade10_fin_board(p,n)
   v=q['visual']['values'];amount=Decimal(v.get('amount','0'));principal=Decimal(v['principal']);rate=Decimal(v['rate']);years=Decimal(v['years'])
   if v['mode']==1:assert amount==principal+Decimal(v['interest']) and Decimal(v['interest'])==(principal*rate*years).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)
   if v['mode']==2:assert amount==(principal*(1+rate)**int(years)).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)
   if v.get('unit')=='people':assert amount==(principal*(1+rate)**int(years)).quantize(Decimal('1'),rounding=ROUND_HALF_UP)
   if v.get('direction')=='compare':assert Decimal(v['difference'])==Decimal(v['amount'])-Decimal(v['old_amount'])
   if v['mode']==4:assert Decimal(v['balance'])==principal-Decimal(v['deposit']) and Decimal(v['instalment'])==(amount/Decimal(v['months'])).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)
def test_public_preview_hides_derived_values():
 with TestClient(app) as client:
  topic=client.get('/api/v1/curriculum/grades/grade-10/topics/finance-and-growth');assert topic.status_code==200
  for n in range(1,7):
   response=client.get(f'/api/v1/lessons/g10-fin-{n:02}');assert response.status_code==200,response.text
   for q in response.json()['whiteboard_questions']:
    assert 'answer' not in q and len(q['whiteboard']['steps'])==1
    scene=json.loads(q['whiteboard']['visualization']['parameters']['scene_json'])
    assert not {'answer','actions'} & scene.keys()
    assert not {'answer','amount','interest','simple','deposit','balance','instalment','old_amount','difference'} & scene['visual']['values'].keys()
   revealed=client.post(f'/api/v1/lessons/g10-fin-{n:02}/questions/g10-fin-l{n:02}-w01/reveal')
   assert revealed.status_code==200 and len(revealed.json()['whiteboard']['steps'])==5
