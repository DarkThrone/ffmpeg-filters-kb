/* FFmpeg Filters KB — app.js
 * Handles: keyboard shortcuts, sidebar toggle, Algolia search modal
 */

// ─── Sidebar ────────────────────────────────────────────────────────────────
const sidebar = document.getElementById('sidebar');
const sidebarToggle = document.getElementById('sidebar-toggle');

function toggleSidebar() {
  sidebar.classList.toggle('collapsed');
  localStorage.setItem('sidebar-collapsed', sidebar.classList.contains('collapsed'));
}

// Restore sidebar state from localStorage
if (localStorage.getItem('sidebar-collapsed') === 'true') {
  sidebar.classList.add('collapsed');
}

sidebarToggle.addEventListener('click', toggleSidebar);

// ─── Search Modal ────────────────────────────────────────────────────────────
const searchModal  = document.getElementById('search-modal');
const searchInput  = document.getElementById('search-input');
const searchResults = document.getElementById('search-results');
const searchTrigger = document.getElementById('search-trigger');

let searchIndex = null;
let currentFocus = -1;

function openSearch() {
  searchModal.classList.add('open');
  searchInput.focus();
  currentFocus = -1;
}

function closeSearch() {
  searchModal.classList.remove('open');
  searchInput.value = '';
  searchResults.innerHTML = '';
  currentFocus = -1;
}

searchTrigger.addEventListener('click', openSearch);
searchModal.addEventListener('click', (e) => { if (e.target === searchModal) closeSearch(); });

// Algolia search
function initAlgolia() {
  if (!ALGOLIA_APP_ID || !ALGOLIA_SEARCH_KEY) return;
  const client = algoliasearch(ALGOLIA_APP_ID, ALGOLIA_SEARCH_KEY);
  searchIndex = client.initIndex(ALGOLIA_INDEX);
}

async function performSearch(query) {
  if (!query.trim()) { searchResults.innerHTML = ''; return; }
  if (!searchIndex) { renderFallback(query); return; }

  try {
    const { hits } = await searchIndex.search(query, { hitsPerPage: 8 });
    renderHits(hits);
  } catch (err) {
    console.error('Algolia search error:', err);
  }
}

function renderHits(hits) {
  if (!hits.length) {
    searchResults.innerHTML = '<div class="search-empty">No filters found.</div>';
    return;
  }
  searchResults.innerHTML = hits.map((hit, i) => `
    <a class="search-hit" href="${hit.url}" data-index="${i}">
      <span class="badge badge-${hit.category} hit-badge">${hit.category}</span>
      <div class="hit-name">${hit._highlightResult?.name?.value || hit.name}</div>
      <div class="hit-desc">${hit.description}</div>
    </a>
  `).join('');
  currentFocus = -1;
}

function renderFallback(_query) {
  searchResults.innerHTML = '<div class="search-empty">Search unavailable — Algolia not configured.</div>';
}

searchInput.addEventListener('input', (e) => performSearch(e.target.value));

// ─── Keyboard Navigation in Search Results ───────────────────────────────────
function moveFocus(dir) {
  const hits = searchResults.querySelectorAll('.search-hit');
  if (!hits.length) return;
  hits[currentFocus]?.classList.remove('focused');
  currentFocus = (currentFocus + dir + hits.length) % hits.length;
  hits[currentFocus]?.classList.add('focused');
  hits[currentFocus]?.scrollIntoView({ block: 'nearest' });
}

searchInput.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowDown')  { e.preventDefault(); moveFocus(1); }
  if (e.key === 'ArrowUp')    { e.preventDefault(); moveFocus(-1); }
  if (e.key === 'Enter') {
    const focused = searchResults.querySelector('.search-hit.focused');
    if (focused) { window.location.href = focused.href; closeSearch(); }
  }
});

// ─── Keyboard Shortcuts Modal ────────────────────────────────────────────────
const kbdModal = document.getElementById('kbd-modal');

function toggleKbdModal() { kbdModal.classList.toggle('open'); }
kbdModal.addEventListener('click', (e) => { if (e.target === kbdModal) kbdModal.classList.remove('open'); });

// ─── Global Keyboard Handler ─────────────────────────────────────────────────
document.addEventListener('keydown', (e) => {
  const tag = document.activeElement.tagName.toLowerCase();
  const typing = (tag === 'input' || tag === 'textarea');

  // Esc — close any open modal
  if (e.key === 'Escape') {
    if (searchModal.classList.contains('open'))  { closeSearch(); return; }
    if (kbdModal.classList.contains('open'))     { kbdModal.classList.remove('open'); return; }
  }

  if (typing) return; // don't hijack when user is typing

  // Ctrl+K or Cmd+K — open search
  if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
    e.preventDefault();
    searchModal.classList.contains('open') ? closeSearch() : openSearch();
    return;
  }

  // [ — toggle sidebar
  if (e.key === '[') { toggleSidebar(); return; }

  // ? — show keyboard shortcuts
  if (e.key === '?') { toggleKbdModal(); return; }
});

// ─── Copy Buttons on Code Blocks ─────────────────────────────────────────────
document.querySelectorAll('pre').forEach((pre) => {
  const btn = document.createElement('button');
  btn.className = 'copy-btn';
  btn.textContent = 'Copy';
  pre.style.position = 'relative';
  pre.appendChild(btn);
  btn.addEventListener('click', () => {
    const code = pre.querySelector('code')?.innerText || pre.innerText;
    navigator.clipboard.writeText(code).then(() => {
      btn.textContent = 'Copied!';
      btn.classList.add('copied');
      setTimeout(() => { btn.textContent = 'Copy'; btn.classList.remove('copied'); }, 2000);
    });
  });
});

// ─── Highlight active nav item ───────────────────────────────────────────────
document.querySelectorAll('.nav-item').forEach((link) => {
  if (link.href === window.location.href) link.classList.add('active');
});

// ─── Init ─────────────────────────────────────────────────────────────────────
initAlgolia();
