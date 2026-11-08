const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'../..'),page=fs.readFileSync(path.join(root,'frontend/lesson.html'),'utf8');
const ops=vm.createContext({});vm.runInContext(fs.readFileSync(path.join(root,'frontend/js/whiteboard/animation-registry.js'),'utf8'),ops);
const visuals=new Map();vm.runInNewContext(fs.readFileSync(path.join(root,'frontend/js/visualization/geometry/grade9-surface-volume-renderers.js'),'utf8'),{AthenaVisualizationRegistry:{register:(t,n,r)=>visuals.set(`${t}:${n}`,r)},escapeWhiteboardHtml:s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;'),Math});
test('all 90 surface/volume examples reveal five question-specific visual states',()=>{
 assert.match(page,/grade9-surface-volume-renderers\.js/);assert.match(page,/grade9-surface-volume\.css/);
 for(let n=1;n<=6;n++){
  const data=JSON.parse(fs.readFileSync(path.join(root,'backend/app/curriculum/grade9/generated',`surface_volume_${String(n).padStart(2,'0')}.json`),'utf8'));
  const op=vm.runInContext(`AthenaWhiteboardRegistry.resolve("grade9_surface_${n}_step")`,ops),renderer=visuals.get(`geometry:grade9_surface_${n}`);assert.ok(renderer);
  for(const scene of data.worked){
   const params={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem,total_steps:5};
   const render=(i,phase,p=params)=>renderer.render(p,{annotations:[`stage:${i}`],working_state:scene.actions[Math.max(0,i-1)],after_state:scene.actions[Math.max(0,i-1)]},phase);
   const initial=render(0,'ready');assert.match(initial,/data-object-id="model"/);assert.doesNotMatch(initial,/data-object-id="verification"[^>]*>[^<]+/);
   let previous=initial;
   for(let i=1;i<=5;i++){
    assert.equal(op.render({operation:{type:`grade9_surface_${n}_step`,value:scene.actions[i-1]},before_expression:'before',after_expression:'after'},'result',{hasVisualization:true}),'');
    const current=render(i,'result');assert.notEqual(current.match(/<div data-object-id="model"[\s\S]*?<\/div>/)[0],previous.match(/<div data-object-id="model"[\s\S]*?<\/div>/)[0],`${scene.id}: stage ${i} unchanged`);previous=current;
   }
   assert.match(render(5,'result'),/data-object-id="verification"[^>]*>Check/);
   const preview=JSON.parse(JSON.stringify(scene));for(const key of ['answer','actions','check'])delete preview[key];
   for(const key of ['surface_area','volume','volume_pi','surface_area_pi','triangle_area','capacity_num','capacity_den','original','new_volume','factor','litres_num','litres_den','correct_value'])delete preview.visual.values[key];
   assert.match(render(0,'ready',{...params,scene_json:JSON.stringify(preview)}),/data-object-id="model"/);
   assert.throws(()=>render(0,'ready',{...params,question_id:'foreign'}),/another question/);
  }
 }
});
test('open-top boxes omit the top; cylinder nets preserve the two discs and curved wall',()=>{
 const data=JSON.parse(fs.readFileSync(path.join(root,'backend/app/curriculum/grade9/generated/surface_volume_06.json'),'utf8'));
 const renderer=visuals.get('geometry:grade9_surface_6');const scene=data.worked[0];
 const params={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem,total_steps:5};
 const open=renderer.render(params,{annotations:['stage:4'],after_state:'material area'},'result');assert.doesNotMatch(open,/data-object-id="opposite-base"/);assert.match(open,/One base and four sides|Material =/);
 const cylinder=data.worked[2];const cparams={...params,scene_json:JSON.stringify(cylinder),question_id:cylinder.id,prompt:cylinder.problem};
 const surface=renderer.render(cparams,{annotations:['stage:4'],after_state:'answer'},'result');assert.match(surface,/data-object-id="circle-top"/);assert.match(surface,/data-object-id="unwrapped-wall"/);
});
