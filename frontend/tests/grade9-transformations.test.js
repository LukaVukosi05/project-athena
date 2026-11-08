const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const base=require('node:path').join(__dirname,'../../backend/app/curriculum/grade9/generated');
const renderers={};const ctx={escapeWhiteboardHtml:s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('"','&quot;'),AthenaVisualizationRegistry:{register:(domain,template,renderer)=>renderers[template]=renderer}};
vm.runInNewContext(fs.readFileSync(require('node:path').join(__dirname,'../js/visualization/geometry/grade9-transformation-renderers.js'),'utf8'),ctx);
test('all 105 question-specific diagrams retain original and reveal image in order',()=>{
 for(let n=1;n<=7;n++){
  const data=JSON.parse(fs.readFileSync(require('node:path').join(base,`transformation_${String(n).padStart(2,'0')}.json`)));
  assert.equal(data.worked.length,15);
  for(const scene of data.worked){
   const params={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem};
   const state=i=>({annotations:[`stage:${i}`],working_state:scene.actions[i-1]||'',after_state:scene.actions[i-1]||''});
   const initial=renderers[`grade9_transform_${n}`].render(params,state(1),'initial');
   const original=renderers[`grade9_transform_${n}`].render(params,state(1),'result');
   const first=renderers[`grade9_transform_${n}`].render(params,state(3),'result');
   const final=renderers[`grade9_transform_${n}`].render(params,state(5),'result');
   assert.ok(!initial.includes('image-polygon')&&!initial.includes('original-polygon'));
   assert.ok(original.includes('original-polygon')&&!original.includes('image-polygon'));
   assert.ok(first.includes('A′')&&!first.includes('image-polygon'));
   assert.ok(final.includes('image-polygon')&&final.includes('B′')&&final.includes('C′'));
   assert.ok(final.includes(`data-question-id="${scene.id}"`));
  }
 }
});
