/* One stable coordinate plane per question; original and image persist across stages. */
(() => {
 const esc=x=>escapeWhiteboardHtml(String(x??''));
 let scale=21;const coord=(x,y)=>[250+scale*x,152-scale*y];
 const label=(id,x,y,s)=>`<text data-object-id="${id}" x="${x}" y="${y}">${esc(s)}</text>`;
 function polygon(points,cls,id){return `<polygon data-object-id="${id}" class="${cls}" points="${points.map(([x,y])=>coord(x,y).join(',')).join(' ')}"/>`}
 function vertex(name,p,cls){const [x,y]=coord(...p);return `<circle data-object-id="${name}" class="${cls}" cx="${x}" cy="${y}" r="4.5"/>${label(`${name}-label`,x+6,y-7,`${name}(${p[0]}, ${p[1]})`)}`}
 function stage(state,phase){const tag=(state.annotations||[]).find(s=>/^stage:\d+$/.test(s));return phase==='result'?Number(tag?.slice(6)||0):Math.max(0,Number(tag?.slice(6)||0)-1)}
 function render(params,state,phase,n){
  const scene=JSON.parse(params.scene_json),v=scene.visual?.values,step=stage(state,phase);
  if(!v||scene.id!==params.question_id||scene.lesson!==n||scene.problem!==params.prompt||v.lesson!==n||v.original?.length!==3)throw Error('Transformation scene belongs to another question');
  const extents=[...v.original,...(v.image||[]),v.centre];
  const maxX=Math.max(10,...extents.map(p=>Math.abs(p[0]))),maxY=Math.max(6,...extents.map(p=>Math.abs(p[1])));
  scale=Math.min(21,185/maxX,120/maxY);
  let grid='';for(let i=-Math.ceil(maxX);i<=Math.ceil(maxX);i++){
   const [x]=coord(i,0),[,y]=coord(0,i);
   grid+=`<line class="g9-tg-grid" x1="${x}" y1="17" x2="${x}" y2="287"/>`;
  }
  for(let i=-Math.ceil(maxY);i<=Math.ceil(maxY);i++){const [,y]=coord(0,i);grid+=`<line class="g9-tg-grid" x1="40" y1="${y}" x2="460" y2="${y}"/>`;
  }
  grid+='<line class="g9-tg-axis" x1="40" y1="152" x2="460" y2="152"/><line class="g9-tg-axis" x1="250" y1="17" x2="250" y2="287"/>'+label('x-axis',462,155,'x')+label('y-axis',254,20,'y');
  let marks='';if(step>=1){marks+=polygon(v.original,'g9-tg-original','original-polygon');v.original.forEach((p,i)=>marks+=vertex('ABC'[i],p,'g9-tg-original-dot'))}
  if(step>=2){
   if(v.kind==='reflect_x'||v.kind==='reflect_y')marks+=`<line class="g9-tg-reference" x1="${v.kind==='reflect_y'?250:40}" y1="${v.kind==='reflect_y'?17:152}" x2="${v.kind==='reflect_y'?250:460}" y2="${v.kind==='reflect_y'?287:152}"/>`;
   if(v.kind==='reflect_diag'){const [lx,ly]=coord(-6,-6),[rx,ry]=coord(6,6);marks+=`<line class="g9-tg-reference" x1="${lx}" y1="${ly}" x2="${rx}" y2="${ry}"/>`}
   if(['enlarge','rotate_ccw','rotate_cw'].includes(v.kind))marks+=vertex('O',v.centre,'g9-tg-centre');
   marks+=label('rule',45,298,v.rule);
  }
  if(step>=3){const [x,y]=coord(...v.image[0]);const [ox,oy]=coord(...v.original[0]);marks+=`<line class="g9-tg-path" x1="${ox}" y1="${oy}" x2="${x}" y2="${y}"/>`+vertex('A′',v.image[0],'g9-tg-image-dot')}
  if(step>=4){marks+=polygon(v.image,'g9-tg-image','image-polygon');v.image.slice(1).forEach((p,i)=>marks+=vertex(['B′','C′'][i],p,'g9-tg-image-dot'))}
  if(step>=5)marks+=label('check',44,32,n===6?`Perimeter ×${v.factor}; area ×${v.factor*v.factor}`:'Check every vertex against the rule');
  return `<section class="g9-tg-board" data-managed-visibility="true" data-question-id="${esc(scene.id)}"><p data-object-id="problem">${esc(scene.problem)}</p><div data-object-id="model" class="g9-tg-model"><svg viewBox="0 0 500 310" role="img" aria-label="${esc(scene.problem)}"><title>Original and transformed triangle on a fixed coordinate plane</title>${grid}${marks}</svg></div><p data-object-id="operation">${phase==='operation'?esc(state.working_state):''}</p><p data-object-id="result">${phase==='result'&&step<5?esc(state.after_state):''}</p><p data-object-id="verification">${phase==='result'&&step===5?esc(state.after_state):''}</p></section>`;
 }
 for(let n=1;n<=7;n++)AthenaVisualizationRegistry.register('geometry',`grade9_transform_${n}`,{render:(p,s,phase)=>render(p,s,phase,n),destroy(){}});
})();
