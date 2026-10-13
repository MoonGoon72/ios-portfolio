let printState = [];
window.addEventListener('beforeprint', () => {
  printState = [...document.querySelectorAll('details')].map(el => [el, el.open]);
  printState.forEach(([el]) => { el.open = true; });
});
window.addEventListener('afterprint', () => {
  printState.forEach(([el, open]) => { el.open = open; });
});

function openHashTarget() {
  let id;
  try { id = decodeURIComponent(window.location.hash.slice(1)); } catch { return; }
  if (!id) return;
  const target = document.getElementById(id);
  if (!target) return;
  let parent = target;
  while (parent) {
    if (parent instanceof HTMLDetailsElement) parent.open = true;
    parent = parent.parentElement;
  }
  requestAnimationFrame(() => target.scrollIntoView({ block: 'start' }));
}
window.addEventListener('hashchange', openHashTarget);
openHashTarget();
