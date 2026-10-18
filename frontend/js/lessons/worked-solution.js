class WorkedSolution {
  constructor(mount, { steps = [], whyExplanations = [], answer = "" } = {}) { this.mount=mount;this.steps=steps;this.whyExplanations=whyExplanations;this.answer=answer; }
  mountSolution() {
    const items=this.steps.map((step,index)=>{const structured=typeof step==="object";const expression=structured?step.expression:step;const explanation=structured?step.explanation:"";const why=structured?step.why:this.whyExplanations[index];const verification=structured?step.verification:"";return `<li><div class="math-step">${escapeWhiteboardHtml(expression)}</div>${explanation?`<p>${escapeWhiteboardHtml(explanation)}</p>`:""}${why?`<button type="button" class="why-toggle" data-why="${index}" aria-expanded="false" aria-controls="why-${index}">Why?</button><p id="why-${index}" data-why-panel="${index}" hidden>${escapeWhiteboardHtml(why)}</p>`:""}${verification?`<p class="solution-verification"><strong>Verify against the original:</strong> ${escapeWhiteboardHtml(verification)}</p>`:""}</li>`;}).join("");
    this.mount.innerHTML=`<div class="worked-solution"><button type="button" class="btn btn-ghost worked-solution__toggle" aria-expanded="false">Show Worked Solution ▼</button><section class="solution-paper" aria-label="Worked solution" hidden><h4>Worked Solution</h4><ol>${items}</ol>${this.steps.length?"":`<p>${escapeWhiteboardHtml(this.answer)}</p>`}</section></div>`;
    const toggle=this.mount.querySelector(".worked-solution__toggle"),panel=this.mount.querySelector(".solution-paper");
    toggle.onclick=()=>{panel.hidden=!panel.hidden;toggle.setAttribute("aria-expanded",String(!panel.hidden));toggle.textContent=panel.hidden?"Show Worked Solution ▼":"Hide Worked Solution ▲";};
    this.mount.querySelectorAll("[data-why]").forEach(button=>button.onclick=()=>{const why=this.mount.querySelector(`[data-why-panel="${button.dataset.why}"]`);why.hidden=!why.hidden;button.setAttribute("aria-expanded",String(!why.hidden));});return this;
  }
}
