import fs from "node:fs";
import path from "node:path";

const origin = "http://127.0.0.1:8000";
const output = path.resolve("artifacts/grade8-algebraic-equations-lesson1");
fs.mkdirSync(output, { recursive: true });
const source = JSON.parse(fs.readFileSync("backend/app/curriculum/grade8/generated/lesson_01.json", "utf8"));
const targets = await (await fetch("http://127.0.0.1:9222/json")).json();
const target = targets.find(item => item.type === "page");
if (!target) throw new Error("No Chrome page target is available");
const socket = new WebSocket(target.webSocketDebuggerUrl);
await new Promise((resolve, reject) => { socket.onopen = resolve; socket.onerror = reject; });
let sequence = 0;
const pending = new Map();
socket.onmessage = event => {
  const message = JSON.parse(event.data);
  if (!message.id || !pending.has(message.id)) return;
  const { resolve, reject } = pending.get(message.id); pending.delete(message.id);
  if (message.error) reject(new Error(message.error.message)); else resolve(message.result);
};
function command(method, params = {}) {
  return new Promise((resolve, reject) => { const id = ++sequence; pending.set(id, { resolve, reject }); socket.send(JSON.stringify({ id, method, params })); });
}
const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
async function evaluate(expression, awaitPromise = false) {
  const result = await command("Runtime.evaluate", { expression, awaitPromise, returnByValue: true });
  if (result.exceptionDetails) throw new Error(result.exceptionDetails.text);
  return result.result.value;
}
async function navigate(url, wait = 900) { await command("Page.navigate", { url }); await delay(wait); }
async function screenshot(name) {
  const result = await command("Page.captureScreenshot", { format: "png", captureBeyondViewport: false });
  fs.writeFileSync(path.join(output, name), Buffer.from(result.data, "base64"));
}
async function viewport(width, height, mobile = false) { await command("Emulation.setDeviceMetricsOverride", { width, height, deviceScaleFactor: 1, mobile }); }

await command("Page.enable"); await command("Runtime.enable");
await command("Emulation.setEmulatedMedia", { features: [{ name: "prefers-reduced-motion", value: "no-preference" }] });
await viewport(1440, 1100);
await navigate(`${origin}/`); await screenshot("grade-selector-desktop.png");
await navigate(`${origin}/grade.html?grade=grade-8`); await screenshot("g8-catalogue-desktop.png");
await viewport(390, 844, true); await navigate(`${origin}/grade.html?grade=grade-8`); await screenshot("g8-catalogue-mobile.png");
await viewport(1440, 1100); await navigate(`${origin}/topic.html?grade=grade-8&topic=algebraic-equations`); await screenshot("g8-algebraic-equations-topic-desktop.png");
const topicAudit = await evaluate(`({rows:document.querySelectorAll('#lessons-list .topic-row').length,links:document.querySelectorAll('#lessons-list a.topic-row').length,disabled:document.querySelectorAll('#lessons-list [aria-disabled="true"]').length,paper:[...document.querySelectorAll('#topic-paper,#crumb-paper')].every(x=>x.hidden)})`);
if (topicAudit.rows !== 10 || topicAudit.links !== 1 || topicAudit.disabled !== 9 || !topicAudit.paper) throw new Error(`Topic audit failed: ${JSON.stringify(topicAudit)}`);
await navigate(`${origin}/lesson.html?grade=grade-8&topic=algebraic-equations&lesson=g8-algebraic-equations-01`); await screenshot("g8-algebraic-equations-01-initial.png");
const breadcrumb = await evaluate(`({title:document.querySelector('#lesson-title').textContent,topic:document.querySelector('#crumb-topic').textContent,paperHidden:document.querySelector('#lesson-paper').hidden,examples:document.querySelectorAll('.example-dots span').length})`);
if (breadcrumb.title !== "Meaning of equality" || breadcrumb.topic !== "Algebraic Equations" || !breadcrumb.paperHidden || breadcrumb.examples !== 15) throw new Error(`Lesson audit failed: ${JSON.stringify(breadcrumb)}`);

