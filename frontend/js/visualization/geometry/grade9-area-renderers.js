/* Lengths, regions and units follow the current question rather than a stock sketch. */
(() => {
  const esc=value=>escapeWhiteboardHtml(String(value??''));
  const stage=(state,phase)=>{
    const marker=(state.annotations||[]).find(x=>/^stage:\d+$/.test(x));
    const n=marker?Number(marker.slice(6)):0;return phase==='result'?n:Math.max(0,n-1);
  };
  const label=(id,x,y,content)=>`<text data-object-id="${id}" x="${x.toFixed(1)}" y="${y.toFixed(1)}">${esc(content)}</text>`;
  const rect=(x,y,w,h,cls='')=>`<rect x="${x.toFixed(1)}" y="${y.toFixed(1)}" width="${w.toFixed(1)}" height="${h.toFixed(1)}" class="${cls}"/>`;
  const path=(points,cls='')=>`<polygon points="${points.map(([x,y])=>`${x.toFixed(1)},${y.toFixed(1)}`).join(' ')}" class="${cls}"/>`;
  function draw(scene,done){
    const v=scene.visual?.values;
    if(!v)return '<svg viewBox="0 0 500 290" role="img" aria-label="Measurement question awaiting its first step"><rect x="90" y="65" width="310" height="170"/></svg>';
    let drawing='',notes='';const late=done>=4;
    if(scene.lesson===1){
      const unit=Math.min(335/v.length,155/v.width),width=v.length*unit,height=v.width*unit,x=80,y=60;
      drawing=rect(x,y,width,height,done>=4?'g9-area-filled':'')+
        label('given-length',x+width/2,y+height+26,`${v.length_mm} mm`)+label('given-width',x-46,y+height/2,`${v.width} cm`);
      if(done>=2)notes+=label('converted-length',185,270,`${v.length} cm = ${v.length_mm} mm`);
      if(done>=3)notes+=label('boundary',x+width-120,y-12,'boundary traced');
      if(late)notes+=label('measure',270,270,`P ${v.perimeter} cm · A ${v.area} cm²`);
    }else if(scene.lesson===2){
      const x=80,y=35,unit=Math.min(340/v.length,180/v.width),w=v.length*unit,h=v.width*unit,cw=v.cut_width*unit,ch=v.cut_height*unit;
      const outline=[[x,y],[x+w-cw,y],[x+w-cw,y+ch],[x+w,y+ch],[x+w,y+h],[x,y+h]];
      drawing=path(outline,done>=3?'g9-area-filled':'')+
        label('outer-length',x+145,y+h+28,`${v.length} cm`)+label('outer-width',x-44,y+h/2,`${v.width} cm`)+
        label('cut-width',x+w-cw/2,y-7,`${v.cut_width} cm`)+label('cut-height',x+w-20,y+ch/2,`${v.cut_height} cm`);
      if(done>=2)notes+=rect(x+w-cw,y,cw,ch,'g9-area-cutout');
      if(late)notes+=label('measure',175,275,`A ${v.area} cm² · P ${v.perimeter} cm`);
    }else if(scene.lesson===3){
      const cx=250,cy=132,r=92;
      drawing=`<circle cx="${cx}" cy="${cy}" r="${r}" class="${done>=4?'g9-area-filled':''}"/>`+
        `<line x1="${cx}" y1="${cy}" x2="${cx+r}" y2="${cy}" class="g9-area-radius"/>`+
        label('centre',cx-12,cy-12,'O')+label('radius',cx+30,cy-8,`r = ${v.radius} cm`);
      if(done>=2)notes+=`<line x1="${cx-r}" y1="${cy}" x2="${cx+r}" y2="${cy}" class="g9-area-diameter"/>`;
      if(late)notes+=label('measure',115,270,`d ${v.diameter} cm · C ${v.circumference_coefficient}π cm · A ${v.area_coefficient}π cm²`);
    }else if(scene.lesson===4){
      const k=v.factor,newL=v.length*(v.mode==='both'||v.mode==='length_only'?k:1),newW=v.width*(v.mode==='both'||v.mode==='width_only'?k:1);
      const unit=Math.min(86/v.length,245/newL,150/newW),smallW=v.length*unit,smallH=v.width*unit,x=58,y=190;
      drawing=rect(x,y-smallH,smallW,smallH)+label('original',x,y+25,`${v.length} × ${v.width} cm`);
      if(done>=2){drawing+=rect(190,190-newW*unit,newL*unit,newW*unit,done>=4?'g9-area-filled':'')+
        label('scaled',190,216,`${newL} × ${newW} cm`);
        notes+=label('factor',105,65,`double ${v.mode.replaceAll('_',' ')}`)}
      if(late)notes+=label('measure',120,270,`P ${v.new_perimeter} cm · A ${v.new_area} cm²`);
    }else if(scene.lesson===5){
      const outerL=v.length+2*v.path,outerW=v.width+2*v.path,ratio=Math.min(340/outerL,170/outerW);
      const ow=outerL*ratio,oh=outerW*ratio,p=v.path*ratio,x=70,y=45;
      drawing=rect(x,y,ow,oh,done>=4?'g9-area-path':'')+rect(x+p,y+p,v.length*ratio,v.width*ratio,'g9-area-garden')+
        label('garden-length',x+p+v.length*ratio/2,y+p+v.width*ratio/2,`${v.length} m × ${v.width} m`)+
        label('path-width',x+8,y+oh/2,`${v.path} m path`);
      if(done>=2)notes+=label('outer-measure',225,245,`outer ${outerL} m × ${outerW} m`);
      if(late)notes+=label('measure',125,275,`path ${v.path_area} m² · fence ${v.fence} m`);
    }else throw Error('Unsupported measurement diagram');
    return `<svg viewBox="0 0 500 290" role="img" aria-label="${esc(scene.problem)}; ${late?'calculated measurements shown':'calculated measurements concealed'}"><title>Question-specific dimensions, with length and square units distinguished</title><g class="g9-area-shapes">${drawing}</g><g class="g9-area-notes">${notes}</g></svg>`;
  }
  for(let number=1;number<=5;number++)AthenaVisualizationRegistry.register('geometry',`grade9_area_${number}`,{
    render(params,state,phase){
      const scene=JSON.parse(params.scene_json),done=stage(state,phase);
      if(scene.lesson!==number||scene.id!==params.question_id)throw Error('Measurement diagram belongs to another question');
      return `<section class="g9-area-board" data-managed-visibility="true" data-question-id="${esc(params.question_id)}">
        <p data-object-id="problem" class="g9-area-question">${esc(params.prompt)}</p>
        <div data-object-id="model" class="g9-area-model">${draw(scene,done)}</div>
        <p data-object-id="operation">${phase==='operation'?esc(state.working_state):''}</p>
        <p data-object-id="result">${phase==='result'&&done<Number(params.total_steps)?esc(state.after_state):''}</p>
        <p data-object-id="verification">${phase==='result'&&done===Number(params.total_steps)?esc(state.after_state):''}</p>
      </section>`;
    },destroy(){}
  });
})();
