"""Exact powers/roots and authentic unit-aware contexts with gated solutions."""
import json
from copy import deepcopy
from fractions import Fraction
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import get_settings
from app.curriculum.grade8.fractions_runtime import LESSON_5,LESSON_6,SCENES_5,SCENES_6
from app.curriculum.grade8.fractions_math import answer,value
from app.curriculum.grade8.assessment_fractions_56 import banks
from app.curriculum.grade8.structure import GRADE_8
from app.curriculum.validation import validate_curriculum
from app.visualization.registry import CATALOGUE,validate_visualization

def test_original_scenes_are_exact_and_all_learning_contracts_hold():
 for n,lesson,scenes in ((5,LESSON_5,SCENES_5),(6,LESSON_6,SCENES_6)):
  assert len(scenes)==len(lesson.whiteboard_questions)==15
  assert len({s['problem'] for s in scenes})==15
  assert not [e for e in validate_curriculum([GRADE_8]) if e.lesson_id==lesson.id]
  p,m,r,repairs,rules=banks(n)
  assert (len(p),len(m),len(r))==(15,5,3) and repairs and rules
  for q,s,practice in zip(lesson.whiteboard_questions,scenes,p,strict=True):
   op=s['operation'] if n==6 else s['exponent']
   assert answer(s['kind'],s['values'],op)==s['answer']
   assert q.id==s['id'] and len(q.whiteboard.steps)==5
   assert q.whiteboard.visualization.template=='grade8_fraction_powers_context'
   assert validate_visualization(q.whiteboard) is None
   assert practice.prompt!=s['problem'] and practice.answer_hidden_before_submission
   assert all(step.narration==next(e.text for e in step.events if e.type=='caption') for step in q.whiteboard.steps)

def test_roots_are_positive_and_exact_and_contexts_keep_units():
 assert answer('root',['121/144'],2)=='11/12'
 assert answer('root',['64/125'],3)=='4/5'
 with pytest.raises(ValueError):answer('root',['2/3'],2)
 for scene in SCENES_6:
  assert scene['unit'] and scene['answer_unit']
  if scene['operation']=='divide':
   assert value(scene['values'][1])>0
   assert scene['answer_unit'] in {'ribbons','bottles','servings','litres per learner'}

def test_visual_validator_rejects_wrong_result_and_missing_context_unit():
 validate=CATALOGUE[('algebra','grade8_fraction_powers_context')].validate
 for lesson in (LESSON_5,LESSON_6):
  params=deepcopy(lesson.whiteboard_questions[0].whiteboard.visualization.parameters)
  s=json.loads(params['scene_json']);s['answer']='999';params['scene_json']=json.dumps(s)
  with pytest.raises(ValueError):validate(params)
  if lesson==LESSON_6:
   s['answer']='18';s['unit']='';params['scene_json']=json.dumps(s)
   with pytest.raises(ValueError):validate(params)

def test_catalogue_api_gates_worked_answers_and_exposes_independent_practice():
 settings=get_settings();old=settings.unlock_all_lessons;settings.unlock_all_lessons=True
 try:
  with TestClient(app) as client:
   topic=client.get('/api/v1/curriculum/grades/grade-8/topics/common-fractions')
   assert topic.status_code==200
   assert [x['id'] for x in topic.json()['subtopics'][0]['lessons']][:6]==[f'g8-common-fractions-{n:02}' for n in range(1,7)]
   for n in (5,6):
    lid=f'g8-common-fractions-{n:02}'
    response=client.get('/api/v1/lessons/'+lid)
    assert response.status_code==200
    for q in response.json()['whiteboard_questions']:
     public_scene=json.loads(q['whiteboard']['visualization']['parameters']['scene_json'])
     assert not {'answer','memo','rows','misconception'}&public_scene.keys()
     assert len(q['whiteboard']['steps'])==1 and q['solution_gated']
    revealed=client.post(f'/api/v1/lessons/{lid}/questions/g8-frac-l{n:02}-w01/reveal')
    assert revealed.status_code==200 and len(revealed.json()['whiteboard']['steps'])==5
    assert len(client.get(f'/api/v1/practice/{lid}').json()['questions'])==15
    assert len(client.get(f'/api/v1/practice/{lid}/mastery').json()['questions'])==5
 finally:settings.unlock_all_lessons=old
