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
  }
  mountSet() { this.render(); return this; }
  render() {
    if (this.board) { this.board.destroy?.(); this.board = null; }
    const question = this.questions[this.index];
    const difficulty = { foundation:"Foundation", easy:"Easy", standard:"Standard", intermediate:"Intermediate", exam:"Exam Level", advanced:"Advanced", expert:"Expert" }[question.difficulty] || question.difficulty;
    this.mount.innerHTML = `<section class="whiteboard-question-set" aria-label="Worked example set">
      ${question.solution_gated ? `<div class="card worked-example-gate"><label>Worked example <select data-example-action="select" aria-label="Choose worked example">${this.questions.map((_, index) => `<option value="${index}" ${this.index === index ? "selected" : ""}>Example ${index + 1} of ${this.questions.length}</option>`).join("")}</select></label><span class="badge">${escapeWhiteboardHtml(difficulty)}</span><p>Predict the next legal operation, then open the explanation.</p><button type="button" class="btn btn-primary" data-example-action="reveal">Open explanation →</button></div>` : ""}
      <div data-role="current-whiteboard"></div>
    </section>`;
    if (!question.solution_gated) {
      const currentIndex = this.index;
      this.board = new StatefulWhiteboard(this.mount.querySelector('[data-role="current-whiteboard"]'), question.whiteboard, {
        initialStep: this.steps[currentIndex], initialStatus:this.statuses[currentIndex],
        exampleIndex:currentIndex, exampleCount:this.questions.length, guidanceLevel:question.guidance_level,
        diagnosticContext:{ lesson_id:this.lessonId, question_id:question.id }, teachingNotes:this.teachingNotes,
        onStateChange:(step, status) => { if (this.index !== currentIndex) return; this.steps[currentIndex] = step; this.statuses[currentIndex] = status; this.syncUrl(step); },
        onNextExample:() => currentIndex === this.questions.length - 1 ? this.onPractice() : this.moveTo(currentIndex + 1),
        onPreviousExample:() => this.moveTo(currentIndex - 1),
        onSelectExample:index => this.moveTo(index)
      }).mountBoard();
    }
    const reveal = this.mount.querySelector('[data-example-action="reveal"]');
    if (reveal) reveal.onclick = async () => {
      const requestedIndex = this.index;
      reveal.disabled = true;
      try {
        const full = await this.solutionLoader(question.id);
        if (this.destroyed) return;
        this.questions[requestedIndex] = full;
        this.steps[requestedIndex] = Math.min(this.steps[requestedIndex], full.whiteboard.steps.length - 1);
        if (this.index === requestedIndex) this.render();
      } catch (error) {
        if (this.destroyed || this.index !== requestedIndex) return;
        reveal.disabled = false;
        reveal.insertAdjacentHTML("afterend", `<p role="alert">${escapeWhiteboardHtml(error.message)}</p>`);
      }
    };
    const picker = this.mount.querySelector('[data-example-action="select"]');
    if (picker) picker.onchange = event => this.moveTo(Number(event.target.value));
    this.syncUrl(this.steps[this.index]);
    if (reveal && this.requestedStep > 0) reveal.click();
    this.requestedStep = 0;
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
