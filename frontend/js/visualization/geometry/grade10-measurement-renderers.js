(function(){
 const esc=x=>escapeWhiteboardHtml(String(x));
 const stage=s=>Math.max(1,Math.min(5,Number((s.annotations||[]).find(x=>/^stage:\d+$/.test(x))?.split(':')[1]||1)));
 const t=(id,x,y,value)=>`<text data-object-id="${id}" x="${x}" y="${y}" class="g10m-text">${esc(value)}</text>`;
 function prism(v,k){
  const a=Number(v.a),b=Number(v.b),h=Number(v.h),A=k>=2&&v.scaled_a?Number(v.scaled_a):a,B=k>=2&&v.scaled_b?Number(v.scaled_b):b,H=k>=2&&v.scaled_h?Number(v.scaled_h):h;
  const w=Math.min(190,72+A*10),depth=Math.min(90,28+B*5),height=Math.min(160,55+H*7),x=170,y=235,dx=depth,dy=-depth*.45;
  let out=`<polygon data-object-id="front-face" points="${x},${y} ${x+w},${y} ${x+w},${y-height} ${x},${y-height}" class="g10m-face ${k>=4?'g10m-focus':''}"/>`;
  out+=`<polygon data-object-id="top-face" points="${x},${y-height} ${x+dx},${y-height+dy} ${x+w+dx},${y-height+dy} ${x+w},${y-height}" class="g10m-face ${k>=2?'g10m-focus':''}"/>`;
  out+=`<polygon data-object-id="side-face" points="${x+w},${y} ${x+w+dx},${y+dy} ${x+w+dx},${y-height+dy} ${x+w},${y-height}" class="g10m-face ${k>=4?'g10m-focus':''}"/>`;
  out+=t('length-label',x+w/3,y+25,`${A} cm`)+t('width-label',x+w+dx-10,y+10,`${B} cm`)+t('height-label',x-55,y-height/2,`${H} cm`);
  if(k>=2&&v.scale)out+=t('scale-label',x+10,300,v.one_dimension?`Length × ${v.scale}; width and height unchanged`:`All dimensions × ${v.scale}`);
  return out;
 }
 function cylinder(v,k,composite){
  const r=Number(v.r),h=Number(v.h),w=Math.min(190,70+r*11),height=Math.min(140,48+h*6),x=260,y=240,rx=w/2,ry=23,top=y-height;
  let out=`<path data-object-id="curved-wall" d="M${x-rx} ${top} L${x-rx} ${y} A${rx} ${ry} 0 0 0 ${x+rx} ${y} L${x+rx} ${top}" class="g10m-face ${k>=4?'g10m-focus':''}"/>`;
  out+=`<ellipse data-object-id="bottom-disc" cx="${x}" cy="${y}" rx="${rx}" ry="${ry}" class="g10m-disc ${k>=4?'g10m-focus':''}"/>`;
  if(composite){out+=`<path data-object-id="hemisphere" d="M${x-rx} ${top} A${rx} ${rx*.75} 0 0 1 ${x+rx} ${top}" class="g10m-curve ${k>=3?'g10m-focus':''}"/>`;
   if(k>=2)out+=`<ellipse data-object-id="internal-join" cx="${x}" cy="${top}" rx="${rx}" ry="${ry}" class="g10m-join"/>`;
  }else out+=`<ellipse data-object-id="top-disc" cx="${x}" cy="${top}" rx="${rx}" ry="${ry}" class="g10m-disc ${k>=4&&!v.open_top?'g10m-focus':''} ${v.open_top?'g10m-open':''}"/>`;
  out+=`<line data-object-id="radius" x1="${x}" y1="${y}" x2="${x+rx}" y2="${y}" class="g10m-dimension"/>`+t('radius-label',x+rx/3,y-4,`r = ${r} cm`)+t('height-label',x-rx-100,top+height/2,`h = ${h} cm`);
  if(k>=4)out+=t('surface-rule',80,320,composite?'Internal join excluded; outside bottom included':v.open_top?'Top open: count wall and bottom only':'Closed: count wall and both discs');
  return out;
 }
 function sphere(v,k){const r=Number(v.r),hemi=v.shape==='hemisphere',cx=260,cy=165,rad=Math.min(110,55+r*3);
  let out=hemi?`<path data-object-id="curved-hemisphere" d="M${cx-rad} ${cy} A${rad} ${rad} 0 0 1 ${cx+rad} ${cy}" class="g10m-curve ${k>=4?'g10m-focus':''}"/><ellipse data-object-id="flat-base" cx="${cx}" cy="${cy}" rx="${rad}" ry="17" class="g10m-disc ${k>=4?'g10m-focus':''}"/>`:`<circle data-object-id="sphere" cx="${cx}" cy="${cy}" r="${rad}" class="g10m-face ${k>=4?'g10m-focus':''}"/><ellipse data-object-id="equator" cx="${cx}" cy="${cy}" rx="${rad}" ry="${rad/4}" class="g10m-join"/>`;
  out+=`<line data-object-id="radius" x1="${cx}" y1="${cy}" x2="${cx+rad}" y2="${cy}" class="g10m-dimension"/>`+t('radius-label',cx+20,cy-8,`r = ${r} cm`);
  if(k>=4&&hemi)out+=t('base-inclusion',110,315,'Curved half-sphere + flat circular base');
  return out;
 }
 function apex(v,k){const cone=v.shape==='cone',r=Number(v.r||v.b/2),h=Number(v.h),slant=Number(v.slant),cx=265,top=54,base=Math.min(120,50+r*5),bottom=Math.min(245,top+90+h*6);
  let out=`<path data-object-id="sloped-face" d="M${cx} ${top} L${cx-base} ${bottom} A${base} 22 0 0 0 ${cx+base} ${bottom} Z" class="g10m-face ${k>=4?'g10m-focus':''}"/>`;
  if(cone)out+=`<ellipse data-object-id="cone-base" cx="${cx}" cy="${bottom}" rx="${base}" ry="22" class="g10m-disc ${k>=4?'g10m-focus':''}"/>`;
  else out+=`<polygon data-object-id="pyramid-base" points="${cx-base},${bottom} ${cx},${bottom+25} ${cx+base},${bottom} ${cx},${bottom-20}" class="g10m-disc ${k>=4?'g10m-focus':''}"/>`;
  out+=`<line data-object-id="perpendicular-height" x1="${cx}" y1="${top}" x2="${cx}" y2="${bottom}" class="g10m-dimension"/>`+t('height-label',cx-86,(top+bottom)/2,`h = ${h} cm`)+t('base-label',cx+base+4,bottom+14,cone?`r = ${v.r} cm`:`side = ${v.b} cm`);
  if(k>=2&&slant)out+=t('slant-label',cx+35,top+58,`l = ${slant} cm`);
  return out;
 }
 function render(p,state,phase,n){
  const q=JSON.parse(p.scene_json),v=q.visual?.values,k=stage(state);
  if(q.id!==p.question_id||q.problem!==p.prompt||q.lesson!==n||q.visual?.family!=='grade10_measurement'||v?.lesson!==n)throw Error('Measurement scene belongs to another question');
  const shape=v.shape;
  if(!['prism','cylinder','sphere','hemisphere','cone','pyramid','cylinder_hemisphere'].includes(shape))throw Error('Unsupported measurement shape');
  for(const dim of shape==='prism'?['a','b','h']:shape==='pyramid'?['b','h']:shape==='sphere'||shape==='hemisphere'?['r']:['r','h'])if(!Number.isFinite(Number(v[dim]))||Number(v[dim])<=0)throw Error('Invalid measurement dimension');
  const diagram=shape==='prism'?prism(v,k):shape==='cylinder'||shape==='cylinder_hemisphere'?cylinder(v,k,shape==='cylinder_hemisphere'):shape==='sphere'||shape==='hemisphere'?sphere(v,k):apex(v,k);
  const output=k>=3&&v.volume!==undefined?t('volume-label',45,355,`Volume = ${v.volume}${shape==='prism'||shape==='pyramid'?'':'π'} cm³`):'';
  const surface=k>=4&&v.surface!==undefined?t('surface-label',310,355,`Outside area = ${v.surface}${shape==='prism'||shape==='pyramid'?'':'π'} cm²`):'';
  return `<section class="g10m-board" data-managed-visibility="true" data-question-id="${esc(q.id)}"><p data-object-id="problem">${esc(q.problem)}</p><div data-object-id="model" class="g10m-model"><svg viewBox="0 0 590 380" role="img" aria-label="Measurement diagram for ${esc(q.id)}"><title>Question-specific ${esc(shape)}, stage ${k} of 5</title>${diagram}${output}${surface}</svg></div><p data-object-id="operation">${phase==='operation'?esc(state.working_state):''}</p><p data-object-id="result">${phase==='result'&&k<5?esc(state.after_state):''}</p><p data-object-id="verification">${phase==='result'&&k===5?esc(state.after_state):''}</p></section>`;
 }
 for(let n=1;n<=6;n++)AthenaVisualizationRegistry.register('geometry',`grade10_meas_${n}`,{render:(p,s,phase)=>render(p,s,phase,n)});
})();
