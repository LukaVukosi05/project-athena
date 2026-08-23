class WhiteboardQuestionSet {
  constructor(mount, questions, { onPractice } = {}) {
    this.mount = mount; this.questions = questions; this.onPractice = onPractice || function () {};
    this.steps = new Array(questions.length).fill(0);
    const params = new URLSearchParams(location.search);
    this.index = Math.max(0, Math.min(Number(params.get("example") || 1) - 1, questions.length - 1));
    this.steps[this.index] = Math.max(0, Math.min(Number(params.get("step") || 0), questions[this.index].whiteboard.steps.length - 1));
  }
  mountSet() { this.render(); return this; }
  render() {
    const question = this.questions[this.index];
    const difficulty = { foundation:"Foundation", easy:"Easy", standard:"Standard", intermediate:"Intermediate", exam:"Exam Level", advanced:"Advanced", expert:"Expert" }[question.difficulty] || question.difficulty;
    const complete = this.steps[this.index] === question.whiteboard.steps.length - 1;
    this.mount.innerHTML = `<section class="whiteboard-question-set" aria-label="Worked example set">
      <div class="example-progress"><strong>Example ${this.index + 1} of ${this.questions.length}</strong><span class="badge">${escapeWhiteboardHtml(difficulty)}</span></div>
      <div class="example-dots" aria-hidden="true">${this.questions.map((_, i) => `<span class="${i <= this.index ? "complete" : ""}"></span>`).join("")}</div>
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
      onStateChange: step => { this.steps[this.index] = step; this.syncUrl(step); this.updateCompletion(); }
    }).mountBoard();
    const previous = this.mount.querySelector('[data-example-action="previous"]');
    if (previous) previous.onclick = () => this.move(-1);
    this.mount.querySelector('[data-example-action="next"]').onclick = () => this.index === this.questions.length - 1 || this.questions.length === 1 ? this.onPractice() : this.move(1);
    this.mount.querySelector('[data-example-action="practice"]').onclick = () => this.onPractice();
    this.syncUrl(this.steps[this.index]);
  }
  move(amount) { this.index = Math.max(0, Math.min(this.index + amount, this.questions.length - 1)); this.render(); }
  updateCompletion() { const panel = this.mount.querySelector('[data-role="example-completion"]'); if (panel) panel.hidden = this.steps[this.index] !== this.questions[this.index].whiteboard.steps.length - 1; }
  syncUrl(step) { const url = new URL(location.href); url.searchParams.set("example", this.index + 1); url.searchParams.set("step", step); history.replaceState(null, "", url); }
}
