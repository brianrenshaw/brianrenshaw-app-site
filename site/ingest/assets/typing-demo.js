/* Interactive demos for Metadata Assist (;) and rename tokens ({…}). Progressive enhancement. */
(() => {
  const FIELDS = [
    { id: 'location', label: 'Location', aliases: ['loc', 'place', 'city'] },
    { id: 'caption', label: 'Caption', aliases: ['cap', 'title'] },
    { id: 'keywords', label: 'Keywords', aliases: ['kw', 'tags'] },
    { id: 'creator', label: 'Creator', aliases: ['by', 'author', 'photographer'] },
    { id: 'copyright', label: 'Copyright', aliases: ['©', 'rights'] },
    { id: 'client', label: 'Client', aliases: ['job'] },
    { id: 'event', label: 'Event', aliases: [] },
    { id: 'title', label: 'Title', aliases: [] }
  ];

  const SAMPLE = {
    yyyy: '2026', yy: '26', mm: '09', dd: '25',
    hh: '16', mn: '07', seqn: '0042', seq: '42',
    base: 'DSC01206', ext: 'JPG', filename: 'DSC01206.JPG',
    client: 'Northside', event: 'Wedding', location: 'Louisville',
    city: 'Louisville', address: 'Main Street', shootdate: '2026-09-25',
    model: 'EOS R5', lens: 'RF 50mm', iso: '400', aperture: 'f/2',
    shutter: '1/500', folder: 'Card'
  };

  const expandTemplate = (template) => {
    return template.replace(/\{([^}]+)\}/g, (full, key) => {
      const k = key.trim();
      if (Object.prototype.hasOwnProperty.call(SAMPLE, k)) return SAMPLE[k];
      // date: patterns — show a readable stand-in
      if (k.startsWith('date:')) return 'Sep 25, 2026';
      if (k.includes(':')) {
        const [name] = k.split(':');
        if (Object.prototype.hasOwnProperty.call(SAMPLE, name)) return SAMPLE[name];
      }
      return full; // unknown token stays visible
    });
  };

  const fieldMatches = (query) => {
    const q = query.toLowerCase();
    return FIELDS.filter(f => {
      if (!q) return true;
      const hay = `${f.label} ${f.id} ${(f.aliases || []).join(' ')}`.toLowerCase();
      return hay.includes(q) || f.id.startsWith(q) || f.label.toLowerCase().startsWith(q);
    });
  };

  document.querySelectorAll('[data-typing-demo="metadata"]').forEach(root => {
    const input = root.querySelector('[data-demo-input]');
    const menu = root.querySelector('[data-demo-menu]');
    const review = root.querySelector('[data-demo-review]');
    const hint = root.querySelector('[data-demo-hint]');
    if (!input || !menu || !review) return;

    let active = 0;
    let matches = [];
    let pendingField = null;

    const setHint = (text) => { if (hint) hint.textContent = text; };

    const paintMenu = () => {
      menu.innerHTML = '';
      if (!matches.length) {
        menu.hidden = true;
        return;
      }
      menu.hidden = false;
      matches.forEach((f, i) => {
        const li = document.createElement('li');
        li.className = 'typing-demo-option' + (i === active ? ' is-active' : '');
        li.textContent = f.label;
        li.addEventListener('mousedown', (e) => {
          e.preventDefault();
          choose(f);
        });
        menu.appendChild(li);
      });
    };

    const choose = (field) => {
      pendingField = field;
      input.value = '';
      input.placeholder = `${field.label}…`;
      menu.hidden = true;
      matches = [];
      setHint(`Type a value for ${field.label}, then press Return. Nothing is written until you apply in the real app.`);
      input.focus();
    };

    const addReview = (field, value) => {
      review.hidden = false;
      const row = document.createElement('div');
      row.className = 'typing-demo-review-row';
      row.innerHTML = `<strong>${field.label}</strong><span>${value.replace(/</g,'&lt;')}</span>`;
      review.querySelector('[data-demo-review-list]').appendChild(row);
      pendingField = null;
      input.placeholder = 'Type ; for another field…';
      setHint('Review panel (demo). In Ingest, Apply writes only after you confirm.');
    };

    input.addEventListener('input', () => {
      const v = input.value;
      if (pendingField) return;
      if (v.startsWith(';')) {
        const q = v.slice(1);
        matches = fieldMatches(q);
        active = 0;
        paintMenu();
        setHint(matches.length ? '↑↓ to move, Tab or Return to take the field.' : 'No matching fields.');
      } else {
        matches = [];
        menu.hidden = true;
        if (!v) setHint('Type ; to see field options — same habit as Metadata Assist.');
      }
    });

    input.addEventListener('keydown', (e) => {
      if (!pendingField && input.value.startsWith(';') && matches.length) {
        if (e.key === 'ArrowDown') { e.preventDefault(); active = Math.min(active + 1, matches.length - 1); paintMenu(); }
        if (e.key === 'ArrowUp') { e.preventDefault(); active = Math.max(active - 1, 0); paintMenu(); }
        if (e.key === 'Tab' || e.key === 'Enter') { e.preventDefault(); choose(matches[active]); }
        if (e.key === 'Escape') { e.preventDefault(); input.value = ''; matches = []; menu.hidden = true; setHint('Type ; to see field options — same habit as Metadata Assist.'); }
        return;
      }
      if (pendingField && e.key === 'Enter') {
        e.preventDefault();
        const value = input.value.trim() || '(example value)';
        input.value = '';
        addReview(pendingField, value);
      }
      if (pendingField && e.key === 'Escape') {
        e.preventDefault();
        pendingField = null;
        input.value = '';
        input.placeholder = 'Type ; for a field…';
        setHint('Type ; to see field options — same habit as Metadata Assist.');
      }
    });
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
