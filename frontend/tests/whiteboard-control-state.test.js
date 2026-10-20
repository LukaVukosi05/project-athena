const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

global.escapeWhiteboardHtml = value => String(value);
global.AthenaVisualizationResolver = { resolve() { return null; } };
global.matchMedia = () => ({ matches: false });
vm.runInThisContext(fs.readFileSync(path.join(__dirname, "../js/whiteboard/stateful-whiteboard.js"), "utf8"));

test("the primary control has exactly one state-aware action", () => {
  const expected = {
    idle: ["start"],
    playing: [],
    paused: ["continue"],
    step_complete: ["next", "start"],
    example_complete: ["next-example"],
  };
  for (const [status, callsExpected] of Object.entries(expected)) {
    const calls = [], board = Object.create(StatefulWhiteboard.prototype);
    Object.assign(board, { status,
      startCurrent(){calls.push("start");}, pauseCurrent(){calls.push("pause");}, continueCurrent(){calls.push("continue");},
      nextStep(){calls.push("next");}, restartExample(){calls.push("restart");}, onNextExample(){calls.push("next-example");},
    });
    board.primaryAction();
    assert.deepEqual(calls, callsExpected, status);
  }
});

test("manual Next reconstructs one and only one mathematical state", () => {
  const calls = [], board = Object.create(StatefulWhiteboard.prototype);
  Object.assign(board, { status: "step_complete", index: 0, block: { steps: [{}, {}, {}] }, reconstruct(phase,status){calls.push([phase,status,this.index]);this.status=status;} });
  board.nextStep();
  assert.equal(board.index, 1);
  assert.deepEqual(calls, [["ready", "idle", 1]]);
  board.nextStep();
  assert.equal(board.index, 1, "Next cannot skip while the selected step is not complete");
});

test("Previous on step one returns to the previous example only when it exists", () => {
  const calls = [], board = Object.create(StatefulWhiteboard.prototype);
  Object.assign(board, {index:0, exampleIndex:5, onPreviousExample(){calls.push("previous-example");}});
  board.previousStep();
  assert.deepEqual(calls, ["previous-example"]);
  board.exampleIndex = 0;
  board.previousStep();
  assert.deepEqual(calls, ["previous-example"]);
});

test("final Next is disabled by controller semantics", () => {
  const board = Object.create(StatefulWhiteboard.prototype);
  Object.assign(board, { status: "step_complete", index: 1, block: { steps: [{}, {}] }, reconstruct(){throw new Error("must not reconstruct");} });
  board.nextStep();
  assert.equal(board.index, 1);
});

test("prior results remain on the board through ready, operation, and result", () => {
  const tracePane = {scrollTop:0,scrollHeight:444};
  const stage = {innerHTML:"",setAttribute(){},querySelector(selector){return selector === ".g8-completed-steps" ? tracePane : null;},dataset:{}};
  global.CSS = {escape:value => value};
  global.AthenaWhiteboardRegistry = {resolve(){return {render(){return "";}};}};
  const board = Object.create(StatefulWhiteboard.prototype);
  Object.assign(board, {
    index:2, status:"idle", visualSession:{render(){return '<div data-object-id="operation">current</div>';}},
    block:{initial_expression:"x + 2 = 8",visualization:{type:"algebra"},steps:[
      {after_expression:"x + 2 − 2 = 8 − 2",operation:{type:"test"},events:[],screen_reader_description:"Subtract"},
      {after_expression:"x = 6",operation:{type:"test"},events:[],screen_reader_description:"Simplify"},
      {after_expression:"8 = 8",operation:{type:"test"},events:[],screen_reader_description:"Verify"},
    ]},
    mount:{querySelector(selector){if(selector===".whiteboard-stage")return stage;if(selector==='[data-role="checkpoint"]')return {hidden:false};return null;}},
    stopTimeline(){},renderTeachingNotes(){},renderOpeningCaption(){},setStatus(){},
  });
  for (const phase of ["ready","operation","result"]) {
    board.reconstruct(phase,"idle");
    assert.equal(stage.dataset.layout,"split");
    assert.match(stage.innerHTML,/class="whiteboard-visual-pane"/);
    assert.match(stage.innerHTML,/class="g8-completed-steps"/);
    assert.match(stage.innerHTML,/x \+ 2 = 8/);
    assert.match(stage.innerHTML,/x = 6/);
    assert.equal((stage.innerHTML.match(/x = 6/g)||[]).length,1);
    assert.ok(stage.innerHTML.indexOf("x = 6") > stage.innerHTML.indexOf("current"), "written working follows the active diagram");
    if (phase === "result") assert.match(stage.innerHTML, /Step 3<\/span>.*8 = 8/, "the final written solution includes the current check");
    assert.equal(tracePane.scrollTop,444,"the newest written line remains visible in its pane");
  }
  board.index=0;
  board.reconstruct("ready","idle");
  assert.match(stage.innerHTML,/Steps appear here as the explanation progresses/);
  assert.doesNotMatch(stage.innerHTML,/class="is-latest"/);
});
