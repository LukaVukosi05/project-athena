/* ============================================================
   QUIZ ENGINE
   ------------------------------------------------------------
   Renders a lesson's quiz and enforces the product rule: a
   learner must pass the quiz (score >= passMark) before the
   next lesson unlocks (see AthenaState.isLessonUnlocked).
   Phase 1 grades client-side from curriculum-data.js answers;
   once the backend exists, grading moves server-side (see
   backend/app/api/v1/quizzes.py) so answers are never shipped
   to the browser — this file's render/onComplete contract
   should not need to change when that happens.
   ============================================================ */
class QuizEngine {
  constructor(mountEl, quizSpec, { onComplete } = {}) {
    this.mountEl = mountEl;
    this.spec = quizSpec;
    this.onComplete = onComplete || function () {};
    this.answers = new Array(quizSpec.questions.length).fill(null);
    this.qIndex = 0;
  }

  mount() { this.renderQuestion(); return this; }

  renderQuestion() {
    const q = this.spec.questions[this.qIndex];
    const chosen = this.answers[this.qIndex];
    const answered = chosen !== null;

    this.mountEl.innerHTML = `
      <div class="quiz-panel">
        <div class="progress-label"><span>Question ${this.qIndex + 1} of ${this.spec.questions.length}</span></div>
        <h4>${escapeHtml(q.q)}</h4>
        <div data-role="options"></div>
        <div data-role="feedback"></div>
        <div style="display:flex;justify-content:flex-end;gap:12px;margin-top:8px;">
          <button class="btn btn-primary" data-action="continue" ${answered ? "" : "disabled"}>
            ${this.qIndex === this.spec.questions.length - 1 ? "See results" : "Continue"}
          </button>
        </div>
      </div>`;

    const optWrap = this.mountEl.querySelector('[data-role="options"]');
    q.options.forEach((opt, i) => {
      const btn = document.createElement("button");
      btn.className = "quiz-option";
      btn.type = "button";
      btn.textContent = opt;
      if (chosen !== null) {
        btn.disabled = true;
        if (i === q.correctIndex) btn.classList.add("correct");
        else if (i === chosen) btn.classList.add("incorrect");
      }
      btn.onclick = () => this.selectAnswer(i);
      optWrap.appendChild(btn);
    });

    if (answered) {
      const correct = chosen === q.correctIndex;
      this.mountEl.querySelector('[data-role="feedback"]').innerHTML =
        `<p class="quiz-feedback ${correct ? "correct" : "incorrect"}">${correct ? "Correct." : "Not quite."} ${escapeHtml(q.explanation)}</p>`;
    }

    this.mountEl.querySelector('[data-action="continue"]').onclick = () => {
      if (this.qIndex < this.spec.questions.length - 1) { this.qIndex++; this.renderQuestion(); }
      else this.finish();
    };
  }

  selectAnswer(i) {
    if (this.answers[this.qIndex] !== null) return;
    this.answers[this.qIndex] = i;
    this.renderQuestion();
  }

  finish() {
    const total = this.spec.questions.length;
    const correct = this.answers.filter((a, i) => a === this.spec.questions[i].correctIndex).length;
    const score = correct / total;
    const passed = score >= (this.spec.passMark || 0.7);

    this.mountEl.innerHTML = `
      <div class="quiz-panel" style="text-align:center;">
        <h3>${passed ? "Lesson passed" : "Not quite there yet"}</h3>
        <p>You got ${correct} of ${total} correct (${Math.round(score * 100)}%). ${passed ? "The next lesson is now unlocked." : `You need ${Math.round((this.spec.passMark || 0.7) * 100)}% to unlock the next lesson.`}</p>
        <div style="display:flex;gap:12px;justify-content:center;">
          ${passed ? "" : `<button class="btn btn-secondary" data-action="retry">Try again</button>`}
          <button class="btn btn-primary" data-action="ok">${passed ? "Continue" : "Review lesson"}</button>
        </div>
      </div>`;

    const retry = this.mountEl.querySelector('[data-action="retry"]');
    if (retry) retry.onclick = () => { this.answers = new Array(total).fill(null); this.qIndex = 0; this.renderQuestion(); };

    // Record the attempt immediately (independent of whether the learner clicks a button)
    this.onComplete({ score, passed, correct, total, silent: true });
    this.mountEl.querySelector('[data-action="ok"]').onclick = () => this.onComplete({ score, passed, correct, total });
  }
}

function escapeHtml(str) {
  return String(str).replace(/[&<>"']/g, s => ({ "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;" }[s]));
}
