const {test}=require("node:test"), assert=require("node:assert/strict"), fs=require("node:fs"), path=require("node:path"), vm=require("node:vm");
const root=path.resolve(__dirname,"../..");
global.escapeWhiteboardHtml=value=>String(value).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
for(const file of ["visualization-registry.js","algebra/grade8-two-step-renderers.js"])
  vm.runInThisContext(fs.readFileSync(path.join(root,"frontend/js/visualization",file),"utf8"));
const examples=JSON.parse(fs.readFileSync(path.join(root,"backend/app/curriculum/grade8/generated/lesson_05.json"),"utf8")).worked_examples;
const family={"algebra:two_step_balance":"two_step_balance_native","algebra:operation_machine":"operation_machine",
  "algebra:two_step_number_line":"two_step_number_line","algebra:fraction_scale":"two_step_fraction_scale",
  "algebra:context_to_equation":"two_step_context"};
const state=(item,n)=>({before_state:item.prompt,working_state:"Undo the outside operation on both sides",after_state:item.answer,annotations:[`stage:${n}`]});
const render=(item,phase,n=1,totalSteps=5)=>AthenaVisualizationRegistry.resolve("algebra",family[item.renderer]).render(
  {prompt:item.prompt,question_id:item.id,source_data:item.question_data,total_steps:totalSteps},state(item,n),phase);

test("all 15 questions select one of five native models and reveal one operation at a time",()=>{
  assert.equal(examples.length,15);assert.equal(new Set(Object.values(family)).size,5);
  for(const item of examples){
    const initial=render(item,"initial"),operation=render(item,"operation"),result=render(item,"result",2);
    assert.ok(initial.includes(escapeWhiteboardHtml(item.prompt)),item.id);
    assert.ok(initial.includes(`data-question-id="${item.id}"`));
    assert.notEqual(initial,operation,item.id);assert.notEqual(operation,result,item.id);
    assert.ok(!initial.includes(`<strong>${escapeWhiteboardHtml(item.answer)}</strong>`),item.id);
    for(const id of ["problem","balance-beam","operation","result","verification","left-expression","right-expression","inverse-operation","left-operation","right-operation","cancellation"])
      assert.ok(result.includes(`data-object-id="${id}"`),`${item.id}: ${id}`);
  }
});

test("specific equation and scenario values govern diagrams",()=>{
  assert.ok(render(examples[0],"result",4).includes("11"));
  assert.ok(render(examples[1],"result",4).includes("16"));
  assert.notEqual(render(examples[0],"result",4),render(examples[1],"result",4));
  assert.ok(render(examples[2],"initial").includes("divide by 4"));
  assert.ok(render(examples[7],"initial").includes("2/3"));
  assert.ok(render(examples[10],"initial").includes("34 cm"));
  assert.ok(render(examples[11],"initial").includes("R72"));
  assert.ok(render(examples[12],"result",5,6).includes("7 equal jumps"));
  assert.ok(render(examples[14],"operation",3).includes("divide by a if a != 0"));
});

test("the reverse machine and balance expose successive mathematical states",()=>{
  const machine=examples[2];
  const initial=render(machine,"initial",1),first=render(machine,"operation",1),second=render(machine,"operation",3);
  assert.ok(initial.includes("inverse step hidden"));
  assert.ok(first.includes("subtract 2") && first.includes("inverse step hidden"));
  assert.ok(second.includes("subtract 2") && second.includes("multiply by 4"));
  const balance=examples[0];
  assert.ok(render(balance,"initial",1).includes("given value"));
  assert.ok(render(balance,"result",2).includes("after the same inverse on each side"));
  assert.ok(render(balance,"result",2).includes(">8</strong>"));
});
