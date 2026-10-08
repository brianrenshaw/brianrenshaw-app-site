/* On phones, a step list becomes a slideshow: one step at a time, dots and arrows
   below it, swipe to move. Wider screens and no-script visitors see every step. */
(() => {
  const narrow = matchMedia('(max-width: 560px)');
  document.querySelectorAll('[data-step-carousel]').forEach((list, n) => {
    const steps = [...list.children];
    if (steps.length < 2) return;
    const button = (className, label, mark) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = className;
      b.setAttribute('aria-label', label);
      b.innerHTML = '<span aria-hidden="true">' + mark + '</span>';
      return b;
    };
    const controls = document.createElement('div');
    controls.className = 'step-carousel-controls';
    controls.hidden = true;
    const prev = button('step-carousel-arrow', 'Previous step', '‹');
    const next = button('step-carousel-arrow', 'Next step', '›');
    const dots = document.createElement('div');
    dots.className = 'step-carousel-dots';
    dots.setAttribute('role', 'tablist');
    dots.setAttribute('aria-label', list.getAttribute('aria-label') || 'Steps');
    const tabs = steps.map((step, i) => {
      const title = (step.querySelector('h3')?.textContent || '').replace(/\.$/, '');
      const tab = button('', 'Step ' + (i + 1) + ': ' + title, '');
      tab.setAttribute('role', 'tab');
      tab.id = 'step-tab-' + n + '-' + (i + 1);
      step.id ||= 'step-' + n + '-' + (i + 1);
      tab.setAttribute('aria-controls', step.id);
      dots.append(tab);
      return tab;
    });
    controls.append(prev, dots, next);
    // The controls sit right under the screenshot, at the same height on every step.
    const frame = document.createElement('div');
    frame.className = 'step-carousel';
    list.before(frame);
    frame.append(list, controls);
    const place = () => {
      const shot = on && (steps[current].querySelector('[data-step-shot]') || steps[current].querySelector('img'));
      controls.style.top = shot ? (shot.getBoundingClientRect().bottom - frame.getBoundingClientRect().top + 6) + 'px' : '';
    };
    let current = 0, on = false;
    const render = (focus = false) => {
      steps.forEach((step, i) => {
        const active = i === current;
        step.hidden = on && !active;
        step.inert = on && !active;
        if (on) { step.setAttribute('role', 'tabpanel'); step.setAttribute('aria-labelledby', tabs[i].id); }
        else { step.removeAttribute('role'); step.removeAttribute('aria-labelledby'); }
        tabs[i].setAttribute('aria-selected', String(active));
        tabs[i].tabIndex = active ? 0 : -1;
      });
      prev.disabled = current === 0;
      next.disabled = current === steps.length - 1;
      // Load this step and the next one before they are needed.
      [current, current + 1].forEach(i => steps[i]?.querySelectorAll('img').forEach(img => { img.loading = 'eager'; }));
      place();
      if (focus) tabs[current].focus();
    };
    const select = (index, focus = false) => {
      current = Math.max(0, Math.min(steps.length - 1, index));
      render(focus);
    };
    tabs.forEach((tab, i) => {
      tab.addEventListener('click', () => select(i));
      tab.addEventListener('keydown', event => {
        const target = {ArrowRight: current + 1, ArrowLeft: current - 1, Home: 0, End: steps.length - 1}[event.key];
        if (target !== undefined) { event.preventDefault(); select(target, true); }
      });
    });
    prev.addEventListener('click', () => select(current - 1));
    next.addEventListener('click', () => select(current + 1));
    // Keep vertical scrolling and pinch zoom; only a deliberate sideways swipe changes step.
    let start;
    list.addEventListener('touchstart', event => {
      start = on && event.touches.length === 1 ? {x: event.touches[0].clientX, y: event.touches[0].clientY} : null;
    }, {passive: true});
    list.addEventListener('touchend', event => {
      if (!start || event.changedTouches.length !== 1) return;
      const dx = event.changedTouches[0].clientX - start.x;
      const dy = event.changedTouches[0].clientY - start.y;
      start = null;
      if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.5) select(current + (dx < 0 ? 1 : -1));
    }, {passive: true});
    list.addEventListener('touchcancel', () => { start = null; }, {passive: true});
    const apply = () => {
      on = narrow.matches;
      list.classList.toggle('is-carousel', on);
      frame.classList.toggle('is-carousel', on);
      controls.hidden = !on;
      render();
    };
    narrow.addEventListener('change', apply);
    addEventListener('resize', place);
    steps.forEach(step => step.querySelectorAll('img').forEach(img => img.addEventListener('load', place)));
    apply();
  });
})();
