// T060-T062: Theme map view — UMAP scatter of free-text embeddings,
// clustered by HDBSCAN, auto-named, click-to-drill side panel.

import { escapeHTML, openSidePanel } from '../app.js';

const STATE = {
  columnId: null,
  colorBy: 'sentiment',  // 'sentiment' | 'school' | 'grade' | 'event' | 'year' | 'cluster'
};

const MIN_ITEMS = 30;

export function renderThemeMap(root, appState) {
  const wrap = document.createElement('div');
  wrap.innerHTML = `
    <h1>Theme map</h1>
    <p class="lede">UMAP projection of every free-text response. Dots cluster by topic; clusters are auto-named. Click any dot to read the response, or click a cluster label to see all members.</p>

    <div class="panel">
      <div class="panel-title">free-text column (≥${MIN_ITEMS} items)</div>
      <select id="tm-col"></select>
    </div>

    <div class="panel">
      <div class="panel-title">color by</div>
      <span class="chip" data-color="cluster" tabindex="0">cluster</span>
      <span class="chip" data-color="sentiment" tabindex="0">sentiment</span>
      <span class="chip" data-color="school" tabindex="0">school</span>
      <span class="chip" data-color="grade" tabindex="0">grade</span>
      <span class="chip" data-color="event" tabindex="0">event</span>
    </div>

    <div class="panel">
      <div class="panel-title">map</div>
      <div id="tm-host" style="min-height:560px"></div>
    </div>
  `;
  root.appendChild(wrap);

  populateColumns(appState);
  bindColorChips(appState);
  document.getElementById('tm-col').addEventListener('change', e => {
    STATE.columnId = e.target.value || null;
    drawMap(appState);
  });
  drawMap(appState);
}

function populateColumns(appState) {
  const sel = document.getElementById('tm-col');
  sel.innerHTML = '';
  const cols = appState.bundle.columns
    .filter(c => c.inferred_type === 'freetext')
    .filter(c => (appState.freetextByColumn.get(c.id)?.length ?? 0) >= MIN_ITEMS);
  cols.sort((a, b) =>
    appState.freetextByColumn.get(b.id).length - appState.freetextByColumn.get(a.id).length
  );
  for (const c of cols) {
    const sheet = appState.sheetById.get(c.sheet_id);
    const o = document.createElement('option');
    o.value = c.id;
    const n = appState.freetextByColumn.get(c.id).length;
    o.textContent = `[${sheet?.period_label ?? c.sheet_id}] ${c.original_header.slice(0, 60)} (n=${n})`;
    if (c.id === STATE.columnId) o.selected = true;
    sel.appendChild(o);
  }
  if (!STATE.columnId && cols.length > 0) {
    // Prefer "what did you learn" RTU column
    const preferred = cols.find(c =>
      c.original_header.toLowerCase().includes('what did you learn') &&
      appState.sheetById.get(c.sheet_id)?.workbook_id === 'rtu_2025_26'
    );
    STATE.columnId = (preferred ?? cols[0]).id;
    sel.value = STATE.columnId;
  }
}

function bindColorChips(appState) {
  document.querySelectorAll('[data-color]').forEach(el => {
    el.classList.toggle('active', el.dataset.color === STATE.colorBy);
    el.classList.toggle('muted', el.dataset.color !== STATE.colorBy);
    el.addEventListener('click', () => {
      STATE.colorBy = el.dataset.color;
      bindColorChips(appState);
      recolor(appState);
    });
  });
}

function drawMap(appState) {
  const host = document.getElementById('tm-host');
  host.innerHTML = '';
  if (!STATE.columnId) {
    host.innerHTML = `<div class="empty-state">No free-text columns with ≥${MIN_ITEMS} items.</div>`;
    return;
  }
  const items = (appState.freetextByColumn.get(STATE.columnId) || [])
    .filter(ft => ft.coords_2d != null);
  if (items.length < MIN_ITEMS) {
    host.innerHTML = `<div class="empty-state">Not enough free-text responses to build a theme map for this column.</div>`;
    return;
  }
  const clusters = (appState.themeClustersByColumn.get(STATE.columnId) || []);

  const W = 940, H = 560;
  const margin = { top: 12, right: 12, bottom: 12, left: 12 };
  const innerW = W - margin.left - margin.right;
  const innerH = H - margin.top - margin.bottom;
  const xs = items.map(i => i.coords_2d[0]);
  const ys = items.map(i => i.coords_2d[1]);
  const x = d3.scaleLinear().domain([d3.min(xs), d3.max(xs)]).range([0, innerW]).nice();
  const y = d3.scaleLinear().domain([d3.min(ys), d3.max(ys)]).range([innerH, 0]).nice();

  const svg = d3.select(host).append('svg')
    .attr('viewBox', `0 0 ${W} ${H}`).style('width', '100%').style('height', H + 'px');
  const g = svg.append('g').attr('transform', `translate(${margin.left}, ${margin.top})`);

  // Dots
  g.append('g').attr('class', 'dots')
    .selectAll('circle').data(items).enter().append('circle')
    .attr('cx', d => x(d.coords_2d[0]))
    .attr('cy', d => y(d.coords_2d[1]))
    .attr('r', 3.5)
    .attr('fill-opacity', 0.7)
    .attr('fill', d => colorForDot(d, appState))
    .style('cursor', 'pointer')
    .on('mouseover', function (e, d) { showTip(e, d, appState); })
    .on('mouseout', hideTip)
    .on('click', (e, d) => showItem(d, appState));

  // Cluster labels
  g.append('g').attr('class', 'labels')
    .selectAll('g').data(clusters).enter().append('g')
    .attr('transform', d => `translate(${x(d.centroid_2d[0])}, ${y(d.centroid_2d[1])})`)
    .style('cursor', 'pointer')
    .on('click', (e, d) => showCluster(d, appState))
    .each(function (d) {
      d3.select(this).append('rect')
        .attr('x', -d.label.length * 3.4 - 6).attr('y', -10)
        .attr('width', d.label.length * 6.8 + 12).attr('height', 20)
        .attr('rx', 4)
        .attr('fill', 'rgba(0,53,30,0.85)');
      d3.select(this).append('text')
        .attr('text-anchor', 'middle').attr('dy', 4)
        .style('font-family', 'var(--font-mono)')
        .style('font-size', '11px')
        .style('fill', 'white')
        .text(d.label);
    });
}

