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
  };
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
