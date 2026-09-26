/* Site command palette. Progressive enhancement — navigation works without JS. */
(() => {
  const INDEX_URL = '/ingest/assets/search-index.json';
  const DOWNLOAD = 'https://github.com/brianrenshaw/brianrenshaw-app-site/releases/download/ingest-v0.9.3/Ingest-0.9.3.dmg';

  const isMac = /Mac|iPhone|iPad|iPod/.test(navigator.platform || '') || (navigator.userAgentData && navigator.userAgentData.platform === 'macOS');
  const modLabel = isMac ? '⌘' : 'Ctrl';

  let index = [];
  let active = 0;
  let open = false;
  let loaded = false;

  const root = document.createElement('div');
  root.className = 'ingest-palette';
  root.hidden = true;
  root.innerHTML = `
    <div class="ingest-palette-backdrop" data-close></div>
    <div class="ingest-palette-dialog" role="dialog" aria-modal="true" aria-label="Search Ingest">
      <div class="ingest-palette-input-row">
        <input type="search" class="ingest-palette-input" placeholder="Search pages and sections…" autocomplete="off" spellcheck="false" aria-controls="ingest-palette-list" aria-autocomplete="list">
        <kbd class="ingest-palette-esc">esc</kbd>
      </div>
      <ul class="ingest-palette-list" id="ingest-palette-list" role="listbox"></ul>
      <p class="ingest-palette-empty" hidden>No matches.</p>
      <p class="ingest-palette-footer"><span>↑↓ to move</span><span>↩ to open</span><span>${modLabel}K anytime</span></p>
    </div>`;
  document.body.appendChild(root);

  const input = root.querySelector('.ingest-palette-input');
  const list = root.querySelector('.ingest-palette-list');
  const empty = root.querySelector('.ingest-palette-empty');
  let lastFocus = null;

  const score = (item, q) => {
    if (!q) return item.type === 'page' ? 2 : 1;
    const hay = `${item.title} ${item.keywords || ''} ${item.hint || ''} ${item.page || ''}`.toLowerCase();
    const parts = q.toLowerCase().split(/\s+/).filter(Boolean);
    if (!parts.every(p => hay.includes(p))) return -1;
    let s = 0;
    if (item.title.toLowerCase().startsWith(parts[0])) s += 8;
    if (item.type === 'page') s += 3;
    if ((item.url || '').includes(location.pathname) && location.pathname !== '/ingest/') s += 2;
    s += Math.max(0, 6 - Math.min(item.title.length / 12, 6));
    return s;
  };

  const filter = (q) => {
    const scored = index.map(item => ({ item, s: score(item, q) })).filter(x => x.s >= 0);
    scored.sort((a, b) => b.s - a.s || a.item.title.localeCompare(b.item.title));
    return scored.slice(0, 12).map(x => x.item);
  };

  const render = (items) => {
    list.innerHTML = '';
    empty.hidden = items.length > 0;
    items.forEach((item, i) => {
      const li = document.createElement('li');
      li.setAttribute('role', 'option');
      li.id = `ingest-palette-opt-${i}`;
      li.className = 'ingest-palette-option' + (i === active ? ' is-active' : '');
      li.setAttribute('aria-selected', String(i === active));
      const hint = item.hint || item.page || (item.type === 'page' ? 'Page' : 'Section');
      li.innerHTML = `<span class="ingest-palette-title">${escapeHtml(item.title)}</span><span class="ingest-palette-hint">${escapeHtml(hint)}</span>`;
      li.addEventListener('mouseenter', () => { active = i; paint(); });
      li.addEventListener('click', () => go(item));
      list.appendChild(li);
    });
    input.setAttribute('aria-activedescendant', items.length ? `ingest-palette-opt-${active}` : '');
  };

  const paint = () => {
    [...list.children].forEach((li, i) => {
      li.classList.toggle('is-active', i === active);
      li.setAttribute('aria-selected', String(i === active));
    });
    const cur = list.children[active];
    if (cur) cur.scrollIntoView({ block: 'nearest' });
    input.setAttribute('aria-activedescendant', list.children.length ? `ingest-palette-opt-${active}` : '');
  };

  const escapeHtml = (s) => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

  const currentItems = () => filter(input.value.trim());

  const go = (item) => {
    close();
    if (!item) return;
    if (item.url === DOWNLOAD || item.action === 'download') {
      location.href = DOWNLOAD;
      return;
    }
    const url = new URL(item.url, location.origin);
    if (url.pathname === location.pathname && url.hash) {
      const el = document.getElementById(url.hash.slice(1));
      if (el) {
        history.pushState(null, '', url.hash);
        el.scrollIntoView({ behavior: 'smooth', block: 'start' });
        return;
      }
    }
    location.href = item.url;
  };

  const openPalette = async () => {
    if (open) return;
    if (!loaded) {
      try {
        const res = await fetch(INDEX_URL, { credentials: 'same-origin' });
        index = await res.json();
        index.push({ type: 'page', title: 'Download Ingest', url: DOWNLOAD, keywords: 'download dmg install', hint: 'Download', action: 'download' });
        loaded = true;
      } catch (e) {
        index = [
          { type: 'page', title: 'Home', url: '/ingest/', hint: 'Page' },
          { type: 'page', title: 'Getting started', url: '/ingest/getting-started/', hint: 'Page' },
          { type: 'page', title: 'Guide', url: '/ingest/guide/', hint: 'Page' },
          { type: 'page', title: 'Shortcuts', url: '/ingest/shortcuts/', hint: 'Page' },
          { type: 'page', title: 'Support', url: '/ingest/support/', hint: 'Page' },
          { type: 'page', title: 'Download Ingest', url: DOWNLOAD, hint: 'Download', action: 'download' }
        ];
        loaded = true;
      }
      // Merge live headings on this page so brand-new anchors still appear.
      document.querySelectorAll('main h2[id], main h3[id], main section.guide-section[id], main section[id][aria-labelledby]').forEach(el => {
        let title = '';
        let id = el.id;
        if (el.matches('section[aria-labelledby]')) {
          const h = document.getElementById(el.getAttribute('aria-labelledby'));
          title = h ? h.innerText.replace(/\s+/g, ' ').trim() : el.id;
        } else if (el.matches('section.guide-section')) {
          const h = el.querySelector('h2');
          title = h ? h.innerText.replace(/\s+/g, ' ').trim() : el.id;
        } else {
          title = el.innerText.replace(/\s+/g, ' ').trim();
        }
        if (!title || !id) return;
        const url = `${location.pathname}#${id}`;
        if (!index.some(x => x.url === url)) {
          index.push({ type: 'section', title, url, keywords: title.toLowerCase(), hint: 'On this page', page: 'On this page' });
        }
      });
    }
    lastFocus = document.activeElement;
    open = true;
    root.hidden = false;
    document.documentElement.classList.add('ingest-palette-open');
    input.value = '';
    active = 0;
    render(currentItems());
    requestAnimationFrame(() => input.focus());
  };

  const close = () => {
    if (!open) return;
    open = false;
    root.hidden = true;
    document.documentElement.classList.remove('ingest-palette-open');
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  };

  input.addEventListener('input', () => { active = 0; render(currentItems()); });
  input.addEventListener('keydown', (event) => {
    const items = currentItems();
    if (event.key === 'ArrowDown') { event.preventDefault(); active = Math.min(active + 1, Math.max(items.length - 1, 0)); paint(); }
    if (event.key === 'ArrowUp') { event.preventDefault(); active = Math.max(active - 1, 0); paint(); }
    if (event.key === 'Home') { event.preventDefault(); active = 0; paint(); }
    if (event.key === 'End') { event.preventDefault(); active = Math.max(items.length - 1, 0); paint(); }
    if (event.key === 'Enter') { event.preventDefault(); go(items[active]); }
    if (event.key === 'Escape') { event.preventDefault(); close(); }
  });
  root.addEventListener('click', (event) => { if (event.target.closest('[data-close]')) close(); });

  document.addEventListener('keydown', (event) => {
    const meta = event.metaKey || event.ctrlKey;
    if (meta && event.key.toLowerCase() === 'k') {
      const tag = (event.target && event.target.tagName) || '';
      if (!open && (tag === 'INPUT' || tag === 'TEXTAREA' || event.target.isContentEditable)) return;
      event.preventDefault();
      if (open) close(); else openPalette();
    }
    if (event.key === 'Escape' && open) { event.preventDefault(); close(); }
  });

  document.querySelectorAll('[data-ingest-palette]').forEach(btn => {
    btn.addEventListener('click', (event) => {
      event.preventDefault();
      openPalette();
    });
  });

  // Expose for debugging without polluting globals heavily
  window.__ingestOpenPalette = openPalette;
})();
