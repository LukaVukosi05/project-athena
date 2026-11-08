const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const renderers={};const ctx={escapeWhiteboardHtml:s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('"','&quot;'),AthenaVisualizationRegistry:{register:(d,k,r)=>renderers[k]=r}};
vm.runInNewContext(fs.readFileSync(path.join(__dirname,'../js/visualization/algebra/grade10-equation-renderers.js'),'utf8'),ctx);
test('all Grade 10 equation examples use question data and reveal five different stages',()=>{
 for(let n=1;n<=9;n++){
  const data=JSON.parse(fs.readFileSync(path.join(__dirname,`../../backend/app/curriculum/grade10/generated/eei_${String(n).padStart(2,'0')}.json`)));
  for(const scene of data.worked){
   const p={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem};
   const state=i=>({annotations:[`stage:${i}`],working_state:scene.actions[i-1],after_state:scene.actions[i-1]});
   const start=renderers[`grade10_eei_${n}`].render(p,state(1),'initial');
   const middle=renderers[`grade10_eei_${n}`].render(p,state(3),'result');
   const end=renderers[`grade10_eei_${n}`].render(p,state(5),'result');
   assert.ok(start.includes(scene.id)&&start.includes('data-object-id="model"'));
   assert.ok(!start.includes('data-object-id="derived"')&&!start.includes('data-object-id="interval"'));
   assert.notEqual(start,middle);assert.notEqual(middle,end);
   assert.ok(end.includes(scene.answer));
  }
 }
});
