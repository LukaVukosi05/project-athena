const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

global.escapeWhiteboardHtml = value => String(value).replaceAll("&", "&amp;").replaceAll("<", "&lt;");
global.AthenaVisualizationResolver = { resolve() { return null; } };
global.AthenaWhiteboardRegistry = { resolve() { return { render() { return '<div data-object-id="model">Diagram</div>'; } }; } };
global.matchMedia = () => ({ matches:false });
global.CSS = { escape:value => value };
vm.runInThisContext(fs.readFileSync(path.join(__dirname, "../js/whiteboard/stateful-whiteboard.js"), "utf8"));

for (const [topic, type] of [["fn", "function_graph"], ["rules", "trigonometry"], ["stat", "statistics"], ["prob", "statistics"], ["fin", "finance"]]) {
  test(`Grade 11 ${topic} keeps the growing written solution beside its visual`, () => {
    const stage = {
      dataset:{}, innerHTML:"", scrollTarget:{ scrollTop:0, scrollHeight:100 }, setAttribute(){},
      querySelector(selector) { return selector === ".g8-completed-steps" && this.innerHTML.includes('class="g8-completed-steps"') ? this.scrollTarget : null; },
    };
    const checkpoint = { hidden:false };
    const mount = { querySelector(selector) { return selector === '[data-role="checkpoint"]' ? checkpoint : stage; } };
    const steps = [1, 2, 3].map(n => ({
      id:`step-${n}`, operation:{type:"test"}, after_expression:`${n}. ${["Find the given", "Calculate the value", "Check the answer"][n-1]}`,
      working_expression:`Working ${n}`, screen_reader_description:`Step ${n}`, events:[],
    }));
    const board = Object.create(StatefulWhiteboard.prototype);
    Object.assign(board, { mount, index:0, block:{
      id:`g11-${topic}-l01-w01-board`, problem:"Find the value", initial_expression:"Read the original question",
      visualization:{type}, steps,
    }, visualSession:{ render() { return '<figure data-object-id="problem">Question-specific diagram</figure>'; } },
    stopTimeline(){}, renderTeachingNotes(){}, renderOpeningCaption(){}, setStatus(status){this.status=status;},
    createTimeline(){}, applyCompleteTimeline(){}, diagnosticContext:{}, destroyed:false });

    board.reconstruct("ready", "idle");
    assert.equal(stage.dataset.layout, "split");
    assert.match(stage.innerHTML, /Written solution so far/);
    assert.doesNotMatch(stage.innerHTML, /<li/);
    board.reconstruct("result", "step_complete");
    assert.deepEqual([...stage.innerHTML.matchAll(/<li/g)].map(() => true), [true]);
    assert.match(stage.innerHTML, /Find the given/);
    board.index = 1;
    board.reconstruct("ready", "idle");
    assert.match(stage.innerHTML, /Find the given/);
    assert.doesNotMatch(stage.innerHTML, /Calculate the value/);
    board.reconstruct("result", "step_complete");
    assert.match(stage.innerHTML, /Find the given[\s\S]*Calculate the value/);
    board.index = 2;
    board.reconstruct("result", "example_complete");
    assert.match(stage.innerHTML, /Find the given[\s\S]*Calculate the value[\s\S]*Check the answer/);
    board.index = 1;
    board.reconstruct("result", "step_complete");
    assert.doesNotMatch(stage.innerHTML, /Check the answer/);
    assert.match(stage.innerHTML, /Question-specific diagram/);
  });
}
