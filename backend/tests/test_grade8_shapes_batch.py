"""Five real shape lessons, private banks and question-specific visual contracts."""
import json
from math import acos, degrees, hypot
from fastapi.testclient import TestClient
from app.main import app
from app.curriculum.grade8.shapes_cases import LESSONS,variant,validate_all
from app.curriculum.grade8.shapes_runtime import LESSONS_RUNTIME
from app.curriculum.grade8.assessment_shapes import banks
from app.practice.service import check_answer
from app.visualization.registry import validate_visualization
from app.whiteboard.registry import registry


def _angle(points,index):
    p=points[index];a=points[index-1];b=points[(index+1)%len(points)]
    u=(a[0]-p[0],a[1]-p[1]);v=(b[0]-p[0],b[1]-p[1])
    return degrees(acos(max(-1,min(1,(u[0]*v[0]+u[1]*v[1])/(hypot(*u)*hypot(*v))))))


def test_drawn_angle_sizes_match_question_values():
    for case in LESSONS[5]:
        pts=case.scene['points']
        if case.scene['kind']=='sum':
            for i,known in enumerate(case.given):
                assert abs(_angle(pts,i)-known)<1e-6,(case.id,i)
            assert abs(_angle(pts,3)-int(case.answer.rstrip('°')))<1e-6
        else:
            assert abs(_angle(pts,0)-case.given[0])<1e-6
    for case in LESSONS[1]:
        points=case.scene['points']
        a=hypot(points[2][0]-points[1][0],points[2][1]-points[1][1])
        b=hypot(points[2][0]-points[0][0],points[2][1]-points[0][1])
        c=hypot(points[1][0]-points[0][0],points[1][1]-points[0][1])
        assert max(abs(a/c-case.given[0]/case.given[2]),abs(b/c-case.given[1]/case.given[2]))<1e-6


def test_all_five_shape_lessons_are_distinct_and_exact():
    assert validate_all()
    assert len({c.problem for cases in LESSONS.values() for c in cases})==75
    for n,cases in LESSONS.items():
        lesson=LESSONS_RUNTIME[n]
        assert len(lesson.whiteboard_questions)==15 and lesson.source_sha256
        assert lesson.release_approved is False
        practice,mastery,reassessment,repairs,rules=banks(n)
        assert (len(practice),len(mastery),len(reassessment))==(15,5,3)
        assert repairs and rules
        for case,q in zip(cases,lesson.whiteboard_questions):
            validate_visualization(q.whiteboard)
            registry.validate(q.whiteboard)
            assert case.answer==q.answer
            assert len(q.whiteboard.steps)==len(case.working)+1
            scene=json.loads(q.whiteboard.visualization.parameters['scene_json'])
            assert 'answer' not in scene and 'memo' not in scene
            assert q.whiteboard.steps[-1].state_after['verification_complete']
            assert variant(case,1).problem!=case.problem
        assert check_answer(practice[0].id,practice[0].accepted_answers[-1])


def test_public_api_has_five_lessons_and_hides_unrequested_solutions():
    with TestClient(app) as client:
        topic=client.get('/api/v1/curriculum/grades/grade-8/topics/geometry-of-2d-shapes')
        assert topic.status_code==200
        lessons=topic.json()['subtopics'][0]['lessons']
        assert [row['id'] for row in lessons]==[f'g8-shapes-{n:02}' for n in range(1,6)]
        for n in range(1,6):
            lid=f'g8-shapes-{n:02}'
            bank=client.get(f'/api/v1/practice/{lid}')
            assert bank.status_code==200 and len(bank.json()['questions'])==15
            lesson=client.get(f'/api/v1/lessons/{lid}')
            if lesson.status_code==200:
                questions=lesson.json()['whiteboard_questions']
                assert len(questions)==15
                assert all('answer' not in q and 'full_memo' not in q for q in questions)
                assert all(len(q['whiteboard']['steps'])==1 for q in questions)
