/* Question-specific quadratic tables and figural tile constructions. */
(() => {
  const esc=value=>escapeWhiteboardHtml(String(value??''));
  const stage=(state,phase)=>{const n=Number((state.annotations||[]).find(x=>/^stage:\d+$/.test(x))?.slice(6)||0);return phase==='result'?n:Math.max(0,n-1)};
  const tag=(x,y,label,klass='')=>`<text x="${x}" y="${y}" class="${klass}">${esc(label)}</text>`;
  const rect=(x,y,w,h,klass='')=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="7" class="${klass}"/>`;
  function table(v,s){
    const t=v.terms,first=t.slice(1).map((value,i)=>value-t[i]),second=first.slice(1).map((value,i)=>value-first[i]);
    const a=second[0]/2,b=first[0]-3*a,c=t[0]-a-b;
    let out=tag(24,35,'Original terms','g11-pat-label');
    for(let k=0;k<5;k++){
      const x=123+k*96;
      out+=rect(x,10,86,44,'g11-pat-cell')+tag(x+8,38,`T${k+1} = ${t[k]}`);
      if(s>=2&&k<4)out+=tag(x+31,96,`${first[k]}`,'g11-pat-diff');
      if(s>=3&&k<3)out+=tag(x+75,145,`${second[k]}`,'g11-pat-second');
    }
    if(s>=2)out+=tag(24,96,'First differences','g11-pat-label');
    if(s>=3)out+=tag(24,178,`Constant second difference = ${second[0]} = 2a`,'g11-pat-label');
    if(s>=3)out+=tag(24,195,`a = ${a}`,'g11-pat-coeff');
    if(s>=4){
      out+=tag(140,195,`b = ${b}, c = ${c}`,'g11-pat-coeff');
      const sign=(n,k)=>n===0?'':n<0?`− ${Math.abs(n)}${k}`:`+ ${n}${k}`;
      out+=tag(24,239,`Tₙ = ${a}n² ${sign(b,'n')} ${sign(c,'')}`.replace(/\s+/g,' ').trim(),'g11-pat-rule');
    }
    if(s>=5)out+=tag(24,297,`Verify: T₅ = ${a}·25 + (${b})·5 + (${c}) = ${t[4]}`,'g11-pat-check');
    return out;
  }
  function figures(v,s){
    const q=v.columns_offset,extra=v.extra;
    let out='';
    for(let n=1;n<=3;n++){
      const x=28+(n-1)*196,y=20;out+=tag(x,y+14,`Figure ${n}`,'g11-pat-label');
      if(s>=1||n===1){
        for(let row=0;row<n;row++)for(let col=0;col<n+q;col++)out+=`<circle cx="${x+11+col*19}" cy="${y+43+row*19}" r="5" class="g11-pat-tile"/>`;
        for(let k=0;k<extra;k++)out+=`<circle cx="${x+11+k*19}" cy="${y+124}" r="5" class="g11-pat-extra"/>`;
      }
      if(s>=2)out+=tag(x,y+158,`${n}(${n+q}) + ${extra} = ${v.terms[n-1]}`,'g11-pat-count');
    }
    return out;
  }
  function render(p,state,phase,number){
    const scene=JSON.parse(p.scene_json);
    if(scene.lesson!==number||scene.id!==p.question_id||scene.problem!==p.prompt||scene.visual?.family!=='grade11_patterns')throw Error('Pattern diagram differs from this question');
    const v=scene.visual.values,s=stage(state,phase);
    // Figural diagrams occupy their own upper panel; the difference table remains beneath.
    const figure=v.mode==='figural';
    const visual=figure?`<svg viewBox="0 0 620 205" role="img" aria-label="Tile figures for this question">${figures(v,s)}</svg>`:'';
    const working=table(v,s);
    return `<section class="g11-pat-board" data-managed-visibility="true" data-question-id="${esc(scene.id)}"><p data-object-id="problem">${esc(scene.problem)}</p>
      <div data-object-id="model" class="g11-pat-model">${visual}<svg viewBox="0 0 620 325" role="img" aria-label="Difference table stage ${s} of 5"><title>Quadratic pattern terms and differences</title>${working}</svg></div>
      <p data-object-id="operation">${phase==='operation'?esc(state.working_state):''}</p>
      <p data-object-id="result">${phase==='result'&&s<5?esc(state.after_state):''}</p>
      <p data-object-id="verification">${phase==='result'&&s===5?esc(state.after_state):''}</p></section>`;
  }
  for(let n=1;n<=5;n++)AthenaVisualizationRegistry.register('algebra',`grade11_pat_${n}`,{render:(p,s,phase)=>render(p,s,phase,n),destroy(){}});
})();
