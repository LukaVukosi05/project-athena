/* Question-specific global graph: given curve reading or progressively constructed story. */
(() => {
  const esc=v=>escapeWhiteboardHtml(String(v));
  const fmt=v=>Number(v).toFixed(2).replace(/\.00$/,'');
  function renderGraph(scene,stage,phase){
    const a=scene.axis, points=scene.points,W=620,H=380,L=62,R=590,T=28,B=324;
    const px=x=>L+(x-a.x_min)*(R-L)/(a.x_max-a.x_min);
    const py=y=>B-(y-a.y_min)*(B-T)/(a.y_max-a.y_min);
    const completed=phase==='result'?stage:Math.max(0,stage-1);
    const current=phase==='operation'?stage:0;
    const ticks=(axis,min,max,tick,project)=>{let out='';for(let v=Math.ceil(min/tick)*tick;v<=max;v+=tick){out+=axis==='x'?`<g><line x1="${fmt(project(v))}" y1="${B}" x2="${fmt(project(v))}" y2="${B+5}"/><text x="${fmt(project(v))}" y="${B+23}" text-anchor="middle">${esc(v)}</text></g>`:`<g><line x1="${L-5}" y1="${fmt(project(v))}" x2="${L}" y2="${fmt(project(v))}"/><text x="${L-9}" y="${fmt(project(v)+4)}" text-anchor="end">${esc(v)}</text></g>`;}return out;};
    const dot=(p,i,active=false,label='')=>`<g data-object-id="graph-point-${i+1}" class="g8-global-dot ${active?'is-current':''}"><circle cx="${fmt(px(p.x))}" cy="${fmt(py(p.y))}" r="5"/><text x="${fmt(px(p.x)+7)}" y="${fmt(py(p.y)-9)}">${label?esc(label)+' ':''}(${esc(p.x)}, ${esc(p.y)})</text></g>`;
    let segments='',dots='';
    if(scene.kind==='compare'){
      const secondary=scene.secondary_points;
      if(scene.domain==='continuous'){
        segments=`<polyline data-object-id="graph-a" class="g8-global-given" points="${points.map(p=>`${fmt(px(p.x))},${fmt(py(p.y))}`).join(' ')}"/><polyline data-object-id="graph-b" class="g8-global-secondary" points="${secondary.map(p=>`${fmt(px(p.x))},${fmt(py(p.y))}`).join(' ')}"/>`;
      }
      dots=points.map((p,i)=>dot(p,i,false,'A')).join('')+secondary.map((p,i)=>`<g data-object-id="series-b-point-${i+1}" class="g8-global-dot g8-global-dot--secondary"><circle cx="${fmt(px(p.x))}" cy="${fmt(py(p.y))}" r="5"/><text x="${fmt(px(p.x)+8)}" y="${fmt(py(p.y)+17)}">B(${esc(p.x)}, ${esc(p.y)})</text></g>`).join('');
      if(stage>0){
        const series=current||completed;
        if(series>=2)segments+=`<polyline data-object-id="graph-a-focus" class="g8-global-highlight" points="${points.map(p=>`${fmt(px(p.x))},${fmt(py(p.y))}`).join(' ')}"/>`;
        if(series>=3)segments+=`<polyline data-object-id="graph-b-focus" class="g8-global-highlight g8-global-highlight--secondary" points="${secondary.map(p=>`${fmt(px(p.x))},${fmt(py(p.y))}`).join(' ')}"/>`;
      }
    }else if(scene.kind==='read'||scene.kind==='diagnose'){
      // The source graph is a given. Reading highlights just the interval being taught.
      dots=points.map((p,i)=>dot(p,i)).join('');
      if(scene.domain==='continuous')segments=`<polyline data-object-id="given-graph" class="g8-global-given" points="${points.map(p=>`${fmt(px(p.x))},${fmt(py(p.y))}`).join(' ')}"/>`;
      if(stage>0){const last=Math.min(current||completed,3);for(let index=0;index<last;index++){const p=points[index],q=points[index+1];segments+=`<line data-object-id="graph-highlight-${index+1}" class="g8-global-highlight ${current===index+1?'is-animating':''}" x1="${fmt(px(p.x))}" y1="${fmt(py(p.y))}" x2="${fmt(px(q.x))}" y2="${fmt(py(q.y))}"/>`;}if(stage>=3){const q=points[scene.kind==='diagnose'?scene.focus_index:3];segments+=`<line class="g8-global-projection" x1="${fmt(px(q.x))}" x2="${fmt(px(q.x))}" y1="${fmt(py(q.y))}" y2="${B}"/>`;}}
    }else{
      const visible=Math.min(points.length,Math.max(0,completed,current));
      dots=points.slice(0,visible).map((p,i)=>dot(p,i,current===i)).join('');
      if(scene.domain==='continuous')segments=points.slice(1,visible).map((p,i)=>`<line data-object-id="graph-segment-${i+1}" class="g8-global-segment ${current===i+2?'is-animating':''}" x1="${fmt(px(points[i].x))}" y1="${fmt(py(points[i].y))}" x2="${fmt(px(p.x))}" y2="${fmt(py(p.y))}"/>`).join('');
    }
    const description=scene.kind==='draw'?'The graph is constructed one point and interval at a time.':scene.kind==='compare'?'Graphs A and B share one scale; each is examined in sequence.':'The given graph is visible; the active interval is highlighted in sequence.';
    return `<svg class="grade8-global-graph" viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(scene.title)} graph, ${esc(a.x_unit)} horizontally and ${esc(a.y_unit)} vertically"><title>${esc(scene.title)}</title><desc>${description} ${scene.domain==='discrete'?'Only whole-count points are drawn.':''}</desc><line class="g8-global-axis" x1="${L}" y1="${B}" x2="${R}" y2="${B}"/><line class="g8-global-axis" x1="${L}" y1="${T}" x2="${L}" y2="${B}"/><g class="g8-global-ticks">${ticks('x',a.x_min,a.x_max,a.x_tick,px)}${ticks('y',a.y_min,a.y_max,a.y_tick,py)}</g><text x="${R-8}" y="${B-10}" text-anchor="end">${esc(a.x_unit)}</text><text x="${L+12}" y="${T+15}">${esc(a.y_unit)}</text>${scene.kind==='compare'?`<text x="${R-96}" y="${T+15}" class="g8-global-legend">A ■  B ◆</text>`:''}${segments}${dots}</svg>`;
  }
  AthenaVisualizationRegistry.register('coordinate_geometry','grade8_global_story',{
    render(parameters,state,phase){
      const scene=parameters.scene||JSON.parse(parameters.scene_json);
      const stage=Number(((state.annotations||[]).find(x=>x.startsWith('stage:'))||'stage:0').slice(6));
      const final=phase==='result'&&stage===Number(parameters.total_steps);
      const diagnosis=scene.kind==='diagnose'?`<p data-object-id="learner-claim" class="g8-global-claim ${final?'is-corrected':stage>1?'is-disputed':''}"><span>Learner claim:</span> ${esc(scene.claim)}</p>`:'';
      return `<section class="grade8-global-board" data-managed-visibility="true" data-question-id="${esc(parameters.question_id)}" data-phase="${esc(phase)}"><p data-object-id="problem" class="g8-original">${esc(parameters.prompt)}</p><div data-object-id="model">${renderGraph(scene,stage,phase)}${diagnosis}</div><div class="g8-mathematical-transition"><div class="g8-state g8-state--before">${esc(state.before_state||'')}</div><div class="g8-action-slot"><div data-object-id="operation" class="g8-timeline-object g8-operation ${phase==='ready'?'is-hidden':'is-visible'}"><span>Graph action</span><strong>${phase==='ready'?'':esc(state.working_state||'')}</strong></div><div data-object-id="result" class="g8-timeline-object g8-result ${phase==='result'&&!final?'is-visible':'is-hidden'}"><span>Result of this step</span><strong>${phase==='result'&&!final?esc(state.after_state||''):''}</strong></div><div data-object-id="verification" class="g8-timeline-object g8-verification ${final?'is-visible':'is-hidden'}"><span>Check the story and axes</span><strong>${final?esc(state.after_state||''):''}</strong></div></div></div></section>`;
    },destroy(){}
  });
})();
