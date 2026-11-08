"""Grade 10 statistics arithmetic, source integrity and public preview gates."""
import copy
import json
from fractions import Fraction
from hashlib import sha256
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.curriculum.grade10.algebra import GRADE_10,STAT_LESSONS
from app.curriculum.grade10.assessment import STAT_BANKS
from app.curriculum.validation import validate_curriculum
from app.visualization.registry import _grade10_stat_board

ROOT=Path(__file__).resolve().parents[2]

def test_six_lessons_are_source_backed_and_have_private_banks():
    topic=GRADE_10.topics[6]
    assert (topic.id,topic.term,topic.paper)==('statistics',3,'Paper 2')
    assert [l.id for l in topic.subtopics[0].lessons]==[f'g10-stat-{n:02}' for n in range(1,7)]
    assert not [e for e in validate_curriculum([GRADE_10]) if e.grade_id=='grade-10']
    manifest=json.loads((ROOT/'docs/curriculum/grade10/statistics/topic07-acceptance-manifest.json').read_text())
    for n,(lesson,data) in STAT_LESSONS.items():
        practice,mastery,reassessment,_,_=STAT_BANKS[n]
        assert (len(data['worked']),len(practice),len(mastery),len(reassessment))==(15,15,5,3)
        assert len({q['problem'] for q in data['worked']})>=10
        assert all(len(q.whiteboard.steps)==5 for q in lesson.whiteboard_questions)
        assert all(q.type=='multiple_choice' and len(set(q.options))==4 for q in practice)
        source=ROOT/'docs/curriculum/grade10/statistics'/data['source']
        assert sha256(source.read_bytes()).hexdigest()==manifest[n-1]['source_sha256']
        for q in data['worked']:
            params={'scene_json':json.dumps(q),'question_id':q['id'],'prompt':q['problem'],'total_steps':5}
            _grade10_stat_board(params,n)
            tampered=copy.deepcopy(q);tampered['visual']['values']['data'][0]+=1
            params['scene_json']=json.dumps(tampered)
            with pytest.raises(ValueError):_grade10_stat_board(params,n)

def test_derived_statistics_and_answer_keys():
    for n,(_,bank) in STAT_LESSONS.items():
        for q in bank['worked']:
            v=q['visual']['values'];data=v['data'];assert data==sorted(data) and len(data)==10
            if n==1:
                task=q['problem'].rsplit('the ',1)[-1].rstrip('.')
                if task=='mean':assert q['answer']==str(Fraction(sum(data),10))
                elif task=='median':assert q['answer']==str(Fraction(data[4]+data[5],2))
            if n in (3,4):
                assert v['summary']==[data[0],data[2],str(Fraction(data[4]+data[5],2)),data[7],data[-1]]
                if 'interquartile range' in q['problem'] or 'IQR' in q['problem']:assert q['answer']==str(data[7]-data[2])
            if n in (2,5):
                freq=v['frequencies'];assert len(freq)==4 and all(f>0 for f in freq)
                assert all(v['upper'][j]==v['lower'][j+1] for j in range(3))
                if 'total frequency' in q['problem']:assert q['answer']==str(sum(freq))
            if n==6:
                other=v['other'];assert len(other)==10
                assert other[4]+other[5]>data[4]+data[5]
                assert other[7]-other[2]>data[7]-data[2]

def test_public_payload_hides_answers_and_reveals_all_five_steps():
    with TestClient(app) as client:
        topic=client.get('/api/v1/curriculum/grades/grade-10/topics/statistics')
        assert topic.status_code==200 and len(topic.json()['subtopics'][0]['lessons'])==6
        for n in range(1,7):
            r=client.get(f'/api/v1/lessons/g10-stat-{n:02}')
            assert r.status_code==200,r.text
            for q in r.json()['whiteboard_questions']:
                assert 'answer' not in q and len(q['whiteboard']['steps'])==1
                scene=json.loads(q['whiteboard']['visualization']['parameters']['scene_json'])
                assert 'answer' not in scene and 'actions' not in scene
                assert not {'answer','summary','other_summary','q1','q3','median','minimum','maximum'} & scene['visual']['values'].keys()
            reveal=client.post(f'/api/v1/lessons/g10-stat-{n:02}/questions/g10-stat-l{n:02}-w01/reveal')
            assert reveal.status_code==200 and len(reveal.json()['whiteboard']['steps'])==5
