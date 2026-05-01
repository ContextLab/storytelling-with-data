// Figure 3: Themes that emerge from "How will you apply what you learned?"
// Uses the curated theme codebook from pipeline/curated_themes.py:
// every applicable freetext_item carries `curated_theme_id` (e.g. "kindness",
// "avoid_substances") assigned via cosine match to a small set of human-named
// themes. Renders as bar chart + per-theme drill-down.

import { escapeHTML, openSidePanel } from '../app.js';

const STATE = {
  groupBy: 'event',  // 'event' | 'role' | 'session' | 'all'
  showOther: false,
  showUncertain: false,
};

export function renderApplicationThemes(root, state) {
  root.innerHTML = '';
  // Find all "how will you apply" columns
  const applyCols = state.bundle.columns.filter(c =>
    c.original_header.toLowerCase().includes('how will you apply')
  );
  const applyColIds = new Set(applyCols.map(c => c.id));

  // Pull all freetext items for those columns
  const items = state.bundle.freetext_items.filter(ft => applyColIds.has(ft.column_id));

  // Curated theme metadata
  const themeRecords = state.bundle.curated_themes || [];
  const themeById = new Map(themeRecords.map(t => [t.id, t]));

  // Filter "other" / "uncertain" if disabled
  let visible = items.filter(ft => ft.curated_theme_id);
  if (!STATE.showOther)     visible = visible.filter(ft => ft.curated_theme_id !== 'other');
  if (!STATE.showUncertain) visible = visible.filter(ft => ft.curated_theme_id !== 'uncertain');

  // Group: themeId × groupKey → list of items
  const buckets = new Map();
  for (const ft of visible) {
    const groupKey = themeGroupKey(ft, state);
    const key = `${groupKey}::${ft.curated_theme_id}`;
    if (!buckets.has(key)) buckets.set(key, { groupKey, themeId: ft.curated_theme_id, items: [] });
    buckets.get(key).items.push(ft);
  }

  const rows = [...buckets.values()]
    .map(b => ({ ...b, theme: themeById.get(b.themeId), n: b.items.length }))
    .filter(b => b.theme)
    .sort((a, b) => b.n - a.n);

  const totalAssigned = rows.reduce((a, b) => a + b.n, 0);
  const totalItems = items.length;
  const otherCount = items.filter(ft => ft.curated_theme_id === 'other').length;
  const uncertainCount = items.filter(ft => ft.curated_theme_id === 'uncertain').length;

  const wrap = document.createElement('div');
  wrap.innerHTML = `
    <div class="panel">
      <div class="panel-title">about this figure</div>
      <h2 style="margin-top:0">Themes from "How will you apply what you learned?"</h2>
      <p class="lede">Every "how will you apply" response is matched against a curated codebook of <strong>${themeRecords.length - 1}</strong> human-named themes by cosine similarity in MiniLM embedding space. Below-threshold responses fall into the "Other" bucket.
      Click any theme to read sample responses + see the demographic breakdown.</p>
      <p class="lede" style="font-size:13px"><strong>${totalItems} total responses</strong> · ${totalAssigned} fall into a named theme · ${otherCount} are "Other" · ${uncertainCount} are "Not sure / no answer"</p>
    </div>

    <div class="panel">
      <div class="panel-title">controls</div>
      group themes by:
      <span class="chip" data-group="event" tabindex="0">event</span>
      <span class="chip" data-group="role" tabindex="0">role</span>
      <span class="chip" data-group="session" tabindex="0">session</span>
      <span class="chip" data-group="all" tabindex="0">all (no grouping)</span>
      &nbsp;&nbsp;
      <span class="chip" data-other tabindex="0">${STATE.showOther ? '✓ ' : ''}include "other"</span>
      <span class="chip" data-uncertain tabindex="0">${STATE.showUncertain ? '✓ ' : ''}include "not sure"</span>
    </div>

    <div class="panel">
      <div class="panel-title">themes (sorted by size within each group)</div>
      <div id="at-host"></div>
    </div>
  `;
  root.appendChild(wrap);

  document.querySelectorAll('[data-group]').forEach(el => {
    el.classList.toggle('active', el.dataset.group === STATE.groupBy);
    el.classList.toggle('muted',  el.dataset.group !== STATE.groupBy);
    el.addEventListener('click', () => { STATE.groupBy = el.dataset.group; renderApplicationThemes(root, state); });
  });
  document.querySelector('[data-other]').addEventListener('click', () => {
    STATE.showOther = !STATE.showOther;
    renderApplicationThemes(root, state);
  });
  document.querySelector('[data-uncertain]').addEventListener('click', () => {
    STATE.showUncertain = !STATE.showUncertain;
    renderApplicationThemes(root, state);
  });

  drawThemeBars(rows, state, themeById);
}

