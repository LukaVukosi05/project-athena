/* Labelled triangles reconstructed from each question's measurements. */
(() => {
  const esc=x=>escapeWhiteboardHtml(String(x??''));
  const f=x=>Number(x).toFixed(1);
  const rad=x=>x*Math.PI/180;
  function stage(state,phase){
    const mark=(state.annotations||[]).find(x=>/^stage:\d+$/.test(x));
    const n=Number(mark?.slice(6)||0);
    return phase==='result'?n:Math.max(0,n-1);
  }
  function shape(a,b,c,known,shift=0){
    const x=(c*c+a*a-b*b)/(2*a), h=Math.sqrt(Math.max(0,c*c-x*x));
    const scale=Math.min(270/Math.max(a,1),170/Math.max(h,1));
    const B=[85+shift,225],C=[85+shift+a*scale,225],A=[85+shift+x*scale,225-h*scale];
    const label=(p,dx,dy,s)=>`<text x="${f(p[0]+dx)}" y="${f(p[1]+dy)}">${esc(s)}</text>`;
    const line=(u,v,k='side')=>`<line x1="${f(u[0])}" y1="${f(u[1])}" x2="${f(v[0])}" y2="${f(v[1])}" class="g11-rules-${k}"/>`;
    let out=`${line(A,B)}${line(B,C)}${line(A,C)}${label(A,-5,-13,'A')}${label(B,-18,16,'B')}${label(C,6,16,'C')}`;
    out+=label([(B[0]+C[0])/2,230],0,14,known.a??'a');
    out+=label([(A[0]+C[0])/2,(A[1]+C[1])/2],5,-3,known.b??'b');
    out+=label([(A[0]+B[0])/2,(A[1]+B[1])/2],-27,-3,known.c??'c');
    if(known.A)out+=label(A,10,23,`${f(known.A)}°`);
    if(known.B)out+=label(B,16,-12,`${f(known.B)}°`);
    return {out,A,B,C};
  }
  function draw(scene,s){
    const v=scene.visual.values,mode=v.mode,proof=mode.startsWith('proof_');
    let a=v.a,b=v.b,c=v.c,A=v.A,B=v.B;
    if(proof){a=10;b=9;c=11;A=55;B=50;}
    else if(mode==='sine_side'){
      const angleC=180-A-B,c0=a*Math.sin(rad(angleC))/Math.sin(rad(A));
      b=a*Math.sin(rad(B))/Math.sin(rad(A));c=c0;
    }else if(mode==='ambiguous'){
      B=v.B1??Math.asin(b*Math.sin(rad(A))/a)*180/Math.PI;
      c=a*Math.sin(rad(180-A-B))/Math.sin(rad(A));
    }else if(mode==='cosine_side'){
      a=Math.sqrt(b*b+c*c-2*b*c*Math.cos(rad(A)));
    }else if(mode==='cosine_angle'){
      A=Math.acos((b*b+c*c-a*a)/(2*b*c))*180/Math.PI;
    }else if(mode==='area'){
      a=Math.sqrt(b*b+c*c-2*b*c*Math.cos(rad(A)));
    }
    const given={};
    if(!proof){
      if(mode==='sine_side')Object.assign(given,{a:`${v.a} cm`,A:v.A,B:v.B});
      if(mode==='ambiguous')Object.assign(given,{a:`${v.a} cm`,b:`${v.b} cm`,A:v.A});
      if(mode==='cosine_side')Object.assign(given,{b:`${v.b} cm`,c:`${v.c} cm`,A:v.A});
      if(mode==='cosine_angle')Object.assign(given,{a:`${v.a} cm`,b:`${v.b} cm`,c:`${v.c} cm`});
      if(mode==='area')Object.assign(given,{b:`${v.b} m`,c:`${v.c} m`,A:v.A});
    }
    const one=shape(a,b,c,given);
    let out=one.out;
    if(s>=1 && (proof||mode==='sine_side'||mode==='cosine_side'||mode==='area')){
      const p=one.A,q=one.C,r=one.B,ux=r[0]-p[0],uy=r[1]-p[1];
      const t=((q[0]-p[0])*ux+(q[1]-p[1])*uy)/(ux*ux+uy*uy);
      const foot=[p[0]+t*ux,p[1]+t*uy];
      out+=`<line x1="${f(q[0])}" y1="${f(q[1])}" x2="${f(foot[0])}" y2="${f(foot[1])}" class="g11-rules-altitude"/>`;
      out+=`<text x="${f(foot[0]+6)}" y="${f(foot[1]-7)}">h</text>`;
    }
    if(s>=1&&(mode==='cosine_angle'||mode==='ambiguous')){
      const p=mode==='cosine_angle'?one.A:one.B;
      out+=`<circle cx="${f(p[0])}" cy="${f(p[1])}" r="18" class="g11-rules-angle-mark"/>`;
      out+=`<text x="${f(p[0]+20)}" y="${f(p[1]-15)}">${mode==='ambiguous'?'B = ?':'A = ?'}</text>`;
    }
    if(mode==='ambiguous'&&s>=3){
      const B2=180-B,c2=a*Math.sin(rad(180-A-B2))/Math.sin(rad(A));
      const second=shape(a,b,c2,{a:`${v.a} cm`,b:`${v.b} cm`,A:v.A,B:B2},0);
      out+=`<g class="g11-rules-branch">${second.out}</g>`;
      out+=`<text x="32" y="32">Two valid positions for A: B₁ = ${f(B)}°, B₂ = ${f(B2)}°</text>`;
    }
    const rule=mode==='sine_side'||mode==='ambiguous'||mode==='proof_sine'?'a / sin A = b / sin B':
      mode==='area'||mode==='proof_area'?'Area = ½bc sin A':'a² = b² + c² − 2bc cos A';
    if(s>=2)out+=`<text x="22" y="280" class="g11-rules-rule">${esc(rule)}</text>`;
    if(s>=3){
      const substitution=mode==='sine_side'?`${v.a} / sin ${v.A}° = b / sin ${v.B}°`:
        mode==='ambiguous'?`sin B = ${v.b} sin ${v.A}° / ${v.a}`:
        mode==='cosine_side'?`a² = ${v.b}² + ${v.c}² − 2(${v.b})(${v.c}) cos ${v.A}°`:
        mode==='cosine_angle'?`cos A = (${v.b}² + ${v.c}² − ${v.a}²) / 2(${v.b})(${v.c})`:
        mode==='area'?`Area = ½(${v.b})(${v.c}) sin ${v.A}°`:'Use the altitude and the right triangles';
      out+=`<text x="22" y="300" class="g11-rules-rule">${esc(substitution)}</text>`;
    }
    if(s>=4&&!proof){
      const claim=mode==='ambiguous'?'Both B angles pass the triangle angle-sum check':'Calculate with full precision, then round once';
      out+=`<text x="22" y="320" class="g11-rules-rule">${esc(claim)}</text>`;
    }
    if(s>=5)out+=`<text x="22" y="340" class="g11-rules-answer">${esc(scene.answer)}</text>`;
    return out;
  }
  function render(parameters,state,phase,n){
    const scene=JSON.parse(parameters.scene_json);
    if(scene.id!==parameters.question_id||scene.problem!==parameters.prompt||scene.lesson!==n||scene.visual?.family!=='grade11_triangle_rules')throw Error('Triangle diagram belongs to another question');
    const s=stage(state,phase);
    return `<section class="g11-rules-board" data-managed-visibility="true" data-question-id="${esc(scene.id)}">
      <p data-object-id="problem">${esc(scene.problem)}</p>
      <div data-object-id="model" class="g11-rules-model"><svg viewBox="0 0 560 360" role="img" aria-label="${esc(scene.problem)}"><title>Question-specific triangle construction, step ${s} of 5</title>${draw(scene,s)}</svg></div>
      <p data-object-id="operation">${phase==='operation'?esc(state.working_state):''}</p>
      <p data-object-id="result">${phase==='result'&&s<5?esc(state.after_state):''}</p>
      <p data-object-id="verification">${phase==='result'&&s===5?esc(state.after_state):''}</p>
    </section>`;
  }
  for(let n=1;n<=5;n++)AthenaVisualizationRegistry.register('trigonometry',`grade11_rules_${n}`,
    {render:(p,state,phase)=>render(p,state,phase,n),destroy(){}});
})();
