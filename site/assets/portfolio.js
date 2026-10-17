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
    const project = target?.closest('[data-category]');
    if (project?.hidden) {
      filterProjects('all');
      target.scrollIntoView({ block: 'start' });
    }
  }

  window.addEventListener('hashchange', revealHashTarget);
  browser.hidden = false;
})();