function themeGroupKey(ft, state) {
  if (STATE.groupBy === 'all') return 'all themes';
  const col = state.columnById.get(ft.column_id);
  if (STATE.groupBy === 'role')    return col?.rtu_role ?? 'unspecified';
  if (STATE.groupBy === 'session') return col?.rtu_session ?? 'unspecified';
  if (STATE.groupBy === 'event') {
    const ev = state.bundle.events.find(e => e.sheet_id === col?.sheet_id);
    return ev?.display_name ?? '?';
  }
  return 'all';
}

function drawThemeBars(rows, state, themeById) {
  const host = document.getElementById('at-host');
  host.innerHTML = '';
  if (rows.length === 0) {
    host.innerHTML = '<div class="empty-state">No themes match the current filter.</div>';
    return;
  }

  // Group rows by groupKey for visual sectioning
  const sections = new Map();
  for (const r of rows) {
    if (!sections.has(r.groupKey)) sections.set(r.groupKey, []);
    sections.get(r.groupKey).push(r);
  }

  const cat = state.bundle.palette.categorical;
  const groupKeys = [...sections.keys()].sort();
  const groupColor = d3.scaleOrdinal().domain(groupKeys).range(groupKeys.map((_, i) => cat[i % cat.length]));

  for (const gk of groupKeys) {
    const section = document.createElement('div');
    section.style.marginBottom = '20px';
    const sectionRows = sections.get(gk);
    const sectionTotal = sectionRows.reduce((a, b) => a + b.n, 0);
    section.innerHTML = `
      <div class="panel-title" style="border-left: 3px solid ${groupColor(gk)}; padding-left: 10px; margin-bottom: 8px;">
        ${escapeHTML(gk)} · ${sectionRows.length} themes · ${sectionTotal} responses
      </div>
      <div class="theme-bars" style="display: grid; grid-template-columns: 220px 1fr 60px 1fr; gap: 6px 12px; align-items: center;"></div>
    `;
    host.appendChild(section);

    const grid = section.querySelector('.theme-bars');
    const maxInSection = Math.max(...sectionRows.map(r => r.n));

    for (const r of sectionRows) {
      const labelCell = document.createElement('div');
      labelCell.style.fontFamily = 'var(--font-mono)';
      labelCell.style.fontSize = '12px';
      labelCell.style.color = 'var(--cat-1)';
      labelCell.style.cursor = 'pointer';
      labelCell.textContent = r.theme.name;
      labelCell.tabIndex = 0;
      labelCell.title = 'Click for response detail';
      labelCell.addEventListener('click', () => showThemeDrill(r, state));

      const barCell = document.createElement('div');
      barCell.style.position = 'relative';
      barCell.style.height = '18px';
      barCell.style.background = 'var(--seq-1)';
      barCell.style.borderRadius = '3px';
      barCell.style.cursor = 'pointer';
      const fill = document.createElement('div');
      fill.style.height = '100%';
      fill.style.width = (r.n / maxInSection * 100) + '%';
      fill.style.background = groupColor(gk);
      fill.style.borderRadius = '3px';
      fill.style.transition = 'width 200ms ease';
      barCell.appendChild(fill);
      barCell.addEventListener('click', () => showThemeDrill(r, state));

      const countCell = document.createElement('div');
      countCell.style.fontFamily = 'var(--font-mono)';
      countCell.style.fontSize = '12px';
      countCell.style.color = 'var(--ink-soft)';
      countCell.style.textAlign = 'right';
      countCell.textContent = `n=${r.n}`;

      const descCell = document.createElement('div');
      descCell.style.fontFamily = 'var(--font-serif)';
      descCell.style.fontStyle = 'italic';
      descCell.style.fontSize = '12px';
      descCell.style.color = 'var(--ink-soft)';
      descCell.textContent = r.theme.description;

      grid.appendChild(labelCell);
      grid.appendChild(barCell);
      grid.appendChild(countCell);
      grid.appendChild(descCell);
    }
  }
}

