/* Search only the public catalogue. No visitor data or external search service. */
(() => {
  const normalize = value => String(value).toLowerCase().normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9]+/g, ' ').trim();
  function rank(items, query, category = 'All') {
    const terms = normalize(query).split(' ').filter(Boolean);
    const contains = (text, term) => text.split(' ').some(word => word.startsWith(term) || (term.length > 3 && term.endsWith('s') && word === term.slice(0, -1)));
    return items.filter(item => category === 'All' || item.category === category)
      .map(item => {
        const title = normalize(item.title), description = normalize(item.description);
        const text = title + ' ' + description + ' ' + normalize(item.categoryLabel);
        if (!terms.every(term => contains(text, term))) return null;
        const score = terms.reduce((n, term) => n + (contains(title, term) ? 8 : 1), 0)
          + (terms.length && title.includes(normalize(query)) ? 12 : 0);
        return {item, score};
      }).filter(Boolean).sort((a, b) => b.score - a.score).map(result => result.item);
  }
  if (typeof module !== 'undefined') { module.exports = {rank}; return; }
  const input = document.querySelector('#site-search');
  if (!input) return;
  const fr = document.documentElement.lang === 'fr-CA';
  const prefix = fr ? '/fr' : '';
  const form = document.querySelector('#site-search-form');
  const results = document.querySelector('#search-results');
  const status = document.querySelector('#search-status');
  const filters = [...document.querySelectorAll('[data-category]')];
  const popular = ['/flags/canada/', '/custom-flags/', '/flag-rentals/', '/flagpole-installation/', '/flagpole-repair/', '/accessories/'];
  let items = [], ready = false, category = 'All';
  function readURL() {
    const params = new URLSearchParams(location.search);
    input.value = (params.get('q') || '').slice(0, 160);
    category = filters.some(button => button.dataset.category === params.get('category')) ? params.get('category') : 'All';
  }
  function render() {
    if (!ready) return;
    const query = input.value.trim();
    const browsing = !query && category === 'All';
    const matches = browsing ? popular.map(url => items.find(item => item.url === prefix + url)).filter(Boolean) : rank(items, query, category);
    filters.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.category === category)));
    results.replaceChildren();
    matches.forEach(item => {
      const link = document.createElement('a'); link.className = 'search-result'; link.href = item.url;
      const label = document.createElement('span'); label.className = 'eyebrow'; label.textContent = item.categoryLabel;
      const title = document.createElement('h2'); title.textContent = item.title;
      const description = document.createElement('p'); description.textContent = item.description;
      const arrow = document.createElement('span'); arrow.className = 'result-arrow'; arrow.setAttribute('aria-hidden', 'true'); arrow.textContent = '↗';
      link.append(label, title, description, arrow); results.append(link);
    });
    status.textContent = browsing ? (fr ? 'Quelques points de départ.' : 'Popular starting points.') : (fr ? `${matches.length} résultat${matches.length === 1 ? '' : 's'}.` : `${matches.length} result${matches.length === 1 ? '' : 's'}.`);
    document.querySelector('#search-empty').hidden = matches.length !== 0;
  }
  function update() {
    const params = new URLSearchParams();
    if (input.value.trim()) params.set('q', input.value.trim());
    if (category !== 'All') params.set('category', category);
    const query = params.size ? '?' + params.toString() : '';
    history.replaceState(null, '', location.pathname + query);
    document.querySelectorAll('.language-link').forEach(link => { link.search = query; });
    render();
  }
  form.addEventListener('submit', event => { event.preventDefault(); update(); });
  input.addEventListener('input', update);
  filters.forEach(button => button.addEventListener('click', () => { category = button.dataset.category; update(); }));
  window.addEventListener('popstate', () => { readURL(); render(); });
  readURL();
  fetch(`/assets/search-${fr ? 'fr' : 'en'}.json`, {cache: 'no-cache'}).then(response => {
    if (!response.ok) throw new Error('Search unavailable');
    return response.json();
  }).then(data => { items = data; ready = true; render(); }).catch(() => {
    status.textContent = '';
    document.querySelector('#search-unavailable').hidden = false;
  });
})();
