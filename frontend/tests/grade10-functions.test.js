const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const renderers={};vm.runInNewContext(fs.readFileSync(path.join(__dirname,'../js/visualization/algebra/grade10-functions-renderers.js'),'utf8'),{
 escapeWhiteboardHtml:s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('"','&quot;'),
 AthenaVisualizationRegistry:{register:(d,k,r)=>renderers[k]=r}});
const state=(q,i)=>({annotations:[`stage:${i}`],working_state:q.actions[i-1],after_state:q.actions[i-1]});
const params=q=>({scene_json:JSON.stringify(q),question_id:q.id,prompt:q.problem});
test('105 worked examples use their own family, values and retained graph stages',()=>{
 for(let n=1;n<=7;n++){
  const data=JSON.parse(fs.readFileSync(path.join(__dirname,`../../backend/app/curriculum/grade10/generated/functions_${String(n).padStart(2,'0')}.json`)));
  for(const q of data.worked){
   const r=renderers[`grade10_fn_${n}`],initial=r.render(params(q),state(q,1),'initial');
   const second=r.render(params(q),state(q,2),'result'),fourth=r.render(params(q),state(q,4),'result');
   const final=r.render(params(q),state(q,5),'result');
   assert.ok(initial.includes(q.id)&&initial.includes('data-object-id="model"'));
   assert.notEqual(initial,second);assert.notEqual(second,fourth);assert.notEqual(fourth,final);
   assert.ok(q.visual.values.mode==='discrete'?fourth.includes('data-object-id="context-point-0"')&&!fourth.includes('data-object-id="curve-'):fourth.includes('data-object-id="curve-'));
   assert.ok(!initial.includes('data-object-id="curve-'));
   assert.ok(!fourth.includes('NaN')&&!fourth.includes('undefined</text>'));
   assert.throws(()=>r.render({...params(q),question_id:'wrong'},state(q,1),'initial'));
  }
 }
});
test('discrete context uses isolated points while continuous context joins them',()=>{
 const data=JSON.parse(fs.readFileSync(path.join(__dirname,'../../backend/app/curriculum/grade10/generated/functions_07.json'))).worked;
 const discrete=data.find(q=>q.visual.values.mode==='discrete'),continuous=data.find(q=>q.visual.values.mode==='continuous');
 assert.ok(discrete&&continuous);
 const r=renderers.grade10_fn_7;
 const d=r.render(params(discrete),state(discrete,4),'result'),c=r.render(params(continuous),state(continuous,4),'result');
 assert.ok(d.includes('data-object-id="context-point-2"')&&!d.includes('data-object-id="curve-'));
 assert.ok(c.includes('data-object-id="context-point-2"')&&c.includes('data-object-id="curve-'));
});
test('hyperbola and tangent traces never join across excluded inputs',()=>{
 const load=(n,f)=>JSON.parse(fs.readFileSync(path.join(__dirname,`../../backend/app/curriculum/grade10/generated/functions_0${n}.json`))).worked.find(q=>q.visual.values.family===f);
 for(const [n,f,boundaries] of [[2,'hyperbola',[250]],[4,'tangent',[152.5,347.5]]]){
  const q=load(n,f),html=renderers[`grade10_fn_${n}`].render(params(q),state(q,4),'result');
  const paths=[...html.matchAll(/data-object-id="curve-\d+" d="([^"]+)"/g)].map(m=>m[1]);
  assert.ok(paths.length>=2);
  for(const d of paths){const xs=[...d.matchAll(/[ML]([\d.]+),/g)].map(m=>Number(m[1]));
   for(const boundary of boundaries)assert.ok(!(Math.min(...xs)<boundary && Math.max(...xs)>boundary));}
 }
});
test('public inference preview can show stated points without private coefficients',()=>{
 const q=JSON.parse(fs.readFileSync(path.join(__dirname,'../../backend/app/curriculum/grade10/generated/functions_06.json'))).worked[0];
 const preview=JSON.parse(JSON.stringify(q));delete preview.visual.values.a;delete preview.visual.values.q;delete preview.answer;
 const html=renderers.grade10_fn_6.render(params(preview),state(q,1),'initial');
 assert.ok(html.includes('data-object-id="given-0"'));
 assert.ok(!html.includes('data-object-id="curve-'));
});
