"""Topic 10 source, mathematical invariants and public answer gates."""
import hashlib,json
from fractions import Fraction
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app
from app.curriculum.grade9.whole_numbers_runtime import GRADE_9,SHAPE_LESSONS
from app.curriculum.grade9.assessment_whole_numbers import SHAPE_BANKS
from app.curriculum.validation import validate_curriculum
from app.practice.service import check_answer
from app.visualization.registry import validate_visualization
ROOT=Path(__file__).resolve().parents[2]

def test_all_eight_authored_lessons_match_their_diagrams_and_banks():
    topic=GRADE_9.topics[9]
    assert topic.id=='geometry-of-2d-shapes' and topic.product_order==10
    assert [l.id for l in topic.subtopics[0].lessons]==[f'g9-shapes-{n:02}' for n in range(1,9)]
    assert not [error for error in validate_curriculum([GRADE_9]) if error.grade_id=='grade-9']
    manifest=json.loads((ROOT/'docs/curriculum/grade9/geometry-of-2d-shapes/topic10-acceptance-manifest.json').read_text())
    assert len(manifest)==8
    for n,(lesson,data) in SHAPE_LESSONS.items():
        practice,mastery,reassessment,repairs,rules=SHAPE_BANKS[n]
        assert (len(data['worked']),len(practice),len(mastery),len(reassessment))==(15,15,5,3)
        assert repairs and rules and not lesson.release_approved
        assert len({c['problem'] for c in data['worked']})==15
        if n==1:assert {c['visual']['values']['model'] for c in data['worked']}=={'isosceles','equilateral','right'}
        if n==3:assert {c['visual']['values']['model'] for c in data['worked']}=={'parallelogram','rectangle','rhombus','trapezium','square','kite'}
        if n==4:assert {c['visual']['values']['model'] for c in data['worked']}=={'regular_polygon','diagonals'}
        if n==5:assert {c['visual']['values']['criterion'] for c in data['worked']}=={'SAS','SSS','ASA'}
        if n==6:assert {c['visual']['values']['criterion'] for c in data['worked']}=={'given','AA','SAS','SSS'}
        assert len({c['prompt'] for c in data['practice']+data['mastery']+data['reassessment']})==23
        source=(ROOT/'docs/curriculum/grade9/geometry-of-2d-shapes'/data['source']).read_bytes()
        assert manifest[n-1]['source_sha256']==hashlib.sha256(source).hexdigest()
        for scene,q in zip(data['worked'],lesson.whiteboard_questions):
            v=scene['visual']['values'];target=v['target']
            assert len(q.whiteboard.steps)==5 and scene['actions'][-1]==scene['check']
            assert q.whiteboard.visualization.type=='geometry'
            assert validate_visualization(q.whiteboard) is None
            if n in (7,8):assert v['apex']+2*target==180
            elif n==1:
                assert (v['apex']+2*target==180 if v['model']=='isosceles' else target==60 if v['model']=='equilateral' else v['given']+target==90)
            elif n==2:assert v['left']+v['right']==target
            elif n==3:assert (v['given']+target==180 if v['model'] in ('parallelogram','rhombus','trapezium') else v['given']==target)
            elif n==4:
                assert (target==(v['sides']-2)*180 and v['each']==str(Fraction(target,v['sides'])) if v['model']=='regular_polygon' else target==v['given'])
            elif n==5:assert v['sides'][2]==target
            else:assert v['criterion'] in ('given','AA','SAS','SSS') and target==(v['small']+2)*v['scale']
        for q in practice:
            assert len(set(q.options))==4 and check_answer(q.id,q.accepted_answers[0])
            assert all(not check_answer(q.id,wrong) for wrong in q.options if wrong!=q.accepted_answers[0])

def test_public_lesson_previews_are_gated_and_reveals_complete():
    with TestClient(app) as client:
        topic=client.get('/api/v1/curriculum/grades/grade-9/topics/geometry-of-2d-shapes')
        assert topic.status_code==200 and len(topic.json()['subtopics'][0]['lessons'])==8
        for n in range(1,9):
            lesson_id=f'g9-shapes-{n:02}'
            public=client.get(f'/api/v1/lessons/{lesson_id}')
            assert public.status_code==200
            for q in public.json()['whiteboard_questions']:
                assert q['solution_gated'] and len(q['whiteboard']['steps'])==1
                assert 'answer' not in q and 'full_memo' not in q
                scene=json.loads(q['whiteboard']['visualization']['parameters']['scene_json'])
                assert scene['visual']['family']=='shapes' and scene['visual']['values']['lesson']==n
                assert 'target' not in scene['visual']['values'] and 'each' not in scene['visual']['values']
                assert not {'answer','actions','check'}&scene.keys()
                reveal=client.post(f'/api/v1/lessons/{lesson_id}/questions/{q["id"]}/reveal')
                assert reveal.status_code==200 and len(reveal.json()['whiteboard']['steps'])==q['total_step_count']
            practice=client.get(f'/api/v1/practice/{lesson_id}')
            mastery=client.get(f'/api/v1/practice/{lesson_id}/mastery')
            assert practice.status_code==mastery.status_code==200
            assert len(practice.json()['questions'])==15 and len(mastery.json()['questions'])==5
            assert all('accepted_answers' not in q for q in practice.json()['questions'])


def test_shape_validator_rejects_a_diagram_answer_mismatch():
    from copy import deepcopy
    import pytest
    original=SHAPE_LESSONS[5][0].whiteboard_questions[0].whiteboard
    board=deepcopy(original)
    scene=json.loads(board.visualization.parameters['scene_json'])
    scene['visual']['values']['target']+=1
    board.visualization.parameters['scene_json']=json.dumps(scene)
    with pytest.raises(ValueError,match='Shape calculation'):
        validate_visualization(board)
