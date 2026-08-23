const assert = require("assert");
const fs = require("fs");
const vm = require("vm");

global.location = { href: "https://athena.test/lesson.html?lesson=trig" };
global.history = { replaceState() {} };
global.escapeWhiteboardHtml = value => String(value);

class Element {
  constructor() { this.hidden = false; this.disabled = false; this.onclick = null; }
}
class Mount {
  set innerHTML(value) {
    this.html = value; this.nodes = { board: new Mount(), completion: new Element() };
    for (const action of ["previous", "practice", "next"]) if (value.includes(`data-example-action="${action}"`)) this.nodes[action] = new Element();
    this.nodes.completion.hidden = value.includes('data-role="example-completion" hidden');
  }
  get innerHTML() { return this.html; }
  querySelector(selector) {
    if (selector === '[data-role="current-whiteboard"]') return this.nodes.board;
    if (selector === '[data-role="example-completion"]') return this.nodes.completion;
    const match = selector.match(/data-example-action="([^"]+)/); return match ? this.nodes[match[1]] || null : null;
  }
}
global.StatefulWhiteboard = class {
  constructor(mount, block, options) { this.block = block; this.index = options.initialStep; this.options = options; }
  mountBoard() { return this; }
  complete() { this.index = this.block.steps.length - 1; this.options.onStateChange(this.index); }
};

vm.runInThisContext(fs.readFileSync(require("path").join(__dirname, "../js/whiteboard/whiteboard-question-set.js"), "utf8"));
const makeQuestion = (index, count = 3) => ({ difficulty: index ? "easy" : "foundation", guidance_level: "high", whiteboard: { problem: `Problem ${index + 1}`, steps: new Array(count).fill({}) } });

const mount = new Mount();
let practised = false;
const set = new WhiteboardQuestionSet(mount, new Array(12).fill(null).map((_, index) => makeQuestion(index)), { onPractice: () => { practised = true; } }).mountSet();
assert.strictEqual(set.board.block.problem, "Problem 1");
assert.strictEqual(mount.nodes.completion.hidden, true);
set.board.complete();
assert.strictEqual(mount.nodes.completion.hidden, false);
mount.nodes.next.onclick();
assert.strictEqual(set.board.block.problem, "Problem 2");
assert.strictEqual(set.board.index, 0);
set.board.complete();
mount.nodes.previous.onclick();
assert.strictEqual(set.board.block.problem, "Problem 1");
assert.strictEqual(set.board.index, 2);
set.index = 11; set.render(); set.board.complete();
assert.ok(mount.innerHTML.includes("Start Practice"));

const singleMount = new Mount();
const single = new WhiteboardQuestionSet(singleMount, [makeQuestion(0)], { onPractice: () => { practised = true; } }).mountSet();
single.board.complete();
assert.ok(singleMount.innerHTML.includes("Start Practice"));
assert.ok(!singleMount.innerHTML.includes("Next Example →"));
singleMount.nodes.next.onclick();
assert.strictEqual(practised, true);
console.log("whiteboard question-set flow passed");
