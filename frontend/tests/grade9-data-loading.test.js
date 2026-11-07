const {test}=require('node:test');const assert=require('node:assert/strict');const fs=require('node:fs');const path=require('node:path');const vm=require('node:vm');
const root=path.resolve(__dirname,'../..');const page=fs.readFileSync(path.join(root,'frontend/lesson.html'),'utf8');
const ops=vm.createContext({});vm.runInContext(fs.readFileSync(path.join(root,'frontend/js/whiteboard/animation-registry.js'),'utf8'),ops);
const visuals=new Map();vm.runInNewContext(fs.readFileSync(path.join(root,'frontend/js/visualization/statistics/grade9-data-renderers.js'),'utf8'),{AthenaVisualizationRegistry:{register:(t,n,r)=>visuals.set(`${t}:${n}`,r)},escapeWhiteboardHtml:s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;'),Math});
test('all 120 data scenes use their datasets, axes and delayed conclusions',()=>{
 assert.match(page,/grade9-data-renderers\.js/);assert.match(page,/grade9-data\.css/);
 for(let n=1;n<=8;n++){
  const data=JSON.parse(fs.readFileSync(path.join(root,'backend/app/curriculum/grade9/generated',`data_${String(n).padStart(2,'0')}.json`),'utf8'));
  const op=vm.runInContext(`AthenaWhiteboardRegistry.resolve("grade9_data_${n}_step")`,ops),renderer=visuals.get(`statistics:grade9_data_${n}`);assert.ok(renderer);
  for(const scene of data.worked){
   const params={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem,total_steps:5};
   const render=(i,phase)=>renderer.render(params,{annotations:[`stage:${i}`],working_state:scene.actions[Math.max(0,i-1)],after_state:scene.actions[Math.max(0,i-1)]},phase);
   const initial=render(0,'ready');assert.match(initial,/data-object-id="model"/);assert.match(initial,/data-object-id="problem"/);assert.doesNotMatch(initial,/data-object-id="verification"[^>]*>[^<]+/);
   let previous=initial;
   for(let i=1;i<=5;i++){
    assert.equal(op.render({operation:{type:`grade9_data_${n}_step`,value:scene.actions[i-1]},before_expression:'before',after_expression:'after'},'result',{hasVisualization:true}),'');
    const current=render(i,'result');assert.match(current,/data-object-id="model"/);
    assert.notEqual(current.match(/<div data-object-id="model"[\s\S]*?<\/div>/)[0],previous.match(/<div data-object-id="model"[\s\S]*?<\/div>/)[0],`${scene.id}: visual stage ${i} did not change`);
    previous=current;
   }
   assert.match(render(5,'result'),/data-object-id="verification"/);assert.notEqual(initial,render(5,'result'));
   const preview=JSON.parse(JSON.stringify(scene));for(const key of ['answer','actions','check'])delete preview[key];
   for(const key of ['young_pick','old_pick','total','mode','median','mean_rounded','range','outlier','gain_a','gain_b','modal_interval','walk_angle_num','walk_angle_den','prediction','difference','percent'])delete preview.visual.values[key];
   assert.match(renderer.render({...params,scene_json:JSON.stringify(preview)},{annotations:[],working_state:'',after_state:''},'ready'),/data-object-id="model"/);
  }
 }
});
