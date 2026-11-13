"""Independent arithmetic, source integrity and public gates for Topic 7."""
import json
import math
from hashlib import sha256
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from app.curriculum.grade11 import GRADE_11
from app.curriculum.grade11.assessment_triangle_rules import BANKS
from app.curriculum.validation import validate_curriculum
from app.practice.catalog import PRACTICE_BANKS

ROOT=Path(__file__).resolve().parents[2]
def rad(deg):return math.radians(deg)
def n(value):return f'{value:.2f}'

def test_triangle_rule_lessons_and_independent_calculations():
    assert validate_curriculum([GRADE_11])==[]
    topic=GRADE_11.topics[6]
    assert topic.id=='trigonometry-sine-cosine-area-rules' and topic.paper=='Paper 2'
    assert len(topic.subtopics[0].lessons)==5
    count=0
    for number,lesson in enumerate(topic.subtopics[0].lessons,1):
        assert lesson.status.value=='teacher_review_required' and not lesson.release_approved
        assert len(lesson.whiteboard_questions)==len(PRACTICE_BANKS[lesson.id])==15
        assert tuple(map(len,BANKS[number][:3]))==(15,5,3)
        source=ROOT/'docs/curriculum/grade11/triangle-rules'/lesson.source_document
        assert sha256(source.read_bytes()).hexdigest()==lesson.source_sha256
        bank=json.loads((ROOT/f'backend/app/curriculum/grade11/generated/triangle_rules_{number:02}.json').read_text())
        assert len({q['problem'] for q in bank['worked']})==15
        for case in bank['worked']:
            v=case['visual']['values'];mode=v['mode'];answer=case['answer']
            assert len(case['actions'])==5 and answer in case['check']
            if mode=='sine_side':
                assert n(v['b']) in answer
                assert math.isclose(v['a']/math.sin(rad(v['A'])),v['b']/math.sin(rad(v['B'])),rel_tol=1e-12)
            elif mode=='ambiguous':
                assert 0<v['A']+v['B1']<180 and 0<v['A']+v['B2']<180
                assert math.isclose(v['B1']+v['B2'],180,abs_tol=1e-12)
                for B in (v['B1'],v['B2']):
                    assert math.isclose(math.sin(rad(B)),v['b']*math.sin(rad(v['A']))/v['a'],rel_tol=1e-12)
                    assert n(B) in answer
            elif mode=='cosine_side':
                assert math.isclose(v['a']**2,v['b']**2+v['c']**2-2*v['b']*v['c']*math.cos(rad(v['A'])),rel_tol=1e-12)
                assert n(v['a']) in answer
            elif mode=='cosine_angle':
                assert abs(v['b']-v['c'])<v['a']<v['b']+v['c']
                assert math.isclose(v['a']**2,v['b']**2+v['c']**2-2*v['b']*v['c']*math.cos(rad(v['A'])),rel_tol=1e-12)
                assert n(v['A']) in answer
            elif mode=='area':
                assert math.isclose(v['area'],v['b']*v['c']*math.sin(rad(v['A']))/2,rel_tol=1e-12)
                assert n(v['area']) in answer
        for section in ('practice','mastery','reassessment'):
            for item in bank[section]:
                assert len(set(item['options']))==4
                assert item['options'][item['answer_index']] in item['memo']
        count+=sum(len(bank[s]) for s in ('worked','practice','mastery','reassessment'))
    assert count==190

def test_triangle_rule_public_previews_hide_answers_and_reveal_steps(monkeypatch):
    monkeypatch.setattr('app.api.v1.lessons.enforce_lesson_access',lambda *a:None)
    with TestClient(app) as client:
        for number in range(1,6):
            response=client.get(f'/api/v1/lessons/g11-rules-{number:02}')
            assert response.status_code==200,response.text
            payload=response.json()
            assert payload['paper']=='Paper 2'
            for question in payload['whiteboard_questions']:
                assert question['solution_gated'] and question['total_step_count']==5
                assert len(question['whiteboard']['steps'])==1
                assert 'answer' not in question and 'full_memo' not in question
                scene=json.loads(question['whiteboard']['visualization']['parameters']['scene_json'])
                assert not any(k in scene for k in ('actions','answer','check'))
                v=scene['visual']['values']
                assert not any(k in v for k in ('B1','B2','area'))
                if v['mode']=='sine_side':assert 'b' not in v
                if v['mode']=='cosine_side':assert 'a' not in v
                if v['mode']=='cosine_angle':assert 'A' not in v
            qid=payload['whiteboard_questions'][0]['id']
            reveal=client.post(f'/api/v1/lessons/g11-rules-{number:02}/questions/{qid}/reveal')
            assert reveal.status_code==200,reveal.text
            assert len(reveal.json()['whiteboard']['steps'])==5
