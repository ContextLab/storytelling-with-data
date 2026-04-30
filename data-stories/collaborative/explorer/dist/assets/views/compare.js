// T035-T037: Compare view — pick a measure, pick schools, split by school/grade/year.
// Uses D3 grouped bars with N labels per group; export PNG + JSON caption.

import { escapeHTML } from '../app.js';
import { exportSvgPng } from '../util/export.js';

const STATE = {
  measureId: null,
  schools: new Set(),
  splitBy: 'school',  // 'school' | 'grade' | 'year'
};

export function renderCompare(root, appState) {
  const wrap = document.createElement('div');
  wrap.innerHTML = `
    <h1>Compare measures across schools</h1>
    <p class="lede">Pick a measure and one or more schools, then split by school, grade, or year.</p>

    <div class="panel">
      <div class="panel-title">measure</div>
      <input type="search" id="cmp-search" placeholder="search by question text…" style="width:100%" />
      <div id="cmp-measure-list" style="max-height:200px;overflow:auto;margin-top:8px"></div>
    </div>

    <div class="panel">
      <div class="panel-title">schools</div>
      <div id="cmp-schools" style="line-height:2"></div>
    </div>

    <div class="panel">
      <div class="panel-title">split by</div>
      <span class="chip" data-split="school" tabindex="0">school</span>
      <span class="chip" data-split="grade" tabindex="0">grade</span>
      <span class="chip" data-split="year" tabindex="0">year</span>
    </div>

    <div class="panel">
      <div class="panel-title">chart</div>
      <div id="cmp-chart-host" style="min-height:340px"></div>
      <div style="margin-top:10px;text-align:right">
        <button id="cmp-export" type="button">export PNG + caption</button>
      </div>
    </div>
  `;
  root.appendChild(wrap);

  populateMeasureList(appState);
  populateSchools(appState);
  bindSplitChips(appState);
  document.getElementById('cmp-search').addEventListener('input', () => populateMeasureList(appState));
  document.getElementById('cmp-export').addEventListener('click', () => doExport(appState));
  drawChart(appState);
}

function populateMeasureList(appState) {
  const q = (document.getElementById('cmp-search')?.value || '').toLowerCase();
  const list = document.getElementById('cmp-measure-list');
  list.innerHTML = '';
  const measures = appState.bundle.measures
    .filter(m => m.value_scale_canonical !== 'free')
    .filter(m => !q || m.display_name.toLowerCase().includes(q) || m.description.toLowerCase().includes(q));
  for (const m of measures) {
    const item = document.createElement('div');
    item.className = 'chip ' + (m.id === STATE.measureId ? 'active' : 'muted');
    item.style.display = 'block';
    item.style.maxWidth = '100%';
    item.style.whiteSpace = 'nowrap';
    item.style.overflow = 'hidden';
    item.style.textOverflow = 'ellipsis';
    item.tabIndex = 0;
    item.title = m.description;
    item.textContent = `${m.display_name}  ·  ${m.coverage_workbooks.join(',')}  ·  ${m.coverage_years.join(',') || 'event series'}`;
    item.addEventListener('click', () => {
      STATE.measureId = m.id;
      populateMeasureList(appState);
      drawChart(appState);
    });
    list.appendChild(item);
  }
  if (measures.length === 0) {
    list.innerHTML = '<div class="empty-state">No measures match.</div>';
  }
}

function populateSchools(appState) {
  const box = document.getElementById('cmp-schools');
  box.innerHTML = '';
  const schoolIds = [...new Set(appState.bundle.responses.map(r => r.school))].sort();
  for (const sid of schoolIds) {
    const sch = appState.schoolById.get(sid);
    const chip = document.createElement('span');
    chip.className = 'chip muted';
    chip.tabIndex = 0;
    chip.textContent = sch?.display_name ?? sid;
    chip.addEventListener('click', () => {
      if (STATE.schools.has(sid)) {
        STATE.schools.delete(sid);
        chip.classList.remove('active'); chip.classList.add('muted');
      } else {
        STATE.schools.add(sid);
        chip.classList.add('active'); chip.classList.remove('muted');
      }
      drawChart(appState);
    });
    box.appendChild(chip);
  }
}

function bindSplitChips(appState) {
  document.querySelectorAll('[data-split]').forEach(el => {
    if (el.dataset.split === STATE.splitBy) {
      el.classList.add('active'); el.classList.remove('muted');
    } else {
      el.classList.add('muted'); el.classList.remove('active');
    }
    el.addEventListener('click', () => {
      STATE.splitBy = el.dataset.split;
      bindSplitChips(appState);
      drawChart(appState);
    });
  });
}

