"""Grade 9 Topic 14 source, mathematical model, answer gates and assessment."""
import hashlib,json
from copy import deepcopy
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.curriculum.grade9.whole_numbers_runtime import GRADE_9,SOLID_LESSONS
from app.curriculum.grade9.assessment_whole_numbers import SOLID_BANKS
from app.curriculum.validation import validate_curriculum
from app.practice.service import check_answer
from app.visualization.registry import validate_visualization
ROOT=Path(__file__).resolve().parents[2]
def test_four_complete_solid_lessons_and_source_hashes():
 topic=GRADE_9.topics[13]
 assert topic.id=='geometry-of-3d-objects' and topic.product_order==14 and topic.term==4
 assert [l.id for l in topic.subtopics[0].lessons]==[f'g9-solid-{n:02}' for n in range(1,5)]
 assert not [e for e in validate_curriculum([GRADE_9]) if e.grade_id=='grade-9']
 manifest=json.loads((ROOT/'docs/curriculum/grade9/geometry-of-3d-objects/topic14-acceptance-manifest.json').read_text())
 assert len(manifest)==4
 for n,(lesson,data) in SOLID_LESSONS.items():
  practice,mastery,reassess,repairs,rules=SOLID_BANKS[n]
  assert (len(data['worked']),len(practice),len(mastery),len(reassess))==(15,15,5,3)
  assert repairs and rules and not lesson.release_approved
  assert len({x['problem'] for x in data['worked']})==15
  source=(ROOT/'docs/curriculum/grade9/geometry-of-3d-objects'/data['source']).read_bytes()
  assert manifest[n-1]['source_sha256']==hashlib.sha256(source).hexdigest()
  for scene,q in zip(data['worked'],lesson.whiteboard_questions):
   assert len(q.whiteboard.steps)==5 and scene['actions'][-1]==scene['check']
   assert q.whiteboard.visualization.type=='geometry'
   assert validate_visualization(q.whiteboard) is None
  for question in practice:
   assert len(set(question.options))==4 and check_answer(question.id,question.accepted_answers[0])
   assert all(not check_answer(question.id,x) for x in question.options if x!=question.accepted_answers[0])
@pytest.mark.parametrize('number,field',[(1,'edges'),(3,'faces'),(4,'faces')])
def test_tampered_solid_face_counts_rejected(number,field):
 board=deepcopy(SOLID_LESSONS[number][0].whiteboard_questions[0].whiteboard)
 scene=json.loads(board.visualization.parameters['scene_json']);scene['visual']['values'][field]+=1
 board.visualization.parameters['scene_json']=json.dumps(scene)
 with pytest.raises(ValueError,match='Solid answer or pictured faces'):validate_visualization(board)
def test_public_previews_and_four_lessons_load():
 with TestClient(app) as client:
  topic=client.get('/api/v1/curriculum/grades/grade-9/topics/geometry-of-3d-objects')
  assert topic.status_code==200 and len(topic.json()['subtopics'][0]['lessons'])==4
  for n in range(1,5):
   lid=f'g9-solid-{n:02}';resp=client.get(f'/api/v1/lessons/{lid}')
   assert resp.status_code==200
   for q in resp.json()['whiteboard_questions']:
    assert q['solution_gated'] and len(q['whiteboard']['steps'])==1
    assert 'answer' not in q and 'full_memo' not in q
    scene=json.loads(q['whiteboard']['visualization']['parameters']['scene_json'])
    assert scene['visual']['family']=='solids' and not {'answer','actions','check'}&scene.keys()
    assert not {'target','parts','missing','faces','edges','vertices'}&scene['visual']['values'].keys()
    reveal=client.post(f'/api/v1/lessons/{lid}/questions/{q["id"]}/reveal')
    assert reveal.status_code==200 and len(reveal.json()['whiteboard']['steps'])==q['total_step_count']
   practice=client.get(f'/api/v1/practice/{lid}');mastery=client.get(f'/api/v1/practice/{lid}/mastery')
   assert practice.status_code==mastery.status_code==200
   assert len(practice.json()['questions'])==15 and len(mastery.json()['questions'])==5
   assert all('accepted_answers' not in x for x in practice.json()['questions'])
