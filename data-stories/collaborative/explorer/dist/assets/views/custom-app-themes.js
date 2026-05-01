// Figure 3: Themes that emerge from "How will you apply what you learned?"
// Aggregates HDBSCAN clusters across all 12 columns where this question appears,
// shows them as a bubble/treemap chart sized by member count, with a per-cluster
// side panel showing demographic distribution (school × grade × event × role).

import { escapeHTML, openSidePanel } from '../app.js';

const STATE = {
  groupBy: 'event',  // 'event' | 'role' | 'session' | 'school' | 'grade' | 'all'
  showUncategorized: false,
};

export function renderApplicationThemes(root, state) {
  root.innerHTML = '';
  // Find all "how will you apply" columns
  const applyCols = state.bundle.columns.filter(c =>
    c.original_header.toLowerCase().includes('how will you apply')
  );
  const applyColIds = new Set(applyCols.map(c => c.id));

  // Get all clusters for those columns
  const allClusters = state.bundle.theme_clusters
    .filter(tc => applyColIds.has(tc.column_id))
    .filter(tc => STATE.showUncategorized || !tc.id.endsWith('uncategorized'));

  // Annotate each cluster with the parent column's metadata
  const annotated = allClusters.map(tc => {
    const col = state.columnById.get(tc.column_id);
    return { ...tc, _col: col };
  });

  // Group clusters by chosen dimension and sum members
  const buckets = new Map();  // key -> { label, total, clusters: [] }
  for (const tc of annotated) {
    const groupKey = themeGroupKey(tc, state);
    const themeKey = `${groupKey}::${tc.label}`;
    if (!buckets.has(themeKey)) {
      buckets.set(themeKey, { groupKey, label: tc.label, total: 0, clusters: [] });
    }
    const b = buckets.get(themeKey);
    b.total += tc.member_count;
    b.clusters.push(tc);
  }

  const rows = [...buckets.values()].sort((a, b) => b.total - a.total);
  const totalMembers = rows.reduce((a, b) => a + b.total, 0);

  const wrap = document.createElement('div');
  wrap.innerHTML = `
    <div class="panel">
      <div class="panel-title">about this figure</div>
      <h2 style="margin-top:0">Themes from "How will you apply what you learned?"</h2>
      <p class="lede">Each row is one auto-named theme cluster from HDBSCAN over MiniLM embeddings of every "how will you apply" response across the dataset (${applyCols.length} columns).
      Bars are sized by member count. Click any theme to drill into the actual responses + demographic breakdown.</p>
      <p class="lede" style="font-size:13px"><strong>${rows.length} themes</strong> · <strong>${totalMembers} responses</strong> · grouped by <strong>${STATE.groupBy}</strong></p>
    </div>

    <div class="panel">
      <div class="panel-title">controls</div>
      group themes by:
      <span class="chip" data-group="event" tabindex="0">event</span>
      <span class="chip" data-group="role" tabindex="0">role</span>
      <span class="chip" data-group="session" tabindex="0">session</span>
      <span class="chip" data-group="all" tabindex="0">none (all)</span>
      &nbsp;&nbsp;
      <span class="chip" data-uncat tabindex="0">${STATE.showUncategorized ? '✓ ' : ''}include uncategorized</span>
    </div>

    <div class="panel">
      <div class="panel-title">themes (sorted by size)</div>
      <div id="at-host"></div>
    </div>
  `;
  root.appendChild(wrap);

  document.querySelectorAll('[data-group]').forEach(el => {
    el.classList.toggle('active', el.dataset.group === STATE.groupBy);
    el.classList.toggle('muted',  el.dataset.group !== STATE.groupBy);
    el.addEventListener('click', () => { STATE.groupBy = el.dataset.group; renderApplicationThemes(root, state); });
  });
  document.querySelector('[data-uncat]').addEventListener('click', () => {
    STATE.showUncategorized = !STATE.showUncategorized;
    renderApplicationThemes(root, state);
  });

  drawThemeBars(rows, state, totalMembers);
}

function themeGroupKey(tc, state) {
  if (STATE.groupBy === 'all') return 'all themes';
  if (STATE.groupBy === 'role')    return tc._col?.rtu_role ?? 'unspecified';
  if (STATE.groupBy === 'session') return tc._col?.rtu_session ?? 'unspecified';
  if (STATE.groupBy === 'event') {
    const ev = state.bundle.events.find(e => e.sheet_id === tc._col?.sheet_id);
    return ev?.display_name ?? '?';
  }
  return 'all';
}

