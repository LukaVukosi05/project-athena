const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'../..'),page=fs.readFileSync(path.join(root,'frontend/lesson.html'),'utf8');
const ops=vm.createContext({});vm.runInContext(fs.readFileSync(path.join(root,'frontend/js/whiteboard/animation-registry.js'),'utf8'),ops);
const visuals=new Map();vm.runInNewContext(fs.readFileSync(path.join(root,'frontend/js/visualization/statistics/grade9-probability-renderers.js'),'utf8'),{AthenaVisualizationRegistry:{register:(t,n,r)=>visuals.set(`${t}:${n}`,r)},escapeWhiteboardHtml:s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;'),Math});
test('all 75 probability scenes are question-specific and reveal five distinct states',()=>{
 assert.match(page,/grade9-probability-renderers\.js/);assert.match(page,/grade9-probability\.css/);
 for(let n=1;n<=5;n++){
  const data=JSON.parse(fs.readFileSync(path.join(root,'backend/app/curriculum/grade9/generated',`probability_${String(n).padStart(2,'0')}.json`),'utf8'));
  const op=vm.runInContext(`AthenaWhiteboardRegistry.resolve("grade9_probability_${n}_step")`,ops),renderer=visuals.get(`statistics:grade9_probability_${n}`);assert.ok(renderer);
  for(const scene of data.worked){
   const params={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem,total_steps:5};
   const render=(i,phase,p=params)=>renderer.render(p,{annotations:[`stage:${i}`],working_state:scene.actions[Math.max(0,i-1)],after_state:scene.actions[Math.max(0,i-1)]},phase);
   const initial=render(0,'ready');assert.match(initial,/data-object-id="model"/);assert.doesNotMatch(initial,/data-object-id="verification"[^>]*>[^<]+/);
   let previous=initial;
   for(let i=1;i<=5;i++){
    assert.equal(op.render({operation:{type:`grade9_probability_${n}_step`,value:scene.actions[i-1]},before_expression:'before',after_expression:'after'},'result',{hasVisualization:true}),'');
    const current=render(i,'result');assert.notEqual(current.match(/<div data-object-id="model"[\s\S]*?<\/div>/)[0],previous.match(/<div data-object-id="model"[\s\S]*?<\/div>/)[0],`${scene.id}: visual stage ${i} unchanged`);previous=current;
   }
   assert.match(render(5,'result'),/data-object-id="verification"[^>]*>Check/);
   const preview=JSON.parse(JSON.stringify(scene));for(const key of ['answer','actions','check'])delete preview[key];
   for(const key of ['favourable','row_total','column_total','grand_total','first_red_num','first_red_den','second_red_num','second_red_den','prob_num','prob_den','tails','predicted_heads','multiples_of_three','favourable_pairs','total_pairs'])delete preview.visual.values[key];
   assert.match(render(0,'ready',{...params,scene_json:JSON.stringify(preview)}),/data-object-id="model"/);
   assert.throws(()=>render(0,'ready',{...params,question_id:'foreign'}),/another question/);
  }
 }
});
