const assert=require("assert"),fs=require("fs"),vm=require("vm"),path=require("path");
global.window=undefined;
vm.runInThisContext(fs.readFileSync(path.join(__dirname,"../js/whiteboard/timeline-controller.js"),"utf8"));

let clock=0,queued=null,cancelled=0;
const narration={spoken:[],paused:0,resumed:0,stopped:0,muted:false,speak(text){this.spoken.push(text);},pause(){this.paused++;},resume(){this.resumed++;},stop(){this.stopped++;},setMuted(value){this.muted=value;}};
const caption={hidden:false,textContent:""};
const stage={querySelector(){return null;},querySelectorAll(){return [];}};
const events=[
  {at_ms:100,type:"caption",text:"Inspect the terms."},
  {at_ms:100,type:"narration",text:"Inspect the terms."},
  {at_ms:900,type:"caption",text:"The differences match."},
  {at_ms:900,type:"narration",text:"The differences match."},
];
const controller=new TimelineController(stage,{duration_ms:1200,events},{caption,narration,now:()=>clock,requestFrame:callback=>(queued=callback,1),cancelFrame:()=>cancelled++});
const applied=[];const originalApply=controller.apply.bind(controller);controller.apply=event=>{applied.push(event.at_ms+":"+event.type);originalApply(event);};
controller.play();clock=500;queued(500);
assert.deepStrictEqual(applied,["100:caption","100:narration"]);assert.strictEqual(caption.textContent,"Inspect the terms.");
controller.pause();const pausedAt=controller.position;clock=900;controller.play();clock=1100;queued(1100);
assert.ok(controller.position>=pausedAt);assert.deepStrictEqual(applied,["100:caption","100:narration"]);
clock=1500;queued(1500);assert.deepStrictEqual(applied,["100:caption","100:narration","900:caption","900:narration"]);
assert.deepStrictEqual(narration.spoken,["Inspect the terms.","The differences match."]);
controller.replay();assert.strictEqual(controller.position,0);assert.strictEqual(controller.cursor,0);assert.ok(narration.stopped>0);

const checkpointEvents=[{at_ms:100,type:"checkpoint",text:"Predict the change",checkpoint_type:"predict_next_step"}];
let checkpoint=null;clock=0;const checkpointController=new TimelineController(stage,{duration_ms:500,events:checkpointEvents},{narration,now:()=>clock,requestFrame:callback=>(queued=callback,2),cancelFrame(){},onCheckpoint:event=>checkpoint=event});
checkpointController.play();clock=150;queued(150);assert.strictEqual(checkpoint.text,"Predict the change");assert.strictEqual(checkpointController.playing,false);

assert.doesNotThrow(()=>new BrowserNarrationProvider().speak("Fallback narration"));
const reduced=new TimelineController(stage,{duration_ms:1200,events},{caption,narration,now:()=>0,requestFrame(){},cancelFrame(){}});const spokenBefore=narration.spoken.length;reduced.completeReducedMotion();assert.strictEqual(reduced.position,1200);assert.strictEqual(narration.spoken.length,spokenBefore);assert.strictEqual(caption.textContent,"The differences match.");
controller.destroy();assert.strictEqual(controller.destroyed,true);
const css=fs.readFileSync(path.join(__dirname,"../css/components.css"),"utf8");assert.ok(css.includes("@media(max-width:640px)"));assert.ok(css.includes("@media(prefers-reduced-motion:reduce)"));
console.log("semantic timeline controller passed");
