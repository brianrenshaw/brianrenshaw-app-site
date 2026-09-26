/* Progressively enhanced screenshot tours. All panels are readable without JS. */
(() => {
  document.querySelectorAll('[data-tour]').forEach(tour => {
    const tablist = tour.querySelector('.tour-tabs');
    const tabs = [...tablist.querySelectorAll('[data-tab]')];
    const panels = tabs.map(tab => document.getElementById(tab.dataset.tab));
    if (!tabs.length || panels.some(panel => !panel)) return;
    tablist.setAttribute('role', 'tablist');
    tabs.forEach((tab, index) => {
      tab.setAttribute('role', 'tab');
      tab.setAttribute('aria-controls', panels[index].id);
      panels[index].setAttribute('role', 'tabpanel');
      panels[index].setAttribute('aria-labelledby', tab.id);
      panels[index].tabIndex = 0;
    });
    const select = (index, focus = false) => {
      tabs.forEach((tab, i) => {
        tab.setAttribute('aria-selected', String(i === index));
        tab.tabIndex = i === index ? 0 : -1;
        panels[i].hidden = i !== index;
      });
      // Start loading the selected capture immediately without loading every tour image.
      panels[index].querySelectorAll('img').forEach(img => { img.loading = 'eager'; });
      if (focus) tabs[index].focus();
    };
    tabs.forEach((tab, index) => {
      tab.addEventListener('click', () => select(index));
      tab.addEventListener('keydown', event => {
        let next;
        if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
        if (event.key === 'ArrowLeft') next = (index + tabs.length - 1) % tabs.length;
        if (event.key === 'Home') next = 0;
        if (event.key === 'End') next = tabs.length - 1;
        if (next !== undefined) { event.preventDefault(); select(next, true); }
      });
    });
    const showHash = () => {
      const index = panels.findIndex(panel => panel.id === location.hash.slice(1));
      if (index !== -1) select(index);
    };
    select(0);
    tablist.hidden = false;
    tour.classList.add('is-enhanced');
    showHash();
    window.addEventListener('hashchange', showHash);
  });
})();

/* Before/after scrubber. Readable without JS as stacked panels. */
(() => {
  document.querySelectorAll('[data-scrubber]').forEach(root => {
    const after = root.querySelector('.scrubber-after');
    const range = root.querySelector('input[type="range"]');
    const guide = root.querySelector('.scrubber-guide');
    if (!after || !range) return;
    const set = (value) => {
      const pct = Math.max(0, Math.min(100, Number(value)));
      after.style.clipPath = `inset(0 0 0 ${pct}%)`;
      if (guide) guide.style.left = `${pct}%`;
      range.setAttribute('aria-valuenow', String(pct));
      range.value = String(pct);
    };
    range.addEventListener('input', () => set(range.value));
    root.classList.add('is-enhanced');
    set(range.value || 52);
  });
})();
