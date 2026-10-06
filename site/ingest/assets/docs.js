/* Progressive help navigation; ordinary article links need no script. */
(() => {
  const navigation = document.querySelector('.wiki-navigation');
  if (navigation) {
    const compact = matchMedia('(max-width: 960px)');
    const fit = () => { navigation.open = !compact.matches; };
    fit();
    compact.addEventListener('change', fit);
  }
  // Keep links shipped in app Help menus, search engines and bookmarks useful.
  const followLegacyAnchor = () => {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    if (!id) return;
    const entry = document.getElementById(id);
    if (entry?.dataset.article) location.replace(entry.dataset.article);
  };
  followLegacyAnchor();
  addEventListener('hashchange', followLegacyAnchor);
})();

(() => {
  const topics = document.querySelector('.wiki-page-sections');
  if (!topics) return;
  const narrow = matchMedia('(max-width: 1200px)');
  const fit = () => { topics.open = !narrow.matches; };
  fit();
  narrow.addEventListener('change', fit);
  topics.querySelector('summary').addEventListener('click', event => {
    if (!narrow.matches) event.preventDefault();
  });
  const links = [...topics.querySelectorAll('a[href^="#"]')];
  links.forEach(link => link.addEventListener('click', () => {
    if (narrow.matches) topics.open = false;
  }));
  if (!('IntersectionObserver' in window)) return;
  const observer = new IntersectionObserver(entries => {
    const visible = entries.filter(entry => entry.isIntersecting);
    if (!visible.length) return;
    const id = visible[0].target.id;
    links.forEach(link => {
      if (link.hash === '#' + id) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  }, {rootMargin: '-5% 0px -65% 0px'});
  links.forEach(link => {
    const heading = document.getElementById(link.hash.slice(1));
    if (heading) observer.observe(heading);
  });
})();
