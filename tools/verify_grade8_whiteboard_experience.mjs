import { spawn } from "node:child_process";
import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";

const baseUrl="http://127.0.0.1:8011";
const output=path.resolve("artifacts/grade8-algebraic-equations-lesson1/whiteboard-experience");
mkdirSync(output,{recursive:true});
const chromePath="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const chrome=spawn(chromePath,["--headless=new","--remote-debugging-port=9228",`--user-data-dir=${path.join(output,"chrome-profile")}`,"--window-size=1440,1000","--disable-gpu","--no-first-run"],{stdio:"ignore"});
const delay=ms=>new Promise(resolve=>setTimeout(resolve,ms));
async function poll(url){for(let i=0;i<80;i+=1){try{const response=await fetch(url);if(response.ok)return response.json();}catch(_){}await delay(100);}throw new Error(`Unavailable: ${url}`);}
class CDP{
  constructor(url){this.socket=new WebSocket(url);this.next=1;this.pending=new Map();this.socket.onmessage=event=>{const message=JSON.parse(event.data);if(!message.id)return;const pending=this.pending.get(message.id);this.pending.delete(message.id);message.error?pending.reject(new Error(message.error.message)):pending.resolve(message.result);};}
  ready(){return new Promise((resolve,reject)=>{this.socket.onopen=resolve;this.socket.onerror=reject;});}
  send(method,params={}){const id=this.next++;return new Promise((resolve,reject)=>{this.pending.set(id,{resolve,reject});this.socket.send(JSON.stringify({id,method,params}));});}
}
await poll("http://127.0.0.1:9228/json/version");
const target=await fetch(`http://127.0.0.1:9228/json/new?${encodeURIComponent(baseUrl)}`,{method:"PUT"}).then(response=>response.json());
const cdp=new CDP(target.webSocketDebuggerUrl);await cdp.ready();await cdp.send("Page.enable");await cdp.send("Runtime.enable");
const evaluate=async expression=>{const result=await cdp.send("Runtime.evaluate",{expression,awaitPromise:true,returnByValue:true});if(result.exceptionDetails)throw new Error(result.exceptionDetails.exception?.description||result.exceptionDetails.text);return result.result.value;};
const waitFor=async(expression,timeout=20000)=>{const started=Date.now();while(Date.now()-started<timeout){if(await evaluate(expression))return;await delay(80);}const debug=await evaluate(`({url:location.href,ready:document.readyState,body:document.body?.innerText?.slice(0,1200),scripts:[...document.scripts].map(item=>item.src)})`);throw new Error(`Timed out: ${expression}\n${JSON.stringify(debug)}`);};
const click=selector=>evaluate(`(()=>{const node=document.querySelector(${JSON.stringify(selector)});if(!node)throw new Error('Missing ${selector}');node.click();return true})()`);
const frames=[];
async function shot(name,record=true){const data=(await cdp.send("Page.captureScreenshot",{format:"png",captureBeyondViewport:false})).data;writeFileSync(path.join(output,name),Buffer.from(data,"base64"));if(record)frames.push(data);}
async function scroll(selector,block="center"){await evaluate(`document.querySelector(${JSON.stringify(selector)})?.scrollIntoView({block:${JSON.stringify(block)}})`);await delay(120);}
async function navigate(example,width=1440,height=1000){
  await cdp.send("Emulation.setDeviceMetricsOverride",{width,height,deviceScaleFactor:1,mobile:width<700});
  await cdp.send("Page.navigate",{url:`${baseUrl}/lesson.html?grade=grade-8&topic=algebraic-equations&lesson=g8-algebraic-equations-01&example=${example}`});
  await waitFor(`document.querySelector('[data-example-action="reveal"]')`);await click('[data-example-action="reveal"]');await waitFor(`document.querySelector('.stateful-whiteboard')`);await scroll('.stateful-whiteboard','start');
}
const setReduced=enabled=>evaluate(`(()=>{const input=document.querySelector('[data-action="reduced-motion"]');if(input.checked!==${enabled})input.click();return input.checked})()`);
const setMuted=muted=>evaluate(`(()=>{const button=document.querySelector('[data-action="mute"]');const isMuted=button.getAttribute('aria-pressed')==='true';if(isMuted!==${muted})button.click();return button.getAttribute('aria-pressed')})()`);
const boardState=()=>evaluate(`(()=>{const board=document.querySelector('.stateful-whiteboard'),stage=document.querySelector('.whiteboard-stage'),dock=document.querySelector('.whiteboard-control-bar'),visual=document.querySelector('.g8-equation-visual');return {status:board?.dataset.controllerState,step:document.querySelector('[data-role="position"]')?.textContent,question:visual?.dataset.questionId,stage:visual?.dataset.stage,action:visual?.dataset.action,caption:document.querySelector('[data-role="caption"]')?.textContent,operationVisible:!!stage?.querySelector('[data-object-id="operation"].is-visible'),resultVisible:!!stage?.querySelector('[data-object-id="result"].is-visible'),verificationVisible:!!stage?.querySelector('[data-object-id="verification"].is-visible'),focused:stage?.querySelectorAll('.is-focused').length||0,missing:stage?.dataset.missingTargets||'',history:stage?.querySelectorAll('.math-history').length||0,pageOverflow:document.documentElement.scrollWidth-document.documentElement.clientWidth,stageOverflow:stage?stage.scrollWidth-stage.clientWidth:0,stageHeight:stage?.getBoundingClientRect().height,dockHeight:dock?.getBoundingClientRect().height,primary:document.querySelector('[data-action="primary"]')?.textContent,replayHidden:document.querySelector('[data-action="replay"]')?.hidden,html:stage?.innerHTML||''};})()`);
const payload=questionId=>evaluate(`fetch('/api/v1/lessons/g8-algebraic-equations-01/questions/${questionId}/reveal',{method:'POST'}).then(response=>response.json())`);
async function finishReduced(){
  await setMuted(true);await setReduced(true);
  for(let guard=0;guard<12;guard+=1){const state=await boardState();if(state.status==="example_complete")return;if(state.status==="playing")await click('[data-action="primary"]');await click('[data-action="primary"]');await delay(40);}
  throw new Error(`Could not finish ${JSON.stringify(await boardState())}`);
}
async function inspectFirstOperation(example,file){
  await navigate(example);await setMuted(true);await setReduced(false);
  const id=`g8-ae-l01-w${String(example).padStart(2,"0")}`,data=await payload(id),step=data.whiteboard.steps[0];
  await click('[data-action="primary"]');await delay(450);const focus=await boardState();
  const operationAt=step.events.find(event=>event.type==="show_operation").at_ms;await delay(Math.max(0,operationAt-450+180));const operation=await boardState();await shot(file);
  const resultAt=step.events.find(event=>event.type==="reveal"&&event.targets.includes("result")).at_ms;await delay(Math.max(0,resultAt-operationAt+150));const result=await boardState();
  if(!focus.focused||!operation.operationVisible||operation.resultVisible||!result.resultVisible)throw new Error(`${id} does not visibly perform focus, operation, result`);
  await click('[data-action="primary"]');const paused=await boardState();await click('[data-action="primary"]');const continued=await boardState();
  if(paused.status!=="paused"||continued.status!=="playing")throw new Error(`${id} Pause/Continue failed`);
  await click('[data-action="primary"]');await click('[data-action="replay"]');await delay(120);const replayed=await boardState();
  if(replayed.status!=="playing"||replayed.step!==focus.step)throw new Error(`${id} Replay failed`);
  await click('[data-action="primary"]');await setReduced(true);await click('[data-action="replay"]');await delay(50);
  const reconstructed=await boardState();await click('[data-action="next"]');const next=await boardState();await click('[data-action="previous"]');const previous=await boardState();
  if(reconstructed.status!=="step_complete"||next.step===reconstructed.step||previous.step!==reconstructed.step)throw new Error(`${id} Previous/Next reconstruction failed`);
  return {id,focus:focus.focused,operation:operation.action,result:result.resultVisible,pause:paused.status,continue:continued.status,replay:replayed.status,next:next.step,previous:previous.step};
}

