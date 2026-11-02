const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const root=path.resolve(__dirname,'../..');
global.escapeWhiteboardHtml=value=>String(value).replace(/[&<>"']/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
for(const name of ['visualization-registry.js','graphs/grade8-coordinate-renderer.js'])
  vm.runInThisContext(fs.readFileSync(path.join(root,'frontend/js/visualization',name),'utf8'));
const scenes=JSON.parse(fs.readFileSync(path.join(root,'docs/curriculum/grade8/graphs/lesson-02-scenes.json'),'utf8')).scenes;
function render(scene,stage,phase){
  const block={representation:'visual',id:`${scene.id}-board`,visualization:{type:'coordinate_geometry',template:'grade8_coordinate_plane',parameters:{scene}}};
  const session=AthenaVisualizationResolver.resolve(block,{question_id:scene.id});
  assert.ok(session.instruction);
  return session.render({visualization_state:{annotations:[`stage:${stage}`]}},phase);
}
test('all 15 graphs consume their current table and keep previous points visible',()=>{
  assert.equal(scenes.length,15);
  assert.equal(new Set(scenes.map(scene=>JSON.stringify({points:scene.graph.points,mode:scene.graph.mode}))).size,15);
  for(const scene of scenes){
    const initial=render(scene,1,'ready');
    assert.match(initial,/data-object-id="x-axis"/);
    assert.match(initial,/data-object-id="y-axis"/);
    if(scene.graph.mode!=='given_line')assert.doesNotMatch(initial,/class="coord-graph-line"/);
    for(const point of scene.derived) assert.doesNotMatch(initial,new RegExp(`>${point.label} \\(`));
    const final=render(scene,4,'result');
    for(const point of scene.derived) assert.ok(final.includes(`${point.label} (${point.x}, ${point.y})`),scene.id);
    if(scene.derived.length>1 && scene.derived[0].reveal_step<4){
      assert.match(render(scene,4,'ready'),/data-object-id="point-1"/);
      assert.match(render(scene,4,'operation'),/data-object-id="point-1"/);
    }
  }
});
test('straight lines appear only after the final step; discrete and nonlinear stay separate',()=>{
  for(const scene of scenes){
    const initial=render(scene,1,'ready');
    const operation=render(scene,4,'operation');
    const result=render(scene,4,'result');
    if(scene.graph.mode==='given_line')assert.match(initial,/data-object-id="graph-line"/);
    else if(['line','error'].includes(scene.graph.mode))assert.match(operation,/coord-graph-line--drawing/);
    else assert.doesNotMatch(operation,/data-object-id="graph-line"/);
    if(['line','given_line','error'].includes(scene.graph.mode))assert.match(result,/data-object-id="graph-line"/);
    else assert.doesNotMatch(result,/data-object-id="graph-line"/);
  }
  assert.equal(scenes[11].graph.mode,'discrete');
  assert.equal(scenes[14].graph.mode,'nonlinear');
});
test('a learner error stays visible beside the corrected point and data changes change coordinates',()=>{
  const scene=scenes[10];
  const initial=render(scene,1,'ready'),final=render(scene,4,'result');
  assert.match(initial,/Learner C/);
  assert.doesNotMatch(initial,/C \(2, 5\)/);
  assert.match(final,/C \(2, 5\)/);
  assert.match(final,/Learner C/);
  const changed=structuredClone(scenes[0]);
  changed.graph.table[1].y=4;
  assert.throws(()=>render(changed,4,'result'),/Graph and table disagree/);
});

test('the real whiteboard keeps plotted points while the written solution grows',()=>{
  global.matchMedia=()=>({matches:false});
  global.CSS={escape:value=>value};
  global.AthenaWhiteboardRegistry={resolve(){return {render(){return '';}};}};
  vm.runInThisContext(fs.readFileSync(path.join(root,'frontend/js/whiteboard/stateful-whiteboard.js'),'utf8'));
  const scene=scenes[0], stages=[1,2,3,4];
  const block={id:`${scene.id}-board`,representation:'visual',initial_expression:'Read the labelled axes',
    visualization:{type:'coordinate_geometry',template:'grade8_coordinate_plane',parameters:{scene,prompt:'Plot the coordinates',question_id:scene.id,total_steps:4}},
    steps:stages.map(n=>({id:`step-${n}`,operation:{type:'test'},events:[],screen_reader_description:`Stage ${n}`,
      working_expression:`Move to stage ${n}`,after_expression:`Stage ${n} complete`,
      visualization_state:{annotations:[`stage:${n}`],before_state:`Before ${n}`,working_state:`Move ${n}`,after_state:`After ${n}`}}))};
  const tracePane={scrollTop:0,scrollHeight:400};
  const stage={innerHTML:'',dataset:{},setAttribute(){},querySelector(selector){return selector==='.g8-completed-steps'?tracePane:null;}};
  const board=Object.create(StatefulWhiteboard.prototype);
  Object.assign(board,{block,index:0,visualSession:AthenaVisualizationResolver.resolve(block),
    mount:{querySelector(selector){if(selector==='.whiteboard-stage')return stage;if(selector==='[data-role="checkpoint"]')return {hidden:false};return null;}},
    stopTimeline(){},renderTeachingNotes(){},renderOpeningCaption(){},setStatus(){}});
  board.reconstruct('ready','idle');
  assert.equal(stage.dataset.layout,'graph');
  assert.match(stage.innerHTML,/class="grade8-coordinate-plane"/);
  assert.doesNotMatch(stage.innerHTML,/data-object-id="point-1"/);
  board.index=2;
  board.reconstruct('operation','playing');
  assert.match(stage.innerHTML,/data-object-id="point-1"/);
  assert.match(stage.innerHTML,/data-object-id="point-2"/);
  assert.doesNotMatch(stage.innerHTML,/data-object-id="point-3"/);
  assert.match(stage.innerHTML,/data-object-id="x-guide-3"/);
  board.reconstruct('result','step_complete');
  assert.match(stage.innerHTML,/data-object-id="point-1"/);
  assert.match(stage.innerHTML,/data-object-id="point-3"/);
  assert.match(stage.innerHTML,/A \(0, 1\)/);
  assert.match(stage.innerHTML,/Stage 3 complete/);
  board.index=3;
  board.reconstruct('ready','idle');
  assert.match(stage.innerHTML,/data-object-id="point-1"/);
  assert.match(stage.innerHTML,/data-object-id="point-2"/);
  assert.match(stage.innerHTML,/Stage 3 complete/);
  board.reconstruct('result','example_complete');
  assert.match(stage.innerHTML,/data-object-id="point-3"/);
  assert.match(stage.innerHTML,/Stage 4 complete/);
  assert.equal(tracePane.scrollTop,400);
  const css=fs.readFileSync(path.join(root,'frontend/css/components.css'),'utf8');
  assert.match(css,/\.whiteboard-stage\[data-layout="graph"\][^{]*\{display:grid;grid-template-columns:minmax\(0,1\.55fr\) minmax\(265px,\.85fr\)/);
});
test('each table point appears in its own step, with both guides animated first',()=>{
  for(const scene of scenes){
    for(const point of scene.derived){
      const before=render(scene,point.reveal_step,'ready');
      const working=render(scene,point.reveal_step,'operation');
      const after=render(scene,point.reveal_step,'result');
      assert.doesNotMatch(before,new RegExp(`>${point.label} \\(${point.x}, ${point.y}\\)`),scene.id);
      assert.match(working,/coord-guide--fresh-x|coord-guide--fresh-y/,scene.id);
      assert.match(working,/coord-preview/,scene.id);
      assert.match(after,new RegExp(`${point.label} \\(${point.x}, ${point.y}\\)`),scene.id);
    }
  }
});
