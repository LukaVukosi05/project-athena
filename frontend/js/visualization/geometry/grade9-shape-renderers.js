/* Question-specific geometry, with marks introduced only as each proof advances. */
(() => {
  const esc=v=>escapeWhiteboardHtml(String(v??''));
  const stage=(state,phase)=>{
    const marker=(state.annotations||[]).find(x=>/^stage:\d+$/.test(x));
    const n=marker?Number(marker.slice(6)):0;
    return phase==='result'?n:Math.max(0,n-1);
  };
  const point=(x,y)=>`${x.toFixed(1)},${y.toFixed(1)}`;
  const line=(x1,y1,x2,y2,extra='')=>`<line x1="${x1.toFixed(1)}" y1="${y1.toFixed(1)}" x2="${x2.toFixed(1)}" y2="${y2.toFixed(1)}" ${extra}/>`;
  const text=(id,x,y,value,cls='')=>`<text data-object-id="${id}" x="${x.toFixed(1)}" y="${y.toFixed(1)}" class="${cls}">${esc(value)}</text>`;
  const polygon=(vertices,cls='')=>`<polygon points="${vertices.map(p=>point(...p)).join(' ')}" class="${cls}"/>`;
  const tri=(A,B,C,labels=['A','B','C'])=>polygon([A,B,C])+[A,B,C].map((p,i)=>text('vertex-'+i,p[0]+(i===0?-12:i===1?8:0),p[1]+(i===2?-8:18),labels[i])).join('');
  function triangleFromSides(ab,ac,bc,origin,scale,mirror=false){
    const x=(ab*ab+ac*ac-bc*bc)/(2*ab),y=Math.sqrt(Math.max(0,ac*ac-x*x));
    return [[origin[0],origin[1]],[origin[0]+ab*scale,origin[1]],[origin[0]+x*scale,origin[1]-(mirror?-y:y)*scale]];
  }
  function draw(scene,done){
    const v=scene.visual?.values;
    if(!v)return '<svg viewBox="0 0 500 280" role="img" aria-label="Geometry question awaiting the first step"><path d="M60 210L250 40L440 210Z"/></svg>';
    let shapes='',labels='',marks='';
    const late=done>=4;
    if([1,7,8].includes(scene.lesson)){
      if(scene.lesson===1&&v.model==='equilateral'){
        const A=[250,52],B=[150,225],C=[350,225];shapes=tri(A,B,C);
        labels=text('given-side',170,132,`${v.side} cm`)+text('base-left',B[0]+25,210,late?'60°':'x');
        if(done>=2)marks=text('equal-sides',325,130,'AB = BC = CA');
      }else if(scene.lesson===1&&v.model==='right'){
        const width=Math.min(215,150*Math.tan(v.given*Math.PI/180)),height=width/Math.tan(v.given*Math.PI/180);
        const A=[132,225-height],B=[132,225],C=[132+width,225];shapes=tri(A,B,C);
        labels=text('given-angle',A[0]+17,A[1]+23,`${v.given}°`)+text('right-angle',B[0]+19,205,'90°')+text('given-side',B[0]+width/2,245,`${v.side} cm`)+text('base-right',C[0]-53,204,late?`${v.target}°`:'x');
        marks='<path d="M132 211h14v14" class="g9-shape-right"/>';
      }else{
        const half=Math.min(195,170*Math.tan(v.apex*Math.PI/360)),height=half/Math.tan(v.apex*Math.PI/360),A=[250,225-height],B=[250-half,225],C=[250+half,225];
        shapes=tri(A,B,C);
        labels=text('given-angle',235,A[1]+30,`${v.apex}°`)+text('base-left',B[0]+26,207,late?`${v.target}°`:'x')+text('base-right',C[0]-48,207,done>=2?late?`${v.target}°`:'x':'?');
        marks=done>=1?`<path d="M${point(0.55*A[0]+0.45*B[0]-7,0.55*A[1]+0.45*B[1]-7)}l14 14 M${point(0.55*A[0]+0.45*C[0]-7,0.55*A[1]+0.45*C[1]+7)}l14 -14" class="g9-shape-equal"/>`:'';
        if(scene.lesson===8&&done>=2)labels+=text('claim',20,258,`Learner's claim: ${v.claimed}°`,done>=3?'g9-shape-error':'');
      }
    } else if(scene.lesson===2){
      const b=v.right*Math.PI/180,c=(180-v.left-v.right)*Math.PI/180;
      const rise=1/(1/Math.tan(b)+1/Math.tan(c)),raw=rise/Math.tan(b);
      const xmin=Math.min(0,1,raw),xmax=Math.max(0,1,raw),factor=Math.min(300/(xmax-xmin),150/rise);
      const B=[90-xmin*factor,215],C=[90+(1-xmin)*factor,215],A=[90+(raw-xmin)*factor,215-rise*factor];
      shapes=tri(A,B,C)+line(C[0],215,Math.min(450,C[0]+65),215,'class="g9-shape-extension"');
      labels=text('given-angle-a',A[0]+8,A[1]+26,`${v.left}°`)+text('given-angle-b',B[0]+29,199,`${v.right}°`)+text('target-angle',Math.min(450,C[0]+25),190,late?`${v.target}°`:'x');
      if(done>=2)labels+=text('interior-angle',C[0]-63,198,`${180-v.target}°`);
    } else if(scene.lesson===3){
      const model=v.model,angle=v.given*Math.PI/180;
      let A,B,C,D;
      if(model==='kite'){
        A=[250,42];B=[152,135];C=[250,237];D=[348,135];
      }else if(model==='square'){
        A=[175,220];B=[325,220];C=[325,70];D=[175,70];
      }else if(model==='rectangle'){
        A=[140,220];B=[350,220];C=[350,85];D=[140,85];
      }else if(model==='trapezium'){
        A=[160,220];B=[405,220];D=[160+100*Math.cos(angle),220-100*Math.sin(angle)];C=[D[0]+160,D[1]];
      }else if(model==='rhombus'){
        A=[175,220];B=[315,220];D=[175+140*Math.cos(angle),220-140*Math.sin(angle)];C=[315+140*Math.cos(angle),220-140*Math.sin(angle)];
      }else{
        A=[140,220];B=[345,220];const dx=110*Math.cos(angle),dy=110*Math.sin(angle);D=[140+dx,220-dy];C=[345+dx,220-dy];
      }
      shapes=polygon([A,B,C,D])+[A,B,C,D].map((p,i)=>text('vertex-'+i,p[0]+(i<2?-13:7),p[1]+(i<2?17:-8),'ABCD'[i])).join('');
      if(['rectangle','square','kite'].includes(model)){
        const label=model==='rectangle'?'CD':model==='square'?'BC':'AD';
        labels=text('given-side',(A[0]+B[0])/2,A[1]+25,`${v.given} cm`)+text('target-side',(model==='rectangle'?(C[0]+D[0])/2:model==='square'?(B[0]+C[0])/2:(A[0]+D[0])/2),model==='rectangle'?D[1]-12:model==='square'?(B[1]+C[1])/2:(A[1]+D[1])/2,late?`${v.target} cm`:label+' ?');
      }else{
        const target=model==='trapezium'?D:B;
        labels=text('given-angle',A[0]+25,A[1]-18,`${v.given}°`)+text('target-angle',target[0]+(model==='trapezium'?16:-50),target[1]+(model==='trapezium'?22:-16),late?`${v.target}°`:'x');
      }
      if(done>=1&&model!=='kite')marks=line(A[0]+20,A[1],B[0]-20,B[1],'class="g9-shape-parallel"')+line(D[0]+20,D[1],C[0]-20,C[1],'class="g9-shape-parallel"');
    } else if(scene.lesson===4){
      if(v.model==='regular_polygon'){
        const n=v.sides,r=104,cx=250,cy=138,pts=Array.from({length:n},(_,i)=>[cx+r*Math.cos(-Math.PI/2+2*Math.PI*i/n),cy+r*Math.sin(-Math.PI/2+2*Math.PI*i/n)]);
        shapes=polygon(pts);
        if(done>=2)marks=pts.slice(2,-1).map(p=>line(...pts[0],...p,'class="g9-shape-diagonal"')).join('');
        labels=text('vertices',20,255,`${n} vertices`)+(late?text('total',290,254,`sum ${v.target}°; each ${v.each}°`):'');
      }else{
        let A=[145,220],B=[355,220],C=[355,90],D=[145,90];
        if(v.shape==='square'){A=[170,220];B=[330,220];C=[330,60];D=[170,60]}
        if(v.shape==='parallelogram'){A=[140,220];B=[345,220];C=[395,95];D=[190,95]}
        if(v.shape==='rhombus'){A=[175,215];B=[315,215];C=[385,94];D=[245,94]}
        if(v.shape==='kite'){A=[250,45];B=[145,135];C=[250,235];D=[355,135]}
        shapes=polygon([A,B,C,D])+[A,B,C,D].map((p,i)=>text('vertex-'+i,p[0]+(i<2?-14:7),p[1]+(i<2?17:-8),'ABCD'[i])).join('');
        const E=[(A[0]+C[0])/2,(A[1]+C[1])/2];
        if(done>=2)marks=line(...A,...C,'class="g9-shape-diagonal"')+line(...B,...D,'class="g9-shape-diagonal"')+text('intersection',E[0]+8,E[1]-8,'E');
        const side=v.shape==='rectangle'||v.shape==='square'?'BD':v.shape==='kite'?'ED':'EC';
        labels=text('given',v.shape==='kite'?B[0]+28:A[0]+55,v.shape==='kite'?B[1]-10:A[1]-45,`${v.given} cm`)+text('target',v.shape==='kite'?D[0]-80:C[0]-62,v.shape==='kite'?D[1]-10:C[1]+55,late?`${v.target} cm`:`${side} ?`);
      }
    } else if(scene.lesson===5){
      const [ab,ac,bc]=v.sides,unit=90/Math.max(ab,ac,bc),left=triangleFromSides(ab,ac,bc,[65,210],unit),right=left.map(([x,y])=>[x+260,y]);
      shapes=tri(...left)+tri(...right,['D','E','F']);
      const mid=(p,q)=>[(p[0]+q[0])/2,(p[1]+q[1])/2];
      labels=text('ab',...mid(left[0],left[1]),`${ab} cm`)+text('de',...mid(right[0],right[1]),`${ab} cm`);
      if(v.criterion!=='ASA')labels+=text('ac',...mid(left[0],left[2]),`${ac} cm`)+text('df',...mid(right[0],right[2]),`${ac} cm`)+text('bc',...mid(left[1],left[2]),`${bc} cm`)+text('ef',...mid(right[1],right[2]),v.criterion==='SSS'?`${bc} cm`:late?`${bc} cm`:'?');
      if(done>=2)marks=text('congruence-marks',170,265,v.criterion==='SSS'?'Three corresponding side pairs':v.criterion==='ASA'?'∠A = ∠D and ∠B = ∠E':'∠A = ∠D (included)');
    } else if(scene.lesson===6){
      const small=v.small,scale=v.scale,ratio=small+2,foot=(small*small+(small+1)**2-ratio*ratio)/(2*small),alt=Math.sqrt((small+1)**2-foot*foot),unit=Math.min(60/ratio,150/(alt*scale),200/(small*scale));
      const left=triangleFromSides(small,small+1,ratio,[65,205],unit),right=triangleFromSides(small*scale,(small+1)*scale,ratio*scale,[258,205],unit);
      shapes=tri(...left)+tri(...right,['D','E','F']);
      labels=text('ab',88,224,`${small} cm`)+text('bc',125,153,`${small+2} cm`)+text('de',285,224,`${small*scale} cm`)+text('ef',387,148,v.criterion==='SSS'||late?`${v.target} cm`:'?');
      if(v.criterion==='SAS'||v.criterion==='SSS')labels+=text('ac',82,163,`${small+1} cm`)+text('df',300,104,`${(small+1)*scale} cm`);
      if(done>=2)marks=text('similarity-condition',145,260,v.criterion==='given'?'△ABC ∼ △DEF':v.criterion==='AA'?'∠A = ∠D, ∠B = ∠E':v.criterion==='SAS'?'∠A = ∠D (included)':'three proportional side pairs');
    } else throw Error('Unsupported shape diagram');
    return `<svg viewBox="0 0 500 280" role="img" aria-label="${esc(scene.problem)}; ${late?'calculated value shown':'target concealed'}"><title>Question-owned geometry, dimensions shown only where given</title><g class="g9-shape-lines">${shapes}${marks}</g><g class="g9-shape-labels">${labels}</g></svg>`;
  }
  for(let number=1;number<=8;number++)AthenaVisualizationRegistry.register('geometry',`grade9_shapes_${number}`,{
    render(params,state,phase){
      const scene=JSON.parse(params.scene_json),done=stage(state,phase);
      if(scene.lesson!==number||scene.id!==params.question_id)throw Error('Shape diagram belongs to another question');
      return `<section class="g9-shapes-board" data-managed-visibility="true" data-question-id="${esc(params.question_id)}">
        <p data-object-id="problem" class="g9-shapes-question">${esc(params.prompt)}</p>
        <div data-object-id="model" class="g9-shapes-model">${draw(scene,done)}</div>
        <p data-object-id="operation">${phase==='operation'?esc(state.working_state):''}</p>
        <p data-object-id="result">${phase==='result'&&done<Number(params.total_steps)?esc(state.after_state):''}</p>
        <p data-object-id="verification">${phase==='result'&&done===Number(params.total_steps)?esc(state.after_state):''}</p>
      </section>`;
    },destroy(){}
  });
})();