await navigate(1);await setMuted(true);await shot("example-01__initial.png");await scroll('.whiteboard-control-bar','center');await shot("desktop-controls.png");await scroll('.stateful-whiteboard','start');
const example1=await payload("g8-ae-l01-w01"),first1=example1.whiteboard.steps[0];await click('[data-action="primary"]');await delay(first1.events.find(event=>event.type==="show_operation").at_ms+160);await shot("example-01__operation.png");await delay(first1.events.find(event=>event.type==="reveal"&&event.targets.includes("result")).at_ms-first1.events.find(event=>event.type==="show_operation").at_ms+160);await shot("example-01__result.png");
await click('[data-action="primary"]');await click('[data-action="primary"]');await click('[data-action="primary"]');await click('[data-action="replay"]');await delay(100);if((await boardState()).status!=="playing")throw new Error("Example 1 Replay from pause failed");await click('[data-action="primary"]');await setReduced(true);await click('[data-action="replay"]');const example1Step=await boardState();await click('[data-action="next"]');const example1Next=await boardState();await click('[data-action="previous"]');if(example1Step.step===example1Next.step||(await boardState()).step!==example1Step.step)throw new Error("Example 1 Previous/Next failed");

await navigate(2);await setMuted(true);await shot("example-02__initial.png");const example2=await payload("g8-ae-l01-w02");
await setReduced(true);await click('[data-action="primary"]');await setReduced(false);await click('[data-action="primary"]');const inverseStep=example2.whiteboard.steps[1],inverseAt=inverseStep.events.find(event=>event.type==="introduce_inverse").at_ms;await delay(inverseAt+160);let inverseState=await boardState();await shot("example-02__inverse-operation.png");if(!inverseState.operationVisible)throw new Error("Example 2 inverse operation is not visible");
await click('[data-action="primary"]');await setReduced(true);await click('[data-action="replay"]');await click('[data-action="primary"]');await setReduced(false);await click('[data-action="primary"]');const substituteStep=example2.whiteboard.steps[3],subAt=substituteStep.events.find(event=>event.type==="substitute_value").at_ms;await delay(subAt+160);let substitutionState=await boardState();await shot("example-02__substitution.png");if(!substitutionState.operationVisible)throw new Error("Example 2 substitution operation is not visible");
await click('[data-action="primary"]');await setReduced(true);await click('[data-action="replay"]');await finishReduced();await scroll('.g8-verification','center');await shot("example-02__verification.png");const example2Final=await boardState();
await click('[data-action="previous"]');const example2Previous=await boardState();await click('[data-action="primary"]');const example2Restored=await boardState();if(example2Previous.step===example2Final.step||example2Restored.status!=="example_complete")throw new Error("Example 2 Previous/Next reconstruction failed");await click('[data-action="primary"]');if((await boardState()).step!=="Step 1 of 6")throw new Error("Example 2 primary Replay lesson failed");
const requiredStates=["9 + 4 = □ + 5","13 = □ + 5","8 = □","□ = 8","9 + 4 = 8 + 5","13 = 13"];
const serialised2=JSON.stringify(example2);for(const required of requiredStates)if(!serialised2.includes(required))throw new Error(`Example 2 missing ${required}`);
const operations2=example2.whiteboard.steps.flatMap(step=>step.events.map(event=>event.type));for(const required of ["evaluate_expression","introduce_inverse","apply_to_both_sides","cancel_inverse_pair","reverse_equality","substitute_value","replace_unknown","compare_both_sides","restore_balance","verify_original","show_conclusion"])if(!operations2.includes(required))throw new Error(`Example 2 missing ${required}`);

