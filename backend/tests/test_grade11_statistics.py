"""Independent data arithmetic, source provenance and hidden-answer contracts."""
import json
import math
from hashlib import sha256
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from app.curriculum.grade11 import GRADE_11
from app.curriculum.grade11.assessment_statistics import BANKS
from app.curriculum.validation import validate_curriculum
from app.practice.catalog import PRACTICE_BANKS

ROOT=Path(__file__).resolve().parents[2]
def quartiles(x):
    a=sorted(x);h=len(a)//2
    return [a[0],(a[1]+a[2])/2,a[h],(a[h+2]+a[h+3])/2,a[-1]]

def test_statistics_seven_lessons_and_all_calculations():
    assert validate_curriculum([GRADE_11])==[]
    topic=GRADE_11.topics[7]
    assert (topic.id,topic.paper,topic.term)==('statistics-data-handling','Paper 2',3)
    assert len(topic.subtopics[0].lessons)==7
    count=0
    for number,lesson in enumerate(topic.subtopics[0].lessons,1):
        assert lesson.status.value=='teacher_review_required' and not lesson.release_approved
        assert len(lesson.whiteboard_questions)==len(PRACTICE_BANKS[lesson.id])==15
        assert tuple(map(len,BANKS[number][:3]))==(15,5,3)
        source=ROOT/'docs/curriculum/grade11/statistics'/lesson.source_document
        assert sha256(source.read_bytes()).hexdigest()==lesson.source_sha256
        data=json.loads((ROOT/f'backend/app/curriculum/grade11/generated/statistics_{number:02}.json').read_text())
        assert len({q['problem'] for q in data['worked']})==15
        for scene in data['worked']:
            v=scene['visual']['values'];mode=v['mode'];answer=scene['answer']
            assert len(scene['actions'])==5 and answer in scene['check']
            if mode=='ungrouped':
                assert v['sum']==sum(v['data'])
                assert math.isclose(v['mean'],sum(v['data'])/len(v['data']))
                assert f"{v['mean']:.2f}" in answer
            elif mode=='grouped':
                freq=v['frequencies'];mids=[v['start']+(j+.5)*v['width'] for j in range(5)]
                assert v['total']==sum(freq) and mids==v['midpoints']
                assert v['weighted']==sum(a*b for a,b in zip(mids,freq))
                assert math.isclose(v['mean'],v['weighted']/v['total'])
                assert f"{v['mean']:.2f}" in answer
            elif mode in ('box','outlier'):
                assert v['data']==sorted(v['data']) and quartiles(v['data'])==v['five']
                assert v['iqr']==v['five'][3]-v['five'][1]
                if mode=='outlier':
                    assert v['upper_fence']==v['five'][3]+1.5*v['iqr']
                    assert v['data'][-1]>v['upper_fence']>=v['data'][-2]
                    assert str(v['data'][-1]) in answer
                else:assert f'IQR = {v["iqr"]:g}' in answer
            elif mode=='histogram':
                assert v['peak']==v['frequencies'].index(max(v['frequencies']))
                assert str(v['start']+v['peak']*v['width']) in answer
            elif mode=='ogive':
                assert v['cumulative'][0]==0
                assert [v['cumulative'][j+1]-v['cumulative'][j] for j in range(5)]==v['frequencies']
                assert v['total']==v['cumulative'][-1] and v['total']%2==1
                rank=(v['total']+1)//2
                idx=next(j for j in range(5) if v['cumulative'][j]<rank<=v['cumulative'][j+1])
                assert v['median_class']==idx and str(v['start']+idx*v['width']) in answer
            elif mode=='deviation':
                x=v['data'];mean=sum(x)/len(x)
                assert math.isclose(v['mean'],mean)
                assert math.isclose(v['squares'],sum((a-mean)**2 for a in x))
                assert math.isclose(v['variance'],v['squares']/len(x))
                assert math.isclose(v['sd'],math.sqrt(v['variance']))
                assert f"{v['sd']:.2f}" in answer
            else:
                assert mode=='scatter'
                y=v['y'];d=[y[j+1]-y[j] for j in range(5)]
                assert d==v['first_differences']
                assert [d[j+1]-d[j] for j in range(4)]==v['second_differences']
                inferred='linear' if len(set(d))==1 else 'quadratic' if len(set(v['second_differences']))==1 else 'exponential'
                assert v['model']==inferred and inferred in answer
        for section in ('practice','mastery','reassessment'):
            for item in data[section]:
                assert len(set(item['options']))==4
                assert item['options'][item['answer_index']] in item['memo']
        count+=sum(len(data[s]) for s in ('worked','practice','mastery','reassessment'))
    assert count==266

def test_statistics_public_previews_and_reveal(monkeypatch):
    monkeypatch.setattr('app.api.v1.lessons.enforce_lesson_access',lambda *a:None)
    with TestClient(app) as client:
        for number in range(1,8):
            response=client.get(f'/api/v1/lessons/g11-stat-{number:02}')
            assert response.status_code==200,response.text
            payload=response.json();assert payload['paper']=='Paper 2'
            for q in payload['whiteboard_questions']:
                assert q['solution_gated'] and q['total_step_count']==5
                assert len(q['whiteboard']['steps'])==1
                assert 'answer' not in q and 'full_memo' not in q
                scene=json.loads(q['whiteboard']['visualization']['parameters']['scene_json'])
                assert not any(k in scene for k in ('actions','answer','check'))
                assert not any(k in scene['visual']['values'] for k in
                               ('mean','five','iqr','cumulative','variance','sd','model','peak','median_class'))
            qid=payload['whiteboard_questions'][0]['id']
            reveal=client.post(f'/api/v1/lessons/g11-stat-{number:02}/questions/{qid}/reveal')
            assert reveal.status_code==200,reveal.text
            assert len(reveal.json()['whiteboard']['steps'])==5
