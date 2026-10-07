/* Progressive topic search: the complete directory is available without JS. */
(() => {
  const navigation = document.querySelector('.wiki-navigation');
  const wide = window.matchMedia('(min-width:961px)');
  const setNavigation = () => { if (navigation) navigation.open = wide.matches; };
  setNavigation();
  wide.addEventListener('change', setNavigation);
  const input = document.querySelector('#topic-search');
  if (!input) return;
  document.querySelector('.help-search').hidden = false;
  const rows = [...document.querySelectorAll('[data-topic]')];
  const collections = [...document.querySelectorAll('.help-collection')];
  const status = document.querySelector('#search-status');
  input.addEventListener('input', () => {
    const words = input.value.toLocaleLowerCase().trim().split(/\s+/).filter(Boolean);
    let count = 0;
    rows.forEach(row => {
      row.hidden = !words.every(word => row.dataset.topic.toLocaleLowerCase().includes(word));
      if (!row.hidden) count++;
    });
    collections.forEach(group => { group.hidden = ![...group.querySelectorAll('[data-topic]')].some(row => !row.hidden); });
    status.textContent = words.length ? `${count} ${count === 1 ? 'guide' : 'guides'} found.${count ? '' : ' Try a shorter term, or clear the search to browse all topics.'}` : '';
  });
})();
/* Keep historical deep links useful, including when JavaScript is disabled. */
(() => {
  const followFragment = () => {
    const id = decodeURIComponent(location.hash.slice(1));
    if (!id) return;
    const target = document.getElementById(id);
    if (target?.dataset.article) location.replace(target.dataset.article);
    else if (target) {
      const details = target.closest('details');
      if (details) { details.open = true; target.scrollIntoView(); }
    }
  };
  followFragment();
  addEventListener('hashchange', followFragment);
})();