function drawThemeBars(rows, state, totalMembers) {
  const host = document.getElementById('at-host');
  host.innerHTML = '';
  if (rows.length === 0) {
    host.innerHTML = '<div class="empty-state">No themes match the current filter.</div>';
    return;
  }

  // Group themes by groupKey for visual sectioning
  const sections = new Map();  // groupKey -> rows[]
  for (const r of rows) {
    if (!sections.has(r.groupKey)) sections.set(r.groupKey, []);
    sections.get(r.groupKey).push(r);
  }

  const cat = state.bundle.palette.categorical;
  const seq = state.bundle.palette.sequential;
  const groupKeys = [...sections.keys()].sort();
  const groupColor = d3.scaleOrdinal().domain(groupKeys).range(groupKeys.map((_, i) => cat[i % cat.length]));

  for (const gk of groupKeys) {
    const section = document.createElement('div');
    section.style.marginBottom = '20px';
    const sectionRows = sections.get(gk);
    const sectionTotal = sectionRows.reduce((a, b) => a + b.total, 0);
    section.innerHTML = `
      <div class="panel-title" style="border-left: 3px solid ${groupColor(gk)}; padding-left: 10px; margin-bottom: 8px;">
        ${escapeHTML(gk)} · ${sectionRows.length} themes · ${sectionTotal} responses
      </div>
      <div class="theme-bars" style="display: grid; grid-template-columns: 220px 1fr 60px 1fr; gap: 6px 12px; align-items: center;"></div>
    `;
    host.appendChild(section);

    const grid = section.querySelector('.theme-bars');
    const maxInSection = Math.max(...sectionRows.map(r => r.total));

    for (const r of sectionRows) {
      const labelCell = document.createElement('div');
      labelCell.style.fontFamily = 'var(--font-mono)';
      labelCell.style.fontSize = '12px';
      labelCell.style.color = 'var(--cat-1)';
      labelCell.style.cursor = 'pointer';
      labelCell.textContent = r.label;
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
      fill.style.width = (r.total / maxInSection * 100) + '%';
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
      countCell.textContent = `n=${r.total}`;

      const descCell = document.createElement('div');
      descCell.style.fontFamily = 'var(--font-serif)';
      descCell.style.fontStyle = 'italic';
      descCell.style.fontSize = '12px';
      descCell.style.color = 'var(--ink-soft)';
      const sampleDesc = r.clusters[0]?.description ?? '';
      descCell.textContent = sampleDesc;

      grid.appendChild(labelCell);
      grid.appendChild(barCell);
      grid.appendChild(countCell);
      grid.appendChild(descCell);
    }
  }
}

function showThemeDrill(row, state) {
  // Gather all freetext items belonging to this theme's cluster ids
  const clusterIds = new Set(row.clusters.map(c => c.id));
  const items = state.bundle.freetext_items.filter(ft => clusterIds.has(ft.cluster_id));

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

  // Sample responses (top 12 by sentiment_score range)
  const sampleSorted = items.slice().sort((a, b) => b.sentiment_score - a.sentiment_score);
  const samples = [];
  if (sampleSorted.length > 0) samples.push({ tag: 'most positive', ft: sampleSorted[0] });
  if (sampleSorted.length > 2) samples.push({ tag: 'median',         ft: sampleSorted[Math.floor(sampleSorted.length/2)] });
  if (sampleSorted.length > 1) samples.push({ tag: 'most negative',  ft: sampleSorted[sampleSorted.length-1] });
  // Plus 5 random ones
  const rng = mulberry32(items.length);
  const rest = sampleSorted.slice(1, -1);
  for (let i = 0; i < 5 && rest.length > 0; i++) {
    samples.push({ tag: 'random sample', ft: rest[Math.floor(rng() * rest.length)] });
  }

  const sampleCards = samples.map(s => {
    const resp = state.responseById.get(s.ft.response_id);
    return `
      <div style="border-left:3px solid var(--cat-3);padding:8px 10px;margin:6px 0;background:var(--seq-1)">
        <div style="font-family:var(--font-mono);font-size:10px;letter-spacing:0.06em;text-transform:uppercase;color:var(--ink-soft)">${s.tag} · sentiment ${s.ft.sentiment_score.toFixed(2)}</div>
        <div style="font-family:var(--font-serif);margin-top:4px">${escapeHTML(s.ft.text)}</div>
        <div style="font-family:var(--font-mono);font-size:11px;color:var(--ink-soft);margin-top:4px">${escapeHTML(resp?.school ?? '')} · grade ${escapeHTML(resp?.grade_level ?? '?')}</div>
      </div>
    `;
  }).join('');

  openSidePanel(`
    <h3>${escapeHTML(row.label)}</h3>
    <div class="question">${escapeHTML(row.groupKey)}</div>
    <div class="stat-row"><span class="k">total responses</span><span class="v">${row.total}</span></div>
    <div class="stat-row"><span class="k">source clusters</span><span class="v">${row.clusters.length}</span></div>
    <div class="stat-row"><span class="k">naming method</span><span class="v">${escapeHTML(row.clusters[0]?.naming_method ?? '?')}</span></div>
    ${renderBuckets(byEvent, 'by event')}
    ${renderBuckets(byRole, 'by role')}
    ${renderBuckets(bySchool, 'by school')}
    ${renderBuckets(byGrade, 'by grade')}
    <h4 style="font-family:var(--font-mono);font-size:11px;letter-spacing:0.06em;text-transform:uppercase;color:var(--ink-soft);margin:14px 0 4px">sample responses</h4>
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
