const test=require('node:test'), assert=require('node:assert/strict'), fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
global.escapeWhiteboardHtml=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const found={};global.AthenaVisualizationRegistry={register:(t,n,r)=>found[`${t}:${n}`]=r};
vm.runInThisContext(fs.readFileSync(path.join(__dirname,'../js/visualization/finance/grade11-finance-renderers.js'),'utf8'));
for(let n=1;n<=6;n++)test(`finance lesson ${n} stages 15 question-owned visuals`,()=>{
 const bank=JSON.parse(fs.readFileSync(path.join(__dirname,`../../backend/app/curriculum/grade11/generated/finance_${String(n).padStart(2,'0')}.json`)));
 const render=found[`finance:grade11_fin_${n}`]?.render;assert.ok(render);
 for(const q of bank.worked){const p={scene_json:JSON.stringify(q),question_id:q.id,prompt:q.problem};
  const state={annotations:['stage:1'],working_state:q.actions[0],after_state:q.actions[0]};
  const initial=render(p,state,'ready');assert.match(initial,/data-object-id="model"/);assert.ok(!initial.includes(q.answer));
  let prior=initial;
  for(let k=1;k<=5;k++){const out=render(p,{annotations:[`stage:${k}`],working_state:q.actions[k-1],after_state:q.actions[k-1]},'result');assert.notEqual(out,prior);prior=out;}
  assert.ok(prior.includes(q.answer));
  assert.throws(()=>render({...p,question_id:'wrong'},state,'ready'));
 }
});
