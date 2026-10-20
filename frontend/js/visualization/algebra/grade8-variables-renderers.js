/* Grade 8 Lesson 6: models selected by each question's approved scenario. */
(function () {
  const esc=value=>escapeWhiteboardHtml(String(value??""));
  const fields=source=>Object.fromEntries(String(source||"").split(";").map(part=>{
    const at=part.indexOf("=");return at<0?["",""]:[part.slice(0,at).trim(),part.slice(at+1).trim()];
  }).filter(([key])=>key));
  const stage=state=>Number(String((state.annotations||[]).find(a=>a.startsWith("stage:"))||"stage:0").split(":")[1]);
  const active=(state,phase,n)=>phase==="result"&&stage(state)>=n;
  const terminal=(p,state,phase)=>active(state,phase,Number(p.total_steps));
  const finalValue=(d,p,state,phase)=>terminal(p,state,phase)?esc(d.solution||d["break even input"]||d["meeting week"]||"revealed above"):"?";
  function side(d,p,state,phase){
    const n=Number(p.question_id.slice(-2)),left=Number(d["left coefficient"]||d["left x tiles"]||([3,5,4,-2,-3,0,0,0,0,6][n-1])),right=Number(d["right coefficient"]||d["right x tiles"]||([1,2,6,1,1,0,0,0,0,2][n-1]));
    const variable=n===2?"y":n===3?"a":n===4?"m":n===5?"p":"x";
    const tiles=(count,prefix)=>Array.from({length:Math.min(8,Math.abs(count)||1)},(_,i)=>`<span class="var-tile ${count<0?"var-tile--negative":""}" data-tile="${prefix}-${i}">${count<0?"−":""}${variable}</span>`).join("");
    const removed=active(state,phase,n===3?3:n===4?3:2),quantity=Number(d["remove x tiles"]||d["right coefficient"]||d["right x tiles"]||(n===10?2:0));
    const leftUnits=d["left constant"]??d["left units"]??(n===10?-4:""),rightUnits=d["right constant"]??d["right units"]??(n===10?12:"");
    return `<div class="var-balance" data-object-id="balance-beam"><div class="var-pan" data-object-id="balance-left-pan"><strong>Left expression</strong><div class="var-tile-row">${tiles(left,"left")}</div><span>${esc(leftUnits)}</span></div>
      <span class="var-equals" aria-label="equals">=</span><div class="var-pan" data-object-id="balance-right-pan"><strong>Right expression</strong><div class="var-tile-row">${tiles(right,"right")}</div><span>${esc(rightUnits)}</span></div>
      <p class="var-model-note" data-object-id="context">${removed?`The same variable group ${quantity?`(${quantity}${variable})`:""} leaves both sides.`:"Keep both original sides balanced."} ${terminal(p,state,phase)?`The original sides agree when the unknown is ${finalValue(d,p,state,phase)}.`:""}</p></div>`;
  }
  function comparison(d,p,state,phase){
    const n=Number(p.question_id.slice(-2)),parts=n===7?3:n===14?4:10;
    const left=d["left expression"]||d["left fraction"]||"-1/2 n + 6",right=d["right expression"]||d["right fraction"]||"1/4 n - 3";
    const selected=active(state,phase,n===14?3:3);
    const row=(label,value,count)=>`<div class="var-comparison-row"><strong>${label}</strong><div class="var-parts" aria-label="${parts} equal sections">${Array.from({length:parts},(_,i)=>`<span class="var-part ${selected&&i<count?"var-part--removed":""}">${i<count?"variable part":"unit"}</span>`).join("")}</div><span>${esc(value)}</span></div>`;
    return `<div class="var-comparison" data-object-id="balance-beam"><p data-object-id="context">${parts} equal sections expose the signed coefficient.</p>${row("Left",left,n===14?2:n===7?2:5)}${row("Right",right,1)}<p data-object-id="balance-left-pan">${selected?"Matching variable sections have been removed from both rows.":"The sections are still intact."}</p><p data-object-id="balance-right-pan">${terminal(p,state,phase)?`Both original expressions now agree at ${finalValue(d,p,state,phase)}.`:"The unknown remains concealed."}</p></div>`;
  }
  function classification(d,p,state,phase){
    const n=Number(p.question_id.slice(-2)),general=n===15,opened=stage(state),done=terminal(p,state,phase);
    if(general){
      return `<div class="var-classification" data-object-id="balance-beam"><p data-object-id="context">${esc(d["general equation"]||"ax + b = cx + d")}</p><div class="var-branches"><div class="var-branch ${active(state,phase,5)?"is-open":""}">a ≠ c ${active(state,phase,5)?"→ one solution":"→ ?"}</div><div class="var-branch ${active(state,phase,6)?"is-open":""}">a = c, b = d ${active(state,phase,6)?"→ identity":"→ ?"}</div><div class="var-branch ${active(state,phase,7)?"is-open":""}">a = c, b ≠ d ${active(state,phase,7)?"→ no solution":"→ ?"}</div></div><p data-object-id="balance-left-pan">Example: ${esc(d["example left"])} = ${esc(d["example right"])}</p><p data-object-id="balance-right-pan">${done?"One-solution branch: x = 8, both sides equal −5.":"Decide the case before solving the example."}</p></div>`;
    }
    const left=d["left expression"]||"variable term + constant",right=d["right expression"]||"variable term + constant";
    const reveal=active(state,phase,2),test=active(state,phase,3);
    return `<div class="var-classification" data-object-id="balance-beam"><div class="var-compare-pair"><span data-object-id="balance-left-pan">${esc(left)}</span><strong>=</strong><span data-object-id="balance-right-pan">${esc(right)}</span></div><p data-object-id="context">${reveal?(n===8?"Matching constants remain after equal variable terms cancel.":"Unequal constants remain after equal variable terms cancel."):"Remove identical variable terms from both complete sides."}</p><div class="var-test-cards">${test?`<span>Test an input: ${esc(state.after_state)}</span>`:"<span>Input cards are covered</span>"}</div><p class="var-classification-result">${done?(n===8?"Identity: infinitely many solutions":"Contradiction: no solution"):"Classification hidden until the argument is complete"}</p></div>`;
  }
  function rate(d,p,state,phase){
    const n=Number(p.question_id.slice(-2)),savings=n===12,aBase=Number(d["plan a base rand"]||d["start a rand"]),bBase=Number(d["plan b base rand"]||d["start b rand"]),aRate=Number(d["plan a rate rand"]||d["weekly a rand"]),bRate=Number(d["plan b rate rand"]||d["weekly b rand"]);
    const meeting=Number(d["break even input"]||d["meeting week"]),xMax=Math.max(12,meeting+2),yMax=Math.max(aBase+aRate*xMax,bBase+bRate*xMax),xy=(x,y)=>`${42+x/xMax*450},${187-y/yMax*140}`;
    const partial=active(state,phase,2),done=terminal(p,state,phase),meetingValue=aBase+aRate*meeting;
    const visibleExtent=done?xMax:meeting*(partial?.7:.35);
    return `<div class="var-rates" data-object-id="balance-beam"><svg viewBox="0 0 550 230" role="img" aria-label="Two ${savings?"savings":"cost"} lines from their actual starting amounts and rates; meeting point ${done?"shown":"hidden"}"><line x1="42" y1="187" x2="510" y2="187" stroke="currentColor"/><line x1="42" y1="16" x2="42" y2="187" stroke="currentColor"/>
      <polyline points="${xy(0,aBase)} ${xy(visibleExtent,aBase+aRate*visibleExtent)}" fill="none" stroke="#197795" stroke-width="3"/><polyline points="${xy(0,bBase)} ${xy(visibleExtent,bBase+bRate*visibleExtent)}" fill="none" stroke="#ad6634" stroke-width="3"/>
      ${done?`<circle cx="${42+meeting/xMax*450}" cy="${187-meetingValue/yMax*140}" r="7" fill="#257956"/><text x="${42+meeting/xMax*450}" y="${179-meetingValue/yMax*140}" text-anchor="middle">${meeting} ${savings?"weeks":"GB"} · R${meetingValue}</text>`:""}<text x="8" y="208">0</text><text x="480" y="208">${savings?"weeks":"GB"}</text></svg>
      <div class="var-rate-legend"><span data-object-id="balance-left-pan">${esc(d["person a"]||"Plan A")}: R${aBase} + R${aRate} per ${savings?"week":"GB"}</span><span data-object-id="balance-right-pan">${esc(d["person b"]||"Plan B")}: R${bBase} + R${bRate} per ${savings?"week":"GB"}</span></div><p data-object-id="context">${partial?"Set the two totals equal at their intersection.":"The meeting input and amount are concealed."}</p></div>`;
  }
  function triangle(d,p,state,phase){
    const done=terminal(p,state,phase),labelA=d["side a"]||"3x + 2 cm",labelB=d["side b"]||"5x − 10 cm";
    return `<div class="var-triangle" data-object-id="balance-beam"><svg viewBox="0 0 420 250" role="img" aria-label="Isosceles triangle with equal side marks and labels ${esc(labelA)} and ${esc(labelB)}"><path d="M210 25 L40 205 L380 205 Z" fill="#f4faff" stroke="#27809c" stroke-width="3"/><path d="M112 116 l12 12 m182 -12 l-12 12" stroke="#27809c" stroke-width="3"/><text x="20" y="95">${esc(labelA)}</text><text x="290" y="95">${esc(labelB)}</text></svg><p data-object-id="context">Matching side marks mean the two expressions are equal.</p><p data-object-id="balance-left-pan">${active(state,phase,2)?"Set the two marked side lengths equal.":"Side equality is the next step."}</p><p data-object-id="balance-right-pan">${done?"x = 6; each marked side is 20 cm.":"The numeric length is still hidden."}</p></div>`;
  }
  const models={variables_both_sides_native:side,expression_comparison:comparison,identity_contradiction:classification,dual_rate_timeline:rate,equal_sides_triangle:triangle};
  for(const [template,model] of Object.entries(models)) AthenaVisualizationRegistry.register("algebra",template,{
    render(p,state,phase){
      const d=fields(p.source_data),n=stage(state),done=terminal(p,state,phase),operating=phase==="operation"||phase==="result",finished=phase==="result";
      return `<section class="var-visual" data-question-id="${esc(p.question_id)}" data-stage="${n}" data-phase="${esc(phase)}" data-managed-visibility="true"><p class="g8-original"><strong>Original question</strong><span data-object-id="problem">${esc(p.prompt)}</span></p>
        ${model(d,p,state,phase)}<div class="g8-mathematical-transition"><div class="g8-state g8-state--before"><span data-object-id="left-expression">${esc(state.before_state)}</span><span data-object-id="right-expression" hidden></span><span data-object-id="variable-slot" hidden></span></div><div class="g8-action-slot">
        <div data-object-id="operation" class="g8-timeline-object g8-operation ${operating?"is-visible":"is-hidden"}"><span>Current mathematical operation</span><strong>${operating?esc(state.working_state):""}</strong></div>
        <div data-object-id="result" class="g8-timeline-object g8-result ${finished&&!done?"is-visible":"is-hidden"}"><span>Result of this step</span><strong>${finished?esc(state.after_state):""}</strong></div>
        <div data-object-id="verification" class="g8-timeline-object g8-verification ${done?"is-visible":"is-hidden"}"><span>Checked in the original question</span><strong>${done?esc(state.after_state):""}</strong></div>
        <span data-object-id="inverse-operation" hidden></span><span data-object-id="left-operation" hidden></span><span data-object-id="right-operation" hidden></span><span data-object-id="cancellation" hidden></span><span data-object-id="substitution-slot" hidden></span><span data-object-id="conclusion" hidden></span></div></div></section>`;
    },destroy(){},
  });
})();
