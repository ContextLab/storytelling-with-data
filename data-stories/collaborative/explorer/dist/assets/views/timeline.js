// T040-T042: Timeline view — multi-measure overlay or small multiples;
// x-axis = years (Core Measures) or events (RTU); gaps for missing periods.

import { escapeHTML } from '../app.js';
import { exportSvgPng } from '../util/export.js';

const STATE = {
  measureIds: new Set(),
  axis: 'year',     // 'year' | 'event'
  layout: 'overlay', // 'overlay' | 'small-multiples'
};

export function renderTimeline(root, appState) {
  const wrap = document.createElement('div');
  wrap.innerHTML = `
    <h1>Timelines of selected measures</h1>
    <p class="lede">Multi-measure overlay across years (2022–2025) or RTU event sequence. Gaps where data is missing — never zero-filled.</p>

    <div class="panel">
      <div class="panel-title">x axis</div>
      <span class="chip" data-axis="year" tabindex="0">by year</span>
      <span class="chip" data-axis="event" tabindex="0">by event</span>

      <span style="margin-left:24px"></span>
      <span class="chip" data-layout="overlay" tabindex="0">overlay</span>
      <span class="chip" data-layout="small-multiples" tabindex="0">small multiples</span>
    </div>

    <div class="panel">
      <div class="panel-title">measures</div>
      <div id="tl-measures" style="max-height:200px;overflow:auto"></div>
    </div>

    <div class="panel">
      <div class="panel-title">chart</div>
      <div id="tl-chart-host" style="min-height:380px"></div>
      <div style="text-align:right;margin-top:10px">
        <button id="tl-export" type="button">export PNG + caption</button>
      </div>
    </div>
  `;
  root.appendChild(wrap);

  bindAxisLayoutChips(appState);
  populateMeasures(appState);
  document.getElementById('tl-export').addEventListener('click', () => doExport(appState));
  drawChart(appState);
}

function bindAxisLayoutChips(appState) {
  document.querySelectorAll('[data-axis]').forEach(el => {
    el.classList.toggle('active', el.dataset.axis === STATE.axis);
    el.classList.toggle('muted', el.dataset.axis !== STATE.axis);
    el.addEventListener('click', () => {
      STATE.axis = el.dataset.axis;
      bindAxisLayoutChips(appState);
      populateMeasures(appState);
      drawChart(appState);
    });
  });
  document.querySelectorAll('[data-layout]').forEach(el => {
    el.classList.toggle('active', el.dataset.layout === STATE.layout);
    el.classList.toggle('muted', el.dataset.layout !== STATE.layout);
    el.addEventListener('click', () => {
      STATE.layout = el.dataset.layout;
      bindAxisLayoutChips(appState);
      drawChart(appState);
    });
  });
}

function populateMeasures(appState) {
  const list = document.getElementById('tl-measures');
  list.innerHTML = '';
  // Filter measures that have data for the chosen axis
  const measures = appState.bundle.measures.filter(m => {
    if (m.value_scale_canonical === 'free') return false;
    if (STATE.axis === 'year') return m.coverage_years && m.coverage_years.length >= 2;
    if (STATE.axis === 'event') return m.coverage_workbooks.includes('rtu_2025_26');
    return true;
  });
  for (const m of measures) {
    const chip = document.createElement('span');
    chip.className = 'chip ' + (STATE.measureIds.has(m.id) ? 'active' : 'muted');
    chip.tabIndex = 0;
    chip.style.display = 'inline-block';
    chip.style.margin = '3px';
    chip.title = m.description;
    chip.textContent = m.display_name;
    chip.addEventListener('click', () => {
      if (STATE.measureIds.has(m.id)) STATE.measureIds.delete(m.id);
      else STATE.measureIds.add(m.id);
      populateMeasures(appState);
      drawChart(appState);
    });
    list.appendChild(chip);
  }
  if (measures.length === 0) {
    list.innerHTML = '<div class="empty-state">No measures available for this axis.</div>';
  }
}

