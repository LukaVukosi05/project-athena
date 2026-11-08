const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const renderers={};const ctx={escapeWhiteboardHtml:s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('"','&quot;'),AthenaVisualizationRegistry:{register:(d,k,r)=>renderers[k]=r}};
vm.runInNewContext(fs.readFileSync(path.join(__dirname,'../js/visualization/geometry/grade10-trigonometry-renderers.js'),'utf8'),ctx);
test('105 trigonometry examples reveal question-specific triangle or coordinate stages',()=>{
 for(let n=1;n<=7;n++){
  const data=JSON.parse(fs.readFileSync(path.join(__dirname,`../../backend/app/curriculum/grade10/generated/trig_${String(n).padStart(2,'0')}.json`)));
  for(const scene of data.worked){
   const p={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem};
   const state=i=>({annotations:[`stage:${i}`],working_state:scene.actions[i-1],after_state:scene.actions[i-1]});
   const initial=renderers[`grade10_trig_${n}`].render(p,state(1),'initial');
   const middle=renderers[`grade10_trig_${n}`].render(p,state(3),'result');
   const final=renderers[`grade10_trig_${n}`].render(p,state(5),'result');
   assert.ok(initial.includes(scene.id)&&initial.includes('data-object-id="model"'));
   assert.ok(!initial.includes('data-object-id="answer"'));
   assert.notEqual(initial,middle);assert.notEqual(middle,final);
   assert.ok(final.includes('data-object-id="answer"'));
   assert.ok(!final.includes('undefined/undefined'));
   if(n===7){assert.ok(middle.includes('data-object-id="point"'));assert.ok(middle.includes('data-object-id="vertical-leg"'))}
  }
 }
});
