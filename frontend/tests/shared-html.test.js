const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const {test} = require('node:test');
const root = path.join(__dirname, '..');
const context = vm.createContext({});
vm.runInContext(fs.readFileSync(path.join(root, 'js/engine/html.js'), 'utf8'), context);

test('shared escaping protects text and quoted attributes while preserving maths', () => {
  assert.equal(context.escapeHtml('<img src=x onerror="bad()"> & \'x\''), '&lt;img src=x onerror=&quot;bad()&quot;&gt; &amp; &#39;x&#39;');
  assert.equal(context.escapeHtml('x² − 3π = ½'), 'x² − 3π = ½');
  assert.equal(context.escapeHtml(null), 'null');
  assert.equal(context.escapeHtml(42), '42');
});

test('every application page loads escaping before its consumers', () => {
  for (const file of fs.readdirSync(root).filter(name => name.endsWith('.html'))) {
    const html = fs.readFileSync(path.join(root, file), 'utf8');
    const scripts = [...html.matchAll(/<script\b[^>]*\bsrc="([^"?]+)(?:\?[^" ]*)?"/g)].map(match => match[1]);
    for (const src of scripts.filter(src => src.startsWith('js/'))) {
      assert.ok(fs.existsSync(path.join(root, src)), `${file}: missing ${src}`);
      if (/\bescapeHtml\(/.test(fs.readFileSync(path.join(root, src), 'utf8')) && src !== 'js/engine/html.js') {
        assert.ok(scripts.indexOf('js/engine/html.js') >= 0 && scripts.indexOf('js/engine/html.js') < scripts.indexOf(src), `${file}: escaping must load before ${src}`);
      }
    }
  }
});
