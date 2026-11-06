/* Question-owned Grade 9 expression scenes. Every stage retains the original model. */
(() => {
 const esc=value=>escapeWhiteboardHtml(String(value??''));
 const progress=(state,phase)=>{const mark=(state.annotations||[]).find(x=>/^stage:\d+$/.test(x))||'stage:0';
  const stage=Number(mark.slice(6));return phase==='result'?stage:Math.max(0,stage-1)};
 const fraction=value=>{
  const match=String(value).match(/^([−-]?\d+)\/(\d+)(x?)$/);
  return match?`<span class="g9-ex-fraction" aria-label="${esc(value)}"><span>${esc(match[1])}</span><span>${esc(match[2])}</span></span>${esc(match[3])}`:esc(value);
 };
 const cards=(items,done)=>`<div class="g9-ex-terms" aria-label="Terms from the original expression">${items.map((v,i)=>`<span class="g9-ex-term ${done>=1&&i===0?'is-current':''}" data-term="${i}">${fraction(v)}</span>`).join('')}</div>`;
 const area=(v,done)=>{
  const rows=v.rows||[],columns=v.columns||[];
  if(rows.length!==2||columns.length!==2)return cards(v.givens,done);
  return `<div class="g9-ex-area" role="img" aria-label="Four-cell area model using the current brackets"><div class="g9-ex-corner"></div>${columns.map(c=>`<div class="g9-ex-label">${fraction(c)}</div>`).join('')}${rows.map((r,ri)=>`<div class="g9-ex-label ${done>=1&&ri===0?'is-current':''}">${fraction(r)}</div>${columns.map((c,ci)=>`<div class="g9-ex-cell ${done>=2?'is-filled':''} ${v.family==='diagnosis'&&ri===1&&ci===0&&done>=2?'is-error':''}" data-cell="${ri}-${ci}">${done>=2?`${fraction(r)} × ${fraction(c)}`:'?'}</div>`).join('')}`).join('')}</div>`;
 };
 const factor=(v,done)=>`<div class="g9-ex-factor">${cards(v.givens,done)}<div class="g9-ex-brackets" aria-label="Factor structure">${done<2?'Which terms share a factor?':v.conjugates?`Conjugates: (${esc(v.conjugates[0])}) and (${esc(v.conjugates[1])})`:v.factor?`Shared factor: ${esc(v.factor)}`:'Find two factors whose product and sum match the original.'}</div></div>`;
 const distribute=(v,done)=>`<div class="g9-ex-distribute"><span class="g9-ex-term ${done>=1?'is-current':''}">${esc(v.factor)}</span><span aria-hidden="true">→</span>${v.givens.slice(1).map((term,i)=>`<span class="g9-ex-term ${done>=2?'is-current':''}" data-branch="${i}">${done>=2?`${esc(v.factor)} × ${fraction(term)}`:fraction(term)}</span>`).join('')}</div>`;
 const rational=(v,done)=>`<div class="g9-ex-rational"><div class="g9-ex-quotient"><div>${fraction(v.givens[0])}</div><div>${fraction(v.givens[1])}</div></div><p class="g9-ex-restriction" data-object-id="restriction">${done>=1?`Keep: ${esc(v.restriction)}`:'Find the excluded value before cancelling.'}</p></div>`;
 const model=(v,done)=>v.family==='area'||v.family==='diagnosis'?area(v,done):v.family==='distribution'?distribute(v,done):v.family==='fraction'?rational(v,done):v.family==='difference_squares'||v.family==='trinomial'||v.family==='common_factor'?factor(v,done):cards(v.givens,done);
 for(let n=1;n<=9;n++)AthenaVisualizationRegistry.register('algebra',`grade9_expression_${n}`,{
  render(params,state,phase){const scene=JSON.parse(params.scene_json),v=scene.visual,done=progress(state,phase),total=Number(params.total_steps);
   const given=v.family==='givens';
   return `<section class="g9-ex-board" data-managed-visibility="true" data-question-id="${esc(params.question_id)}" data-phase="${esc(phase)}"><p data-object-id="problem" class="g9-ex-question">${esc(params.prompt)}</p><div data-object-id="model" class="g9-ex-model">${given?'<p>Read the original expression and identify its terms.</p>':model(v,done)}</div>${!given&&v.claim?`<p class="g9-ex-claim">Learner’s claim: ${esc(v.claim)}</p>`:''}<p data-object-id="selection" class="g9-ex-result">${!given&&done>=total-1?'Result: '+esc(scene.answer):''}</p><div class="g9-ex-action"><div data-object-id="operation">${phase==='operation'?esc(state.working_state):''}</div><div data-object-id="result">${phase==='result'&&done<total?esc(state.after_state):''}</div><div data-object-id="verification">${phase==='result'&&done===total?esc(state.after_state):''}</div></div></section>`;
  },destroy(){}
 });
})();