function drawChart(appState) {
  const host = document.getElementById('tl-chart-host');
  if (!host) return;
  host.innerHTML = '';
  if (STATE.measureIds.size === 0) {
    host.innerHTML = '<div class="empty-state">Pick one or more measures to plot.</div>';
    return;
  }

  const measures = [...STATE.measureIds].map(id => appState.measureById.get(id)).filter(Boolean);

  // x-axis points
  let xPoints = [];
  if (STATE.axis === 'year') xPoints = [2022, 2023, 2024, 2025];
  else xPoints = appState.bundle.events.map(e => e.id);

  // Aggregate per-measure per-x mean of (treating yes/agree as 1, else 0)
  const series = new Map();  // measure_id -> [{x, mean, n}]
  for (const m of measures) {
    const points = [];
    for (const x of xPoints) {
      const vals = collectValues(appState, m, x);
      if (vals.length === 0) {
        points.push({ x, mean: null, n: 0 });
      } else {
        const mean = vals.reduce((a, b) => a + b, 0) / vals.length;
        points.push({ x, mean, n: vals.length });
      }
    }
    series.set(m.id, points);
  }

  if (STATE.layout === 'overlay') drawOverlay(host, measures, series, xPoints, appState);
  else drawSmallMultiples(host, measures, series, xPoints, appState);
}

function collectValues(appState, measure, xKey) {
  const colIds = new Set(measure.aliases.map(a => a.column_id));
  const out = [];
  for (const r of appState.bundle.responses) {
    const sheet = appState.sheetById.get(r.sheet_id);
    if (!sheet) continue;
    if (STATE.axis === 'year') {
      if (sheet.period !== xKey) continue;
    } else {
      // event axis
      if (!appState.bundle.events.some(e => e.sheet_id === sheet.id && e.id === xKey)) continue;
    }
    for (const cid of colIds) {
      if (!sheet.column_ids.includes(cid)) continue;
      const v = r.values[cid];
      if (v == null) continue;
      out.push(positiveScore(v));
    }
  }
  return out;
}

function positiveScore(v) {
  // Map common Likert / yes-no answers to 0..1
  const s = String(v).toLowerCase();
  if (/strongly agree|always|great risk|very wrong|yes\b/.test(s)) return 1;
  if (/agree|often|moderate risk|wrong/.test(s)) return 0.75;
  if (/neither|sometimes|slight risk/.test(s)) return 0.5;
  if (/disagree|rarely|no risk|not wrong/.test(s)) return 0.25;
  if (/strongly disagree|never|no\b/.test(s)) return 0;
  // Numeric fallback
  const n = Number(v);
  if (Number.isFinite(n)) return Math.max(0, Math.min(1, n / 5));
  return 0.5;
}

function drawOverlay(host, measures, series, xPoints, appState) {
  const margin = { top: 24, right: 20, bottom: 60, left: 50 };
  const W = 880, H = 380;
  const innerW = W - margin.left - margin.right;
  const innerH = H - margin.top - margin.bottom;

  const svg = d3.select(host).append('svg')
    .attr('viewBox', `0 0 ${W} ${H}`)
    .style('width', '100%').style('height', H + 'px');
  const g = svg.append('g').attr('transform', `translate(${margin.left}, ${margin.top})`);

  const x = STATE.axis === 'year'
    ? d3.scalePoint().domain(xPoints.map(String)).range([0, innerW])
    : d3.scalePoint().domain(xPoints).range([0, innerW]);
  const y = d3.scaleLinear().domain([0, 1]).range([innerH, 0]);
  const cat = appState.bundle.palette.categorical;

  g.append('g').attr('class', 'axis').attr('transform', `translate(0, ${innerH})`)
    .call(d3.axisBottom(x).tickFormat(d => formatX(d, appState)));
  g.append('g').attr('class', 'axis').call(d3.axisLeft(y).ticks(5).tickFormat(d3.format('.0%')));

  // Gridlines
  for (let t = 0; t <= 1; t += 0.25) {
    g.append('line').attr('class', 'gridline')
      .attr('x1', 0).attr('x2', innerW).attr('y1', y(t)).attr('y2', y(t));
  }

  let i = 0;
  for (const m of measures) {
    const pts = series.get(m.id);
    const color = cat[i % cat.length];
    i++;
    // Break the line into segments where y is non-null (gaps for missing data)
    const segments = [];
    let cur = [];
    for (const p of pts) {
      if (p.mean == null) { if (cur.length) segments.push(cur); cur = []; }
      else cur.push(p);
    }
    if (cur.length) segments.push(cur);

    const line = d3.line()
      .x(p => x(STATE.axis === 'year' ? String(p.x) : p.x))
      .y(p => y(p.mean));

    for (const seg of segments) {
      g.append('path')
        .datum(seg)
        .attr('fill', 'none')
        .attr('stroke', color)
        .attr('stroke-width', 2)
        .attr('d', line);
    }
    // Dots + n labels
    g.selectAll(`.pt-${i}`).data(pts.filter(p => p.mean != null))
      .enter().append('circle')
      .attr('cx', p => x(STATE.axis === 'year' ? String(p.x) : p.x))
      .attr('cy', p => y(p.mean))
      .attr('r', 3)
      .attr('fill', color)
      .append('title').text(p => `${m.display_name} @ ${formatX(p.x, appState)}: ${(p.mean*100).toFixed(0)}% (n=${p.n})`);
  }

  // Footnote about gaps
  const hasGap = measures.some(m => series.get(m.id).some(p => p.mean == null));
  if (hasGap) {
    svg.append('text').attr('class', 'footnote')
      .attr('x', margin.left).attr('y', H - 12)
      .text('Breaks indicate periods with no data — never interpolated or zero-filled.');
  }

  // Legend
  const legend = svg.append('g').attr('transform', `translate(${margin.left}, ${margin.top - 14})`);
  let lx = 0;
  let i2 = 0;
  for (const m of measures) {
    const color = cat[i2 % cat.length]; i2++;
    const grp = legend.append('g').attr('transform', `translate(${lx}, 0)`);
    grp.append('line').attr('x1', 0).attr('x2', 14).attr('y1', 4).attr('y2', 4)
      .attr('stroke', color).attr('stroke-width', 2);
    grp.append('text').attr('x', 18).attr('y', 7).attr('class', 'label').text(m.display_name);
    lx += m.display_name.length * 6 + 40;
  }
}

