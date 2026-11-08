const assert = require('node:assert/strict');
const fs = require('node:fs');
const {rank} = require('../dist/assets/search.js');
const en = JSON.parse(fs.readFileSync('dist/assets/search-en.json'));
const fr = JSON.parse(fs.readFileSync('dist/assets/search-fr.json'));
assert.equal(rank(en, 'Canadian flags')[0].url, '/flags/canada/');
assert.ok(rank(en, 'flag rentals').some(item => item.url === '/flag-rentals/'));
assert.equal(rank(en, 'Toronto', 'Locations')[0].url, '/locations/ontario/toronto/');
assert.ok(rank(en, 'rope').some(item => item.url === '/accessories/halyard-rope/'));
assert.ok(!rank(en, 'rope').some(item => item.url === '/industries/property-management/'));
assert.ok(rank(en, 'rope', 'Accessories').every(item => item.category === 'Accessories'));
assert.deepEqual(rank(fr, 'montreal'), rank(fr, 'Montréal'));
assert.equal(rank(fr, 'montreal', 'Locations')[0].url, '/fr/locations/quebec/montreal/');
assert.ok(rank(fr, 'mats').some(item => item.url === '/fr/flagpoles/'));
assert.deepEqual(rank(en, 'zzzznomatch'), []);
assert.deepEqual(rank(en, '<script>alert(1)</script>'), []);
for (const [prefix, index] of [['', en], ['/fr', fr]]) {
  assert.equal(new Set(index.map(item => item.url)).size, index.length);
  index.forEach(item => { assert.ok(item.url.startsWith(prefix + '/')); assert.ok(fs.existsSync('dist' + item.url + 'index.html')); });
}
console.log('PASS: relevant product/service search, category filters, accents, singular/plural, no matches, safe text queries and valid bilingual result URLs.');
