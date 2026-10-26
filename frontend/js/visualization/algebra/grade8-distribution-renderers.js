/* Grade 8 bracket distribution: authored paths for signed terms. */
(() => {
  const safe=value=>escapeWhiteboardHtml(String(value??''));
  const stage=state=>Number(((state.annotations||[]).find(item=>item.startsWith('stage:'))||'stage:0').slice(6));
  function scene(family,params,phase,current){
    const tokens=params.model_tokens, lanes=params.model_lanes||[];
    if(family==='compare_paths'){
      const reached=current>1||(current===1&&!['initial','ready'].includes(phase));
      const token=(index,multiplier=false)=>`<div class="${multiplier?'distribution-multiplier':'distribution-term'} ${!multiplier&&reached&&[1,2,5,6].includes(index)?'distribution-term--reached':''}" data-object-id="token-${index+1}"><small>${safe(lanes[index]||'given quantity')}</small><strong>${safe(tokens[index])}</strong>${!multiplier&&[1,2,5,6].includes(index)?`<span class="distribution-path" data-object-id="path-${index+1}" aria-hidden="${!reached}">${reached?'↘':''}</span>`:''}</div>`;
      const group=(factor,terms)=>`<div class="distribution-group">${token(factor,true)}<span class="distribution-bracket" aria-hidden="true">(</span>${terms.map(index=>token(index)).join('')}<span class="distribution-bracket" aria-hidden="true">)</span></div>`;
      if(tokens.length===7)return `<div class="distribution-scene distribution-scene--compare_paths" data-object-id="model">${group(0,[1,2])}${token(3)}${group(4,[5,6])}</div>`;
      return `<div class="distribution-scene distribution-scene--compare_paths" data-object-id="model">${group(0,[1,2])}${token(3)}</div>`;
    }
    const signedTerms=tokens.slice(1);
    const terms=signedTerms.map((token,index)=>{
      const reached=current>1||(current===1&&!['initial','ready'].includes(phase));
      return `<div class="distribution-term ${reached?'distribution-term--reached':''}" data-object-id="token-${index+2}"><small>${safe(lanes[index+1]||`term ${index+1}`)}</small><strong>${safe(token)}</strong><span class="distribution-path" data-object-id="path-${index+1}" aria-hidden="${!reached}">${reached?'↘':''}</span></div>`;
    }).join('');
    const segments=params.model_scene?.segments?.split('|')||signedTerms;
    const area=family==='area_distribute'?`<div class="distribution-area" data-object-id="area-model" role="img" aria-label="${safe(params.model_scene?.side||tokens[0])} by ${safe(segments.join(' and '))} split area">${segments.map((piece,index)=>`<span data-object-id="region-${index+1}">${safe(piece)} × ${safe(params.model_scene?.side||tokens[0])}</span>`).join('')}</div>`:'';
    const signs=family==='signed_distribute'?`<div class="distribution-signs" aria-label="Signed factors">${tokens.map(token=>`<span>${safe(token.trim().startsWith('-')?'negative':'positive')}</span>`).join('')}</div>`:'';
    const comparison=family==='compare_paths'&&tokens.some(token=>token.startsWith('claim:'))?'<p class="distribution-claim">Compare the learner claim with both multiplication paths.</p>':'';
    return `<div class="distribution-scene distribution-scene--${safe(family)}" data-object-id="model"><div class="distribution-multiplier" data-object-id="token-1"><small>${safe(lanes[0]||'outside multiplier')}</small><strong>${safe(tokens[0])}</strong></div><span class="distribution-bracket" aria-hidden="true">(</span><div class="distribution-terms">${terms}</div><span class="distribution-bracket" aria-hidden="true">)</span>${signs}${area}${comparison}</div>`;
  }
  for(const family of ['distribute_strip','signed_distribute','trinomial_branches','area_distribute','compare_paths']){
    AthenaVisualizationRegistry.register('algebra',family,{render(params,state,phase){
      const current=stage(state),active=phase==='operation'||phase==='result',result=phase==='result',final=result&&current>=Number(params.total_steps);
      return `<section class="distribution-visual" data-question-id="${safe(params.question_id)}" data-phase="${safe(phase)}" data-stage="${current}" data-managed-visibility="true"><p class="g8-original"><strong>Original question</strong><span data-object-id="problem">${safe(params.prompt)}</span></p>${scene(family,params,phase,current)}<div class="g8-mathematical-transition"><div class="g8-state g8-state--before">${safe(state.before_state)}</div><div class="g8-action-slot"><div data-object-id="operation" class="g8-timeline-object g8-operation ${active?'is-visible':'is-hidden'}"><span>Mathematical action</span><strong>${active?safe(state.working_state):''}</strong></div><div data-object-id="result" class="g8-timeline-object g8-result ${result&&!final?'is-visible':'is-hidden'}"><span>Result of this step</span><strong>${result?safe(state.after_state):''}</strong></div><div data-object-id="verification" class="g8-timeline-object g8-verification ${final?'is-visible':'is-hidden'}"><span>Checked conclusion</span><strong>${final?safe(state.after_state):''}</strong></div></div></div></section>`;
    },destroy(){}});
  }
})();
