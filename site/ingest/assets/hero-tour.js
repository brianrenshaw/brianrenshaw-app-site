/* A manual still-image tour: no timer, playback, or automatic advancement. */
(() => {
  const tour = document.querySelector('[data-manual-tour]');
  if (!tour) return;
  const tablist = tour.querySelector('.hero-tour-tabs');
  const tabs = [...tablist.querySelectorAll('button')];
  const panels = tabs.map(tab => document.getElementById(tab.dataset.panel));
  if (panels.some(panel => !panel)) return;
  let current = 0;
  tablist.setAttribute('role', 'tablist');
  tabs.forEach((tab, i) => {
    tab.setAttribute('role', 'tab');
    tab.setAttribute('aria-controls', panels[i].id);
    panels[i].setAttribute('role', 'tabpanel');
    panels[i].setAttribute('aria-labelledby', tab.id);
    panels[i].tabIndex = 0;
  });
  const select = (index, focus = false) => {
    current = (index + tabs.length) % tabs.length;
    tabs.forEach((tab, i) => {
      tab.setAttribute('aria-selected', String(i === current));
      tab.tabIndex = i === current ? 0 : -1;
      panels[i].hidden = i !== current;
    });
    panels[current].querySelector('img').loading = 'eager';
    if (focus) tabs[current].focus();
  };
  tabs.forEach((tab, i) => {
    tab.addEventListener('click', () => select(i));
    tab.addEventListener('keydown', event => {
      const target = {ArrowRight: current + 1, ArrowLeft: current - 1, Home: 0, End: tabs.length - 1}[event.key];
      if (target !== undefined) {event.preventDefault(); select(target, true);}
    });
  });
  // Preserve vertical page scrolling and pinch zoom; only deliberate horizontal
  // gestures on the screenshot choose another view.
  const stage = tour.querySelector('.hero-tour-stage');
  let start;
  stage.addEventListener('touchstart', event => {
    start = event.touches.length === 1 ? {x: event.touches[0].clientX, y: event.touches[0].clientY} : null;
  }, {passive: true});
  stage.addEventListener('touchend', event => {
    if (!start || event.changedTouches.length !== 1) return;
    const dx = event.changedTouches[0].clientX - start.x;
    const dy = event.changedTouches[0].clientY - start.y;
    start = null;
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.5) select(current + (dx < 0 ? 1 : -1));
  }, {passive: true});
  stage.addEventListener('touchcancel', () => {start = null;}, {passive: true});
  select(0);
  tour.classList.add('is-enhanced');
  tablist.hidden = false;
})();
