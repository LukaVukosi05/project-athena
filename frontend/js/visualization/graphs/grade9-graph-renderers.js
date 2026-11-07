/* Question-owned Cartesian diagrams. Axes and revealed marks persist across steps. */
(() => {
  const esc=value=>escapeWhiteboardHtml(String(value??''));
  function stage(state,phase){
    const note=(state.annotations||[]).find(value=>/^stage:\d+$/.test(value));
    const n=note?Number(note.slice(6)):0;
    return phase==='result'?n:Math.max(0,n-1);
  }
  function plot(scene,number,done){
    const visual=scene.visual||{},v=visual.values||{},all=v.points||[];
    let shown=[];
    if(number===1)shown=all.slice(0,Math.min(done,4));
    else if(number===2)shown=all.slice(0,Math.min(done,4));
    else if(number===3)shown=all.slice(0,Math.min(done,2));
    else if(number===4)shown=[...(done>=2?[all[1]]:[]),...(done>=4?[all[0]]:[])];
    else if(number===5)shown=all.slice(0,done<2?0:done===2?1:done===3?2:done===4?3:4);
    else shown=all.slice(0,Math.min(done,3));
    const xvals=all.map(p=>p[0]),yvals=all.map(p=>p[1]);
    let xmin=Math.min(-1,...xvals)-1,xmax=Math.max(1,...xvals)+1,
        ymin=Math.min(-1,...yvals)-1,ymax=Math.max(1,...yvals)+1;
    const width=420,height=300,left=45,right=22,top=18,bottom=36;
    const X=x=>left+(x-xmin)*(width-left-right)/(xmax-xmin);
    const Y=y=>height-bottom-(y-ymin)*(height-top-bottom)/(ymax-ymin);
    const ticks=(lo,hi)=>{const inc=Math.max(1,Math.ceil((hi-lo)/12));let values=[];for(let n=Math.ceil(lo/inc)*inc;n<=hi;n+=inc)values.push(n);return values;};
    const grid=ticks(xmin,xmax).map(x=>`<line x1="${X(x)}" y1="${top}" x2="${X(x)}" y2="${height-bottom}" class="g9-gr-grid"/><text x="${X(x)}" y="${height-10}" text-anchor="middle">${x}</text>`).join('')+
      ticks(ymin,ymax).map(y=>`<line x1="${left}" y1="${Y(y)}" x2="${width-right}" y2="${Y(y)}" class="g9-gr-grid"/><text x="${left-7}" y="${Y(y)+4}" text-anchor="end">${y}</text>`).join('');
    const lineReady=number===1?shown.length>=2:number===5?done>=6:(number===6||number===7)?done>=3:done>=2 && number!==2?true:done>=4;
    const path=lineReady&&shown.length>=2?`<polyline class="g9-gr-path" points="${shown.map(([x,y])=>`${X(x)},${Y(y)}`).join(' ')}"/>`:'';
    const marks=shown.map(([x,y],i)=>`<g class="g9-gr-point"><circle cx="${X(x)}" cy="${Y(y)}" r="5"/><text x="${X(x)+8}" y="${Y(y)-9}">(${x}, ${y})</text></g>`).join('');
    let triangle='';
    if(number===3&&done>=4&&all.length===2){const [[a,b],[c,d]]=all;
      triangle=`<path class="g9-gr-triangle" d="M ${X(a)} ${Y(b)} L ${X(c)} ${Y(b)} L ${X(c)} ${Y(d)}"/><text x="${(X(a)+X(c))/2}" y="${Y(b)+18}" text-anchor="middle">run ${v.run}</text><text x="${X(c)+6}" y="${(Y(b)+Y(d))/2}">rise ${v.rise}</text>`;}
    const title=number===1?'Tank reading (litres) against time (hours)':'Coordinate plane with x and y axes';
    return `<svg viewBox="0 0 ${width} ${height}" role="img" aria-label="${esc(title)}; ${shown.length} of ${all.length} points shown" preserveAspectRatio="xMidYMid meet">
      <title>${esc(title)}</title>${grid}<line x1="${X(0)}" y1="${top}" x2="${X(0)}" y2="${height-bottom}" class="g9-gr-axis"/><line x1="${left}" y1="${Y(0)}" x2="${width-right}" y2="${Y(0)}" class="g9-gr-axis"/>${path}${triangle}${marks}<text x="${width-12}" y="${Y(0)-7}">x</text><text x="${X(0)+7}" y="${top+7}">y</text></svg>`;
  }
  for(let number=1;number<=7;number++)AthenaVisualizationRegistry.register('algebra',`grade9_graph_${number}`,{
    render(params,state,phase){
      const scene=JSON.parse(params.scene_json),done=stage(state,phase);
      if(scene.lesson!==number)throw Error('The graph belongs to another lesson');
      return `<section class="g9-gr-board" data-managed-visibility="true" data-question-id="${esc(params.question_id)}">
        <p data-object-id="problem" class="g9-gr-question">${esc(params.prompt)}</p>
        <div data-object-id="model" class="g9-gr-model">${plot(scene,number,done)}</div>
        <p data-object-id="operation" class="g9-gr-operation">${phase==='operation'?esc(state.working_state):''}</p>
        <p data-object-id="result" class="g9-gr-result">${phase==='result'&&done<Number(params.total_steps)?esc(state.after_state):''}</p>
        <p data-object-id="verification" class="g9-gr-verification">${phase==='result'&&done===Number(params.total_steps)?esc(state.after_state):''}</p>
      </section>`;
    },destroy(){}
  });
})();
