class WorkedSolution {
  constructor(mount, { steps = [], whyExplanations = [], answer = "" } = {}) {
    this.mount = mount; this.steps = steps; this.whyExplanations = whyExplanations; this.answer = answer;
  }
  mountSolution() {
    this.mount.innerHTML = `<div class="worked-solution">
      <button type="button" class="btn btn-ghost worked-solution__toggle" aria-expanded="false">Show Worked Solution ▼</button>
      <section class="solution-paper" aria-label="Worked solution" hidden><h4>Worked Solution</h4>
        <ol>${this.steps.map((step, index) => `<li><span class="math-step">${escapeWhiteboardHtml(step)}</span>${this.whyExplanations[index] ? `<button type="button" class="why-toggle" data-why="${index}" aria-expanded="false">Why?</button><p data-why-panel="${index}" hidden>${escapeWhiteboardHtml(this.whyExplanations[index])}</p>` : ""}</li>`).join("")}</ol>
        ${this.steps.length ? "" : `<p>${escapeWhiteboardHtml(this.answer)}</p>`}</section></div>`;
    const toggle = this.mount.querySelector(".worked-solution__toggle");
    const panel = this.mount.querySelector(".solution-paper");
    toggle.onclick = () => { panel.hidden = !panel.hidden; toggle.setAttribute("aria-expanded", String(!panel.hidden)); toggle.textContent = panel.hidden ? "Show Worked Solution ▼" : "Hide Worked Solution ▲"; };
    this.mount.querySelectorAll("[data-why]").forEach(button => button.onclick = () => { const why = this.mount.querySelector(`[data-why-panel="${button.dataset.why}"]`); why.hidden = !why.hidden; button.setAttribute("aria-expanded", String(!why.hidden)); });
    return this;
  }
}
