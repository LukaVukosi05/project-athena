const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const src = fs.readFileSync(path.join(__dirname,'../js/visualization/geometry/grade8-angle-chains.js'),'utf8');
const renderers = {};
const context = {AthenaVisualizationRegistry:{register:(kind,name,renderer)=>{renderers[`${kind}:${name}`]=renderer;}},
  escapeWhiteboardHtml: value => String(value).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;')};
vm.runInNewContext(src,context);
const scene = (lesson,given,relation='corresponding_linear') => ({scene_json:JSON.stringify({family:relation,given,
  target_label:lesson===4?'(2x + 10)°':'x',wrong_claim:lesson===5?'The corresponding angles add to 180°.':'',relation:'corresponding',lesson}),
  prompt:`Given ${given}°, find x`});
const state = (n,text='') => ({annotations:[`stage:${n}`],working_state:text,after_state:`Step ${n}: ${text}`});

test('three native templates show only the given and unknown before teaching',()=>{
  for (const [number,template] of [[3,'grade8_angle_chain'],[4,'grade8_angle_equation'],[5,'grade8_angle_error']]) {
    const renderer=renderers[`geometry:${template}`];
    assert.ok(renderer);
    const initial=renderer.render(scene(number,64),{},'initial');
    assert.match(initial,/64°/);
    assert.match(initial,/data-object-id="angle-intermediate"[^>]*>\?</);
    assert.doesNotMatch(initial,/target angle = 116°/);
    const intermediate=renderer.render(scene(number,64),state(number===5?4:3,'relationship'), 'result');
    assert.match(intermediate,/data-object-id="angle-intermediate"[^>]*>64°/);
    const solved=renderer.render(scene(number,64),state(number===5?5:4,'second theorem'),'result');
    assert.match(solved,/target angle = 116°/);
    assert.notEqual(initial,intermediate);
    assert.notEqual(intermediate,solved);
    assert.match(solved,/data-object-id="verification"/);
  }
});

test('changed question values change the diagram and the error is marked only at diagnosis',()=>{
  const r=renderers['geometry:grade8_angle_error'];
  assert.notEqual(r.render(scene(5,64),state(5),'result'),r.render(scene(5,72),state(5),'result'));
  assert.doesNotMatch(r.render(scene(5,64),state(1),'result'),/is-invalid/);
  assert.match(r.render(scene(5,64),state(3),'result'),/is-invalid/);
  assert.throws(()=>r.render({scene_json:JSON.stringify({family:'unknown',lesson:3})},{}),/Unsupported/);
});
