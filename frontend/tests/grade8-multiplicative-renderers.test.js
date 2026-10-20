const {test}=require("node:test"), assert=require("node:assert/strict"), fs=require("node:fs"), path=require("node:path"), vm=require("node:vm");
const root=path.resolve(__dirname,"../..");
global.escapeWhiteboardHtml=value=>String(value).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
for(const file of ["visualization-registry.js","algebra/grade8-multiplicative-renderers.js"])
  vm.runInThisContext(fs.readFileSync(path.join(root,"frontend/js/visualization",file),"utf8"));
const examples=JSON.parse(fs.readFileSync(path.join(root,"backend/app/curriculum/grade8/generated/lesson_04.json"),"utf8")).worked_examples;
const family={"algebra:equal_groups":"equal_groups","algebra:multiplicative_inverse":"multiplicative_balance",
  "algebra:fraction_scale":"fraction_scale","algebra:context_to_equation":"multiplicative_context"};
const state=(item,phase,n)=>({before_state:item.prompt,working_state:"Apply the inverse to both sides",after_state:item.answer,
  annotations:[`stage:${n}`]});

test("all 15 approved examples have question-specific models and semantic targets",()=>{
  assert.equal(examples.length,15);
  assert.equal(new Set(Object.values(family)).size,4);
  for(const item of examples){
    const renderer=AthenaVisualizationRegistry.resolve("algebra",family[item.renderer]);
    const params={prompt:item.prompt,question_id:item.id,source_data:item.question_data,total_steps:4};
    const initial=renderer.render(params,state(item,"initial",1),"initial");
    const operation=renderer.render(params,state(item,"operation",1),"operation");
    const result=renderer.render(params,state(item,"result",2),"result");
    assert.ok(initial.includes(escapeWhiteboardHtml(item.prompt)),item.id); assert.ok(initial.includes(`data-question-id="${item.id}"`));
    assert.notEqual(initial,operation,item.id); assert.notEqual(operation,result,item.id);
    assert.ok(!initial.includes(`<strong>${item.answer}</strong>`),item.id);
    for(const target of ["problem","operation","result","verification","left-expression","right-expression","balance-beam","inverse-operation","left-operation","right-operation","cancellation"])
      assert.ok(result.includes(`data-object-id="${target}"`),`${item.id}: ${target}`);
  }
});

test("equal groups, fraction bars, and context visuals use this question's values",()=>{
  const render=(item,n=2)=>AthenaVisualizationRegistry.resolve("algebra",family[item.renderer]).render(
    {prompt:item.prompt,question_id:item.id,source_data:item.question_data,total_steps:4},state(item,"result",n),"result");
  assert.ok(render(examples[0]).includes("35"));
  assert.ok(render(examples[1]).includes("24"));
  assert.notEqual(render(examples[0]),render(examples[7]));
  assert.ok(render(examples[5]).includes("2/3"));
  assert.ok(render(examples[10]).includes("72 cm²"));
  assert.ok(render(examples[11]).includes("R245"));
});
