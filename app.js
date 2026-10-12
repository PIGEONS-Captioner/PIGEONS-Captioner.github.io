/* All scholarly content is static HTML; JavaScript only enhances interactions. */
const dialog = document.querySelector('#image-dialog');
const largeImage = document.querySelector('#large-image');
for (const link of document.querySelectorAll('.figure-link')) {
  link.addEventListener('click', event => {
    if (!dialog.showModal) return;
    event.preventDefault();
    largeImage.src = link.href;
    largeImage.alt = link.querySelector('img').alt;
    dialog.showModal();
  });
}
document.querySelector('#close-image').addEventListener('click', () => dialog.close());
dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
document.querySelector('#copy-citation').addEventListener('click', async () => {
  const code = document.querySelector('#bibtex');
  const status = document.querySelector('#copy-status');
  try {
    await navigator.clipboard.writeText(code.textContent);
    status.textContent = 'BibTeX copied.';
  } catch {
    const selection = window.getSelection();
    const range = document.createRange();
    range.selectNodeContents(code);
    selection.removeAllRanges();
    selection.addRange(range);
    status.textContent = 'Citation selected. Press Ctrl+C or ⌘C to copy.';
  }
});
// Keep resource links in sync with the release configuration.
fetch('links.json').then(response => {
  if (!response.ok) throw new Error('Link configuration unavailable');
  return response.json();
}).then(links => {
  for (const link of document.querySelectorAll('[data-resource]')) {
    const url = links[link.dataset.resource];
    if (typeof url !== 'string' || !url.startsWith('https://')) continue;
    link.href = url;
  }
}).catch(() => { /* Keep the static resource links when configuration cannot be loaded. */ });
