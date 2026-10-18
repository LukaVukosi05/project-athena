class StatefulWhiteboard {
  constructor(mount, block, options = {}) {
    this.mount = mount; this.block = block;
    this.index = Math.max(0, Math.min(options.initialStep || 0, block.steps.length - 1));
    this.status = this.index > 0 ? (this.index === block.steps.length - 1 ? "example_complete" : "step_complete") : "idle";
    this.guidanceLevel = options.guidanceLevel || "high";
    this.onStateChange = options.onStateChange || function () {};
    this.onNextExample = options.onNextExample || function () {};
    this.teachingNotes = options.teachingNotes || {};
    this.diagnosticContext = options.diagnosticContext || {};
    this.visualSession = AthenaVisualizationResolver.resolve(block, this.diagnosticContext);
    this.systemReducedMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
    this.reducedMotion = this.systemReducedMotion;
    this.playbackSpeed = 1; this.captionsEnabled = true; this.muted = false;
    this.destroyed = false; this.transitionToken = 0; this.actionLocked = false;
  }

  mountBoard() {
    this.mount.innerHTML = `<section class="stateful-whiteboard" aria-label="Interactive worked example" data-controller-state="${this.status}">
      <header tabindex="-1"><span class="badge">Worked example</span><strong>${escapeWhiteboardHtml(this.block.problem)}</strong></header>
      <div class="whiteboard-workspace"><div class="whiteboard-stage" role="img" aria-label="Mathematical whiteboard"></div>
      <div class="timeline-caption" data-role="caption" aria-live="polite" aria-atomic="true"></div>
      <div class="timeline-checkpoint" data-role="checkpoint" hidden></div>
      <div class="whiteboard-control-bar" aria-label="Whiteboard controls">
        <div class="whiteboard-step-navigation"><button type="button" class="btn btn-ghost" data-action="previous" aria-label="Previous mathematical step">Previous step</button>
        <span class="whiteboard-step-status" data-role="position" aria-live="polite"></span>
        <button type="button" class="btn btn-ghost" data-action="next" aria-label="Next mathematical step">Next step</button></div>
        <button type="button" class="btn btn-primary whiteboard-primary-action" data-action="primary"></button>
        <div class="whiteboard-secondary-controls"><button type="button" class="btn btn-ghost" data-action="replay" aria-label="Replay current mathematical step">Replay</button>
        <button type="button" class="btn btn-ghost" data-action="captions" aria-pressed="true">Captions on</button>
        <button type="button" class="btn btn-ghost" data-action="mute" aria-pressed="false">Audio on</button>
        <details class="whiteboard-settings"><summary class="btn btn-ghost" aria-label="More playback settings">Settings</summary>
          <div class="whiteboard-settings-panel">
            <button type="button" class="btn btn-ghost" data-action="restart">Restart example</button>
            <label class="playback-speed">Playback speed <select data-action="speed" aria-label="Playback speed"><option value="0.75">0.75×</option><option value="1" selected>1×</option><option value="1.25">1.25×</option><option value="1.5">1.5×</option></select></label>
            <label class="reduced-motion-setting"><input type="checkbox" data-action="reduced-motion" ${this.reducedMotion ? "checked" : ""}> Reduced motion</label>
          </div>
        </details></div>
      </div>
      <details class="whiteboard-solution-trail"><summary>Solution trail</summary><ol data-role="solution-trail"></ol></details></div>
      <details class="whiteboard-teaching-notes"><summary>Teaching notes</summary><div class="teaching-notes-grid" data-role="teaching-notes"></div></details>
    </section>`;
    this.listeners = new AbortController();
    const bind = (action, event, handler) => this.mount.querySelector(`[data-action="${action}"]`).addEventListener(event, handler, { signal:this.listeners.signal });
    bind("primary", "click", () => this.runAction(() => this.primaryAction()));
    bind("previous", "click", () => this.runAction(() => this.previousStep()));
    bind("next", "click", () => this.runAction(() => this.nextStep()));
    bind("replay", "click", () => this.runAction(() => this.replayStep()));
    bind("restart", "click", () => this.runAction(() => this.restartExample()));
    bind("speed", "change", event => { this.playbackSpeed = Number(event.target.value); this.timeline?.setSpeed(this.playbackSpeed); });
    bind("captions", "click", event => { this.captionsEnabled = !this.captionsEnabled; this.timeline?.setCaptions(this.captionsEnabled); event.currentTarget.textContent = this.captionsEnabled ? "Captions on" : "Captions off"; event.currentTarget.setAttribute("aria-pressed", String(this.captionsEnabled)); });
    bind("mute", "click", event => { this.muted = !this.muted; this.timeline?.setMuted(this.muted); event.currentTarget.textContent = this.muted ? "Audio off" : "Audio on"; event.currentTarget.setAttribute("aria-pressed", String(this.muted)); });
    bind("reduced-motion", "change", event => { this.reducedMotion = event.currentTarget.checked; });
    document.addEventListener("keydown", event => {
      if (event.code !== "Space" || /^(INPUT|TEXTAREA|SELECT|BUTTON|A)$/.test(event.target?.tagName || "")) return;
      event.preventDefault(); this.runAction(() => this.primaryAction());
    }, { signal:this.listeners.signal });
    this.visibilityHandler = () => { if (document.hidden && this.status === "playing") this.pauseCurrent(); };
    document.addEventListener("visibilitychange", this.visibilityHandler);
    this.reconstruct(this.index > 0 ? "result" : "ready", this.status, false);
    return this;
  }

  runAction(action) { if (this.destroyed || this.actionLocked) return; this.actionLocked = true; try { action(); } finally { queueMicrotask(() => { this.actionLocked = false; }); } }
  primaryAction() {
    if (this.status === "idle") this.startCurrent();
    else if (this.status === "playing") this.pauseCurrent();
    else if (this.status === "paused") this.continueCurrent();
    else if (this.status === "step_complete") { this.nextStep(); this.startCurrent(); }
    else if (this.status === "example_complete") { this.restartExample(); this.startCurrent(); }
  }
  startCurrent() {
    if (this.reducedMotion) { this.reconstruct("result", this.isFinalStep() ? "example_complete" : "step_complete"); return; }
    this.reconstruct("operation", "playing", false);
    if (this.timeline) { this.timeline.setSpeed(this.playbackSpeed); this.timeline.play(); } else this.completeCurrentStep();
  }
  pauseCurrent() { if (this.status !== "playing") return; this.timeline?.pause(); this.setStatus("paused"); }
  continueCurrent() { if (this.status !== "paused") return; this.setStatus("playing"); this.timeline?.play(); }
  nextStep() { if (this.status !== "step_complete" || this.isFinalStep()) return; this.index += 1; this.reconstruct("ready", "paused"); }
  previousStep() { if (this.index === 0) return; this.index -= 1; this.reconstruct("result", "step_complete"); }
  replayStep() { if (this.reducedMotion) this.reconstruct("result", this.isFinalStep() ? "example_complete" : "step_complete"); else { this.reconstruct("operation", "playing", false); this.timeline?.setSpeed(this.playbackSpeed); this.timeline?.play(); } }
  restartExample() { this.index = 0; this.reconstruct("ready", "idle"); this.mount.querySelector(".stateful-whiteboard header")?.focus(); }
  completeCurrentStep() { if (!this.destroyed) this.reconstruct("result", this.isFinalStep() ? "example_complete" : "step_complete"); }
  isFinalStep() { return this.index === this.block.steps.length - 1; }
  stopTimeline() { this.transitionToken += 1; this.timeline?.destroy(); this.timeline = null; }

  reconstruct(phase, status, notify = true) {
    this.stopTimeline(); this.renderPhase = phase;
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
    stage.innerHTML = `${visualization}${renderer.render(step, phase, { history, hasVisualization:Boolean(this.visualSession) })}`;
    stage.setAttribute("aria-label", step.screen_reader_description);
    const targets = [...new Set((step.events || []).flatMap(event => event.targets || []))];
    const missing = targets.filter(id => !stage.querySelector(`[data-object-id="${CSS.escape(id)}"]`));
    if (missing.length) { stage.dataset.missingTargets = missing.join(","); AthenaVisualizationDiagnostics.emit("EVENT_TARGETS_MISSING", { ...this.diagnosticContext, block_id:this.block.id, step_id:step.id || String(step.step_number), targets:missing }); }
    else delete stage.dataset.missingTargets;
    this.renderTeachingNotes(step); this.renderSolutionTrail(); this.renderOpeningCaption(step, phase);
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
  renderSolutionTrail() {
    const trail = this.mount.querySelector('[data-role="solution-trail"]');
    const details = this.mount.querySelector(".whiteboard-solution-trail");
    if (!trail || !details) return;
    const completed = this.block.steps.slice(0, this.index).map(step => step.after_expression);
    trail.innerHTML = completed.map(value => `<li>${escapeWhiteboardHtml(value)}</li>`).join("");
    details.hidden = completed.length === 0;
  }
  setStatus(status, notify = true) {
    this.status = status; this.mount.querySelector(".stateful-whiteboard").dataset.controllerState = status;
    const labels = { idle:"Start lesson", playing:"Pause", paused:"Continue", step_complete:"Continue", example_complete:"Replay lesson" };
    const primary = this.mount.querySelector('[data-action="primary"]'); primary.textContent = labels[status]; primary.setAttribute("aria-label", labels[status]);
    this.mount.querySelector('[data-action="previous"]').disabled = this.index === 0;
    this.mount.querySelector('[data-action="next"]').disabled = status !== "step_complete" || this.isFinalStep();
    const replay = this.mount.querySelector('[data-action="replay"]'); replay.disabled = status === "playing"; replay.hidden = status === "example_complete";
    this.mount.querySelector('[data-role="position"]').textContent = `Step ${this.index + 1} of ${this.block.steps.length}`;
    if (notify) this.onStateChange(this.index, status);
  }
  destroy() { if (this.destroyed) return; this.destroyed = true; this.listeners?.abort(); this.stopTimeline(); this.visualSession?.destroy(); if (this.visibilityHandler) document.removeEventListener("visibilitychange", this.visibilityHandler); this.mount.replaceChildren(); }
  showCheckpoint(event, controller) {
    this.setStatus("paused"); const panel = this.mount.querySelector('[data-role="checkpoint"]'); panel.hidden = false;
    panel.innerHTML = `<strong>Think first</strong><p>${escapeWhiteboardHtml(event.text)}</p><button type="button" class="btn btn-primary">Continue</button>`;
    panel.querySelector("button").onclick = () => { panel.hidden = true; this.setStatus("playing"); controller.play(); }; panel.querySelector("button").focus();
  }
}
