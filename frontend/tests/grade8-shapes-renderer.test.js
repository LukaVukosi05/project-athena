const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
global.escapeWhiteboardHtml=x=>String(x).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const templates={};global.AthenaVisualizationRegistry={register:(type,name,renderer)=>templates[`${type}:${name}`]=renderer};
vm.runInThisContext(fs.readFileSync(path.join(__dirname,'../js/visualization/geometry/grade8-shapes.js'),'utf8'));
const state=(n,after='')=>({annotations:[`stage:${n}`],working_state:`Use the given property at stage ${n}`,after_state:after});
const scenes={
 triangle_sides:{shape:'triangle',points:[[55,185],[285,185],[170,52]],labels:{AB:'7',AC:'7',BC:'10'},family:'triangle_sides'},
 triangle_sum:{shape:'triangle',points:[[45,185],[295,185],[150,45]],angles:{A:'50°',B:'60°',C:'x'},family:'triangle_sum'},
 equal_triangle:{shape:'triangle',points:[[170,52],[55,185],[285,185]],angles:{A:'40°',B:'x'},ticks:'isosceles',family:'equal_triangle'},
 quad_classify:{shape:'quadrilateral',points:[[65,175],[295,175],[245,65],[100,65]],properties:'exactly one pair of parallel sides',family:'quad_classify'},
 quad_angle:{shape:'quadrilateral',points:[[80,175],[260,175],[305,55],[125,55]],angles:{A:'68°',C:'x'},kind:'parallelogram_opposite',family:'quad_angle'}
};
test('all five native shape families reveal givens, theorem and result in order',()=>{
 for(const [family,scene] of Object.entries(scenes)){
  const render=templates[`geometry:grade8_${family}`]?.render;assert.equal(typeof render,'function');
  const params={scene_json:JSON.stringify(scene),prompt:'Use the marked figure'};
  const initial=render(params,state(1),'ready'),working=render(params,state(3),'operation'),result=render(params,state(3,'Verified: x = 70°; answer 70°'),'result');
  assert.match(initial,/<polygon/);assert.match(initial,/data-object-id="model"/);
  assert.doesNotMatch(initial,/Verified: x = 70°/);
  for(const id of ['shape-given','shape-reason','operation','result','verification'])assert.match(initial,new RegExp(`data-object-id="${id}"`));
  assert.notEqual(initial,working);assert.notEqual(working,result);assert.match(result,/Verified: x = 70°/);
  if(family==='quad_classify')assert.match(result,/g8-shape-parallel/);
  if(family==='equal_triangle')assert.match(result,/g8-shape-tick/);
 }
});
test('different shape points and angle measures change the actual SVG',()=>{
 const r=templates['geometry:grade8_triangle_sum'].render;
 const base={scene_json:JSON.stringify(scenes.triangle_sum),prompt:'Find angle C'};
 const changed={...base,scene_json:JSON.stringify({...scenes.triangle_sum,points:[[45,185],[250,185],[110,80]],angles:{A:'65°',B:'45°',C:'x'}})};
 assert.notEqual(r(base,state(2),'result'),r(changed,state(2),'result'));
});
