const assert = require('assert'), fs = require('fs'), vm = require('vm');
const source = fs.readFileSync(__dirname + '/../js/pages/landing.js', 'utf8');
async function landing(user, membership, fails = false) {
  const nodes = new Map();
  const node = id => {
    if (!nodes.has(id)) nodes.set(id, {textContent: 'Start my 14-day free trial', href: 'login.html?next=%2Fcheckout.html'});
    return nodes.get(id);
  };
  let ready, requests = 0;
  vm.runInNewContext(source, {
    document: {addEventListener: (_, fn) => ready = fn, getElementById: node},
    AthenaAuth: {restoreSession: async () => user, request: async () => {requests++; if (fails) throw Error('offline'); return membership;}},
    renderNav() {}, encodeURIComponent,
    fetch() {throw Error('The landing page must not fetch the removed curriculum catalogue');}
  });
  await ready();
  return {node, requests};
}
(async () => {
  const guest = await landing(null);
  assert.equal(guest.requests, 0);
  const active = await landing({grade: 'grade-9'}, {has_access: true});
  assert.equal(active.node('landing-primary-cta').textContent, 'Continue learning');
  assert.equal(active.node('landing-primary-cta').href, 'grade.html?grade=grade-9');
  assert.equal(active.node('landing-account-link').href, 'account.html');
  const unpaid = await landing({grade: 'grade-11'}, {has_access: false});
  assert.equal(unpaid.node('landing-primary-cta').href, 'checkout.html');
  const offline = await landing({grade: 'grade-8'}, null, true);
  assert.equal(offline.node('landing-account-link').href, 'account.html');
  assert.equal(offline.node('landing-primary-cta').href, 'login.html?next=%2Fcheckout.html');
  console.log('Landing retains member routing without the removed catalogue or offer');
})().catch(error => {console.error(error); process.exitCode = 1;});
