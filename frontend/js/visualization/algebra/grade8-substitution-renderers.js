/* Grade 8 numerical value: labelled input slots and scenario-specific paths. */
(() => {
  const safe=value=>escapeWhiteboardHtml(String(value??''));
  const stage=state=>Number(((state.annotations||[]).find(value=>value.startsWith('stage:'))||'stage:0').slice(6));
  const families=['value_machine','signed_slot','exponent_scope','compare_scope',
    'two_input','bracket_input','layered_order','fraction_gate',
    'equivalent_value_paths','error_substitution','context_measure'];
  function scene(family,params,current,phase){
    const tokens=params.model_tokens||[],count=Number(params.model_scene?.input_count||2);
    const final=current>=Number(params.total_steps)-1&&phase==='result'||current>=Number(params.total_steps);
    const card=(i)=>`<div class="substitution-card ${i<count?'substitution-card--given':'substitution-card--output'} ${i<count||final?'is-visible':'is-concealed'}" data-object-id="token-${i+1}"><small>${i<count?(i===0?'Expression or dimension':'Given value'):'Calculated value'}</small><strong>${i<count||final?safe(tokens[i]):'?'}</strong></div>`;
    const group=(name,items)=>`<div class="substitution-group" data-path="${safe(name)}"><strong>${safe(name)}</strong><div class="substitution-cards">${items.map(card).join('')}</div></div>`;
    let visual;
    if(family==='compare_scope'||family==='equivalent_value_paths'){
      const input=family==='compare_scope'?2:2;
      visual=group('First expression',[0,input+1])+group('Second expression',[1,input+2])+group('Use this input',[input]);
    }else if(family==='two_input'){
      visual=group('Original expression',[0])+group('Separate variable slots',[1,2])+group('Output',[3]);
    }else if(family==='fraction_gate'&&count===3){
      visual=group('Original fraction',[0])+group('First denominator',[1,3])+group('Second denominator',[2,4]);
    }else if(family==='layered_order'&&count===4){
      visual=group('Power branch',[0])+group('Bracket branch',[1])+group('Quotient branch',[2])+group('Signed input and total',[3,4]);
    }else if(family==='context_measure'){
      visual=`<svg class="substitution-rectangle" viewBox="0 0 290 150" role="img" aria-label="Rectangle with sides ${safe(tokens[0])} and ${safe(tokens[1])}"><title>Rectangle perimeter</title><rect x="47" y="16" width="198" height="105" rx="3"/><text x="145" y="142" text-anchor="middle">${safe(tokens[0])}</text><text x="18" y="80" text-anchor="middle" transform="rotate(-90 18 80)">${safe(tokens[1])}</text><text x="145" y="75" text-anchor="middle">${phase==='ready'?'P = ?':'trace all four sides'}</text></svg>`+
        group('Given dimensions and rule',[0,1,2,3])+group('Perimeter after calculation',[4]);
    }else if(family==='error_substitution'){
      visual=group('Original and signed input',[0,1])+group('Learner claim to inspect',[2])+group('Repaired result',[3]);
    }else{
      visual=group(family==='exponent_scope'?'Bracket the signed base before squaring':family==='bracket_input'?'Keep the bracket around the group':family==='fraction_gate'?'Keep the denominator beneath the fraction bar':'Move the given value into the variable slot',Array.from({length:count},(_,i)=>i))+
        group('Numerical output',Array.from({length:tokens.length-count},(_,i)=>count+i));
    }
    const prompt=family==='fraction_gate'&&count===3?'<p class="substitution-check">A zero denominator makes that input undefined. Check both branches.</p>':
      family==='exponent_scope'||family==='compare_scope'||family==='error_substitution'?'<p class="substitution-check">Keep a negative input inside parentheses before applying a power.</p>':'';
    return `<div class="substitution-scene substitution-scene--${safe(family)}" data-object-id="model">${visual}${prompt}</div>`;
  }
  for(const family of families){
    AthenaVisualizationRegistry.register('algebra',family,{render(params,state,phase){
      const current=stage(state),active=phase==='operation'||phase==='result',result=phase==='result';
      const final=result&&current>=Number(params.total_steps);
      return `<section class="substitution-visual" data-question-id="${safe(params.question_id)}" data-phase="${safe(phase)}" data-stage="${current}" data-managed-visibility="true"><p class="g8-original"><strong>Original question</strong><span data-object-id="problem">${safe(params.prompt)}</span></p>${scene(family,params,current,phase)}<div class="g8-mathematical-transition"><div class="g8-state g8-state--before">${safe(state.before_state)}</div><div class="g8-action-slot"><div data-object-id="operation" class="g8-timeline-object g8-operation ${active?'is-visible':'is-hidden'}"><span>Mathematical action</span><strong>${active?safe(state.working_state):''}</strong></div><div data-object-id="result" class="g8-timeline-object g8-result ${result&&!final?'is-visible':'is-hidden'}"><span>Result of this step</span><strong>${result?safe(state.after_state):''}</strong></div><div data-object-id="verification" class="g8-timeline-object g8-verification ${final?'is-visible':'is-hidden'}"><span>Checked conclusion</span><strong>${final?safe(state.after_state):''}</strong></div></div></div></section>`;
    },destroy(){}});
  }
})();
