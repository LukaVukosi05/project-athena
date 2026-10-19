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
    if (this.steps[this.index]) this.statuses[this.index] = this.steps[this.index] === questions[this.index].whiteboard.steps.length - 1 ? "example_complete" : "step_complete";
    this.destroyed = false;
    this.loading = new Set();
    this.loadErrors = new Map();
  }
  mountSet() { this.render(); return this; }
  render() {
    if (this.board) { this.board.destroy?.(); this.board = null; }
    const question = this.questions[this.index];
    this.mount.innerHTML = `<section class="whiteboard-question-set" aria-label="Worked example set">
      <div data-role="current-whiteboard"></div>
      <div data-role="example-loading" role="status" aria-live="polite"></div>
    </section>`;
    const currentIndex = this.index;
    this.board = new StatefulWhiteboard(this.mount.querySelector('[data-role="current-whiteboard"]'), question.whiteboard, {
        initialStep: this.steps[currentIndex], initialStatus:this.statuses[currentIndex],
        exampleIndex:currentIndex, exampleCount:this.questions.length, pending:Boolean(question.solution_gated), guidanceLevel:question.guidance_level,
        diagnosticContext:{ lesson_id:this.lessonId, question_id:question.id }, teachingNotes:this.teachingNotes,
        onStateChange:(step, status) => { if (this.index !== currentIndex) return; this.steps[currentIndex] = step; this.statuses[currentIndex] = status; this.syncUrl(step); },
        onNextExample:() => currentIndex === this.questions.length - 1 ? this.onPractice() : this.moveTo(currentIndex + 1),
        onPreviousExample:() => this.moveTo(currentIndex - 1),
        onSelectExample:index => this.moveTo(index)
      }).mountBoard();
    this.syncUrl(this.steps[this.index]);
    if (question.solution_gated) {
      this.mount.querySelector('[data-role="example-loading"]').textContent = "Loading the teaching steps…";
      this.loadExample(currentIndex);
    }
    this.requestedStep = 0;
  }
  async loadExample(index) {
    if (this.loading.has(index) || !this.questions[index]?.solution_gated) return;
    this.loading.add(index);
    const message = this.mount.querySelector('[data-role="example-loading"]');
    if (this.index === index && message) message.textContent = "Loading the teaching steps…";
    try {
      if (!this.solutionLoader) throw new Error("Teaching steps are unavailable.");
      const full = await this.solutionLoader(this.questions[index].id);
      if (this.destroyed) return;
      this.questions[index] = full;
      this.steps[index] = Math.min(this.steps[index], full.whiteboard.steps.length - 1);
      this.loadErrors.delete(index);
      if (this.index === index) this.render();
    } catch (error) {
      if (this.destroyed) return;
      this.loadErrors.set(index, error);
      if (this.index === index && message) {
        message.innerHTML = `<p role="alert">${escapeWhiteboardHtml(error.message)}</p><button type="button" class="btn btn-ghost" data-example-action="retry">Retry loading example</button>`;
        message.querySelector('[data-example-action="retry"]')?.addEventListener('click', () => this.loadExample(index));
      }
    } finally { this.loading.delete(index); }
  }
  moveTo(index) {
    if (!Number.isInteger(index) || index < 0 || index >= this.questions.length || index === this.index) return;
    if (["playing", "paused"].includes(this.statuses[this.index])) {
      this.steps[this.index] = Math.max(0, this.steps[this.index] - 1);
      this.statuses[this.index] = this.steps[this.index] ? "step_complete" : "idle";
    }
    this.index = index;
    this.requestedStep = 0;
    this.render();
    this.mount.querySelector(".stateful-whiteboard header")?.focus();
  }
  move(amount) { this.moveTo(this.index + amount); }
  destroy() { this.destroyed = true; this.board?.destroy?.(); this.board = null; this.mount.replaceChildren(); }
  syncUrl(step) { const url = new URL(location.href); url.searchParams.set("example", this.index + 1); url.searchParams.set("step", step); history.replaceState(null, "", url); }
}
