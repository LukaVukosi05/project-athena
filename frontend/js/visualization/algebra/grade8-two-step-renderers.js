/* Native Grade 8 Lesson 5 diagrams. The current question supplies every value. */
(function () {
  const esc = value => escapeWhiteboardHtml(String(value ?? ""));
  const fields = source => Object.fromEntries(String(source||"").split(";").map(part => {
    const at=part.indexOf("="); return at<0?["",""]:[part.slice(0,at).trim(),part.slice(at+1).trim()];
  }).filter(([key])=>key));
  const step = state => Number(String((state.annotations||[]).find(a=>a.startsWith("stage:"))||"stage:0").split(":")[1]);
  const result = (state,phase,min=4) => phase==="result"&&step(state)>=min;
  const list = source => String(source||"").replace(/^\[|\]$/g,"").split(",").map(value=>value.trim().replace(/^['"]|['"]$/g,"")).filter(Boolean);

  function balance(d,p,state,phase){
    const coefficient=d.coefficient||"?", constant=d.constant||d["left constant"]||"?", given=d["right value"]||"?";
    const count=Math.min(7,Math.max(1,Math.ceil(Math.abs(Number(coefficient)))||2));
    const known=result(state,phase,Number(p.total_steps)-1)?d.solution||"?":"?";
    const outsideRemoved=phase==="result"&&step(state)>=(d["left constant"]?3:2);
    const intermediate=d.intermediate || (Number.isFinite(Number(given)-Number(constant))?String(Number(given)-Number(constant)):"?");
    return `<div class="two-model two-balance" data-object-id="balance-beam"><div class="two-pan" data-object-id="balance-left-pan">
      <small>variable groups · coefficient ${esc(coefficient)}</small><div class="two-tiles">${Array.from({length:count},(_,i)=>`<span class="two-tile" data-group="${i+1}">${esc(known)}</span>`).join("")}</div>
      <span class="two-constant ${outsideRemoved?"is-removed":""}">${Number(constant)<0?"−":"+"} ${esc(String(constant).replace(/^-/,""))}</span></div>
      <strong aria-hidden="true">=</strong><div class="two-pan" data-object-id="balance-right-pan"><small>${outsideRemoved?"after the same inverse on each side":"given value"}</small><strong>${esc(outsideRemoved?intermediate:given)}</strong></div>
      <p class="two-reverse" data-object-id="context">Undo the outside constant, then undo the signed coefficient.</p></div>`;
  }
  function machine(d,p,state,phase){
    const forward=list(d["forward operations"]|| (d["general equation"]?"['multiply by a', 'add b']":"")),
      reverse=list(d["reverse operations"]|| (d["general equation"]?"['subtract b', 'divide by a if a != 0']":""));
    const show=phase!=="initial";
    const first=d["incorrect state"]?2:1, second=d["incorrect state"]?4:3, n=step(state);
    const start=d.input||"x",end=d["general equation"]?"c":d.output||d["example c"]||"c";
    return `<div class="two-model two-machine" data-object-id="balance-beam"><p class="two-machine-row" data-object-id="balance-left-pan"><span class="two-node">${esc(start)} = ${result(state,phase,Number(p.total_steps)-1)?esc(d.solution):"?"}</span>
      ${forward.map((operation,i)=>`<span class="two-arrow">→</span><span class="two-box" data-box="${i+1}">${esc(operation)}</span>`).join("")}
      <span class="two-arrow">→</span><strong class="two-node" data-object-id="balance-right-pan">${esc(end)}</strong></p>
      <p class="two-machine-reverse" data-object-id="context"><strong>Reverse path</strong>${reverse.map((operation,i)=>`<span class="two-box ${show&&n>=(i?second:first)?"is-revealed":"is-pending"}" data-reverse="${i+1}">${show&&n>=(i?second:first)?esc(operation):"inverse step hidden"}</span>`).join("")}</p></div>`;
  }
  function line(d,p,state,phase){
    const start=Number(d.start??d["start temperature c"]),end=Number(d.end??d["end temperature c"]);
    const valid=Number.isFinite(start)&&Number.isFinite(end),low=valid?Math.min(start,end)-3:-10,high=valid?Math.max(start,end)+3:10;
    const x=value=>45+(value-low)/(high-low)*460;
    const jumps=result(state,phase,Number(p.total_steps)-1)?
      (d.term?1:Math.min(12,Math.max(1,Number(d.solution||d["solution hours"])||1))):0;
    const points=Array.from({length:jumps},(_,i)=>start+(end-start)*(i+1)/jumps);
    return `<div class="two-model two-line" data-object-id="balance-beam"><svg viewBox="0 0 560 145" role="img" aria-label="Number line from ${esc(start)} to ${esc(end)}${jumps?` in ${jumps} equal jumps`:"; jumps not revealed"}">
      <line x1="35" y1="91" x2="530" y2="91" stroke="currentColor" stroke-width="2"/>
      ${valid?`<circle cx="${x(start)}" cy="91" r="6" fill="currentColor"/><circle cx="${x(end)}" cy="91" r="6" fill="currentColor"/><text x="${x(start)}" y="119" text-anchor="middle">${start}</text><text x="${x(end)}" y="119" text-anchor="middle">${end}</text>`:""}
      ${points.map((point,i)=>`<path d="M${x(i?points[i-1]:start)} 74 Q${(x(i?points[i-1]:start)+x(point))/2} 22 ${x(point)} 74" fill="none" stroke="currentColor" stroke-width="2"/>`).join("")}</svg>
      <p data-object-id="balance-left-pan">Start ${esc(start)} · end ${esc(end)}</p><p data-object-id="balance-right-pan">${jumps?(d.term?`One directed change ${esc(d.difference||end-start)}; ${esc(d.term)} = ${esc(d.difference||end-start)}`:`${jumps} equal jumps`):"How far and how many jumps?"}</p><span data-object-id="context" hidden></span></div>`;
  }
  function fraction(d,p,state,phase){
    const factor=d.coefficient||(`1/${d.divisor||5}`),parts=factor==="2/3"?3:factor==="0.5"?2:Math.max(2,Math.min(10,Number(d.divisor)||5));
    const known=factor==="2/3"?2:1,whole=result(state,phase,Number(p.total_steps)-1)?d.solution||"?":"?";
    const outsideRemoved=phase==="result"&&step(state)>=2;
    return `<div class="two-model two-fraction" data-object-id="balance-beam"><p data-object-id="context">Variable fraction ${esc(factor)} · <span class="${outsideRemoved?"is-removed":""}">outside constant ${esc(d.constant)}</span></p>
      <div class="two-part-row" data-object-id="balance-left-pan">${Array.from({length:parts},(_,i)=>`<span class="two-part ${i<known?"is-known":""}" data-part="${i+1}">${i<known?"given portion":"?"}</span>`).join("")}</div>
      <p data-object-id="balance-right-pan">${outsideRemoved?`After the first inverse: ${esc(d.intermediate||state.after_state)}`:`Given result: ${esc(d["right value"])}`} · whole: ${esc(whole)}</p></div>`;
  }
  function context(d,p,state,phase){
    const rectangle=d.shape==="rectangle",taxi=d.context==="taxi fare";
    const known=rectangle?`${esc(d["known side cm"])} cm`:taxi?`R${esc(d["fixed fee rand"])}`:"?";
    const total=rectangle?`${esc(d["perimeter cm"])} cm`:taxi?`R${esc(d["total rand"])}`:"?";
    const unknown=result(state,phase,Number(p.total_steps)-1)?(rectangle?`${esc(d["solution cm"])} cm`:`${esc(d["solution km"])} km`):"?";
    return `<div class="two-model two-context" data-object-id="balance-beam"><p data-object-id="context">${rectangle?"Perimeter: two equal lengths and two equal widths":"Taxi fare: fixed amount plus a rate per kilometre"}</p>
      ${rectangle?`<div class="two-rectangle" data-object-id="balance-left-pan"><span>length ${unknown}</span><span>width ${known}</span></div>`:
        `<div class="two-fare" data-object-id="balance-left-pan"><span>Base fare ${known}</span><span>R${esc(d["rate rand per km"])} per km</span><span>distance ${unknown}</span></div>`}
      <strong data-object-id="balance-right-pan">Given total ${total}</strong></div>`;
  }
  const models={two_step_balance_native:balance,operation_machine:machine,two_step_number_line:line,
    two_step_fraction_scale:fraction,two_step_context:context};
  for(const [template,model] of Object.entries(models)) AthenaVisualizationRegistry.register("algebra",template,{
    render(parameters,state,phase){
      const d=fields(parameters.source_data),n=step(state),done=phase==="result"&&n>=Number(parameters.total_steps);
      const operating=phase==="operation"||phase==="result",finished=phase==="result";
      return `<section class="two-visual" data-question-id="${esc(parameters.question_id)}" data-stage="${n}" data-phase="${esc(phase)}" data-managed-visibility="true">
        <p class="g8-original"><strong>Original question</strong><span data-object-id="problem">${esc(parameters.prompt)}</span></p>
        ${model(d,parameters,state,phase)}
        <div class="g8-mathematical-transition"><div class="g8-state g8-state--before"><span data-object-id="left-expression">${esc(state.before_state)}</span><span data-object-id="right-expression" hidden></span><span data-object-id="variable-slot" hidden></span></div>
          <div class="g8-action-slot"><div data-object-id="operation" class="g8-timeline-object g8-operation ${operating?"is-visible":"is-hidden"}"><span>Current inverse operation</span><strong>${operating?esc(state.working_state):""}</strong></div>
          <div data-object-id="result" class="g8-timeline-object g8-result ${finished&&!done?"is-visible":"is-hidden"}"><span>Result of this step</span><strong>${finished?esc(state.after_state):""}</strong></div>
          <div data-object-id="verification" class="g8-timeline-object g8-verification ${done?"is-visible":"is-hidden"}"><span>Checked in the original equation</span><strong>${done?esc(state.after_state):""}</strong></div>
          <span data-object-id="inverse-operation" hidden></span><span data-object-id="left-operation" hidden></span><span data-object-id="right-operation" hidden></span><span data-object-id="cancellation" hidden></span><span data-object-id="substitution-slot" hidden></span><span data-object-id="conclusion" hidden></span>
        </div></div></section>`;
    },destroy(){},
  });
})();
