const assert=require("assert"),fs=require("fs"),vm=require("vm"),path=require("path");
vm.runInThisContext(fs.readFileSync(path.join(__dirname,"../js/whiteboard/animation-registry.js"),"utf8"));

for (const template of ["additive_balance", "additive_number_line", "additive_context"]) {
  const operation = `${template}_step`;
  const renderer = AthenaWhiteboardRegistry.resolve(operation);
  const step = {
    before_expression: "x + 3 = 8",
    working_expression: "x + 3 − 3 = 8 − 3",
    after_expression: "x = 5",
    operation: {type: operation, value: "Subtract three from both sides"},
  };
  assert.strictEqual(renderer.render(step, "ready", {hasVisualization: true}), "");
  const plain = markup => markup.replace(/<[^>]+>/g, "").replace(/\s+/g, " ");
  assert(plain(renderer.render(step, "operation", {history: []})).includes("x + 3 − 3"));
  const result = renderer.render(step, "result", {history: []});
  assert(result.includes('math-expression--result') && plain(result).includes("5"));
}

const step={
  before_expression:"2x − 8 = 10",
  working_expression:"2x − 8 + 8 = 10 + 8",
  after_expression:"2x = 18",
  operation:{type:"subtract_both_sides",value:-8},
};
const renderer=AthenaWhiteboardRegistry.resolve("subtract_both_sides");
const context={history:["2x − 8 = 10"]};
const ready=renderer.render(step,"ready",context);
const operation=renderer.render(step,"operation",context);
const result=renderer.render(step,"result",context);
const text=markup=>markup.replace(/<[^>]+>/g,"").replace(/\s+/g," ");

assert(ready.includes("2x"));
assert(!ready.includes("2x = 18"));
assert(!ready.includes("2x − 8 + 8 = 10 + 8"));
assert(text(operation).includes("2x − 8 + 8")&&text(operation).includes("10 + 8"));
assert(!operation.includes("2x = 18"));
assert(text(result).includes("2x")&&text(result).includes("18"));
assert(result.indexOf("math-expression--history")<result.indexOf("math-expression--result"));
assert(operation.includes('data-object-id="left-side"'));
assert(operation.includes('data-object-id="right-side"'));
assert(operation.includes('data-object-id="equals"'));
assert(operation.includes("math-token"));

const semantic=AthenaWhiteboardRegistry.resolve("apply_both_sides_display");
const balanceStep={before_expression:"3x + 7 = 22",working_expression:"3x + 7 - 7 = 22 - 7",after_expression:"3x + 7 - 7 = 22 - 7",operation:{type:"apply_both_sides_display",value:7}};
const semanticReady=semantic.render(balanceStep,"ready",{history:["3x + 7 = 22"]});
const semanticOperation=semantic.render(balanceStep,"operation",{history:["3x + 7 = 22"]});
assert(!text(semanticReady).includes("x = 5"));
assert(text(semanticOperation).includes("3x + 7 - 7 = 22 - 7"));
assert.strictEqual((semanticOperation.match(/data-object-id="subtract-left"/g)||[]).length,1);
assert.strictEqual((semanticOperation.match(/data-object-id="subtract-right"/g)||[]).length,1);
assert(semanticOperation.includes('data-object-id="coefficient"'));

const css=fs.readFileSync(path.join(__dirname,"../css/components.css"),"utf8");
assert(css.includes("overflow-wrap:break-word"));
assert(css.includes("word-break:normal"));
assert(!/\.algebra-prompt[^}]*overflow-wrap:anywhere/.test(css));

const source=fs.readFileSync(path.join(__dirname,"../js/whiteboard/stateful-whiteboard.js"),"utf8");
assert(!source.includes('["ready","settled"].includes(phase) ? "result"'));
for(const state of ["idle","playing","paused","step_complete","example_complete"])assert(source.includes(state));
assert(source.includes('"Start explanation →"'));
assert(source.includes('playing:"Explaining…"'));
assert(source.includes('paused:"Continue explanation →"'));
assert(source.includes('step_complete:"Next step →"'));
assert(source.includes('"Next example →"'));
assert(source.includes('this.reconstruct("ready", "idle")'));
assert(source.includes('this.reconstruct("result", "step_complete")'));
assert(source.includes('class="g8-completed-steps"'));
assert(source.includes("actionLocked"));
assert(source.includes("listeners?.abort"));
console.log("question-first whiteboard rendering passed");
