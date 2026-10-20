const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const registered=new Map(),context={AthenaVisualizationRegistry:{register(type,name,renderer){registered.set(`${type}:${name}`,renderer);}},escapeWhiteboardHtml:x=>String(x??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))};
vm.runInNewContext(fs.readFileSync(path.join(__dirname,'../js/visualization/algebra/grade8-equation-renderers.js'),'utf8'),context);
const payload=JSON.parse(fs.readFileSync(path.join(__dirname,'../../backend/app/curriculum/grade8/generated/lesson_02.json'),'utf8'));
const state=(before,working,after,index)=>({before_state:before,working_state:working,after_state:after,annotations:[`stage:${index}`]});
test('all four inspection models use their current question and hide answers initially',()=>{
 const families=new Set(payload.worked_examples.map(x=>x.renderer));assert.equal(families.size,4);
 for(const item of payload.worked_examples){
  const renderer=registered.get(item.renderer),params={prompt:item.prompt,source_data:item.question_data,question_id:item.id,total_steps:3};assert.ok(renderer,item.id);
  const ready=renderer.render(params,state(item.prompt,'test',item.answer,0),'ready');
  const working=renderer.render(params,state(item.prompt,'test',item.answer,1),'operation');
  const result=renderer.render(params,state(item.prompt,'test',item.answer,1),'result');
  assert.notEqual(ready,working,item.id);assert.notEqual(working,result,item.id);
  assert.match(ready,/data-object-id="problem"/);assert.match(result,/data-object-id="result"/);
  assert.match(ready,/g8-result is-hidden/);assert.match(result,/g8-result is-visible/);
  assert.doesNotMatch(ready,/g8-result is-visible/);
 }
});
test('candidate table reveals rows one at a time and geometry keeps its units',()=>{
 const item=payload.worked_examples[11],renderer=registered.get(item.renderer),params={prompt:item.prompt,source_data:item.question_data,question_id:item.id,total_steps:4};
 const initial=renderer.render(params,state(item.prompt,'test','x = 6',1),'ready');
 const first=renderer.render(params,state(item.prompt,'test','x = 4 → 11 ≠ 13',1),'result');
 const third=renderer.render(params,state('x = 5 → 13 ≠ 14','test','x = 6 → 15 = 15',3),'result');
 assert.doesNotMatch(initial,/x = 6/);assert.match(first,/x = 4/);assert.doesNotMatch(first,/x = 6/);assert.match(third,/x = 6/);
 const rect=payload.worked_examples[12],geometry=registered.get(rect.renderer),rp={prompt:rect.prompt,source_data:rect.question_data,question_id:rect.id,total_steps:3};
 assert.match(geometry.render(rp,state('Rectangle: width 5 cm; area 60 cm²','Area = length × width','length × 5 cm = 60 cm²',1),'ready'),/60 cm²/);
 assert.match(geometry.render(rp,state('length × 5 cm = 60 cm²','find length','length = 12 cm',2),'result'),/12 cm/);
});
test('number line conceals the missing start until inspection finds it',()=>{
 const item=payload.worked_examples[1],renderer=registered.get(item.renderer),params={prompt:item.prompt,source_data:item.question_data,question_id:item.id,total_steps:3};
 const first=renderer.render(params,state('y − 7 = 5','count forward','5 + 7 = 12',1),'ready');
 const found=renderer.render(params,state('y − 7 = 5','count forward','5 + 7 = 12',1),'result');
 assert.doesNotMatch(first,/<text[^>]*>12<\/text>/);assert.match(found,/<text[^>]*>12<\/text>/);
});
