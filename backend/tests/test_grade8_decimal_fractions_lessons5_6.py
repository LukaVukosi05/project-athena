import json
from copy import deepcopy
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import get_settings
from app.curriculum.grade8.decimals_runtime import LESSON_5,LESSON_6,SCENES_5,SCENES_6
from app.curriculum.grade8.decimal_math import power_root
from app.curriculum.grade8.assessment_decimals_powers import banks
from app.curriculum.grade8.structure import GRADE_8
from app.curriculum.validation import validate_curriculum
from app.visualization.registry import CATALOGUE

def test_exact_scenes_and_distinct_banks():
 assert not [e for e in validate_curriculum([GRADE_8]) if e.topic_id=='decimal-fractions']
 for n,lesson,scenes in ((5,LESSON_5,SCENES_5),(6,LESSON_6,SCENES_6)):
  kind='power' if n==5 else 'root'
  p,m,r,repairs,rules=banks(n)
  assert (len(lesson.whiteboard_questions),len(scenes),len(p),len(m),len(r))==(15,15,15,5,3)
  assert len({s['problem'] for s in scenes})==15
  assert set(q.prompt for q in p).isdisjoint(s['problem'] for s in scenes)
  assert repairs and rules
  for s,q in zip(scenes,lesson.whiteboard_questions,strict=True):
   assert power_root(kind,s['values'])==(s['answer'],s['rows'],s['problem'],s['memo'])
   assert len(q.whiteboard.steps)==len(s['rows'])+2
   assert all(step.narration==next(e.text for e in step.events if e.type=='caption') for step in q.whiteboard.steps)
  params=deepcopy(lesson.whiteboard_questions[0].whiteboard.visualization.parameters)
  scene=json.loads(params['scene_json']);scene['answer']='999';params['scene_json']=json.dumps(scene)
  with pytest.raises(ValueError):CATALOGUE[('algebra',lesson.whiteboard_questions[0].whiteboard.visualization.template)].validate(params)
 assert power_root('power',['0.2','3'])[0]=='0.008'
 assert power_root('root',['0.008','3'])[0]=='0.2'
 assert power_root('root',['1.5625','2'])[0]=='1.25'
 with pytest.raises(ValueError):power_root('root',['2.0','2'])

def test_public_payload_conceals_answers():
 settings=get_settings();prior=settings.unlock_all_lessons;settings.unlock_all_lessons=True
 try:
  with TestClient(app) as client:
   topic=client.get('/api/v1/curriculum/grades/grade-8/topics/decimal-fractions').json()
   assert [x['id'] for x in topic['subtopics'][0]['lessons']]==[f'g8-decimal-fractions-{n:02}' for n in range(1,7)]
   for n in (5,6):
    lid=f'g8-decimal-fractions-{n:02}';response=client.get('/api/v1/lessons/'+lid)
    assert response.status_code==200
    for q in response.json()['whiteboard_questions']:
     scene=json.loads(q['whiteboard']['visualization']['parameters']['scene_json'])
     assert not {'answer','memo','rows','misconception'}&scene.keys()
     assert q['solution_gated'] and len(q['whiteboard']['steps'])==1 and q['total_step_count']>5
    revealed=client.post(f'/api/v1/lessons/{lid}/questions/g8-dec-l{n:02}-w01/reveal')
    assert revealed.status_code==200 and len(revealed.json()['whiteboard']['steps'])>5
    assert len(client.get(f'/api/v1/practice/{lid}').json()['questions'])==15
 finally:settings.unlock_all_lessons=prior