function drawSmallMultiples(host, measures, series, xPoints, appState) {
  for (const m of measures) {
    const card = document.createElement('div');
    card.className = 'panel';
    card.style.padding = '10px';
    card.style.marginBottom = '12px';
    card.innerHTML = `<div class="panel-title">${escapeHTML(m.display_name)}</div>`;
    host.appendChild(card);

    const pts = series.get(m.id);
    const margin = { top: 6, right: 12, bottom: 28, left: 36 };
    const W = 760, H = 160;
    const innerW = W - margin.left - margin.right;
    const innerH = H - margin.top - margin.bottom;

    const svg = d3.select(card).append('svg')
      .attr('viewBox', `0 0 ${W} ${H}`).style('width', '100%').style('height', H + 'px');
    const g = svg.append('g').attr('transform', `translate(${margin.left}, ${margin.top})`);

    const x = STATE.axis === 'year'
      ? d3.scalePoint().domain(xPoints.map(String)).range([0, innerW])
      : d3.scalePoint().domain(xPoints).range([0, innerW]);
    const y = d3.scaleLinear().domain([0, 1]).range([innerH, 0]);
    g.append('g').attr('class', 'axis').attr('transform', `translate(0, ${innerH})`)
      .call(d3.axisBottom(x).tickFormat(d => formatX(d, appState)));
    g.append('g').attr('class', 'axis').call(d3.axisLeft(y).ticks(3).tickFormat(d3.format('.0%')));

    const segments = [];
    let cur = [];
    for (const p of pts) { if (p.mean == null) { if (cur.length) segments.push(cur); cur = []; } else cur.push(p); }
    if (cur.length) segments.push(cur);

    const line = d3.line()
      .x(p => x(STATE.axis === 'year' ? String(p.x) : p.x))
      .y(p => y(p.mean));
    for (const seg of segments) {
      g.append('path').datum(seg).attr('fill', 'none').attr('stroke', 'var(--dartmouth-green)').attr('stroke-width', 2).attr('d', line);
    }
    g.selectAll('circle').data(pts.filter(p => p.mean != null)).enter().append('circle')
      .attr('cx', p => x(STATE.axis === 'year' ? String(p.x) : p.x))
      .attr('cy', p => y(p.mean)).attr('r', 3).attr('fill', 'var(--dartmouth-green)');
  }
}

function formatX(d, appState) {
  if (STATE.axis === 'year') return String(d);
  const ev = appState.bundle.events.find(e => e.id === d);
  return ev?.display_name ?? String(d);
}

function doExport(appState) {
  const svg = document.querySelector('#tl-chart-host svg');
  if (!svg) return;
  exportSvgPng(svg, `timeline_${[...STATE.measureIds].join('-')}_${STATE.axis}`, {
    view: 'timeline',
    measure_ids: [...STATE.measureIds],
    axis: STATE.axis,
    layout: STATE.layout,
    generated_at: new Date().toISOString(),
  });
}
