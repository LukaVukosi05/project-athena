import copy,json
from hashlib import sha256
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.curriculum.grade10 import GRADE_10
from app.curriculum.grade10.algebra import LESSONS
from app.curriculum.grade10.assessment import ALGEBRA_BANKS
from app.curriculum.validation import validate_curriculum
from app.visualization.registry import _grade10_algebra_board
ROOT=Path(__file__).resolve().parents[2]
def test_six_source_backed_lessons_and_assessments():
 topic=GRADE_10.topics[0]
 assert topic.id=='algebraic-expressions' and topic.term==1 and topic.paper=='Paper 1'
 assert [lesson.id for lesson in topic.subtopics[0].lessons]==[f'g10-algebra-{n:02}' for n in range(1,7)]
 assert not [e for e in validate_curriculum([GRADE_10]) if e.grade_id=='grade-10']
 manifest=json.loads((ROOT/'docs/curriculum/grade10/algebraic-expressions/topic01-acceptance-manifest.json').read_text())
 for n,(lesson,data) in LESSONS.items():
  practice,mastery,reassessment,repairs,rules=ALGEBRA_BANKS[n]
  assert (len(data['worked']),len(practice),len(mastery),len(reassessment))==(15,15,5,3)
  assert all(q.type=='multiple_choice' and len(set(q.options))==4 for q in practice)
  assert all(len(q.whiteboard.steps)==5 for q in lesson.whiteboard_questions)
  assert len({q['problem'] for q in data['worked']})==15
  assert sha256((ROOT/'docs/curriculum/grade10/algebraic-expressions'/data['source']).read_bytes()).hexdigest()==manifest[n-1]['source_sha256']
@pytest.mark.parametrize('n,key,mutation',[ (1,'radicand',1),(2,'lower',1),(3,'coefficients',None),(4,'coefficients',None),(5,'cube',1),(6,'excluded',1)])
def test_tampered_math_rejected(n,key,mutation):
 q=copy.deepcopy(LESSONS[n][1]['worked'][0]);v=q['visual']['values']
 if mutation is None:v[key]['0']+=1
 else:v[key]+=mutation
 p={'scene_json':json.dumps(q),'question_id':q['id'],'prompt':q['problem'],'total_steps':5}
 with pytest.raises(ValueError):_grade10_algebra_board(p,n)
def test_real_numbers_and_algebraic_fractions_cover_both_cases():
 number_cases=LESSONS[1][1]['worked']
 assert {'rational','irrational'}=={q['visual']['values']['kind'] for q in number_cases}
 fractions=LESSONS[6][1]['worked']
 assert {'simplify','combine'}=={q['visual']['values']['kind'] for q in fractions}
 assert {'+','−'}=={q['visual']['values'].get('operator') for q in fractions if q['visual']['values']['kind']=='combine'}
 assert all('x ≠' in q['answer'] for q in fractions)

def test_direct_urls_answer_gate_and_grade11_topic1_is_visible():
 with TestClient(app) as client:
  grade=client.get('/api/v1/curriculum/grades/grade-10');topic=client.get('/api/v1/curriculum/grades/grade-10/topics/algebraic-expressions')
  assert grade.status_code==topic.status_code==200
  assert len(grade.json()['topics'])==10
  assert len(topic.json()['subtopics'][0]['lessons'])==6
  assert [topic['id'] for topic in client.get('/api/v1/curriculum/grades/grade-11').json()['topics']]==['exponents-and-surds','equations-and-inequalities','trigonometry-reduction-and-equations','euclidean-geometry','analytical-geometry','functions-graphs','trigonometry-sine-cosine-area-rules','statistics-data-handling','probability','finance-growth-decay']
  for n in range(1,7):
   lesson=client.get(f'/api/v1/lessons/g10-algebra-{n:02}')
   assert lesson.status_code==200,lesson.text
   payload=lesson.json();assert len(payload['whiteboard_questions'])==15
   for q in payload['whiteboard_questions']:
    assert 'answer' not in q and len(q['whiteboard']['steps'])==1
    scene=json.loads(q['whiteboard']['visualization']['parameters']['scene_json'])
    assert 'answer' not in scene and 'actions' not in scene
    assert not {'coefficients','excluded','first','second','decimal','a','b','lower','upper'} & scene['visual']['values'].keys()
   revealed=client.post(f'/api/v1/lessons/g10-algebra-{n:02}/questions/g10-aex-l{n:02}-w01/reveal')
   assert revealed.status_code==200
   assert len(revealed.json()['whiteboard']['steps'])==5
