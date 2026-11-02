const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
global.escapeWhiteboardHtml = x => String(x).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const registry = {};
global.AthenaVisualizationRegistry = {register:(type,name,renderer)=>registry[`${type}:${name}`]=renderer};
vm.runInThisContext(fs.readFileSync(path.join(__dirname,'../js/visualization/geometry/grade8-straight-lines.js'),'utf8'));
const state = (n,after='') => ({annotations:[`stage:${n}`],working_state:`Identify relationship ${n}`,after_state:after});

test('distinct line families use their own real SVG construction and preserve semantic targets',()=>{
  const cases = [
    ['grade8_intersecting_angles',{diagram:'intersection',relationship:'vertical',given_label:'47°',target_label:'x',reason:'vertical'}],
    ['grade8_intersecting_angles',{diagram:'perpendicular',relationship:'right_angle',given_label:'34°',target_label:'x',reason:'right angle'}],
    ['grade8_parallel_angles',{diagram:'transversal',relationship:'cointerior',given_label:'112°',target_label:'x',reason:'cointerior'}]
  ];
  const outputs = cases.map(([name,scene])=>{
    const render = registry[`geometry:${name}`].render;
    const parameters={scene_json:JSON.stringify(scene),prompt:'Find x'};
    const initial=render(parameters,state(1),'ready');
    const operation=render(parameters,state(3),'operation');
    const result=render(parameters,state(3,'x = 68°'),'result');
    assert.ok(initial.includes(`data-object-id="angle-given"`) && initial.includes(scene.given_label));
    for(const target of ['model','angle-target','angle-reason','operation','result','verification'])
      assert.ok(initial.includes(`data-object-id="${target}"`));
    assert.ok(!initial.includes('x = 68°'));
    assert.notEqual(initial,operation);
    assert.notEqual(operation,result);
    return result;
  });
  assert.equal(new Set(outputs).size,3);
  assert.ok(outputs[2].includes('g8-angles-parallel'));
  assert.ok(outputs[1].includes('g8-angles-right'));
});
