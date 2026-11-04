"""Grade 9 Topic 1 batch contract: static banks, gating and registered visuals."""
import json
import hashlib
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app
from app.curriculum.grade9.whole_numbers_runtime import GRADE_9, EXTENDED, EXTENDED_TEMPLATES
from app.curriculum.grade9.assessment_whole_numbers import EXTENDED_BANKS
from app.curriculum.validation import validate_curriculum
from app.practice.service import check_answer


def test_six_authored_lessons_and_private_four_option_banks():
    assert [item.id for item in GRADE_9.topics[0].subtopics[0].lessons]==[f'g9-whole-numbers-{n:02}' for n in range(1,9)]
    assert not [e for e in validate_curriculum([GRADE_9]) if e.grade_id=='grade-9']
    for n,(lesson,data) in EXTENDED.items():
        practice,mastery,reassess,repairs,rules=EXTENDED_BANKS[n]
        assert (len(lesson.whiteboard_questions),len(practice),len(mastery),len(reassess))==(15,15,5,3)
        assert len({q.prompt for q in practice+mastery+reassess})==23
        assert len({q.whiteboard.problem for q in lesson.whiteboard_questions})==15
        assert not {q.whiteboard.problem for q in lesson.whiteboard_questions}&{q.prompt for q in practice+mastery+reassess}
        assert repairs and rules and lesson.release_approved is False
        for q,source in zip(lesson.whiteboard_questions,data['worked']):
            board=q.whiteboard
            assert board.visualization.template==EXTENDED_TEMPLATES[n]
            scene=json.loads(board.visualization.parameters['scene_json'])
            assert scene['problem']==source['problem'] and scene['visual']==source['visual']
            assert len(board.steps)==len(source['actions'])>=4
            assert board.steps[-1].after_expression.endswith(source['check'])
        for q in practice:
            assert len(set(q.options))==4 and check_answer(q.id,q.accepted_answers[0])
            assert all(not check_answer(q.id,option) for option in q.options if option!=q.accepted_answers[0])
        for q in mastery+reassess:
            assert len(set(q.options))==4 and q.answer in q.options
            assert 'answer' not in q.public()


def test_topic_manifest_matches_source_hashes_and_all_eight_runtime_ids():
    source=Path(__file__).resolve().parents[2]/'docs/curriculum/grade9/whole-numbers'
    manifest=json.loads((source/'topic1-acceptance-manifest.json').read_text(encoding='utf-8'))
    assert len(manifest)==8
    for number,entry in enumerate(manifest,1):
        assert entry['lesson_id']==f'g9-whole-numbers-{number:02}'
        assert entry['source_sha256']==hashlib.sha256((source/entry['source']).read_bytes()).hexdigest()
        for key,count in [('worked',15),('practice',15),('mastery',5),('reassessment',3)]:
            assert entry[f'{key}_count']==len(set(entry[f'{key}_ids']))==count
        assert entry['status']=='teacher_review_required' and not entry['teacher_approved']


def test_six_lesson_apis_gate_results_until_reveal():
    with TestClient(app) as client:
        for n in range(3,9):
            lesson_id=f'g9-whole-numbers-{n:02}'
            preview=client.get(f'/api/v1/lessons/{lesson_id}')
            bank=client.get(f'/api/v1/practice/{lesson_id}')
            mastery=client.get(f'/api/v1/practice/{lesson_id}/mastery')
            assert preview.status_code==bank.status_code==mastery.status_code==200,(n,preview.text[:200])
            questions=preview.json()['whiteboard_questions']
            assert len(questions)==15 and len(bank.json()['questions'])==15 and len(mastery.json()['questions'])==5
            assert all(len(q['options'])==4 and 'answer' not in q for q in bank.json()['questions'])
            for q in questions:
                scene=json.loads(q['whiteboard']['visualization']['parameters']['scene_json'])
                assert not {'answer','actions','wrongs','wrong_methods','check','option_rationales','misconception'}&set(scene)
                assert scene['visual']=={'family':'givens'}
                assert q['solution_gated'] and len(q['whiteboard']['steps'])==1
                assert 'answer' not in q and 'full_memo' not in q
                revealed=client.post(f'/api/v1/lessons/{lesson_id}/questions/{q["id"]}/reveal')
                assert revealed.status_code==200,(q['id'],revealed.text[:200])
                assert len(revealed.json()['whiteboard']['steps'])==q['total_step_count']
