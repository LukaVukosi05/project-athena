"""Independent calculations and public gates for Grade 11 Topic 6."""
import json
import math
from hashlib import sha256
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from app.curriculum.grade11 import GRADE_11
from app.curriculum.grade11.assessment_functions import BANKS
from app.curriculum.validation import validate_curriculum
from app.practice.catalog import PRACTICE_BANKS

DATA=Path(__file__).resolve().parents[1]/'app/curriculum/grade11/generated'
SOURCES=Path(__file__).resolve().parents[2]/'docs/curriculum/grade11/functions-graphs'

def numeric(text):
    text=text.replace('−','-').replace('√2',str(math.sqrt(2))).replace('√3',str(math.sqrt(3)))
    a,*tail=text.split('/')
    return float(a)/float(tail[0]) if tail else float(a)

def test_eight_function_lessons_have_correct_features_and_complete_banks():
    assert validate_curriculum([GRADE_11])==[]
    topic=GRADE_11.topics[5]
    assert (topic.id,topic.paper,topic.term)==('functions-graphs','Both',2)
    assert len(topic.subtopics[0].lessons)==8
    total=0
    for n,lesson in enumerate(topic.subtopics[0].lessons,1):
        assert lesson.status.value=='teacher_review_required' and not lesson.release_approved
        assert lesson.paper==('Paper 1' if n<=4 else 'Paper 2')
        assert len(lesson.whiteboard_questions)==len(PRACTICE_BANKS[lesson.id])==15
        assert tuple(map(len,BANKS[n][:3]))==(15,5,3)
        assert sha256((SOURCES/lesson.source_document).read_bytes()).hexdigest()==lesson.source_sha256
        bank=json.loads((DATA/f'functions_{n:02}.json').read_text())
        assert len({s['problem'] for s in bank['worked']})==15
        for scene in bank['worked']:
            v=scene['visual']['values'];answer=scene['answer']
            assert len(scene['actions'])==5 and answer in scene['check']
            if n==1:assert v['vertex']==[-v['p'],v['q']] and answer==str(tuple(v['vertex']))
            if n==2:assert v['vertical']==-v['p'] and v['horizontal']==v['q']
            if n==3:assert v['target_y']==v['a']*v['b']+v['q'] and v['target_x']+v['p']==1
            if n==4:
                f=lambda x:v['a']*(x+v['p'])**2+v['q']
                assert (v['y0'],v['y1'])==(f(v['x0']),f(v['x1']))
                assert v['slope']*(v['x1']-v['x0'])==v['y1']-v['y0']
            if n==5:
                value=getattr(math,v['fn'])(math.radians(v['theta']))
                assert math.isclose(value,numeric(v['result']),abs_tol=1e-9),scene['id']
            if n in (6,8):
                assert v['period']==(180 if v['fn']=='tan' else 360)//v['k']
            if n==7:assert v['shift']==-v['p']
        for section in ('practice','mastery','reassessment'):
            for item in bank[section]:
                assert len(set(item['options']))==4
                assert item['options'][item['answer_index']] in item['memo']
                assert not any('alternative' in option for option in item['options'])
        total+=sum(len(bank[s]) for s in ('worked','practice','mastery','reassessment'))
    assert total==304

def test_public_function_previews_hide_results_and_reveal_five_steps(monkeypatch):
    monkeypatch.setattr('app.api.v1.lessons.enforce_lesson_access',lambda *a:None)
    with TestClient(app) as client:
        for n in range(1,9):
            response=client.get(f'/api/v1/lessons/g11-fn-{n:02}')
            assert response.status_code==200,response.text
            payload=response.json()
            assert payload['paper']==('Paper 1' if n<=4 else 'Paper 2')
            for q in payload['whiteboard_questions']:
                assert q['solution_gated'] and q['total_step_count']==5
                assert len(q['whiteboard']['steps'])==1
                assert 'answer' not in q and 'full_memo' not in q
                scene=json.loads(q['whiteboard']['visualization']['parameters']['scene_json'])
                assert not any(k in scene for k in ('actions','answer','check'))
                assert not any(k in scene['visual']['values'] for k in
                    ('vertex','vertical','horizontal','target_y','y0','y1','slope','result','period','shift'))
            qid=payload['whiteboard_questions'][0]['id']
            reveal=client.post(f'/api/v1/lessons/g11-fn-{n:02}/questions/{qid}/reveal')
            assert reveal.status_code==200
            assert len(reveal.json()['whiteboard']['steps'])==5
