from fastapi.testclient import TestClient
from app.main import app
from app.curriculum.repository import curriculum_repository
from app.practice.catalog import PRACTICE_BANKS


def test_catalogue_matches_authored_banks_for_every_grade_without_answers():
    seen = set()
    with TestClient(app) as client:
        for number in range(8, 13):
            grade_id = f'grade-{number}'
            response = client.get(f'/api/v1/practice/catalogue/grades/{grade_id}')
            assert response.status_code == 200
            payload = response.json()
            grade = curriculum_repository.get_grade(grade_id)
            assert [t['id'] for t in payload['topics']] == [t.id for t in grade.topics]
            for topic in payload['topics']:
                for lesson in topic['lessons']:
                    bank = PRACTICE_BANKS.get(lesson['id'], [])
                    assert lesson['question_count'] == len(bank)
                    assert lesson['choice_count'] == sum(bool(q.options) for q in bank)
                    if bank:
                        seen.add(lesson['id'])
            for private in ('accepted_answers', 'worked_solution', 'hints', 'correct_answer', 'prompt'):
                assert f'"{private}"' not in response.text
        assert seen == set(PRACTICE_BANKS)
        assert client.get('/api/v1/practice/catalogue/grades/grade-7').status_code == 404
