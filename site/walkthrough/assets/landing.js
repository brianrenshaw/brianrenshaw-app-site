document.querySelectorAll('.comparison').forEach((comparison) => {
  const range = comparison.querySelector('input[type="range"]');
  const photos = comparison.querySelector('.compare-photos');
  if (!range || !photos) return;
  comparison.classList.add('compare-enabled');
  comparison.querySelector('.comparison-control').hidden = false;
  comparison.querySelector('figcaption > span').textContent = 'Drag photo or use the slider to compare.';
  const update = () => {
    const value = Number(range.value);
    comparison.style.setProperty('--split', `${value}%`);
    range.setAttribute('aria-valuetext', `${value}% original photo, ${100 - value}% outlined photo`);
    comparison.querySelectorAll('[data-compare-value]').forEach(button => {
      button.setAttribute('aria-pressed', String(Number(button.dataset.compareValue) === value));
    });
  };
  comparison.querySelectorAll('[data-compare-value]').forEach(button => {
    button.addEventListener('click', () => {
      range.value = button.dataset.compareValue;
      update();
    });
  });
  const setFromPointer = (event) => {
    const bounds = photos.getBoundingClientRect();
    range.value = Math.round(Math.max(0, Math.min(100, (event.clientX - bounds.left) / bounds.width * 100)));
    update();
  };
  range.addEventListener('input', update);
  photos.addEventListener('pointerdown', (event) => {
    if (event.button !== 0) return;
    photos.setPointerCapture(event.pointerId);
    setFromPointer(event);
  });
  photos.addEventListener('pointermove', (event) => {
    if (photos.hasPointerCapture(event.pointerId)) setFromPointer(event);
  });
  const endDrag = (event) => {
    if (photos.hasPointerCapture(event.pointerId)) photos.releasePointerCapture(event.pointerId);
  };
  photos.addEventListener('pointerup', endDrag);
  photos.addEventListener('pointercancel', endDrag);
  update();
});

document.querySelectorAll('.listing-sequence').forEach(sequence => {
  const controls = sequence.querySelector('.naming-controls');
  if (!controls) return;
  const buttons = [...controls.querySelectorAll('[data-naming]')];
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  let animations = [];
  const stop = () => { animations.forEach(animation => animation.cancel()); animations = []; };
  buttons.forEach(button => button.addEventListener('click', () => {
    if (button.getAttribute('aria-pressed') === 'true') return;
    stop();
    sequence.dataset.naming = button.dataset.naming;
    buttons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    sequence.querySelectorAll('.sequence-filename').forEach(label => {
      if (!motion.matches && label.animate) animations.push(label.animate([{opacity: .45}, {opacity: 1}], {duration: 180}));
    });
  }));
  motion.addEventListener('change', stop);
  sequence.dataset.naming = 'named';
  controls.hidden = false;
});
