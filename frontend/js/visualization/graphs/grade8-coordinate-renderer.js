/* Grade 8 coordinates. This renderer consumes one question's validated scene. */
(() => {
  const esc=value=>escapeWhiteboardHtml(String(value));
  const fmt=value=>Number(value).toFixed(2).replace(/\.00$/,'');
  function verify(scene) {
    const a=scene.axis;
    if (!a || ![a.x_min,a.x_max,a.y_min,a.y_max,a.x_tick,a.y_tick].every(Number.isFinite)
      || a.x_min>0 || a.x_max<=0 || a.y_min>0 || a.y_max<=0 || a.x_tick<=0 || a.y_tick<=0)
      throw Error(`Invalid coordinate axes for ${scene.id||'unknown scene'}`);
    const labels=new Set();
    for(const point of [...(scene.given||[]),...(scene.derived||[])]) {
      if(!Number.isFinite(point.x)||!Number.isFinite(point.y)||point.x<a.x_min||point.x>a.x_max||point.y<a.y_min||point.y>a.y_max)
        throw Error(`Point out of bounds for ${scene.id||'unknown scene'}`);
      if(labels.has(point.label))throw Error(`Duplicate point label for ${scene.id||'unknown scene'}`);
      labels.add(point.label);
    }
  }
  const ticks=(min,max,interval)=>{
    const values=[];
    for(let step=Math.ceil(min/interval);step<=Math.floor(max/interval);step++)values.push(step*interval);
    return values;
  };
  function renderScene(scene,stage,phase){
    verify(scene);
    const a=scene.axis,W=640,H=460,left=64,right=618,top=35,bottom=411;
    const px=x=>left+(x-a.x_min)*(right-left)/(a.x_max-a.x_min);
    const py=y=>bottom-(y-a.y_min)*(bottom-top)/(a.y_max-a.y_min);
    const ox=px(0),oy=py(0),completed=phase==='result'?stage:stage-1;
    const xTicks=ticks(a.x_min,a.x_max,a.x_tick).map(x=>`<g data-object-id="x-tick-${esc(x)}"><line x1="${fmt(px(x))}" y1="${fmt(oy-5)}" x2="${fmt(px(x))}" y2="${fmt(oy+5)}"/><text x="${fmt(px(x))}" y="${fmt(oy+22)}" text-anchor="middle">${esc(x)}</text></g>`).join('');
    const yTicks=ticks(a.y_min,a.y_max,a.y_tick).map(y=>`<g data-object-id="y-tick-${esc(y)}"><line x1="${fmt(ox-5)}" y1="${fmt(py(y))}" x2="${fmt(ox+5)}" y2="${fmt(py(y))}"/><text x="${fmt(ox-11)}" y="${fmt(py(y)+4)}" text-anchor="end">${esc(y)}</text></g>`).join('');
    const given=(scene.given||[]).map((point,i)=>`<g data-object-id="given-point-${i+1}" class="coord-point ${point.error?'is-error':''}"><circle cx="${fmt(px(point.x))}" cy="${fmt(py(point.y))}" r="5"/><text x="${fmt(px(point.x)+9)}" y="${fmt(py(point.y)-9)}">${esc(point.label)}${point.coordinates_hidden?'':` (${esc(point.x)}, ${esc(point.y)})`}</text></g>`).join('');
    const derived=(scene.derived||[]).map((point,i)=>{
      const visible=completed>=point.reveal_step;
      // On the active operation, travel along x. The point and y guide wait
      // until the operation completes, and remain visible in later steps.
      const guiding=phase==='operation'&&stage===point.reveal_step;
      return `<g data-object-id="target-${i+1}">${visible||guiding?`<line data-object-id="x-guide-${i+1}" class="coord-guide" x1="${fmt(ox)}" y1="${fmt(oy)}" x2="${fmt(px(point.x))}" y2="${fmt(oy)}"/>`:''}${visible?`<line data-object-id="y-guide-${i+1}" class="coord-guide" x1="${fmt(px(point.x))}" y1="${fmt(oy)}" x2="${fmt(px(point.x))}" y2="${fmt(py(point.y))}"/><circle data-object-id="point-${i+1}" class="coord-result" cx="${fmt(px(point.x))}" cy="${fmt(py(point.y))}" r="6"/><text data-object-id="point-label-${i+1}" x="${fmt(px(point.x)+9)}" y="${fmt(py(point.y)-9)}">${esc(point.label)} (${esc(point.x)}, ${esc(point.y)})</text>`:''}</g>`;
    }).join('');
    return `<svg class="grade8-coordinate-plane" viewBox="0 0 ${W} ${H}" role="img" aria-label="Coordinate plane for ${esc(scene.id)}"><title>Coordinate plane for ${esc(scene.id)}</title><desc>Tick labels match this question's horizontal and vertical scales. Plotted points appear as the explanation progresses.</desc><line data-object-id="x-axis" x1="${left}" y1="${fmt(oy)}" x2="${right}" y2="${fmt(oy)}"/><line data-object-id="y-axis" x1="${fmt(ox)}" y1="${top}" x2="${fmt(ox)}" y2="${bottom}"/><g class="coord-ticks">${xTicks}${yTicks}</g><text data-object-id="origin" x="${fmt(ox+8)}" y="${fmt(oy+17)}">0</text><text x="${right-20}" y="${fmt(oy-13)}">x${a.x_unit?` (${esc(a.x_unit)})`:''}</text><text x="${fmt(ox+13)}" y="${top+15}">y${a.y_unit?` (${esc(a.y_unit)})`:''}</text>${given}${derived}</svg>`;
  }
  const renderer={
    render(parameters,state,phase){
      const stage=Number(((state.annotations||[]).find(item=>item.startsWith('stage:'))||'stage:0').slice(6));
      const scene=parameters.scene||JSON.parse(parameters.scene_json);
      const final=phase==='result'&&stage>=Number(parameters.total_steps||0);
      const action=phase==='ready'?'':esc(state.working_state||'');
      const result=phase==='result'?esc(state.after_state||''):'';
      return `<section class="grade8-coordinate-board" data-managed-visibility="true" data-question-id="${esc(parameters.question_id)}" data-phase="${esc(phase)}"><p class="g8-original" data-object-id="problem">${esc(parameters.prompt)}</p><div data-object-id="model">${renderScene(scene,stage,phase)}</div><div class="g8-mathematical-transition"><div class="g8-state g8-state--before">${esc(state.before_state||'')}</div><div class="g8-action-slot"><div data-object-id="operation" class="g8-timeline-object g8-operation ${phase==='ready'?'is-hidden':'is-visible'}"><span>Coordinate action</span><strong>${action}</strong></div><div data-object-id="result" class="g8-timeline-object g8-result ${phase==='result'&&!final?'is-visible':'is-hidden'}"><span>Result of this step</span><strong>${result}</strong></div><div data-object-id="verification" class="g8-timeline-object g8-verification ${final?'is-visible':'is-hidden'}"><span>Check the original point</span><strong>${final?result:''}</strong></div></div></div></section>`;
    },destroy(){}
  };
  AthenaVisualizationRegistry.register('graphs','coordinate_plane',renderer);
  AthenaVisualizationRegistry.register('coordinate_geometry','grade8_coordinate_plane',renderer);
})();
