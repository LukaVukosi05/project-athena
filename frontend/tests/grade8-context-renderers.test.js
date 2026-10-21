const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'../..');
global.escapeWhiteboardHtml=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
for(const file of ['visualization-registry.js','algebra/grade8-context-renderers.js'])vm.runInThisContext(fs.readFileSync(path.join(root,'frontend/js/visualization',file),'utf8'));
const questions=JSON.parse(fs.readFileSync(path.join(root,'backend/app/curriculum/grade8/generated/lesson_09.json'),'utf8')).worked_examples;
const family=q=>q.renderer.split(':')[1]+'_native';
const render=(q,phase='initial',n=1,total=10)=>AthenaVisualizationRegistry.resolve('algebra',family(q)).render({prompt:q.prompt,question_id:q.id,source_data:q.question_data,total_steps:total},{before_state:q.prompt,working_state:'Model this situation',after_state:'Result of this step',annotations:[`stage:${n}`]},phase);
test('15 approved contexts resolve to 8 distinct native models with changing states',()=>{
  assert.equal(questions.length,15);
  assert.equal(new Set(questions.map(family)).size,8);
  for(const q of questions){const initial=render(q),working=render(q,'operation'),result=render(q,'result',2);
    assert.notEqual(initial,working,q.id);assert.notEqual(working,result,q.id);
    assert.ok(!initial.includes(`<strong>${escapeWhiteboardHtml(q.answer)}</strong>`),q.id);
    for(const id of ['problem','model','fraction-1','fraction-2','denominator','operation','result','verification','inverse-operation','left-operation','right-operation','cancellation','conclusion'])
      assert.ok(result.includes(`data-object-id="${id}"`),`${q.id}: ${id}`);
  }
});
test('perimeter graphics show exactly the scenario shape and all physical sides',()=>{
  const rectangle=render(questions[3],'result',3),triangle=render(questions[10],'result',4);
  assert.ok(rectangle.includes('<rect'));assert.equal((rectangle.match(/x \+ 3/g)||[]).length>=2,true);
  assert.ok(triangle.includes('<polygon'));assert.ok(triangle.includes('x + 1')&&triangle.includes('2x - 3')&&triangle.includes('x + 4'));
  assert.ok(!rectangle.includes('<polygon'));
});
test('money, travel, sharing and age models preserve current scenario values',()=>{
  assert.ok(render(questions[2],'result',3).includes('R18'));assert.ok(render(questions[2],'result',3).includes('R12'));
  assert.ok(render(questions[11],'result',3).includes('R150'));assert.ok(render(questions[11],'result',3).includes('R25'));
  assert.ok(render(questions[12],'result',3).includes('210'));assert.ok(render(questions[12],'result',3).includes('30'));
  assert.ok(render(questions[6],'result',3).includes('44 years'));
  assert.ok(render(questions[8]).includes('3 - 2x = 17'));
});
test('rate and perimeter diagrams follow parameter changes rather than example number',()=>{
  const a=questions[9],different={...a,question_data:a.question_data.replace("'fixed': 80", "'fixed': 110").replace("'rate': 2", "'rate': 9")};
  assert.ok(render(a).includes('R80'));assert.ok(render(different).includes('R110'));assert.ok(render(different).includes('R9 per minute'));
  const shape=questions[10],changed={...shape,question_data:shape.question_data.replace("'x + 1'", "'x + 8'")};
  assert.ok(render(changed,'result',4).includes('x + 8'));
  assert.ok(!render(shape,'result',4).includes('x + 8'));
});
