/* Native Grade 9 exponent visuals: expand the actual base, move the decimal, then check. */
(() => {
  const esc=value=>escapeWhiteboardHtml(String(value??''));
  const visible=(state,phase)=>{
    const marker=(state.annotations||[]).find(x=>/^stage:\d+$/.test(x))||'stage:0';
    const n=Number(marker.slice(6));return phase==='result'?n:Math.max(0,n-1);
  };
  const fraction=(value)=>{
    const parts=String(value).split('/');return parts.length===2?
      `<span class="g9-exp-fraction" role="math" aria-label="${esc(parts[0])} over ${esc(parts[1])}"><span>${esc(parts[0])}</span><span>${esc(parts[1])}</span></span>`:esc(value);
  };
  const factors=(v,done)=>{
    const n=Math.min(12,Math.max(0,v.exponents?.at(-1)||0)),shown=Math.min(n,Math.max(0,done));
    return `<div class="g9-exp-factors" aria-label="Repeated factors of ${esc(v.base)}">${Array.from({length:n},(_,i)=>`<span class="${i<shown?'is-active':''}">${i<shown?esc(v.base):'?'}</span>`).join('<b aria-hidden="true">×</b>')}</div><p>${done>=2?'Now multiply the visible factors.':'The exponent tells us how many factors to reveal.'}</p>`;
  };
  const law=(v,done)=>`<div class="g9-exp-law" aria-label="Exponent law for the current base"><div><small>Base</small><strong>${esc(v.base)}</strong></div>${(v.exponents||[]).map((e,i)=>`<div><small>${i===(v.exponents||[]).length-1&&v.operator!=='product_power'?'Result exponent':`Given exponent ${i+1}`}</small><strong>${i===(v.exponents||[]).length-1&&v.operator!=='product_power'&&done<2?'?':esc(e)}</strong></div>`).join('')}<div><small>Power value</small><strong>${done>=3?esc(v.values?.at(-1)):'?'}</strong></div></div>`;
  const reciprocal=(v,done)=>`<div class="g9-exp-reciprocal" aria-label="Zero or negative exponent"><span>${esc(v.base)}<sup>${esc(v.exponent)}</sup></span><b aria-hidden="true">→</b>${v.operator==='zero'?`<strong>${done>=3?'1':'?'}</strong>`:done>=2?fraction(`1/${v.denominator}`):fraction('1/?')}</div><p>${done>=1?(v.operator==='zero'?'A nonzero base to zero equals one.':'A negative exponent asks for a reciprocal.'):''}</p>`;
  const scale=(v,done)=>`<div class="g9-exp-scale" aria-label="Scientific notation decimal movement"><div><small>Original value</small><strong>${esc(v.raw)}</strong></div><div><small>Coefficient between 1 and 10</small><strong>${done>=1?esc(v.coefficient):'?'}</strong></div><div><small>Decimal places and direction</small><strong>${done>=2?`${Math.abs(v.exponent)} ${v.exponent<0?'toward smaller values':'toward larger values'}`:'?'}</strong></div><div><small>Power of ten</small><strong>${done>=3?`10${String(v.exponent).replace(/[-0-9]/g,c=>({'-':'⁻','0':'⁰','1':'¹','2':'²','3':'³','4':'⁴','5':'⁵','6':'⁶','7':'⁷','8':'⁸','9':'⁹'}[c]))}`:'?'}</strong></div></div>`;
  const compare=(v,done)=>`<div class="g9-exp-compare" aria-label="Compare aligned scientific values"><div><small>A: given coefficient and power</small><strong>${esc(v.a?.[0])} × 10<sup>${esc(v.a?.[1])}</sup></strong><span>${done>=2?esc(v.values?.[0]):'?'}</span></div><div><small>B: given coefficient and power</small><strong>${esc(v.b?.[0])} × 10<sup>${esc(v.b?.[1])}</sup></strong><span>${done>=2?esc(v.values?.[1]):'?'}</span></div></div>`;
  const context=(v,done)=>`<div class="g9-exp-context" aria-label="Measured units and scaled total"><div><small>One unit</small><strong>${esc(v.coefficient)} × 10<sup>${esc(v.exponent)}</sup> ${esc(v.unit)}</strong></div><div><small>Number of units</small><strong>${esc(v.multiplier)}</strong></div><div><small>Total coefficient</small><strong>${done>=2?esc(v.result_coefficient):'?'}</strong></div><div><small>Normalized power</small><strong>${done>=3?`10^${esc(v.result_exponent)}`:'?'}</strong></div></div>`;
  const diagnosis=(v,done)=>`<div class="g9-exp-diagnosis" aria-label="Locate and repair the first exponent error"><p>Claim: ${esc(v.claim)}</p><p class="${done>=2?'is-marked':''}">${done>=2?`First error: ${esc(v.kind)} rule`:'Inspect the base, sign and exponent operation.'}</p><p>Corrected: ${done>=3?fraction(v.correction):'?'}</p></div>`;
  const draw={factors,law,reciprocal,scale,compare,context,diagnosis};
  for(let number=1;number<=6;number++)AthenaVisualizationRegistry.register('algebra',`grade9_exponent_${number}`,{
    render(params,state,phase){
      const scene=JSON.parse(params.scene_json),done=visible(state,phase),count=Number(params.total_steps);
      const model=scene.visual?.family==='givens'?'<p>Read the base and exponent before applying a law.</p>':draw[scene.visual?.family]?.(scene.visual,done)||'';
      return `<section class="g9-exp-board" data-managed-visibility="true" data-question-id="${esc(params.question_id)}" data-phase="${esc(phase)}"><p class="g9-exp-question" data-object-id="problem">${esc(params.prompt)}</p><div class="g9-exp-givens">${(scene.givens||[]).map((x,i)=>`<span data-given="${i}">${esc(x)}</span>`).join('')}</div><div class="g9-exp-model" data-object-id="model">${model}</div><p data-object-id="selection" class="g9-exp-answer">${scene.answer&&done>=count-1?'Result: '+fraction(scene.answer):''}</p><div class="g9-exp-action"><div data-object-id="operation">${phase==='operation'?esc(state.working_state):''}</div><div data-object-id="result">${phase==='result'&&done<count?esc(state.after_state):''}</div><div data-object-id="verification">${phase==='result'&&done===count?esc(state.after_state):''}</div></div></section>`;
    },destroy(){}
  });
})();
