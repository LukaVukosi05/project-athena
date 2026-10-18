class WhiteboardQuestionSet {
  constructor(mount, questions, { onPractice, lessonId, solutionLoader, teachingNotes } = {}) {
    this.mount = mount; this.questions = questions; this.onPractice = onPractice || function () {}; this.lessonId = lessonId; this.solutionLoader = solutionLoader;
    this.steps = new Array(questions.length).fill(0);
    this.statuses = new Array(questions.length).fill("idle");
    this.teachingNotes = teachingNotes || {};
    const params = new URLSearchParams(location.search);
    this.index = Math.max(0, Math.min(Number(params.get("example") || 1) - 1, questions.length - 1));
    this.requestedStep = Math.max(0, Number(params.get("step") || 0));
    this.steps[this.index] = Math.max(0, Math.min(this.requestedStep, questions[this.index].whiteboard.steps.length - 1));
  }
  mountSet() { this.render(); return this; }
  render() {
    if (this.board) { this.board.destroy?.(); this.board = null; }
    const question = this.questions[this.index];
    const difficulty = { foundation:"Foundation", easy:"Easy", standard:"Standard", intermediate:"Intermediate", exam:"Exam Level", advanced:"Advanced", expert:"Expert" }[question.difficulty] || question.difficulty;
    const complete = !question.solution_gated && this.statuses[this.index] === "example_complete";
    this.mount.innerHTML = `<section class="whiteboard-question-set" aria-label="Worked example set">
      <div class="example-progress"><strong>Example ${this.index + 1} of ${this.questions.length}</strong><span class="badge">${escapeWhiteboardHtml(difficulty)}</span></div>
      <div class="example-dots" aria-hidden="true">${this.questions.map((_, i) => `<span class="${i <= this.index ? "complete" : ""}"></span>`).join("")}</div>
      ${question.solution_gated ? '<div class="card worked-example-gate"><p>Try to predict the next legal operation before opening the teacher walkthrough.</p><button type="button" class="btn btn-primary" data-example-action="reveal">Start worked example</button></div>' : ""}
      <div data-role="current-whiteboard"></div>
      <section class="example-completion" data-role="example-completion" ${complete ? "" : "hidden"} aria-live="polite">
        <strong>${this.index === this.questions.length - 1 ? "✓ You've completed all worked examples" : "✓ Example complete"}</strong>
        <p>${this.index === this.questions.length - 1 ? "You're ready to practise." : "Ready for a slightly harder one?"}</p>
        <nav class="example-controls" aria-label="Worked example navigation">
          ${this.index > 0 ? '<button type="button" class="btn btn-ghost" data-example-action="previous">← Previous Example</button>' : ""}
          <button type="button" class="btn btn-ghost" data-example-action="practice">I'm Ready to Practise</button>
          <button type="button" class="btn btn-primary" data-example-action="next">${this.index === this.questions.length - 1 || this.questions.length === 1 ? "Start Practice →" : "Next Example →"}</button>
        </nav>
      </section>
    </section>`;
    this.board = new StatefulWhiteboard(this.mount.querySelector('[data-role="current-whiteboard"]'), question.whiteboard, {
      initialStep: this.steps[this.index], guidanceLevel: question.guidance_level,
      diagnosticContext: { lesson_id: this.lessonId, question_id: question.id }, teachingNotes: this.teachingNotes,
      onStateChange: (step, status) => { this.steps[this.index] = step; this.statuses[this.index] = status; this.syncUrl(step); this.updateCompletion(); },
      onNextExample: () => this.index === this.questions.length - 1 || this.questions.length === 1 ? this.onPractice() : this.move(1)
    }).mountBoard();
    const reveal = this.mount.querySelector('[data-example-action="reveal"]');
    if (reveal) reveal.onclick = async () => {
      reveal.disabled = true;
      try {
        const full = await this.solutionLoader(question.id);
        this.questions[this.index] = full;
        this.steps[this.index] = Math.min(this.requestedStep, full.whiteboard.steps.length - 1);
        this.render();
      } catch (error) {
        reveal.disabled = false;
        reveal.insertAdjacentHTML("afterend", `<p role="alert">${escapeWhiteboardHtml(error.message)}</p>`);
      }
    };
    const previous = this.mount.querySelector('[data-example-action="previous"]');
    if (previous) previous.onclick = () => this.move(-1);
    this.mount.querySelector('[data-example-action="next"]').onclick = () => this.index === this.questions.length - 1 || this.questions.length === 1 ? this.onPractice() : this.move(1);
    this.mount.querySelector('[data-example-action="practice"]').onclick = () => this.onPractice();
    this.syncUrl(this.steps[this.index]);
    if (reveal && this.requestedStep > 0) reveal.click();
  }
  move(amount) { this.index = Math.max(0, Math.min(this.index + amount, this.questions.length - 1)); this.render(); this.mount.querySelector(".stateful-whiteboard header")?.focus(); }
  destroy() { this.board?.destroy?.(); this.board = null; this.mount.replaceChildren(); }
  updateCompletion() { const panel = this.mount.querySelector('[data-role="example-completion"]'); if (panel) panel.hidden = this.statuses[this.index] !== "example_complete"; }
  syncUrl(step) { const url = new URL(location.href); url.searchParams.set("example", this.index + 1); url.searchParams.set("step", step); history.replaceState(null, "", url); }
}
