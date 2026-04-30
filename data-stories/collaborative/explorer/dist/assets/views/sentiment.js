// T055-T057: Sentiment view — pick a free-text column, group by event/school/grade/year,
// drill into representative responses (most positive, most negative, median).

import { escapeHTML, openSidePanel } from '../app.js';
import { exportSvgPng } from '../util/export.js';

const STATE = {
  columnId: null,
  groupBy: 'event',  // 'event' | 'school' | 'grade' | 'year' | 'ungrouped'
};

export function renderSentiment(root, appState) {
  const wrap = document.createElement('div');
  wrap.innerHTML = `
    <h1>Sentiment of free responses</h1>
    <p class="lede">Aggregate sentiment scored locally for every non-empty free-text answer. Click a bar to drill into representative responses.</p>

    <div class="panel">
      <div class="panel-title">free-text column</div>
      <select id="sn-col"></select>
    </div>

    <div class="panel">
      <div class="panel-title">group by</div>
      <span class="chip" data-grp="event" tabindex="0">event</span>
      <span class="chip" data-grp="school" tabindex="0">school</span>
      <span class="chip" data-grp="grade" tabindex="0">grade</span>
      <span class="chip" data-grp="year" tabindex="0">year</span>
      <span class="chip" data-grp="ungrouped" tabindex="0">ungrouped</span>
    </div>

    <div class="panel">
      <div class="panel-title">chart</div>
      <div id="sn-chart-host" style="min-height:340px"></div>
      <div style="text-align:right;margin-top:10px">
        <button id="sn-export" type="button">export PNG + caption</button>
      </div>
    </div>
  `;
  root.appendChild(wrap);

  populateColumns(appState);
  bindGroupChips(appState);
  document.getElementById('sn-col').addEventListener('change', e => {
    STATE.columnId = e.target.value || null;
    drawChart(appState);
  });
  document.getElementById('sn-export').addEventListener('click', () => doExport());
  drawChart(appState);
}

function populateColumns(appState) {
  const sel = document.getElementById('sn-col');
  sel.innerHTML = '<option value="">— pick a column —</option>';
  const cols = appState.bundle.columns
    .filter(c => c.inferred_type === 'freetext')
    .filter(c => (appState.freetextByColumn.get(c.id)?.length ?? 0) > 0);
  // Sort by item count desc
  cols.sort((a, b) => (appState.freetextByColumn.get(b.id).length) - (appState.freetextByColumn.get(a.id).length));
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
    // Prefer an RTU "what did you learn" column so default 'event' grouping has data
    const preferred = cols.find(c =>
      c.original_header.toLowerCase().includes('what did you learn') &&
      appState.sheetById.get(c.sheet_id)?.workbook_id === 'rtu_2025_26'
    );
    STATE.columnId = (preferred ?? cols[0]).id;
    sel.value = STATE.columnId;
  }
}

function bindGroupChips(appState) {
  document.querySelectorAll('[data-grp]').forEach(el => {
    el.classList.toggle('active', el.dataset.grp === STATE.groupBy);
    el.classList.toggle('muted', el.dataset.grp !== STATE.groupBy);
    el.addEventListener('click', () => {
      STATE.groupBy = el.dataset.grp;
      bindGroupChips(appState);
      drawChart(appState);
    });
  });
}

