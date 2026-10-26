/* Grade 8 division: question-specific quotient lanes and persistent divisor paths. */
(() => {
  const safe=value=>escapeWhiteboardHtml(String(value??''));
  const stage=state=>Number(((state.annotations||[]).find(item=>item.startsWith('stage:'))||'stage:0').slice(6));
  const families=['equal_share','signed_quotient','factor_cancel','term_share','three_term_share',
                  'exponent_lanes','context_packs','error_division','two_quotients'];

  function scene(family,params,phase,current){
    const tokens=params.model_tokens,lanes=params.model_lanes||[];
    const paths=current>1||(current===1&&['operation','result'].includes(phase));
    const target=(index,role)=>`<div class="division-card division-card--${role}" data-object-id="token-${index+1}"><small>${safe(lanes[index]||role)}</small><strong>${safe(tokens[index])}</strong></div>`;
    const lane=(index,denominator)=>`<div class="division-lane" data-division-lane="${index+1}">${target(index,'numerator')}<span class="division-connector ${paths?'is-drawn':''}" aria-hidden="${!paths}">${paths?'÷':' '}</span><span class="division-denominator-ref">${safe(tokens[denominator])}</span></div>`;
    let body;
    if(family==='two_quotients'){
      const first=current===1&&paths?'is-active':'',second=current===2&&paths?'is-active':'',subtraction=current===3&&paths?'is-active':'';
      body=`<div class="division-group ${first}" data-division-group="first"><span class="division-group-label">First quotient</span>${lane(0,2)}${lane(1,2)}${target(2,'divisor')}</div><div class="division-subtract ${subtraction}">${target(3,'subtract')}</div><div class="division-group ${second}" data-division-group="second"><span class="division-group-label">Second quotient</span>${lane(4,6)}${lane(5,6)}${target(6,'divisor')}</div>`;
    }else if(family==='error_division'){
      const error=current>=3&&paths?'<span class="division-error" data-diagnosis="undivided-constant">The constant was copied without division.</span>':'';
      body=`<div class="division-group" data-division-group="claim-check">${lane(0,2)}${lane(1,2)}${target(2,'divisor')}${target(3,'claim')}${error}</div>`;
    }else if(family==='factor_cancel'&&tokens.length===4){
      body=`<div class="division-group" data-division-group="factor-pairs">${target(0,'numerator')}${target(1,'factor')}${target(2,'divisor')}${target(3,'factor')}<span class="division-connector ${paths?'is-drawn':''}" aria-hidden="${!paths}">${paths?'Match one variable factor':' '}</span></div>`;
    }else{
      const denominator=tokens.length-1;
      body=`<div class="division-group" data-division-group="all-terms">${tokens.slice(0,denominator).map((_,index)=>lane(index,denominator)).join('')}${target(denominator,'divisor')}</div>`;
    }
    const restriction=/[≠]|cannot be zero|nonzero|restriction/i.test(params.prompt)
      ?'<p class="division-restriction">A variable divisor excludes zero; keep this condition after simplifying.</p>':'';
    const numberOfGroups=family==='context_packs'?6:family==='equal_share'?Number(tokens.at(-1)):0;
    const groups=numberOfGroups>0&&numberOfGroups<=8
      ?`<div class="division-equal-groups" role="img" aria-label="${numberOfGroups} equal groups; quantities still to be shared">${Array.from({length:numberOfGroups},(_,i)=>`<span data-share-group="${i+1}">Group ${i+1}<small>${paths?'each numerator part is shared':'? per group'}</small></span>`).join('')}</div>`:'';
    const count=groups?'<p class="division-context">Each equal group receives a share of every relevant quantity.</p>':'';
    return `<div class="division-scene division-scene--${safe(family)}" data-object-id="model">${body}${groups}${restriction}${count}</div>`;
  }

  for(const family of families){
    AthenaVisualizationRegistry.register('algebra',family,{render(params,state,phase){
      const current=stage(state),active=phase==='operation'||phase==='result',result=phase==='result';
      const final=result&&current>=Number(params.total_steps);
      return `<section class="division-visual" data-question-id="${safe(params.question_id)}" data-phase="${safe(phase)}" data-stage="${current}" data-managed-visibility="true"><p class="g8-original"><strong>Original question</strong><span data-object-id="problem">${safe(params.prompt)}</span></p>${scene(family,params,phase,current)}<div class="g8-mathematical-transition"><div class="g8-state g8-state--before">${safe(state.before_state)}</div><div class="g8-action-slot"><div data-object-id="operation" class="g8-timeline-object g8-operation ${active?'is-visible':'is-hidden'}"><span>Mathematical action</span><strong>${active?safe(state.working_state):''}</strong></div><div data-object-id="result" class="g8-timeline-object g8-result ${result&&!final?'is-visible':'is-hidden'}"><span>Result of this step</span><strong>${result?safe(state.after_state):''}</strong></div><div data-object-id="verification" class="g8-timeline-object g8-verification ${final?'is-visible':'is-hidden'}"><span>Checked conclusion</span><strong>${final?safe(state.after_state):''}</strong></div></div></div></section>`;
    },destroy(){}});
  }
})();
