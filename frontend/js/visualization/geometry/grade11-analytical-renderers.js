/* Coordinate geometry: scene-specific plots, permanent constructions, staged solutions. */
(() => {
  const esc=value=>escapeWhiteboardHtml(String(value??""));
  const num=x=>Number(String(x).replace('−','-').split('/')[0]) / (String(x).includes('/') ? Number(String(x).split('/')[1]) : 1);
  const f=x=>Number(x).toFixed(1);
  const stage=(state,phase)=>{
    const key=(state.annotations||[]).find(a=>/^stage:\d+$/.test(a));
    const n=Number(key?.slice(6)||0);
    return phase==='result'?n:Math.max(0,n-1);
  };
  function sceneGraph(scene,s){
    const v=scene.visual.values,mode=v.mode;
    const a=v.a?.map(num),b=v.b?.map(num),p=v.p?.map(num),mid=v.mid?.map(num);
    const values=[a,b,p,mid].filter(Boolean).flat();
    const xs=[0,...[a,b,p,mid].filter(Boolean).map(q=>q[0])];
    const ys=[0,...[a,b,p,mid].filter(Boolean).map(q=>q[1])];
    const extent=Math.max(7,...values.map(Math.abs))*1.25;
    const bound=extent<16?16:Math.ceil(extent/5)*5;
    const X=x=>270+225*x/bound,Y=y=>182-145*y/bound;
    const pt=(q,label,klass='')=>`<circle cx="${f(X(q[0]))}" cy="${f(Y(q[1]))}" r="5" class="g11-ag-point ${klass}"/><text x="${f(X(q[0])+(X(q[0])>380?-8:7))}" y="${f(Y(q[1])-9)}" text-anchor="${X(q[0])>380?'end':'start'}" class="g11-ag-label">${esc(label)} (${esc(q[0])}, ${esc(q[1])})</text>`;
    const line=(u,w,klass='g11-ag-segment')=>`<line x1="${f(X(u[0]))}" y1="${f(Y(u[1]))}" x2="${f(X(w[0]))}" y2="${f(Y(w[1]))}" class="${klass}"/>`;
    const note=(x,y,t)=>`<text x="${f(x)}" y="${f(y)}" class="g11-ag-note">${esc(t)}</text>`;
    let svg=`<line x1="40" y1="${f(Y(0))}" x2="500" y2="${f(Y(0))}" class="g11-ag-axis"/>
      <line x1="${f(X(0))}" y1="25" x2="${f(X(0))}" y2="345" class="g11-ag-axis"/>
      <text x="506" y="${f(Y(0)+5)}">x</text><text x="${f(X(0)+6)}" y="20">y</text>
      <text x="42" y="${f(Y(0)+18)}">−${bound}</text><text x="475" y="${f(Y(0)+18)}">${bound}</text>
      <text x="${f(X(0)+7)}" y="34">${bound}</text><text x="${f(X(0)+7)}" y="340">−${bound}</text>`;
    if(mode==='inclination'){
      svg+=pt(p,'P')+line(p,[p[0]+Math.min(6,bound/3),p[1]],'g11-ag-guide');
      if(s>=2){const angle=v.theta*Math.PI/180,d=Math.min(6,bound/3);
        svg+=line(p,[p[0]+d*Math.cos(angle),p[1]+d*Math.sin(angle)],'g11-ag-derived');}
      if(s>=3)svg+=note(330,45,`tan θ = ${v.m}`);
      if(s>=4)svg+=note(330,68,`θ = ${v.theta}°`);
      return svg;
    }
    svg+=pt(a,'A');
    if(!(mode==='midpoint'&&v.missing&&s<3))svg+=pt(b,'B');
    if(mode==='parallel_perpendicular')svg+=pt(p,'P');
    if(mode==='midpoint'){
      if(v.missing)svg+=pt(mid,'M','g11-ag-midpoint');
      if(s>=1 && !v.missing)svg+=line(a,b);
      if(s>=2 && !v.missing)svg+=pt(mid,'M','g11-ag-midpoint');
      if(s>=3 && v.missing)svg+=line(a,b);
      if(s>=4)svg+=note(335,45,v.missing?`B = (${v.b.join(', ')})`:`M = (${v.mid.join(', ')})`);
      return svg;
    }
    if(s>=1)svg+=line(a,b);
    if(s>=2){
      const corner=[b[0],a[1]];
      svg+=line(a,corner,'g11-ag-guide')+line(corner,b,'g11-ag-guide');
      svg+=note(335,45,`Δx = ${b[0]-a[0]}; Δy = ${b[1]-a[1]}`);
    }
    if(mode==='distance' && s>=4)svg+=note(335,69,`AB = ${v.length} units`);
    if(mode==='gradient' && s>=4)svg+=note(335,69,`m = ${v.m}`);
    if(mode==='equation' && s>=3){
      const m=num(v.m),c=num(v.c);
      svg+=line([-bound,m*(-bound)+c],[bound,m*bound+c],'g11-ag-derived');
      if(s>=4)svg+=note(335,69,`y = ${v.m}x + (${v.c})`);
    }
    if(mode==='parallel_perpendicular' && s>=3){
      const m=num(v.target_m),c=num(v.c);
      svg+=line([-bound,m*(-bound)+c],[bound,m*bound+c],'g11-ag-derived');
      if(s>=4)svg+=note(335,69,`mnew = ${v.target_m}`);
    }
    return svg;
  }
  function render(parameters,state,phase,n){
    const scene=JSON.parse(parameters.scene_json);
    if(scene.id!==parameters.question_id||scene.problem!==parameters.prompt||scene.lesson!==n||
       scene.visual?.family!=='grade11_analytical')throw Error('Coordinate plot belongs to a different question');
    const s=stage(state,phase);
    return `<section class="g11-ag-board" data-managed-visibility="true" data-question-id="${esc(scene.id)}">
      <p data-object-id="problem">${esc(scene.problem)}</p>
      <div data-object-id="model" class="g11-ag-model"><svg viewBox="0 0 540 370" role="img" aria-label="${esc(scene.problem)}"><title>Coordinate construction, step ${s} of 5</title>${sceneGraph(scene,s)}</svg></div>
      <p data-object-id="operation">${phase==='operation'?esc(state.working_state):''}</p>
      <p data-object-id="result">${phase==='result'&&s<5?esc(state.after_state):''}</p>
      <p data-object-id="verification">${phase==='result'&&s===5?esc(state.after_state):''}</p>
    </section>`;
  }
  for(let n=1;n<=6;n++)AthenaVisualizationRegistry.register('coordinate_geometry',`grade11_ag_${n}`,
    {render:(p,state,phase)=>render(p,state,phase,n),destroy(){}});
})();
