const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const root=path.resolve(__dirname,'../..');
global.escapeWhiteboardHtml=value=>String(value).replace(/[&<>"']/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
for(const name of ['visualization-registry.js','graphs/grade8-coordinate-renderer.js'])
  vm.runInThisContext(fs.readFileSync(path.join(root,'frontend/js/visualization',name),'utf8'));
const scenes=JSON.parse(fs.readFileSync(path.join(root,'docs/curriculum/grade8/graphs/lesson-01-scenes.json'),'utf8')).scenes;
function render(scene,stage,phase){
  const block={representation:'visual',id:`${scene.id}-board`,visualization:{type:'graphs',template:'coordinate_plane',parameters:{scene}}};
  const session=AthenaVisualizationResolver.resolve(block,{question_id:scene.id});
  assert.ok(session.instruction);
  return session.render({visualization_state:{annotations:[`stage:${stage}`]}},phase);
}
test('all 15 original scenarios have question-specific labelled axes and bounds',()=>{
  assert.equal(scenes.length,15);
  const first=render(scenes[0],1,'ready'),scaled=render(scenes[7],1,'ready');
  assert.notEqual(first,scaled);
  assert.match(scaled,/x-tick-6/);
  assert.match(scaled,/y-tick-10/);
  assert.match(render(scenes[11],1,'ready'),/min/);
  assert.match(render(scenes[11],1,'ready'),/km/);
  for(const scene of scenes){
    const ready=render(scene,1,'ready');
    assert.match(ready,/data-object-id="x-axis"/);
    assert.match(ready,/data-object-id="y-axis"/);
    assert.match(ready,/role="img"/);
    for(const point of scene.derived)assert.doesNotMatch(ready,new RegExp(`data-object-id="point-label-[0-9]+"[^>]*>${point.label} `));
    const last=Math.max(1,...scene.derived.map(point=>point.reveal_step));
    const complete=render(scene,last,'result');
    for(const point of scene.derived)assert.ok(complete.includes(`${point.label} (${point.x}, ${point.y})`),scene.id);
  }
});
test('operation shows one horizontal guide before the point, and earlier points persist',()=>{
  const compare=scenes[6];
  const ready=render(compare,2,'ready'),operation=render(compare,2,'operation'),result=render(compare,2,'result');
  assert.doesNotMatch(ready,/data-object-id="point-1"/);
  assert.match(operation,/data-object-id="x-guide-1"/);
  assert.doesNotMatch(operation,/data-object-id="point-1"/);
  assert.match(result,/data-object-id="point-1"/);
  assert.match(render(compare,4,'ready'),/data-object-id="point-1"/);
  assert.match(render(compare,4,'operation'),/data-object-id="point-1"/);
  assert.doesNotMatch(render(compare,4,'operation'),/data-object-id="point-2"/);
  assert.match(render(compare,4,'result'),/data-object-id="point-2"/);
});
test('point coordinates are scaled from actual values and invalid scenes fail',()=>{
  const scene=scenes[7],shown=render(scene,4,'result');
  assert.match(shown,/J \(6, 10\)/);
  assert.doesNotMatch(render(scene,2,'ready'),/J \(6, 10\)/);
  const changed=structuredClone(scene);changed.derived[0].x=8;
  assert.notEqual(render(changed,4,'result'),shown);
  changed.derived[0].x=100;
  assert.throws(()=>render(changed,4,'result'),/out of bounds/);
});
test('moving left and down is drawn before the final labelled point',()=>{
  const scene=scenes[5]; // F(-2, -4): horizontal on 2, vertical on 3, plot on 4.
  const first=render(scene,1,'result'),horizontal=render(scene,2,'operation');
  assert.doesNotMatch(first,/data-object-id="x-guide-1"/);
  assert.match(horizontal,/data-object-id="x-guide-1"[^>]*coord-guide--fresh-x/);
  assert.doesNotMatch(horizontal,/data-object-id="y-guide-1"/);
  const horizontalResult=render(scene,2,'result');
  assert.match(horizontalResult,/data-object-id="x-guide-1"/);
  assert.doesNotMatch(horizontalResult,/data-object-id="point-1"/);
  const vertical=render(scene,3,'operation');
  assert.match(vertical,/data-object-id="x-guide-1"/);
  assert.match(vertical,/data-object-id="y-guide-1"[^>]*coord-guide--fresh-y/);
  assert.doesNotMatch(vertical,/data-object-id="point-1"/);
  assert.match(render(scene,3,'result'),/class="coord-waypoint/);
  assert.match(render(scene,4,'operation'),/data-object-id="plot-preview-1"/);
  assert.doesNotMatch(render(scene,4,'operation'),/F \(-2, -4\)/);
  assert.match(render(scene,4,'result'),/F \(-2, -4\)/);
});
test('every authored point has ordered, question-specific motion stages',()=>{
  for(const scene of scenes){
    for(const point of scene.derived){
      assert.ok(point.horizontal_step<=point.vertical_step&&point.vertical_step<=point.reveal_step,scene.id);
      assert.match(render(scene,point.horizontal_step,'operation'),/coord-guide--fresh-x/,scene.id);
      assert.match(render(scene,point.vertical_step,'operation'),/coord-guide--fresh-y/,scene.id);
      assert.match(render(scene,point.reveal_step,'result'),new RegExp(`${point.label} \\(${point.x}, ${point.y}\\)`),scene.id);
    }
    for(const point of scene.given){
      assert.match(render(scene,point.x_read_step,'operation'),/given-x-guide/,scene.id);
      assert.match(render(scene,point.y_read_step,'operation'),/given-y-guide/,scene.id);
    }
  }
});
test('zero displacement is highlighted on the axis rather than pretending to move',()=>{
  assert.match(render(scenes[2],3,'operation'),/class="coord-zero-highlight"/); // C(4, 0)
  assert.match(render(scenes[3],2,'operation'),/class="coord-zero-highlight"/); // D(0, -5)
});
