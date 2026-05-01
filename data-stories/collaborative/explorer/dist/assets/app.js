// T023: App shell — bundle loader + view router + filter store.

import { renderTables } from './views/tables.js';
import { renderCompare } from './views/compare.js';
import { renderTimeline } from './views/timeline.js';
import { renderSankey } from './views/sankey.js';
import { renderEffectiveness } from './views/effectiveness.js';
import { renderSentiment } from './views/sentiment.js';
import { renderThemeMap } from './views/theme-map.js';
import { renderRecipes } from './views/recipes.js';
import { renderCustom } from './views/custom.js';

const VIEWS = {
  'tables': renderTables, 'compare': renderCompare, 'timeline': renderTimeline,
  'sankey': renderSankey, 'effectiveness': renderEffectiveness,
  'sentiment': renderSentiment, 'theme-map': renderThemeMap, 'recipes': renderRecipes,
  'custom': renderCustom,
};

export const state = {
  bundle: null, currentView: 'tables',
  currentWorkbookId: null, currentSheetId: null,
  filters: { schools: new Set(), grades: new Set(), freetextQuery: '' },
  sheetById: new Map(), columnById: new Map(), workbookById: new Map(),
  measureById: new Map(), schoolById: new Map(),
  responsesBySheet: new Map(), freetextByColumn: new Map(),
  themeClustersByColumn: new Map(),
};

const subscribers = new Set();
export function onChange(fn) { subscribers.add(fn); return () => subscribers.delete(fn); }
function emit() { for (const fn of subscribers) try { fn(state); } catch (e) { console.error(e); } }

export function setHTML(el, html) { el.innerHTML = html; }
export function appendHTML(el, html) { el.insertAdjacentHTML('beforeend', html); }

async function loadBundle() {
  const candidates = ['data.json.gz', 'data.json'];
  let lastErr = null;
  for (const c of candidates) {
    try {
      const resp = await fetch(c);
      if (!resp.ok) { lastErr = new Error(c + ': HTTP ' + resp.status); continue; }
      if (c.endsWith('.gz')) {
        if (typeof DecompressionStream === 'undefined') continue;
        const stream = resp.body.pipeThrough(new DecompressionStream('gzip'));
        const text = await new Response(stream).text();
        return JSON.parse(text);
      }
      return await resp.json();
    } catch (err) { lastErr = err; }
  }
  throw lastErr || new Error('bundle not found');
}

function buildIndexes(bundle) {
  state.bundle = bundle;
  state.workbookById = new Map(bundle.workbooks.map(w => [w.id, w]));
  state.sheetById = new Map(bundle.sheets.map(s => [s.id, s]));
  state.columnById = new Map(bundle.columns.map(c => [c.id, c]));
  state.measureById = new Map(bundle.measures.map(m => [m.id, m]));
  state.schoolById = new Map(bundle.schools.map(s => [s.id, s]));
  state.responsesBySheet = new Map();
  for (const r of bundle.responses) {
    if (!state.responsesBySheet.has(r.sheet_id)) state.responsesBySheet.set(r.sheet_id, []);
    state.responsesBySheet.get(r.sheet_id).push(r);
  }
  state.freetextByColumn = new Map();
  for (const ft of bundle.freetext_items) {
    if (!state.freetextByColumn.has(ft.column_id)) state.freetextByColumn.set(ft.column_id, []);
    state.freetextByColumn.get(ft.column_id).push(ft);
  }
  state.themeClustersByColumn = new Map();
  for (const c of bundle.theme_clusters) {
    if (!state.themeClustersByColumn.has(c.column_id)) state.themeClustersByColumn.set(c.column_id, []);
    state.themeClustersByColumn.get(c.column_id).push(c);
  }
  state.responseById = new Map(bundle.responses.map(r => [r.id, r]));
  state.freetextById = new Map(bundle.freetext_items.map(ft => [ft.id, ft]));
  state.currentWorkbookId = bundle.workbooks[0]?.id ?? null;
  if (state.currentWorkbookId) {
    state.currentSheetId = state.workbookById.get(state.currentWorkbookId).sheet_ids[0] ?? null;
  }
}

function populateTopBar() {
  const wbSel = document.getElementById('workbook-select');
  const shSel = document.getElementById('sheet-select');
  setHTML(wbSel, '');
  for (const w of state.bundle.workbooks) {
    const o = document.createElement('option');
    o.value = w.id; o.textContent = w.title;
    if (w.id === state.currentWorkbookId) o.selected = true;
    wbSel.appendChild(o);
  }
  refreshSheetSelect();
  wbSel.addEventListener('change', e => {
    state.currentWorkbookId = e.target.value;
    state.currentSheetId = state.workbookById.get(state.currentWorkbookId).sheet_ids[0] ?? null;
    refreshSheetSelect(); routeAndRender(); emit();
  });
  shSel.addEventListener('change', e => {
    state.currentSheetId = e.target.value; routeAndRender(); emit();
  });
  document.getElementById('bundle-badge').textContent =
    'bundle v' + state.bundle.version + ' · ' +
    state.bundle.workbooks.length + ' workbooks · ' +
    state.bundle.responses.length + ' responses';
}

