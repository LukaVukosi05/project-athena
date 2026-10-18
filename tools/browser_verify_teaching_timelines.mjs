import fs from "node:fs";
import path from "node:path";

const origin="http://127.0.0.1:8000",output=path.resolve("artifacts/grade8-algebraic-equations-lesson1/teaching-timeline-repair");
fs.mkdirSync(output,{recursive:true});
const source=JSON.parse(fs.readFileSync("backend/app/curriculum/grade8/generated/lesson_01.json","utf8"));
const targets=await (await fetch("http://127.0.0.1:9223/json")).json(),target=targets.find(item=>item.type==="page");if(!target)throw new Error("No Chrome target");
const socket=new WebSocket(target.webSocketDebuggerUrl);await new Promise((resolve,reject)=>{socket.onopen=resolve;socket.onerror=reject;});let sequence=0;const pending=new Map();socket.onmessage=event=>{const message=JSON.parse(event.data);if(!message.id||!pending.has(message.id))return;const task=pending.get(message.id);pending.delete(message.id);message.error?task.reject(new Error(message.error.message)):task.resolve(message.result);};
const command=(method,params={})=>new Promise((resolve,reject)=>{const id=++sequence;pending.set(id,{resolve,reject});socket.send(JSON.stringify({id,method,params}));});const delay=ms=>new Promise(resolve=>setTimeout(resolve,ms));
async function evaluate(expression,awaitPromise=false){const result=await command("Runtime.evaluate",{expression,awaitPromise,returnByValue:true});if(result.exceptionDetails)throw new Error(result.exceptionDetails.exception?.description||result.exceptionDetails.text);return result.result.value;}
async function click(selector){await evaluate(`(()=>{const node=document.querySelector(${JSON.stringify(selector)});if(!node)throw new Error('Missing ${selector}');node.click()})()`);}
async function shot(name,video=false){const data=(await command("Page.captureScreenshot",{format:"png",captureBeyondViewport:false})).data;fs.writeFileSync(path.join(output,name),Buffer.from(data,"base64"));if(video)frames.push(data);}
async function state(){return evaluate(`(()=>{const root=document.querySelector('.stateful-whiteboard'),stage=document.querySelector('.whiteboard-stage'),caption=document.querySelector('[data-role="caption"]');return {controller:root.dataset.controllerState,step:document.querySelector('[data-role="position"]').textContent,caption:caption.textContent,operationVisible:!!stage.querySelector('[data-object-id="operation"].is-visible'),resultVisible:!!stage.querySelector('[data-object-id="result"].is-visible'),verificationVisible:!!stage.querySelector('[data-object-id="verification"].is-visible'),html:stage.innerHTML,missing:stage.dataset.missingTargets||'',overflow:stage.scrollWidth>stage.clientWidth+1};})()`);}
await command("Page.enable");await command("Runtime.enable");await command("Emulation.setDeviceMetricsOverride",{width:1440,height:1000,deviceScaleFactor:1,mobile:false});await command("Emulation.setEmulatedMedia",{features:[{name:"prefers-reduced-motion",value:"no-preference"}]});
await command("Page.navigate",{url:`${origin}/lesson.html?grade=grade-8&topic=algebraic-equations&lesson=g8-algebraic-equations-01`});await delay(900);await evaluate(`document.querySelector('.whiteboard-question-set').scrollIntoView({block:'start'})`);
const banned=["Reveal the complete equation","Highlight the left hand side","Place 12 on both scale pans","Show that the scale remains level"];
const reports=[],frames=[],representatives=new Set([0,4,9,14]);
for(let index=0;index<15;index++){
  const sourceQuestion=source.worked_examples[index];await click('[data-example-action="reveal"]');await delay(150);
  const payload=await evaluate(`fetch('/api/v1/lessons/g8-algebraic-equations-01/questions/${sourceQuestion.id}/reveal',{method:'POST'}).then(r=>r.json())`,true);
  const serialized=JSON.stringify(payload);if(serialized.includes("internal_instruction")||banned.some(text=>serialized.includes(text)))throw new Error(`${sourceQuestion.id} leaked authoring instructions`);
  const first=payload.whiteboard.steps[0],operationAt=first.events.find(event=>event.type==="show_operation").at_ms,resultAt=first.events.find(event=>event.type==="reveal"&&event.targets.includes("result")).at_ms;
  const initial=await state();if(initial.missing||initial.overflow||initial.operationVisible||initial.resultVisible||banned.some(text=>initial.caption.includes(text)))throw new Error(`${sourceQuestion.id} invalid initial state ${JSON.stringify(initial)}`);
  await shot(`${sourceQuestion.id}-initial.png`,representatives.has(index));await click('[data-action="primary"]');await delay(operationAt+250);const operation=await state();if(!operation.operationVisible||operation.resultVisible||operation.html===initial.html)throw new Error(`${sourceQuestion.id} operation did not animate`);await shot(`${sourceQuestion.id}-operation.png`,representatives.has(index));
  await delay(Math.max(100,resultAt-operationAt+250));const result=await state();if(!result.resultVisible||result.html===operation.html)throw new Error(`${sourceQuestion.id} result did not follow operation`);await shot(`${sourceQuestion.id}-result.png`,representatives.has(index));
  if(result.controller==="playing")await click('[data-action="primary"]');
  await click('.whiteboard-settings>summary');await click('[data-action="reduced-motion"]');await click('[data-action="restart"]');await click('.whiteboard-settings>summary');
  let middle=null;
  for(let step=0;step<payload.whiteboard.steps.length;step++){
    if(step>0)await click('[data-action="primary"]');
    await click('[data-action="primary"]');await delay(20);
    const current=await state();if(!current.operationVisible||!current.resultVisible||current.caption!==payload.whiteboard.steps[step].narration)throw new Error(`${sourceQuestion.id} reduced-motion step ${step+1} lost teaching content`);
    if(step===Math.floor(payload.whiteboard.steps.length/2))middle=current;
  }
  const final=await state();if(final.controller!=="example_complete"||!final.verificationVisible||!final.caption.toLowerCase().match(/check|substitut|confirm|original|verif/))throw new Error(`${sourceQuestion.id} verification is incomplete`);
  await shot(`${sourceQuestion.id}-middle.png`,representatives.has(index));await shot(`${sourceQuestion.id}-verification.png`,representatives.has(index));
  const replayBefore=final.html;await click('[data-action="replay"]');const replayAfter=(await state()).html;if(replayBefore!==replayAfter)throw new Error(`${sourceQuestion.id} replay is not deterministic`);
  await click('[data-action="previous"]');const previous=await state();if(previous.step===final.step)throw new Error(`${sourceQuestion.id} previous did not reconstruct`);await click('[data-action="primary"]');await click('[data-action="primary"]');const restored=await state();if(restored.step!==final.step||restored.html!==final.html)throw new Error(`${sourceQuestion.id} next did not reconstruct verification`);
  reports.push({question_id:sourceQuestion.id,steps:payload.whiteboard.steps.length,initial_caption:initial.caption,middle_caption:middle.caption,verification_caption:final.caption,operation_animated:true,result_after_operation:true,replay_deterministic:true});
  if(index<14)await click('[data-action="primary"]');
  console.log(`verified ${sourceQuestion.id}`);
}
const video=await evaluate(`(async()=>{const frames=${JSON.stringify(frames)};const canvas=document.createElement('canvas');canvas.width=960;canvas.height=667;const ctx=canvas.getContext('2d');const stream=canvas.captureStream(4);const recorder=new MediaRecorder(stream,{mimeType:'video/webm'});const chunks=[];recorder.ondataavailable=e=>chunks.push(e.data);const stopped=new Promise(resolve=>recorder.onstop=resolve);recorder.start();for(const frame of frames){const image=new Image();image.src='data:image/png;base64,'+frame;await image.decode();ctx.drawImage(image,0,0,canvas.width,canvas.height);await new Promise(resolve=>setTimeout(resolve,650));}recorder.stop();await stopped;const bytes=new Uint8Array(await new Blob(chunks,{type:'video/webm'}).arrayBuffer());let binary='';for(let i=0;i<bytes.length;i+=8192)binary+=String.fromCharCode(...bytes.subarray(i,i+8192));return btoa(binary);})()`,true);
fs.writeFileSync(path.join(output,"examples-01-05-10-15-mathematical-teaching.webm"),Buffer.from(video,"base64"));fs.writeFileSync(path.join(output,"browser-verification.json"),JSON.stringify(reports,null,2));console.log(JSON.stringify({examples:reports.length,videoFrames:frames.length},null,2));socket.close();
