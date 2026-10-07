let printState = [];
window.addEventListener('beforeprint', () => {
  printState = [...document.querySelectorAll('details')].map(el => [el, el.open]);
  printState.forEach(([el]) => { el.open = true; });
});
window.addEventListener('afterprint', () => {
  printState.forEach(([el, open]) => { el.open = open; });
});
