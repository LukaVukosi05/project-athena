"""Topic 11 measurement math, source integrity and answer gating."""
import hashlib,json,math
from copy import deepcopy
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.curriculum.grade9.whole_numbers_runtime import GRADE_9,AREA_LESSONS
from app.curriculum.grade9.assessment_whole_numbers import AREA_BANKS
from app.curriculum.validation import validate_curriculum
from app.practice.service import check_answer
from app.visualization.registry import validate_visualization
ROOT=Path(__file__).resolve().parents[2]

def test_five_measurement_lessons_have_checked_math_and_separate_banks():
    topic=GRADE_9.topics[10]
    assert topic.id=='area-and-perimeter' and topic.product_order==11
    assert [l.id for l in topic.subtopics[0].lessons]==[f'g9-area-{n:02}' for n in range(1,6)]
    assert not [e for e in validate_curriculum([GRADE_9]) if e.grade_id=='grade-9']
    manifest=json.loads((ROOT/'docs/curriculum/grade9/area-and-perimeter/topic11-acceptance-manifest.json').read_text())
    assert len(manifest)==5
    for n,(lesson,data) in AREA_LESSONS.items():
        practice,mastery,reassess,repairs,rules=AREA_BANKS[n]
        assert (len(data['worked']),len(practice),len(mastery),len(reassess))==(15,15,5,3)
        assert repairs and rules and not lesson.release_approved
        assert len({x['problem'] for x in data['worked']})==15
        assert len({x['prompt'] for name in ('practice','mastery','reassessment') for x in data[name]})==23
        source=(ROOT/'docs/curriculum/grade9/area-and-perimeter'/data['source']).read_bytes()
        assert manifest[n-1]['source_sha256']==hashlib.sha256(source).hexdigest()
        modes=set()
        for scene,q in zip(data['worked'],lesson.whiteboard_questions):
            v=scene['visual']['values'];L,W=v['length'],v['width']
            assert len(q.whiteboard.steps)==5 and scene['actions'][-1]==scene['check']
            assert q.whiteboard.visualization.type=='geometry'
            assert validate_visualization(q.whiteboard) is None
            if n==1:assert v['length_mm']==10*L and v['area']==L*W and v['perimeter']==2*(L+W)
            elif n==2:assert v['area']==L*W-v['cut_width']*v['cut_height'] and v['perimeter']==2*(L+W)
            elif n==3:
                assert v['diameter']==2*v['radius'] and v['area_coefficient']==v['radius']**2
                assert f'≈ {math.pi*v["diameter"]:.2f} cm' in scene['answer']
                assert f'≈ {math.pi*v["radius"]**2:.2f} cm²' in scene['answer']
            elif n==4:
                modes.add(v['mode'])
                assert v['mode'] in ('both','length_only','width_only') and v['new_area']==v['scaled_length']*v['scaled_width'] and v['new_perimeter']==2*(v['scaled_length']+v['scaled_width'])
            else:assert v['path_area']==(L+2*v['path'])*(W+2*v['path'])-L*W
        if n==4:assert modes=={'both','length_only','width_only'}
        for q in practice:
            assert len(set(q.options))==4 and check_answer(q.id,q.accepted_answers[0])
            assert all(not check_answer(q.id,wrong) for wrong in q.options if wrong!=q.accepted_answers[0])

def test_mismatched_area_value_is_rejected():
    board=deepcopy(AREA_LESSONS[5][0].whiteboard_questions[0].whiteboard)
    scene=json.loads(board.visualization.parameters['scene_json'])
    scene['visual']['values']['path_area']+=1
    board.visualization.parameters['scene_json']=json.dumps(scene)
    with pytest.raises(ValueError,match='Area measure'):
        validate_visualization(board)

def test_five_lessons_open_with_question_specific_gated_previews():
    with TestClient(app) as client:
        topic=client.get('/api/v1/curriculum/grades/grade-9/topics/area-and-perimeter')
        assert topic.status_code==200 and len(topic.json()['subtopics'][0]['lessons'])==5
        for n in range(1,6):
            lid=f'g9-area-{n:02}';public=client.get(f'/api/v1/lessons/{lid}')
            assert public.status_code==200
            for q in public.json()['whiteboard_questions']:
                assert q['solution_gated'] and len(q['whiteboard']['steps'])==1
                assert 'answer' not in q and 'full_memo' not in q
                v=json.loads(q['whiteboard']['visualization']['parameters']['scene_json'])
                assert v['visual']['family']=='area' and v['visual']['values']['lesson']==n
                assert not {'answer','actions','check'}&v.keys()
                assert not {'area','perimeter','path_area','new_area','fence','diameter'}&v['visual']['values'].keys()
                reveal=client.post(f'/api/v1/lessons/{lid}/questions/{q["id"]}/reveal')
                assert reveal.status_code==200 and len(reveal.json()['whiteboard']['steps'])==q['total_step_count']
            practice=client.get(f'/api/v1/practice/{lid}');mastery=client.get(f'/api/v1/practice/{lid}/mastery')
            assert practice.status_code==mastery.status_code==200
            assert len(practice.json()['questions'])==15 and len(mastery.json()['questions'])==5
            assert all('accepted_answers' not in item for item in practice.json()['questions'])
