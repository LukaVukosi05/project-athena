class StatefulWhiteboard {
  constructor(mount, block, options = {}) {
    this.mount = mount; this.block = block;
    this.index = Math.max(0, Math.min(options.initialStep || 0, block.steps.length - 1));
    this.status = options.initialStatus || (this.index > 0 ? (this.index === block.steps.length - 1 ? "example_complete" : "step_complete") : "idle");
    this.guidanceLevel = options.guidanceLevel || "high";
    this.onStateChange = options.onStateChange || function () {};
    this.onNextExample = options.onNextExample || function () {};
    this.onPreviousExample = options.onPreviousExample || function () {};
    this.onSelectExample = options.onSelectExample || function () {};
    this.exampleIndex = options.exampleIndex || 0;
    this.exampleCount = options.exampleCount || 1;
    this.pending = Boolean(options.pending);
    this.teachingNotes = options.teachingNotes || {};
    this.diagnosticContext = options.diagnosticContext || {};
    this.visualSession = AthenaVisualizationResolver.resolve(block, this.diagnosticContext);
    this.systemReducedMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
    this.reducedMotion = this.systemReducedMotion;
    this.playbackSpeed = 1; this.captionsEnabled = true; this.muted = false;
    this.destroyed = false; this.transitionToken = 0; this.actionLocked = false;
  }

  speakerIcon(muted) {
    return `<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 9h4l5-4v14l-5-4H4z"/>${muted ? '<path d="m17 9 5 6m0-6-5 6"/>' : '<path d="M17 9a5 5 0 0 1 0 6m2-9a9 9 0 0 1 0 12"/>'}</svg>`;
  }

  mountBoard() {
    this.mount.innerHTML = `<section class="stateful-whiteboard" aria-label="Interactive worked example" data-controller-state="${this.status}">
      <header tabindex="-1"><div class="whiteboard-heading-row"><span class="whiteboard-example-title">Worked example ${this.exampleIndex + 1} of ${this.exampleCount}</span><div class="whiteboard-utilities"><button type="button" class="btn btn-ghost whiteboard-icon-button" data-action="mute" aria-label="Mute audio" aria-pressed="false" title="Audio on">${this.speakerIcon(false)}</button><details class="whiteboard-settings"><summary class="btn btn-ghost whiteboard-icon-button" aria-label="More whiteboard settings" title="More settings">⋯</summary><div class="whiteboard-settings-panel"><button type="button" class="btn btn-ghost" data-action="replay">Replay step</button><button type="button" class="btn btn-ghost" data-action="restart">Restart example</button><button type="button" class="btn btn-ghost" data-action="captions" aria-pressed="true">Captions on</button><label class="playback-speed">Playback speed <select data-action="speed" aria-label="Playback speed"><option value="0.75">0.75×</option><option value="1" selected>1×</option><option value="1.25">1.25×</option><option value="1.5">1.5×</option></select></label><label class="reduced-motion-setting"><input type="checkbox" data-action="reduced-motion" ${this.reducedMotion ? "checked" : ""}> Reduced motion</label></div></details></div></div><strong>${escapeWhiteboardHtml(this.block.problem)}</strong><nav class="whiteboard-example-navigation" aria-label="Choose worked example">${Array.from({ length:this.exampleCount }, (_, index) => `<button type="button" class="whiteboard-example-number ${index === this.exampleIndex ? "is-current" : ""}" data-example-index="${index}" aria-label="Example ${index + 1} of ${this.exampleCount}" ${index === this.exampleIndex ? 'aria-current="step"' : ""}>${index + 1}</button>`).join("")}</nav></header>
      <div class="whiteboard-workspace"><div class="whiteboard-stage" role="region" aria-label="Mathematical whiteboard"></div>
      <div class="timeline-caption" data-role="caption" aria-live="polite" aria-atomic="true"></div>
      <div class="timeline-checkpoint" data-role="checkpoint" hidden></div>
      <div class="whiteboard-control-bar" aria-label="Whiteboard controls">
        <button type="button" class="btn btn-ghost" data-action="previous" aria-label="Previous mathematical step or example">← Previous</button>
        <span class="whiteboard-step-status" data-role="position" aria-live="polite"></span>
        <button type="button" class="btn btn-primary whiteboard-primary-action" data-action="primary"></button>
        <button type="button" class="btn btn-ghost whiteboard-pause" data-action="pause" aria-label="Pause explanation" hidden><svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" aria-hidden="true"><rect x="5" y="4" width="5" height="16" rx="1"/><rect x="14" y="4" width="5" height="16" rx="1"/></svg></button>
      </div>
      </div>
      <details class="whiteboard-teaching-notes"><summary>Teaching notes</summary><div class="teaching-notes-grid" data-role="teaching-notes"></div></details>
    </section>`;
    this.listeners = new AbortController();
    const bind = (action, event, handler) => this.mount.querySelector(`[data-action="${action}"]`).addEventListener(event, handler, { signal:this.listeners.signal });
    bind("primary", "click", () => this.runAction(() => this.primaryAction()));
    bind("previous", "click", () => this.runAction(() => this.previousStep()));
    bind("pause", "click", () => this.runAction(() => this.pauseCurrent()));
    this.mount.querySelectorAll("[data-example-index]").forEach(button => button.addEventListener("click", () => this.onSelectExample(Number(button.dataset.exampleIndex)), { signal:this.listeners.signal }));
    bind("replay", "click", () => this.runAction(() => this.replayStep()));
    bind("restart", "click", () => this.runAction(() => this.restartExample()));
    bind("speed", "change", event => { this.playbackSpeed = Number(event.target.value); this.timeline?.setSpeed(this.playbackSpeed); });
    bind("captions", "click", event => { this.captionsEnabled = !this.captionsEnabled; this.timeline?.setCaptions(this.captionsEnabled); event.currentTarget.textContent = this.captionsEnabled ? "Captions on" : "Captions off"; event.currentTarget.setAttribute("aria-pressed", String(this.captionsEnabled)); });
    bind("mute", "click", event => { this.muted = !this.muted; this.timeline?.setMuted(this.muted); event.currentTarget.innerHTML = this.speakerIcon(this.muted); event.currentTarget.title = this.muted ? "Audio off" : "Audio on"; event.currentTarget.setAttribute("aria-label", this.muted ? "Unmute audio" : "Mute audio"); event.currentTarget.setAttribute("aria-pressed", String(this.muted)); });
    bind("reduced-motion", "change", event => { this.reducedMotion = event.currentTarget.checked; });
    document.addEventListener("keydown", event => {
      if (event.code !== "Space" || /^(INPUT|TEXTAREA|SELECT|BUTTON|A)$/.test(event.target?.tagName || "")) return;
      if (this.status === "playing") { event.preventDefault(); this.runAction(() => this.pauseCurrent()); }
    }, { signal:this.listeners.signal });
    this.visibilityHandler = () => { if (document.hidden && this.status === "playing") this.pauseCurrent(); };
    document.addEventListener("visibilitychange", this.visibilityHandler);
    this.reconstruct(["step_complete", "example_complete"].includes(this.status) ? "result" : "ready", this.status, false);
    return this;
  }

  runAction(action) { if (this.destroyed || this.actionLocked) return; this.actionLocked = true; try { action(); } finally { queueMicrotask(() => { this.actionLocked = false; }); } }
  primaryAction() {
    if (this.status === "idle") this.startCurrent();
    else if (this.status === "playing") return;
    else if (this.status === "paused") this.continueCurrent();
    else if (this.status === "step_complete") { this.nextStep(); this.startCurrent(); }
    else if (this.status === "example_complete") this.onNextExample();
  }
  startCurrent() {
    if (this.reducedMotion) { this.reconstruct("result", this.isFinalStep() ? "example_complete" : "step_complete"); return; }
    this.reconstruct("operation", "playing");
    if (this.timeline) { this.timeline.setSpeed(this.playbackSpeed); this.timeline.play(); } else this.completeCurrentStep();
  }
  pauseCurrent() { if (this.status !== "playing") return; this.timeline?.pause(); this.setStatus("paused"); }
  continueCurrent() { if (this.status !== "paused") return; this.mount.querySelector('[data-role="checkpoint"]').hidden = true; this.setStatus("playing"); this.timeline?.play(); }
  nextStep() { if (this.status !== "step_complete" || this.isFinalStep()) return; this.index += 1; this.reconstruct("ready", "idle"); }
  previousStep() { if (this.index === 0) { if (this.exampleIndex > 0) this.onPreviousExample(); return; } this.index -= 1; this.reconstruct("result", "step_complete"); }
  replayStep() { if (this.reducedMotion) this.reconstruct("result", this.isFinalStep() ? "example_complete" : "step_complete"); else { this.reconstruct("operation", "playing", false); this.timeline?.setSpeed(this.playbackSpeed); this.timeline?.play(); } }
  restartExample() { this.index = 0; this.reconstruct("ready", "idle"); this.mount.querySelector(".stateful-whiteboard header")?.focus(); }
  completeCurrentStep() { if (!this.destroyed) this.reconstruct("result", this.isFinalStep() ? "example_complete" : "step_complete"); }
  isFinalStep() { return this.index === this.block.steps.length - 1; }
  stopTimeline() { this.transitionToken += 1; this.timeline?.destroy(); this.timeline = null; }

  reconstruct(phase, status, notify = true) {
    this.stopTimeline(); this.renderPhase = phase;
    this.mount.querySelector('[data-role="checkpoint"]').hidden = true;
    const step = this.block.steps[this.index];
    const renderer = AthenaWhiteboardRegistry.resolve(step.operation.type);
    const history = [this.block.initial_expression];
    for (let cursor = 0; cursor < this.index; cursor += 1) {
      const previous = this.block.steps[cursor];
      if (previous.working_expression && previous.working_expression !== history.at(-1)) history.push(previous.working_expression);
      if (previous.after_expression !== history.at(-1)) history.push(previous.after_expression);
    }
    let visualization = "";
    if (this.visualSession) {
      try { visualization = this.visualSession.render(step, phase); }
      catch (error) { AthenaVisualizationDiagnostics.emit("VISUALIZATION_RENDER_FAILED", { ...this.diagnosticContext, block_id:this.block.id }); visualization = `<div class="visualization-fallback" role="note"><strong>Diagram unavailable.</strong><p>${escapeWhiteboardHtml(step.screen_reader_description)}</p></div>`; }
    }
    const stage = this.mount.querySelector(".whiteboard-stage");
    const writtenSteps = this.block.steps.slice(0, this.index + (phase === "result" ? 1 : 0));
    const trace = writtenSteps.length ? `<section class="g8-completed-steps" aria-label="Written solution so far"><h3>Written solution so far</h3><p>Original: ${escapeWhiteboardHtml(this.block.initial_expression)}</p><ol>${writtenSteps.map((prior, index) => `<li><span>Step ${index + 1}</span><div>${prior.working_expression ? `<small>Operation: ${escapeWhiteboardHtml(prior.working_expression)}</small>` : ""}<strong>${escapeWhiteboardHtml(prior.after_expression)}</strong></div></li>`).join("")}</ol></section>` : "";
    stage.innerHTML = `${visualization}${renderer.render(step, phase, { history, hasVisualization:Boolean(this.visualSession) })}${this.visualSession?.type === "algebra" || this.block.visualization?.type === "algebra" ? trace : ""}`;
    stage.setAttribute("aria-label", step.screen_reader_description);
    const targets = [...new Set((step.events || []).flatMap(event => event.targets || []))];
    const missing = targets.filter(id => !stage.querySelector(`[data-object-id="${CSS.escape(id)}"]`));
    if (missing.length) { stage.dataset.missingTargets = missing.join(","); AthenaVisualizationDiagnostics.emit("EVENT_TARGETS_MISSING", { ...this.diagnosticContext, block_id:this.block.id, step_id:step.id || String(step.step_number), targets:missing }); }
    else delete stage.dataset.missingTargets;
    this.renderTeachingNotes(step); this.renderOpeningCaption(step, phase);
    if (step.events?.length && (phase === "ready" || phase === "operation")) this.createTimeline(step);
    if (phase === "result") this.applyCompleteTimeline(step);
    this.setStatus(status, notify);
  }

  createTimeline(step) {
    const token = this.transitionToken;
    this.timeline = new TimelineController(this.mount.querySelector(".whiteboard-stage"), step, {
      caption:this.mount.querySelector('[data-role="caption"]'),
      narration:step.narration_audio_url ? new PrerecordedNarrationProvider(step.narration_audio_url) : new BrowserNarrationProvider(),
      onStateChange:controller => {
        if (this.destroyed || token !== this.transitionToken || this.suppressCompletion) return;
        if (!controller.playing && controller.position >= step.duration_ms) queueMicrotask(() => {
          if (!this.destroyed && token === this.transitionToken && this.status === "playing") this.completeCurrentStep();
        });
      },
      onCheckpoint:(event, controller) => this.showCheckpoint(event, controller),
    });
    this.timeline.setCaptions(this.captionsEnabled); this.timeline.setMuted(this.muted);
  }
  applyCompleteTimeline(step) { if (!step.events?.length) return; this.createTimeline(step); this.suppressCompletion = true; this.timeline.completeReducedMotion(); this.suppressCompletion = false; }
  renderOpeningCaption(step, phase) {
    const caption = this.mount.querySelector('[data-role="caption"]');
    const events = step.events || []; const captions = events.filter(event => event.type === "caption");
    const event = phase === "result" ? captions.at(-1) : captions[0] || events.find(item => item.type === "narration");
    caption.hidden = !this.captionsEnabled; caption.textContent = event?.text || step.explanation?.what || "";
  }
  renderTeachingNotes(step) {
    const note = (title, value) => value ? `<section><h4>${title}</h4><p>${escapeWhiteboardHtml(value)}</p></section>` : "";
    this.mount.querySelector('[data-role="teaching-notes"]').innerHTML = [
      note("Why this matters", this.teachingNotes.why || step.explanation?.why), note("Purpose", step.explanation?.purpose),
      note("Review", step.explanation?.remember || this.teachingNotes.review), note("Misconception guidance", step.common_mistake),
    ].join("");
  }
  setStatus(status, notify = true) {
    this.status = status; this.mount.querySelector(".stateful-whiteboard").dataset.controllerState = status;
    const labels = { idle:this.index ? "Explain this step →" : "Start explanation →", playing:"Explaining…", paused:"Continue explanation →", step_complete:"Next step →", example_complete:this.exampleIndex + 1 < this.exampleCount ? "Next example →" : "Start practice →" };
    const primary = this.mount.querySelector('[data-action="primary"]'); primary.textContent = labels[status]; primary.setAttribute("aria-label", labels[status]);
    primary.disabled = status === "playing" || this.pending;
    if (this.pending) primary.textContent = "Loading example…";
    this.mount.querySelector('[data-action="previous"]').disabled = this.index === 0 && this.exampleIndex === 0;
    this.mount.querySelector('[data-action="pause"]').hidden = status !== "playing";
    const replay = this.mount.querySelector('[data-action="replay"]'); replay.disabled = status === "playing"; replay.hidden = status === "example_complete";
    this.mount.querySelector('[data-role="position"]').textContent = `Step ${this.index + 1} of ${this.block.steps.length}`;
    if (notify) this.onStateChange(this.index, status);
  }
  destroy() { if (this.destroyed) return; this.destroyed = true; this.listeners?.abort(); this.stopTimeline(); this.visualSession?.destroy(); if (this.visibilityHandler) document.removeEventListener("visibilitychange", this.visibilityHandler); this.mount.replaceChildren(); }
  showCheckpoint(event, controller) {
    this.setStatus("paused"); const panel = this.mount.querySelector('[data-role="checkpoint"]'); panel.hidden = false;
    panel.innerHTML = `<strong>Think first</strong><p>${escapeWhiteboardHtml(event.text)}</p>`;
    this.mount.querySelector('[data-action="primary"]').focus();
  }
}