const representatives=[];for(const [number,file] of [[5,"example-05__operation.png"],[10,"example-10__operation.png"],[15,"example-15__operation.png"]])representatives.push(await inspectFirstOperation(number,file));

const allExamples=[];
for(let number=1;number<=15;number+=1){
  await navigate(number);const id=`g8-ae-l01-w${String(number).padStart(2,"0")}`,data=await payload(id),initial=await boardState();
  if(initial.missing||initial.history||initial.pageOverflow>1||initial.stageOverflow>1||initial.resultVisible||initial.verificationVisible)throw new Error(`${id} invalid initial state ${JSON.stringify(initial)}`);
  const heights=[];await setMuted(true);await setReduced(true);
  for(let guard=0;guard<data.whiteboard.steps.length+2;guard+=1){const current=await boardState();heights.push(current.stageHeight);if(current.status==="example_complete")break;await click('[data-action="primary"]');await delay(35);}
  const final=await boardState();if(final.status!=="example_complete"||!final.verificationVisible||final.missing||final.history||final.pageOverflow>1||final.stageOverflow>1||!final.replayHidden)throw new Error(`${id} invalid final state ${JSON.stringify(final)}`);
  if(Math.max(...heights)-Math.min(...heights)>120)throw new Error(`${id} stage grew vertically: ${heights.join(",")}`);
  allExamples.push({id,steps:data.whiteboard.steps.length,initialAnswerHidden:!initial.resultVisible,verified:final.verificationVisible,stableHeightRange:Math.max(...heights)-Math.min(...heights),caption:final.caption});
}

