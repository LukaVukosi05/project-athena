const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
global.escapeWhiteboardHtml=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const found={};global.AthenaVisualizationRegistry={register:(t,n,r)=>found[`${t}:${n}`]=r};
vm.runInThisContext(fs.readFileSync(path.join(__dirname,'../js/visualization/patterns/grade11-pattern-renderers.js'),'utf8'));
for(let n=1;n<=5;n++)test(`quadratic lesson ${n} draws 15 question-specific difference tables`,()=>{
 const bank=JSON.parse(fs.readFileSync(path.join(__dirname,`../../backend/app/curriculum/grade11/generated/patterns_${String(n).padStart(2,'0')}.json`)));
 const render=found[`algebra:grade11_pat_${n}`]?.render;assert.ok(render);
 for(const q of bank.worked){const scene=structuredClone(q);delete scene.answer;delete scene.actions;delete scene.check;delete scene.visual.values.target;
  const p={scene_json:JSON.stringify(scene),question_id:q.id,prompt:q.problem};
  const initial=render(p,{annotations:['stage:1']},'ready');
  assert.match(initial,/data-object-id="model"/);assert.ok(!initial.includes(q.answer));
  let prior=initial;
  for(let k=1;k<=5;k++){
   const out=render(p,{annotations:[`stage:${k}`],working_state:q.actions[k-1],after_state:q.actions[k-1]},'result');
   assert.notEqual(out,prior);prior=out;
  }
  assert.ok(prior.includes(q.answer));
  if(n===4){const match=initial.match(/class="g11-pat-tile"/g)||[];assert.equal(match.length,1+q.visual.values.columns_offset);}
  assert.throws(()=>render({...p,question_id:'other'},{annotations:['stage:1']},'ready'));
 }
});
