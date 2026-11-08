import copy
import json
from hashlib import sha256
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.curriculum.grade9.whole_numbers_runtime import GRADE_9, TRANSFORM_LESSONS
from app.curriculum.validation import validate_curriculum
from app.visualization.registry import _grade9_transform_board
ROOT=Path(__file__).resolve().parents[2]
def test_all_seven_lessons_have_valid_source_and_independent_assessments():
 topic=GRADE_9.topics[15]
 assert topic.id=='transformation-geometry' and topic.product_order==16 and topic.term==4
 assert [l.id for l in topic.subtopics[0].lessons]==[f'g9-tg-{n:02}' for n in range(1,8)]
 assert not [e for e in validate_curriculum([GRADE_9]) if e.grade_id=='grade-9']
 manifest=json.loads((ROOT/'docs/curriculum/grade9/transformation-geometry/topic16-acceptance-manifest.json').read_text())
 for n,(lesson,data) in TRANSFORM_LESSONS.items():
  assert len(data['worked'])==len(data['practice'])==15
  assert len(data['mastery'])==5 and len(data['reassessment'])==3
  assert len({q['problem'] for q in data['worked']})==15
  assert all(len(q.whiteboard.steps)==5 for q in lesson.whiteboard_questions)
  assert sha256((ROOT/'docs/curriculum/grade9/transformation-geometry'/data['source']).read_bytes()).hexdigest()==manifest[n-1]['source_sha256']
  for q in data['worked']:
   assert q['answer'].split(';')[0] in q['actions'][-1] or n in (5,7)
   p={'scene_json':json.dumps(q),'question_id':q['id'],'prompt':q['problem'],'total_steps':5}
   _grade9_transform_board(p,n)
@pytest.mark.parametrize('n',[1,2,3,4,5,6,7])
def test_wrong_image_or_original_rejected(n):
 q=copy.deepcopy(TRANSFORM_LESSONS[n][1]['worked'][0]);p={'question_id':q['id'],'prompt':q['problem'],'total_steps':5}
 q['visual']['values']['image'][1][0]+=1
 p['scene_json']=json.dumps(q)
 with pytest.raises(ValueError,match='contradicts'): _grade9_transform_board(p,n)
def test_public_payload_and_direct_urls_gate_answers():
 with TestClient(app) as client:
  response=client.get('/api/v1/curriculum/grades/grade-9/topics/transformation-geometry')
  assert response.status_code==200
  for n in range(1,8):
   lesson=client.get(f'/api/v1/lessons/g9-tg-{n:02}')
   assert lesson.status_code==200,lesson.text
   public=lesson.json()
   assert len(public['whiteboard_questions'])==15
   for q in public['whiteboard_questions']:
    assert 'answer' not in q and len(q['whiteboard']['steps'])==1
    scene=json.loads(q['whiteboard']['visualization']['parameters']['scene_json'])
    assert scene['visual']['family']=='transformation'
    assert 'image' not in scene['visual']['values'] and 'rule' not in scene['visual']['values'] and 'answer' not in scene
