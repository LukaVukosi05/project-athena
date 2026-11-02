"""Exact Grade 8 decimal values, private banks and question-specific whiteboard contract."""
import json
from copy import deepcopy
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import get_settings
from app.curriculum.grade8.decimals_runtime import LESSON_1,LESSON_2,SCENES_1,SCENES_2
from app.curriculum.grade8.assessment_decimals import banks
from app.curriculum.grade8.decimal_math import solution
from app.curriculum.grade8.structure import GRADE_8
from app.curriculum.validation import validate_curriculum
from app.visualization.registry import CATALOGUE

def test_exact_answers_and_registered_whiteboard_states():
 assert not [e for e in validate_curriculum([GRADE_8]) if e.topic_id=='decimal-fractions']
 for n,lesson,scenes in ((1,LESSON_1,SCENES_1),(2,LESSON_2,SCENES_2)):
  assert len(lesson.whiteboard_questions)==len(scenes)==15
  assert len({s['problem'] for s in scenes})==15
  p,m,r,repairs,rules=banks(n)
  assert (len(p),len(m),len(r))==(15,5,3) and repairs and rules
  assert set(q.prompt for q in p).isdisjoint(s['problem'] for s in scenes)
  for scene,q in zip(scenes,lesson.whiteboard_questions,strict=True):
   answer,rows,problem,check=solution(scene['kind'],scene['values'])
   assert (answer,rows,problem,check)==(scene['answer'],scene['rows'],scene['problem'],scene['memo'])
   assert q.id==scene['id'] and len(q.whiteboard.steps)==5
   assert q.whiteboard.visualization.template==('grade8_decimal_columns' if n==1 else 'grade8_decimal_rounding')
   assert all(step.narration==next(event.text for event in step.events if event.type=='caption') for step in q.whiteboard.steps)
  params=deepcopy(lesson.whiteboard_questions[0].whiteboard.visualization.parameters)
  scene=json.loads(params['scene_json']);scene['answer']='999';params['scene_json']=json.dumps(scene)
  with pytest.raises(ValueError):CATALOGUE[('algebra',lesson.whiteboard_questions[0].whiteboard.visualization.template)].validate(params)
  valid=lesson.whiteboard_questions[0].whiteboard.visualization.parameters
  wrong='grade8_decimal_rounding' if n==1 else 'grade8_decimal_columns'
  with pytest.raises(ValueError):CATALOGUE[('algebra',wrong)].validate(valid)
 assert solution('round',['19.995','2'])[0]=='20.00'
 assert solution('compare',['2.5','2.50'])[0]=='='
 assert solution('estimate',['49.995','2.885','2'])[0]=='52.89'

def test_public_api_gates_answers_and_exposes_unseen_banks():
 settings=get_settings();prior=settings.unlock_all_lessons;settings.unlock_all_lessons=True
 try:
  with TestClient(app) as client:
   grade=client.get('/api/v1/curriculum/grades/grade-8').json()
   assert next(row for row in grade['topics'] if row['product_order']==9)['id']=='decimal-fractions'
   topic=client.get('/api/v1/curriculum/grades/grade-8/topics/decimal-fractions').json()
   assert [x['id'] for x in topic['subtopics'][0]['lessons']][:2]==['g8-decimal-fractions-01','g8-decimal-fractions-02']
   for n in (1,2):
    lid=f'g8-decimal-fractions-{n:02}';result=client.get('/api/v1/lessons/'+lid)
    assert result.status_code==200
    for q in result.json()['whiteboard_questions']:
     scene=json.loads(q['whiteboard']['visualization']['parameters']['scene_json'])
     assert not {'answer','memo','rows','misconception'} & scene.keys()
     assert q['solution_gated'] and len(q['whiteboard']['steps'])==1
    revealed=client.post(f'/api/v1/lessons/{lid}/questions/g8-dec-l{n:02}-w01/reveal')
    assert revealed.status_code==200 and len(revealed.json()['whiteboard']['steps'])==5
    assert len(client.get(f'/api/v1/practice/{lid}').json()['questions'])==15
    assert len(client.get(f'/api/v1/practice/{lid}/mastery').json()['questions'])==5
 finally:settings.unlock_all_lessons=prior
