"""All existing Grade 8 lessons retain gated mastery and gain a topic revision check."""
from fastapi.testclient import TestClient

from app.main import app
from app.curriculum.grade8.structure import GRADE_8
from app.curriculum.grade8.coverage import ATP_URL, REMAINING_SCOPE, UNREGISTERED_TOPICS
from app.api.v1.practice import ASSESSMENT_BANKS


def test_coverage_plan_is_honest_and_all_existing_lessons_have_mastery():
    topics={topic.id:topic for topic in GRADE_8.topics}
    assert len(topics)==13
    assert len(UNREGISTERED_TOPICS)==5
    assert not set(UNREGISTERED_TOPICS)&topics.keys()
    assert set(REMAINING_SCOPE)=={'whole-numbers','geometry-of-straight-lines','geometry-of-2d-shapes'}
    assert ATP_URL.startswith('https://www.education.gov.za/')
    for topic in topics.values():
        for subtopic in topic.subtopics:
            for lesson in subtopic.lessons:
                assert len(lesson.whiteboard_questions)==15,lesson.id
                assert lesson.id in ASSESSMENT_BANKS,lesson.id
                mastery,reassessment,repairs,rules=ASSESSMENT_BANKS[lesson.id]
                assert len(mastery)==5 and len(reassessment)==3,lesson.id
                assert repairs and rules,lesson.id


def test_all_registered_topics_have_gated_revision_checks_and_lesson_routes():
    with TestClient(app) as client:
        for topic in GRADE_8.topics:
            url=f'/api/v1/practice/topics/grade-8/{topic.id}/diagnostic'
            public=client.get(url)
            assert public.status_code==200,(topic.id,public.text)
            questions=public.json()['questions']
            lessons=[lesson for subtopic in topic.subtopics for lesson in subtopic.lessons]
            assert len(questions)>=len(lessons),topic.id
            assert all('answer' not in item and 'solution' not in item for item in questions)
            assert client.post(url,json={'answers':{}}).status_code==422
            if topic.id=='functions-relationships':
                continue  # Its dedicated 18-item topic check has separate tests.
            answers={item.id:item.answer for lesson in lessons for item in ASSESSMENT_BANKS[lesson.id][0][:2]}
            result=client.post(url,json={'answers':answers})
            assert result.status_code==200,(topic.id,result.text)
            data=result.json()
            assert data['score']==data['total']==len(questions),topic.id
            assert [area['lesson_id'] for area in data['areas']]==[lesson.id for lesson in lessons]
            assert data['recommended_lesson_id'] is None
            assert client.post(url,json={'answers':{**answers,next(iter(answers)):'wrong'}}).json()['recommended_lesson_id']==lessons[0].id
        straight=client.get('/api/v1/curriculum/grades/grade-8/topics/geometry-of-straight-lines').json()
    assert len(straight['subtopics'][0]['lessons'])==2
    assert len(straight['remaining_scope'])==3


def test_unknown_topics_are_not_faked_as_checks():
    with TestClient(app) as client:
        assert client.get('/api/v1/practice/topics/grade-8/data-handling/diagnostic').status_code==404
