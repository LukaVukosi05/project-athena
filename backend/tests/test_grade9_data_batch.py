"""Grade 9 data source integrity, arithmetic and answer gates."""
import hashlib,json
from copy import deepcopy
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.curriculum.grade9.whole_numbers_runtime import GRADE_9,DATA_LESSONS
from app.curriculum.grade9.assessment_whole_numbers import DATA_BANKS
from app.curriculum.validation import validate_curriculum
from app.practice.service import check_answer
from app.visualization.registry import validate_visualization
ROOT=Path(__file__).resolve().parents[2]
def test_eight_distinct_data_lessons_with_answered_banks():
    topic=GRADE_9.topics[11]
    assert topic.id=='data-handling' and topic.product_order==12
    assert [l.id for l in topic.subtopics[0].lessons]==[f'g9-data-{n:02}' for n in range(1,9)]
    assert not [e for e in validate_curriculum([GRADE_9]) if e.grade_id=='grade-9']
    manifest=json.loads((ROOT/'docs/curriculum/grade9/data-handling/topic12-acceptance-manifest.json').read_text())
    assert len(manifest)==8
    for n,(lesson,data) in DATA_LESSONS.items():
        practice,mastery,reassess,repairs,rules=DATA_BANKS[n]
        assert (len(data['worked']),len(practice),len(mastery),len(reassess))==(15,15,5,3)
        assert repairs and rules and not lesson.release_approved
        assert len({x['problem'] for x in data['worked']})==15
        assert len({x['prompt'] for key in ('practice','mastery','reassessment') for x in data[key]})==23
        source=(ROOT/'docs/curriculum/grade9/data-handling'/data['source']).read_bytes()
        assert manifest[n-1]['source_sha256']==hashlib.sha256(source).hexdigest()
        models=set()
        for scene,q in zip(data['worked'],lesson.whiteboard_questions):
            models.add(scene['visual']['values']['model'])
            assert len(q.whiteboard.steps)==5 and scene['actions'][-1]==scene['check']
            assert q.whiteboard.visualization.type=='statistics'
            assert validate_visualization(q.whiteboard) is None
        assert models==({'pie','scatter'} if n==7 else {['survey','stratified','frequency','dotplot','double_bar','histogram',None,'misleading_bar'][n-1]})
        for question in practice:
            assert len(set(question.options))==4 and check_answer(question.id,question.accepted_answers[0])
            assert all(not check_answer(question.id,option) for option in question.options if option!=question.accepted_answers[0])
def test_tampered_chart_calculation_is_rejected():
    board=deepcopy(DATA_LESSONS[4][0].whiteboard_questions[0].whiteboard)
    scene=json.loads(board.visualization.parameters['scene_json']);scene['visual']['values']['median']+=1
    board.visualization.parameters['scene_json']=json.dumps(scene)
    with pytest.raises(ValueError,match='Data calculation'):validate_visualization(board)
def test_data_lessons_open_without_answers_and_reveal_full_work():
    with TestClient(app) as client:
        topic=client.get('/api/v1/curriculum/grades/grade-9/topics/data-handling')
        assert topic.status_code==200 and len(topic.json()['subtopics'][0]['lessons'])==8
        for n in range(1,9):
            lid=f'g9-data-{n:02}';resp=client.get(f'/api/v1/lessons/{lid}')
            assert resp.status_code==200
            for q in resp.json()['whiteboard_questions']:
                assert q['solution_gated'] and len(q['whiteboard']['steps'])==1
                assert 'answer' not in q and 'full_memo' not in q
                scene=json.loads(q['whiteboard']['visualization']['parameters']['scene_json'])
                assert scene['visual']['family']=='data' and scene['visual']['values']['lesson']==n
                assert not {'answer','actions','check'}&scene.keys()
                assert not {'total','median','mean_rounded','prediction','gain_a','percent','walk_angle_num'}&scene['visual']['values'].keys()
                reveal=client.post(f'/api/v1/lessons/{lid}/questions/{q["id"]}/reveal')
                assert reveal.status_code==200 and len(reveal.json()['whiteboard']['steps'])==q['total_step_count']
            practice=client.get(f'/api/v1/practice/{lid}');mastery=client.get(f'/api/v1/practice/{lid}/mastery')
            assert practice.status_code==mastery.status_code==200
            assert len(practice.json()['questions'])==15 and len(mastery.json()['questions'])==5
            assert all('accepted_answers' not in item for item in practice.json()['questions'])
