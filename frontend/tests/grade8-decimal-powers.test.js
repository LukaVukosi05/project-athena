const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
global.escapeWhiteboardHtml=x=>String(x).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const registry={};global.AthenaVisualizationRegistry={register:(t,n,r)=>registry[`${t}:${n}`]=r};
vm.runInThisContext(fs.readFileSync(path.join(__dirname,'../js/visualization/decimals/grade8-decimal-operations.js'),'utf8'));
for(const [n,template] of [[5,'grade8_decimal_power'],[6,'grade8_decimal_root']])test(`decimal lesson ${n} question-specific progressive states`,()=>{
 const scenes=JSON.parse(fs.readFileSync(path.join(__dirname,`../../docs/curriculum/grade8/decimal-fractions/lesson-0${n}-scenes.json`))).scenes;
 assert.equal(scenes.length,15);
 for(const scene of scenes){
  const p={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem,total_steps:scene.rows.length+2};
  const render=registry[`algebra:${template}`].render,state=k=>({annotations:[`stage:${k}`],working_state:`Operation ${k}`,after_state:`Result ${k}`});
  let prior=render(p,state(1),'ready');assert.ok(!prior.includes('Answer:'));
  if(n===6)assert.ok(!prior.includes(scene.answer));
  for(let k=2;k<=p.total_steps;k++){
   const html=render(p,state(k),'result');assert.notEqual(html,prior,`${scene.id} stage ${k}`);
   assert.ok(!html.includes('NaN')&&html.includes('data-object-id="model"'));
   prior=html;
  }
  assert.ok(prior.includes(`Answer: ${scene.answer}`));
 }
});
test('root candidate is hidden until the candidate test',()=>{
 const scene=JSON.parse(fs.readFileSync(path.join(__dirname,'../../docs/curriculum/grade8/decimal-fractions/lesson-06-scenes.json'))).scenes[0];
 const render=registry['algebra:grade8_decimal_root'].render,p={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem,total_steps:scene.rows.length+2};
 const state=k=>({annotations:[`stage:${k}`],working_state:'work',after_state:'result'});
 assert.ok(!render(p,state(3),'result').includes('root-factor-1'));
 assert.ok(render(p,state(4),'result').includes('root-factor-1'));
 assert.ok(render(p,state(6),'result').includes('root-factor-1'));
});
