/* Native Grade 11 plots: exact scene coefficients, sampled branches and staged marks. */
(() => {
  const esc=x=>escapeWhiteboardHtml(String(x??''));
  const f=x=>Number(x).toFixed(1);
  const stage=(state,phase)=>{
    const label=(state.annotations||[]).find(a=>/^stage:\d+$/.test(a));
    const n=Number(label?.slice(6)||0);
    return phase==='result'?n:Math.max(0,n-1);
  };
  const trig=(fn,x)=>Math[fn](x*Math.PI/180);
  function draw(scene,s){
    const v=scene.visual.values,mode=v.mode,isTrig=mode.startsWith('trig_');
    const xmin=isTrig?-360:-9,xmax=isTrig?360:9;
    const xscale=x=>45+470*(x-xmin)/(xmax-xmin);
    const maxY=mode==='secant'?Math.max(10,Math.abs(v.a*(v.x0+v.p)**2+v.q),Math.abs(v.a*(v.x1+v.p)**2+v.q))*1.25:
      mode==='quadratic'?12:mode==='exponential'?10:mode==='trig_two'?Math.max(3,Math.abs(v.a)*1.4):3;
    const minY=-maxY;
    const yscale=y=>186-155*y/maxY;
    const axes=`<line x1="45" y1="${f(yscale(0))}" x2="515" y2="${f(yscale(0))}" class="g11-fn-axis"/>
      <line x1="${f(xscale(0))}" y1="31" x2="${f(xscale(0))}" y2="341" class="g11-fn-axis"/>
      <text x="510" y="${f(yscale(0)+19)}">${isTrig?'360°':'x'}</text>
      <text x="45" y="${f(yscale(0)+19)}">${isTrig?'−360°':''}</text><text x="${f(xscale(0)+6)}" y="28">y</text>`;
    const point=(x,y,label)=>`<circle cx="${f(xscale(x))}" cy="${f(yscale(y))}" r="5" class="g11-fn-point"/><text x="${f(xscale(x)+7)}" y="${f(yscale(y)-10)}" class="g11-fn-label">${esc(label)}</text>`;
    const guide=(x,y,klass='g11-fn-guide')=>`<line x1="${f(xscale(x))}" y1="${f(yscale(0))}" x2="${f(xscale(x))}" y2="${f(yscale(y))}" class="${klass}"/>`;
    const text=(x,y,label)=>`<text x="${f(x)}" y="${f(y)}" class="g11-fn-note">${esc(label)}</text>`;
    function path(fn,klass){
      let segment='',paths='';const steps=isTrig?720:420;
      for(let i=0;i<=steps;i++){
        const x=xmin+(xmax-xmin)*i/steps,y=fn(x);
        if(!Number.isFinite(y)||Math.abs(y)>maxY*1.15){if(segment)paths+=`<path d="${segment}" class="${klass}"/>`;segment='';continue;}
        const px=f(xscale(x)),py=f(yscale(y));
        segment+=`${segment?' L':'M'} ${px} ${py}`;
      }
      if(segment)paths+=`<path d="${segment}" class="${klass}"/>`;
      return paths;
    }
    let base=()=>0,target=()=>0;
    if(mode==='quadratic'||mode==='secant'){
      base=x=>x*x;target=x=>v.a*(x+v.p)**2+v.q;
    }else if(mode==='hyperbola'){
      base=x=>1/x;target=x=>v.a/(x+v.p)+v.q;
    }else if(mode==='exponential'){
      base=x=>v.b**x;target=x=>v.a*v.b**(x+v.p)+v.q;
    }else{
      base=x=>trig(v.fn,x);
      target=x=>v.a!==undefined?v.a*trig(v.fn,(v.k||1)*x):trig(v.fn,(v.k||1)*(x+(v.p||0)));
    }
    let output=axes;
    if(s>=1)output+=path(base,'g11-fn-parent');
    if(s>=2)output+=path(target,'g11-fn-curve');
    if(s>=3){
      if(mode==='quadratic')output+=guide(-v.p,v.q)+point(-v.p,v.q,'turning point');
      if(mode==='hyperbola')output+=`<line x1="${f(xscale(-v.p))}" y1="31" x2="${f(xscale(-v.p))}" y2="341" class="g11-fn-asymptote"/><line x1="45" y1="${f(yscale(v.q))}" x2="515" y2="${f(yscale(v.q))}" class="g11-fn-asymptote"/>`;
      if(mode==='exponential')output+=guide(v.target_x,v.target_y)+point(v.target_x,v.target_y,'requested point');
      if(mode==='secant')output+=point(v.x0,v.y0,'A')+point(v.x1,v.y1,'B')+
        `<line x1="${f(xscale(v.x0))}" y1="${f(yscale(v.y0))}" x2="${f(xscale(v.x1))}" y2="${f(yscale(v.y1))}" class="g11-fn-secant"/>`;
      if(mode==='trig_point')output+=guide(v.theta,trig(v.fn,v.theta))+point(v.theta,trig(v.fn,v.theta),'θ');
      if(mode==='trig_frequency'||mode==='trig_two')output+=guide(0,0)+guide(v.period,0,'g11-fn-period');
      if(mode==='trig_shift')output+=guide(v.shift,0,'g11-fn-period');
    }
    if(s>=4){
      let label='';
      if(mode==='quadratic')label=`turning point (${v.vertex.join(', ')})`;
      if(mode==='hyperbola')label=`x = ${v.vertical}; y = ${v.horizontal}`;
      if(mode==='exponential')label=`f(${v.target_x}) = ${v.target_y}`;
      if(mode==='secant')label=`average gradient = ${v.slope}`;
      if(mode==='trig_point')label=`${v.fn}(${v.theta}°) = ${v.result}`;
      if(mode==='trig_frequency'||mode==='trig_two')label=`period = ${v.period}°`;
      if(mode==='trig_shift')label=`shift = ${v.shift}°`;
      output+=text(30,365,label);
    }
    return output;
  }
  function render(parameters,state,phase,n){
    const scene=JSON.parse(parameters.scene_json);
    if(scene.id!==parameters.question_id||scene.problem!==parameters.prompt||scene.lesson!==n||
       scene.visual?.family!=='grade11_functions')throw Error('Function graph belongs to another question');
    const s=stage(state,phase);
    return `<section class="g11-fn-board" data-managed-visibility="true" data-question-id="${esc(scene.id)}">
      <p data-object-id="problem">${esc(scene.problem)}</p>
      <div data-object-id="model" class="g11-fn-model"><svg viewBox="0 0 550 380" role="img" aria-label="${esc(scene.problem)}"><title>Question-specific function graph, step ${s} of 5</title>${draw(scene,s)}</svg></div>
      <p data-object-id="operation">${phase==='operation'?esc(state.working_state):''}</p>
      <p data-object-id="result">${phase==='result'&&s<5?esc(state.after_state):''}</p>
      <p data-object-id="verification">${phase==='result'&&s===5?esc(state.after_state):''}</p>
    </section>`;
  }
  for(let n=1;n<=8;n++)AthenaVisualizationRegistry.register('function_graph',`grade11_fn_${n}`,
    {render:(p,state,phase)=>render(p,state,phase,n),destroy(){}});
})();
