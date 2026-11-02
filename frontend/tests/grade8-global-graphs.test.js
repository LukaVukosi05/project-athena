const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'../..');
global.escapeWhiteboardHtml=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
for(const file of ['visualization-registry.js','graphs/grade8-global-graph-renderer.js'])vm.runInThisContext(fs.readFileSync(path.join(root,'frontend/js/visualization',file),'utf8'));
const read=JSON.parse(fs.readFileSync(path.join(root,'docs/curriculum/grade8/graphs/lesson-03-scenes.json'),'utf8')).scenes;
const draw=JSON.parse(fs.readFileSync(path.join(root,'docs/curriculum/grade8/graphs/lesson-04-scenes.json'),'utf8')).scenes;
const render=(s,stage,phase)=>AthenaVisualizationRegistry.resolve('coordinate_geometry','grade8_global_story').render({scene:s,question_id:s.id,prompt:s.problem,total_steps:4},{annotations:[`stage:${stage}`],working_state:s.actions[Math.max(0,stage-1)],after_state:s.answer},phase);
test('all given graphs are visible at first and later highlights remain in view',()=>{
 assert.equal(read.length,15);
 for(const scene of read){const first=render(scene,1,'ready'),third=render(scene,3,'result');assert.match(first,/graph-point-4/);assert.doesNotMatch(first,/graph-highlight-1/);assert.match(third,/graph-highlight-1/);assert.match(third,/graph-highlight-2/);assert.match(third,/graph-highlight-3/);assert.match(third,/grade8-global-graph/);}
});
test('all story graphs grow in four meaningful states and never join discrete counts',()=>{
 assert.equal(draw.length,15);
 for(const scene of draw){const first=render(scene,1,'ready'),second=render(scene,2,'result'),third=render(scene,3,'result'),last=render(scene,4,'result');assert.doesNotMatch(first,/graph-point-1/);assert.match(render(scene,1,'operation'),/graph-point-1/);assert.doesNotMatch(first,/graph-point-2/);assert.match(second,/graph-point-2/);assert.doesNotMatch(second,/graph-point-3/);assert.match(third,/graph-point-3/);assert.doesNotMatch(third,/graph-point-4/);assert.match(last,/graph-point-4/);if(scene.domain==='discrete')assert.doesNotMatch(last,/graph-segment-1/);else assert.match(last,/graph-segment-3/);assert.notEqual(first,last);}
});
test('the graph and its labels change when the question changes',()=>{
 assert.notEqual(render(read[0],4,'result'),render(read[1],4,'result'));
 assert.notEqual(render(draw[0],4,'result'),render(draw[1],4,'result'));
 assert.match(render(draw[5],4,'result'),/>-4</);
});
