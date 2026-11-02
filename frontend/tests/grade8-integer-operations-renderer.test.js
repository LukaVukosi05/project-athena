const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
global.escapeWhiteboardHtml=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const registry={};global.AthenaVisualizationRegistry={register:(type,name,renderer)=>registry[`${type}:${name}`]=renderer};
vm.runInThisContext(fs.readFileSync(path.join(__dirname,'../js/visualization/numbers/grade8-integer-operations-renderer.js'),'utf8'));
const render=registry['algebra:grade8_integer_operations'].render;
for(const n of [3,4])test(`Integer operations ${n} keeps previous reasoning and hides the answer`,()=>{
 const scenes=JSON.parse(fs.readFileSync(path.join(__dirname,`../../docs/curriculum/grade8/integers/lesson-0${n}-scenes.json`))).scenes;
 assert.equal(scenes.length,15);
 for(const s of scenes){
  const p={scene_json:JSON.stringify(s),question_id:s.id,prompt:s.problem,total_steps:s.actions.length};
  const state=k=>({annotations:[`stage:${k}`],before_state:'Original',working_state:s.actions[k-1],after_state:`Stage ${k}`});
  const ready=render(p,state(1),'ready'),one=render(p,state(2),'result'),two=render(p,state(3),'result'),last=render(p,state(p.total_steps),'result');
  assert.ok(ready.includes('data-object-id="model"'));
  assert.ok(!ready.includes(`Answer: ${s.answer}`));
  assert.notEqual(ready,one);assert.notEqual(one,two);
  assert.ok(two.includes('data-object-id="reason-1"'));
  assert.ok(two.includes('data-object-id="reason-2"'));
  assert.ok(last.includes(`Answer: ${s.answer}`));
 }
});
