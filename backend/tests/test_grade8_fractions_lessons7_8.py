"""Percent scene arithmetic, release gating and visual parameters."""
import json
from copy import deepcopy
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import get_settings
from app.curriculum.grade8.fractions_runtime import LESSON_7,LESSON_8,SCENES_7,SCENES_8
from app.curriculum.grade8.percentage_math import answer
from app.curriculum.grade8.assessment_fractions_78 import banks
from app.visualization.registry import CATALOGUE
from app.curriculum.grade8.structure import GRADE_8
from app.curriculum.validation import validate_curriculum

def test_exact_answers_repair_and_staged_scenes():
 for n,lesson,scenes in ((7,LESSON_7,SCENES_7),(8,LESSON_8,SCENES_8)):
  assert len(scenes)==len(lesson.whiteboard_questions)==15
  assert len({s['problem'] for s in scenes})==15
  assert not [e for e in validate_curriculum([GRADE_8]) if e.lesson_id==lesson.id]
  p,m,r,repairs,rules=banks(n)
  assert (len(p),len(m),len(r))==(15,5,3) and repairs and rules
  for q,s,practice in zip(lesson.whiteboard_questions,scenes,p,strict=True):
   assert s['answer']==answer(s['kind'],s['values'])
   assert q.whiteboard.visualization.template=='grade8_percentage_grid'
   assert len(q.whiteboard.steps)==5 and practice.prompt!=s['problem']
   assert all(step.narration==next(e.text for e in step.events if e.type=='caption') for step in q.whiteboard.steps)
  validator=CATALOGUE[('algebra','grade8_percentage_grid')].validate
  bad=deepcopy(lesson.whiteboard_questions[0].whiteboard.visualization.parameters)
  scene=json.loads(bad['scene_json']);scene['answer']='wrong';bad['scene_json']=json.dumps(scene)
  with pytest.raises(ValueError):validator(bad)
 assert answer('change',['105','140'])=='25% decrease'
 assert answer('convert',['17/8'])=='212.5%'

def test_public_and_revealed_question_data():
 settings=get_settings();old=settings.unlock_all_lessons;settings.unlock_all_lessons=True
 try:
  with TestClient(app) as client:
   topic=client.get('/api/v1/curriculum/grades/grade-8/topics/common-fractions').json()
   assert [x['id'] for x in topic['subtopics'][0]['lessons']][-2:]==['g8-common-fractions-07','g8-common-fractions-08']
   for n in (7,8):
    lid=f'g8-common-fractions-{n:02}'
    payload=client.get('/api/v1/lessons/'+lid);assert payload.status_code==200
    for q in payload.json()['whiteboard_questions']:
     s=json.loads(q['whiteboard']['visualization']['parameters']['scene_json'])
     assert not {'answer','rows','memo','misconception'}&s.keys()
     assert len(q['whiteboard']['steps'])==1
    revealed=client.post(f'/api/v1/lessons/{lid}/questions/g8-frac-l{n:02}-w01/reveal')
    assert revealed.status_code==200 and len(revealed.json()['whiteboard']['steps'])==5
    assert len(client.get(f'/api/v1/practice/{lid}').json()['questions'])==15
 finally:settings.unlock_all_lessons=old
