/* Grade 9 Topic 2: signed arithmetic scenes use the current question's values. */
(() => {
  const esc=value=>escapeWhiteboardHtml(String(value??''));
  const stage=(state,phase)=>{
    const marker=(state.annotations||[]).find(s=>/^stage:\d+$/.test(s));
    const n=Number((marker||'stage:0').slice(6));
    return phase==='result'?n:Math.max(0,n-1);
  };
  const tickLine=(visual,done)=>{
    const values=visual.values||[],path=visual.path||[];
    const shown=path.slice(0,Math.max(1,Math.min(done,path.length)));
    const min=Math.min(0,...values,...shown),max=Math.max(0,...values,...shown);
    const span=Math.max(1,max-min),pad=Math.max(2,Math.ceil(span*.12));
    const lo=min-pad,hi=max+pad,scale=n=>34+(n-lo)/(hi-lo)*492;
    const count=8,ticks=Array.from({length:count+1},(_,i)=>Math.round(lo+(hi-lo)*i/count));
    return `<svg class="g9-integer-line" viewBox="0 0 560 138" role="img" aria-label="Signed number line for ${esc(values.join(', '))}"><title>Signed number line</title><desc>The marked values and completed moves appear in order.</desc><line x1="34" x2="526" y1="76" y2="76" class="axis"/>${[...new Set([...ticks,0,...values])].map(n=>`<g><line x1="${scale(n)}" x2="${scale(n)}" y1="70" y2="82" class="tick"/><text x="${scale(n)}" y="102" text-anchor="middle">${esc(n)}</text></g>`).join('')}${shown.map((n,i)=>`<circle cx="${scale(n)}" cy="76" r="${i===shown.length-1?7:5}" class="${i===shown.length-1?'focused':'previous'}"/>`).join('')}${shown.length>1?`<path d="M${scale(shown[0])} 52 Q${(scale(shown[0])+scale(shown[1]))/2} 12 ${scale(shown[1])} 52" class="move"/>`:''}</svg>`;
  };
  const tiles=(v,done)=>`<div class="g9-integer-tiles" aria-label="Signed operation tiles">${(v.values||[]).map((n,i)=>`<span class="${done>=i+1?'is-active':''}" data-tile="${i}">${n<0?'−':'+'}${esc(Math.abs(n))}</span>`).join('<b aria-hidden="true">→</b>')}<span class="g9-integer-outcome">${done>=3?esc(v.path?.at(-1)):'?'}</span></div><p class="g9-integer-rule">${done>=1?esc(v.operator==='square'?'Repeat the entire signed base':v.operator==='cube'?'Three signed factors':v.operator==='distributive'?'Distribute to both terms':'Keep the sign of each term'):''}</p>`;
  const roots=(v,done)=>`<div class="g9-integer-root" aria-label="Root and power model"><div><small>Given number</small><strong>${esc(v.values?.[0])}</strong></div><div><small>${esc(v.operator==='cube_root'?'Three equal factors':'Two equal factors')}</small><strong>${done>=2?esc(v.values?.[1]):'?'}</strong></div><div><small>Principal result</small><strong>${done>=3?esc(v.path?.at(-1)):'?'}</strong></div></div>`;
  const context=(v,done)=>`<div class="g9-integer-context" aria-label="Signed changes in sequence"><div class="g9-integer-context-row"><span>Start</span><strong>${esc(v.path?.[0])}${esc(v.unit||'')}</strong></div><div class="g9-integer-context-row"><span>First action</span><strong>${done>=2?esc(v.path?.[1])+esc(v.unit||''):'?'}</strong></div><div class="g9-integer-context-row"><span>Second action</span><strong>${done>=3?esc(v.path?.at(-1))+esc(v.unit||''):'?'}</strong></div></div>`;
  const diagnosis=(v,done)=>`<div class="g9-integer-diagnosis" aria-label="Find the learner's first incorrect operation"><p>Claim: ${esc(v.learner_claim)}</p><p class="${done>=2?'is-marked':''}">${done>=2?'First incorrect operation: '+esc(v.operator):'Inspect the sign and the operation before the equals sign.'}</p><p>${done>=3?'Corrected result: '+esc(v.path?.at(-1)):'Corrected result: ?'}</p></div>`;
  const draw={line:tickLine,tiles,root:roots,context,diagnosis};
  for(let number=1;number<=5;number++)AthenaVisualizationRegistry.register('algebra',`grade9_integer_${number}`,{
    render(params,state,phase){
      const scene=JSON.parse(params.scene_json),done=stage(state,phase),count=Number(params.total_steps);
      const model=scene.visual?.family==='givens'?`<p>Mark the given values before calculating.</p>`:
        draw[scene.visual?.family]?.(scene.visual,done)||'';
      return `<section class="g9-integer-board" data-managed-visibility="true" data-question-id="${esc(params.question_id)}" data-phase="${esc(phase)}"><p class="g9-integer-question" data-object-id="problem">${esc(params.prompt)}</p><div class="g9-integer-givens">${(scene.givens||[]).map((g,i)=>`<span data-given="${i}">${esc(g)}</span>`).join('')}</div><div class="g9-integer-model" data-object-id="model">${model}</div><p data-object-id="selection" class="g9-integer-answer">${scene.answer&&done>=count-1?'Result: '+esc(scene.answer):''}</p><div class="g9-integer-action"><div data-object-id="operation">${phase==='operation'?esc(state.working_state):''}</div><div data-object-id="result">${phase==='result'&&done<count?esc(state.after_state):''}</div><div data-object-id="verification">${phase==='result'&&done===count?esc(state.after_state):''}</div></div></section>`;
    },destroy(){}
  });
})();
