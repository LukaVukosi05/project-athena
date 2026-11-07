const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const root=path.resolve(__dirname,'../..');
const page=fs.readFileSync(path.join(root,'frontend/lesson.html'),'utf8');
const registry=vm.createContext({});
vm.runInContext(fs.readFileSync(path.join(root,'frontend/js/whiteboard/animation-registry.js'),'utf8'),registry);
const visuals=new Map();
vm.runInNewContext(fs.readFileSync(path.join(root,'frontend/js/visualization/graphs/grade9-graph-renderers.js'),'utf8'),{
 AthenaVisualizationRegistry:{register:(type,name,r)=>visuals.set(`${type}:${name}`,r)},
 escapeWhiteboardHtml:s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;')
});
const count=html=>(html.match(/class="g9-gr-point"/g)||[]).length;
test('all 105 graph examples load and reveal points without erasing earlier marks',()=>{
 assert.match(page,/grade9-graph-renderers\.js/);assert.match(page,/grade9-graphs\.css/);
 for(let lesson=1;lesson<=7;lesson++){
  const data=JSON.parse(fs.readFileSync(path.join(root,'backend/app/curriculum/grade9/generated',`graphs_${String(lesson).padStart(2,'0')}.json`),'utf8'));
  const op=vm.runInContext(`AthenaWhiteboardRegistry.resolve("grade9_graph_${lesson}_step")`,registry);
  const renderer=visuals.get(`algebra:grade9_graph_${lesson}`);assert.ok(renderer);
  for(const scene of data.worked){
   const params={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem,total_steps:scene.actions.length};
   let prior=renderer.render(params,{annotations:['stage:0']},'ready');assert.equal(count(prior),0,scene.id);
   assert.ok(!prior.includes(scene.answer),`${scene.id}: leaked answer`);
   for(let i=1;i<=scene.actions.length;i++){
    const step={operation:{type:`grade9_graph_${lesson}_step`,value:scene.actions[i-1]},before_expression:i===1?'Question':scene.actions[i-2],working_expression:scene.actions[i-1],after_expression:scene.actions[i-1]};
    assert.equal(op.render(step,'operation',{hasVisualization:true}),'');
    const html=renderer.render(params,{annotations:[`stage:${i}`],working_state:scene.actions[i-1],after_state:scene.actions[i-1]},'result');
    assert.ok(count(html)>=count(prior),`${scene.id}: lost plotted point at ${i}`);prior=html;
   }
   assert.ok(count(prior)>=2,`${scene.id}: missing final graph`);
  }
 }
});
