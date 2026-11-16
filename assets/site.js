const settings = { mode: 'sk-appearance', palette: 'sk-palette' };
const root = document.documentElement;
const modeButton = document.querySelector('#mode-toggle');
const paletteSelect = document.querySelector('#palette-select');

function synchronizeMode() {
  const dark = root.dataset.bsTheme === 'dark';
  modeButton.setAttribute('aria-pressed', String(dark));
  modeButton.setAttribute('aria-label', dark ? 'Switch to light mode' : 'Switch to dark mode');
}

function saveSetting(key, value) {
  try {
    localStorage.setItem(key, value);
  } catch {
    // The setting still works on the current page when storage is unavailable.
  }
}

synchronizeMode();
paletteSelect.value = root.dataset.palette;
modeButton.addEventListener('click', () => {
  root.dataset.bsTheme = root.dataset.bsTheme === 'dark' ? 'light' : 'dark';
  saveSetting(settings.mode, root.dataset.bsTheme);
  synchronizeMode();
});
paletteSelect.addEventListener('change', () => {
  root.dataset.palette = paletteSelect.value;
  saveSetting(settings.palette, root.dataset.palette);
});
lucide.createIcons();
