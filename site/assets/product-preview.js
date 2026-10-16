/* Real product captures, chosen by the visitor. All panels remain readable without JS. */
(() => {
  const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  document.querySelectorAll('[data-product-preview]').forEach(root => {
    const tablist = root.querySelector('[data-preview-tabs]');
    const tabs = [...(tablist?.querySelectorAll('button[aria-controls]') || [])];
    const panels = tabs.map(tab => document.getElementById(tab.getAttribute('aria-controls')));
    if (!tabs.length || panels.some(panel => !panel || !root.contains(panel))) return;
    let current = -1;
    let animations = [];
    const stopMotion = () => {
      animations.forEach(animation => animation.cancel());
      animations = [];
      panels.forEach((panel, index) => { panel.hidden = index !== current; });
    };
    const select = (index, animate = true) => {
      if (index === current) return;
      const previous = current;
      stopMotion();
      current = index;
      tabs.forEach((tab, i) => {
        const selected = i === current;
        tab.setAttribute('aria-selected', String(selected));
        tab.tabIndex = selected ? 0 : -1;
        panels[i].hidden = !selected;
        panels[i].inert = !selected;
        panels[i].setAttribute('aria-hidden', String(!selected));
      });
      const next = panels[current];
      next.querySelectorAll('img').forEach(img => { img.loading = 'eager'; });
      if (!animate || previous < 0 || motion.matches || !next.animate) return;
      const outgoing = panels[previous];
      outgoing.hidden = false;
      const duration = Number(root.dataset.previewDuration) || 200;
      const out = outgoing.animate([{opacity: 1}, {opacity: 0}], {duration, easing: 'ease-out'});
      const incoming = next.animate([{opacity: 0}, {opacity: 1}], {duration, easing: 'ease-out'});
      animations = [out, incoming];
      out.onfinish = () => { if (current !== previous) outgoing.hidden = true; };
    };
    tablist.setAttribute('role', 'tablist');
    tabs.forEach((tab, index) => {
      tab.setAttribute('role', 'tab');
      panels[index].setAttribute('role', 'tabpanel');
      panels[index].setAttribute('aria-labelledby', tab.id);
      panels[index].tabIndex = 0;
      tab.addEventListener('click', () => select(index));
      tab.addEventListener('keydown', event => {
        const vertical = tablist.getAttribute('aria-orientation') === 'vertical';
        const keys = vertical ? ['ArrowUp', 'ArrowDown'] : ['ArrowLeft', 'ArrowRight'];
        let next;
        if (event.key === keys[0]) next = (index - 1 + tabs.length) % tabs.length;
        if (event.key === keys[1]) next = (index + 1) % tabs.length;
        if (event.key === 'Home') next = 0;
        if (event.key === 'End') next = tabs.length - 1;
        if (next === undefined) return;
        event.preventDefault();
        select(next);
        tabs[next].focus();
      });
    });
    root.classList.add('preview-enhanced');
    const revealHash = () => {
      let id;
      try { id = decodeURIComponent(location.hash.slice(1)); } catch { return false; }
      const target = id && document.getElementById(id);
      const index = panels.findIndex(panel => panel === target || (target && panel.contains(target)));
      if (index < 0) return false;
      select(index, false);
      for (let parent = target.parentElement; parent && parent !== root; parent = parent.parentElement) {
        if (parent.tagName === 'DETAILS') parent.open = true;
      }
      requestAnimationFrame(() => target.scrollIntoView({block: 'start', behavior: 'instant'}));
      return true;
    };
    if (!revealHash()) select(0, false);
    tablist.hidden = false;
    window.addEventListener('hashchange', revealHash);
    // A second click on the current hash does not emit hashchange. It still
    // needs to reveal that chapter after the visitor has selected another tab.
    document.addEventListener('click', event => {
      const link = event.target.closest?.('a[href^="#"]');
      if (link && link.getAttribute('href') === location.hash) revealHash();
    });
    motion.addEventListener('change', stopMotion);
    if (root.hasAttribute('data-preview-swipe')) {
      const stage = root.querySelector('[data-preview-stage]');
      let start;
      stage?.addEventListener('touchstart', event => {
        start = event.touches.length === 1 ? {x: event.touches[0].clientX, y: event.touches[0].clientY} : null;
      }, {passive: true});
      stage?.addEventListener('touchend', event => {
        if (!start || event.changedTouches.length !== 1) return;
        const dx = event.changedTouches[0].clientX - start.x;
        const dy = event.changedTouches[0].clientY - start.y;
        start = null;
        if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.5) select((current + (dx < 0 ? 1 : -1) + tabs.length) % tabs.length);
      }, {passive: true});
      stage?.addEventListener('touchcancel', () => { start = null; }, {passive: true});
    }
  });
})();
