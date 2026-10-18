class SelfGuidedPractice {
  constructor(mount, lessonId, { lessonCount = null } = {}) {
    Object.assign(this, { mount, lessonId, lessonCount, bank: null, sessionId: null, index: 0 });
    this.states = {}; this.answers = {}; this.solutionCache = {}; this.pendingHint = false;
  }
  async request(path, options = {}) {
    const token = typeof AthenaState !== "undefined" ? AthenaState.accessToken() : null;
    const response = await fetch(path, { ...options, headers: { "Content-Type": "application/json", ...(token ? { Authorization: `Bearer ${token}` } : {}) } });
    if (!response.ok) throw new Error((await response.json().catch(() => ({}))).detail || "Practice request failed.");
    return response.json();
  }
  async mountPractice() {
    this.index = 0; this.states = {}; this.answers = {}; this.solutionCache = {}; this.pendingHint = false;
    this.mount.innerHTML = '<section class="card practice-loading" aria-live="polite">Loading self-guided practice…</section>';
    try {
      this.bank = await this.request(`/api/v1/practice/${encodeURIComponent(this.lessonId)}`);
      const started = await this.request(`/api/v1/practice/${encodeURIComponent(this.lessonId)}/sessions`, { method: "POST" });
      this.sessionId = started.session_id; this.render();
    } catch (error) { this.mount.innerHTML = `<section class="card practice-error" role="alert"><h3>Self-guided practice</h3><p>${escapeWhiteboardHtml(error.message)}</p></section>`; }
    return this;
  }
  question() { return this.bank.questions[this.index]; }
  state() { return this.states[this.question().id] || { state: "unanswered", answer: "", attempts: 0, hints_used: 0, correct: false, solution_available: false, solution_viewed: false, next_enabled: false, hint_index: 0, hint_history: [], hint_complete: false }; }
  resetHints(questionId) { const previous = this.states[questionId] || {}; this.states[questionId] = { ...previous, hint_index: 0, hint_history: [], hint_complete: false }; this.pendingHint = false; }
  renderControl(question, state) {
    const value = this.answers[question.id] ?? state.answer ?? "";
    if (["classification", "multiple_choice", "error_analysis"].includes(question.type)) return `<fieldset class="practice-select"><legend>Choose your answer</legend>${question.options.map(option => `<label class="practice-choice"><input type="radio" name="practice-answer" value="${escapeWhiteboardHtml(option)}" ${value === option ? "checked" : ""}><span>${escapeWhiteboardHtml(option)}</span></label>`).join("")}</fieldset>`;
    const numeric = ["numeric", "missing_term"].includes(question.type);
    return `<label class="practice-answer-label" for="practice-answer">Your answer</label><input id="practice-answer" class="practice-answer-input" ${numeric ? 'inputmode="decimal"' : ""} autocomplete="off" value="${escapeWhiteboardHtml(value)}">`;
  }
  render() {
    const question = this.question(), state = this.state(), answered = state.attempts > 0;
    const progress = Math.round(Object.values(this.states).filter(item => item.next_enabled).length / this.bank.questions.length * 100);
    const hintButton = answered && !state.correct ? `<button type="button" class="btn btn-ghost" data-action="hint" ${state.hint_complete ? "disabled" : ""}>${state.hint_complete ? "No more hints" : "Give Me a Hint"}</button>` : "";
    this.mount.innerHTML = `<section class="card self-guided-practice" aria-labelledby="practice-title"><header><div><h3 id="practice-title">${escapeWhiteboardHtml(this.bank.title)}</h3><p>${escapeWhiteboardHtml(this.bank.supporting_text)}</p></div><span class="badge">${escapeWhiteboardHtml(question.difficulty)}</span></header><div class="practice-progress"><div class="progress-label"><span>Question ${question.question_number} of ${this.bank.questions.length}</span><span>${progress}% complete</span></div><div class="progress-track" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${progress}"><div class="progress-fill" style="width:${progress}%"></div></div></div><article class="practice-focus"><p class="practice-meta">${escapeWhiteboardHtml(question.cognitive_level)} · ${question.marks} marks</p><h4 tabindex="-1">${escapeWhiteboardHtml(question.prompt)}</h4><form data-role="answer-form">${this.renderControl(question, state)}<button class="btn btn-primary" data-action="submit" type="submit" disabled>Submit answer</button></form><div class="practice-feedback ${state.correct ? "is-correct" : answered ? "is-support" : ""}" data-role="feedback" aria-live="polite">${state.feedback ? escapeWhiteboardHtml(state.feedback) : ""}</div><div class="practice-support">${answered && !state.correct ? '<button type="button" class="btn btn-secondary" data-action="retry">Try Again</button>' : ""}${hintButton}${state.solution_available && !this.solutionCache[question.id] ? '<button type="button" class="btn btn-ghost" data-action="solution">Show Worked Solution</button>' : ""}</div><div class="practice-hints" data-role="hints" aria-live="polite">${(state.hint_history || []).map((hint, i) => `<p><strong>Hint ${i + 1}:</strong> ${escapeWhiteboardHtml(hint)}</p>`).join("")}</div><div data-role="solution"></div></article><nav class="practice-navigation" aria-label="Practice questions"><button type="button" class="btn btn-ghost" data-action="previous" ${this.index === 0 ? "disabled" : ""}>← Previous Question</button><span>Question ${question.question_number} of ${this.bank.questions.length}</span><button type="button" class="btn btn-primary" data-action="next" ${state.next_enabled ? "" : "disabled"}>${this.index === this.bank.questions.length - 1 ? "Practice Summary" : "Next Question →"}</button></nav></section>`;
    this.wire(); if (this.solutionCache[question.id]) this.renderSolution(this.solutionCache[question.id]);
  }
  wire() {
    const question = this.question(), form = this.mount.querySelector('[data-role="answer-form"]'), submit = form.querySelector('[data-action="submit"]');
    const update = () => { const checked = form.querySelector('input[name="practice-answer"]:checked'), input = form.querySelector(".practice-answer-input"), answer = checked?.value ?? input?.value ?? ""; this.answers[question.id] = answer; submit.disabled = !answer.trim(); };
    form.addEventListener("input", update); form.addEventListener("change", update); update();
    form.onsubmit = async event => { event.preventDefault(); if (submit.disabled) return; submit.disabled = true; const result = await this.request(`/api/v1/practice/${this.lessonId}/sessions/${this.sessionId}/questions/${question.id}/submit`, { method: "POST", body: JSON.stringify({ answer: this.answers[question.id] }) }); this.states[question.id] = { ...this.state(), ...result }; this.render(); };
    this.mount.querySelector('[data-action="retry"]')?.addEventListener("click", () => { this.resetHints(question.id); this.states[question.id].feedback = "Try the question again using your previous response as evidence."; this.render(); this.mount.querySelector("input")?.focus(); });
    this.mount.querySelector('[data-action="hint"]')?.addEventListener("click", async event => {
      if (this.pendingHint || this.state().hint_complete) return;
      this.pendingHint = true; event.currentTarget.disabled = true;
      const previous = this.state(), requested = Number(previous.hint_index || 0);
      try {
        const result = await this.request(`/api/v1/practice/${this.lessonId}/sessions/${this.sessionId}/questions/${question.id}/hint?hint_index=${requested}`, { method: "POST" });
        const history = [...(previous.hint_history || [])];
        if (result.hint_index === requested && !history.includes(result.hint)) history.push(result.hint);
        this.states[question.id] = { ...previous, ...result, hint_index: requested + 1, hint_history: history };
      } finally { this.pendingHint = false; }
      this.render();
    });
    this.mount.querySelector('[data-action="solution"]')?.addEventListener("click", async () => { const result = await this.request(`/api/v1/practice/${this.lessonId}/sessions/${this.sessionId}/questions/${question.id}/solution`); this.states[question.id] = { ...this.state(), ...result }; this.solutionCache[question.id] = result; this.render(); });
    this.mount.querySelector('[data-action="previous"]').onclick = () => { this.resetHints(question.id); this.index -= 1; this.resetHints(this.question().id); this.render(); this.mount.querySelector("h4")?.focus(); };
    this.mount.querySelector('[data-action="next"]').onclick = () => { if (this.index === this.bank.questions.length - 1) this.renderSummary(); else { this.resetHints(question.id); this.index += 1; this.resetHints(this.question().id); this.render(); this.mount.querySelector("h4")?.focus(); } };
  }
  renderSolution(data) { const host = this.mount.querySelector('[data-role="solution"]'); if (host) { new WorkedSolution(host, { steps: data.worked_solution }).mountSolution(); host.querySelector(".worked-solution__toggle")?.click(); } }
  async renderSummary() {
    const summary = await this.request(`/api/v1/practice/${this.lessonId}/sessions/${this.sessionId}/summary`), number = Number(this.lessonId.slice(-2)), nextLesson = this.lessonCount && number < this.lessonCount ? this.lessonId.replace(/\d{2}$/, String(number + 1).padStart(2, "0")) : null, isGrade8 = this.lessonId === "g8-algebraic-equations-01";
    this.mount.innerHTML = `<section class="card practice-summary"><h3>Practice summary</h3><p class="practice-score">${summary.score}%</p><dl><div><dt>Questions correct</dt><dd>${summary.questions_correct} of ${summary.total_questions}</dd></div><div><dt>First-attempt accuracy</dt><dd>${summary.first_attempt_accuracy}%</dd></div><div><dt>Hints used</dt><dd>${summary.hints_used}</dd></div><div><dt>Mastery target</dt><dd>${summary.mastery_threshold}%</dd></div></dl><h4>${summary.mastered ? "Independent practice complete" : "Keep building confidence"}</h4><p>${escapeWhiteboardHtml(summary.recommended_review)}</p>${summary.misconception_areas.length ? `<p><strong>Review:</strong> ${summary.misconception_areas.map(escapeWhiteboardHtml).join(", ")}</p>` : ""}<div class="practice-summary-actions"><button class="btn btn-secondary" data-action="retry-practice">Retry Practice</button>${isGrade8 ? '<button class="btn btn-primary" data-action="start-mastery">Start five-question mastery</button>' : ""}<a class="btn btn-ghost" href="lesson.html?lesson=${this.lessonId}">Return to Lesson</a>${summary.mastered && nextLesson ? `<a class="btn btn-primary" href="lesson.html?lesson=${nextLesson}">Continue to Next Lesson</a>` : ""}</div></section>`;
    this.mount.querySelector('[data-action="retry-practice"]').onclick = () => this.mountPractice(); this.mount.querySelector('[data-action="start-mastery"]')?.addEventListener("click", () => this.renderMastery());
  }
  async renderMastery() { const bank = await this.request(`/api/v1/practice/${this.lessonId}/mastery`); this.renderAssessment("Mastery assessment", bank.questions, async answers => { const result = await this.request(`/api/v1/practice/${this.lessonId}/sessions/${this.sessionId}/mastery`, { method: "POST", body: JSON.stringify({ answers }) }); this.renderMasteryResult(result); }); }
  renderAssessment(title, questions, onSubmit) { this.mount.innerHTML = `<section class="card mastery-assessment"><h3>${escapeWhiteboardHtml(title)}</h3><p>Work independently. Answers and memos remain on the server until submission.</p><form data-role="assessment-form">${questions.map(item => `<label class="practice-answer-label" for="assessment-${item.id}">${item.number}. ${escapeWhiteboardHtml(item.prompt)}</label><input required id="assessment-${item.id}" class="practice-answer-input" data-question-id="${item.id}" autocomplete="off">`).join("")}<button class="btn btn-primary" type="submit">Submit assessment</button></form></section>`; this.mount.querySelector('[data-role="assessment-form"]').onsubmit = async event => { event.preventDefault(); const answers = Object.fromEntries([...event.currentTarget.querySelectorAll('[data-question-id]')].map(input => [input.dataset.questionId, input.value])); await onSubmit(answers); }; }
  renderMasteryResult(result) {
    this.mount.innerHTML = `<section class="card mastery-result"><h3>${result.mastered ? "Mastery achieved" : "Targeted repair required"}</h3><p class="practice-score">${result.score}%</p><p>${result.questions_correct} of ${result.total_questions} correct. Backend decision: ${escapeWhiteboardHtml(result.readiness_decision)}.</p>${result.repair_routes.length ? `<div>${result.repair_routes.map(route => `<article><strong>${escapeWhiteboardHtml(route.tag)}</strong><p>${escapeWhiteboardHtml(route.diagnosis)}</p><p>${escapeWhiteboardHtml(route.repair)}</p></article>`).join("")}</div><button class="btn btn-primary" data-action="complete-repair">I completed the targeted repair</button>` : "<p>You met the authoritative 80% rule.</p>"}</section>`;
    this.mount.querySelector('[data-action="complete-repair"]')?.addEventListener("click", async () => { await this.request(`/api/v1/practice/${this.lessonId}/sessions/${this.sessionId}/repair/complete`, { method: "POST" }); const bank = await this.request(`/api/v1/practice/${this.lessonId}/sessions/${this.sessionId}/reassessment`); this.renderAssessment("Parallel reassessment", bank.questions, async answers => { const result = await this.request(`/api/v1/practice/${this.lessonId}/sessions/${this.sessionId}/reassessment`, { method: "POST", body: JSON.stringify({ answers }) }); this.mount.innerHTML = `<section class="card"><h3>${result.ready ? "Ready to progress" : "More repair required"}</h3><p>${result.questions_correct} of 3 correct. Backend decision: ${escapeWhiteboardHtml(result.readiness_decision)}.</p></section>`; }); });
  }
}
