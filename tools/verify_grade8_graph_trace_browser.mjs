import { spawn } from 'node:child_process';
import { mkdirSync, writeFileSync } from 'node:fs';
import path from 'node:path';

const base = process.env.ATHENA_URL || 'http://127.0.0.1:8037';
const chromePath = process.env.CHROME_PATH || 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const output = path.resolve('artifacts/grade8-graphs/trace-check');
mkdirSync(output, { recursive: true });
const port = 9248;
const chrome = spawn(chromePath, ['--headless=new', `--remote-debugging-port=${port}`,
  `--user-data-dir=${path.join(output, 'chrome-profile')}`, '--window-size=1400,1000',
  '--disable-gpu', '--no-first-run'], { stdio: 'ignore' });
const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
async function poll(url) {
  for (let i = 0; i < 100; i++) {
    try { const response = await fetch(url); if (response.ok) return response.json(); } catch {}
    await delay(100);
  }
  throw new Error(`Chrome did not start at ${url}; check CHROME_PATH`);
}
class CDP {
  constructor(url) {
    this.socket = new WebSocket(url); this.next = 1; this.pending = new Map();
    this.socket.onmessage = event => {
      const message = JSON.parse(event.data);
      if (!message.id) return;
      const task = this.pending.get(message.id); this.pending.delete(message.id);
      message.error ? task.reject(new Error(message.error.message)) : task.resolve(message.result);
    };
  }
  ready() { return new Promise((resolve, reject) => { this.socket.onopen = resolve; this.socket.onerror = reject; }); }
  send(method, params = {}) {
    const id = this.next++;
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject }); this.socket.send(JSON.stringify({ id, method, params }));
    });
  }
}
let cdp;
try {
  await poll(`http://127.0.0.1:${port}/json/version`);
  const target = await fetch(`http://127.0.0.1:${port}/json/new?${encodeURIComponent(base)}`, { method: 'PUT' }).then(r => r.json());
  cdp = new CDP(target.webSocketDebuggerUrl); await cdp.ready();
  await cdp.send('Page.enable'); await cdp.send('Runtime.enable');
  const evaluate = async expression => {
    const result = await cdp.send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });
    if (result.exceptionDetails) throw new Error(result.exceptionDetails.exception?.description || result.exceptionDetails.text);
    return result.result.value;
  };
  const waitFor = async expression => {
    for (let i = 0; i < 120; i++) { if (await evaluate(expression)) return; await delay(100); }
    throw new Error(`Page did not become ready: ${expression}`);
  };
  const state = () => evaluate(`(()=>{const stage=document.querySelector('.whiteboard-stage'),svg=stage?.querySelector('.grade8-coordinate-plane'),trace=stage?.querySelector('.g8-completed-steps'),graphBox=svg?.getBoundingClientRect(),traceBox=trace?.getBoundingClientRect();return {layout:stage?.dataset.layout,svgWidth:graphBox?.width||0,traceBesideGraph:Boolean(traceBox&&graphBox&&traceBox.left>=graphBox.right-3),points:svg?.querySelectorAll('.coord-result').length||0,guides:svg?.querySelectorAll('.coord-guide').length||0,lines:svg?.querySelectorAll('.coord-graph-line').length||0,steps:trace?.querySelectorAll('li').length||0,trace:trace?.innerText||'',overflow:document.documentElement.scrollWidth-document.documentElement.clientWidth,primary:document.querySelector('[data-action="primary"]')?.textContent,status:document.querySelector('.stateful-whiteboard')?.dataset.controllerState};})()`);
  const click = selector => evaluate(`(()=>{const button=document.querySelector(${JSON.stringify(selector)});if(!button)throw Error('Missing ${selector}');button.click();return true;})()`);
  const screenshot = async name => writeFileSync(path.join(output, name), Buffer.from((await cdp.send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false })).data, 'base64'));
  const results = [];
  for (const { lesson, example } of [
    { lesson: 'g8-graphs-01', example: 1 },
    { lesson: 'g8-graphs-01', example: 6 },
    { lesson: 'g8-graphs-02', example: 1 },
  ]) {
    await cdp.send('Emulation.setDeviceMetricsOverride', { width: 1400, height: 1000, deviceScaleFactor: 1, mobile: false });
    await cdp.send('Page.navigate', { url: `${base}/lesson.html?grade=grade-8&topic=graphs&lesson=${lesson}&example=${example}` });
    await waitFor('document.querySelector(".grade8-coordinate-plane") && !document.querySelector("[data-action=primary]")?.disabled');
    await click('[data-action="reduced-motion"]');
    let current = await state();
    if (current.layout !== 'graph' || current.svgWidth < 480 || !current.traceBesideGraph || current.points !== 0 || current.steps !== 0 || current.overflow > 1)
      throw new Error(`${lesson}: initial graph not prominent and empty: ${JSON.stringify(current)}`);
    await screenshot(`${lesson}-example-${example}-initial.png`);
    const lessonData = await fetch(`${base}/api/v1/lessons/${lesson}`).then(r => r.json());
    const questionId = lessonData.whiteboard_questions?.[example - 1]?.id;
    if (!questionId) throw new Error(`${lesson}: first question unavailable`);
    const reveal = await fetch(`${base}/api/v1/lessons/${lesson}/questions/${questionId}/reveal`, { method: 'POST' });
    if (!reveal.ok) throw new Error(`${lesson}: reveal API returned ${reveal.status}`);
    const full = await reveal.json(), steps = full.whiteboard.steps;
    for (let index = 0; index < steps.length; index++) {
      await click('[data-action="primary"]');
      current = await state();
      const expectedPoints = lesson === 'g8-graphs-02' ? Math.min(index + 1, 3) : index === 3 ? 1 : 0;
      const expectedGuides = lesson === 'g8-graphs-02' ? Math.min(index + 1, 3) * 2 : Math.min(Math.max(index, 0), 2);
      if (current.steps !== index + 1 || current.layout !== 'graph' || current.svgWidth < 480 || !current.traceBesideGraph || current.overflow > 1
        || current.points !== expectedPoints || current.guides !== expectedGuides)
        throw new Error(`${lesson}: stage ${index + 1} regression: ${JSON.stringify(current)}`);
      if (index === 1 || index === 2) await screenshot(`${lesson}-example-${example}-step-${index + 1}.png`);
      if (index < steps.length - 1 && current.status !== 'step_complete')
        throw new Error(`${lesson}: step ${index + 1} not complete: ${JSON.stringify(current)}`);
    }
    if (current.points < 1 || current.status !== 'example_complete' || (lesson === 'g8-graphs-02' && current.lines !== 1))
      throw new Error(`${lesson}: final point missing: ${JSON.stringify(current)}`);
    await screenshot(`${lesson}-example-${example}-result.png`);
    results.push({ lesson, example, steps: steps.length, plottedPoints: current.points, graphWidth: current.svgWidth });
  }
  console.log(JSON.stringify({ results, screenshots: output }, null, 2));
} finally {
  cdp?.socket.close(); chrome.kill();
}