await navigate(1);await setMuted(true);await setReduced(true);await click('[data-action="primary"]');await shot("reduced-motion.png");
await navigate(1,390,844);await setMuted(true);await scroll('.whiteboard-control-bar','center');await shot("mobile-controls.png");const mobile=await boardState();if(mobile.pageOverflow>1||mobile.stageOverflow>1)throw new Error(`Mobile overflow ${JSON.stringify(mobile)}`);
await navigate(1);await setMuted(false);const audioOn=await evaluate(`document.querySelector('[data-action="mute"]').textContent`);await click('[data-action="primary"]');await delay(300);await click('[data-action="primary"]');await click('[data-action="primary"]');await click('[data-action="primary"]');await click('[data-action="replay"]');await delay(100);await click('[data-example-action="next"]');const rapid=await boardState();if(audioOn!=="Audio on"||rapid.question!=="g8-ae-l01-w02")throw new Error("Audio, narration Replay, or example-switch cleanup failed");

const video=await evaluate(`(async()=>{const frames=${JSON.stringify(frames)};const canvas=document.createElement('canvas');canvas.width=960;canvas.height=667;const context=canvas.getContext('2d');const stream=canvas.captureStream(4);const recorder=new MediaRecorder(stream,{mimeType:'video/webm'});const chunks=[];recorder.ondataavailable=event=>chunks.push(event.data);const stopped=new Promise(resolve=>recorder.onstop=resolve);recorder.start();for(const frame of frames){const image=new Image();image.src='data:image/png;base64,'+frame;await image.decode();context.drawImage(image,0,0,canvas.width,canvas.height);await new Promise(resolve=>setTimeout(resolve,500));}recorder.stop();await stopped;const bytes=new Uint8Array(await new Blob(chunks,{type:'video/webm'}).arrayBuffer());let binary='';for(let index=0;index<bytes.length;index+=8192)binary+=String.fromCharCode(...bytes.subarray(index,index+8192));return btoa(binary);})()`,true);
writeFileSync(path.join(output,"whiteboard-experience.webm"),Buffer.from(video,"base64"));
writeFileSync(path.join(output,"browser-verification.json"),JSON.stringify({checkedAt:new Date().toISOString(),allExamples,example2:{requiredStates,semanticOperations:operations2,final:example2Final},representatives,mobile,rapid},null,2));
cdp.socket.close();chrome.kill();console.log(JSON.stringify({examples:allExamples.length,representatives:representatives.length,example2Behaviours:16,mobileOverflow:mobile.pageOverflow,videoFrames:frames.length},null,2));
