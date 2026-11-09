/* Exact angle mathematics with staged, question-owned unit-circle construction. */
(() => {
  const esc=value=>escapeWhiteboardHtml(String(value??""));
  const sin=a=>Math.sin(a*Math.PI/180),cos=a=>Math.cos(a*Math.PI/180);
  const c={x:245,y:165,r:118};
  const P=a=>({x:c.x+c.r*cos(a),y:c.y-c.r*sin(a)});
  const round=n=>Number(n).toFixed(1);
  const line=(x1,y1,x2,y2,klass="g11-tr-line")=>
    `<line x1="${round(x1)}" y1="${round(y1)}" x2="${round(x2)}" y2="${round(y2)}" class="${klass}"/>`;
  const label=(x,y,s,klass="g11-tr-label")=>
    `<text x="${round(x)}" y="${round(y)}" class="${klass}">${esc(s)}</text>`;
  const dot=(a,klass="g11-tr-dot")=>{const p=P(a);return `<circle cx="${round(p.x)}" cy="${round(p.y)}" r="5" class="${klass}"/>`;};
  const ray=(a,klass="g11-tr-ray")=>{const p=P(a);return line(c.x,c.y,p.x,p.y,klass)+dot(a);};
  const stage=(state,phase)=>{
    const tag=(state.annotations||[]).find(item=>/^stage:\d+$/.test(item));
    const index=Number(tag?.slice(6)||0);
    return phase==="result"?index:Math.max(0,index-1);
  };
  const circle=()=>`<circle cx="${c.x}" cy="${c.y}" r="${c.r}" class="g11-tr-circle"/>`+
    line(74,c.y,416,c.y,"g11-tr-axis")+line(c.x,18,c.x,312,"g11-tr-axis")+
    label(419,c.y+6,"0°")+label(c.x+6,26,"90°")+label(46,c.y+6,"180°")+label(c.x+6,313,"270°");
  function triangle(v,s){
    const p={x:330,y:55},left={x:90,y:255},right={x:330,y:255};
    let out=line(left.x,left.y,right.x,right.y)+line(right.x,right.y,p.x,p.y)+line(left.x,left.y,p.x,p.y);
    out+=label(78,281,"θ")+label(163,280,`adjacent ${v.adjacent}`);
    if(s>=1)out+=label(335,156,`opposite ${v.opposite}`);
    if(s>=2)out+=label(154,140,`hypotenuse ${v.hypotenuse}`);
    if(s>=3)out+=`<path d="M 316 255 L 316 239 L 330 239" class="g11-tr-right-angle"/>`;
    if(s>=4)out+=label(96,311,v.task==="tan"?"tan = sin ÷ cos":v.task==="cos"?"sin² + cos² = 1":"opposite² + adjacent² = hypotenuse²");
    return out;
  }
  function domain(v,s){
    let out=circle();
    if(s>=1)for(const a of v.angles||[])out+=dot(a)+label(P(a).x+5,P(a).y-8,`${a}°`);
    if(s>=3)for(const a of v.excluded||[]){
      const p=P(a);out+=line(p.x-9,p.y-9,p.x+9,p.y+9,"g11-tr-excluded")+
        line(p.x-9,p.y+9,p.x+9,p.y-9,"g11-tr-excluded");
    }
    if(s>=4)out+=label(25,327,"Crossed points make the denominator zero.");
    return out;
  }
  function reduction(v,s){
    let out=circle();
    if(s>=1)out+=ray(v.theta)+label(P(v.theta).x+8,P(v.theta).y-8,`${v.theta}°`);
    if(s>=2){
      const a=v.reference,point=P(a);
      out+=line(c.x,c.y,point.x,point.y,"g11-tr-reference")+dot(a,"g11-tr-reference-dot")+
        label(point.x+8,point.y-9,`reference ${a}°`);
    }
    if(s>=3&&Number.isFinite(v.theta)){
      const point=P(v.theta);
      out+=line(point.x,point.y,point.x,c.y,"g11-tr-projection")+
        line(point.x,point.y,c.x,point.y,"g11-tr-projection");
    }
    if(s>=4)out+=label(30,326,`${v.function} sign in quadrant ${v.quadrant}`);
    return out;
  }
  function solutions(v,s){
    let out=circle();
    if(s>=1&&Number.isFinite(v.reference))out+=ray(v.reference,"g11-tr-reference");
    if(s>=2&&Number.isFinite(v.reference)){
      const a=v.reference,positive=Number(v.sign)>0;
      const roots=v.function==="sin"?(positive?[a,180-a]:[180+a,360-a]):
        v.function==="cos"?(positive?[a,360-a]:[180-a,180+a]):
        positive?[a,180+a]:[180-a,360-a];
      for(const angle of roots)out+=ray(angle)+label(P(angle).x+8,P(angle).y-8,`${angle}°`);
      if(s>=3&&v.mode==="general")out+=label(18,327,`Period: ${v.function==="tan"?180:360}°; add integer multiples.`);
      if(s>=3&&v.mode==="interval")out+=label(20,327,`Keep 0° ≤ θ < ${v.upper}°.`);
    }
    return out;
  }
  function render(parameters,state,phase,number){
    const scene=JSON.parse(parameters.scene_json);
    if(scene.id!==parameters.question_id||scene.problem!==parameters.prompt||scene.lesson!==number||
       scene.visual?.family!=="grade11_trigonometry")throw Error("Trigonometry visual belongs to another question");
    const v=scene.visual.values,s=stage(state,phase);
    const svg=v.mode==="triangle"?triangle(v,s):v.mode==="domain"?domain(v,s):
      v.mode==="reduction"?reduction(v,s):solutions(v,s);
    return `<section class="g11-tr-board" data-managed-visibility="true" data-question-id="${esc(scene.id)}">
      <p data-object-id="problem">${esc(scene.problem)}</p>
      <div data-object-id="model" class="g11-tr-model"><svg viewBox="0 0 500 340" role="img" aria-label="${esc(scene.problem)}">
        <title>Trigonometry construction, step ${s} of 5</title>${svg}</svg></div>
      <p data-object-id="operation">${phase==="operation"?esc(state.working_state):""}</p>
      <p data-object-id="result">${phase==="result"&&s<5?esc(state.after_state):""}</p>
      <p data-object-id="verification">${phase==="result"&&s===5?esc(state.after_state):""}</p>
    </section>`;
  }
  for(let n=1;n<=7;n++)AthenaVisualizationRegistry.register("algebra",`grade11_tr_${n}`,
    {render:(p,state,phase)=>render(p,state,phase,n),destroy(){}});
})();