function drawChart(appState) {
  const host = document.getElementById('sn-chart-host');
  host.innerHTML = '';
  if (!STATE.columnId) {
    host.innerHTML = '<div class="empty-state">Pick a column above.</div>';
    return;
  }
  const items = appState.freetextByColumn.get(STATE.columnId) || [];
  if (items.length === 0) {
    host.innerHTML = '<div class="empty-state">No items in this column.</div>';
    return;
  }

  // Group by chosen dimension
  const buckets = new Map();
  for (const ft of items) {
    const resp = appState.responseById.get(ft.response_id);
    if (!resp) continue;
    const key = groupKey(resp, appState);
    if (key == null) continue;
    if (!buckets.has(key)) buckets.set(key, []);
    buckets.get(key).push(ft);
  }
  const rows = [...buckets.entries()].map(([k, arr]) => ({
    key: k,
    n: arr.length,
    mean: arr.reduce((a, b) => a + b.sentiment_score, 0) / arr.length,
    items: arr,
  }));
  // Sort
  if (STATE.groupBy === 'event') {
    const order = appState.bundle.events.map(e => e.display_name);
    rows.sort((a, b) => order.indexOf(a.key) - order.indexOf(b.key));
  } else if (STATE.groupBy === 'year') {
    rows.sort((a, b) => Number(a.key) - Number(b.key));
  } else {
    rows.sort((a, b) => a.key.localeCompare(b.key));
  }

  const margin = { top: 16, right: 16, bottom: 64, left: 60 };
  const W = 880, H = 360;
  const innerW = W - margin.left - margin.right;
  const innerH = H - margin.top - margin.bottom;

  const svg = d3.select(host).append('svg')
    .attr('viewBox', `0 0 ${W} ${H}`).style('width', '100%').style('height', H + 'px');
  const g = svg.append('g').attr('transform', `translate(${margin.left}, ${margin.top})`);

  const x = d3.scaleBand().domain(rows.map(r => r.key)).range([0, innerW]).padding(0.3);
  const y = d3.scaleLinear().domain([-1, 1]).range([innerH, 0]);

  // Zero line
  g.append('line').attr('x1', 0).attr('x2', innerW).attr('y1', y(0)).attr('y2', y(0))
    .attr('stroke', 'var(--border)').attr('stroke-dasharray', '3 3');

  g.append('g').attr('class', 'axis').call(d3.axisLeft(y).ticks(5).tickFormat(d3.format('+.1f')));
  g.append('g').attr('class', 'axis').attr('transform', `translate(0, ${innerH})`)
    .call(d3.axisBottom(x))
    .selectAll('text').attr('transform', 'rotate(-25)').style('text-anchor', 'end');

  for (const r of rows) {
    const yPos = y(r.mean);
    const ybase = y(0);
    const positive = r.mean >= 0;
    g.append('rect')
      .attr('x', x(r.key)).attr('y', Math.min(yPos, ybase))
      .attr('width', x.bandwidth()).attr('height', Math.abs(ybase - yPos))
      .attr('fill', positive ? 'var(--cat-3)' : 'var(--div-1)')
      .style('cursor', 'pointer')
      .on('click', () => showDrill(appState, r));
    g.append('text')
      .attr('x', x(r.key) + x.bandwidth() / 2)
      .attr('y', yPos + (positive ? -4 : 14))
      .attr('text-anchor', 'middle')
      .attr('class', 'label')
      .text(`n=${r.n}`);
  }

  // Footnote
  svg.append('text').attr('class', 'footnote').attr('x', margin.left).attr('y', H - 6)
    .text('Click any bar to see most-positive, most-negative, and median responses.');
}

function groupKey(resp, appState) {
  if (STATE.groupBy === 'event') {
    const sheet = appState.sheetById.get(resp.sheet_id);
    if (!sheet) return null;
    const ev = appState.bundle.events.find(e => e.sheet_id === sheet.id);
    return ev?.display_name ?? null;
  }
  if (STATE.groupBy === 'school') {
    const s = appState.schoolById.get(resp.school);
    return s?.display_name ?? resp.school;
  }
  if (STATE.groupBy === 'grade') return resp.grade_level || 'unknown';
  if (STATE.groupBy === 'year') {
    const sheet = appState.sheetById.get(resp.sheet_id);
    return sheet && Number.isInteger(sheet.period) ? String(sheet.period) : null;
  }
  return 'all';
}

function showDrill(appState, row) {
  const sorted = row.items.slice().sort((a, b) => a.sentiment_score - b.sentiment_score);
  const min = sorted[0];
  const max = sorted[sorted.length - 1];
  const med = sorted[Math.floor(sorted.length / 2)];
  const card = (label, ft) => `
    <div style="border-left:3px solid var(--cat-3);padding:8px 10px;margin:8px 0;background:var(--seq-1);">
      <div class="panel-title">${label} · score ${ft.sentiment_score.toFixed(2)} (${ft.sentiment_label})</div>
      <div style="font-family:var(--font-serif)">${escapeHTML(ft.text)}</div>
      <div style="font-family:var(--font-mono);font-size:10px;color:var(--ink-soft);margin-top:4px">${escapeHTML(ft.response_id)}</div>
    </div>`;
  const html = `
    <h3>${escapeHTML(row.key)}</h3>
    <div class="question">${row.n} responses · mean sentiment ${row.mean.toFixed(2)}</div>
    ${card('Most positive', max)}
    ${card('Median', med)}
    ${card('Most negative', min)}
  `;
  openSidePanel(html);
}

function doExport() {
  const svg = document.querySelector('#sn-chart-host svg');
  if (!svg) return;
  exportSvgPng(svg, `sentiment_${STATE.columnId}_by_${STATE.groupBy}`, {
    view: 'sentiment',
    column_id: STATE.columnId,
    group_by: STATE.groupBy,
    generated_at: new Date().toISOString(),
  });
}