function showThemeDrill(row, state) {
  const items = row.items;

  // Demographic breakdown
  const bySchool = bucketCount(items, ft => state.responseById.get(ft.response_id)?.school);
  const byGrade  = bucketCount(items, ft => state.responseById.get(ft.response_id)?.grade_level);
  const byRole   = bucketCount(items, ft => state.columnById.get(ft.column_id)?.rtu_role);
  const byEvent  = bucketCount(items, ft => {
    const sheet = state.sheetById.get(state.responseById.get(ft.response_id)?.sheet_id);
    return state.bundle.events.find(e => e.sheet_id === sheet?.id)?.display_name;
  });

  const renderBuckets = (m, title) => {
    const sorted = [...m.entries()].sort((a, b) => b[1] - a[1]);
    if (sorted.length === 0) return '';
    return `
      <h4 style="font-family:var(--font-mono);font-size:11px;letter-spacing:0.06em;text-transform:uppercase;color:var(--ink-soft);margin:14px 0 4px">${title}</h4>
      ${sorted.map(([k, n]) => `
        <div style="display:flex;justify-content:space-between;font-family:var(--font-mono);font-size:12px;padding:2px 0">
          <span>${escapeHTML(k ?? 'unknown')}</span>
          <span style="color:var(--cat-1)">${n}</span>
        </div>
      `).join('')}
    `;
  };

  // Sample responses by sentiment range + 5 random
  const sampleSorted = items.slice().sort((a, b) => b.sentiment_score - a.sentiment_score);
  const samples = [];
  if (sampleSorted.length > 0) samples.push({ tag: 'most positive', ft: sampleSorted[0] });
  if (sampleSorted.length > 2) samples.push({ tag: 'median',         ft: sampleSorted[Math.floor(sampleSorted.length/2)] });
  if (sampleSorted.length > 1) samples.push({ tag: 'most negative',  ft: sampleSorted[sampleSorted.length-1] });
  const rng = mulberry32(items.length);
  const rest = sampleSorted.slice(1, -1);
  for (let i = 0; i < 7 && rest.length > 0; i++) {
    samples.push({ tag: 'random sample', ft: rest[Math.floor(rng() * rest.length)] });
  }

  const sampleCards = samples.map(s => {
    const resp = state.responseById.get(s.ft.response_id);
    return `
      <div style="border-left:3px solid var(--cat-3);padding:8px 10px;margin:6px 0;background:var(--seq-1)">
        <div style="font-family:var(--font-mono);font-size:10px;letter-spacing:0.06em;text-transform:uppercase;color:var(--ink-soft)">
          ${s.tag} · sentiment ${s.ft.sentiment_score.toFixed(2)} · theme score ${(s.ft.curated_theme_score ?? 0).toFixed(2)}
        </div>
        <div style="font-family:var(--font-serif);margin-top:4px">${escapeHTML(s.ft.text)}</div>
        <div style="font-family:var(--font-mono);font-size:11px;color:var(--ink-soft);margin-top:4px">${escapeHTML(resp?.school ?? '')} · grade ${escapeHTML(resp?.grade_level ?? '?')}</div>
      </div>
    `;
  }).join('');

  // Theme exemplars (so the user can see how the theme is anchored)
  const exemplarsHtml = (row.theme.exemplars || []).slice(0, 5).map(e =>
    `<div style="font-family:var(--font-serif);font-style:italic;font-size:12px;color:var(--ink-soft);margin:2px 0;">— ${escapeHTML(e)}</div>`
  ).join('');

  openSidePanel(`
    <h3>${escapeHTML(row.theme.name)}</h3>
    <div class="question">${escapeHTML(row.theme.description)}</div>
    <div class="stat-row"><span class="k">group</span><span class="v">${escapeHTML(row.groupKey)}</span></div>
    <div class="stat-row"><span class="k">responses in this cell</span><span class="v">${row.n}</span></div>
    <div class="stat-row"><span class="k">theme id</span><span class="v">${escapeHTML(row.theme.id)}</span></div>
    ${exemplarsHtml ? `
      <h4 style="font-family:var(--font-mono);font-size:11px;letter-spacing:0.06em;text-transform:uppercase;color:var(--ink-soft);margin:14px 0 4px">codebook exemplars</h4>
      ${exemplarsHtml}
    ` : ''}
    ${renderBuckets(byEvent, 'by event')}
    ${renderBuckets(byRole, 'by role')}
    ${renderBuckets(bySchool, 'by school')}
    ${renderBuckets(byGrade, 'by grade')}
    <h4 style="font-family:var(--font-mono);font-size:11px;letter-spacing:0.06em;text-transform:uppercase;color:var(--ink-soft);margin:14px 0 4px">sample responses (verbatim)</h4>
    ${sampleCards}
  `);
}

function bucketCount(items, keyFn) {
  const m = new Map();
  for (const ft of items) {
    const k = keyFn(ft);
    m.set(k, (m.get(k) || 0) + 1);
  }
  return m;
}

function mulberry32(seed) {
  return function() {
    let t = seed += 0x6D2B79F5;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
