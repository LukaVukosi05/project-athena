class StatefulWhiteboard {
  constructor(mount, block, options = {}) {
    this.mount = mount;
    this.block = block;
    this.index = Math.max(0, Math.min(options.initialStep || 0, block.steps.length - 1));
    this.guidanceLevel = options.guidanceLevel || "high";
    this.onStateChange = options.onStateChange || function () {};
    this.transitionToken = 0;
    this.destroyed = false;
    this.diagnosticContext = options.diagnosticContext || {};
    this.visualSession = AthenaVisualizationResolver.resolve(block, this.diagnosticContext);
    this.reducedMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
  }

  mountBoard() {
    this.mount.innerHTML = `<section class="stateful-whiteboard" aria-label="Interactive worked example">
      <header tabindex="-1"><span class="badge">Worked example</span><strong>${escapeWhiteboardHtml(this.block.problem)}</strong></header>
      <div class="whiteboard-workspace">
        <div class="whiteboard-stage" role="img" aria-live="polite"></div>
        <aside class="step-explanation" data-role="explanation" aria-label="Teacher explanation"></aside>
      </div>
      <div class="whiteboard-state-controls">
        <button class="btn btn-ghost" data-action="previous">← Previous Step</button>
        <button class="btn btn-secondary" data-action="play">▶ Play</button>
        <button class="btn btn-ghost" data-action="pause">Pause</button>
        <button class="btn btn-primary" data-action="next">Next Step →</button>
        <button class="btn btn-ghost" data-action="replay">Replay</button>
        <button class="btn btn-ghost" data-action="restart">Restart Example</button>
        <label class="playback-speed">Speed <select data-action="speed" aria-label="Playback speed"><option value="0.75">0.75×</option><option value="1" selected>1×</option><option value="1.25">1.25×</option><option value="1.5">1.5×</option></select></label>
        <button class="btn btn-ghost" data-action="captions" aria-pressed="true">Captions on</button>
        <button class="btn btn-ghost" data-action="mute" aria-pressed="false">Mute</button>
      </div>
      <div class="timeline-caption" data-role="caption" aria-live="polite"></div>
      <div class="timeline-checkpoint" data-role="checkpoint" hidden></div>
      <div class="progress-label" data-role="position"></div>
    </section>`;
    this.mount.querySelector('[data-action="previous"]').onclick = () => this.goTo(this.index - 1);
    this.mount.querySelector('[data-action="next"]').onclick = () => this.goTo(this.index + 1, true);
    this.mount.querySelector('[data-action="play"]').onclick = () => this.animateCurrent();
    this.mount.querySelector('[data-action="pause"]').onclick = () => this.timeline?.pause();
    this.mount.querySelector('[data-action="replay"]').onclick = () => this.timeline ? this.timeline.replay() : this.animateCurrent();
    this.mount.querySelector('[data-action="restart"]').onclick = () => this.goTo(0);
    this.mount.querySelector('[data-action="speed"]').onchange = event => this.timeline?.setSpeed(Number(event.target.value));
    this.mount.querySelector('[data-action="captions"]').onclick = event => { this.captionsEnabled=!this.captionsEnabled;this.timeline?.setCaptions(this.captionsEnabled);event.currentTarget.textContent=this.captionsEnabled?"Captions on":"Captions off";event.currentTarget.setAttribute("aria-pressed",String(this.captionsEnabled)); };
    this.mount.querySelector('[data-action="mute"]').onclick = event => { this.muted=!this.muted;this.timeline?.setMuted(this.muted);event.currentTarget.textContent=this.muted?"Unmute":"Mute";event.currentTarget.setAttribute("aria-pressed",String(this.muted)); };
    this.captionsEnabled=true;this.muted=false;
    this.visibilityHandler=()=>{if(document.hidden)this.timeline?.pause();};document.addEventListener("visibilitychange",this.visibilityHandler);
    this.render("ready");
    return this;
  }

  goTo(index, animate = false) {
    if (index < 0 || index >= this.block.steps.length) return;
    this.transitionToken++;
    this.index = index;
    this.onStateChange(index);
    if (animate && index > 0) { this.render("ready"); this.animateCurrent(); }
    else this.render(index === 0 ? "ready" : "settled");
  }

  render(phase) {
    this.timeline?.destroy(); this.timeline = null;
    const step = this.block.steps[this.index];
    const renderer = AthenaWhiteboardRegistry.resolve(step.operation.type);
    const history = [this.block.initial_expression];
    for (let index = 0; index < this.index; index += 1) {
      const previous = this.block.steps[index];
      const working = previous.working_expression;
      if (working && working !== history[history.length - 1]) history.push(working);
      if (previous.after_expression !== history[history.length - 1]) history.push(previous.after_expression);
    }
    let visualization = "";
    if (this.visualSession) {
      try { visualization = this.visualSession.render(step, ["ready","settled"].includes(phase) ? "result" : phase); }
      catch (error) { AthenaVisualizationDiagnostics.emit("VISUALIZATION_RENDER_FAILED",{...this.diagnosticContext,block_id:this.block.id,template:this.visualSession.instruction ? `${this.visualSession.instruction.type}:${this.visualSession.instruction.template}` : "fallback"}); visualization = `<div class="visualization-fallback" role="note"><strong>Diagram unavailable.</strong><p>${escapeWhiteboardHtml(step.screen_reader_description)}</p></div>`; }
    }
    const stage = this.mount.querySelector(".whiteboard-stage");
    stage.innerHTML = `${visualization}${renderer.render(step, ["ready","settled"].includes(phase) ? "result" : phase, { history, hasVisualization:Boolean(this.visualSession) })}`;
    stage.setAttribute("aria-label", step.screen_reader_description);
    if (step.events?.length) {
      this.timeline = new TimelineController(stage, step, {
        caption: this.mount.querySelector('[data-role="caption"]'),
        narration: step.narration_audio_url ? new PrerecordedNarrationProvider(step.narration_audio_url) : new BrowserNarrationProvider(),
        onStateChange: controller => {
          this.mount.querySelector('[data-action="play"]').textContent = controller.playing ? "Playing…" : "▶ Play";
          this.mount.querySelector('[data-action="pause"]').disabled = !controller.playing;
        },
        onCheckpoint: (event, controller) => this.showCheckpoint(event, controller),
      });
      this.timeline.setCaptions(this.captionsEnabled);
      this.timeline.setMuted(this.muted);
      if (this.reducedMotion || phase === "settled") this.timeline.completeReducedMotion();
    }
    const showFullGuidance = this.guidanceLevel === "high";
    const showModerateGuidance = showFullGuidance || this.guidanceLevel === "moderate";
    this.mount.querySelector('[data-role="explanation"]').innerHTML = `
      <h4>${escapeWhiteboardHtml(step.title)}</h4>
      ${this.guidanceLevel === "reduced" && this.index > 0 ? '<p class="prediction-prompt">What do you think we should do next?</p>' : ""}
      ${this.guidanceLevel === "minimal" ? `<button type="button" class="btn btn-ghost" data-action="reveal-help" aria-expanded="false">Explain this step</button><div data-role="minimal-help" hidden><p>${escapeWhiteboardHtml(step.explanation.why)}</p></div>` : `<dl>${showFullGuidance ? `<div><dt>WHAT</dt><dd>${escapeWhiteboardHtml(step.explanation.what)}</dd></div>` : ""}
      <div><dt>WHY</dt><dd>${escapeWhiteboardHtml(step.explanation.why)}</dd></div>
      ${showFullGuidance ? `<div><dt>PURPOSE</dt><dd>${escapeWhiteboardHtml(step.explanation.purpose)}</dd></div><div><dt>REMEMBER</dt><dd>${escapeWhiteboardHtml(step.explanation.remember)}</dd></div>` : ""}</dl>
      ${showModerateGuidance && step.common_mistake ? `<p class="watch-out"><strong>WATCH OUT:</strong> ${escapeWhiteboardHtml(step.common_mistake)}</p>` : ""}`}`;
    const help = this.mount.querySelector('[data-action="reveal-help"]');
    if (help) help.onclick = () => { const panel = this.mount.querySelector('[data-role="minimal-help"]'); panel.hidden = !panel.hidden; help.setAttribute("aria-expanded", String(!panel.hidden)); };
    this.mount.querySelector('[data-role="position"]').textContent = `State ${this.index} of ${this.block.steps.length - 1}`;
    this.mount.querySelector('[data-action="previous"]').disabled = this.index === 0;
    this.mount.querySelector('[data-action="next"]').disabled = this.index === this.block.steps.length - 1;
  }

  animateCurrent() {
    if (this.timeline) { this.timeline.play(); return; }
    const token = ++this.transitionToken;
    this.render("operation");
    this.explainAgain();
    if (this.reducedMotion) { this.render("result"); return; }
    setTimeout(() => { if (token === this.transitionToken) this.render("result"); }, 900);
  }

  destroy() {
    if (this.destroyed) return;
    this.destroyed = true;
    this.transitionToken++;
    this.visualSession?.destroy();
    this.timeline?.destroy();
    if (this.visibilityHandler && typeof document !== "undefined") document.removeEventListener("visibilitychange", this.visibilityHandler);
    if (typeof window !== "undefined" && "speechSynthesis" in window) speechSynthesis.cancel();
    this.mount.replaceChildren();
  }

  showCheckpoint(event, controller) {
    const panel = this.mount.querySelector('[data-role="checkpoint"]');
    panel.hidden = false;
    panel.innerHTML = `<strong>Think first</strong><p>${escapeWhiteboardHtml(event.text)}</p><button type="button" class="btn btn-primary">Continue</button>`;
    panel.querySelector("button").onclick = () => { panel.hidden = true; controller.play(); };
    panel.querySelector("button").focus();
  }

  explainAgain() {
    if (typeof window === "undefined" || !("speechSynthesis" in window)) return;
    const step = this.block.steps[this.index];
    const words = `${step.title}. What: ${step.explanation.what} Why: ${step.explanation.why} Purpose: ${step.explanation.purpose} Remember: ${step.explanation.remember}`;
    const utterance = new SpeechSynthesisUtterance(words);
    utterance.lang = "en-ZA";
    utterance.rate = 0.9;
    speechSynthesis.cancel();
    speechSynthesis.speak(utterance);
  }
}
