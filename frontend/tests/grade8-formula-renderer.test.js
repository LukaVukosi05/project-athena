const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
global.escapeWhiteboardHtml=x=>String(x).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
for(const file of ['visualization-registry.js','algebra/grade8-formula-renderer.js'])vm.runInThisContext(fs.readFileSync(path.join(__dirname,'../js/visualization',file),'utf8'));
const render=(scene,stage,phase,givens,derived)=>AthenaVisualizationRegistry.resolve('algebra','formula_rectangle').render({question_id:'g8-fr-l04-w03',prompt:'Find the missing length',scene_json:JSON.stringify(scene),given_objects:givens,derived_objects:derived,total_steps:4},{annotations:[`stage:${stage}`],before_state:'A=l×w',working_state:'24=l×4',after_state:'l=6 cm'},phase);
test('inverse area hides the missing side until its operation, preserves given area and scales dimensions',()=>{
 const scene={length:6,width:4,area:24,units:'cm'},givens=['area 24 cm²','width 4 cm'],derived=['length 6 cm'];
 const initial=render(scene,1,'ready',givens,derived), operation=render(scene,3,'operation',givens,derived), result=render(scene,3,'result',givens,derived);
 assert.match(initial,/length \?/);assert.doesNotMatch(initial,/length 6 cm<\/span>/);
 assert.match(initial,/24 cm²/);assert.match(operation,/24=l×4/);assert.match(result,/6 cm/);
 assert.notEqual(initial,operation);assert.notEqual(operation,result);
 assert.match(result,/data-object-id="given-1"/);assert.match(result,/data-object-id="derived-1"/);
 const changed=render({length:8,width:4,area:32,units:'cm'},3,'result',['area 32 cm²','width 4 cm'],['length 8 cm']);
 assert.notEqual(changed,result);
 assert.throws(()=>render({length:8,width:4,area:24,units:'cm'},1,'ready',givens,derived),/Invalid rectangle/);
});
test('a relationship such as twice the width does not expose its calculated length initially',()=>{
 const html=render({length:12,width:6,area:72,units:'cm'},1,'ready',['area 72 cm²','length twice width'],['length 12 cm']);
 assert.match(html,/length \?/);assert.doesNotMatch(html,/length 12 cm<\/span>/);
});