const capturedFamilies = new Set();
for (let index = 0; index < 15; index += 1) {
  await evaluate(`document.querySelector('[data-example-action="reveal"]')?.click()`); await delay(250);
  const questionId = source.worked_examples[index].id, family = source.worked_examples[index].renderer.split(":")[1];
  await evaluate(`document.querySelector('.whiteboard-question-set').scrollIntoView({block:'start'})`); await delay(80);
  if (!capturedFamilies.has(family)) {
    await screenshot(`${questionId}-${family}-initial.png`);
    await evaluate(`document.querySelector('.whiteboard-question-set [data-action="play"]').click()`); await delay(120);
    await screenshot(`${questionId}-${family}-operation.png`);
    await evaluate(`document.querySelector('.whiteboard-question-set [data-action="pause"]').click()`);
    capturedFamilies.add(family);
  }
  const finalState = await evaluate(`(()=>{const position=document.querySelector('[data-role="position"]');const total=Number(position.textContent.match(/of ([0-9]+)/)[1]);for(let i=0;i<total;i++)document.querySelector('[data-action="next"]').click();document.querySelector('[data-action="previous"]').click();document.querySelector('[data-action="next"]').click();document.querySelector('[data-action="replay"]').click();document.querySelector('[data-action="pause"]').click();return {position:position.textContent,missing:document.querySelector('.whiteboard-stage')?.dataset.missingTargets||""};})()`);
  if (finalState.missing) throw new Error(`${questionId} missing targets: ${finalState.missing}`);
  if (index === 0 || [2,7,8,10,12,14].includes(index)) await screenshot(`${questionId}-${family}-result.png`);
  if (index < 14) { await evaluate(`document.querySelector('[data-example-action="next"]').click()`); await delay(120); }
}

await evaluate(`document.querySelector('[data-example-action="practice"]').click()`); await delay(250);
await screenshot("g8-algebraic-equations-01-practice-before-submit.png");
for (const item of source.practice_questions) {
  await evaluate(`(()=>{const root=document.querySelector('.self-guided-practice'),input=root.querySelector('.practice-answer-input');input.value=${JSON.stringify(item.answer)};input.dispatchEvent(new Event('input',{bubbles:true}));root.querySelector('[data-role="answer-form"]').requestSubmit();})()`); await delay(100);
  const correct = await evaluate(`document.querySelector('.self-guided-practice .practice-feedback').classList.contains('is-correct')`);
  if (!correct) throw new Error(`${item.id} was not accepted by the server`);
  await evaluate(`document.querySelector('.self-guided-practice [data-action="next"]').click()`); await delay(80);
}
await delay(150); await evaluate(`document.querySelector('[data-action="start-mastery"]').click()`); await delay(150);
await evaluate(`(()=>{for(const input of document.querySelectorAll('[data-question-id]'))input.value='incorrect';document.querySelector('[data-role="assessment-form"]').requestSubmit();})()`); await delay(200);
await screenshot("g8-algebraic-equations-01-mastery-repair.png");
await evaluate(`document.querySelector('[data-action="complete-repair"]').click()`); await delay(200);
for (const item of source.reassessment_questions) await evaluate(`document.querySelector('[data-question-id="${item.id}"]').value=${JSON.stringify(item.answer)}`);
await evaluate(`document.querySelector('[data-role="assessment-form"]').requestSubmit()`); await delay(200);
await screenshot("g8-algebraic-equations-01-reassessment-ready.png");

const masteryPass = await evaluate(`(async()=>{const session=await (await fetch('/api/v1/practice/g8-algebraic-equations-01/sessions',{method:'POST'})).json();const response=await fetch('/api/v1/practice/g8-algebraic-equations-01/sessions/'+session.session_id+'/mastery',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({answers:${JSON.stringify(Object.fromEntries(source.mastery_questions.map(item => [item.id, item.answer])))}})});return response.json();})()`, true);
if (!masteryPass.mastered || masteryPass.questions_correct !== 5) throw new Error("Browser mastery-pass request failed");
await viewport(390, 844, true); await navigate(`${origin}/lesson.html?grade=grade-8&topic=algebraic-equations&lesson=g8-algebraic-equations-01`); await screenshot("g8-algebraic-equations-01-mobile.png");
await viewport(1440, 1100); await navigate(`${origin}/lesson.html?grade=grade-8&topic=algebraic-equations&lesson=g8-algebraic-equations-01&example=3&step=2`, 1200);
const restored = await evaluate(`({example:document.querySelector('.example-progress strong')?.textContent,state:document.querySelector('[data-role="position"]')?.textContent})`);
if (!restored.example?.includes("Example 3 of 15") || !restored.state?.startsWith("State 2 of")) throw new Error(`Direct URL restoration failed: ${JSON.stringify(restored)}`);
await screenshot("g8-algebraic-equations-01-direct-url-restored.png");
await navigate(`${origin}/grade.html?grade=grade-12`); await screenshot("grade12-regression-desktop.png");
const grade12 = await evaluate(`({p1:document.body.textContent.includes('Paper 1 topics'),p2:document.body.textContent.includes('Paper 2 topics')})`);
if (!grade12.p1 || !grade12.p2) throw new Error("Grade 12 paper grouping regressed");
console.log(JSON.stringify({ topicAudit, breadcrumb, rendererFamilies: [...capturedFamilies], masteryPass, restored, grade12, screenshots: fs.readdirSync(output).filter(name => name.endsWith('.png')).length }, null, 2));
socket.close();
