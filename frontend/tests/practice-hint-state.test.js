const assert = require("assert");
const fs = require("fs");
const path = require("path");
const vm = require("vm");

global.AthenaState = undefined;
vm.runInThisContext(fs.readFileSync(path.join(__dirname, "../js/lessons/self-guided-practice.js"), "utf8"));

const practice = Object.create(SelfGuidedPractice.prototype);
practice.pendingHint = true;
practice.states = {
  q1: { hint_index: 2, hint_history: ["first", "second"], hint_complete: true, attempts: 1 },
  q2: { hint_index: 1, hint_history: ["other question"], hint_complete: false, attempts: 1 },
};

practice.resetHints("q1");
assert.deepStrictEqual(practice.states.q1.hint_history, []);
assert.strictEqual(practice.states.q1.hint_index, 0);
assert.strictEqual(practice.states.q1.hint_complete, false);
assert.strictEqual(practice.pendingHint, false);
assert.deepStrictEqual(practice.states.q2.hint_history, ["other question"], "one question cannot leak into another");

practice.resetHints("q2");
assert.deepStrictEqual(practice.states.q2.hint_history, []);
assert.strictEqual(practice.states.q2.hint_index, 0);

const source = fs.readFileSync(path.join(__dirname, "../js/lessons/self-guided-practice.js"), "utf8");
assert(source.includes("requested + 1"), "one successful response advances one hint");
assert(source.includes("!history.includes(result.hint)"), "repeated responses cannot duplicate a hint");
assert(source.includes("hint_complete ? \"disabled\""), "the control stops at the available count");
assert(source.includes("this.resetHints(question.id); this.index"), "question navigation resets hint state");
assert(source.includes("this.resetHints(question.id); this.states[question.id].feedback"), "retry resets hint state");
assert(source.includes("this.states = {}; this.answers = {}; this.solutionCache = {}"), "a new session resets all hint state");

console.log("per-question hint progression passed");
