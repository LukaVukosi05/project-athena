import json
from copy import deepcopy
from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.core.config import get_settings
from app.curriculum.grade8.exponents_runtime import LESSON_1,LESSON_2,SCENES_1,SCENES_2
from app.curriculum.grade8.exponent_math import solve
from app.curriculum.grade8.assessment_exponents import banks
from app.curriculum.grade8.structure import GRADE_8
from app.curriculum.validation import validate_curriculum
from app.visualization.registry import CATALOGUE

def test_exact_questions_and_distinct_private_banks():
 assert not [e for e in validate_curriculum([GRADE_8]) if e.topic_id=='exponents']
 for n,lesson,scenes in ((1,LESSON_1,SCENES_1),(2,LESSON_2,SCENES_2)):
  p,m,r,repairs,rules=banks(n)
  assert (len(scenes),len(lesson.whiteboard_questions),len(p),len(m),len(r))==(15,15,15,5,3)
  assert set(q.prompt for q in p).isdisjoint(s['problem'] for s in scenes)
  for scene,q in zip(scenes,lesson.whiteboard_questions,strict=True):
   assert solve(scene['kind'],scene['values'])==(scene['answer'],scene['rows'],scene['problem'],scene['memo'])
   assert len(q.whiteboard.steps)==len(scene['rows'])+2
   assert all(step.narration==next(e.text for e in step.events if e.type=='caption') for step in q.whiteboard.steps)
  params=deepcopy(lesson.whiteboard_questions[0].whiteboard.visualization.parameters)
  tampered=json.loads(params['scene_json']);tampered['answer']='999';params['scene_json']=json.dumps(tampered)
  with pytest.raises(ValueError):CATALOGUE[('algebra',lesson.whiteboard_questions[0].whiteboard.visualization.template)].validate(params)
 assert solve('negative',['-3','3'])[0]=='-27'
 assert solve('science',['70500'])[0]=='7.05 × 10^4'
 assert solve('quotient',['9','5','5'])[0]=='1'
 assert solve('power_product',['2','3','2'])[0]=='36'
 assert solve('mixed',['3','4','2','3'])[0]=='27'
 assert '⁴' in solve('compare',['2','4','15'])[2]
 assert all(' + ' not in s['problem'] or s['kind']=='mixed' for s in SCENES_2)
 assert '(3+2)² = 25' in next(s['misconception'] for s in SCENES_2 if s['kind']=='power_product')

def test_catalogue_and_initial_answer_gate():
 settings=get_settings();prior=settings.unlock_all_lessons;settings.unlock_all_lessons=True
 try:
  with TestClient(app) as client:
   topic=client.get('/api/v1/curriculum/grades/grade-8/topics/exponents')
   assert topic.status_code==200
   assert [x['id'] for x in topic.json()['subtopics'][0]['lessons']]==[f'g8-exponents-{k:02}' for k in range(1,7)]
   for n in (1,2):
    lid=f'g8-exponents-{n:02}';response=client.get(f'/api/v1/lessons/{lid}')
    assert response.status_code==200
    for q in response.json()['whiteboard_questions']:
     scene=json.loads(q['whiteboard']['visualization']['parameters']['scene_json'])
     assert not {'answer','memo','rows','misconception'}&scene.keys()
     assert len(q['whiteboard']['steps'])==1 and q['solution_gated']
    assert client.post(f'/api/v1/lessons/{lid}/questions/g8-exp-l{n:02}-w01/reveal').status_code==200
    assert len(client.get(f'/api/v1/practice/{lid}').json()['questions'])==15
 finally:settings.unlock_all_lessons=prior
