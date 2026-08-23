/* ============================================================
   ANIMATION ENGINE (Phase 1 foundation for Phase 3)
   ------------------------------------------------------------
   Implements the architecture from the brief:

     AI Reasoning -> Structured Teaching Plan -> Animation
     Instruction -> Pre-built Animation Template -> Rendered Lesson

   The engine NEVER executes arbitrary code from a lesson or from
   the AI. It only knows how to render a fixed set of named
   templates (TEMPLATES below), driven by a small, declarative
   step list like:

     { op: "subtract_both_sides", value: 5, before: "...", after: "..." }

   This is the same shape the future AI Tutor (Phase 4) will emit
   as its "animation instruction" — see backend/app/services/
   animation_service.py, the backend counterpart that will
   validate/produce these instructions server-side. Today the
   instructions come straight from curriculum-data.js.

   Adding a new visual concept later means adding one new function
   to TEMPLATES — never adding new "if animation type is X" branches
   scattered across pages.
   ============================================================ */

const TEMPLATES = {
  linear_equation_balance(ctx, w, h, step) {
    ctx.clearRect(0, 0, w, h);
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";

    const midY = h * 0.42;
    ctx.strokeStyle = "#94A3B8";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(w * 0.12, midY); ctx.lineTo(w * 0.88, midY); ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(w * 0.5, midY); ctx.lineTo(w * 0.5, midY + 18); ctx.stroke();

    const expr = step.after || step.expression || step.value || "";
    ctx.fillStyle = "#101828";
    ctx.font = "600 34px 'JetBrains Mono', monospace";
    ctx.fillText(expr, w / 2, midY - 40);

    if (step.op && step.op !== "show" && step.op !== "substitute") {
      const opLabel = describeOp(step);
      ctx.fillStyle = "#2456CF";
      ctx.font = "600 16px Inter, sans-serif";
      ctx.fillText(opLabel, w * 0.22, midY + 34);
      ctx.fillText(opLabel, w * 0.78, midY + 34);
      drawArrow(ctx, w * 0.22, midY + 44, w * 0.22, midY + 58);
      drawArrow(ctx, w * 0.78, midY + 44, w * 0.78, midY + 58);
    }

    if (step.before && step.op !== "show") {
      ctx.fillStyle = "#94A3B8";
      ctx.font = "400 15px Inter, sans-serif";
      ctx.fillText(`from  ${step.before}`, w / 2, midY - 74);
    }
  },

  tangent_line(ctx, w, h, step) {
    ctx.clearRect(0, 0, w, h);
    const originX = w * 0.2, originY = h * 0.82;
    const scale = 16;

    ctx.strokeStyle = "#CBD5E1";
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(originX, h * 0.08); ctx.lineTo(originX, originY);
    ctx.moveTo(originX, originY); ctx.lineTo(w * 0.92, originY);
    ctx.stroke();

    ctx.strokeStyle = "#2456CF";
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    for (let px = 0; px <= 5.2; px += 0.05) {
      const x = originX + px * scale;
      const y = originY - (px * px) * (scale / 6);
      if (px === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    ctx.stroke();

    if (step.op === "plot_point" || step.op === "draw_tangent") {
      const px = 2, py = px * px;
      const x = originX + px * scale;
      const y = originY - py * (scale / 6);
      ctx.fillStyle = "#101828";
      ctx.beginPath(); ctx.arc(x, y, 5, 0, Math.PI * 2); ctx.fill();
      ctx.font = "500 13px Inter, sans-serif";
      ctx.fillText("x = 2", x + 10, y - 10);
    }

    if (step.op === "draw_tangent") {
      const px = 2, py = px * px;
      const cx = originX + px * scale;
      const cy = originY - py * (scale / 6);
      const slope = 4;
      ctx.strokeStyle = "#B45309";
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(cx - 60, cy + slope * (60 / scale) * (scale / 6));
      ctx.lineTo(cx + 60, cy - slope * (60 / scale) * (scale / 6));
      ctx.stroke();
      ctx.fillStyle = "#B45309";
      ctx.font = "600 13px Inter, sans-serif";
      ctx.fillText("f'(2) = 4", cx + 55, cy - 30);
    }
  }
};

function describeOp(step) {
  switch (step.op) {
    case "subtract_both_sides": return `− ${step.value}`;
    case "add_both_sides": return `+ ${step.value}`;
    case "multiply_both_sides": return `× ${step.value}`;
    case "divide_both_sides": return `÷ ${step.value}` + (step.flipSign ? "  (sign flips)" : "");
    default: return step.op;
  }
}
function drawArrow(ctx, x1, y1, x2, y2) {
  ctx.strokeStyle = "#2456CF";
  ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(x2, y2); ctx.lineTo(x2 - 4, y2 - 6); ctx.lineTo(x2 + 4, y2 - 6); ctx.closePath();
  ctx.fillStyle = "#2456CF"; ctx.fill();
}

class AnimationEngine {
  constructor(mountEl, animationSpec) {
    this.mountEl = mountEl;
    this.spec = animationSpec;
    this.stepIndex = 0;
    this.speechEnabled = true;
    this.speechSupported = "speechSynthesis" in window && "SpeechSynthesisUtterance" in window;
  }

  mount() {
    const tpl = TEMPLATES[this.spec.template];
    this.mountEl.innerHTML = `
      <div class="whiteboard">
        <canvas width="640" height="280" aria-label="${escapeHtml(this.spec.title || 'Animated worked example')}"></canvas>
        <p class="lesson-narration" style="margin:0;color:var(--color-text-secondary);font-size:var(--fs-sm);text-align:center;min-height:1.4em;">${escapeHtml(this.spec.steps[0].narration || "")}</p>
        <ol class="solution-history" data-role="solution-history" aria-live="polite"></ol>
        <div class="whiteboard__step-nav">
          <button class="icon-btn" data-action="prev" aria-label="Previous step">‹</button>
          <span data-role="step-label">Step 1 of ${this.spec.steps.length}</span>
          <button class="icon-btn" data-action="next" aria-label="Next step">›</button>
        </div>
        <div class="whiteboard__controls">
          <button class="icon-btn" data-action="speak" aria-label="Read this step aloud" title="Read this step aloud">🔊</button>
          <button class="icon-btn" data-action="speech-toggle" aria-label="Turn narration off" aria-pressed="true" title="Turn narration off">Audio on</button>
        </div>
      </div>`;
    this.canvas = this.mountEl.querySelector("canvas");
    this.ctx = this.canvas.getContext("2d");
    this.templateFn = tpl || TEMPLATES.linear_equation_balance;

    this.mountEl.querySelector('[data-action="prev"]').onclick = () => this.goTo(this.stepIndex - 1);
    this.mountEl.querySelector('[data-action="next"]').onclick = () => this.goTo(this.stepIndex + 1);
    const speakButton = this.mountEl.querySelector('[data-action="speak"]');
    const speechToggle = this.mountEl.querySelector('[data-action="speech-toggle"]');
    if (!this.speechSupported) {
      speakButton.disabled = true;
      speechToggle.disabled = true;
      speakButton.title = "Audio narration is not supported by this browser";
      speechToggle.textContent = "Audio unavailable";
    } else {
      speakButton.onclick = () => this.speakCurrentStep(true);
      speechToggle.onclick = () => this.toggleSpeech();
    }
    this.render();
    return this;
  }

  render() {
    const step = this.spec.steps[this.stepIndex];
    this.templateFn(this.ctx, this.canvas.width, this.canvas.height, step);
    const narrationEl = this.mountEl.querySelector(".lesson-narration");
    if (narrationEl) narrationEl.textContent = step.narration || "";
    const historyEl = this.mountEl.querySelector('[data-role="solution-history"]');
    if (historyEl) {
      historyEl.innerHTML = this.spec.steps.slice(0, this.stepIndex + 1).map((revealed, index) => {
        const work = revealed.after || revealed.expression || revealed.value || "";
        const explanation = revealed.explanation || revealed.narration || "";
        return `<li><strong>Step ${index + 1}: ${escapeHtml(work)}</strong><p>${escapeHtml(explanation)}</p></li>`;
      }).join("");
    }
    const label = this.mountEl.querySelector('[data-role="step-label"]');
    if (label) label.textContent = `Step ${this.stepIndex + 1} of ${this.spec.steps.length}`;
    this.mountEl.querySelector('[data-action="prev"]').disabled = this.stepIndex === 0;
    this.mountEl.querySelector('[data-action="next"]').disabled = this.stepIndex === this.spec.steps.length - 1;
  }

  goTo(i) {
    if (i < 0 || i >= this.spec.steps.length) return;
    this.stepIndex = i;
    this.render();
    this.speakCurrentStep();
  }
  toggleSpeech() {
    if (!this.speechSupported) return;
    this.speechEnabled = !this.speechEnabled;
    const button = this.mountEl.querySelector('[data-action="speech-toggle"]');
    button.textContent = this.speechEnabled ? "Audio on" : "Audio off";
    button.setAttribute("aria-pressed", String(this.speechEnabled));
    button.setAttribute("aria-label", this.speechEnabled ? "Turn narration off" : "Turn narration on");
    button.title = button.getAttribute("aria-label");
    if (!this.speechEnabled) window.speechSynthesis.cancel();
    else this.speakCurrentStep(true);
  }

  speakCurrentStep(force = false) {
    if (!this.speechSupported || (!this.speechEnabled && !force)) return;
    const step = this.spec.steps[this.stepIndex];
    const work = step.after || step.expression || step.value || "";
    const explanation = step.explanation || step.narration || "";
    const utterance = new SpeechSynthesisUtterance(
      `Step ${this.stepIndex + 1}. ${mathForSpeech(work)}. ${explanation}`
    );
    utterance.lang = "en-ZA";
    utterance.rate = 0.9;
    const voices = window.speechSynthesis.getVoices();
    utterance.voice = voices.find(voice => voice.lang.toLowerCase() === "en-za")
      || voices.find(voice => voice.lang.toLowerCase().startsWith("en"))
      || null;
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utterance);
  }
}

function mathForSpeech(value) {
  return String(value)
    .replace(/f′/g, "f prime")
    .replace(/f″/g, "f double prime")
    .replace(/dy\/dx/g, "d y by d x")
    .replace(/d\/dx/g, "the derivative of")
    .replace(/lim\s*h→0/gi, "the limit as h approaches zero of")
    .replace(/→/g, " approaches ")
    .replace(/⇒/g, " therefore ")
    .replace(/≈/g, " approximately equals ")
    .replace(/≠/g, " is not equal to ")
    .replace(/=/g, " equals ")
    .replace(/−/g, " minus ")
    .replace(/\+/g, " plus ")
    .replace(/÷/g, " divided by ")
    .replace(/×/g, " times ")
    .replace(/²/g, " squared ")
    .replace(/³/g, " cubed ")
    .replace(/⁴/g, " to the power four ")
    .replace(/⁵/g, " to the power five ")
    .replace(/\//g, " over ")
    .replace(/\s+/g, " ")
    .trim();
}

function escapeHtml(str) {
  return String(str).replace(/[&<>"']/g, s => ({ "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;" }[s]));
}
