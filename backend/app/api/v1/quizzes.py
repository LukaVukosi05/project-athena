"""
api/v1/quizzes.py — quiz fetch + grading endpoints.

Endpoints to implement:

  GET /api/v1/quizzes/{lesson_id}
    -> quiz questions WITHOUT correct_index or explanation —
       unlike frontend/js/data/curriculum-data.js (a Phase 1 mock
       that ships answers to the browser for convenience), the real
       API must never leak the answer key to the client.

  POST /api/v1/quizzes/{lesson_id}/submit
    body: { answers: [selected_index, ...] }
    -> grades server-side against the stored correct answers,
       writes a db/models/progress.py::QuizAttempt row, marks the
       lesson complete if score >= pass_mark, and returns
       { score, passed, per_question_feedback }

This endpoint is what frontend/js/engine/quiz-engine.js should call
instead of grading from the in-browser curriculum-data.js object.

# TODO (Phase 2, alongside db/models/progress.py)
"""
