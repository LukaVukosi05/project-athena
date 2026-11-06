const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
global.escapeWhiteboardHtml=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
for(const file of ['visualization-registry.js','algebra/grade9-expression-renderers.js'])vm.runInThisContext(fs.readFileSync(path.join(__dirname,'../js/visualization',file),'utf8'));
let total=0;
for(let n=1;n<=9;n++){
 const bank=JSON.parse(fs.readFileSync(path.join(__dirname,`../../backend/app/curriculum/grade9/generated/expressions_${String(n).padStart(2,'0')}.json`),'utf8'));
 const renderer=AthenaVisualizationRegistry.resolve('algebra',`grade9_expression_${n}`);
 assert.ok(renderer,`Lesson ${n} registered`);
 for(const scene of bank.worked){
  const params={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem,total_steps:4};
  const state=step=>({annotations:[`stage:${step}`],working_state:`Operation ${step}`,after_state:`Result ${step}`});
  const ready=renderer.render(params,state(1),'ready'),first=renderer.render(params,state(1),'result');
  const second=renderer.render(params,state(2),'result'),third=renderer.render(params,state(3),'result');
  const final=renderer.render(params,state(4),'result');
  assert.ok(ready.includes(scene.problem.replaceAll('×','×'))||ready.includes('&#39;'),scene.id);
  assert.ok(!ready.includes('Result: '+scene.answer),scene.id);
  assert.ok(!first.includes('Result: '+scene.answer),scene.id);
  assert.ok(second!==first&&third!==second,`Stage visibility ${scene.id}`);
  assert.ok(third.includes('Result: '+scene.answer)&&final.includes('Result: '+scene.answer),`Final value ${scene.id}`);
  assert.ok(final.includes('data-object-id="verification"')&&final.includes('Result 4'),scene.id);
  assert.ok(final.includes('data-object-id="model"')&&final.includes('data-object-id="problem"'),scene.id);
  if(scene.visual.family==='area'||scene.visual.family==='diagnosis')assert.ok(second.includes('data-cell="1-1"'),scene.id);
  if(scene.visual.family==='fraction')assert.ok(second.includes('x ≠')&&ready.includes('g9-ex-quotient'),scene.id);
  total++;
 }
}
assert.equal(total,135);
console.log('Grade 9 expression renderers staged 135 question-specific scenes');
