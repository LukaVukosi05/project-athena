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
      return {ok:true, json: async () => init ? {score:7,total:9, note:'Revise',
        areas:[{lesson_id:'g8-functions-relationships-02',title:'Equivalent forms',correct:1,total:3,needs_review:true}],
        review: Array.from({length:9},(_,i)=>({correct:i<7,answer:'7',explanation:'Check the rule.'}))}
        : {questions:Array.from({length:9},(_,i)=>({id:`fr-t0${i+1}`,prompt:`Question ${i+1}`}))}};
    }};
  vm.runInNewContext(source + '\nthis.diagnostic = AthenaTopicDiagnostic;', context);
  context.diagnostic.init();
  assert.equal(button.disabled, false);
  assert.equal(calls, 0);
  await button.onclick();
  assert.equal(calls, 1);
  assert.equal(panel.hidden, false);
  assert.equal((panel.innerHTML.match(/<input /g)||[]).length, 9);
  assert.doesNotMatch(panel.innerHTML,/Answer: 7/);
  const form = {querySelector:()=>({disabled:false}), elements:{namedItem:()=>({value:'7'})}};
  await listeners.submit({preventDefault(){},currentTarget:form});
  assert.match(summary.innerHTML,/functions-relationships-02/);
  assert.match(panel.innerHTML,/Worked review/);
  assert.equal(calls, 2);
  assert.equal(JSON.parse(storage.values().next().value).score, 7);
  assert.doesNotMatch(storage.values().next().value,/Check the rule/);
});
