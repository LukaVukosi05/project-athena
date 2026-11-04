const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
global.escapeWhiteboardHtml=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
for(const name of ['visualization-registry.js','numbers/grade9-context-renderers.js'])vm.runInThisContext(fs.readFileSync(path.join(__dirname,'../js/visualization',name),'utf8'));
const templates={3:'grade9_ratio_rate',4:'grade9_proportion',5:'grade9_transaction',6:'grade9_ledger',7:'grade9_interest',8:'grade9_decision'};
for(const [n,template] of Object.entries(templates)){
 const data=JSON.parse(fs.readFileSync(path.join(__dirname,`../../backend/app/curriculum/grade9/generated/whole_numbers_0${n}.json`),'utf8'));
 assert.equal(data.worked.length,15);
 for(const scene of data.worked){
  const renderer=AthenaVisualizationRegistry.resolve('algebra',template),count=scene.actions.length;
  const args={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem,total_steps:count};
  const at=(stage,phase='result')=>renderer.render(args,{annotations:[`stage:${stage}`],after_state:scene.actions[Math.max(0,stage-1)]},phase);
  const initial=at(0),middle=at(2),last=at(count);
  assert.ok(initial.includes(scene.problem.replace(/&/g,'&amp;')),scene.id);
  assert.ok(!initial.includes(`Result: ${scene.answer}`),scene.id);
  assert.ok(!initial.includes('Check:'),scene.id);
  assert.notEqual(initial,middle,scene.id);assert.notEqual(middle,last,scene.id);
  assert.ok(last.includes(`Result: ${scene.answer}`),scene.id);
  assert.ok(last.includes('data-object-id="verification"'),scene.id);
  for(const id of ['problem','model','operation','result','verification'])assert.ok(initial.includes(`data-object-id="${id}"`),`${scene.id} ${id}`);
 }
}
console.log('Six Grade 9 visual families, 90 question-specific scenes and staged results passed');
