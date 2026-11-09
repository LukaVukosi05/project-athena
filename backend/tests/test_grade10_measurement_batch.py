"""Measurement source, solid geometry and public answer gate checks."""
import copy,json,math
from hashlib import sha256
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.curriculum.grade10.algebra import GRADE_10,MEAS_LESSONS
from app.curriculum.grade10.assessment import MEAS_BANKS
from app.curriculum.validation import validate_curriculum
from app.visualization.registry import _grade10_meas_board
ROOT=Path(__file__).resolve().parents[2]
def test_source_and_shapes():
 topic=GRADE_10.topics[9];assert (topic.id,topic.term,topic.paper)==('measurement',4,'Paper 2')
 assert not [e for e in validate_curriculum([GRADE_10]) if e.grade_id=='grade-10']
 manifest=json.loads((ROOT/'docs/curriculum/grade10/measurement/topic10-acceptance-manifest.json').read_text())
 for n,(lesson,data) in MEAS_LESSONS.items():
  assert lesson.paper=='Paper 2'
  practice,mastery,reassessment,_,_=MEAS_BANKS[n]
  assert (len(data['worked']),len(practice),len(mastery),len(reassessment))==(15,15,5,3)
  assert all(len(q.whiteboard.steps)==5 for q in lesson.whiteboard_questions)
  assert all(q.type=='multiple_choice' and len(set(q.options))==4 for q in practice)
  assert sha256((ROOT/'docs/curriculum/grade10/measurement'/data['source']).read_bytes()).hexdigest()==manifest[n-1]['source_sha256']
  for q in data['worked']:
   p={'scene_json':json.dumps(q),'question_id':q['id'],'prompt':q['problem'],'total_steps':5};_grade10_meas_board(p,n)
   bad=copy.deepcopy(q);bad['visual']['values']['volume']+=1;p['scene_json']=json.dumps(bad)
   with pytest.raises(ValueError):_grade10_meas_board(p,n)
   v=q['visual']['values'];shape=v['shape'];r=v.get('r');h=v.get('h')
   if shape=='prism':
    a=v.get('scaled_a',v['a']);b=v.get('scaled_b',v['b']);height=v.get('scaled_h',h)
    assert v['volume']==a*b*height and v['surface']==2*(a*b+a*height+b*height)
   elif shape=='cylinder':assert v['volume']==r*r*h and v['surface']==2*r*h+(r*r if v['open_top'] else 2*r*r)
   elif shape=='sphere':assert v['volume']==4*r**3//3 and v['surface']==4*r*r
   elif shape=='hemisphere':assert v['volume']==2*r**3//3 and v['surface']==3*r*r
   elif shape=='cone':assert v['slant']**2==r*r+h*h and v['volume']==r*r*h//3 and v['surface']==r*v['slant']+r*r
   elif shape=='pyramid':assert v['slant']**2==h*h+(v['b']//2)**2 and v['volume']==v['b']**2*h//3 and v['surface']==v['b']**2+2*v['b']*v['slant']
   else:assert v['volume']==r*r*h+2*r**3//3 and v['surface']==2*r*h+3*r*r

def test_preview_and_reveal():
 with TestClient(app) as client:
  topic=client.get('/api/v1/curriculum/grades/grade-10/topics/measurement');assert topic.status_code==200
  assert len(topic.json()['subtopics'][0]['lessons'])==6
  for n in range(1,7):
   resp=client.get(f'/api/v1/lessons/g10-meas-{n:02}');assert resp.status_code==200,resp.text
   for q in resp.json()['whiteboard_questions']:
    assert 'answer' not in q and len(q['whiteboard']['steps'])==1
    scene=json.loads(q['whiteboard']['visualization']['parameters']['scene_json'])
    assert not {'answer','actions'} & scene.keys()
    assert not {'answer','volume','surface','scaled_a','scaled_b','scaled_h','slant','cylinder_volume','hemisphere_volume'} & scene['visual']['values'].keys()
   revealed=client.post(f'/api/v1/lessons/g10-meas-{n:02}/questions/g10-meas-l{n:02}-w01/reveal')
   assert revealed.status_code==200 and len(revealed.json()['whiteboard']['steps'])==5
