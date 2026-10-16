/* A fictional explanation of the rule. Nothing is saved or sent. */
document.querySelectorAll('[data-decision-example]').forEach(example => {
  const buttons = [...example.querySelectorAll('[data-example-person]')];
  const result = example.querySelector('[data-example-result]');
  const explanation = example.querySelector('[data-example-explanation]');
  const outcome = example.querySelector('.example-outcome');
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  let animation;
  const update = () => {
    animation?.cancel();
    const count = buttons.filter(button => button.getAttribute('aria-pressed') === 'true').length;
    buttons.forEach(button => {
      button.textContent = `${button.dataset.examplePerson}: ${button.getAttribute('aria-pressed') === 'true' ? 'cancel' : 'keep the plan'}`;
    });
    result.textContent = count === 2 ? 'The plan is canceled.' : 'The plan is on.';
    explanation.textContent = count === 2 ? 'Both people chose to cancel. They can now see the shared result.' : count === 1 ? 'One person chose to cancel. That choice stays private; the plan is still on.' : 'Neither person has chosen to cancel.';
    outcome.classList.toggle('is-canceled', count === 2);
    if (count === 2 && !motion.matches && result.animate) animation = result.animate([{opacity: 0, transform: 'scale(1.04)'}, {opacity: 1, transform: 'scale(1)'}], {duration: 250, easing: 'ease-out'});
  };
  buttons.forEach(button => button.addEventListener('click', () => {
    button.setAttribute('aria-pressed', String(button.getAttribute('aria-pressed') !== 'true'));
    update();
  }));
  example.querySelector('.example-reset').addEventListener('click', () => {
    buttons.forEach(button => button.setAttribute('aria-pressed', 'false'));
    update();
  });
  motion.addEventListener('change', () => animation?.cancel());
  example.hidden = false;
});
