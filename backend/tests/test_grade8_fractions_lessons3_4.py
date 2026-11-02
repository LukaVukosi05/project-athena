"""Exact fraction products/quotients, preview gating, independent practice, and visual contracts."""
import json
from copy import deepcopy
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import get_settings
from app.curriculum.grade8.fractions_runtime import LESSON_3,LESSON_4,SCENES_3,SCENES_4
from app.curriculum.grade8.fractions_math import answer,common_denominator
from app.curriculum.grade8.assessment_fractions_operations import banks
from app.curriculum.grade8.structure import GRADE_8
from app.curriculum.validation import validate_curriculum
from app.visualization.registry import CATALOGUE,validate_visualization

def test_authored_operations_have_exact_solutions_and_complete_visual_steps():
 for n,lesson,scenes in ((3,LESSON_3,SCENES_3),(4,LESSON_4,SCENES_4)):
  assert len(scenes)==len(lesson.whiteboard_questions)==15
  assert len({s['problem'] for s in scenes})==15
  assert not [e for e in validate_curriculum([GRADE_8]) if e.lesson_id==lesson.id]
  practice,mastery,parallel,repairs,rules=banks(n)
  assert (len(practice),len(mastery),len(parallel))==(15,5,3)
  assert repairs and rules and not lesson.release_approved
  for q,s,p in zip(lesson.whiteboard_questions,scenes,practice,strict=True):
   assert q.id==s['id'] and len(q.whiteboard.steps)==5
   assert q.whiteboard.visualization.template=='grade8_fraction_operations'
   assert answer(s['kind'],s['values'])==s['answer']
   assert common_denominator(s['values'])==s['common_denominator']
   assert validate_visualization(q.whiteboard) is None
   assert p.prompt!=s['problem'] and p.answer_hidden_before_submission
   assert all(step.narration==next(ev.text for ev in step.events if ev.type=='caption') for step in q.whiteboard.steps)

def test_invalid_operation_answer_and_zero_divisor_rejected():
 validate=CATALOGUE[('algebra','grade8_fraction_operations')].validate
 params=deepcopy(LESSON_4.whiteboard_questions[0].whiteboard.visualization.parameters)
 scene=json.loads(params['scene_json']);scene['answer']='999';params['scene_json']=json.dumps(scene)
 with pytest.raises(ValueError):validate(params)
 scene['values'][1]='0';params['scene_json']=json.dumps(scene)
 with pytest.raises(ValueError):validate(params)

def test_public_preview_is_gated_and_practice_is_independent():
 settings=get_settings();old=settings.unlock_all_lessons;settings.unlock_all_lessons=True
 try:
  with TestClient(app) as client:
   for n in (3,4):
    lid=f'g8-common-fractions-{n:02}'
    preview=client.get('/api/v1/lessons/'+lid)
    assert preview.status_code==200
    for q in preview.json()['whiteboard_questions']:
     scene=json.loads(q['whiteboard']['visualization']['parameters']['scene_json'])
     assert not {'answer','memo','rows','misconception'}&scene.keys()
     assert q['solution_gated'] and len(q['whiteboard']['steps'])==1
    revealed=client.post(f'/api/v1/lessons/{lid}/questions/g8-frac-l{n:02}-w01/reveal')
    assert revealed.status_code==200 and len(revealed.json()['whiteboard']['steps'])==5
    assert len(client.get(f'/api/v1/practice/{lid}').json()['questions'])==15
    assert len(client.get(f'/api/v1/practice/{lid}/mastery').json()['questions'])==5
 finally:settings.unlock_all_lessons=old
