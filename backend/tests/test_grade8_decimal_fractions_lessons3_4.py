"""Exact decimal products, quotient digits and answer gating."""
import json
from copy import deepcopy
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import get_settings
from app.curriculum.grade8.decimals_runtime import LESSON_3,LESSON_4,SCENES_3,SCENES_4
from app.curriculum.grade8.decimal_math import operation
from app.curriculum.grade8.assessment_decimals_operations import banks
from app.curriculum.grade8.structure import GRADE_8
from app.curriculum.validation import validate_curriculum
from app.visualization.registry import CATALOGUE

def test_exact_operations_and_distinct_banks():
 assert not [e for e in validate_curriculum([GRADE_8]) if e.topic_id=='decimal-fractions']
 for n,lesson,scenes in ((3,LESSON_3,SCENES_3),(4,LESSON_4,SCENES_4)):
  assert len(lesson.whiteboard_questions)==len(scenes)==15
  p,m,r,repairs,rules=banks(n)
  assert (len(p),len(m),len(r))==(15,5,3) and repairs and rules
  assert set(q.prompt for q in p).isdisjoint(s['problem'] for s in scenes)
  for s,q in zip(scenes,lesson.whiteboard_questions,strict=True):
   assert operation(s['kind'],s['values'])==(s['answer'],s['rows'],s['problem'],s['memo'])
   assert len(q.whiteboard.steps)==len(s['rows'])+2
   assert all(step.narration==next(e.text for e in step.events if e.type=='caption') for step in q.whiteboard.steps)
  params=deepcopy(lesson.whiteboard_questions[0].whiteboard.visualization.parameters)
  s=json.loads(params['scene_json']);s['answer']='999';params['scene_json']=json.dumps(s)
  template=lesson.whiteboard_questions[0].whiteboard.visualization.template
  with pytest.raises(ValueError):CATALOGUE[('algebra',template)].validate(params)
 assert operation('multiply',['0.004','2.5'])[0]=='0.01'
 assert operation('divide',['7.875','0.35'])[0]=='22.5'
 assert operation('divide',['45.12','0.048'])[0]=='940'
 with pytest.raises(ValueError):operation('divide',['2.5','0.0'])

def test_topic_api_and_gated_answers():
 settings=get_settings();old=settings.unlock_all_lessons;settings.unlock_all_lessons=True
 try:
  with TestClient(app) as client:
   topic=client.get('/api/v1/curriculum/grades/grade-8/topics/decimal-fractions').json()
   assert [x['id'] for x in topic['subtopics'][0]['lessons']]==[f'g8-decimal-fractions-{n:02}' for n in range(1,7)]
   for n in (3,4):
    lid=f'g8-decimal-fractions-{n:02}';resp=client.get('/api/v1/lessons/'+lid)
    assert resp.status_code==200
    for q in resp.json()['whiteboard_questions']:
     scene=json.loads(q['whiteboard']['visualization']['parameters']['scene_json'])
     assert not {'answer','memo','rows','misconception'}&scene.keys()
     assert q['solution_gated'] and len(q['whiteboard']['steps'])==1 and q['total_step_count']>5
    revealed=client.post(f'/api/v1/lessons/{lid}/questions/g8-dec-l{n:02}-w01/reveal')
    assert revealed.status_code==200 and len(revealed.json()['whiteboard']['steps'])>5
    assert len(client.get(f'/api/v1/practice/{lid}').json()['questions'])==15
 finally:settings.unlock_all_lessons=old
