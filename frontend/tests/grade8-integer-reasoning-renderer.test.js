const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
global.escapeWhiteboardHtml=x=>String(x).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const r={};global.AthenaVisualizationRegistry={register:(t,n,v)=>r[`${t}:${n}`]=v};
vm.runInThisContext(fs.readFileSync(path.join(__dirname,'../js/visualization/numbers/grade8-integer-reasoning-renderer.js'),'utf8'));
const render=r['algebra:grade8_integer_reasoning'].render;
for(const n of [5,6])test(`Integers ${n}: question-specific claim or story remains visible through reasoning`,()=>{
 const scenes=JSON.parse(fs.readFileSync(path.join(__dirname,`../../docs/curriculum/grade8/integers/lesson-0${n}-scenes.json`))).scenes;
 assert.equal(scenes.length,15);
 for(const s of scenes){
  const p={scene_json:JSON.stringify(s),question_id:s.id,prompt:s.problem,total_steps:s.actions.length};
  const state=k=>({annotations:[`stage:${k}`],before_state:'Original',working_state:s.actions[k-1],after_state:`Stage ${k}`});
  const a=render(p,state(1),'ready'),b=render(p,state(2),'result'),c=render(p,state(3),'result'),final=render(p,state(5),'result');
  assert.ok(a.includes(s.problem.replace(/&/g,'&amp;')));assert.ok(!a.includes(`Answer: ${s.answer}`));
  assert.notEqual(a,b);assert.notEqual(b,c);assert.ok(c.includes('data-object-id="reason-1"'));
  assert.ok(c.includes('data-object-id="reason-2"'));assert.ok(final.includes(`Answer: ${s.answer}`));
  if(n===5){assert.ok(a.includes('data-object-id="left-claim"'));assert.ok(a.includes('data-object-id="right-claim"'));}
  else{assert.ok(a.includes('data-object-id="start-value"'));assert.ok(c.includes('data-object-id="change-1"'));}
 }
});
