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
