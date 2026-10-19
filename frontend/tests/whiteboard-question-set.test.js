const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");
const path = require("node:path");

global.location = { href: "https://athena.test/lesson.html?lesson=grade8" };
global.history = { replaceState(_state, _title, url) { global.location.href = String(url); } };
global.escapeWhiteboardHtml = value => String(value);
class Element {
  constructor() { this.hidden = false; this.disabled = false; this.onclick = null; this.onchange = null; this.textContent = ""; this.innerHTML = ""; }
  focus() { this.focused = true; }
  insertAdjacentHTML() {}
  querySelector(selector) { if (selector.includes('retry')) return this.retry || (this.retry = { addEventListener(_type, listener) { this.onclick = listener; } }); return null; }
}
class Mount {
  set innerHTML(value) {
    this.html = value;
    this.nodes = { board: new Mount(), header:new Element(), loading:new Element() };
  }
  get innerHTML() { return this.html; }
  querySelector(selector) {
    if (selector === '[data-role="current-whiteboard"]') return this.nodes.board;
    if (selector === ".stateful-whiteboard header") return this.nodes.header;
    if (selector === '[data-role="example-loading"]') return this.nodes.loading;
    const match = selector.match(/data-example-action="([^"]+)/);
    return match ? this.nodes[match[1]] || null : null;
  }
  replaceChildren() { this.html = ""; }
}
global.StatefulWhiteboard = class {
  constructor(mount, block, options) { this.block = block; this.index = options.initialStep; this.status = options.initialStatus; this.options = options; this.destroyed = false; }
  mountBoard() { return this; }
  state(index, status) { this.index = index; this.status = status; this.options.onStateChange(index, status); }
  destroy() { this.destroyed = true; }
};
vm.runInThisContext(fs.readFileSync(path.join(__dirname, "../js/whiteboard/whiteboard-question-set.js"), "utf8"));
const makeQuestion = index => ({ id:`q${index+1}`, difficulty:"standard", guidance_level:"high", whiteboard:{ problem:`Problem ${index+1}`, steps:[{}, {}, {}] } });

test("jump from example 8 to 5 and back preserves the completed state", () => {
  const set = new WhiteboardQuestionSet(new Mount(), Array.from({length:12}, (_, index) => makeQuestion(index))).mountSet();
  set.moveTo(7);
  assert.equal(set.board.block.problem, "Problem 8");
  set.board.state(2, "example_complete");
  const old = set.board;
  set.board.options.onSelectExample(4);
  assert.equal(old.destroyed, true);
  assert.equal(set.board.block.problem, "Problem 5");
  set.board.options.onSelectExample(7);
  assert.equal(set.board.index, 2);
  assert.equal(set.board.status, "example_complete");
  assert.equal(new URL(global.location.href).searchParams.get("example"), "8");
});

test("leaving an interrupted step resumes at the last finished result", () => {
  const set = new WhiteboardQuestionSet(new Mount(), [makeQuestion(0), makeQuestion(1)]).mountSet();
  set.board.state(2, "playing");
  set.moveTo(1);
  set.moveTo(0);
  assert.equal(set.board.index, 1);
  assert.equal(set.board.status, "step_complete");
});

test("one final next-example action starts practice", () => {
  let called = 0;
  const set = new WhiteboardQuestionSet(new Mount(), [makeQuestion(0)], {onPractice:() => called++}).mountSet();
  set.board.options.onNextExample();
  assert.equal(called, 1);
});

test("the whiteboard appears immediately and loads teaching steps without an explanation gate", async () => {
  let finish;
  const deferred = new Promise(resolve => { finish = resolve; });
  const first = {...makeQuestion(0), solution_gated:true};
  const set = new WhiteboardQuestionSet(new Mount(), [first, makeQuestion(1)], {solutionLoader:() => deferred}).mountSet();
  assert.equal(set.board.block.problem, "Problem 1");
  assert.equal(set.board.options.pending, true);
  assert.ok(!set.mount.html.includes("Open explanation"));
  set.board.options.onSelectExample(1);
  finish(makeQuestion(0)); await new Promise(resolve => setImmediate(resolve));
  assert.equal(set.index, 1);
  assert.equal(set.board.block.problem, "Problem 2");
  set.moveTo(0);
  assert.equal(set.board.block.problem, "Problem 1");
  assert.equal(set.board.options.pending, false);
});
