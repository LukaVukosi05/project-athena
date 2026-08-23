/* ============================================================
   PAGE CONTROLLER — Lesson page (brief sections 16–18)
   URL contract: lesson.html?grade=<gradeId>&topic=<topicId>&lesson=<lessonId>
   Wires together: AnimationEngine (whiteboard), the explainer
   text, and QuizEngine (must be passed before the NEXT lesson
   unlocks — see AthenaState.isLessonUnlocked).
   ============================================================ */
document.addEventListener("DOMContentLoaded", async () => {
  renderNav("Learn");
  const params = new URLSearchParams(location.search);
  const gradeId = params.get("grade");
  const topicId = params.get("topic");
  const lessonId = params.get("lesson");
  if (lessonId?.startsWith("g12-")) {
    await renderStructuredLesson(lessonId);
    return;
  }

  const topic = CurriculumAPI.getTopic(gradeId, topicId);
  const lesson = CurriculumAPI.getLesson(gradeId, topicId, lessonId);
  const root = document.getElementById("lesson-root");

  if (!topic || !lesson) {
    root.innerHTML = `<p>We couldn't find that lesson. <a href="dashboard.html">Back to dashboard</a></p>`;
    return;
  }

  if (!AthenaState.isLessonUnlocked(topic, lessonId)) {
    root.innerHTML = `
      <div class="card quiz-lock-notice">
        <strong>This lesson is locked.</strong> Pass the quiz for the previous lesson in
        "${escapeHtml(topic.title)}" to unlock it.
      </div>
      <p style="margin-top:16px;"><a href="topic.html?grade=${gradeId}&topic=${topicId}">← Back to ${escapeHtml(topic.title)}</a></p>`;
    return;
  }

  const state = AthenaState.get();
  const lessonIdx = topic.lessons.findIndex(l => l.id === lessonId);

  document.title = `${lesson.title} — Project Athena`;
  document.getElementById("crumb-topic").textContent = topic.title;
  document.getElementById("crumb-topic").href = `topic.html?grade=${gradeId}&topic=${topicId}`;
  document.getElementById("lesson-progress").textContent = `Lesson ${lessonIdx + 1} of ${topic.lessons.length}`;
  document.getElementById("lesson-title").textContent = lesson.title;

  if (!AthenaState.hasLessonAccess(lesson)) {
    renderPaywall(root, topic, lesson);
    return;
  }

  renderLessonContent(root, gradeId, topicId, topic, lesson, lessonIdx);
});

async function renderStructuredLesson(lessonId) {
  const root = document.getElementById("lesson-root");
  try {
    const token = AthenaState.accessToken();
    const response = await fetch(`/api/v1/lessons/${encodeURIComponent(lessonId)}`, {
      headers: token ? { Authorization: `Bearer ${token}` } : {}
    });
    if (!response.ok) throw new Error(response.status === 403 ? "An active subscription is required." : "Lesson could not be loaded.");
    const lesson = await response.json();
    document.title = `${lesson.title} — Project Athena`;
    document.getElementById("crumb-topic").textContent = "Algebra Foundations / Readiness";
    document.getElementById("crumb-topic").href = "grade.html?grade=grade-12";
    document.getElementById("lesson-progress").textContent = "Linear Equations";
    document.getElementById("lesson-title").textContent = lesson.title;
    new LessonBlockRenderer(root, lesson).render();
  } catch (error) {
    root.innerHTML = `<div class="card"><strong>We couldn't load this lesson.</strong><p>${escapeHtml(error.message)}</p></div>`;
  }
}

function renderLessonContent(root, gradeId, topicId, topic, lesson, lessonIdx) {
  root.innerHTML = `
    <div id="animation-mount"></div>
    <div class="card lesson-explainer">
      <h4>What is happening?</h4>
      <p>${escapeHtml(lesson.explainer)}</p>
    </div>
    <div id="quiz-gate" class="card" style="text-align:center;">
      <h4>Ready to check your understanding?</h4>
      <p>Pass this short quiz to unlock the next lesson.</p>
      <button class="btn btn-primary" id="start-quiz-btn">Take the quiz</button>
    </div>
    <div id="quiz-mount" style="display:none;" class="card"></div>
    <div class="lesson-nav">
      ${lessonIdx > 0
        ? `<a class="btn btn-ghost" href="lesson.html?grade=${gradeId}&topic=${topicId}&lesson=${topic.lessons[lessonIdx - 1].id}">← Previous</a>`
        : `<a class="btn btn-ghost" href="topic.html?grade=${gradeId}&topic=${topicId}">← Back to topic</a>`}
      <span></span>
    </div>`;

  new AnimationEngine(document.getElementById("animation-mount"), lesson.animation).mount();

  document.getElementById("start-quiz-btn").onclick = () => {
    document.getElementById("quiz-gate").style.display = "none";
    const quizMount = document.getElementById("quiz-mount");
    quizMount.style.display = "block";
    new QuizEngine(quizMount, lesson.quiz, {
      onComplete: (result) => {
        if (result.silent) {
          AthenaState.recordQuizAttempt(lesson.id, result.score, result.passed);
          return;
        }
        if (result.passed) {
          const next = topic.lessons[lessonIdx + 1];
          location.href = next
            ? `lesson.html?grade=${gradeId}&topic=${topicId}&lesson=${next.id}`
            : `topic.html?grade=${gradeId}&topic=${topicId}`;
        } else {
          quizMount.style.display = "none";
          document.getElementById("quiz-gate").style.display = "block";
        }
      }
    }).mount();
  };
}

function renderPaywall(root, topic, lesson) {
  root.innerHTML = `
    <div class="card paywall-card">
      <h3>Unlock "${escapeHtml(lesson.title)}"</h3>
      <p>The first two lessons of every topic are free. Go premium for full Grade 8–12 access.</p>
      <div class="price">R150<span style="font-size:var(--fs-sm);color:var(--color-text-secondary);">/month</span></div>
      <ul>
        <li>All Grade 8–12 lessons</li>
        <li>Animated explanations</li>
        <li>AI Tutor</li>
        <li>Unlimited practice</li>
        <li>Past-paper preparation</li>
        <li>Progress tracking</li>
      </ul>
      <button class="btn btn-primary" id="unlock-btn">Start Premium</button>
    </div>`;
  document.getElementById("unlock-btn").onclick = () => {
    // Phase 1 stub: flips a local flag only. Real checkout is Phase 5
    // (see backend/app/api/v1/payments.py and backend/app/services/payments.py).
    const s = AthenaState.get();
    s.isPremium = true;
    localStorage.setItem("athena_v1_state", JSON.stringify(s));
    location.reload();
  };
}

function escapeHtml(str) {
  return String(str).replace(/[&<>"']/g, s => ({ "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;" }[s]));
}
