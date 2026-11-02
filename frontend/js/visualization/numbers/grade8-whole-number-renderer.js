/* Two native boards: operation-group comparison and prime factor trees. */
(() => {
  const esc=value=>escapeWhiteboardHtml(String(value??''));
  AthenaVisualizationRegistry.register('algebra','grade8_whole_number_board',{
    render(p,state,phase){
      const scene=JSON.parse(p.scene_json);
      const step=Number(((state.annotations||[]).find(x=>x.startsWith('stage:'))||'stage:0').slice(6));
      const done=phase==='result'?step:Math.max(0,step-1);
      const final=done===Number(p.total_steps);
      let visual='';
      if(scene.model==='property'){
        const [a,b,c]=scene.values;
        const tiles=scene.kind==='dist'?
          `<div class="g8-whole-area" data-object-id="groups"><span data-object-id="given-1">${esc(a)} rows</span><div class="g8-whole-part" data-object-id="given-2">${esc(b)} tiles in each row</div><div class="g8-whole-part" data-object-id="given-3">${esc(c)} tiles in each row</div></div>`:
          scene.kind==='zero_div'?`<div class="g8-whole-zero" data-object-id="groups"><span data-object-id="given-1">${esc(a)}</span> ÷ <span data-object-id="given-2">0</span><span>How many groups of size zero?</span></div>`:
          `<div class="g8-whole-groups" data-object-id="groups">${[a,b,...(scene.kind.startsWith('assoc')?[c]:[])].map((v,i)=>`<span data-object-id="given-${i+1}" class="g8-whole-quantity">${esc(v)}</span>`).join('')}</div>`;
        visual=`<div class="g8-whole-visual" data-object-id="model"><div class="g8-whole-compare"><span data-object-id="left-expression">${esc(scene.left)}</span><span aria-label="compared with">⇔</span><span data-object-id="right-expression">${done>=2?esc(scene.right):'?'}</span></div>${tiles}<p data-object-id="property-label">${done>=3?`Property: ${esc(scene.property)}`:''}</p><p data-object-id="computed-answer">${final?`Check: ${esc(scene.answer)}`:''}</p></div>`;
      }else{
        const roots=scene.numbers;
        visual=`<div class="g8-whole-visual g8-whole-trees" data-object-id="model">${roots.map((root,i)=>{
          const leaves=(scene.factors||[])[i]||[];
          let current=root;
          const splits=leaves.slice(0,-1).map((prime,j)=>{const quotient=current/prime;
            const line=`<div class="g8-whole-branches" data-object-id="split-${i+1}-${j+1}">${esc(current)} = <span>${esc(prime)}</span> × <span>${esc(quotient)}</span></div>`;
            current=quotient;return line;});
          return `<div class="g8-whole-tree" data-object-id="tree-${i+1}"><strong data-object-id="given-${i+1}">${esc(root)}</strong>${splits.slice(0,Math.max(0,done-1)).join('')}${done>=p.total_steps-1?`<div class="g8-whole-leaves" aria-label="Prime factors of ${esc(root)}">${leaves.map((v,j)=>`<span data-object-id="prime-${i+1}-${j+1}">${esc(v)}</span>`).join('')}</div>`:''}</div>`;
        }).join('')}<p data-object-id="selection-rule">${done>=p.total_steps-1?(scene.kind==='hcf'?'Use smallest powers shared by all roots.':scene.kind==='lcm'?'Use the largest powers needed by any root.':'Select the largest prime leaf.'):''}</p><p data-object-id="computed-answer">${final?`${scene.kind==='largest_prime'?'Largest prime':scene.kind.toUpperCase()} = ${esc(scene.answer)}`:''}</p></div>`;
      }
      return `<section class="g8-whole-board" data-managed-visibility="true" data-question-id="${esc(p.question_id)}" data-phase="${esc(phase)}"><p class="g8-original" data-object-id="problem">${esc(p.prompt)}</p>${visual}<div class="g8-mathematical-transition"><div class="g8-state g8-state--before">${esc(state.before_state||'')}</div><div class="g8-action-slot"><div data-object-id="operation" class="g8-timeline-object g8-operation ${phase==='ready'?'is-hidden':'is-visible'}"><span>Mathematical action</span><strong>${phase==='ready'?'':esc(state.working_state||'')}</strong></div><div data-object-id="result" class="g8-timeline-object g8-result ${phase==='result'&&!final?'is-visible':'is-hidden'}"><span>Result of this step</span><strong>${phase==='result'&&!final?esc(state.after_state||''):''}</strong></div><div data-object-id="verification" class="g8-timeline-object g8-verification ${final?'is-visible':'is-hidden'}"><span>Check the original question</span><strong>${final?esc(state.after_state||''):''}</strong></div></div></div></section>`;
    },destroy(){}
  });
})();
