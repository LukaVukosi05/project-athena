const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
global.escapeWhiteboardHtml=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const found={};global.AthenaVisualizationRegistry={register:(t,n,r)=>found[`${t}:${n}`]=r};
vm.runInThisContext(fs.readFileSync(path.join(__dirname,'../js/visualization/geometry/grade11-measurement-renderers.js'),'utf8'));
for(let n=1;n<=4;n++)test(`measurement ${n} stages 15 question-owned solids`,()=>{
 const bank=JSON.parse(fs.readFileSync(path.join(__dirname,`../../backend/app/curriculum/grade11/generated/measurement_${String(n).padStart(2,'0')}.json`)));
 const render=found[`geometry:grade11_meas_${n}`]?.render;assert.ok(render);
 for(const q of bank.worked){const scene=structuredClone(q);delete scene.answer;delete scene.actions;delete scene.check;
  const p={scene_json:JSON.stringify(scene),question_id:q.id,prompt:q.problem};
  const initial=render(p,{annotations:['stage:1']},'ready');assert.match(initial,/data-object-id="model"/);assert.ok(!initial.includes(q.answer));
  let prior=initial;
  for(let k=1;k<=5;k++){
   const out=render(p,{annotations:[`stage:${k}`],working_state:q.actions[k-1],after_state:q.actions[k-1]},'result');
   assert.notEqual(out,prior);prior=out;
  }
  assert.ok(prior.includes(q.answer));
  if(n===4)assert.match(prior,/g11-meas-join/);
  assert.throws(()=>render({...p,question_id:'other'},{annotations:['stage:1']},'ready'));
 }
});
