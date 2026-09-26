/* Interactive demos for Metadata Assist (;) and rename tokens ({…}). Progressive enhancement. */
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
        mapLocation: { id: 'map.location', label: 'Map Location (GPS)', aliases: ['gps', 'map'], detail: 'Map pin' },
        shootDetails: [
          { id: 'input.client', label: 'Client', aliases: [], detail: 'Shoot detail' },
          { id: 'input.event', label: 'Event', aliases: [], detail: 'Shoot detail' },
          { id: 'input.location', label: 'Location', aliases: [], detail: 'Shoot detail' },
          { id: 'input.shootDate', label: 'Shoot Date', aliases: [], detail: 'Shoot detail' }
        ],
        fields: [
          { id: 'locationsShown', label: 'IPTC Place Shown', aliases: ['location', 'loc'], detail: 'Metadata field' },
          { id: 'description', label: 'Caption', aliases: ['caption'], detail: 'Metadata field' },
          { id: 'keywords', label: 'Keywords', aliases: ['kw'], detail: 'Metadata field' }
        ],
        samplePlaces: [
          { name: 'Louisville, Kentucky', subtitle: 'United States', lat: 38.2527, lon: -85.7585 }
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
    const mapQ = !q || ['map', 'gps', 'place', 'pin', 'location'].some(w => w.includes(q) || q.includes(w));
    if (mapQ) out.push(cat.mapLocation);
    cat.shootDetails.filter(s => matchItem(s, q)).forEach(s => out.push(s));
    cat.fields.filter(f => matchItem(f, q)).forEach(f => out.push(f));
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
    const mapPanel = root.querySelector('[data-demo-map]');
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

    const renderPlaces = (places) => {
      if (!mapPanel) return;
      mapPanel.hidden = false;
      const list = mapPanel.querySelector('[data-demo-map-list]');
      list.innerHTML = places.length
        ? places.map((p) => {
            const idx = cat.samplePlaces.indexOf(p);
            return `<button type="button" class="typing-demo-place" data-place="${idx}"><strong>${escapeHtml(p.name)}</strong><span>${escapeHtml(p.subtitle)} · ${p.lat.toFixed(4)}, ${p.lon.toFixed(4)}</span></button>`;
          }).join('')
        : '<p class="typing-demo-hint">No demo places match. Try Louisville or Park.</p>';
    };

    const choose = (item) => {
      menu.hidden = true;
      matches = [];
      if (item.id === 'map.location') {
        pending = { mode: 'map' };
        input.value = '';
        input.placeholder = 'Search a place for a map pin…';
        setHint('In the app this opens Find place. Typed Location is a name only; Map Location adds a GPS pin you review first.');
        renderPlaces(cat.samplePlaces);
        input.focus();
        return;
      }
      if (mapPanel) mapPanel.hidden = true;
      pending = item;
      input.value = '';
      input.placeholder = `${item.label}…`;
      if (item.id === 'locationsShown' || item.id === 'input.location') {
        setHint('Place name only — no GPS yet. Use Map Location (GPS) when you want a pin.');
      } else if ((item.detail || '').includes('Shoot')) {
        setHint('Shoot detail for naming and folders. Capture times stay unchanged.');
      } else {
        setHint(`Type a value for ${item.label}, then Return. Review appears on the right — nothing writes until Apply in the app.`);
      }
      input.focus();
    };

    const pickPlace = (place) => {
      upsertRow('map.location', 'Map Location (GPS)',
        `${escapeHtml(place.name)}<span class="typing-demo-coords">${place.lat.toFixed(5)}, ${place.lon.toFixed(5)}</span>`,
        'Pin reviewed — GPS + place details');
      upsertRow('locationsShown', 'IPTC Place Shown', escapeHtml(place.name), 'Place text from the pin');
      pending = null;
      input.value = '';
      input.placeholder = 'Type ; for another field…';
      if (mapPanel) mapPanel.hidden = true;
      setHint('Map pin is in the review panel. In Ingest you confirm before GPS is written.');
    };

    if (mapPanel) {
      mapPanel.addEventListener('click', (e) => {
        const btn = e.target.closest('[data-place]');
        if (!btn) return;
        pickPlace(cat.samplePlaces[Number(btn.dataset.place)]);
      });
    }

    input.addEventListener('input', () => {
      const v = input.value;
      if (pending && pending.mode === 'map') {
        const q = v.toLowerCase();
        renderPlaces(cat.samplePlaces.filter(p => !q || `${p.name} ${p.subtitle}`.toLowerCase().includes(q)));
        return;
      }
      if (pending) return;
      if (v.startsWith(';')) {
        matches = suggestionsFor(cat, v.slice(1));
        active = 0;
        paintMenu();
        setHint(matches.length ? '↑↓ to move, Tab or Return to take the field.' : 'No matching fields.');
      } else {
        matches = [];
        menu.hidden = true;
        if (!v) setHint('Type ; to see fields — including Map Location (GPS). Same habit as Metadata Assist.');
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
          setHint('Type ; to see fields — including Map Location (GPS). Same habit as Metadata Assist.');
        }
        return;
      }
      if (pending && pending.mode === 'map' && e.key === 'Escape') {
        e.preventDefault();
        pending = null; input.value = ''; input.placeholder = 'Type ; for a field…';
        if (mapPanel) mapPanel.hidden = true;
        setHint('Type ; to see fields — including Map Location (GPS). Same habit as Metadata Assist.');
        return;
      }
      if (pending && pending.mode !== 'map' && e.key === 'Enter') {
        e.preventDefault();
        const value = input.value.trim() || '(example value)';
        const isPlaceText = pending.id === 'locationsShown' || pending.id === 'input.location';
        upsertRow(pending.id, pending.label, escapeHtml(value),
          isPlaceText ? 'Place name only — no GPS pin' : (pending.detail || ''));
        pending = null;
        input.value = '';
        input.placeholder = 'Type ; for another field…';
        setHint(isPlaceText
          ? 'Place text is staged. Choose Map Location (GPS) when you also want a pin.'
          : 'Review panel updated. In Ingest, Apply writes only after you confirm.');
        return;
      }
      if (pending && pending.mode !== 'map' && e.key === 'Escape') {
        e.preventDefault();
        pending = null; input.value = ''; input.placeholder = 'Type ; for a field…';
        setHint('Type ; to see fields — including Map Location (GPS). Same habit as Metadata Assist.');
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
