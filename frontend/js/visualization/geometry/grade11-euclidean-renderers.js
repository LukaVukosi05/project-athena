/* Question-owned Euclidean constructions. Chords and tangent contact points are geometric. */
(() => {
  const esc=value=>escapeWhiteboardHtml(String(value??""));
  const C={x:238,y:166,r:113};
  const P=angle=>({x:C.x+C.r*Math.cos(angle*Math.PI/180),
                   y:C.y-C.r*Math.sin(angle*Math.PI/180)});
  const f=n=>Number(n).toFixed(1);
  const line=(a,b,klass="g11-euc-line")=>
    `<line x1="${f(a.x)}" y1="${f(a.y)}" x2="${f(b.x)}" y2="${f(b.y)}" class="${klass}"/>`;
  const point=(id,a,label)=>`<circle cx="${f(a.x)}" cy="${f(a.y)}" r="4.5" class="g11-euc-point"/>`+
    `<text x="${f(a.x+7)}" y="${f(a.y-7)}" class="g11-euc-label" data-object-id="${id}">${esc(label)}</text>`;
  const note=(x,y,label,klass="g11-euc-note")=>`<text x="${f(x)}" y="${f(y)}" class="${klass}">${esc(label)}</text>`;
  const circle=()=>`<circle cx="${C.x}" cy="${C.y}" r="${C.r}" class="g11-euc-circle"/>`;
  const stage=(state,phase)=>{
    const match=(state.annotations||[]).find(a=>/^stage:\d+$/.test(a));
    const n=Number(match?.slice(6)||0);
    return phase==="result"?n:Math.max(0,n-1);
  };
  function chord(v,s){
    const r=Number(v.radius),d=Number(v.distance);
    const cy=C.y+C.r*d/r,dx=C.r*Math.sqrt(1-(d/r)**2);
    const a={x:C.x-dx,y:cy},b={x:C.x+dx,y:cy},m={x:C.x,y:cy};
    let out=circle()+line(a,b)+line(C,a,"g11-euc-radius")+
      point("A",a,"A")+point("B",b,"B")+point("O",C,"O")+point("M",m,"M")+
      note(16,35,`OA = ${r} cm, OM = ${d} cm`);
    if(s>=1)out+=line(C,m,"g11-euc-perpendicular")+
      `<path d="M ${f(m.x)} ${f(m.y-12)} h -12 v 12" class="g11-euc-right"/>`;
    if(s>=2)out+=line(C,b,"g11-euc-radius");
    if(s>=3)out+=note(a.x+12,cy-9,`AM = ${v.half} cm`,"g11-euc-derived");
    if(s>=4)out+=note(b.x+10,cy+25,`AB = ${Number(v.half)*2} cm`,"g11-euc-derived");
    return out;
  }
  function chordAngles(v,s){
    const a=P(270-v.central/2),b=P(270+v.central/2),top=P(90),bottom=P(270);
    let out=circle()+line(C,a,"g11-euc-radius")+line(C,b,"g11-euc-radius")+
      point("O",C,"O")+point("A",a,"A")+point("B",b,"B")+
      point("C",top,"C")+note(14,35,`∠AOB = ${v.central}°`);
    if(s>=2)out+=line(top,a)+line(top,b);
    if(v.mode==="centre_cyclic"){
      out+=point("D",bottom,"D");
      if(s>=3)out+=line(bottom,a,"g11-euc-highlight")+line(bottom,b,"g11-euc-highlight");
    }
    if(s>=3)out+=note(top.x+16,top.y+24,`∠ACB = ${v.central/2}°`,"g11-euc-derived");
    if(s>=4&&v.mode==="centre_cyclic")out+=note(bottom.x+18,bottom.y-19,
      `∠ADB = ${180-v.central/2}°`,"g11-euc-derived");
    return out;
  }
  function sameSegment(v,s){
    const a=P(270-v.inscribed),b=P(270+v.inscribed),c=P(125),d=P(55);
    let out=circle()+line(a,b)+point("A",a,"A")+point("B",b,"B")+
      point("C",c,"C")+point("D",d,"D")+note(15,35,`∠ACB = ${v.inscribed}°`);
    if(s>=1)out+=line(c,a)+line(c,b);
    if(s>=2)out+=line(d,a)+line(d,b,"g11-euc-highlight");
    if(s>=3)out+=note(185,141,"same chord AB","g11-euc-derived");
    if(s>=4)out+=note(d.x-95,d.y+34,`∠ADB = ${v.inscribed}°`,"g11-euc-derived");
    return out;
  }
  function cyclic(v,s){
    const t=90-Number(v.given);
    const a=P(90),b=P(180+t),c=P(270),d=P(360-t);
    let out=circle()+line(a,b)+line(b,c)+line(c,d)+line(d,a)+
      point("A",a,"A")+point("B",b,"B")+point("C",c,"C")+point("D",d,"D")+
      note(15,35,`∠BAD = ${v.given}°`);
    if(s>=2)out+=line(c,b,"g11-euc-highlight")+line(c,d,"g11-euc-highlight");
    if(s>=3)out+=note(16,311,"Opposite cyclic angles add to 180°.");
    if(s>=4)out+=note(c.x+22,c.y-22,`∠BCD = ${180-v.given}°`,"g11-euc-derived");
    return out;
  }
  function tangents(v,s){
    const o={x:205,y:167},R=96,d=R*Number(v.external)/Number(v.radius);
    const p={x:o.x+d,y:o.y},t=R*R/d,dy=R*Math.sqrt(1-(R/d)**2);
    const a={x:o.x+t,y:o.y-dy},b={x:o.x+t,y:o.y+dy};
    let out=`<circle cx="${o.x}" cy="${o.y}" r="${R}" class="g11-euc-circle"/>`+
      line(o,p,"g11-euc-guide")+line(p,a)+line(p,b)+line(o,a,"g11-euc-radius")+
      point("O",o,"O")+point("P",p,"P")+point("A",a,"A")+point("B",b,"B")+
      note(15,35,`OP = ${v.external} cm; OA = ${v.radius} cm`);
    if(s>=1){
      const u={x:(o.x-a.x)/R,y:(o.y-a.y)/R};
      const length=Math.hypot(p.x-a.x,p.y-a.y);
      const w={x:(p.x-a.x)/length,y:(p.y-a.y)/length};
      const q=(i,j)=>`${f(a.x+12*u.x*i+12*w.x*j)} ${f(a.y+12*u.y*i+12*w.y*j)}`;
      out+=`<path d="M ${q(1,0)} L ${q(1,1)} L ${q(0,1)}" class="g11-euc-right"/>`;
    }
    if(s>=2)out+=line(o,b,"g11-euc-radius");
    if(s>=3)out+=note(297,102,`PA = ${v.tangent} cm`,"g11-euc-derived");
    if(s>=4)out+=note(297,274,`PB = ${v.tangent} cm`,"g11-euc-derived");
    return out;
  }
  function tangentChord(v,s){
    const g=Number(v.given),a=P(0),b=P(2*g),c=P(250),d=P(g);
    const tangentTop={x:a.x,y:20};
    let out=circle()+line(a,tangentTop,"g11-euc-tangent")+line(a,b)+
      point("A",a,"A")+point("B",b,"B")+point("C",c,"C")+
      note(12,35,`tangent–chord angle = ${g}°`);
    if(s>=1)out+=line(C,a,"g11-euc-radius");
    if(s>=2)out+=line(c,a)+line(c,b,"g11-euc-highlight");
    if(v.mode==="tangent_cyclic"){
      out+=point("D",d,"D");
      if(s>=3)out+=line(d,a,"g11-euc-highlight")+line(d,b,"g11-euc-highlight");
    }
    if(s>=3)out+=note(c.x+14,c.y-10,`∠ACB = ${g}°`,"g11-euc-derived");
    if(s>=4&&v.mode==="tangent_cyclic")out+=note(d.x-100,d.y+30,
      `∠ADB = ${180-g}°`,"g11-euc-derived");
    return out;
  }
  function render(parameters,state,phase,n){
    const scene=JSON.parse(parameters.scene_json),v=scene.visual?.values;
    if(scene.id!==parameters.question_id||scene.problem!==parameters.prompt||scene.lesson!==n||
       scene.visual?.family!=="grade11_euclidean")throw Error("Circle diagram belongs to a different problem");
    const s=stage(state,phase);
    const svg=v.mode==="chord"?chord(v,s):v.mode==="tangents"?tangents(v,s):
      v.mode==="cyclic"?cyclic(v,s):v.mode==="same_segment"?sameSegment(v,s):
      v.mode==="centre"||v.mode==="centre_cyclic"?chordAngles(v,s):tangentChord(v,s);
    return `<section class="g11-euc-board" data-managed-visibility="true" data-question-id="${esc(scene.id)}">
      <p data-object-id="problem">${esc(scene.problem)}</p>
      <div data-object-id="model" class="g11-euc-model"><svg viewBox="0 0 500 335" role="img" aria-label="${esc(scene.problem)}">
        <title>Circle theorem construction, step ${s} of 5</title>${svg}</svg></div>
      <p data-object-id="operation">${phase==="operation"?esc(state.working_state):""}</p>
      <p data-object-id="result">${phase==="result"&&s<5?esc(state.after_state):""}</p>
      <p data-object-id="verification">${phase==="result"&&s===5?esc(state.after_state):""}</p>
    </section>`;
  }
  for(let n=1;n<=8;n++)AthenaVisualizationRegistry.register("geometry",`grade11_euc_${n}`,
    {render:(p,state,phase)=>render(p,state,phase,n),destroy(){}});
})();
