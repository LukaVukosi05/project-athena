const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

global.escapeWhiteboardHtml = value => String(value).replace(/[&<>"']/g, character => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[character]));
vm.runInThisContext(fs.readFileSync(path.join(__dirname, "../js/visualization/visualization-registry.js"), "utf8"));
vm.runInThisContext(fs.readFileSync(path.join(__dirname, "../js/visualization/algebra/grade8-equation-renderers.js"), "utf8"));
vm.runInThisContext(fs.readFileSync(path.join(__dirname, "../js/whiteboard/timeline-controller.js"), "utf8"));

const state = (before, working, after, action, phase="operation", target="left-expression", stage=1) => ({
  before_state:before, working_state:working, after_state:after, target,
  annotations:[`stage:${stage}`,`action:${action}`,`phase:${phase}`],
});
const parameters = { question_id:"g8-ae-l01-w02", prompt:"Complete 9 + 4 = □ + 5.", source_data:"left expression=9 + 4;right expression=□ + 5" };

test("Example 2 uses a stable focused stage with native semantic objects", () => {
  const renderer = AthenaVisualizationRegistry.resolve("algebra", "equality_balance");
  const initial = renderer.render(parameters, state("9 + 4 = □ + 5", "9 + 4 → 13", "13 = □ + 5", "evaluate_expression"), "operation");
  const inverse = renderer.render(parameters, state("13 = □ + 5", "13 − 5 = □", "8 = □", "remove_from_both_sides", "operation", "right-expression", 2), "operation");
  const substitution = renderer.render(parameters, state("□ = 8", "9 + 4 = 8 + 5", "13 = 8 + 5", "substitute_value", "operation", "variable-slot", 4), "result");
  const verification = renderer.render(parameters, state("13 = 13 — balanced", "9 + 4 = 8 + 5", "Checked: 13 = 13; therefore □ = 8", "verify_solution", "verification", "verification", 6), "result");
  for (const markup of [initial,inverse,substitution,verification]) {
    assert.ok(markup.includes('class="g8-action-slot"'));
    assert.ok(markup.includes('data-object-id="balance-left-pan"'));
    assert.ok(markup.includes('data-object-id="balance-right-pan"'));
    assert.ok(markup.includes('data-object-id="left-operation"'));
    assert.ok(markup.includes('data-object-id="right-operation"'));
    assert.ok(!markup.includes("math-history"), "the active stage must not grow a transcript");
  }
  assert.ok(initial.includes("9 + 4"));
  assert.ok(inverse.includes("13 − 5 = □"));
  assert.ok(substitution.includes("13 = 8 + 5"));
  assert.ok(verification.includes("Checked: 13 = 13; therefore □ = 8"));
});

test("balance states, unknown replacement and equality reversal are visibly distinct", () => {
  const renderer = AthenaVisualizationRegistry.resolve("algebra", "equality_balance");
  const level = renderer.render(parameters, state("13 = 13", "compare", "13 = 13 — balanced", "balance_scale"), "result");
  const tilted = renderer.render(parameters, state("5 ≠ 8", "compare", "5 ≠ 8", "diagnose_error"), "result");
  assert.ok(level.includes("is-level"));
  assert.ok(tilted.includes("is-right-heavy"));
  assert.notEqual(level, tilted);
  const source = fs.readFileSync(path.join(__dirname, "../js/whiteboard/timeline-controller.js"), "utf8");
  for (const operation of ["evaluate_expression","introduce_inverse","apply_to_both_sides","cancel_inverse_pair","substitute_value","replace_unknown","reverse_equality","compare_both_sides","tilt_balance","restore_balance","mark_incorrect_step","repair_incorrect_step","verify_original","show_conclusion"]) assert.ok(source.includes(operation), operation);
});

test("automatic completion waits for both the visual and narration", async () => {
  let clock=0, frame, resolveSpeech, completions=0;
  const narration={speak(){return new Promise(resolve=>{resolveSpeech=resolve;});},pause(){},resume(){},stop(){},setMuted(){}};
  const stage={querySelector(){return null;},querySelectorAll(){return [];}};
  const controller=new TimelineController(stage,{duration_ms:100,events:[{at_ms:0,type:"narration",text:"A complete sentence."}]},{narration,now:()=>clock,requestFrame:callback=>(frame=callback,1),cancelFrame(){},onStateChange:current=>{if(!current.playing&&current.position===100)completions+=1;}});
  controller.play();clock=150;frame(150);
  assert.equal(controller.visualComplete,true);assert.equal(controller.playing,true);assert.equal(completions,0);
  resolveSpeech("ended");await new Promise(resolve=>setImmediate(resolve));
  assert.equal(controller.playing,false);assert.equal(completions,1);
});

test("stale narration cannot advance a replayed session", async () => {
  let clock=0, frame, firstResolve, stateChanges=0;
  const narration={speak(){return new Promise(resolve=>{firstResolve=resolve;});},pause(){},resume(){},stop(){},setMuted(){}};
  const stage={querySelector(){return null;},querySelectorAll(){return [];}};
  const controller=new TimelineController(stage,{duration_ms:100,events:[{at_ms:0,type:"narration",text:"Old session."}]},{narration,now:()=>clock,requestFrame:callback=>(frame=callback,1),cancelFrame(){},onStateChange:()=>stateChanges++});
  controller.play();clock=150;frame(150);controller.reset();const changesAfterReset=stateChanges;firstResolve("ended");await new Promise(resolve=>setImmediate(resolve));
  assert.equal(controller.position,0);assert.equal(controller.playing,false);assert.equal(stateChanges,changesAfterReset);
});

test("browser speech resolves on completion, pauses safely and has a bounded failure fallback", async () => {
  const originalUtterance=global.SpeechSynthesisUtterance,originalSynthesis=global.speechSynthesis;
  const calls={speak:0,pause:0,resume:0,cancel:0};let utterance;const timerCallbacks=[];
  global.SpeechSynthesisUtterance=class{constructor(text){this.text=text;}};
  global.speechSynthesis={speaking:false,speak(value){calls.speak+=1;utterance=value;},pause(){calls.pause+=1;},resume(){calls.resume+=1;},cancel(){calls.cancel+=1;}};
  const provider=new BrowserNarrationProvider({setTimer(callback){timerCallbacks.push(callback);return timerCallbacks.length;},clearTimer(){},now:()=>0,fallbackPollMs:100});
  const finished=provider.speak("Both sides remain equal.");provider.pause();provider.resume();utterance.onend();assert.equal(await finished,"ended");
  assert.deepEqual({speak:calls.speak,pause:calls.pause,resume:calls.resume},{speak:1,pause:1,resume:1});
  global.speechSynthesis.speaking=true;
  let settled=false;
  const guarded=provider.speak("A longer explanation must not be cut off while the browser is still speaking.");guarded.then(()=>{settled=true;});
  timerCallbacks.at(-1)();await new Promise(resolve=>setImmediate(resolve));
  assert.equal(settled,false,"the watchdog must not advance the timeline during active speech");
  global.speechSynthesis.speaking=false;
  timerCallbacks.at(-1)();assert.equal(await guarded,"fallback");
  provider.setMuted(true);assert.equal(await provider.speak("Muted narration."),"unavailable");
  global.SpeechSynthesisUtterance=originalUtterance;global.speechSynthesis=originalSynthesis;
});

test("audio-off and reduced-motion progression preserve every teaching event", async () => {
  let clock=0,frame,completed=0;const applied=[];
  const narration={speak(){return Promise.resolve("muted");},pause(){},resume(){},stop(){},setMuted(){}};
  const stage={querySelector(){return null;},querySelectorAll(){return [];}};
  const step={duration_ms:100,events:[{at_ms:0,type:"caption",text:"Explain."},{at_ms:20,type:"focus_object",targets:[]},{at_ms:40,type:"show_operation",targets:[],label:"operation"},{at_ms:80,type:"reveal",targets:[]}]};
  const controller=new TimelineController(stage,step,{narration,now:()=>clock,requestFrame:callback=>(frame=callback,1),cancelFrame(){},onStateChange:current=>{if(!current.playing&&current.position===100)completed+=1;}});
  const original=controller.apply.bind(controller);controller.apply=event=>{applied.push(event.type);original(event);};controller.play();clock=120;frame(120);await new Promise(resolve=>setImmediate(resolve));
  assert.equal(completed,1);assert.deepEqual(applied,["caption","focus_object","show_operation","reveal"]);
  applied.length=0;controller.completeReducedMotion();assert.deepEqual(applied,["caption","focus_object","show_operation","reveal"]);
});

test("the integrated dock has one primary action and no duplicate replay at completion", () => {
  const source=fs.readFileSync(path.join(__dirname,"../js/whiteboard/stateful-whiteboard.js"),"utf8");
  const css=fs.readFileSync(path.join(__dirname,"../css/components.css"),"utf8");
  assert.equal((source.match(/data-action="primary"/g)||[]).length,2, "one button plus one event binding");
  assert.ok(source.includes('replay.hidden = status === "example_complete"'));
  assert.ok(source.includes('class="whiteboard-step-navigation"'));
  assert.ok(source.includes('class="whiteboard-secondary-controls"'));
  assert.ok(source.includes('class="whiteboard-solution-trail"'));
  assert.ok(css.includes(".g8-action-slot{display:grid"));
  assert.ok(css.includes("grid-area:1/1"));
  assert.ok(css.includes("min-height:44px"));
  assert.ok(css.includes("@media(max-width:640px)"));
  assert.ok(css.includes("@media(prefers-reduced-motion:reduce)"));
});
