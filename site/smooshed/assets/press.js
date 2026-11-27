const scene = document.querySelector(".press-scene");
const replay = scene.querySelector(".replay");
const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

function press() {
  if (reducedMotion.matches) return;
  scene.classList.remove("pressing");
  // Restart from the open stack even if the previous press is still running.
  void scene.offsetWidth;
  scene.classList.add("pressing");
}

replay.hidden = false;
replay.addEventListener("click", press);
const observer = new IntersectionObserver(entries => {
  if (entries.some(entry => entry.isIntersecting)) {
    press();
    observer.disconnect();
  }
}, { threshold: 0.35 });
observer.observe(scene);