function recolor(appState) {
  const items = (appState.freetextByColumn.get(STATE.columnId) || []).filter(ft => ft.coords_2d != null);
  d3.select('#tm-host svg .dots').selectAll('circle')
    .data(items)
    .attr('fill', d => colorForDot(d, appState));
}

function colorForDot(ft, appState) {
  const cat = appState.bundle.palette.categorical;
  if (STATE.colorBy === 'cluster') {
    if (ft.cluster_id.endsWith('uncategorized')) return '#bbb';
    const m = ft.cluster_id.match(/cluster_(\d+)/);
    const idx = m ? parseInt(m[1]) % cat.length : 0;
    return cat[idx];
  }
  if (STATE.colorBy === 'sentiment') {
    return d3.interpolateRgb('#a86b6b', '#00351e')(0.5 + ft.sentiment_score / 2);
  }
  const resp = appState.responseById.get(ft.response_id);
  if (!resp) return '#999';
  let key;
  if (STATE.colorBy === 'school') key = resp.school;
  else if (STATE.colorBy === 'grade') key = resp.grade_level || 'unknown';
  else if (STATE.colorBy === 'event') {
    const sheet = appState.sheetById.get(resp.sheet_id);
    const ev = appState.bundle.events.find(e => e.sheet_id === sheet?.id);
    key = ev?.id || 'none';
  } else if (STATE.colorBy === 'year') {
    const sheet = appState.sheetById.get(resp.sheet_id);
    key = String(sheet?.period ?? 'none');
  }
  // Stable hash → palette index
  let h = 0;
  for (let i = 0; i < key.length; i++) h = (h * 31 + key.charCodeAt(i)) >>> 0;
  return cat[h % cat.length];
}

let _tipEl = null;
function showTip(e, ft, appState) {
  if (!_tipEl) {
    _tipEl = document.createElement('div');
    _tipEl.className = 'tooltip';
    document.body.appendChild(_tipEl);
  }
  const resp = appState.responseById.get(ft.response_id);
  _tipEl.innerHTML = `
    <div class="question">${escapeHTML(ft.text.slice(0, 240))}${ft.text.length > 240 ? '…' : ''}</div>
    <div style="margin-top:6px">${escapeHTML(resp?.school ?? '')} · grade ${escapeHTML(resp?.grade_level ?? '?')} · sentiment ${ft.sentiment_score.toFixed(2)}</div>
  `;
  _tipEl.style.left = (e.pageX + 12) + 'px';
  _tipEl.style.top = (e.pageY + 12) + 'px';
  _tipEl.classList.add('show');
}
function hideTip() { _tipEl?.classList.remove('show'); }

function showItem(ft, appState) {
  const resp = appState.responseById.get(ft.response_id);
  const html = `
    <h3>Response detail</h3>
    <div class="question">${escapeHTML(ft.text)}</div>
    <div class="stat-row"><span class="k">school</span><span class="v">${escapeHTML(resp?.school ?? '')}</span></div>
    <div class="stat-row"><span class="k">grade</span><span class="v">${escapeHTML(resp?.grade_level ?? '?')}</span></div>
    <div class="stat-row"><span class="k">sentiment</span><span class="v">${ft.sentiment_score.toFixed(2)} (${ft.sentiment_label})</span></div>
    <div class="stat-row"><span class="k">cluster</span><span class="v">${escapeHTML(ft.cluster_id)}</span></div>
  `;
  openSidePanel(html);
}

function showCluster(cluster, appState) {
  const items = (appState.freetextByColumn.get(STATE.columnId) || [])
    .filter(ft => ft.cluster_id === cluster.id);
  const cards = items.slice(0, 30).map(ft => {
    const resp = appState.responseById.get(ft.response_id);
    return `<div style="border-left:3px solid var(--cat-3);padding:8px 10px;margin:6px 0;background:var(--seq-1)">
      <div style="font-family:var(--font-serif)">${escapeHTML(ft.text.slice(0, 280))}${ft.text.length > 280 ? '…' : ''}</div>
      <div style="font-family:var(--font-mono);font-size:11px;color:var(--ink-soft);margin-top:4px">${escapeHTML(resp?.school ?? '')} · grade ${escapeHTML(resp?.grade_level ?? '?')} · sentiment ${ft.sentiment_score.toFixed(2)}</div>
    </div>`;
  }).join('');
  openSidePanel(`
    <h3>${escapeHTML(cluster.label)}</h3>
    <div class="question">${escapeHTML(cluster.description)}</div>
    <div class="stat-row"><span class="k">members</span><span class="v">${cluster.member_count}</span></div>
    <div class="stat-row"><span class="k">naming</span><span class="v">${escapeHTML(cluster.naming_method)}</span></div>
    <h3 style="margin-top:18px;font-size:14px">Members (showing first ${Math.min(30, items.length)})</h3>
    ${cards}
  `);
}
