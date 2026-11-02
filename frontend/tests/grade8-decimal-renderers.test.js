const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
global.escapeWhiteboardHtml=x=>String(x).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const registry={};global.AthenaVisualizationRegistry={register:(t,n,r)=>registry[`${t}:${n}`]=r};
vm.runInThisContext(fs.readFileSync(path.join(__dirname,'../js/visualization/decimals/grade8-decimal-renderers.js'),'utf8'));
for(const [n,template] of [[1,'grade8_decimal_columns'],[2,'grade8_decimal_rounding']])test(`Decimal lesson ${n}: 15 specific progressively revealed visuals`,()=>{
 const slug=n===1?'place-value-comparison':'rounding-estimating';
 const scenes=JSON.parse(fs.readFileSync(path.join(__dirname,`../../docs/curriculum/grade8/decimal-fractions/lesson-0${n}-scenes.json`))).scenes;
 assert.equal(scenes.length,15);
 for(const scene of scenes){
  const render=registry[`algebra:${template}`].render,p={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem,total_steps:5};
  const state=k=>({annotations:[`stage:${k}`],working_state:`Action ${k}`,after_state:`State ${k}`});
  const initial=render(p,state(1),'ready'),model=render(p,state(2),'result'),working=render(p,state(4),'result'),final=render(p,state(5),'result');
  assert.ok(initial.includes('data-object-id="model"')&&!initial.includes('Answer:'));
  for(let i=1;i<=scene.values.length;i++)assert.ok(initial.includes(`data-object-id="decimal-${i}"`));
  assert.notEqual(initial,model);assert.notEqual(model,working);
  assert.ok(working.includes('Worked solution so far'));
  assert.ok(final.includes(`Answer: ${scene.answer.replaceAll('<','&lt;').replaceAll('>','&gt;')}`));
  assert.ok(!initial.includes('NaN')&&!final.includes('NaN'));
 }
});
test('decimal midpoint and place-value graphics reflect each original number',()=>{
 const round=registry['algebra:grade8_decimal_rounding'].render;
 const scene={id:'x',kind:'round',values:['19.995','2'],problem:'Round 19.995 to 2 decimal places.',rows:[],answer:'20.00',memo:'checked'};
 const p={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem,total_steps:5};
 const ready=round(p,{annotations:['stage:1']},'ready'),before=round(p,{annotations:['stage:3']},'result'),after=round(p,{annotations:['stage:4']},'result');
 assert.ok(ready.includes('19.99')&&ready.includes('20.00'));assert.ok(!ready.includes('19.995</text>'));
 assert.ok(before.includes('19.995'));assert.ok(after.includes('marker-end'));
 const place=registry['algebra:grade8_decimal_columns'].render;
 const a={id:'a',kind:'place',values:['103.056','thousandths'],problem:'',rows:[],answer:'6',memo:''};
 const b={...a,values:['103.057','thousandths']};
 assert.notEqual(place({scene_json:JSON.stringify(a),question_id:'a',prompt:'',total_steps:5},{annotations:['stage:3']},'result'),place({scene_json:JSON.stringify(b),question_id:'b',prompt:'',total_steps:5},{annotations:['stage:3']},'result'));
});
