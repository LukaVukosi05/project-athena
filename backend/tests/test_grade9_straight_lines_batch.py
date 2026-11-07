"""Angle geometry sources, mathematical checks, public reveal and practice gates."""
import hashlib,json
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app
from app.curriculum.grade9.whole_numbers_runtime import GRADE_9,LINE_LESSONS
from app.curriculum.grade9.assessment_whole_numbers import LINE_BANKS
from app.curriculum.validation import validate_curriculum
from app.practice.service import check_answer
from app.visualization.registry import validate_visualization
ROOT=Path(__file__).resolve().parents[2]

def test_five_angle_lessons_and_question_owned_mathematics():
    topic=GRADE_9.topics[8]
    assert topic.id=='geometry-of-straight-lines' and topic.product_order==9
    assert [l.id for l in topic.subtopics[0].lessons]==[f'g9-straight-lines-{n:02}' for n in range(1,6)]
    assert not [e for e in validate_curriculum([GRADE_9]) if e.grade_id=='grade-9']
    manifest=json.loads((ROOT/'docs/curriculum/grade9/geometry-of-straight-lines/topic9-acceptance-manifest.json').read_text())
    assert len(manifest)==5
    for n,(lesson,data) in LINE_LESSONS.items():
        practice,mastery,reassess,repairs,rules=LINE_BANKS[n]
        assert (len(data['worked']),len(practice),len(mastery),len(reassess))==(15,15,5,3)
        assert repairs and rules and not lesson.release_approved
        assert len({c['problem'] for c in data['worked']})==15
        assert len({c['prompt'] for c in data['practice']+data['mastery']+data['reassessment']})==23
        assert not {x['problem'] for x in data['worked']}&{x['prompt'] for x in data['practice']}
        source=(ROOT/'docs/curriculum/grade9/geometry-of-straight-lines'/data['source']).read_bytes()
        assert manifest[n-1]['source_sha256']==hashlib.sha256(source).hexdigest()
        for scene,q in zip(data['worked'],lesson.whiteboard_questions):
            v=scene['visual']['values'];theta=v['theta']
            assert 40<=theta<=84 and scene['actions'][-1]==scene['check']
            assert len(q.whiteboard.steps)==len(scene['actions'])
            assert q.whiteboard.visualization.type=='geometry'
            if n==1:assert v['target']==(theta if v['relation']=='vertical' else 90-theta if v['relation']=='right' else 180-theta)
            elif n in (2,5):assert v['target']==theta and v['given']==(180-theta if v['relation']=='cointerior' else theta)
            elif n==3:assert v['target']+v['given']==180 and v['middle']==theta
            else:assert v['coefficient']*v['solution']+v['constant']==v['target']==180-theta
            if n==5:assert v['claimed']!=v['target']
        for q in practice:
            assert len(set(q.options))==4 and check_answer(q.id,q.accepted_answers[0])
            assert all(not check_answer(q.id,other) for other in q.options if other!=q.accepted_answers[0])

def test_five_line_lessons_open_with_gated_preview_and_complete_reveal():
    with TestClient(app) as client:
        topic=client.get('/api/v1/curriculum/grades/grade-9/topics/geometry-of-straight-lines')
        assert topic.status_code==200 and len(topic.json()['subtopics'][0]['lessons'])==5
        for n in range(1,6):
            lesson_id=f'g9-straight-lines-{n:02}'
            public=client.get(f'/api/v1/lessons/{lesson_id}')
            assert public.status_code==200
            for q in public.json()['whiteboard_questions']:
                assert q['solution_gated'] and len(q['whiteboard']['steps'])==1
                assert 'answer' not in q and 'full_memo' not in q
                scene=json.loads(q['whiteboard']['visualization']['parameters']['scene_json'])
                assert scene['visual']=={'family':'givens'} and not {'answer','actions','check'}&scene.keys()
                full=client.post(f'/api/v1/lessons/{lesson_id}/questions/{q["id"]}/reveal')
                assert full.status_code==200 and len(full.json()['whiteboard']['steps'])==q['total_step_count']
            practice=client.get(f'/api/v1/practice/{lesson_id}')
            mastery=client.get(f'/api/v1/practice/{lesson_id}/mastery')
            assert practice.status_code==mastery.status_code==200
            assert len(practice.json()['questions'])==15 and len(mastery.json()['questions'])==5
            assert all('accepted_answers' not in item for item in practice.json()['questions'])
