/* Grade 8 rule investigations: rows, input/output gaps, signed cells and square arrays. */
(() => {
  const esc=v=>escapeWhiteboardHtml(String(v??''));
  const families=['rule_difference','rule_zero','rule_signed','rule_nonlinear','rule_context','rule_choice'];
  const title={rule_difference:'Compare changes in both columns',rule_zero:'Find the input-zero row',
    rule_signed:'Keep signed inputs and outputs',rule_nonlinear:'Square arrays and changing gaps',
    rule_context:'Read the fixed charge and repeated charge',rule_choice:'Test more than one possible rule'};
  function grid(rows,phase,stage,resolved,revealSteps){
    // A new step begins in "ready". Keep everything proved by prior steps;
    // only the current step's result waits for its result phase.
    const completed=phase==='result'?stage:stage-1;
    const firstKnownGap=rows.findIndex((row,i)=>i<rows.length-1&&row[1]!==null&&rows[i+1][1]!==null);
    return `<div class="rules-table" role="table" aria-label="Input and output table"><div role="row" class="rules-row rules-header"><span role="columnheader">Input x</span><span role="columnheader">Output y</span><span role="columnheader">Change to next row</span></div>${rows.map(([x,y],i)=>{
      const value=y!==null?y:(revealSteps[i]>0&&completed>=revealSteps[i]?resolved[i]:null);
      const next=rows[i+1],nextValue=next&&(next[1]!==null?next[1]:(revealSteps[i+1]>0&&completed>=revealSteps[i+1]?resolved[i+1]:null));
      const delta=!next?'—':value===null||nextValue===null?'Find the missing output':`Δx ${next[0]-x}, Δy ${nextValue-value}`;
      // In the first operation, point to one given gap. Complete the
      // comparison at its result; subsequent steps preserve those gaps.
      const showDelta=completed>=1||(phase==='operation'&&stage===1&&i===firstKnownGap);
      return `<div role="row" class="rules-row" data-row="${i+1}"><span role="cell" data-object-id="input-${i+1}">${esc(x)}</span><span role="cell" data-object-id="output-${i+1}">${value===null?'?':esc(value)}</span><span role="cell" data-object-id="delta-${i+1}" class="rules-delta ${showDelta?'':'is-concealed'}">${showDelta?esc(delta):''}</span></div>`;
    }).join('')}</div>`;
  }
  function motif(family,rows){
    if(family==='rule_nonlinear'){
      const samples=rows.filter(([x,y])=>x>=0&&x<=4&&y!==null).slice(0,4);
      return `<div class="rules-squares" role="group" aria-label="Square arrays for given input values">${samples.map(([x])=>`<div><small>Input ${esc(x)}: ${esc(x)} × ${esc(x)} array</small><span class="rules-square" style="--cols:${Math.max(1,x)}">${Array.from({length:x*x},()=>'<i aria-hidden="true"></i>').join('')||'<em>empty</em>'}</span></div>`).join('')}</div>`;
    }
    if(family==='rule_signed')return `<div class="rules-signs" role="group" aria-label="Signed input positions">${rows.map(([x])=>`<span class="${x<0?'is-negative':''}">${esc(x)}</span>`).join('')}</div>`;
    if(family==='rule_zero')return `<p class="rules-anchor">${rows.some(([x,y])=>x===0&&y===null)?'Input zero: output to find':rows.some(([x,y])=>x===0)?'Input zero: given row highlighted':'Step backward to input zero'}</p>`;
    if(family==='rule_context')return `<p class="rules-anchor">Input counts and matching costs retain their stated units.</p>`;
    if(family==='rule_choice')return `<p class="rules-anchor">A short table may fit more than one candidate rule.</p>`;
    return `<p class="rules-anchor">Each output gap must be compared with its input gap.</p>`;
  }
  for(const family of families)AthenaVisualizationRegistry.register('algebra',family,{
    render(p,state,phase){
      const stage=Number(((state.annotations||[]).find(v=>v.startsWith('stage:'))||'stage:0').slice(6));
      const rows=(p.input_values||[]).map((x,i)=>[x,(p.output_values||[])[i]==='?'?null:(p.output_values||[])[i]]);
      const resolved=p.resolved_outputs||rows.map(row=>row[1]);
      const revealSteps=p.output_reveal_steps||rows.map(()=>null);
      const givens=p.given_objects||[],derived=p.derived_objects||[],total=Number(p.total_steps);
      const final=phase==='result'&&stage>=total;
      const givenObjects=givens.map((v,i)=>`<span class="rules-given" data-object-id="given-${i+1}">${esc(v)}</span>`).join('');
      const outputObjects=derived.map((v,i)=>{
        const revealAt=Math.ceil((i+1)*(total-1)/derived.length);
        const shown=stage>revealAt||(stage===revealAt&&phase==='result');
        return `<span class="rules-derived ${shown?'':'is-concealed'}" data-object-id="derived-${i+1}">${shown?esc(v):'?'}</span>`;
      }).join('');
      return `<section class="rules-board" data-managed-visibility="true" data-question-id="${esc(p.question_id)}" data-phase="${esc(phase)}" data-family="${esc(family)}"><p class="g8-original"><strong>Original question</strong><span data-object-id="problem">${esc(p.prompt)}</span></p><div class="rules-scene" data-object-id="model"><strong>${esc(title[family])}</strong>${grid(rows,phase,stage,resolved,revealSteps)}${motif(family,rows)}<div class="rules-givens">${givenObjects}</div><div class="rules-results">${outputObjects}</div></div><div class="g8-mathematical-transition"><div class="g8-state g8-state--before">${esc(state.before_state)}</div><div class="g8-action-slot"><div data-object-id="operation" class="g8-timeline-object g8-operation ${phase==='ready'?'is-hidden':'is-visible'}"><span>Action on this table</span><strong>${phase==='ready'?'':esc(state.working_state)}</strong></div><div data-object-id="result" class="g8-timeline-object g8-result ${phase==='result'&&!final?'is-visible':'is-hidden'}"><span>Result of this action</span><strong>${phase==='result'?esc(state.after_state):''}</strong></div><div data-object-id="verification" class="g8-timeline-object g8-verification ${final?'is-visible':'is-hidden'}"><span>Verify the given rows</span><strong>${final?esc(state.after_state):''}</strong></div></div></div></section>`;
    },destroy(){}
  });
})();
