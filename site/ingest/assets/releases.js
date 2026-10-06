(() => {
  const picker = document.getElementById('release-version');
  if (!picker) return;
  picker.addEventListener('change', () => {
    const option = picker.selectedOptions[0];
    if (option?.value) location.assign(option.value);
  });
})();
