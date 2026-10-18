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
    playing: ["pause"],
    paused: ["continue"],
    step_complete: ["next", "start"],
    example_complete: ["restart", "start"],
  };
  for (const [status, callsExpected] of Object.entries(expected)) {
    const calls = [], board = Object.create(StatefulWhiteboard.prototype);
    Object.assign(board, { status,
      startCurrent(){calls.push("start");}, pauseCurrent(){calls.push("pause");}, continueCurrent(){calls.push("continue");},
      nextStep(){calls.push("next");}, restartExample(){calls.push("restart");},
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
  assert.deepEqual(calls, [["ready", "paused", 1]]);
  board.nextStep();
  assert.equal(board.index, 1, "Next cannot skip while the selected step is not complete");
});

test("final Next is disabled by controller semantics", () => {
  const board = Object.create(StatefulWhiteboard.prototype);
  Object.assign(board, { status: "step_complete", index: 1, block: { steps: [{}, {}] }, reconstruct(){throw new Error("must not reconstruct");} });
  board.nextStep();
  assert.equal(board.index, 1);
});
