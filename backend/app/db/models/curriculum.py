"""
db/models/curriculum.py — the source-controlled curriculum tables.

Responsibilities when implemented:
  - Models for the hierarchy in the brief (section 3):
    Grade -> Term -> Topic -> Subtopic -> Lesson -> Concept ->
    WorkedExample -> Practice -> Mastery
  - Each Lesson row stores: title, summary, explainer text, an
    `animation_spec` JSON column shaped exactly like the objects
    in frontend/js/data/curriculum-data.js (template + steps), and
    a `free` boolean for the paywall rule (first 1–2 lessons per
    topic are free)
  - Each Topic stores caps_ref / ieb_relevance / difficulty /
    prerequisites, per the CAPS+IEB architecture in brief section 5

This is THE file that retires curriculum-data.js. When it's built,
CurriculumAPI in that frontend file should be swapped for real
fetch() calls to api/v1/curriculum.py, and the JSON shape returned
by the API should match the JS objects it's replacing so the page
controllers (grade.js, topic.js, lesson.js) don't need rewrites.

# TODO (Phase 1–2): Grade, Term, Topic, Lesson SQLAlchemy models,
# with a `animation_spec = Column(JSON)` on Lesson.
"""
