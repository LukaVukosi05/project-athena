"""
db/models/progress.py — per-learner progress & quiz attempts.

Responsibilities when implemented:
  - `LessonCompletion` model: user_id, lesson_id, completed_at
  - `QuizAttempt` model: user_id, lesson_id, score, passed, answers
    (JSON), attempted_at
  - A `topic_progress(user_id, topic_id)` query helper mirroring
    AthenaState.topicProgress() in frontend/js/engine/state.js

This is the server-side counterpart to AthenaState's localStorage
`completedLessons` / `quizAttempts`. Once this exists, the lesson
gating rule (AthenaState.isLessonUnlocked) should be re-checked
server-side too, in api/v1/quizzes.py — a locked lesson must not
be unlockable by editing the frontend's local state.

# TODO (Phase 2, alongside api/v1/quizzes.py)
"""
