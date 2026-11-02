import hashlib
import json
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app
from app.curriculum.grade8.structure import GRADE_8
from app.curriculum.grade8.functions_relationships_lesson5 import DATA as DATA5,LESSON as LESSON5,QUESTIONS as QUESTIONS5
from app.curriculum.grade8.functions_relationships_lesson6 import DATA as DATA6,LESSON as LESSON6,QUESTIONS as QUESTIONS6
from app.curriculum.grade8 import assessment_functions_lesson5 as BANK5,assessment_functions_lesson6 as BANK6
from app.curriculum.validation import validate_curriculum
from app.visualization.registry import validate_visualization


def test_two_original_source_packs_and_question_specific_math():
    for number,data,lesson,questions,bank in ((5,DATA5,LESSON5,QUESTIONS5,BANK5),(6,DATA6,LESSON6,QUESTIONS6,BANK6)):
        source=Path(__file__).resolve().parents[2]/'docs/curriculum/grade8/functions-relationships'/data['source_document']
        assert hashlib.sha256(source.read_bytes().replace(b'\r\n',b'\n')).hexdigest()==data['source_sha256']
        assert len(questions)==len(bank.PRACTICE_BANK)==15
        assert len(bank.MASTERY_BANK)==5 and len(bank.REASSESSMENT_BANK)==3
        assert not lesson.release_approved
        assert [q.id for q in questions]==[f'g8-fr-l{number:02}-w{i:02}' for i in range(1,16)]
        scenes=[json.loads(q.whiteboard.visualization.parameters['scene_json']) for q in questions]
        assert len({json.dumps(s,sort_keys=True) for s in scenes})==15
        assert all(len(q.whiteboard.steps)==4 for q in questions)
        for scene in scenes:
            x=scene['input']
            assert len(scene['candidates'])==2
            assert scene['candidates'][0]['value']!=scene['candidates'][1]['value']
            for candidate in scene['candidates']:
                assert abs(candidate['a']*x*x+candidate['b']*x+candidate['c']-candidate['value'])<1e-7
        assert all(q.whiteboard.steps[-1].state_after['verification_complete'] for q in questions)
    assert not [f for f in validate_curriculum([GRADE_8]) if f.lesson_id in {LESSON5.id,LESSON6.id}]


def test_both_new_lessons_resolve_without_displacing_graphs_and_gate_answers():
    with TestClient(app) as client:
        grade=client.get('/api/v1/curriculum/grades/grade-8').json()
        topic=client.get('/api/v1/curriculum/grades/grade-8/topics/functions-relationships').json()
        assert client.get('/api/v1/curriculum/grades/grade-8/topics/graphs').status_code==200
        assert [row['id'] for row in grade['topics']][2:4]==['functions-relationships','graphs']
        assert [row['id'] for sub in topic['subtopics'] for row in sub['lessons']]==[f'g8-functions-relationships-{n:02}' for n in range(1,7)]
        for n in (5,6):
            lesson_id=f'g8-functions-relationships-{n:02}'
            response=client.get(f'/api/v1/lessons/{lesson_id}')
            practice=client.get(f'/api/v1/practice/{lesson_id}')
            mastery=client.get(f'/api/v1/practice/{lesson_id}/mastery')
            assert response.status_code==practice.status_code==mastery.status_code==200
            payload=response.json()
            assert len(payload['whiteboard_questions'])==len(practice.json()['questions'])==15
            assert len(mastery.json()['questions'])==5
            for preview in payload['whiteboard_questions']:
                assert 'answer' not in preview and 'full_memo' not in preview
                assert len(preview['whiteboard']['steps'])==1
                scene=json.loads(preview['whiteboard']['visualization']['parameters']['scene_json'])
                assert 'chosen' not in scene and all('value' not in path for path in scene['candidates'])
            reveal=client.post(f'/api/v1/lessons/{lesson_id}/questions/g8-fr-l{n:02}-w01/reveal')
            assert reveal.status_code==200 and len(reveal.json()['whiteboard']['steps'])==4
