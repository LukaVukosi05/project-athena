const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const renderers={};vm.runInNewContext(fs.readFileSync(path.join(__dirname,'../js/visualization/probability/grade10-probability-renderers.js'),'utf8'),{
 escapeWhiteboardHtml:s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('"','&quot;'),
 AthenaVisualizationRegistry:{register:(d,k,r)=>renderers[k]=r}});
const params=q=>({scene_json:JSON.stringify(q),question_id:q.id,prompt:q.problem});
const state=(q,k)=>({annotations:[`stage:${k}`],working_state:q.actions[k-1],after_state:q.actions[k-1]});
test('75 question-specific probability models progress from givens to verified counts',()=>{
 for(let n=1;n<=5;n++){
  const data=JSON.parse(fs.readFileSync(path.join(__dirname,`../../backend/app/curriculum/grade10/generated/probability_${String(n).padStart(2,'0')}.json`))).worked;
  for(const q of data){const r=renderers[`grade10_prob_${n}`];let prev='';
   for(let k=1;k<=5;k++){
    const html=r.render(params(q),state(q,k),'result');
    assert.ok(html.includes(`data-question-id="${q.id}"`)&&html.includes('data-object-id="model"'));
    if(k===1)assert.ok(!html.includes('data-object-id="overlap-count"')&&!html.includes('data-object-id="observed-bar"'));
    if(k===3)assert.ok(html.includes(n===1?'data-object-id="theoretical-bar"':'data-object-id="a-only-count"'));
    if(k>1)assert.notEqual(html,prev);prev=html;
   }
   assert.throws(()=>r.render({...params(q),question_id:'wrong'},state(q,1),'result'));
  }
 }
});
test('Venn region labels come from actual counts and public previews render blank circles',()=>{
 const q=JSON.parse(fs.readFileSync(path.join(__dirname,'../../backend/app/curriculum/grade10/generated/probability_02.json'))).worked[0];
 const r=renderers.grade10_prob_2;
 const preview=JSON.parse(JSON.stringify(q));for(const key of ['a_only','b_only','neither','union','answer'])delete preview.visual.values[key];
 const initial=r.render(params(preview),state(q,1),'initial');
 assert.ok(initial.includes('data-object-id="event-a"')&&!initial.includes('data-object-id="overlap-count"'));
 const result=r.render(params(q),state(q,4),'result');
 assert.ok(result.includes(`data-object-id="outside-count"`));
 assert.ok(result.includes(`>${q.visual.values.neither}</text>`));
});
