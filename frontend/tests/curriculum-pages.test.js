const assert = require("assert");
const fs = require("fs");
const vm = require("vm");
const path = require("path");

const elements = new Map();
function element(id) {
  if (!elements.has(id)) elements.set(id, { id, innerHTML: "", textContent: "", style: {}, href: "" });
  return elements.get(id);
}

let ready;
const topics = [
  { id: "sequences-series", title: "Sequences and Series", product_order: 1, paper: "Paper 1", subtopic_count: 1 },
  { id: "functions-graphs", title: "Functions and Graphs", product_order: 2, paper: "Paper 1", subtopic_count: 1, status: "teacher_review_required" },
];
const context = {
  document: { addEventListener: (_name, callback) => { ready = callback; }, getElementById: element },
  AthenaAuth: { requireSession: async () => ({ id: 1 }) },
  AthenaState: { get: () => ({ user: { firstName: "Test" }, completedLessons: [], isPremium: false }), accessToken: () => null },
  renderNav: () => {},
  fetch: async () => ({ ok: true, json: async () => ({ topics }) }),
  console,
  Date,
  encodeURIComponent,
};
vm.createContext(context);
vm.runInContext(fs.readFileSync(path.join(__dirname, "../js/pages/dashboard.js"), "utf8"), context);

(async () => {
  await ready();
  const html = element("topics-list").innerHTML;
  assert(html.includes("Sequences and Series"));
  assert(html.includes("Functions and Graphs"));
  assert(html.includes("topic=functions-graphs"));
  assert(html.includes('topic-row__index">1'));
  assert(html.includes('topic-row__index">2'));

  elements.clear();
  context.fetch = async () => ({ ok: false, status: 503 });
  await ready();
  const error = element("topics-list").innerHTML;
  assert(error.toLowerCase().includes("curriculum could not be loaded"));
  assert(error.includes("Status: 503"));
  assert(!error.includes("Sequences and Series"));
  console.log("backend-authoritative curriculum page flow passed");
})().catch(error => { console.error(error); process.exitCode = 1; });
