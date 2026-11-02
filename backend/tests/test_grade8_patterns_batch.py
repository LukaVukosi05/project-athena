"""Question-specific authored pattern batch and public answer gate."""
import json
from fastapi.testclient import TestClient
from app.main import app
from app.curriculum.grade8.patterns_runtime import LESSON_1, LESSON_2, SCENES_1, SCENES_2
from app.curriculum.grade8.assessment_patterns import banks
from app.curriculum.validation import validate_curriculum
from app.curriculum.grade8.structure import GRADE_8


def test_two_lessons_have_full_distinct_staged_models():
    for number, (lesson,scenes) in enumerate(zip((LESSON_1, LESSON_2),(SCENES_1,SCENES_2)),1):
        assert len(lesson.whiteboard_questions)==15
        assert [q.id for q in lesson.whiteboard_questions]==[f'g8-patterns-l{number:02}-w{n:02}' for n in range(1,16)]
        assert len({q.whiteboard.visualization.parameters['scene_json'] for q in lesson.whiteboard_questions})==15
        for q in lesson.whiteboard_questions:
            scene=json.loads(q.whiteboard.visualization.parameters['scene_json'])
            assert len(q.whiteboard.steps)==4 and scene['id']==q.id
            assert q.whiteboard.steps[-1].after_expression.startswith(f'Verified: {scene["answer"]}')
            assert all(step.narration==next(event.text for event in step.events if event.type=='caption') for step in q.whiteboard.steps)
        practice,mastery,parallel,repairs=banks(number)
        assert (len(practice),len(mastery),len(parallel))==(15,5,3)
        assert repairs
        if number==2:
            assert all(q.accepted_answers[0]!=str(scene["answer"]) for q,scene in zip(practice,scenes))
    assert not [f for f in validate_curriculum([GRADE_8]) if f.topic_id=='numeric-geometric-patterns']


def test_public_payload_and_reveal_gate_pattern_answers():
    with TestClient(app) as client:
        for n in (1,2):
            lid=f'g8-patterns-{n:02}'
            preview=client.get(f'/api/v1/lessons/{lid}')
            assert preview.status_code==200
            q=preview.json()['whiteboard_questions'][0]
            assert 'answer' not in q and len(q['whiteboard']['steps'])==1
            scene=json.loads(q['whiteboard']['visualization']['parameters']['scene_json'])
            assert not {'answer','memo','actions'} & scene.keys()
            reveal=client.post(f'/api/v1/lessons/{lid}/questions/g8-patterns-l{n:02}-w01/reveal')
            assert reveal.status_code==200 and len(reveal.json()['whiteboard']['steps'])==4
            assert client.get(f'/api/v1/practice/{lid}').status_code==200
            assert client.get(f'/api/v1/practice/{lid}/mastery').status_code==200
