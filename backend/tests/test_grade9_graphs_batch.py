import hashlib,json
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app
from app.curriculum.grade9.whole_numbers_runtime import GRADE_9,GRAPH_LESSONS
from app.curriculum.grade9.assessment_whole_numbers import GRAPH_BANKS
from app.curriculum.validation import validate_curriculum
from app.practice.service import check_answer
ROOT=Path(__file__).resolve().parents[2]

def test_seven_graph_lessons_and_independent_banks():
    topic=GRADE_9.topics[7]
    assert topic.id=='graphs' and topic.product_order==8
    assert [l.id for l in topic.subtopics[0].lessons]==[f'g9-graphs-{n:02}' for n in range(1,8)]
    assert not [e for e in validate_curriculum([GRADE_9]) if e.grade_id=='grade-9']
    manifest=json.loads((ROOT/'docs/curriculum/grade9/graphs/topic8-acceptance-manifest.json').read_text())
    assert len(manifest)==7
    for n,(lesson,data) in GRAPH_LESSONS.items():
        practice,mastery,reassess,repairs,rules=GRAPH_BANKS[n]
        assert (len(data['worked']),len(practice),len(mastery),len(reassess))==(15,15,5,3)
        assert repairs and rules and not lesson.release_approved
        assert len({item['problem'] for item in data['worked']})==15
        assert len({item['prompt'] for item in [*data['practice'],*data['mastery'],*data['reassessment']]})==23
        assert not {s['problem'] for s in data['worked']} & {p['prompt'] for p in data['practice']}
        assert manifest[n-1]['source_sha256']==hashlib.sha256((ROOT/'docs/curriculum/grade9/graphs'/data['source']).read_bytes()).hexdigest()
        for scene,q in zip(data['worked'],lesson.whiteboard_questions):
            v=scene['visual']['values'];points=v['points']
            assert len(q.whiteboard.steps)==len(scene['actions'])
            assert q.whiteboard.steps[-1].after_expression.endswith(scene['check'])
            assert len({tuple(p) for p in points})==len(points)
            if n==1:assert points[1][1]==points[2][1]==v['peak'] and all(p[1]<=v['peak'] for p in points)
            else:
                assert all(y==v['m']*x+v['b'] for x,y in points)
                if n==3:assert v['rise']==v['m']*v['run'] and v['run']>0
        for q in practice:
            assert len(set(q.options))==4 and check_answer(q.id,q.accepted_answers[0])
            assert all(not check_answer(q.id,x) for x in q.options if x!=q.accepted_answers[0])

def test_public_graph_previews_and_reveal():
    with TestClient(app) as client:
        topic=client.get('/api/v1/curriculum/grades/grade-9/topics/graphs')
        assert topic.status_code==200 and len(topic.json()['subtopics'][0]['lessons'])==7
        for n in range(1,8):
            lesson_id=f'g9-graphs-{n:02}'
            public=client.get(f'/api/v1/lessons/{lesson_id}')
            assert public.status_code==200
            for q in public.json()['whiteboard_questions']:
                assert q['solution_gated'] and len(q['whiteboard']['steps'])==1
                assert 'answer' not in q and 'full_memo' not in q
                scene=json.loads(q['whiteboard']['visualization']['parameters']['scene_json'])
                assert scene['visual']=={'family':'givens'} and not {'answer','actions','check'} & scene.keys()
                full=client.post(f'/api/v1/lessons/{lesson_id}/questions/{q["id"]}/reveal')
                assert full.status_code==200 and len(full.json()['whiteboard']['steps'])==q['total_step_count']
            practice=client.get(f'/api/v1/practice/{lesson_id}')
            mastery=client.get(f'/api/v1/practice/{lesson_id}/mastery')
            assert practice.status_code==mastery.status_code==200
            assert len(practice.json()['questions'])==15 and len(mastery.json()['questions'])==5
            assert all('accepted_answers' not in x for x in practice.json()['questions'])
