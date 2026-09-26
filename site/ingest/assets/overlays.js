/* Shared Ingest lightbox + detail modals. Progressive: links still navigate without JS. */
(() => {
  const FOCUSABLE = 'a[href],button:not([disabled]),textarea,input,select,summary,[tabindex]:not([tabindex="-1"])';
  let active = null;
  let lastFocus = null;

  const trap = (event) => {
    if (!active || event.key !== 'Tab') return;
    const nodes = [...active.querySelectorAll(FOCUSABLE)].filter(el => !el.hasAttribute('disabled') && el.offsetParent !== null);
    if (!nodes.length) { event.preventDefault(); return; }
    const first = nodes[0];
    const last = nodes[nodes.length - 1];
    if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
    else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
  };

  const close = () => {
    if (!active) return;
    active.remove();
    active = null;
    document.documentElement.classList.remove('ingest-overlay-open');
    document.removeEventListener('keydown', onKey);
    if (lastFocus && typeof lastFocus.focus === 'function') lastFocus.focus();
    lastFocus = null;
  };

  const onKey = (event) => {
    if (event.key === 'Escape') { event.preventDefault(); close(); return; }
    trap(event);
  };

  const openShell = ({ label, labelledBy, className }) => {
    close();
    lastFocus = document.activeElement;
    const root = document.createElement('div');
    root.className = className;
    root.innerHTML = `
      <div class="ingest-overlay-backdrop" data-overlay-close tabindex="-1"></div>
      <div class="ingest-overlay-dialog" role="dialog" aria-modal="true"${labelledBy ? ` aria-labelledby="${labelledBy}"` : ` aria-label="${label}"`}>
        <button type="button" class="ingest-overlay-close" data-overlay-close aria-label="Close">Close</button>
        <div class="ingest-overlay-body"></div>
      </div>`;
    document.body.appendChild(root);
    active = root;
    document.documentElement.classList.add('ingest-overlay-open');
    document.addEventListener('keydown', onKey);
    root.querySelectorAll('[data-overlay-close]').forEach(el => el.addEventListener('click', close));
    return root.querySelector('.ingest-overlay-body');
  };

  const openLightbox = (anchor) => {
    const img = anchor.querySelector('img');
    if (!img) return;
    const href = anchor.getAttribute('href');
    const caption = anchor.closest('figure')?.querySelector('figcaption')?.textContent?.trim()
      || img.getAttribute('alt')
      || '';
    const body = openShell({ label: caption || 'Screenshot', className: 'ingest-overlay ingest-lightbox' });
    body.innerHTML = `
      <figure class="ingest-lightbox-figure">
        <img src="${href}" alt="${(img.getAttribute('alt') || '').replace(/"/g, '&quot;')}" decoding="async">
        ${caption ? `<figcaption id="ingest-lightbox-caption">${caption.replace(/</g, '&lt;')}</figcaption>` : ''}
      </figure>`;
    const dialog = active.querySelector('.ingest-overlay-dialog');
    if (caption) dialog.setAttribute('aria-labelledby', 'ingest-lightbox-caption');
    active.querySelector('.ingest-overlay-close').focus();
  };

  const openDetail = (trigger) => {
    const title = trigger.getAttribute('data-detail-title') || trigger.textContent.trim();
    const html = trigger.getAttribute('data-detail-html') || trigger.getAttribute('data-detail-body') || '';
    const body = openShell({ labelledBy: 'ingest-detail-title', className: 'ingest-overlay ingest-detail-modal' });
    const titleEl = document.createElement('h2');
    titleEl.id = 'ingest-detail-title';
    titleEl.className = 'ingest-detail-title';
    titleEl.textContent = title;
    const content = document.createElement('div');
    content.className = 'ingest-detail-copy';
    // Prefer structured children already in the page (safer than inline HTML attributes).
    const sourceId = trigger.getAttribute('aria-controls') || trigger.getAttribute('data-detail-source');
    const source = sourceId ? document.getElementById(sourceId) : null;
    if (source) {
      const clone = source.cloneNode(true);
      clone.removeAttribute('hidden');
      content.append(...[...clone.childNodes]);
    } else if (html) content.innerHTML = html;
    else content.textContent = trigger.getAttribute('aria-description') || trigger.getAttribute('title') || '';
    body.append(titleEl, content);
    active.querySelector('.ingest-overlay-close').focus();
  };

  document.addEventListener('click', (event) => {
    const detail = event.target.closest('[data-ingest-detail]');
    if (detail) {
      event.preventDefault();
      openDetail(detail);
      return;
    }
    const shot = event.target.closest('.desktop-shot > a[href]');
    if (!shot) return;
    const href = shot.getAttribute('href') || '';
    if (!/\.(webp|png|jpe?g|gif)(\?|#|$)/i.test(href)) return;
    // Keep middle-click / modified clicks as native navigation.
    if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    openLightbox(shot);
  });
})();
