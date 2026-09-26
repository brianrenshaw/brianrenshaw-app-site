/* Interactive demos for Metadata Assist (;) and rename tokens ({…}). Progressive enhancement.
   Map Location / Find place is not demoed here — it uses Apple Maps search in the app. */
(() => {
  const FIELDS_URL = '/ingest/assets/metadata-fields.json';
  const SAMPLE = {
    yyyy: '2026', yy: '26', mm: '09', dd: '25',
    hh: '16', mn: '07', seqn: '0042', seq: '42',
    base: 'DSC01206', ext: 'JPG', filename: 'DSC01206.JPG',
    client: 'Northside', event: 'Wedding', location: 'Louisville',
    city: 'Louisville', address: 'Main Street', shootdate: '2026-09-25',
    model: 'EOS R5', lens: 'RF 50mm', iso: '400', aperture: 'f/2',
    shutter: '1/500', folder: 'Card'
  };

  let catalog = null;

  const loadCatalog = async () => {
    if (catalog) return catalog;
    try {
      catalog = await (await fetch(FIELDS_URL, { credentials: 'same-origin' })).json();
    } catch (e) {
      catalog = {
        shootDetails: [
          { id: 'input.client', label: 'Client', aliases: [], detail: 'Shoot detail' },
          { id: 'input.event', label: 'Event', aliases: [], detail: 'Shoot detail' },
          { id: 'input.location', label: 'Location', aliases: [], detail: 'Shoot detail' },
          { id: 'input.shootDate', label: 'Shoot date', aliases: [], detail: 'Shoot detail' }
        ],
        fields: [
          { id: 'locationsShown', label: 'IPTC Place Shown', aliases: ['location', 'loc'], detail: 'Metadata field' },
          { id: 'description', label: 'Caption', aliases: ['caption'], detail: 'Metadata field' },
          { id: 'keywords', label: 'Keywords', aliases: ['kw'], detail: 'Metadata field' }
        ]
      };
    }
    return catalog;
  };

  const expandTemplate = (template) => template.replace(/\{([^}]+)\}/g, (full, key) => {
    const k = key.trim();
    if (Object.prototype.hasOwnProperty.call(SAMPLE, k)) return SAMPLE[k];
    if (k.startsWith('date:')) return 'Sep 25, 2026';
    if (k.includes(':')) {
      const [name] = k.split(':');
      if (Object.prototype.hasOwnProperty.call(SAMPLE, name)) return SAMPLE[name];
    }
    return full;
  });

  const matchItem = (item, q) => {
    if (!q) return true;
    const hay = `${item.label} ${item.id} ${(item.aliases || []).join(' ')} ${item.detail || ''}`.toLowerCase();
    return q.split(/\s+/).every(p => hay.includes(p));
  };

  const suggestionsFor = (cat, rawQuery) => {
    const q = (rawQuery || '').toLowerCase().trim();
    const out = [];
    (cat.shootDetails || []).filter(s => matchItem(s, q)).forEach(s => out.push(s));
    (cat.fields || []).filter(f => matchItem(f, q)).forEach(f => out.push(f));
    const seen = new Set();
    return out.filter(i => (seen.has(i.id) ? false : (seen.add(i.id), true))).slice(0, 14);
  };

  const escapeHtml = (s) => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

  document.querySelectorAll('[data-typing-demo="metadata"]').forEach(async (root) => {
    const cat = await loadCatalog();
    const input = root.querySelector('[data-demo-input]');
    const menu = root.querySelector('[data-demo-menu]');
    const review = root.querySelector('[data-demo-review]');
    const reviewList = root.querySelector('[data-demo-review-list]');
    const empty = root.querySelector('[data-demo-empty]');
    const hint = root.querySelector('[data-demo-hint]');
    if (!input || !menu || !review || !reviewList) return;

    let active = 0;
    let matches = [];
    let pending = null;

    const setHint = (text) => { if (hint) hint.textContent = text; };
    const syncEmpty = () => {
      const has = reviewList.children.length > 0;
      if (empty) empty.hidden = has;
      review.classList.toggle('has-rows', has);
    };

    const paintMenu = () => {
      menu.innerHTML = '';
      if (!matches.length) { menu.hidden = true; return; }
      menu.hidden = false;
      matches.forEach((item, i) => {
        const li = document.createElement('li');
        li.className = 'typing-demo-option' + (i === active ? ' is-active' : '');
        li.innerHTML = `<span class="typing-demo-option-title">${escapeHtml(item.label)}</span><span class="typing-demo-option-detail">${escapeHtml(item.detail || '')}</span>`;
        li.addEventListener('mousedown', (e) => { e.preventDefault(); choose(item); });
        menu.appendChild(li);
      });
    };

    const upsertRow = (key, label, valueHtml, note) => {
      let row = reviewList.querySelector(`[data-key="${CSS.escape(key)}"]`);
      if (!row) {
        row = document.createElement('div');
        row.className = 'typing-demo-review-row';
        row.dataset.key = key;
        reviewList.appendChild(row);
      }
      row.innerHTML = `<div><strong>${escapeHtml(label)}</strong>${note ? `<span class="typing-demo-note">${escapeHtml(note)}</span>` : ''}</div><div class="typing-demo-value">${valueHtml}</div>`;
      syncEmpty();
    };

    const choose = (item) => {
      menu.hidden = true;
      matches = [];
      pending = item;
      input.value = '';
      input.placeholder = `${item.label}…`;
      setHint(`Type a value for ${item.label}, then Return. Review appears on the right — nothing writes until you confirm in the app.`);
      input.focus();
    };

    input.addEventListener('input', () => {
      const v = input.value;
      if (pending) return;
      if (v.startsWith(';')) {
        matches = suggestionsFor(cat, v.slice(1));
        active = 0;
        paintMenu();
        setHint(matches.length ? '↑↓ to move, Tab or Return to take the field.' : 'No matching fields.');
      } else {
        matches = [];
        menu.hidden = true;
        if (!v) setHint('Type ; to find metadata fields. Same habit as Metadata Assist.');
      }
    });

    input.addEventListener('keydown', (e) => {
      if (!pending && input.value.startsWith(';') && matches.length) {
        if (e.key === 'ArrowDown') { e.preventDefault(); active = Math.min(active + 1, matches.length - 1); paintMenu(); }
        if (e.key === 'ArrowUp') { e.preventDefault(); active = Math.max(active - 1, 0); paintMenu(); }
        if (e.key === 'Tab' || e.key === 'Enter') { e.preventDefault(); choose(matches[active]); }
        if (e.key === 'Escape') {
          e.preventDefault();
          input.value = ''; matches = []; menu.hidden = true;
          setHint('Type ; to find metadata fields. Same habit as Metadata Assist.');
        }
        return;
      }
      if (pending && e.key === 'Enter') {
        e.preventDefault();
        const value = input.value.trim() || '(example value)';
        upsertRow(pending.id, pending.label, escapeHtml(value), pending.detail || '');
        pending = null;
        input.value = '';
        input.placeholder = 'Type ; for another field…';
        setHint('Review panel updated. In Ingest, nothing is saved until you confirm.');
        return;
      }
      if (pending && e.key === 'Escape') {
        e.preventDefault();
        pending = null; input.value = ''; input.placeholder = 'Type ; for a field…';
        setHint('Type ; to find metadata fields. Same habit as Metadata Assist.');
      }
    });

    syncEmpty();
  });

  document.querySelectorAll('[data-typing-demo="rename"]').forEach(root => {
    const input = root.querySelector('[data-demo-input]');
    const out = root.querySelector('[data-demo-output]');
    const hint = root.querySelector('[data-demo-hint]');
    if (!input || !out) return;
    const render = () => {
      const tpl = input.value || '';
      out.textContent = expandTemplate(tpl) || 'Filename preview';
      if (hint) {
        hint.textContent = tpl.includes('{')
          ? 'Curly braces fill variables. Semicolon is a different habit — it finds metadata fields.'
          : 'Try {yyyy}{mm}{dd}-{seqn} or Wedding-{client}-{seqn}.';
      }
    };
    input.addEventListener('input', render);
    render();
  });
})();
