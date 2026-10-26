/* Five native Grade 8 monomial product scenes. Given factors remain visible;
   the operation is shown before the result and the numerical check is last. */
(() => {
  const safe=value=>escapeWhiteboardHtml(String(value??''));
  const stage=state=>Number(((state.annotations||[]).find(value=>value.startsWith('stage:'))||'stage:0').slice(6));
  function given(params,phase,current){
    return `<div class="product-factors" data-object-id="model">${params.model_tokens.map((token,n)=>`<span class="product-factor ${phase!=='initial'&&current>=n+1?'product-factor--active':''}" data-object-id="token-${n+1}"><small>${safe(params.model_lanes?.[n]||`factor ${n+1}`)}</small><strong>${safe(token)}</strong></span>`).join('')}</div>`;
  }
  function grid(rows,cols,unit,share=1){
    if(rows===0)return '<p class="product-zero-model">Zero groups: no product tiles appear.</p>';
    if(!rows||!cols)return '';
    const max=Math.min(rows*cols,48),shown=Math.round(max*share);
    return `<div class="product-area-grid" style="--product-columns:${cols}" role="img" aria-label="${safe(rows)} rows and ${safe(cols)} columns of ${safe(unit)} tiles">${Array.from({length:max},(_,i)=>`<span class="product-area-cell ${i<shown?'':'product-area-cell--unused'}" aria-hidden="true">${safe(unit)}</span>`).join('')}</div>`;
  }
  function drawing(family,params,phase,current){
    const scene=params.model_scene||{};
    if(phase==='initial')return '<div class="product-scene product-scene--ready" aria-label="The complete problem and given factors are shown. Start to build the product."></div>';
    if(family==='factor_array'||family==='area_product'){
      return `<div class="product-scene"><p>${family==='area_product'?'Multiply side lengths to count square units.':'Build the given equal groups.'}</p>${grid(scene.rows,scene.columns,scene.unit||'unit',scene.share||1)}${scene.unit_price?`<small>Each item costs R${scene.unit_price}.</small>`:''}</div>`;
    }
    if(family==='area_comparison')return `<div class="product-scene product-area-comparison"><div><small>Square</small>${grid(scene.square_rows,scene.square_columns,scene.unit)}</div><div><small>Rectangle</small>${grid(scene.rectangle_rows,scene.rectangle_columns,scene.unit)}</div></div>`;
    if(family==='sign_grid'){
      const signs=params.model_tokens.map(item=>item.trim().startsWith('-')?'−':'+');
      return `<div class="product-scene product-signs"><small>Resolve every factor’s sign before writing the product</small><div>${signs.map(sign=>`<span class="product-sign-badge">${sign}</span>`).join('')}</div></div>`;
    }
    if(family==='power_stack'){
      const factors=params.model_tokens.flatMap(token=>{
        if(/^[xyap]$/.test(token))return [token];
        const match=token.match(/\(-?\d+([xyap])\)/);
        return match?[match[1]]:[];
      });
      return `<div class="product-scene product-powers"><small>Count each matching variable factor</small><div>${factors.map(token=>`<span class="product-power-chip">${safe(token)}</span>`).join('')}</div></div>`;
    }
    return '';
  }
  for(const family of ['factor_array','sign_grid','area_product','power_stack','area_comparison']){
    AthenaVisualizationRegistry.register('algebra',family,{render(params,state,phase){
      const current=stage(state),active=phase!=='initial',result=phase==='result',final=result&&current>=Number(params.total_steps);
      return `<section class="product-visual" data-question-id="${safe(params.question_id)}" data-phase="${safe(phase)}" data-stage="${current}" data-managed-visibility="true"><p class="g8-original"><strong>Original question</strong><span data-object-id="problem">${safe(params.prompt)}</span></p>${given(params,phase,current)}${drawing(family,params,phase,current)}<div class="g8-mathematical-transition"><div class="g8-state g8-state--before">${safe(state.before_state)}</div><div class="g8-action-slot"><div data-object-id="operation" class="g8-timeline-object g8-operation ${active?'is-visible':'is-hidden'}"><span>Mathematical action</span><strong>${active?safe(state.working_state):''}</strong></div><div data-object-id="result" class="g8-timeline-object g8-result ${result&&!final?'is-visible':'is-hidden'}"><span>Result of this step</span><strong>${result?safe(state.after_state):''}</strong></div><div data-object-id="verification" class="g8-timeline-object g8-verification ${final?'is-visible':'is-hidden'}"><span>Checked conclusion</span><strong>${final?safe(state.after_state):''}</strong></div></div></div></section>`;
    },destroy(){}});
  }
})();
