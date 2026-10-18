function sequenceTimelineMarkup(parameters, state, phase) {
  const terms = parameters.terms || [];
  const positions = parameters.positions || terms.map((_, index) => index + 1);
  const differences = parameters.differences || terms.slice(1).map((value, index) => value - terms[index]);
  const ratios = parameters.ratios || [];
  const second = parameters.second_differences || differences.slice(1).map((value, index) => value - differences[index]);
  const width = 620;
  const start = 80;
  const gap = terms.length > 1 ? Math.min(135, 470 / (terms.length - 1)) : 100;
  const row = (values, y, prefix, label, offset = 0) => `<g class="sequence-row sequence-row--${prefix}"><text x="15" y="${y}" class="sequence-row__label">${escapeWhiteboardHtml(label)}</text>${values.map((value,index) => {
    const x=start+(index+offset)*gap;
    return `<g data-object-id="${prefix}-${index+1}" data-x="${x}" data-y="${y}" class="semantic-object is-hidden"><text x="${x}" y="${y}" text-anchor="middle">${escapeWhiteboardHtml(value)}</text></g>`;
  }).join("")}</g>`;
  return `<div class="sequence-visual ${phase}">
    <svg viewBox="0 0 ${width} 330" role="img" aria-labelledby="sequence-title sequence-description">
      <title id="sequence-title">${escapeWhiteboardHtml(parameters.title || "Sequence analysis")}</title>
      <desc id="sequence-description">Positions and terms are aligned. Difference rows are revealed as the timeline explains the pattern.</desc>
      <g class="whiteboard-background"><line x1="10" y1="105" x2="610" y2="105"/></g>
      <g class="mathematical-object-layer">
        ${row(positions,65,"position","n")}${row(terms,115,"term","Tₙ")}
        ${row(ratios.length ? ratios.map(value=>`×${value}`) : differences.map(value => `${value >= 0 ? "+" : ""}${value}`),205,"difference",ratios.length?"Ratio":"ΔT",.5)}
        ${second.length ? row(second.map(value => `${value >= 0 ? "+" : ""}${value}`),285,"second-difference","Δ²T",1) : ""}
        <g data-object-id="goal" class="semantic-object is-hidden"><text x="310" y="25" text-anchor="middle">${escapeWhiteboardHtml(parameters.mode === "nth_term" ? "Explain the n−1 jumps" : "Classify the sequence")}</text></g>
        <g data-object-id="classification" class="semantic-object is-hidden"><text x="500" y="315" text-anchor="end">Pattern identified</text></g>
        <g data-object-id="verification" class="semantic-object is-hidden"><text x="595" y="25" text-anchor="end">✓ Verified</text></g>
        <g data-object-id="predicted-change" class="semantic-object is-hidden"><text x="520" y="205" text-anchor="middle">${escapeWhiteboardHtml(parameters.next_change || "?")}</text></g>
        <g data-object-id="next-term" class="semantic-object is-hidden"><text x="590" y="115" text-anchor="middle">${escapeWhiteboardHtml(parameters.next_term || "?")}</text></g>
      </g>
      <g class="instruction-layer" data-role="instruction-layer"></g>
      <g class="interaction-layer" data-role="interaction-layer"></g>
    </svg>
  </div>`;
}

AthenaVisualizationRegistry.register("sequences", "sequence_timeline", {
  render(parameters, state, phase) { return sequenceTimelineMarkup(parameters, state, phase); },
  destroy() {}
});

