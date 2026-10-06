/* Native topic disclosure stays usable without this optional enhancement. */
(() => {
  const topics = document.querySelector('.doc-topics');
  if (!topics) return;
  const compact = matchMedia('(max-width: 1000px)');
  const fitNavigation = () => { topics.open = !compact.matches; };
  fitNavigation();
  compact.addEventListener('change', fitNavigation);
  // On desktop the full topic list remains visible. Compact screens retain
  // a normal native disclosure that can be opened with the keyboard.
  topics.querySelector('summary').addEventListener('click', event => {
    if (!compact.matches) event.preventDefault();
  });
  const links = [...topics.querySelectorAll('a[href^="#"]')];
  links.forEach(link => link.addEventListener('click', () => {
    if (compact.matches) topics.open = false;
  }));
  if (!('IntersectionObserver' in window)) return;
  const observer = new IntersectionObserver(entries => {
    const visible = entries.filter(entry => entry.isIntersecting)
      .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
    if (!visible.length) return;
    const href = `#${visible[0].target.id}`;
    links.forEach(link => {
      if (link.getAttribute('href') === href) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  }, { rootMargin: '-20px 0px -65% 0px', threshold: 0 });
  document.querySelectorAll('.doc-content > section[id]').forEach(section => observer.observe(section));
})();
