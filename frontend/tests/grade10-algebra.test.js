const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const renderers={};const ctx={escapeWhiteboardHtml:s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('"','&quot;'),AthenaVisualizationRegistry:{register:(d,k,r)=>renderers[k]=r}};
vm.runInNewContext(fs.readFileSync(path.join(__dirname,'../js/visualization/algebra/grade10-algebra-renderers.js'),'utf8'),ctx);
test('six distinct Grade 10 visuals reveal derived parts only at their stage',()=>{
 for(let n=1;n<=6;n++){
  const source=JSON.parse(fs.readFileSync(path.join(__dirname,`../../backend/app/curriculum/grade10/generated/algebra_${String(n).padStart(2,'0')}.json`)));
  assert.equal(source.worked.length,15);
  for(const scene of source.worked){
   const params={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem};
   const state=step=>({annotations:[`stage:${step}`],working_state:scene.actions[step-1],after_state:scene.actions[step-1]});
   const first=renderers[`grade10_algebra_${n}`].render(params,state(1),'initial');
   const later=renderers[`grade10_algebra_${n}`].render(params,state(4),'result');
   assert.ok(first.includes(scene.id)&&first.includes('data-object-id="model"'));
   assert.ok(!first.includes('g10-active')&&!first.includes('data-object-id="restriction"'));
   assert.ok(later.includes('data-object-id="model"')&&later!==first);
  }
 }
});
