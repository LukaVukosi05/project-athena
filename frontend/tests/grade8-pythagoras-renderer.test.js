const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
global.escapeWhiteboardHtml=x=>String(x).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const templates={};global.AthenaVisualizationRegistry={register:(type,name,renderer)=>templates[`${type}:${name}`]=renderer};
vm.runInThisContext(fs.readFileSync(path.join(__dirname,'../js/visualization/geometry/grade8-pythagoras.js'),'utf8'));
const state=(n,after='')=>({annotations:[`stage:${n}`],working_state:`Calculate a square in step ${n}`,after_state:after});
const scene=(family,a=3,b=4,c=null,context='')=>({scene_json:JSON.stringify({family,a,b,c,context,problem:'Find the unknown side.'}),prompt:'Find the unknown side.'});
test('all five models have distinct initial, working, and result states with target nodes',()=>{
  for(const family of ['square_areas','hypotenuse','missing_leg','converse','application']){
    const render=templates[`geometry:grade8_pythagoras_${family}`]?.render;assert.equal(typeof render,'function');
    const params=scene(family,3,4,family==='converse'?5:family==='missing_leg'?5:null,family==='application'?'ladder':'');
    const initial=render(params,state(1),'ready'),working=render(params,state(3),'operation'),result=render(params,state(6,'Verified: answer 5 cm'),'result');
    assert.match(initial,/g8-pyth-triangle/);assert.doesNotMatch(initial,/Verified: answer/);
    assert.notEqual(initial,working);assert.notEqual(working,result);
    for(const id of ['model','shape-given','shape-reason','operation','result','verification'])assert.match(initial,new RegExp(`data-object-id="${id}"`));
  }
});
test('square areas, right angle and side coordinates follow the current numbers',()=>{
  const render=templates['geometry:grade8_pythagoras_square_areas'].render;
  const first=render(scene('square_areas',3,4),state(5,'Verified: 9 + 16 = 25 cm²'),'result');
  const second=render(scene('square_areas',5,12),state(5,'Verified: 25 + 144 = 169 cm²'),'result');
  assert.match(first,/>9 cm²/);assert.match(first,/>16 cm²/);assert.match(first,/>25 cm²/);
  assert.match(second,/>144 cm²/);assert.match(second,/>169 cm²/);
  assert.notEqual(first,second);assert.match(first,/g8-pyth-angle/);
});
test('converse triangle is drawn in proportion and cannot falsely show a right-angle marker',()=>{
  const render=templates['geometry:grade8_pythagoras_converse'].render;
  const trueInitial=render(scene('converse',3,4,5),state(1),'ready');
  const trueFinal=render(scene('converse',3,4,5),state(6,'Verified: right-angled'),'result');
  const falseFinal=render(scene('converse',4,5,6),state(6,'Verified: not right-angled'),'result');
  assert.doesNotMatch(trueInitial,/class="g8-pyth-angle"/);
  assert.match(trueFinal,/class="g8-pyth-angle"/);
  assert.doesNotMatch(falseFinal,/class="g8-pyth-angle"/);
  assert.notEqual(trueFinal.match(/class="g8-pyth-triangle"[^>]*d="([^"]+)/)?.[1],falseFinal.match(/class="g8-pyth-triangle"[^>]*d="([^"]+)/)?.[1]);
});
