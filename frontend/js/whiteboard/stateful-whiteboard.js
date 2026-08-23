class StatefulWhiteboard {
  constructor(mount, block) {
    this.mount = mount;
    this.block = block;
    this.index = 0;
    this.transitionToken = 0;
    this.reducedMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
  }

  mountBoard() {
    this.mount.innerHTML = `<section class="stateful-whiteboard" aria-label="Interactive worked example">
      <header><span class="badge">Worked example</span><strong>${escapeWhiteboardHtml(this.block.problem)}</strong></header>
      <div class="whiteboard-workspace">
        <div class="whiteboard-stage" role="img" aria-live="polite"></div>
        <aside class="step-explanation" data-role="explanation" aria-label="Teacher explanation"></aside>
      </div>
      <div class="whiteboard-state-controls">
        <button class="btn btn-ghost" data-action="previous">← Previous Step</button>
        <button class="btn btn-secondary" data-action="play">▶ Play</button>
        <button class="btn btn-primary" data-action="next">Next Step →</button>
        <button class="btn btn-ghost" data-action="replay">Replay</button>
        <button class="btn btn-ghost" data-action="explain">Explain Again</button>
      </div>
      <div class="progress-label" data-role="position"></div>
    </section>`;
    this.mount.querySelector('[data-action="previous"]').onclick = () => this.goTo(this.index - 1);
    this.mount.querySelector('[data-action="next"]').onclick = () => this.goTo(this.index + 1, true);
    this.mount.querySelector('[data-action="play"]').onclick = () => this.animateCurrent();
    this.mount.querySelector('[data-action="replay"]').onclick = () => this.animateCurrent();
    this.mount.querySelector('[data-action="explain"]').onclick = () => this.explainAgain();
    this.render("result");
    return this;
  }

  goTo(index, animate = false) {
    if (index < 0 || index >= this.block.steps.length) return;
    this.transitionToken++;
    this.index = index;
    if (animate && index > 0) this.animateCurrent();
    else this.render("result");
  }

  render(phase) {
    const step = this.block.steps[this.index];
    const renderer = AthenaWhiteboardRegistry.resolve(step.operation.type);
    const history = [this.block.initial_expression];
    for (let index = 0; index < this.index; index += 1) {
      const previous = this.block.steps[index];
      const working = previous.working_expression;
      if (working && working !== history[history.length - 1]) history.push(working);
      if (previous.after_expression !== history[history.length - 1]) history.push(previous.after_expression);
    }
    this.mount.querySelector(".whiteboard-stage").innerHTML = renderer.render(step, phase, { history });
    this.mount.querySelector(".whiteboard-stage").setAttribute("aria-label", step.screen_reader_description);
    this.mount.querySelector('[data-role="explanation"]').innerHTML = `
      <h4>${escapeWhiteboardHtml(step.title)}</h4>
      <dl><div><dt>WHAT</dt><dd>${escapeWhiteboardHtml(step.explanation.what)}</dd></div>
      <div><dt>WHY</dt><dd>${escapeWhiteboardHtml(step.explanation.why)}</dd></div>
      <div><dt>PURPOSE</dt><dd>${escapeWhiteboardHtml(step.explanation.purpose)}</dd></div>
      <div><dt>REMEMBER</dt><dd>${escapeWhiteboardHtml(step.explanation.remember)}</dd></div></dl>
      ${step.common_mistake ? `<p class="watch-out"><strong>WATCH OUT:</strong> ${escapeWhiteboardHtml(step.common_mistake)}</p>` : ""}`;
    this.mount.querySelector('[data-role="position"]').textContent = `State ${this.index} of ${this.block.steps.length - 1}`;
    this.mount.querySelector('[data-action="previous"]').disabled = this.index === 0;
    this.mount.querySelector('[data-action="next"]').disabled = this.index === this.block.steps.length - 1;
  }

  animateCurrent() {
    const token = ++this.transitionToken;
    this.render("operation");
    this.explainAgain();
    if (this.reducedMotion) { this.render("result"); return; }
    setTimeout(() => { if (token === this.transitionToken) this.render("result"); }, 900);
  }

  explainAgain() {
    if (!("speechSynthesis" in window)) return;
    const step = this.block.steps[this.index];
    const words = `${step.title}. What: ${step.explanation.what} Why: ${step.explanation.why} Purpose: ${step.explanation.purpose} Remember: ${step.explanation.remember}`;
    const utterance = new SpeechSynthesisUtterance(words);
    utterance.lang = "en-ZA";
    utterance.rate = 0.9;
    speechSynthesis.cancel();
    speechSynthesis.speak(utterance);
  }
}
