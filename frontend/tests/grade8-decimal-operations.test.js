const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
global.escapeWhiteboardHtml=x=>String(x).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const registry={};global.AthenaVisualizationRegistry={register:(t,n,r)=>registry[`${t}:${n}`]=r};
vm.runInThisContext(fs.readFileSync(path.join(__dirname,'../js/visualization/decimals/grade8-decimal-operations.js'),'utf8'));
for(const [n,template] of [[3,'grade8_decimal_product'],[4,'grade8_decimal_quotient']])test(`Decimal lesson ${n}: 15 examples with one new arithmetic state per step`,()=>{
 const scenes=JSON.parse(fs.readFileSync(path.join(__dirname,`../../docs/curriculum/grade8/decimal-fractions/lesson-0${n}-scenes.json`))).scenes;
 assert.equal(scenes.length,15);
 for(const scene of scenes){
  const render=registry[`algebra:${template}`].render,p={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem,total_steps:scene.rows.length+2};
  const state=k=>({annotations:[`stage:${k}`],working_state:`Action ${k}`,after_state:`State ${k}`});
  let previous=render(p,state(1),'ready');assert.ok(!previous.includes('Answer:'));
  for(let k=2;k<=p.total_steps;k++){
   const current=render(p,state(k),'result');assert.notEqual(current,previous,`${scene.id} step ${k} made no visible move`);
   assert.ok(current.includes('data-object-id="model"')&&current.includes('data-object-id="decimal-1"')&&current.includes('data-object-id="decimal-2"'));
   assert.ok(!current.includes('NaN'));previous=current;
  }
  assert.ok(previous.includes(`Answer: ${scene.answer}`));
 }
});
test('division reveals one quotient digit at a time, retaining earlier digits',()=>{
 const scene=JSON.parse(fs.readFileSync(path.join(__dirname,'../../docs/curriculum/grade8/decimal-fractions/lesson-04-scenes.json'))).scenes[7];
 const render=registry['algebra:grade8_decimal_quotient'].render,p={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem,total_steps:scene.rows.length+2};
 const state=k=>({annotations:[`stage:${k}`],working_state:'working',after_state:'result'});
 const third=render(p,state(3),'result'),fourth=render(p,state(4),'result'),fifth=render(p,state(5),'result');
 assert.ok(!third.includes('quotient-digit-1'));assert.ok(fourth.includes('quotient-digit-1'));
 assert.ok(fifth.includes('quotient-digit-1')&&fifth.includes('quotient-digit-2'));
});
test('multiplication partials are aligned and decimal point move follows sum',()=>{
 const scene=JSON.parse(fs.readFileSync(path.join(__dirname,'../../docs/curriculum/grade8/decimal-fractions/lesson-03-scenes.json'))).scenes.at(-1);
 const render=registry['algebra:grade8_decimal_product'].render,p={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem,total_steps:scene.rows.length+2};
 const state=k=>({annotations:[`stage:${k}`],working_state:'working',after_state:'result'});
 const first=render(p,state(4),'result'),second=render(p,state(5),'result'),late=render(p,state(p.total_steps-1),'result');
 assert.ok(first.includes('partial-1')&&!first.includes('partial-2'));
 assert.ok(second.includes('partial-1')&&second.includes('partial-2'));
 assert.ok(second.includes('g8-dec-current'));
 assert.ok(late.includes('partial-sum')&&late.includes('decimal-shift'));
});
