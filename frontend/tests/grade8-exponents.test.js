const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
global.escapeWhiteboardHtml=x=>String(x).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const registry={};global.AthenaVisualizationRegistry={register:(t,n,r)=>registry[`${t}:${n}`]=r};
vm.runInThisContext(fs.readFileSync(path.join(__dirname,'../js/visualization/exponents/grade8-exponents.js'),'utf8'));
for(const [n,name] of [[1,'grade8_exponent_representation'],[2,'grade8_exponent_laws']])test(`exponent lesson ${n} has 15 question-specific progressive scenes`,()=>{
 const scenes=JSON.parse(fs.readFileSync(path.join(__dirname,`../../docs/curriculum/grade8/exponents/lesson-0${n}-scenes.json`))).scenes;
 assert.equal(scenes.length,15);
 for(const s of scenes){
  const p={scene_json:JSON.stringify(s),question_id:s.id,prompt:s.problem,total_steps:s.rows.length+2};
  const render=registry[`algebra:${name}`].render,state=k=>({annotations:[`stage:${k}`],working_state:`Operation ${k}`,after_state:`Result ${k}`});
  let prior=render(p,state(1),'ready');assert.ok(!prior.includes('Answer:'));
  for(let k=2;k<=p.total_steps;k++){
   const html=render(p,state(k),'result');assert.notEqual(html,prior,`${s.id} step ${k}`);
   assert.ok(!html.includes('NaN')&&html.includes('data-object-id="model"'));prior=html;
  }
  assert.ok(prior.includes(`Answer: ${escapeWhiteboardHtml(s.answer)}`));
 }
});
test('scientific shifts and exponent factors depend on current question',()=>{
 const scenes=JSON.parse(fs.readFileSync(path.join(__dirname,'../../docs/curriculum/grade8/exponents/lesson-01-scenes.json'))).scenes;
 const render=registry['algebra:grade8_exponent_representation'].render,state={annotations:['stage:5'],working_state:'',after_state:'Result'};
 const one=scenes.find(s=>s.kind==='science'),two=scenes.filter(s=>s.kind==='science')[1];
 const params=s=>({scene_json:JSON.stringify(s),question_id:s.id,prompt:s.problem,total_steps:s.rows.length+2});
 assert.notEqual(render(params(one),state,'result'),render(params(two),state,'result'));
 const negative=scenes.find(s=>s.kind==='negative');assert.ok(render(params(negative),state,'result').includes('sign-pairs'));
});

test('product power never presents addition and mixed laws show the denominator',()=>{
 const scenes=JSON.parse(fs.readFileSync(path.join(__dirname,'../../docs/curriculum/grade8/exponents/lesson-02-scenes.json'))).scenes;
 const product=scenes.find(s=>s.kind==='power_product');
 assert.ok(product.problem.includes('²')&&!product.problem.includes('(2 + 3)'));
 const mixed=scenes.find(s=>s.kind==='mixed'),p={scene_json:JSON.stringify(mixed),question_id:mixed.id,prompt:mixed.problem,total_steps:mixed.rows.length+2};
 const state=k=>({annotations:[`stage:${k}`],working_state:'working',after_state:'result'}),render=registry['algebra:grade8_exponent_laws'].render;
 assert.ok(!render(p,state(4),'result').includes('third-power'));
 assert.ok(render(p,state(5),'result').includes('third-power'));
 assert.ok(render(p,state(6),'result').includes('mixed-cancellation'));
});
