/* Angle sectors follow the data's actual relationship; never measure from a decorative sketch. */
(() => {
  const esc=value=>escapeWhiteboardHtml(String(value??''));
  const stage=(state,phase)=>{
    const marker=(state.annotations||[]).find(x=>/^stage:\d+$/.test(x));
    const n=marker?Number(marker.slice(6)):0;return phase==='result'?n:Math.max(0,n-1);
  };
  const p=(x,y,degrees,distance=40)=>{
    const radians=degrees*Math.PI/180;
    return [x+Math.cos(radians)*distance,y-Math.sin(radians)*distance];
  };
  const label=(id,coordinates,value,kind='')=>`<text data-object-id="${id}" x="${coordinates[0].toFixed(1)}" y="${coordinates[1].toFixed(1)}" class="${kind}">${esc(value)}</text>`;
  function draw(scene,done){
    const v=scene.visual?.values;
    if(!v)return `<svg viewBox="0 0 460 260" role="img" aria-label="Angle question awaiting the learner's attempt"><line x1="40" y1="130" x2="420" y2="130"/><line x1="230" y1="35" x2="230" y2="225"/></svg>`;
    const {theta,given,target,relation,kind}=v;
    const showAngle=done>=(scene.lesson===3?5:scene.lesson===4?3:4);
    const targetLabel=scene.lesson===4?`(${v.coefficient}x + ${v.constant})°`:'x';
    const targetValue=showAngle?`${target}°`:targetLabel;
    let geometry='',marks='';
    if(kind==='perpendicular'){
      const [cx,cy]=[230,165],ray=p(cx,cy,theta,135);
      geometry=`<line x1="45" y1="165" x2="415" y2="165"/><line x1="230" y1="165" x2="230" y2="25"/><line x1="230" y1="165" x2="${ray[0]}" y2="${ray[1]}"/><path d="M230 153h12v12" class="g9-lines-right"/>`;
      marks=label('angle-given',p(cx,cy,theta/2,75),`${given}°`)+label('angle-target',p(cx,cy,(theta+90)/2,42),targetValue,showAngle?'g9-lines-target is-revealed':'g9-lines-target');
    } else if(kind==='intersection'){
      const [cx,cy]=[230,130],extent=Math.min(180,125/Math.sin(theta*Math.PI/180)),
        a=p(cx,cy,theta,extent),b=p(cx,cy,theta+180,extent);
      geometry=`<line x1="35" y1="130" x2="425" y2="130"/><line x1="${a[0]}" y1="${a[1]}" x2="${b[0]}" y2="${b[1]}"/>`;
      marks=label('angle-given',p(cx,cy,theta/2,55),`${given}°`)+
        label('angle-target',p(cx,cy,relation==='vertical'?180+theta/2:90+theta/2,52),targetValue,showAngle?'g9-lines-target is-revealed':'g9-lines-target');
    } else if(kind==='parallel'){
      const [ux,uy]=[275,72],ly=188,lx=ux-(ly-uy)/Math.tan(theta*Math.PI/180);
      const slope=Math.tan(theta*Math.PI/180);
      const top=[ux+uy/slope,0],bottom=[lx-(260-ly)/slope,260];
      geometry=`<line x1="30" y1="72" x2="430" y2="72"/><line x1="30" y1="188" x2="430" y2="188"/><line x1="${top[0]}" y1="${top[1]}" x2="${bottom[0]}" y2="${bottom[1]}"/>
        <path d="M75 72l12 -7m-12 7l12 7M75 188l12 -7m-12 7l12 7" class="g9-lines-parallel"/>`;
      const givenAngle=relation==='alternate'?180+theta/2:relation==='cointerior'?270+theta/2:theta/2;
      marks=label('angle-given',p(ux,uy,givenAngle,43),`${given}°`);
      if(scene.lesson>=3){
        marks+=label('angle-intermediate',p(lx,ly,theta/2,46),done>=(scene.lesson===3?3:2)?`${theta}°`:'?',done>=(scene.lesson===3?3:2)?'g9-lines-solved':'');
        marks+=label('angle-target',p(lx,ly,90+theta/2,48),targetValue,showAngle?'g9-lines-target is-revealed':'g9-lines-target');
      }else marks+=label('angle-target',p(lx,ly,theta/2,48),targetValue,showAngle?'g9-lines-target is-revealed':'g9-lines-target');
    }else throw Error('Unsupported line-angle diagram');
    const note=scene.lesson===5&&done>=2?`<p class="g9-lines-claim">Learner's claim: x = ${esc(v.claimed)}°${done>=3?' · relationship checked':''}</p>`:'';
    return `<svg viewBox="0 0 460 260" role="img" aria-label="${esc(kind)} angle diagram; marked sectors and given ${given} degrees; target ${showAngle?target+' degrees':'unknown'}">
      <title>${esc(kind)} angle relationships, not drawn to scale</title><g class="g9-lines-strokes">${geometry}</g>${marks}</svg>${note}`;
  }
  for(let number=1;number<=5;number++)AthenaVisualizationRegistry.register('geometry',`grade9_lines_${number}`,{
    render(params,state,phase){
      const scene=JSON.parse(params.scene_json),done=stage(state,phase);
      if(scene.lesson!==number)throw Error('The angle diagram belongs to another lesson');
      return `<section class="g9-lines-board" data-managed-visibility="true" data-question-id="${esc(params.question_id)}">
        <p data-object-id="problem" class="g9-lines-question">${esc(params.prompt)}</p>
        <div data-object-id="model" class="g9-lines-model">${draw(scene,done)}</div>
        <p data-object-id="operation">${phase==='operation'?esc(state.working_state):''}</p>
        <p data-object-id="result">${phase==='result'&&done<Number(params.total_steps)?esc(state.after_state):''}</p>
        <p data-object-id="verification">${phase==='result'&&done===Number(params.total_steps)?esc(state.after_state):''}</p>
      </section>`;
    },destroy(){}
  });
})();
