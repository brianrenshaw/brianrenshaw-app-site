// Filtering progressively enhances the complete, server-rendered collection.
(() => {
  const browser = document.querySelector('.project-browser');
  const grid = document.querySelector('#project-grid');
  if (!browser || !grid) return;

  const buttons = [...browser.querySelectorAll('[data-filter]')];
  const projects = [...grid.querySelectorAll('[data-category]')];
  const status = browser.querySelector('.project-count');

  function filterProjects(category) {
    let count = 0;
    for (const project of projects) {
      project.hidden = category !== 'all' && !project.dataset.category.split(/\s+/).includes(category);
      if (!project.hidden) count += 1;
    }
    for (const section of grid.querySelectorAll('.collection')) {
      section.hidden = !section.querySelector('li:not([hidden])');
    }
    for (const button of buttons) {
      button.setAttribute('aria-pressed', String(button.dataset.filter === category));
    }
    status.textContent = `${count} ${count === 1 ? 'project' : 'projects'}`;
  }

  for (const button of buttons) {
    button.addEventListener('click', () => filterProjects(button.dataset.filter));
  }

  // Existing deep links still reveal their project after changing a filter.
  function revealHashTarget() {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const target = document.getElementById(id);
    const filteredTarget = target?.closest('[data-category], .collection');
    if (filteredTarget?.hidden || target?.matches('.collection')) {
      filterProjects('all');
      target.scrollIntoView({ block: 'start' });
    }
  }

  window.addEventListener('hashchange', revealHashTarget);
  document.querySelector('.categories')?.addEventListener('click', () => filterProjects('all'));
  browser.hidden = false;
})();

// One featured project for each platform. Manual selection keeps that project in view.
(() => {
  const showcase = document.querySelector('.showcase');
  if (!showcase) return;
  const controls = showcase.querySelector('.switcher');
  const slides = [...showcase.querySelectorAll('.slide')];
  const buttons = [...controls.querySelectorAll('[data-slide]')];
  const playback = controls.querySelector('.playback');
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  let playing = !motion.matches;
  let index = 0;
  let timer;
  let hoveringSlide = false;

  function show(next) {
    index = next;
    slides.forEach((slide, i) => { slide.hidden = i !== index; });
    buttons.forEach((button, i) => button.setAttribute('aria-pressed', String(i === index)));
  }

  function schedule() {
    clearTimeout(timer);
    playback.textContent = playing ? 'Pause' : 'Play';
    playback.setAttribute('aria-label', playing ? 'Pause rotation' : 'Start rotation');
    if (!playing || document.hidden || hoveringSlide) return;
    timer = setTimeout(() => {
      show((index + 1) % slides.length);
      schedule();
    }, 7000);
  }

  buttons.forEach((button, i) => button.addEventListener('click', () => {
    playing = false;
    show(i);
    schedule();
  }));
  playback.addEventListener('click', () => {
    playing = !playing;
    schedule();
  });
  showcase.addEventListener('focusin', event => {
    if (event.target === playback) return;
    playing = false;
    schedule();
  });
  slides.forEach(slide => {
    slide.addEventListener('pointerenter', event => {
      if (event.pointerType !== 'mouse') return;
      hoveringSlide = true;
      schedule();
    });
    slide.addEventListener('pointerleave', () => {
      hoveringSlide = false;
      schedule();
    });
  });
  document.addEventListener('visibilitychange', schedule);
  motion.addEventListener('change', () => {
    if (motion.matches) playing = false;
    schedule();
  });
  controls.hidden = false;
  schedule();
})();
