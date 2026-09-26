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

// Workspace examples: one quiet, keyboard-accessible disclosure at a time.
(() => {
  document.querySelectorAll('[data-workspaces]').forEach(workspaces => {
    const tabs = [...workspaces.querySelectorAll('[data-workspace-tab]')];
    const panels = tabs.map(tab => document.getElementById(tab.dataset.workspaceTab));
    if (!tabs.length || panels.some(panel => !panel)) return;
    tabs.forEach((tab, index) => {
      tab.setAttribute('role', 'tab');
      tab.setAttribute('aria-controls', panels[index].id);
      panels[index].setAttribute('role', 'tabpanel');
      panels[index].setAttribute('aria-labelledby', tab.id);
    });
    const select = (index, focus = false) => {
      tabs.forEach((tab, i) => {
        tab.setAttribute('aria-selected', String(i === index));
        tab.tabIndex = i === index ? 0 : -1;
        panels[i].hidden = i !== index;
      });
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
        if (next !== undefined) {
          event.preventDefault();
          select(next, true);
        }
      });
    });
    select(0);
    workspaces.classList.add('is-enhanced');
  });
})();

// Autoplay belongs only to the hero, never to the documentation tours.
(() => {
  document.querySelectorAll('[data-hero-carousel]').forEach(carousel => {
    const slides = [...carousel.querySelectorAll('[data-hero-slide]')];
    const selectors = [...carousel.querySelectorAll('[data-hero-select]')];
    const toggle = carousel.querySelector('[data-hero-toggle]');
    const status = carousel.querySelector('[data-hero-status]');
    const motion = matchMedia('(prefers-reduced-motion: reduce)');
    if (slides.length < 2 || selectors.length !== slides.length) return;
    let current = 0, timer, request = 0;
    let playing = !motion.matches, hovered = false, focused = false, visible = false;
    const prepare = async index => {
      const img = slides[index].querySelector('img');
      img.loading = 'eager';
      try { await img.decode(); return img.naturalWidth > 0; }
      catch { return false; }
    };
    const canPlay = () => playing && !motion.matches && !hovered && !focused && visible && !document.hidden;
    const schedule = () => {
      clearTimeout(timer);
      if (canPlay()) {
        timer = setTimeout(() => select((current + 1) % slides.length), 6000);
      }
    };
    const updatePlayback = () => {
      toggle.textContent = playing ? 'Pause' : 'Play';
      toggle.setAttribute('aria-label', playing ? 'Pause workspace slideshow' : 'Play workspace slideshow');
      // Reduced motion stays manual even if the user requests playback.
      toggle.hidden = motion.matches;
      schedule();
    };
    const render = () => {
      slides.forEach((slide, i) => {
        const active = i === current;
        slide.classList.toggle('is-active', active);
        slide.setAttribute('aria-hidden', String(!active));
        slide.inert = !active;
        selectors[i].setAttribute('aria-pressed', String(active));
      });
    };
    const select = async (index, manual = false) => {
      const token = ++request;
      clearTimeout(timer);
      if (manual) { playing = false; updatePlayback(); }
      if (!await prepare(index)) {
        if (token !== request) return;
        playing = false;
        status.textContent = 'That screenshot could not load. The current workspace is still available.';
        updatePlayback();
        return;
      }
      if (token !== request) return;
      if (!manual && !canPlay()) { schedule(); return; }
      current = index;
      render();
      if (manual) status.textContent = `${slides[index].dataset.workspace} workspace, ${index + 1} of ${slides.length}.`;
      schedule();
      prepare((current + 1) % slides.length);
    };
    selectors.forEach((button, index) => {
      button.addEventListener('click', () => select(index, true));
      button.addEventListener('keydown', event => {
        let next;
        if (event.key === 'ArrowRight') next = (index + 1) % slides.length;
        if (event.key === 'ArrowLeft') next = (index + slides.length - 1) % slides.length;
        if (event.key === 'Home') next = 0;
        if (event.key === 'End') next = slides.length - 1;
        if (next !== undefined) { event.preventDefault(); selectors[next].focus(); select(next, true); }
      });
    });
    carousel.querySelector('[data-hero-prev]').addEventListener('click', () => select((current + slides.length - 1) % slides.length, true));
    carousel.querySelector('[data-hero-next]').addEventListener('click', () => select((current + 1) % slides.length, true));
    toggle.addEventListener('click', () => { playing = !playing; updatePlayback(); });
    carousel.addEventListener('mouseenter', () => { hovered = true; schedule(); });
    carousel.addEventListener('mouseleave', () => { hovered = false; schedule(); });
    carousel.addEventListener('focusin', () => { focused = true; schedule(); });
    carousel.addEventListener('focusout', event => { focused = carousel.contains(event.relatedTarget); schedule(); });
    document.addEventListener('visibilitychange', schedule);
    motion.addEventListener('change', () => { if (motion.matches) playing = false; updatePlayback(); });
    new IntersectionObserver(entries => {
      visible = entries[0].isIntersecting;
      schedule();
    }, { threshold: .15 }).observe(carousel);
    render();
    carousel.classList.add('is-enhanced');
    carousel.querySelector('.hero-controls').hidden = false;
    updatePlayback();
    prepare(1);
  });
})();
