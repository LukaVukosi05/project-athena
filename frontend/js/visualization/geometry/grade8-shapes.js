/* Question-specific, progressive SVG for the five Grade 8 2D-shape lessons. */
(() => {
  const esc=x=>escapeWhiteboardHtml(String(x??''));
  const stageOf=state=>Number((state.annotations||[]).find(x=>/^stage:\d+$/.test(x))?.slice(6)||0);
  const pos=p=>`${Number(p[0]).toFixed(1)},${Number(p[1]).toFixed(1)}`;
  function tick(points,a,b,count=1){
    const p=points[a],q=points[b],dx=q[0]-p[0],dy=q[1]-p[1],length=Math.hypot(dx,dy);
    if(!length)return '';
    const normal=[-dy/length,dx/length],unit=[dx/length,dy/length];
    return Array.from({length:count},(_,i)=>{
      const offset=(i-(count-1)/2)*7,m=[(p[0]+q[0])/2+unit[0]*offset,(p[1]+q[1])/2+unit[1]*offset];
      return `<line class="g8-shape-tick" x1="${m[0]-normal[0]*5}" y1="${m[1]-normal[1]*5}" x2="${m[0]+normal[0]*5}" y2="${m[1]+normal[1]*5}"/>`;
    }).join('');
  }
  function corner(points,i){
    const p=points[i],left=points[(i+points.length-1)%points.length],right=points[(i+1)%points.length];
    const unit=q=>{const length=Math.hypot(q[0]-p[0],q[1]-p[1]);return [(q[0]-p[0])/length,(q[1]-p[1])/length]};
    const a=unit(left),b=unit(right),size=11;
    return `<path class="g8-shape-right" d="M${p[0]+a[0]*size} ${p[1]+a[1]*size}L${p[0]+(a[0]+b[0])*size} ${p[1]+(a[1]+b[1])*size}L${p[0]+b[0]*size} ${p[1]+b[1]*size}"/>`;
  }
  function parallel(points,a,b,count=1){
    const p=points[a],q=points[b],dx=q[0]-p[0],dy=q[1]-p[1],length=Math.hypot(dx,dy);
    const u=[dx/length,dy/length],normal=[-u[1],u[0]];
    return Array.from({length:count},(_,i)=>{
      const offset=(i-(count-1)/2)*12,m=[(p[0]+q[0])/2+u[0]*offset,(p[1]+q[1])/2+u[1]*offset];
      return `<path class="g8-shape-parallel" d="M${m[0]-u[0]*5+normal[0]*4} ${m[1]-u[1]*5+normal[1]*4}L${m[0]} ${m[1]}L${m[0]-u[0]*5-normal[0]*4} ${m[1]-u[1]*5-normal[1]*4}"/>`;
    }).join('');
  }
  function marks(scene,points){
    if(scene.shape==='triangle'){
      if(scene.ticks==='equilateral')return [[0,1],[1,2],[2,0]].map(([a,b])=>tick(points,a,b)).join('');
      if(scene.ticks==='isosceles')return tick(points,0,1)+tick(points,0,2);
      if(scene.labels){
        const edges=[['AB',0,1],['BC',1,2],['AC',0,2]];
        return edges.filter(([key])=>Object.values(scene.labels).filter(v=>v===scene.labels[key]).length>1)
          .map(([,a,b])=>tick(points,a,b)).join('');
      }
      return '';
    }
    const p=scene.properties||'';
    if(p.includes('four right angles'))return [0,1,2,3].map(i=>corner(points,i)).join('')+
      (p.includes('four equal sides')?[0,1,2,3].map(i=>tick(points,i,(i+1)%4)).join(''):'');
    if(p.includes('four equal sides'))return [0,1,2,3].map(i=>tick(points,i,(i+1)%4)).join('');
    if(p.includes('two pairs of equal adjacent sides'))return tick(points,0,1)+tick(points,1,2)+tick(points,2,3,2)+tick(points,3,0,2);
    if(p.includes('exactly one pair'))return parallel(points,0,1)+parallel(points,2,3);
    if(p.includes('both pairs'))return [0,1,2,3].map(i=>parallel(points,i,(i+1)%4, i%2?2:1)).join('');
    return '';
  }
  function render(params,state,phase){
    const scene=JSON.parse(params.scene_json), points=scene.points;
    if(!Array.isArray(points)||points.length<3||points.length>4||points.some(p=>!Array.isArray(p)||p.length!==2||p.some(x=>!Number.isFinite(x)))) throw Error('Invalid shape scene');
    const stage=stageOf(state), reveal=phase==='result'?stage:Math.max(0,stage-1);
    const letters=scene.vertices==='EFGH'?['E','F','G','H']:['A','B','C','D'];
    const shape=`<polygon points="${points.map(pos).join(' ')}" class="g8-shape-polygon"/>`;
    const vertices=points.map((p,i)=>`<circle cx="${p[0]}" cy="${p[1]}" r="3"/><text x="${p[0]+(p[0]<165?-15:7)}" y="${p[1]+(p[1]<110?-7:18)}">${letters[i]}</text>`).join('');
    const midpoint=(a,b)=>[(points[a][0]+points[b][0])/2,(points[a][1]+points[b][1])/2];
    const sides=scene.labels&&reveal>=1?Object.entries(scene.labels).map(([edge,value])=>{
      const a=letters.indexOf(edge[0]),b=letters.indexOf(edge[1]);if(a<0||b<0)return '';
      const m=midpoint(a,b);return `<text x="${m[0]}" y="${m[1]-8}" class="g8-shape-given">${esc(value)}</text>`;
    }).join(''):'';
    const angles=scene.angles&&reveal>=1?Object.entries(scene.angles).map(([vertex,value])=>{
      const i=letters.indexOf(vertex);if(i<0||!value)return '';
      const p=points[i],centre=[points.reduce((a,x)=>a+x[0],0)/points.length,points.reduce((a,x)=>a+x[1],0)/points.length];
      const x=p[0]+(centre[0]-p[0])*.26,y=p[1]+(centre[1]-p[1])*.27;
      return `<text x="${x}" y="${y}" class="g8-shape-angle">${esc(value)}</text>`;
    }).join(''):'';
    const evidence=scene.properties||(
      scene.ticks==='equilateral'?'AB = BC = CA':scene.ticks==='isosceles'?'AB = AC':'Compare the marked sides and angles');
    const operation=(phase==='operation'||phase==='result')?esc(state.working_state||''):'';
    const result=phase==='result'?esc(state.after_state||''):'';
    return `<div class="g8-shape-stage" data-object-id="model" role="group" aria-label="${esc(params.prompt)}">
      <svg viewBox="0 0 360 225" role="img" aria-label="${esc(scene.shape)} with question-specific marked sides and angles"><g class="g8-shape-lines">${shape}${vertices}${sides}${angles}${reveal>=2?marks(scene,points):''}</g></svg>
      <p data-object-id="shape-given">${reveal>=1?esc(params.prompt):''}</p>
      <p data-object-id="shape-reason">${reveal>=2?esc(evidence):''}</p>
      <p data-object-id="operation">${operation}</p><p data-object-id="result">${result}</p>
      <p data-object-id="verification">${phase==='result'&&String(state.after_state||'').startsWith('Verified:')?result:''}</p></div>`;
  }
  for(const name of ['triangle_sides','triangle_sum','equal_triangle','quad_classify','quad_angle'])
    AthenaVisualizationRegistry.register('geometry',`grade8_${name}`,{render});
  if(typeof module!=='undefined')module.exports={render};
})();