function refreshSheetSelect() {
  const shSel = document.getElementById('sheet-select');
  const wb = state.workbookById.get(state.currentWorkbookId);
  setHTML(shSel, '');
  if (!wb) return;
  for (const sid of wb.sheet_ids) {
    const sheet = state.sheetById.get(sid);
    const o = document.createElement('option');
    o.value = sid;
    o.textContent = sheet?.period_label ?? sid;
    if (sid === state.currentSheetId) o.selected = true;
    shSel.appendChild(o);
  }
  document.getElementById('crumbs').textContent =
    wb.title + ' · ' + (state.sheetById.get(state.currentSheetId)?.period_label ?? '');
}

function bindNav() {
  document.querySelectorAll('.rail .nav-item').forEach(el => {
    el.tabIndex = 0;
    const trigger = () => {
      const v = el.dataset.view;
      if (!v || v === state.currentView) return;
      document.querySelectorAll('.rail .nav-item').forEach(x => x.classList.remove('active'));
      el.classList.add('active');
      state.currentView = v;
      routeAndRender(); emit();
    };
    el.addEventListener('click', trigger);
    el.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); trigger(); }
    });
  });
}

function routeAndRender() {
  const root = document.getElementById('view-root');
  setHTML(root, '');
  const fn = VIEWS[state.currentView];
  if (typeof fn !== 'function') {
    setHTML(root, '<div class="empty-state">View not implemented: ' + state.currentView + '</div>');
    console.error('[explorer] missing view module for', state.currentView);
    return;
  }
  try { fn(root, state); }
  catch (err) {
    console.error('[explorer] view render failed', state.currentView, err);
    setHTML(root, '<div class="empty-state">View failed to render: ' + err.message + '</div>');
  }
}

function buildFilterRail() {
  const sBox = document.getElementById('filter-schools');
  const gBox = document.getElementById('filter-grades');
  const allSchools = [...new Set(state.bundle.responses.map(r => r.school))].sort();
  const allGrades = [...new Set(state.bundle.responses.map(r => r.grade_level).filter(Boolean))].sort();

  function makeChip(label, key, set) {
    const el = document.createElement('span');
    el.className = 'chip muted'; el.tabIndex = 0; el.textContent = label;
    const apply = () => {
      if (set.has(key)) { set.delete(key); el.classList.remove('active'); el.classList.add('muted'); }
      else { set.add(key); el.classList.add('active'); el.classList.remove('muted'); }
      routeAndRender(); emit();
    };
    el.addEventListener('click', apply);
    el.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); apply(); }
    });
    return el;
  }
  for (const sid of allSchools) {
    const s = state.schoolById.get(sid);
    sBox.appendChild(makeChip(s?.display_name ?? sid, sid, state.filters.schools));
  }
  for (const g of allGrades) {
    gBox.appendChild(makeChip('Grade ' + g, g, state.filters.grades));
  }
  document.getElementById('filter-search').addEventListener('input', e => {
    state.filters.freetextQuery = e.target.value.toLowerCase();
    routeAndRender(); emit();
  });
}

export function openSidePanel(html) {
  const panel = document.getElementById('side-panel');
  setHTML(document.getElementById('side-panel-body'), html);
  panel.classList.add('open');
  panel.setAttribute('aria-hidden', 'false');
}
export function closeSidePanel() {
  const panel = document.getElementById('side-panel');
  panel.classList.remove('open');
  panel.setAttribute('aria-hidden', 'true');
}
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('side-panel-close')?.addEventListener('click', closeSidePanel);
});

export function showTooltip(html, x, y) {
  const el = document.getElementById('tooltip');
  setHTML(el, html);
  el.style.left = (x + 12) + 'px';
  el.style.top = (y + 12) + 'px';
  el.classList.add('show');
}
export function hideTooltip() {
  document.getElementById('tooltip').classList.remove('show');
}

export function escapeHTML(s) {
  return String(s ?? '').replace(/[&<>"']/g, ch => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[ch]));
}

(async function main() {
  try {
    const bundle = await loadBundle();
    buildIndexes(bundle);
    populateTopBar();
    bindNav();
    buildFilterRail();
    routeAndRender(); emit();
  } catch (err) {
    console.error('[explorer] failed to load bundle', err);
    document.getElementById('view-root').innerHTML =
      '<div class="empty-state"><strong>Could not load data bundle.</strong><br/>' +
      escapeHTML(err.message) + '<br/><br/>' +
      'Run <code>python build/build.py</code> from the explorer/ folder to produce <code>dist/data.json</code>.</div>';
  }
})();
