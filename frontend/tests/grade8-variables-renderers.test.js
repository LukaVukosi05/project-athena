const {test}=require("node:test"),assert=require("node:assert/strict"),fs=require("node:fs"),path=require("node:path"),vm=require("node:vm");
const root=path.resolve(__dirname,"../..");
global.escapeWhiteboardHtml=value=>String(value).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
for(const file of ["visualization-registry.js","algebra/grade8-variables-renderers.js"])vm.runInThisContext(fs.readFileSync(path.join(root,"frontend/js/visualization",file),"utf8"));
const examples=JSON.parse(fs.readFileSync(path.join(root,"backend/app/curriculum/grade8/generated/lesson_06.json"),"utf8")).worked_examples;
const family={"algebra:variables_both_sides":"variables_both_sides_native","algebra:expression_comparison":"expression_comparison","algebra:identity_contradiction":"identity_contradiction","algebra:dual_rate_timeline":"dual_rate_timeline","algebra:context_to_equation":"equal_sides_triangle"};
const render=(q,phase,n=1,total=9)=>AthenaVisualizationRegistry.resolve("algebra",family[q.renderer]).render({prompt:q.prompt,question_id:q.id,source_data:q.question_data,total_steps:total},{before_state:q.prompt,working_state:"Remove matching terms from both complete sides",after_state:"new equality",annotations:[`stage:${n}`]},phase);
test("all approved examples have distinct visual states, semantic targets and hidden initial answers",()=>{
  assert.equal(examples.length,15);assert.equal(new Set(Object.values(family)).size,5);
  for(const q of examples){const initial=render(q,"initial"),operation=render(q,"operation"),result=render(q,"result",2);
    assert.ok(initial.includes(q.id)&&initial.includes(escapeWhiteboardHtml(q.prompt)));
    assert.notEqual(initial,operation,q.id);assert.notEqual(operation,result,q.id);
    assert.ok(!initial.includes(`<strong>${escapeWhiteboardHtml(q.answer)}</strong>`),q.id);
    for(const id of ["problem","balance-beam","operation","result","verification","left-expression","right-expression","inverse-operation","left-operation","right-operation","cancellation"])
      assert.ok(result.includes(`data-object-id="${id}"`),`${q.id}: ${id}`);
  }
});
test("identity, contradiction and symbolic branches reveal only after reasoning",()=>{
  assert.ok(!render(examples[7],"initial").includes("Identity: infinitely many"));
  assert.ok(render(examples[7],"result",7,7).includes("Identity: infinitely many"));
  assert.ok(!render(examples[8],"initial").includes("Contradiction: no solution"));
  assert.ok(render(examples[8],"result",5,5).includes("Contradiction: no solution"));
  assert.ok(render(examples[14],"initial",1,15).includes("a ≠ c → ?"));
  assert.ok(render(examples[14],"result",7,15).includes("a = c, b ≠ d → no solution"));
});
test("rate charts scale from question data and hide meeting point until final",()=>{
  const plan=render(examples[10],"initial",1,9),saving=render(examples[11],"initial",1,9);
  assert.ok(plan.includes("R50 + R8")&&plan.includes("R20 + R11"));
  assert.ok(saving.includes("R120 + R35")&&saving.includes("R260 + R15"));
  assert.notEqual(plan,saving);assert.ok(!plan.includes("10 GB · R130"));
  assert.ok(render(examples[10],"result",9,9).includes("10 GB · R130"));
  assert.ok(render(examples[11],"result",9,9).includes("7 weeks · R365"));
});
test("triangle uses actual side labels and conceals x and length at initial load",()=>{
  const first=render(examples[12],"initial",1,9);
  assert.ok(first.includes("3x + 2 cm")&&first.includes("5x - 10 cm"));
  assert.ok(!first.includes("each marked side is 20 cm"));
  assert.ok(render(examples[12],"result",9,9).includes("each marked side is 20 cm"));
});
