const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'../..');
global.escapeWhiteboardHtml=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
for(const file of ['visualization-registry.js','graphs/grade8-global-graph-renderer.js'])
 vm.runInThisContext(fs.readFileSync(path.join(root,'frontend/js/visualization',file),'utf8'));
const scenes=n=>JSON.parse(fs.readFileSync(path.join(root,'docs/curriculum/grade8/graphs','lesson-0'+n+'-scenes.json'),'utf8')).scenes;
const render=(s,stage,phase)=>AthenaVisualizationRegistry.resolve('coordinate_geometry','grade8_global_story').render(
 {scene:s,question_id:s.id,prompt:s.problem,total_steps:4},
 {annotations:['stage:'+stage],working_state:s.actions[stage-1],after_state:s.answer},phase);
test('15 comparisons draw both traces on one question-specific scale and preserve highlights',()=>{
 const cases=scenes(5);assert.equal(cases.length,15);
 for(const scene of cases){
  const before=render(scene,1,'ready'),a=render(scene,2,'result'),both=render(scene,3,'result');
  assert.match(before,/graph-point-4/);assert.match(before,/series-b-point-4/);
  assert.doesNotMatch(before,/graph-a-focus/);assert.match(a,/graph-a-focus/);
  assert.match(both,/graph-a-focus/);assert.match(both,/graph-b-focus/);
  assert.ok(before.includes(scene.axis.x_unit));
  if(scene.domain==='discrete'){assert.doesNotMatch(before,/data-object-id="graph-a"/);assert.doesNotMatch(before,/data-object-id="graph-b"/);}
  else {assert.match(before,/data-object-id="graph-a"/);assert.match(before,/data-object-id="graph-b"/);}
 }
 assert.notEqual(render(cases[0],1,'ready'),render(cases[1],1,'ready'));
});
test('15 error cases preserve the original graph, mark the claim, and reveal the repair last',()=>{
 const cases=scenes(6);assert.equal(cases.length,15);
 for(const scene of cases){
  const before=render(scene,1,'ready'),checking=render(scene,3,'operation'),after=render(scene,4,'result');
  assert.match(before,/data-object-id="learner-claim"/);
  assert.ok(before.includes(global.escapeWhiteboardHtml(scene.claim)));
  assert.doesNotMatch(before,/is-corrected/);
  assert.match(checking,/is-disputed/);
  assert.match(after,/is-corrected/);
  assert.ok(after.includes(global.escapeWhiteboardHtml(scene.answer)));
  if(scene.domain==='discrete')assert.doesNotMatch(before,/data-object-id="given-graph"/);
 }
});
