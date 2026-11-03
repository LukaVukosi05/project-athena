const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname, '../js/pages/topic-diagnostic.js'), 'utf8');
const escapeHtml = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

test('topic check is shown only after requested, conceals answers and routes a weak lesson', async () => {
  const storage = new Map(), listeners = {};
  const button = {disabled: true, textContent: ''};
  const summary = {innerHTML: ''};
  const panel = {hidden: true, innerHTML: '', scrollIntoView() {}, querySelector(selector) {
    if (selector === 'form') return {addEventListener: (_, callback) => {listeners.submit = callback;}};
    if (selector === '.topic-diagnostic__error') return {hidden: false, textContent: ''};
    if (selector === '#topic-diagnostic-retry') return {textContent: '', onclick: null};
  }};
  const elements = {'topic-diagnostic-button': button, 'topic-diagnostic': panel, 'topic-weaknesses': summary};
  let calls = 0;
  const context = {escapeHtml, document: {getElementById: id => elements[id]}, localStorage: {
    getItem: k => storage.get(k) || null, setItem: (k, v) => storage.set(k, v)},
    fetch: async (_url, init) => {
      calls++;
      return {ok:true, json: async () => init ? {score:16,total:18, note:'Revise',
        areas:[{lesson_id:'g8-functions-relationships-02',title:'Equivalent forms',correct:1,total:3,needs_review:true}],
        review: Array.from({length:18},(_,i)=>({correct:i<16,answer:'7',explanation:'Check the rule.'}))}
        : {questions:Array.from({length:18},(_,i)=>({id:`fr-t0${i+1}`,prompt:`Question ${i+1}`}))}};
    }};
  vm.runInNewContext(source + '\nthis.diagnostic = AthenaTopicDiagnostic;', context);
  context.diagnostic.init('functions-relationships');
  assert.equal(button.disabled, false);
  assert.equal(calls, 0);
  await button.onclick();
  assert.equal(calls, 1);
  assert.equal(panel.hidden, false);
  assert.equal((panel.innerHTML.match(/<input /g)||[]).length, 18);
  assert.match(panel.innerHTML,/Submit 18 answers/);
  assert.doesNotMatch(panel.innerHTML,/all twelve|all nine/);
  assert.doesNotMatch(panel.innerHTML,/Answer: 7/);
  const form = {querySelector:()=>({disabled:false}), elements:{namedItem:()=>({value:'7'})}};
  await listeners.submit({preventDefault(){},currentTarget:form});
  assert.match(summary.innerHTML,/functions-relationships-02/);
  assert.match(panel.innerHTML,/Worked review/);
  assert.equal(calls, 2);
  assert.equal(JSON.parse(storage.values().next().value).score, 16);
  assert.doesNotMatch(storage.values().next().value,/Check the rule/);
});

test('each topic uses its own endpoint, storage key and lesson route', async () => {
  const button = {disabled: true}, panel = {hidden: true, innerHTML: '', scrollIntoView() {}, querySelector: () => ({addEventListener(){}})};
  const summary = {innerHTML: ''};
  let request;
  const context = {escapeHtml, document:{getElementById: id => ({'topic-diagnostic-button':button,'topic-diagnostic':panel,'topic-weaknesses':summary}[id])},
    localStorage:{getItem:()=>null},fetch:async url => {request=url; return {ok:true,json:async()=>({questions:[{id:'line-1',prompt:'Find x'}]})};}};
  vm.runInNewContext(source+'\nthis.diagnostic = AthenaTopicDiagnostic;',context);
  context.diagnostic.init('geometry-of-straight-lines');
  await button.onclick();
  assert.equal(request,'/api/v1/practice/topics/grade-8/geometry-of-straight-lines/diagnostic');
  assert.match(panel.innerHTML,/Submit 1 answers/);
});
