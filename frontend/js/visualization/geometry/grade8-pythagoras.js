/* Grade 8 Pythagoras: five question-specific models with stage-specific geometry. */
(() => {
  const esc = x => escapeWhiteboardHtml(String(x ?? ''));
  const stageOf = state => Number((state.annotations || []).find(x => /^stage:\d+$/.test(x))?.slice(6) || 0);
  const fmt = n => Number(n).toFixed(1);
  function path(points) { return points.map(([x,y],i) => `${i?'L':'M'}${fmt(x)} ${fmt(y)}`).join('')+'Z'; }
  function rightGeometry(a,b,showSquares) {
    const c=Math.hypot(a,b), A=[0,0],B=[a,0],C=[0,-b];
    const s1=[A,B,[a,a],[0,a]], s2=[A,C,[-b,-b],[-b,0]];
    const s3=[B,C,[b,-b-a],[a+b,-a]];
    const polys=showSquares?[s1,s2,s3]:[];
    const vertices=[A,B,C,...polys.flat()];
    const xs=vertices.map(v=>v[0]),ys=vertices.map(v=>v[1]);
    const minX=Math.min(...xs),maxX=Math.max(...xs),minY=Math.min(...ys),maxY=Math.max(...ys);
    const factor=Math.min(300/(maxX-minX),156/(maxY-minY));
    const project=([x,y])=>[40+(x-minX)*factor,24+(y-minY)*factor];
    return {points:[A,B,C].map(project),squares:polys.map(p=>p.map(project)),c};
  }
  function converseGeometry(a,b,c) {
    const [x,y,z]=[a,b,c].sort((m,n)=>m-n);
    if(x+y<=z)throw Error('Triangle inequality failed');
    const cosine=(x*x+y*y-z*z)/(2*x*y), sine=Math.sqrt(1-cosine*cosine);
    const vertices=[[0,0],[x,0],[y*cosine,-y*sine]];
    const xs=vertices.map(v=>v[0]),ys=vertices.map(v=>v[1]);
    const minX=Math.min(...xs),maxX=Math.max(...xs),minY=Math.min(...ys),maxY=Math.max(...ys);
    const factor=Math.min(300/(maxX-minX),145/(maxY-minY));
    return {points:vertices.map(([u,v])=>[40+(u-minX)*factor,22+(v-minY)*factor]),squares:[],c:z,sorted:[x,y,z]};
  }
  function label(p,q,value,dy=-7) {
    return `<text class="g8-pyth-side" x="${fmt((p[0]+q[0])/2)}" y="${fmt((p[1]+q[1])/2+dy)}">${esc(value)}</text>`;
  }
  function render(params,state,phase) {
    const scene=JSON.parse(params.scene_json),{a,b,c,family,context}=scene;
    if(!['square_areas','hypotenuse','missing_leg','converse','application'].includes(family) ||
       !Number.isInteger(a)||!Number.isInteger(b)||(a<=0&&!(family==='missing_leg'&&a===0))||b<=0 || (c!==null&&(!Number.isInteger(c)||c<=0))) throw Error('Invalid Pythagoras scene');
    const stage=stageOf(state),shown=phase==='result'?stage:Math.max(0,stage-1);
    const g=family==='converse'?converseGeometry(a,b,c):rightGeometry(family==='missing_leg'?Math.sqrt(c*c-b*b):a,b,family==='square_areas');
    const [A,B,C]=g.points, showGiven=shown>=1, showSquare=shown>=2, showThird=shown>=5;
    const right=family!=='converse'||shown>=5&&g.sorted[0]**2+g.sorted[1]**2===g.sorted[2]**2;
    const marks=family==='converse'?label(A,B,`${g.sorted[0]} cm`)+label(A,C,`${g.sorted[1]} cm`,7)+label(B,C,`${g.sorted[2]} cm`,-9):
      label(A,B,family==='missing_leg'?'AB = ?':`${a} ${family==='application'?(context==='route'?'km':context==='screen'?'cm':'m'):'cm'}`,12)+
      label(A,C,`${b} ${family==='application'?(context==='route'?'km':context==='screen'?'cm':'m'):'cm'}`,-7)+
      label(B,C,family==='missing_leg'?`BC = ${c} cm`:'?');
    const R=right?`<path class="g8-pyth-angle" d="M${fmt(A[0]+12)} ${fmt(A[1])}L${fmt(A[0]+12)} ${fmt(A[1]-12)}L${fmt(A[0])} ${fmt(A[1]-12)}"/>`:'';
    const squareSVG=g.squares.map((poly,i)=>`<path class="g8-pyth-square g8-pyth-square-${i+1}${shown>=(i===0?2:i===1?3:5)?' is-visible':''}" d="${path(poly)}"/>`).join('');
    const areas=family==='square_areas'&&showSquare?`<text x="${fmt((A[0]+B[0])/2)}" y="${fmt(B[1]+30)}" class="g8-pyth-area">${a*a} cm²</text>${shown>=3?`<text x="${fmt(A[0]-18)}" y="${fmt((A[1]+C[1])/2)}" class="g8-pyth-area">${b*b} cm²</text>`:''}${showThird?`<text x="${fmt((B[0]+C[0])/2+16)}" y="${fmt((B[1]+C[1])/2)}" class="g8-pyth-area">${a*a+b*b} cm²</text>`:''}`:'';
    const contextSVG=family==='application'&&showGiven?(context==='rectangle'||context==='screen'?`<path class="g8-pyth-context" d="M${fmt(B[0])} ${fmt(B[1])}L${fmt(B[0])} ${fmt(C[1])}L${fmt(C[0])} ${fmt(C[1])}"/>`:context==='route'?`<text class="g8-pyth-context-label" x="${fmt(B[0])}" y="${fmt(B[1]+22)}">E</text><text class="g8-pyth-context-label" x="${fmt(C[0]-18)}" y="${fmt(C[1])}">N</text>`:context==='ladder'?`<path class="g8-pyth-context" d="M${fmt(A[0])} ${fmt(C[1]-6)}L${fmt(A[0])} ${fmt(A[1]+6)}M${fmt(A[0]-10)} ${fmt(A[1])}L${fmt(B[0]+10)} ${fmt(B[1])}"/>`:''):'';
    const operation=(phase==='operation'||phase==='result')?esc(state.working_state||''):'';
    const result=phase==='result'?esc(state.after_state||''):'';
    return `<div class="g8-pyth-stage" data-object-id="model" role="group" aria-label="${esc(params.prompt)}">
      <svg viewBox="0 0 380 230" role="img" aria-label="${esc(family==='converse'?'Given side lengths without an assumed right angle':'Right triangle with question-specific perpendicular sides')}">
        ${squareSVG}${contextSVG}<path class="g8-pyth-triangle" d="${path(g.points)}"/>${R}
        ${showGiven?marks:''}${areas}
      </svg>
      <p data-object-id="shape-given">${showGiven?esc(params.prompt):''}</p>
      <p data-object-id="shape-reason">${shown>=2?esc(family==='converse'?'Compare squares of the two shorter sides with the square of the longest.':family==='missing_leg'?'Subtract the known leg square from the hypotenuse square.':'Add the square areas of perpendicular sides.'):''}</p>
      <p data-object-id="operation">${operation}</p><p data-object-id="result">${result}</p>
      <p data-object-id="verification">${phase==='result'&&String(state.after_state||'').startsWith('Verified:')?'✓ Checked against the original side lengths.':''}</p>
    </div>`;
  }
  for (const family of ['square_areas','hypotenuse','missing_leg','converse','application'])
    AthenaVisualizationRegistry.register('geometry',`grade8_pythagoras_${family}`,{render});
  if(typeof module!=='undefined')module.exports={render,rightGeometry,converseGeometry};
})();
