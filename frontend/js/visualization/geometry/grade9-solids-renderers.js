/* Solid properties and foldable nets driven by the current question. */
(() => {
  const esc=x=>escapeWhiteboardHtml(String(x??''));
  const t=(id,x,y,s)=>`<text data-object-id="${id}" x="${x}" y="${y}">${esc(s)}</text>`;
  const rect=(id,x,y,w,h,cls)=>`<rect data-object-id="${id}" x="${x}" y="${y}" width="${w}" height="${h}" class="${cls}"/>`;
  const line=(x,y,X,Y,cls)=>`<line x1="${x}" y1="${y}" x2="${X}" y2="${Y}" class="${cls}"/>`;
  const poly=(id,pts,cls)=>`<polygon data-object-id="${id}" points="${pts}" class="${cls}"/>`;
  const circle=(id,x,y,r,cls)=>`<circle data-object-id="${id}" cx="${x}" cy="${y}" r="${r}" class="${cls}"/>`;
  const STATS={tetrahedron:[4,6,4,'triangles'],cube:[6,12,8,'squares'],octahedron:[8,12,6,'triangles'],dodecahedron:[12,30,20,'pentagons'],icosahedron:[20,30,12,'triangles']};
  const PARTS={cube:'6 equal squares','rectangular prism':'6 rectangles in three matching pairs','triangular prism':'3 rectangles and 2 matching triangles','square pyramid':'1 square and 4 matching triangles',cylinder:'1 rectangle and 2 matching circles'};
  const phaseStage=(state,phase)=>{const x=(state.annotations||[]).find(s=>/^stage:\d+$/.test(s));const n=x?Number(x.slice(6)):0;return phase==='result'?n:Math.max(0,n-1)};
  function faceIcon(shape,x,y,size,id){
    if(shape==='squares')return rect(id,x,y,size,size,'g9-solid-face');
    const sides=shape==='pentagons'?5:3;
    const pts=Array.from({length:sides},(_,i)=>{const angle=(-Math.PI/2+i*2*Math.PI/sides);return `${(x+size/2+size*.43*Math.cos(angle)).toFixed(1)},${(y+size/2+size*.43*Math.sin(angle)).toFixed(1)}`}).join(' ');
    return poly(id,pts,'g9-solid-face');
  }
  function solidProjection(shape){
    if(shape==='tetrahedron')return poly('projection','225,111 335,111 277,37','g9-solid-face')+line(277,78,225,111,'g9-solid-edge')+line(277,78,335,111,'g9-solid-edge')+line(277,78,277,37,'g9-solid-edge');
    if(shape==='cube')return rect('projection',229,61,85,64,'g9-solid-face')+poly('back-face','248,39 333,39 314,61 229,61','g9-solid-back')+line(314,125,333,103,'g9-solid-edge')+line(333,39,333,103,'g9-solid-edge');
    if(shape==='octahedron')return poly('projection','282,30 347,84 282,133 217,84','g9-solid-face')+line(217,84,347,84,'g9-solid-edge')+line(282,30,282,133,'g9-solid-edge');
    if(shape==='dodecahedron')return poly('projection','280,35 329,68 310,117 250,117 231,68','g9-solid-back')+poly('front-face','280,58 307,77 296,107 264,107 253,77','g9-solid-face')+line(280,35,280,58,'g9-solid-edge')+line(329,68,307,77,'g9-solid-edge')+line(310,117,296,107,'g9-solid-edge')+line(250,117,264,107,'g9-solid-edge')+line(231,68,253,77,'g9-solid-edge');
    return poly('projection','280,26 344,69 321,121 239,121 216,69','g9-solid-back')+poly('centre-face','280,52 311,77 280,108 249,77','g9-solid-face')+line(280,26,280,52,'g9-solid-edge')+line(344,69,311,77,'g9-solid-edge')+line(321,121,280,108,'g9-solid-edge')+line(239,121,280,108,'g9-solid-edge')+line(216,69,249,77,'g9-solid-edge');
  }
  function platonic(v,step){
    const [F,E,V,face]=STATS[v.shape];let pic=t('name',18,31,`Regular ${v.shape}: ${face}`);
    pic+=solidProjection(v.shape);
    if(step>=1){for(let i=0;i<F;i++)pic+=faceIcon(face,27+(i%10)*44,127+Math.floor(i/10)*43,32,`face-${i}`)}
    if(step>=2)pic+=t('givens',18,105,`Faces ${v.target==='faces'?'?':F} · Edges ${v.target==='edges'?'?':E} · Vertices ${v.target==='vertices'?'?':V}`);
    if(step>=3)pic+=t('euler',18,241,'Euler: F + V = E + 2');
    if(step>=4)pic+=t('answer-mark',259,105,`${v.target} = ${v.target==='faces'?F:v.target==='vertices'?V:E}`);
    if(step>=5)pic+=t('check-mark',18,265,`${F} + ${V} = ${E} + 2`);
    return pic;
  }
  function curved(v,step){
    const compare=v.model==='compare',sphere=v.model!=='cylinder',cylinder=v.model!=='sphere';let pic='';
    if(sphere){const cx=compare?130:250;pic+=circle('sphere',cx,125,73,'g9-solid-sphere');if(step>=1)pic+=t('sphere-curved',cx-68,216,'1 curved surface');if(step>=3)pic+=t('sphere-edges',cx-53,239,'0 edges · 0 vertices')}
    if(cylinder){const x=compare?295:177;pic+=rect('lateral',x,85,145,105,'g9-solid-curved');pic+=`<ellipse data-object-id="top-face" cx="${x+72.5}" cy="85" rx="72.5" ry="22" class="g9-solid-face"/>`;
      pic+=`<path data-object-id="bottom-face" d="M ${x} 190 A 72.5 22 0 0 0 ${x+145} 190" class="g9-solid-edge"/>`;
      if(step>=2)pic+=t('flat-faces',x,47,'2 flat circular faces');if(step>=3)pic+=t('curved-edges',x-10,231,'2 curved edges · 0 vertices');}
    if(step>=4)pic+=t('comparison',23,267,compare?'Cylinder: two flat circles; sphere: no edges.':sphere?'Sphere rolls on its curved surface.':'A closed cylinder has two circular bases.');
    return pic;
  }
  function netPieces(shape){
    const square=(id,x,y,w=72,h=60)=>rect(id,x,y,w,h,'g9-solid-face');
    const triangle=(id,pts)=>poly(id,pts,'g9-solid-face');
    if(shape==='cube')return [square('base',170,106,58,58),square('side-left',112,106,58,58),square('side-right',228,106,58,58),square('side-far',286,106,58,58),square('top',170,48,58,58),square('bottom',170,164,58,58)];
    if(shape==='rectangular prism')return [square('base',75,110,96,48),square('side-left',171,110,62,48),square('side-right',233,110,96,48),square('side-far',329,110,62,48),square('top',75,48,96,62),square('bottom',75,158,96,62)];
    if(shape==='triangular prism')return [square('side-0',85,105,95,66),square('side-1',180,105,95,66),square('side-2',275,105,95,66),triangle('triangle-0','180,105 275,105 227.5,22.7'),triangle('triangle-1','180,171 275,171 227.5,253.3')];
    if(shape==='square pyramid')return [square('base',185,101,88,88),triangle('triangle-0','185,101 273,101 229,25'),triangle('triangle-1','273,101 273,189 349,145'),triangle('triangle-2','185,189 273,189 229,265'),triangle('triangle-3','185,101 185,189 109,145')];
    return [rect('lateral',125,98,2*Math.PI*40,92,'g9-solid-face'),circle('circle-0',250.7,58,40,'g9-solid-face'),circle('circle-1',250.7,230,40,'g9-solid-face')];
  }
  function net(v,step,repair){
    const pieces=netPieces(v.shape),shown=repair?pieces.length-1:pieces.length;
    let pic=t('solid-label',17,27,`${v.shape} · one edge marked ${v.scale} cm`);
    pic+=t('edge-label',17,53,`Given edge: ${v.scale} cm`);
    if(step>=1)pic+=pieces[0];
    if(step>=2)pic+=pieces.slice(1,repair?Math.max(2,shown-1):Math.max(2,shown-2)).join('');
    if(step>=3)pic+=pieces.slice(repair?Math.max(2,shown-1):Math.max(2,shown-2),shown).join('');
    if(repair&&step===3)pic+=t('gap',19,266,`First error: ${v.missing||'a face'} is absent`);
    if(step>=4){if(repair)pic+=`<g class="g9-solid-repaired">${pieces.at(-1)}</g>`;if(step===4)pic+=t('complete',20,267,`Complete net: ${PARTS[v.shape]}`)}
    if(step>=5)pic+=t('fold-check',19,267,`Fold matching edges: ${pieces.length} faces close the ${v.shape}.`);
    return pic;
  }
  for(let n=1;n<=4;n++)AthenaVisualizationRegistry.register('geometry',`grade9_solid_${n}`,{
    render(params,state,phase){
      const scene=JSON.parse(params.scene_json),v=scene.visual?.values,step=phaseStage(state,phase);
      if(!v||scene.lesson!==n||scene.id!==params.question_id||scene.problem!==params.prompt)throw Error('Solid model belongs to another question');
      const picture=n===1?platonic(v,step):n===2?curved(v,step):net(v,step,n===4);
      return `<section class="g9-solid-board" data-managed-visibility="true" data-question-id="${esc(scene.id)}"><p data-object-id="problem">${esc(scene.problem)}</p><div data-object-id="model" class="g9-solid-model"><svg viewBox="0 0 500 290" role="img" aria-label="${esc(scene.problem)}"><title>Question-specific ${esc(v.shape||v.model)} model</title>${picture}<text data-object-id="stage-label" x="20" y="283">${step?`Step ${step} of 5`:'Read the givens'}</text></svg></div><p data-object-id="operation">${phase==='operation'?esc(state.working_state):''}</p><p data-object-id="result">${phase==='result'&&step<5?esc(state.after_state):''}</p><p data-object-id="verification">${phase==='result'&&step===5?esc(state.after_state):''}</p></section>`;
    },destroy(){}
  });
})();