(function(){
  const esc=value=>escapeWhiteboardHtml(value);
  const fmt=value=>Number.isInteger(value)?String(value):Number(value).toFixed(3).replace(/0+$/,"").replace(/\.$/,"");
  const stage=(state,phase)=>{const annotation=(state.annotations||[]).find(value=>String(value).startsWith("visual-stage:"));const declared=annotation?Number(annotation.split(":")[1]):0;return phase==="result"?declared+1:declared;};
  function rows(parameters,includeDifferences,includeSums){
    const count=parameters.terms.length,gap=Math.min(82,440/Math.max(1,count-1)),start=70;
    const cells=(values,y,label)=>`<g><text x="18" y="${y}">${esc(label)}</text>${values.map((value,index)=>`<g><rect x="${start+index*gap-25}" y="${y-24}" width="50" height="32" fill="#f8fbff" stroke="#2457d6"/><text x="${start+index*gap}" y="${y-3}" text-anchor="middle">${esc(fmt(value))}</text></g>`).join("")}</g>`;
    return cells(parameters.positions,55,"n")+cells(parameters.terms,110,"Tₙ")+(includeDifferences&&parameters.differences?.length?cells(parameters.differences,170,"ΔT"):"")+(includeDifferences&&parameters.second_differences?.length?cells(parameters.second_differences,225,"Δ²T"):"")+(includeSums&&parameters.partial_sums?.length?cells(parameters.partial_sums,180,"Sₙ"):"");
  }
  function visual(template,parameters,state,phase){
    const current=stage(state,phase),ids=parameters.objects;
    let body="";
    if(template==="term_rows")body=rows(parameters,current>=2,false);
    if(template==="difference_table")body=rows(parameters,current>=1,false);
    if(template==="sigma_expansion")body=`<text x="25" y="65">Σ</text>${parameters.terms.map((term,index)=>`<g><rect x="${75+index*62}" y="40" width="48" height="38" fill="#f8fbff" stroke="#2457d6"/><text x="${99+index*62}" y="65" text-anchor="middle">${esc(fmt(term))}</text>${index<parameters.terms.length-1?`<text x="${132+index*62}" y="65">+</text>`:""}</g>`).join("")}${current>=2?`<text x="280" y="125" text-anchor="middle">= ${esc(parameters.answer)}</text>`:""}`;
    if(template==="partial_sum")body=rows(parameters,false,current>=1);
    if(template==="convergence_diagram")body=parameters.terms.map((term,index)=>{const height=Math.min(95,Math.abs(term)/Math.max(...parameters.terms.map(Math.abs),1)*95);return `<g><rect x="${55+index*72}" y="${145-height}" width="34" height="${height}" fill="#2457d6"/><text x="${72+index*72}" y="170" text-anchor="middle">${esc(fmt(term))}</text></g>`;}).join("")+(current>=2?`<path d="M40 190 H520"/><text x="280" y="215" text-anchor="middle">${esc(parameters.answer)}</text>`:"");
    if(template==="formula_decision")body=`<g class="decision-tree"><rect x="30" y="30" width="150" height="48" fill="#f8fbff" stroke="#2457d6"/><text x="105" y="59" text-anchor="middle">term or total?</text><path d="M180 54 H235"/><rect x="235" y="30" width="150" height="48" fill="#f8fbff" stroke="#2457d6"/><text x="310" y="59" text-anchor="middle">add or multiply?</text>${current>=1?`<path d="M310 78 V115"/><rect x="130" y="115" width="360" height="55" fill="#f8fbff" stroke="#2457d6"/><text x="310" y="139" text-anchor="middle">${esc(parameters.method.slice(0,58))}</text><text x="310" y="158" text-anchor="middle">${esc(parameters.method.slice(58,116))}</text>`:""}${current>=2?`<text x="310" y="210" text-anchor="middle">Answer: ${esc(parameters.answer)}</text>`:""}</g>`;
    if(template==="error_diagnosis")body=`<g><rect x="30" y="28" width="500" height="62" fill="#fff7ed" stroke="#c2410c"/><text x="45" y="53">Claim under test</text><text x="45" y="76">${esc(parameters.title.slice(0,72))}</text>${current>=1?`<path d="M280 94 V125"/><rect x="30" y="125" width="500" height="55" fill="#f0fdf4" stroke="#15803d"/><text x="45" y="148">First repair: ${esc(parameters.working_lines.at(-1).slice(0,65))}</text>`:""}${current>=2?`<text x="280" y="215" text-anchor="middle">${esc(parameters.answer)}</text>`:""}</g>`;
    const svg=`<svg viewBox="0 0 560 245" role="img"><title>${esc(parameters.title)}</title><desc>${esc(parameters.method)} The question-specific values are ${parameters.terms.map(fmt).join(", ")}.</desc>${body}</svg>`;
    const working=parameters.working_lines[Math.min(Math.max(0,current-1),parameters.working_lines.length-1)];
    return `<figure class="sequence-native ${phase}" data-template="${template}" data-managed-visibility="true"><div data-object-id="${ids[0]}" class="semantic-object is-visible">${svg}</div><span data-object-id="${ids[1]}" class="semantic-object ${current?"is-visible":"is-hidden"}">=</span><p data-object-id="${ids[2]}" class="semantic-object ${current?"is-visible":"is-hidden"}">${esc(parameters.method)}</p><p data-object-id="${ids[3]}" class="semantic-object ${current>=1?"is-visible":"is-hidden"}">${esc(working)}</p><p data-object-id="${ids[4]}" class="semantic-object ${phase==="result"?"is-visible":"is-hidden"}">${esc(parameters.answer)}</p><p data-object-id="${ids[5]}" class="semantic-object ${phase==="result"?"is-visible":"is-hidden"}">Verified against the original information.</p></figure>`;
  }
  ["term_rows","difference_table","sigma_expansion","partial_sum","convergence_diagram","formula_decision","error_diagnosis"].forEach(template=>AthenaVisualizationRegistry.register("sequences",template,{render:(parameters,state,phase)=>visual(template,parameters,state,phase)}));
})();
