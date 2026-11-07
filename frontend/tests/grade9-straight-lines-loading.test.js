const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const root=path.resolve(__dirname,'../..');
const page=fs.readFileSync(path.join(root,'frontend/lesson.html'),'utf8');
const ops=vm.createContext({});vm.runInContext(fs.readFileSync(path.join(root,'frontend/js/whiteboard/animation-registry.js'),'utf8'),ops);
const visuals=new Map();vm.runInNewContext(fs.readFileSync(path.join(root,'frontend/js/visualization/geometry/grade9-straight-line-renderers.js'),'utf8'),{
 AthenaVisualizationRegistry:{register:(type,name,r)=>visuals.set(`${type}:${name}`,r)},
 escapeWhiteboardHtml:s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;'),Math
});
test('all 75 line-angle examples have a matching operation, question-owned diagram and staged target',()=>{
 assert.match(page,/grade9-straight-line-renderers\.js/);assert.match(page,/grade9-straight-lines\.css/);
 for(let lesson=1;lesson<=5;lesson++){
  const data=JSON.parse(fs.readFileSync(path.join(root,'backend/app/curriculum/grade9/generated',`straight_lines_${String(lesson).padStart(2,'0')}.json`),'utf8'));
  const op=vm.runInContext(`AthenaWhiteboardRegistry.resolve("grade9_lines_${lesson}_step")`,ops);
  const renderer=visuals.get(`geometry:grade9_lines_${lesson}`);assert.ok(renderer);
  for(const scene of data.worked){
   const params={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem,total_steps:scene.actions.length};
   const render=(n,phase)=>renderer.render(params,{annotations:[`stage:${n}`],working_state:scene.actions[n-1],after_state:scene.actions[n-1]},phase);
   let initial=render(0,'ready');assert.match(initial,/class="g9-lines-model"/);
   assert.match(initial,/data-object-id="angle-target"/);
   assert.match(initial,/not drawn to scale/);
   for(const tag of initial.matchAll(/<line[^>]*>/g))for(const coordinate of tag[0].matchAll(/(?:x1|x2|y1|y2)="(-?\d+(?:\.\d+)?)"/g)){
    const bound=coordinate[0].startsWith('y')?260:460;
    assert.ok(Number(coordinate[1])>=0&&Number(coordinate[1])<=bound,`${scene.id}: line clipped outside SVG`);
   }
   assert.match(initial,/data-object-id="angle-target"[^>]*>[^<]*x[^<]*<\/text>/,`${scene.id}: target leaked initially`);
   for(let i=1;i<=scene.actions.length;i++){
    const step={operation:{type:`grade9_lines_${lesson}_step`,value:scene.actions[i-1]},before_expression:i===1?'Question':scene.actions[i-2],after_expression:scene.actions[i-1]};
    assert.equal(op.render(step,'result',{hasVisualization:true}),'');
    assert.match(render(i,'result'),/data-object-id="model"/);
   }
   assert.match(render(scene.actions.length,'result'),/data-object-id="verification"/);
  }
 }
});
