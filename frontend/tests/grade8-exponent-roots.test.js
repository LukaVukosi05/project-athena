const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
global.escapeWhiteboardHtml=x=>String(x).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const registry={};global.AthenaVisualizationRegistry={register:(type,name,renderer)=>registry[`${type}:${name}`]=renderer};
vm.runInThisContext(fs.readFileSync(path.join(__dirname,'../js/visualization/exponents/grade8-exponents.js'),'utf8'));
const state=k=>({annotations:[`stage:${k}`],working_state:`Action ${k}`,after_state:`State ${k}`});
for(const [n,template] of [[3,'grade8_exponent_roots'],[4,'grade8_exponent_applications']])test(`lesson ${n}: 15 distinct answer-gated progressive root scenes`,()=>{
 const scenes=JSON.parse(fs.readFileSync(path.join(__dirname,`../../docs/curriculum/grade8/exponents/lesson-0${n}-scenes.json`))).scenes;
 assert.equal(scenes.length,15);assert.equal(new Set(scenes.map(s=>s.problem)).size,15);
 const render=registry[`algebra:${template}`].render;
 for(const scene of scenes){
  const params={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem,total_steps:scene.rows.length+2};
  let prior=render(params,state(1),'ready');assert.ok(!prior.includes('Answer:'));
  for(let k=2;k<=params.total_steps;k++){
   const html=render(params,state(k),'result');assert.notEqual(html,prior,`${scene.id} ${k}`);assert.ok(!html.includes('NaN'));prior=html;
  }
  assert.ok(prior.includes(`Answer: ${escapeWhiteboardHtml(scene.answer)}`));
 }
});
test('square and cube reveal different mathematical objects at relevant stages',()=>{
 const scenes=JSON.parse(fs.readFileSync(path.join(__dirname,'../../docs/curriculum/grade8/exponents/lesson-03-scenes.json'))).scenes;
 const square=scenes.find(s=>s.kind==='square_root'),cube=scenes.find(s=>s.kind==='cube_root');
 const p=s=>({scene_json:JSON.stringify(s),question_id:s.id,prompt:s.problem,total_steps:s.rows.length+2});
 const render=registry['algebra:grade8_exponent_roots'].render;
 assert.ok(!render(p(square),state(2),'result').includes('square-tile-1'));
 assert.ok(render(p(square),state(3),'result').includes('square-tile-36'));
 assert.ok(!render(p(cube),state(2),'result').includes('cube-layer-1'));
 assert.ok(render(p(cube),state(3),'result').includes('cube-layer-4'));
 assert.notEqual(render(p(square),state(4),'result'),render(p(cube),state(4),'result'));
});
