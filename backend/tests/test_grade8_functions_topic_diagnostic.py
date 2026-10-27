from fastapi.testclient import TestClient
from app.main import app
from app.curriculum.grade8.functions_topic_diagnostic import ITEMS, score

URL = '/api/v1/practice/topics/grade-8/functions-relationships/diagnostic'


def test_topic_check_covers_each_lesson_and_has_no_public_answers():
    with TestClient(app) as client:
        response = client.get(URL)
    assert response.status_code == 200
    assert len(response.json()['questions']) == 12
    assert {item.lesson_id for item in ITEMS} == {
        'g8-functions-relationships-01', 'g8-functions-relationships-02', 'g8-functions-relationships-03', 'g8-functions-relationships-04'}
    assert all(set(question) == {'id', 'prompt'} for question in response.json()['questions'])


def test_topic_check_scores_exactly_twelve_and_routes_weak_areas():
    answers = {item.id: item.answers[0] for item in ITEMS}
    with TestClient(app) as client:
        full = client.post(URL, json={'answers': answers})
        partial = client.post(URL, json={'answers': {**answers, 'fr-t04': 'wrong', 'fr-t05': 'wrong'}})
        missing = client.post(URL, json={'answers': {'fr-t01': '11'}})
    assert full.status_code == 200 and full.json()['score'] == 12
    assert full.json()['recommended_lesson_id'] is None
    assert partial.json()['score'] == 10
    assert partial.json()['recommended_lesson_id'] == 'g8-functions-relationships-02'
    assert missing.status_code == 422
    assert score(answers)['areas'][0]['correct'] == 3
