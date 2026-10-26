/* Native Grade 8 powers and roots. Each question supplies its factor cards. */
(() => {
  const safe=value=>escapeWhiteboardHtml(String(value??''));
  const stage=state=>Number(((state.annotations||[]).find(v=>v.startsWith('stage:'))||'stage:0').slice(6));
  const families=['square_grid','signed_square','cube_stack','signed_cube','sign_scope',
    'power_factor_stack','root_pairs','absolute_root','cube_root','fraction_cube',
    'error_root','compare_powers','compare_roots'];
  const cube=new Set(['cube_stack','signed_cube','cube_root','fraction_cube']);

  function mathematicalModel(family,tokens,active,inputCount){
    if(family==='square_grid'||family==='signed_square'||family==='power_factor_stack'){
      const side=family==='power_factor_stack'?`${tokens[0]}·${tokens[1]}`:tokens[0];
      return `<svg class="power-root-shape" viewBox="0 0 240 155" role="img" aria-label="A square with both sides equal to ${safe(side)}"><title>Square of the whole algebraic term</title><rect x="72" y="14" width="120" height="120" rx="8"/><text x="132" y="78" text-anchor="middle">${active?'multiply both sides':'area ?'}</text><text x="132" y="150" text-anchor="middle">${safe(side)}</text><text x="18" y="79" text-anchor="middle" transform="rotate(-90 18 79)">${safe(side)}</text></svg>`;
    }
    if(family==='cube_stack'||family==='signed_cube'||family==='fraction_cube'){
      const side=tokens[0];
      return `<svg class="power-root-shape" viewBox="0 0 245 155" role="img" aria-label="Three dimensions all labelled ${safe(side)}"><title>Three complete factors make a cube</title><path d="M55 40 L155 40 L190 18 L90 18 Z M155 40 L190 18 L190 116 L155 137 Z M55 40 L155 40 L155 137 L55 137 Z"/><text x="105" y="93" text-anchor="middle">${active?'factor × factor × factor':'volume ?'}</text><text x="105" y="153" text-anchor="middle">${safe(side)}</text><text x="196" y="82">${safe(side)}</text><text x="94" y="13">${safe(side)}</text></svg>`;
    }
    if(family==='root_pairs'||family==='absolute_root'||family==='cube_root'){
      const size=family==='cube_root'?3:2;
      return `<div class="power-root-match" role="img" aria-label="Match ${size} identical factors from each original group"><strong>${size===3?'Cube-root triples':'Square-root pairs'}</strong><div>${tokens.slice(0,inputCount).map((token,i)=>`<span data-match-group="${i+1}">${safe(token)}<small>${size} matching factors → one factor</small></span>`).join('')}</div></div>`;
    }
    return '';
  }

  function scene(family,params,state,phase,current){
    const tokens=params.model_tokens||[],inputCount=Number(params.model_scene?.input_count||2);
    const active=phase==='operation'||phase==='result';
    const lastTeachingStage=Number(params.total_steps)-1;
    const exposed=(index)=>index<inputCount||
      current>lastTeachingStage||current===lastTeachingStage&&phase==='result';
    const cards=tokens.map((value,index)=>{
      const visible=exposed(index);
      const role=index<inputCount?'given':'derived';
      return `<div class="power-root-factor power-root-factor--${role} ${visible?'is-visible':'is-concealed'}" data-object-id="token-${index+1}" data-factor-index="${index+1}" aria-label="${role} ${index+1}${visible?`: ${safe(value)}`:' not yet taught'}"><small>${role==='given'?'Given factor':'Derived factor'}</small><strong>${visible?safe(value):'?'}</strong></div>`;
    });
    const makeGroup=(label,contents,cls)=>`<div class="power-root-group ${cls}" data-factor-group="${safe(label)}"><span class="power-root-group-label">${safe(label)}</span><div class="power-root-factor-row">${contents}</div></div>`;
    let content;
    if(family==='sign_scope'){
      content=makeGroup('Minus inside the square',cards[0]+cards[2],'power-root-group--square')+
        makeGroup('Minus outside the square',cards[1]+cards[3],'power-root-group--outside');
    }else if(family==='error_root'){
      content=makeGroup('Learner claim',cards[0]+cards[1],'power-root-group--claim')+
        makeGroup('Negative input check and repair',cards[2]+cards[3],'power-root-group--root');
    }else if(family==='compare_powers'||family==='compare_roots'){
      const first=family==='compare_roots'?'Square-root branch':'First square',second=family==='compare_roots'?'Cube-root branch':'Second square';
      content=makeGroup(first,cards[0]+cards[2],'power-root-group--branch')+
        makeGroup(second,cards[1]+cards[3],'power-root-group--branch')+
        makeGroup('Combine and evaluate',cards.slice(4).join(''),'power-root-group--combine');
    }else{
      const grouped=cards.slice(0,inputCount).join('');
      const derived=cards.slice(inputCount).join('');
      const title=family==='absolute_root'?'Principal root: choose a nonnegative magnitude':
        family==='root_pairs'?'Pair equal factors':cube.has(family)?'Three factors in each cube group':'Two copies of the entire base';
      content=makeGroup(title,grouped,cube.has(family)?'power-root-group--cube':'power-root-group--square')+
        makeGroup('Result after the action',derived,'power-root-group--derived');
    }
    const pairs=(family==='root_pairs'||family==='absolute_root')?'<span class="power-root-guide">Pair equal factors → one nonnegative magnitude</span>':
      cube.has(family)?'<span class="power-root-guide">Group three matching factors → one signed factor</span>':
      '<span class="power-root-guide">Keep the exponent attached to the entire parenthesised base</span>';
    const domain=/x ≥ 0|for any real|any real a|every real/.test(params.prompt)
      ?`<p class="power-root-domain">${family==='absolute_root'||family==='error_root'?'√(a²) gives |a| for unrestricted real a.':'For square roots, check the stated sign condition. An odd cube root keeps the sign.'}</p>`:'';
    return `<div class="power-root-scene power-root-scene--${safe(family)}" data-object-id="model">${mathematicalModel(family,tokens,active,inputCount)}${content}${active?pairs:''}${domain}</div>`;
  }
  for(const family of families){
    AthenaVisualizationRegistry.register('algebra',family,{render(params,state,phase){
      const current=stage(state),active=phase==='operation'||phase==='result',result=phase==='result';
      const final=result&&current>=Number(params.total_steps);
      return `<section class="power-root-visual" data-question-id="${safe(params.question_id)}" data-phase="${safe(phase)}" data-stage="${current}" data-managed-visibility="true"><p class="g8-original"><strong>Original question</strong><span data-object-id="problem">${safe(params.prompt)}</span></p>${scene(family,params,state,phase,current)}<div class="g8-mathematical-transition"><div class="g8-state g8-state--before">${safe(state.before_state)}</div><div class="g8-action-slot"><div data-object-id="operation" class="g8-timeline-object g8-operation ${active?'is-visible':'is-hidden'}"><span>Mathematical action</span><strong>${active?safe(state.working_state):''}</strong></div><div data-object-id="result" class="g8-timeline-object g8-result ${result&&!final?'is-visible':'is-hidden'}"><span>Result of this step</span><strong>${result?safe(state.after_state):''}</strong></div><div data-object-id="verification" class="g8-timeline-object g8-verification ${final?'is-visible':'is-hidden'}"><span>Checked conclusion</span><strong>${final?safe(state.after_state):''}</strong></div></div></div></section>`;
    },destroy(){}});
  }
})();
