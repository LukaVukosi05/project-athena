/* Grade 9 pattern models: original figures remain; rule and result appear only when taught. */
(() => {
  const esc=x=>escapeWhiteboardHtml(String(x??''));
  const progress=(state,phase)=>{const mark=(state.annotations||[]).find(x=>/^stage:\d+$/.test(x))||'stage:0';
    const n=Number(mark.slice(6));return phase==='result'?n:Math.max(0,n-1)};
  const cell=(x,y)=>`<rect x="${x}" y="${y}" width="13" height="13" rx="2"/>`;
  const tileSvg=(kind,n,a,b)=>{
    const cells=[];let offset=0;
    for(let group=0;group<a;group++){
      if(kind==='square')for(let y=0;y<n;y++)for(let x=0;x<n;x++)cells.push(cell(offset+16*x,16*y));
      if(kind==='stair')for(let y=0;y<n;y++)for(let x=0;x<=y;x++)cells.push(cell(offset+16*x,16*y));
      if(kind==='border'){
        for(let x=0;x<=n;x++)cells.push(cell(offset+16*x,0));
        for(let y=1;y<=n;y++)cells.push(cell(offset,16*y));
      }
      offset+=(n+2)*16;
    }
    for(let i=0;i<Math.max(0,b);i++)cells.push(cell(offset+16*(i%5),16*Math.floor(i/5)));
    const width=Math.max(96,offset+Math.min(Math.max(b,0),5)*16+10);
    return `<svg viewBox="0 0 ${width} ${Math.max(72,16*Math.max(n,Math.ceil(Math.max(b,0)/5))+8)}" role="img" aria-label="Figure ${n}: ${cells.length} square tiles"><title>Figure ${n}, ${cells.length} tiles</title><g>${cells.join('')}</g></svg>`;
  };
  const model=(v,done)=>{
    const terms=v.known.map((value,i)=>`<div class="g9-pat-term" data-position="${i+1}"><small>Position ${i+1}</small>${v.family==='tiles'?tileSvg(v.kind,i+1,v.a,v.b):''}<strong>${esc(value)}</strong></div>`).join('');
    const changes=done>=2?`<div class="g9-pat-changes" data-object-id="changes"><small>Changes between positions</small><strong>${esc(v.differences.join('  →  '))}</strong>${v.differences.length>2?`<span>Changes of changes: ${esc(v.differences.slice(1).map((x,i)=>x-v.differences[i]).join('  →  '))}</span>`:''}</div>`:'<div data-object-id="changes"></div>';
    const claim=v.family==='diagnosis'?`<p class="g9-pat-claim">Learner’s claim: <strong>${esc(v.claim)}</strong>${done>=2?'<span> First incorrect output highlighted.</span>':''}</p>`:'';
    return `<div class="g9-pat-model" aria-label="Question-specific term positions and figures">${claim}<div class="g9-pat-row">${terms}</div>${changes}${done>=3?`<p class="g9-pat-rule" data-object-id="rule">Tested rule: ${esc(v.rule)}</p>`:'<p data-object-id="rule"></p>'}<p class="g9-pat-target" data-object-id="target">${v.family==='rule'||v.family==='diagnosis'?'':done>=3?`Position ${v.target}: ${esc(v.target_value)}`:`Position ${v.target}: ?`}</p></div>`;
  };
  for(let n=1;n<=5;n++)AthenaVisualizationRegistry.register('algebra',`grade9_pattern_${n}`,{
    render(params,state,phase){
      const scene=JSON.parse(params.scene_json),done=progress(state,phase),count=Number(params.total_steps);
      return `<section class="g9-pat-board" data-managed-visibility="true" data-question-id="${esc(params.question_id)}" data-phase="${esc(phase)}"><p class="g9-pat-question" data-object-id="problem">${esc(params.prompt)}</p><div class="g9-pat-visual" data-object-id="model">${model(scene.visual,done)}</div><p data-object-id="selection" class="g9-pat-answer">${done>=count-1?'Result: '+esc(scene.answer):''}</p><div class="g9-pat-action"><div data-object-id="operation">${phase==='operation'?esc(state.working_state):''}</div><div data-object-id="result">${phase==='result'&&done<count?esc(state.after_state):''}</div><div data-object-id="verification">${phase==='result'&&done===count?esc(state.after_state):''}</div></div></section>`;
    },destroy(){}
  });
})();
