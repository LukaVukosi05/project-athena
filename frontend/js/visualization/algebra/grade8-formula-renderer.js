/* A rectangle model sized and labelled from this question's own measurements. */
(() => {
  const esc = x => escapeWhiteboardHtml(String(x));
  function validate(scene) {
    if (!scene || !['m','cm'].includes(scene.units) || ![scene.length,scene.width,scene.area].every(v=>Number.isFinite(v)&&v>0)
      || Math.abs(scene.length*scene.width-scene.area)>1e-8) throw Error('Invalid rectangle dimensions');
    if (scene.perimeter!==undefined && Math.abs(2*(scene.length+scene.width)-scene.perimeter)>1e-8)
      throw Error('Inconsistent rectangle perimeter');
    if(scene.comparison)validate({...scene.comparison,units:scene.units});
  }
  function draw(scene, label, showLength, showWidth, showArea) {
    const max=Math.max(scene.length,scene.width);
    const w=Math.round(220*scene.length/max);
    const h=Math.round(220*scene.width/max);
    const unit=scene.units;
    const grid=(Number.isInteger(scene.length)&&Number.isInteger(scene.width)&&scene.area<=96)
      ? Array.from({length:scene.length-1},(_,i)=>`<line class="formula-tile" x1="${(i+1)*w/scene.length}" y1="0" x2="${(i+1)*w/scene.length}" y2="${h}"/>`).join('')+
        Array.from({length:scene.width-1},(_,i)=>`<line class="formula-tile" x1="0" y1="${(i+1)*h/scene.width}" x2="${w}" y2="${(i+1)*h/scene.width}"/>`).join('') : '';
    return `<figure class="formula-rectangle" data-object-id="rectangle-${esc(label)}"><figcaption>Rectangle ${esc(label)}</figcaption><svg viewBox="-68 -35 ${w+142} ${h+104}" role="img" aria-label="Rectangle ${esc(label)} with question-specific side proportions"><title>Rectangle ${esc(label)}</title><desc>Area equals length multiplied by width. Given labels are shown before calculated labels.</desc><rect data-object-id="area-grid-${esc(label)}" width="${w}" height="${h}"/>${grid}<text data-object-id="length-label-${esc(label)}" x="${w/2}" y="${h+28}" text-anchor="middle">${showLength?`${esc(scene.symbolic_length||scene.length)} ${unit}`:'length ?'}</text><text data-object-id="width-label-${esc(label)}" x="-6" y="${h/2}" text-anchor="end">${showWidth?`${esc(scene.width)} ${unit}`:'width ?'}</text><text data-object-id="area-label-${esc(label)}" x="${w/2}" y="${h/2}" text-anchor="middle">${showArea?`${esc(scene.area)} ${unit}²`:'area ?'}</text></svg></figure>`;
  }
  AthenaVisualizationRegistry.register('algebra','formula_rectangle',{
    render(params,state,phase){
      const scene=JSON.parse(params.scene_json);validate(scene);
      const givens=params.given_objects||[],stage=Number(((state.annotations||[]).find(v=>v.startsWith('stage:'))||'stage:0').slice(6));
      const final=phase==='result'&&stage>=Number(params.total_steps);
      const revealing=phase==='result'&&stage>=Math.min(3,Number(params.total_steps)-1);
      const has=pattern=>givens.some(v=>pattern.test(v.toLowerCase()));
      const length=has(/(?:^|a )length\s+(?:\d|\()/)||revealing;
      const width=has(/(?:^|a )width\s+(?:\d|x\b)/)||revealing;
      const area=has(/area\s+\d|both areas/)||revealing;
      const second=scene.comparison?draw({...scene.comparison,units:scene.units},'B',revealing,true,true):'';
      const before=esc(state.before_state||'');
      const operation=phase==='ready'?'':esc(state.working_state||'');
      const result=phase==='result'?esc(state.after_state||''):'';
      const givenObjects=givens.map((v,i)=>`<span data-object-id="given-${i+1}" class="formula-given">${esc(v)}</span>`).join('');
      const derivedObjects=(params.derived_objects||[]).map((v,i)=>`<span data-object-id="derived-${i+1}" class="formula-derived ${revealing?'':'is-concealed'}">${revealing?esc(v):'?'}</span>`).join('');
      return `<section class="formula-board" data-managed-visibility="true" data-question-id="${esc(params.question_id)}" data-stage="${stage}" data-phase="${esc(phase)}"><p class="g8-original" data-object-id="problem">${esc(params.prompt)}</p><div data-object-id="model" class="formula-scenes">${draw(scene,scene.comparison?'A':'model',length,width,area)}${second}</div><div class="formula-semantic">${givenObjects}${derivedObjects}</div><div class="g8-mathematical-transition"><div class="g8-state g8-state--before">${before}</div><div class="g8-action-slot"><div data-object-id="operation" class="g8-timeline-object g8-operation ${phase==='ready'?'is-hidden':'is-visible'}"><span>Use the formula</span><strong>${operation}</strong></div><div data-object-id="result" class="g8-timeline-object g8-result ${phase==='result'&&!final?'is-visible':'is-hidden'}"><span>Result of this step</span><strong>${result}</strong></div><div data-object-id="verification" class="g8-timeline-object g8-verification ${final?'is-visible':'is-hidden'}"><span>Check the original measurements</span><strong>${final?result:''}</strong></div></div></div></section>`;
    },destroy(){}
  });
})();
