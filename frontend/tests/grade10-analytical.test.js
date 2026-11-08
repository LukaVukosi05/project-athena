const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const renderers={};vm.runInNewContext(fs.readFileSync(path.join(__dirname,'../js/visualization/geometry/grade10-analytical-renderers.js'),'utf8'),{
 escapeWhiteboardHtml:s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('"','&quot;'),
 AthenaVisualizationRegistry:{register:(d,k,r)=>renderers[k]=r}});
const state=(q,i)=>({annotations:[`stage:${i}`],working_state:q.actions[i-1],after_state:q.actions[i-1]});
const p=q=>({scene_json:JSON.stringify(q),question_id:q.id,prompt:q.problem});
test('90 Cartesian examples keep actual given points and stage their constructions',()=>{
 for(let n=1;n<=6;n++){
  const data=JSON.parse(fs.readFileSync(path.join(__dirname,`../../backend/app/curriculum/grade10/generated/analytical_${String(n).padStart(2,'0')}.json`)));
  for(const q of data.worked){
   const r=renderers[`grade10_ag_${n}`];const initial=r.render(p(q),state(q,1),'initial');
   const plot=r.render(p(q),state(q,1),'result');const middle=r.render(p(q),state(q,3),'result');const final=r.render(p(q),state(q,5),'result');
   assert.ok(initial.includes(q.id)&&initial.includes('data-object-id="x-axis"'));
   assert.ok(!initial.includes('data-object-id="given-0"'));
   assert.ok(plot.includes('data-object-id="given-0"'));
   assert.notEqual(plot,middle);assert.notEqual(middle,final);
   assert.ok(!middle.includes('undefined'));
   assert.throws(()=>r.render({...p(q),question_id:'different'},state(q,1),'result'));
  }
 }
});
test('midpoint construction hides the unknown until its calculation step',()=>{
 const data=JSON.parse(fs.readFileSync(path.join(__dirname,'../../backend/app/curriculum/grade10/generated/analytical_02.json')));
 for(const q of data.worked){
  const r=renderers.grade10_ag_2;const before=r.render(p(q),state(q,3),'result');const after=r.render(p(q),state(q,4),'result');
  assert.ok(!before.includes('data-object-id="constructed-point"'));
  assert.ok(after.includes('data-object-id="constructed-point"'));
 }
});
test('changing a coordinate changes its plotted SVG position',()=>{
 const q=JSON.parse(fs.readFileSync(path.join(__dirname,'../../backend/app/curriculum/grade10/generated/analytical_01.json'))).worked;
 const marker=x=>renderers.grade10_ag_1.render(p(x),state(x,1),'result').match(/data-object-id="given-0"[^>]*>/)[0];
 assert.notEqual(marker(q[0]),marker(q[1]));
});
