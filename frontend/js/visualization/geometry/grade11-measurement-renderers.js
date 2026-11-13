/* Question-owned solid constructions and exposed-face reasoning. */
(() => {
 const esc=x=>escapeWhiteboardHtml(String(x??''));
 const stage=(state,phase)=>{const n=Number((state.annotations||[]).find(x=>/^stage:\d+$/.test(x))?.slice(6)||0);return phase==='result'?n:Math.max(0,n-1)};
 const text=(x,y,t,klass='')=>`<text x="${x}" y="${y}" class="${klass}">${esc(t)}</text>`;
 const line=(x1,y1,x2,y2,klass='')=>`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" class="${klass}"/>`;
 const ellipse=(x,y,rx,ry,klass='')=>`<ellipse cx="${x}" cy="${y}" rx="${rx}" ry="${ry}" class="${klass}"/>`;
 function prism(v,s){
  const x=185,y=100,dx=80+Math.min(70,v.l*5),dy=55+Math.min(35,v.w*4),height=85+Math.min(85,v.h*5);
  let out=`<polygon points="${x},${y} ${x+dx},${y} ${x+dx+dy},${y-30} ${x+dy},${y-30}" class="g11-meas-top"/>`;
  out+=`<polygon points="${x},${y} ${x+dx},${y} ${x+dx},${y+height} ${x},${y+height}" class="g11-meas-front"/>`;
  out+=`<polygon points="${x+dx},${y} ${x+dx+dy},${y-30} ${x+dx+dy},${y+height-30} ${x+dx},${y+height}" class="g11-meas-side"/>`;
  if(s>=1)out+=text(x+dx/3,y+height+26,`${v.l} cm`)+text(x+dx+dy+8,y+height/2,`${v.w} cm`)+text(x-60,y+height/2,`${v.h} cm`);
  if(s>=2)out+=text(20,300,v.mode==='scale'?v.all_dimensions?`All lengths × ${v.k}`:`Height only × ${v.k}`:'Six faces: three pairs','g11-meas-reason');
  if(v.mode==='scale'&&s>=2){
   const dims=v.all_dimensions?[v.l*v.k,v.w*v.k,v.h*v.k]:[v.l,v.w,v.h*v.k];
   const fx=v.all_dimensions?1+.14*(v.k-1):1,fy=1+.14*(v.k-1);
   const wide=dx*fx,tall=height*fy;
   out+=`<path d="M${x} ${y} H${x+wide} V${y+tall} H${x} Z" class="g11-meas-scaled-outline"/>`;
   out+=text(300,330,`New dimensions: ${dims.join(' × ')} cm`,'g11-meas-reason');
   out+=text(20,342,'Schematic outlines; use labelled dimensions for calculations.','g11-meas-sketch-note');
  }
  return out;
 }
 function triangularPrism(v,s){
  const ax=205,ay=265,bx=ax+v.a*8,cy=ay-v.b*5,shift=75+v.length*3,rise=-38;
  const front=`${ax},${ay} ${bx},${ay} ${ax},${cy}`;
  const back=`${ax+shift},${ay+rise} ${bx+shift},${ay+rise} ${ax+shift},${cy+rise}`;
  let out=`<polygon points="${ax},${cy} ${bx},${ay} ${bx+shift},${ay+rise} ${ax+shift},${cy+rise}" class="g11-meas-side"/>`;
  out+=`<polygon points="${ax},${ay} ${bx},${ay} ${bx+shift},${ay+rise} ${ax+shift},${ay+rise}" class="g11-meas-top"/>`;
  out+=`<polygon points="${front}" class="g11-meas-face"/>`;
  out+=`<polygon points="${back}" class="g11-meas-back"/>`;
  if(s>=1)out+=text(bx-24,ay+27,`${v.a} cm`)+text(ax-75,(ay+cy)/2,`${v.b} cm`)+text(bx+shift+8,cy+20,`${v.hyp} cm hyp.`)+text(ax+shift,ay+rise+46,`length ${v.length} cm`);
  if(s>=2)out+=text(20,325,'Two triangular ends + three rectangular side faces','g11-meas-reason');
  return out;
 }
 function cylinder(v,s,part='plain'){
  const r=v.r,rx=42+Math.min(25,r*3),top=part==='plain'?85:160,bottom=top+85+Math.min(65,v.h*5),x=310;
  let out=`<path d="M${x-rx} ${top} V${bottom} A${rx} 20 0 0 0 ${x+rx} ${bottom} V${top}" class="g11-meas-outline"/>`;
  out+=ellipse(x,top,rx,20,part==='plain'?'g11-meas-face':'g11-meas-join');
  out+=ellipse(x,bottom,rx,20,'g11-meas-face');
  if(s>=1)out+=text(x-18,top-30,`r = ${r} cm`)+text(x+rx+10,(top+bottom)/2,`h = ${v.h} cm`);
  if(s>=2)out+=text(20,325,part==='plain'?'Curved side + two exposed circular ends':'Shared top circle hidden; bottom base exposed','g11-meas-reason');
  return out;
 }
 function sphere(v,s){
  const x=310,y=170,rad=65+Math.min(38,v.r*2);
  let out=`<circle cx="${x}" cy="${y}" r="${rad}" class="g11-meas-face"/>`;
  out+=`<path d="M${x-rad} ${y} A${rad} 23 0 0 0 ${x+rad} ${y}" class="g11-meas-outline"/>`;
  if(s>=1)out+=line(x,y,x+rad,y,'g11-meas-radius')+text(x+rad/3,y-9,`r = ${v.r} cm`);
  if(s>=2)out+=text(20,325,'One curved exposed surface; volume uses r³','g11-meas-reason');
  return out;
 }
 function cone(v,s,part='plain'){
  const x=310,top=part==='plain'?62:42,base=part==='plain'?255:160,rx=43+Math.min(30,v.r*3);
  let out=`<path d="M${x} ${top} L${x-rx} ${base} A${rx} 18 0 0 0 ${x+rx} ${base} Z" class="g11-meas-front"/>`;
  out+=ellipse(x,base,rx,18,part==='plain'?'g11-meas-face':'g11-meas-join');
  if(s>=1){out+=line(x,top,x,base,'g11-meas-height')+line(x,base,x+rx,base,'g11-meas-radius');out+=text(x+rx+12,base-72,`h = ${part==='plain'?v.h:v.cone_h} cm`)+text(x+rx/3,base+35,`r = ${v.r} cm`);}
  if(s>=2)out+=text(20,330,part==='plain'?'Slant is √(r² + h²); closed base exposed':'Cone base hidden at the join; curved side exposed','g11-meas-reason');
  return out;
 }
 function stacked(v,s){
  let out=cylinder(v,s,'stacked');
  if(v.mode==='hemisphere_cylinder'){
   const rx=42+Math.min(25,v.r*3),x=310,y=160;
   out+=`<path d="M${x-rx} ${y} A${rx} ${55+v.r*2} 0 0 1 ${x+rx} ${y}" class="g11-meas-cap"/>`;
   if(s>=2)out+=text(20,302,'Hemisphere cap: curved area only','g11-meas-reason');
  }else out+=cone(v,s,'stacked');
  return out;
 }
 function render(p,state,phase,number){
  const scene=JSON.parse(p.scene_json);
  if(scene.lesson!==number||scene.id!==p.question_id||scene.problem!==p.prompt||scene.visual?.family!=='grade11_measurement')throw Error('Measurement solid belongs to another question');
  const v=scene.visual.values,s=stage(state,phase);
  const visual=['prism','scale'].includes(v.mode)?prism(v,s):v.mode==='triangular_prism'?triangularPrism(v,s):v.mode==='cylinder'?cylinder(v,s):v.mode==='sphere'?sphere(v,s):v.mode==='cone'?cone(v,s):stacked(v,s);
  return `<section class="g11-meas-board" data-managed-visibility="true" data-question-id="${esc(scene.id)}"><p data-object-id="problem">${esc(scene.problem)}</p>
    <div data-object-id="model" class="g11-meas-model"><svg viewBox="0 0 620 350" role="img" aria-label="${esc(v.mode)} solid using the question dimensions, stage ${s} of 5"><title>Question-specific measurement construction</title>${visual}</svg></div>
    <p data-object-id="operation">${phase==='operation'?esc(state.working_state):''}</p>
    <p data-object-id="result">${phase==='result'&&s<5?esc(state.after_state):''}</p>
    <p data-object-id="verification">${phase==='result'&&s===5?esc(state.after_state):''}</p></section>`;
 }
 for(let n=1;n<=4;n++)AthenaVisualizationRegistry.register('geometry',`grade11_meas_${n}`,{render:(p,s,phase)=>render(p,s,phase,n),destroy(){}});
})();
