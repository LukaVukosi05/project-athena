const {test}=require('node:test');const assert=require('node:assert/strict');const fs=require('node:fs');const path=require('node:path');const vm=require('node:vm');
const root=path.resolve(__dirname,'../..');const page=fs.readFileSync(path.join(root,'frontend/lesson.html'),'utf8');const ops=vm.createContext({});
vm.runInContext(fs.readFileSync(path.join(root,'frontend/js/whiteboard/animation-registry.js'),'utf8'),ops);
const visuals=new Map();vm.runInNewContext(fs.readFileSync(path.join(root,'frontend/js/visualization/geometry/grade9-area-renderers.js'),'utf8'),{AthenaVisualizationRegistry:{register:(t,n,r)=>visuals.set(`${t}:${n}`,r)},escapeWhiteboardHtml:s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;'),Math});
test('75 measurement scenes draw their own dimensions and reveal results at the last calculation',()=>{
 assert.match(page,/grade9-area-renderers\.js/);assert.match(page,/grade9-area\.css/);
 for(let n=1;n<=5;n++){
  const data=JSON.parse(fs.readFileSync(path.join(root,'backend/app/curriculum/grade9/generated',`area_${String(n).padStart(2,'0')}.json`),'utf8'));
  const op=vm.runInContext(`AthenaWhiteboardRegistry.resolve("grade9_area_${n}_step")`,ops),renderer=visuals.get(`geometry:grade9_area_${n}`);assert.ok(renderer);
  for(const scene of data.worked){
   const params={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem,total_steps:5};
   const render=(i,phase)=>renderer.render(params,{annotations:[`stage:${i}`],working_state:scene.actions[Math.max(0,i-1)],after_state:scene.actions[Math.max(0,i-1)]},phase);
   const initial=render(0,'ready');assert.match(initial,/data-object-id="model"/);assert.match(initial,/data-object-id="problem"/);assert.doesNotMatch(initial,/data-object-id="measure"/);
   for(const tag of initial.matchAll(/<(?:rect|circle|line|text)[^>]*>/g))for(const m of tag[0].matchAll(/(?:x1|x2|y1|y2|x|y|cx|cy)="(-?\d+(?:\.\d+)?)"/g))assert.ok(Number(m[1])>=0&&Number(m[1])<=500,`${scene.id}: clipped coordinate`);
   for(let i=1;i<=5;i++){assert.equal(op.render({operation:{type:`grade9_area_${n}_step`,value:scene.actions[i-1]},before_expression:'before',after_expression:'after'},'result',{hasVisualization:true}),'');assert.match(render(i,'result'),/data-object-id="model"/)}
   assert.match(render(5,'result'),/data-object-id="verification"/);assert.notEqual(initial,render(5,'result'));
   const preview=JSON.parse(JSON.stringify(scene));delete preview.answer;delete preview.actions;delete preview.check;
   for(const key of ['area','perimeter','diameter','circumference_coefficient','area_coefficient','old_perimeter','old_area','new_perimeter','new_area','scaled_length','scaled_width','outer_length','outer_width','path_area','fence'])delete preview.visual.values[key];
   assert.match(renderer.render({...params,scene_json:JSON.stringify(preview)},{annotations:[],working_state:'',after_state:''},'ready'),/data-object-id="model"/);
  }
 }
});
