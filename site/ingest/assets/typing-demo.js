/* Interactive demo for rename tokens ({…}). Progressive enhancement.
   Semicolon / Metadata Assist is not demoed — the app flow is exact only in-app. */
(() => {
  const SAMPLE = {
    yyyy: '2026', yy: '26', mm: '09', dd: '25',
    hh: '16', mn: '07', seqn: '0042', seq: '42',
    base: 'DSC01206', ext: 'JPG', filename: 'DSC01206.JPG',
    client: 'Northside', event: 'Wedding', location: 'Louisville',
    city: 'Louisville', address: 'Main Street', shootdate: '2026-09-25',
    model: 'EOS R5', lens: 'RF 50mm', iso: '400', aperture: 'f/2',
    shutter: '1/500', folder: 'Card'
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
          ? 'Curly braces fill variables. Semicolon is a different habit — it finds metadata fields in Metadata Assist.'
          : 'Try {yyyy}{mm}{dd}-{seqn} or Wedding-{client}-{seqn}.';
      }
    };
    input.addEventListener('input', render);
    render();
  });
})();
