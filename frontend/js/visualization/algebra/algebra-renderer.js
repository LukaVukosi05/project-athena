function algebraToken(id,value,state){const active=(state.highlights||[]).includes(id);return `<span class="algebra-token${active?' is-highlighted':''}" data-object-id="${id}">${escapeWhiteboardHtml(value)}</span>`;}
function algebraNumberLine(parameters){const values=(parameters.values||[]).slice(0,2).sort((a,b)=>a-b);if(values.length<2)return "";const [a,b]=values,x=v=>70+(v-a)/(b-a||1)*280,closed=String(parameters.answer).includes("<=")||String(parameters.answer).includes(">=");return `<svg class="algebra-number-line" viewBox="0 0 420 100" role="img" aria-label="Solution number line"><title>Quadratic inequality solution</title><desc>Critical values ${a} and ${b}. ${escapeWhiteboardHtml(parameters.answer)}</desc><line x1="35" y1="50" x2="385" y2="50"/><circle cx="${x(a)}" cy="50" r="8" class="${closed?'closed':'open'} endpoint"/><circle cx="${x(b)}" cy="50" r="8" class="${closed?'closed':'open'} endpoint"/><text x="${x(a)-8}" y="82">${a}</text><text x="${x(b)-8}" y="82">${b}</text><path class="interval-mark" d="M35 50 H${x(a)-10} M${x(b)+10} 50 H385"/></svg>`;}
function renderAlgebra(parameters,state,phase){
  if((state.annotations||[]).includes("semantic-equation"))return "";
  const mode=parameters.mode;
  const stage=Number((state.annotations||[]).find(item=>String(item).startsWith("stage:"))?.split(":")[1]??6);
  const formula=mode==="quadratic_formula"?`${algebraToken('negative-b','−b',state)} ${algebraToken('plus-minus','±',state)} ${algebraToken('radical','√(b²−4ac)',state)} ${algebraToken('denominator','/ 2a',state)}`:algebraToken('method',parameters.method,state);
  const restriction=stage>=1&&["surd","rational_restrictions"].includes(mode)?`<div class="algebra-restriction" data-object-id="restriction">Restriction / validity condition retained before transforming</div>`:"";
  const method=stage>=2?`<div class="algebra-formula" aria-label="Selected algebra method">${formula}</div>`:"";
  const branches=stage>=3&&["zero_product","quadratic_form","nonlinear_simultaneous"].includes(mode)?`<div class="algebra-branches" aria-label="Solution branches"><span data-object-id="branch-a">Branch A</span><span data-object-id="branch-b">Branch B</span></div>`:"";
  const line=stage>=3&&mode==="inequality"?algebraNumberLine(parameters):"";
  const accessible="The diagram supports the current mathematical operation; the worked state is rendered by the whiteboard timeline.";
  return `<section class="algebra-visual ${phase}" data-mode="${escapeWhiteboardHtml(mode)}" aria-label="Algebra reasoning visual"><h4>${escapeWhiteboardHtml(stage===0?"Orient":mode.replaceAll('_',' '))}</h4>${restriction}${method}${branches}${line}<p class="sr-only">${escapeWhiteboardHtml(parameters.prompt)}. ${accessible}</p></section>`;
}
AthenaVisualizationRegistry.register("algebra","algebra_reasoning",{render:renderAlgebra,destroy(){}});
