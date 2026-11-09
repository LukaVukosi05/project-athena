/* Grade 11 quadratic models: mathematical givens and stage determine each SVG. */
(() => {
  const esc=value=>escapeWhiteboardHtml(String(value??""));
  const math=value=>typeof AthenaMathNotation!=="undefined"?AthenaMathNotation.html(value):esc(value);
  const line=(x1,y1,x2,y2,style="g11-ei-axis")=>`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" class="${style}"/>`;
  const label=(x,y,t)=>`<text x="${x}" y="${y}" class="g11-ei-label">${esc(t)}</text>`;
  const stage=(state,phase)=>{
    const match=(state.annotations||[]).find(x=>/^stage:\d+$/.test(x));
    const n=Number(match?.slice(6)||0);
    return phase==="result"?n:Math.max(0,n-1);
  };
  function graph(v,s){
    const x0=250,y0=167,scale=18;
    let svg=line(12,y0,488,y0)+line(x0,10,x0,315)+label(473,158,"x")+label(256,22,"y");
    for(let x=-10;x<=10;x+=2)svg+=line(x0+x*scale,y0-4,x0+x*scale,y0+4)+label(x0+x*scale-6,y0+23,x);
    const b=Number(v.b),c=Number(v.c);
    if(!Number.isFinite(b)||!Number.isFinite(c))return svg;
    if(s>=2){
      for(let x=-12;x<=12;x+=.1){
        const y=x*x+b*x+c,px=x0+x*scale,py=y0-y*scale;
        if(py<-35||py>345)continue;
        svg+=`<circle cx="${px.toFixed(1)}" cy="${py.toFixed(1)}" r="1.25" class="g11-ei-curve"/>`;
      }
    }
    if(v.mode==="intersection"&&s>=3){
      const m=Number(v.m),constant=Number(v.d);
      svg+=line(x0-12*scale,y0-(m*-12+constant)*scale,x0+12*scale,y0-(m*12+constant)*scale,"g11-ei-straight");
      if(s>=4){
        const diff=(b-m)*(b-m)-4*(c-constant);
        if(diff>=0)for(const x of [(-(b-m)-Math.sqrt(diff))/2,(-(b-m)+Math.sqrt(diff))/2]){
          const y=m*x+constant;
          svg+=`<circle cx="${(x0+x*scale).toFixed(1)}" cy="${(y0-y*scale).toFixed(1)}" r="6" class="g11-ei-root"/>`;
        }
      }
    }
    const discriminant=b*b-4*c;
    if(s>=3&&discriminant>=0&&v.mode!=="intersection"){
      for(const x of [(-b-Math.sqrt(discriminant))/2,(-b+Math.sqrt(discriminant))/2])
        svg+=`<circle cx="${(x0+x*scale).toFixed(1)}" cy="${y0}" r="5" class="g11-ei-root"/>`;
    }
    if(v.mode==="inequality"&&s>=4&&Number.isFinite(v.r)&&Number.isFinite(v.s)){
      const lower=x0+v.r*scale,upper=x0+v.s*scale;
      svg+=v.sign.includes("<")?line(lower,y0+40,upper,y0+40,"g11-ei-region"):
        line(12,y0+40,lower,y0+40,"g11-ei-region")+line(upper,y0+40,488,y0+40,"g11-ei-region");
      for(const x of [lower,upper])svg+=`<circle cx="${x}" cy="${y0+40}" r="5" class="g11-ei-${v.sign.includes("≤")||v.sign.includes("≥")?"closed":"open"}"/>`;
    }
    return svg;
  }
  function square(v,s){
    const h=Number(v.b)/2,c=Number(v.c);
    let svg=`<rect x="90" y="32" width="160" height="160" class="g11-ei-area"/>`+
      label(155,119,"x²")+label(105,230,`+ ${v.b}x ${c>=0?"+":"−"} ${Math.abs(c)}`);
    if(s>=2)svg+=`<rect x="250" y="32" width="105" height="160" class="g11-ei-add"/>`+label(265,116,`2 × ${h}x`);
    if(s>=3)svg+=`<rect x="355" y="32" width="105" height="160" class="g11-ei-corner"/>`+label(370,116,`(${h})²`);
    if(s>=4)svg+=label(110,273,`vertex x = ${-h}`);
    return svg;
  }
  function render(parameters,state,phase,number){
    const scene=JSON.parse(parameters.scene_json);
    if(scene.id!==parameters.question_id||scene.problem!==parameters.prompt||scene.lesson!==number||
       scene.visual?.family!=="grade11_equations")throw Error("Quadratic model does not match its question");
    const v=scene.visual.values,s=stage(state,phase);
    const view=v.mode==="square"?square(v,s):graph(v,s);
    return `<section class="g11-ei-board" data-managed-visibility="true" data-question-id="${esc(scene.id)}">
      <p data-object-id="problem">${math(scene.problem)}</p>
      <div data-object-id="model" class="g11-ei-model"><svg viewBox="0 0 500 330" role="img" aria-label="${esc(scene.problem)}">
        <title>Quadratic model at step ${s} of 5</title>${view}</svg></div>
      <p data-object-id="operation">${phase==="operation"?math(state.working_state):""}</p>
      <p data-object-id="result">${phase==="result"&&s<5?math(state.after_state):""}</p>
      <p data-object-id="verification">${phase==="result"&&s===5?math(state.after_state):""}</p>
    </section>`;
  }
  for(let n=1;n<=7;n++)AthenaVisualizationRegistry.register("algebra",`grade11_ei_${n}`,
    {render:(p,state,phase)=>render(p,state,phase,n),destroy(){}});
})();
