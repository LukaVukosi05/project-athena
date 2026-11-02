const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
global.escapeWhiteboardHtml=x=>String(x).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const registry={};global.AthenaVisualizationRegistry={register:(t,n,r)=>registry[`${t}:${n}`]=r};
vm.runInThisContext(fs.readFileSync(path.join(__dirname,'../js/visualization/exponents/grade8-exponents.js'),'utf8'));
const state=k=>({annotations:[`stage:${k}`],working_state:`Operation ${k}`,after_state:`Result ${k}`});
for(const [n,name] of [[5,'grade8_exponent_error_trace'],[6,'grade8_exponent_integrated']])test(`lesson ${n}: every scene reveals a separate mathematical action and keeps previous work`,()=>{
 const scenes=JSON.parse(fs.readFileSync(path.join(__dirname,`../../docs/curriculum/grade8/exponents/lesson-0${n}-scenes.json`))).scenes;
 assert.equal(scenes.length,15);
 const render=registry[`algebra:${name}`].render;
 for(const scene of scenes){
  const p={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem,total_steps:scene.rows.length+2};
  let prior=render(p,state(1),'ready');assert.ok(!prior.includes('Answer:'));
  for(let k=2;k<=p.total_steps;k++){
   const html=render(p,state(k),'result');assert.notEqual(html,prior,`${scene.id} stage ${k}`);
   assert.ok(html.includes('data-object-id="model"')&&!html.includes('NaN'));
   if(k>=4)assert.ok(html.includes(escapeWhiteboardHtml(scene.rows[0])),`${scene.id} lost first step`);
   prior=html;
  }
  assert.ok(prior.includes('Answer: '+escapeWhiteboardHtml(scene.answer)));
 }
});
test('signed factors, quotient cancellation and measured areas are genuinely distinct',()=>{
 const scenes=n=>JSON.parse(fs.readFileSync(path.join(__dirname,`../../docs/curriculum/grade8/exponents/lesson-0${n}-scenes.json`))).scenes;
 const p=s=>({scene_json:JSON.stringify(s),question_id:s.id,prompt:s.problem,total_steps:s.rows.length+2});
 const render5=registry['algebra:grade8_exponent_error_trace'].render,render6=registry['algebra:grade8_exponent_integrated'].render;
 const sign=scenes(5).find(s=>s.kind==='sign_audit'),quotient=scenes(5).find(s=>s.kind==='quotient_audit');
 assert.ok(!render5(p(sign),state(2),'result').includes('signed-factors'));
 assert.ok(render5(p(sign),state(3),'result').includes('signed-factor-1'));
 assert.ok(!render5(p(quotient),state(4),'result').includes('cancel-pairs'));
 assert.ok(render5(p(quotient),state(5),'result').includes('cancel-pairs'));
 const square=scenes(6).find(s=>s.kind==='square_perimeter_gap');
 assert.ok(render6(p(square),state(3),'result').includes('first-square-edge'));
 assert.ok(!render6(p(square),state(3),'result').includes('second-square-edge'));
 assert.ok(render6(p(square),state(4),'result').includes('second-square-edge'));
});