function drawChart(appState) {
  const host = document.getElementById('cmp-chart-host');
  if (!host) return;
  host.innerHTML = '';

  if (!STATE.measureId) {
    host.innerHTML = '<div class="empty-state">Pick a measure above to draw a chart.</div>';
    return;
  }
  const m = appState.measureById.get(STATE.measureId);
  if (!m) return;
  const colIds = m.aliases.map(a => a.column_id);

  // Aggregate: group_value → series_value → values list
  // group = e.g. school name; series = ordinal/categorical answer levels
  const groups = new Map();  // groupKey -> Map(level -> count)
  const groupKeys = [];

  let n_total = 0;
  for (const r of appState.bundle.responses) {
    if (STATE.schools.size > 0 && !STATE.schools.has(r.school)) continue;
    const groupKey = groupKeyFor(r, appState);
    if (groupKey == null) continue;
    for (const cid of colIds) {
      const v = r.values[cid];
      if (v == null) continue;
      const key = String(v);
      if (!groups.has(groupKey)) { groups.set(groupKey, new Map()); groupKeys.push(groupKey); }
      const inner = groups.get(groupKey);
      inner.set(key, (inner.get(key) || 0) + 1);
      n_total++;
    }
  }

  if (n_total === 0) {
    host.innerHTML = '<div class="empty-state">No data for this measure with the active filters. Try changing schools or split-by.</div>';
    return;
  }

  // Render grouped bars: x = group, color = answer level
  const allLevels = new Set();
  for (const inner of groups.values()) for (const k of inner.keys()) allLevels.add(k);
  const levels = [...allLevels].sort();

  const groupKeysSorted = groupKeys.slice().sort();
  const categorical = appState.bundle.palette.categorical;

  const margin = { top: 20, right: 20, bottom: 80, left: 60 };
  const W = 880, H = 420;
  const innerW = W - margin.left - margin.right;
  const innerH = H - margin.top - margin.bottom;

  const x0 = d3.scaleBand().domain(groupKeysSorted).range([0, innerW]).padding(0.2);
  const x1 = d3.scaleBand().domain(levels).range([0, x0.bandwidth()]).padding(0.05);
  const yMax = d3.max([...groups.values()].flatMap(inner => [...inner.values()])) || 1;
  const y = d3.scaleLinear().domain([0, yMax]).range([innerH, 0]).nice();
  const color = d3.scaleOrdinal().domain(levels).range(levels.map((_, i) => categorical[i % categorical.length]));

  const svg = d3.select(host).append('svg')
    .attr('viewBox', `0 0 ${W} ${H}`)
    .attr('preserveAspectRatio', 'xMidYMid meet')
    .style('width', '100%').style('height', H + 'px');

  const g = svg.append('g').attr('transform', `translate(${margin.left}, ${margin.top})`);

  // Bars
  for (const gk of groupKeysSorted) {
    const inner = groups.get(gk);
    const grpG = g.append('g').attr('transform', `translate(${x0(gk)}, 0)`);
    for (const lvl of levels) {
      const c = inner.get(lvl) || 0;
      grpG.append('rect')
        .attr('x', x1(lvl)).attr('y', y(c))
        .attr('width', x1.bandwidth()).attr('height', innerH - y(c))
        .attr('fill', color(lvl))
        .append('title').text(`${gk} · ${lvl}: ${c}`);
    }
    // N label per group
    const total = [...inner.values()].reduce((a, b) => a + b, 0);
    grpG.append('text')
      .attr('x', x0.bandwidth() / 2)
      .attr('y', innerH + 14)
      .attr('text-anchor', 'middle')
      .attr('class', 'label')
      .text(`n=${total}`);
  }

  // Axes
  g.append('g').attr('class', 'axis').call(d3.axisLeft(y).ticks(6));
  g.append('g').attr('class', 'axis')
    .attr('transform', `translate(0, ${innerH})`)
    .call(d3.axisBottom(x0))
    .selectAll('text').attr('transform', 'rotate(-30)').style('text-anchor', 'end');

  // Title
  g.append('text').attr('x', 0).attr('y', -6).attr('class', 'label').text(m.display_name);

  // Legend
  const legend = svg.append('g').attr('transform', `translate(${margin.left}, ${H - 16})`);
  let lx = 0;
  for (const lvl of levels) {
    const grp = legend.append('g').attr('transform', `translate(${lx}, 0)`);
    grp.append('rect').attr('width', 10).attr('height', 10).attr('fill', color(lvl));
    grp.append('text').attr('x', 14).attr('y', 9).attr('class', 'label').text(lvl);
    lx += String(lvl).length * 7 + 28;
  }
}

function groupKeyFor(r, appState) {
  if (STATE.splitBy === 'school') {
    const sch = appState.schoolById.get(r.school);
    return sch?.display_name ?? r.school;
  }
  if (STATE.splitBy === 'grade') {
    return r.grade_level || 'unknown';
  }
  if (STATE.splitBy === 'year') {
    const sheet = appState.sheetById.get(r.sheet_id);
    if (sheet && Number.isInteger(sheet.period)) return String(sheet.period);
    return null;
  }
  return null;
}

function doExport(appState) {
  const svg = document.querySelector('#cmp-chart-host svg');
  if (!svg) return;
  const m = appState.measureById.get(STATE.measureId);
  exportSvgPng(svg, `compare_${STATE.measureId}_by_${STATE.splitBy}`, {
    view: 'compare',
    measure_id: STATE.measureId,
    measure_display_name: m?.display_name,
    filters: {
      schools: [...STATE.schools],
      split_by: STATE.splitBy,
    },
    generated_at: new Date().toISOString(),
  });
}
