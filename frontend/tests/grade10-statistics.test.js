const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const renderers={};vm.runInNewContext(fs.readFileSync(path.join(__dirname,'../js/visualization/algebra/grade10-statistics-renderers.js'),'utf8'),{
 escapeWhiteboardHtml:s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('"','&quot;'),
 AthenaVisualizationRegistry:{register:(d,k,r)=>renderers[k]=r}});
const param=q=>({scene_json:JSON.stringify(q),question_id:q.id,prompt:q.problem});
const state=(q,k)=>({annotations:[`stage:${k}`],working_state:q.actions[k-1],after_state:q.actions[k-1]});
test('all 90 examples render their own data and expose cumulative statistic stages',()=>{
 for(let n=1;n<=6;n++){
  const data=JSON.parse(fs.readFileSync(path.join(__dirname,`../../backend/app/curriculum/grade10/generated/statistics_${String(n).padStart(2,'0')}.json`))).worked;
  for(const q of data){const r=renderers[`grade10_stat_${n}`];let prev='';
   for(let k=1;k<=5;k++){
    const html=r.render(param(q),state(q,k),'result');assert.ok(html.includes(`data-question-id="${q.id}"`));
    assert.ok(html.includes('data-object-id="model"')&&!html.includes('NaN'));
    if(k===1)assert.ok(!html.includes('data-object-id="box-a"')&&!html.includes('data-object-id="frequency-0"'));
    if(k===3&&[3,4,6].includes(n))assert.ok(html.includes('data-object-id="box-a"'));
    if(k===3&&[2,5].includes(n))assert.ok(html.includes('data-object-id="frequency-0"'));
    if(n===1&&k>=3)assert.ok(html.includes('data-object-id="mean-marker"')&&!html.includes('data-object-id="box-a"'));
    if(n===2&&k>=4)assert.ok(html.includes('data-object-id="cumulative-3"')&&!html.includes('data-object-id="frequency-axis"'));
    if(k>1)assert.notEqual(html,prev);prev=html;
   }
   assert.throws(()=>r.render({...param(q),question_id:'other'},state(q,1),'result'));
  }
 }
});
test('box plot geometry scales with the question values and keeps given raw data',()=>{
 const q=JSON.parse(fs.readFileSync(path.join(__dirname,'../../backend/app/curriculum/grade10/generated/statistics_04.json'))).worked;
 const r=renderers.grade10_stat_4;
 const a=r.render(param(q[0]),state(q[0],3),'result'),b=r.render(param(q[1]),state(q[1],3),'result');
 assert.notEqual(a.match(/data-object-id="box-a"[^>]+/)[0],b.match(/data-object-id="box-a"[^>]+/)[0]);
 assert.equal((a.match(/data-object-id="observation-\d+"/g)||[]).length,10);
});
