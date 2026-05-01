// Figure 2: For each respondent who answered the support-people checkbox AND
// the "what thoughts came up" reflection, plot:
//   x = number of unique support categories selected
//   y = sentiment score of the reflection
// Color/filter by demographics.

import { escapeHTML, openSidePanel } from '../app.js';

// Curated category prefixes — the actual checkbox option labels in the survey.
// Each cell joins selected option full descriptions with commas, BUT the
// descriptions themselves contain commas, so we count by substring presence
// of the option's distinctive prefix.
const SUPPORT_CATEGORIES = [
  { id: 'confidant',   prefix: 'A confidant',                 label: 'Confidant' },
  { id: 'airport',     prefix: 'An "airport driver"',         label: 'Airport driver' },
  { id: 'neighbors',   prefix: 'Reliable neighbors',          label: 'Reliable neighbors' },
  { id: 'hangout',     prefix: 'A hangout buddy',             label: 'Hangout buddy' },
  { id: 'advisor',     prefix: 'An advisor',                  label: 'Advisor' },
  { id: 'guide',       prefix: 'A guide',                     label: 'Guide' },
  { id: 'companion',   prefix: 'A companion',                 label: 'Companion' },
  { id: 'mentor',      prefix: 'A mentor',                    label: 'Mentor' },
  { id: 'role-model',  prefix: 'A role model',                label: 'Role model' },
  { id: 'collaborator',prefix: 'A collaborator',              label: 'Collaborator' },
  { id: 'co-worker',   prefix: 'A co-worker',                 label: 'Co-worker' },
  { id: 'family',      prefix: 'A family member',             label: 'Family member' },
  { id: 'caregiver',   prefix: 'A caregiver',                 label: 'Caregiver' },
  { id: 'protector',   prefix: 'A protector',                 label: 'Protector' },
  { id: 'sponsor',     prefix: 'A sponsor',                   label: 'Sponsor' },
  { id: 'mentee',      prefix: 'A mentee',                    label: 'Mentee' },
  { id: 'protégé',     prefix: 'A protégé',                   label: 'Protégé' },
];

const STATE = {
  colorBy: 'rtu_role',  // 'rtu_role' | 'rtu_session' | 'school' | 'grade'
  schoolFilter: new Set(),
};

function countSupportCategories(cellText) {
  if (!cellText) return 0;
  const t = String(cellText).toLowerCase();
  let n = 0;
  for (const cat of SUPPORT_CATEGORIES) {
    if (t.includes(cat.prefix.toLowerCase())) n++;
  }
  return n;
}

export function renderSupportVsSentiment(root, state) {
  root.innerHTML = '';
  // Find all (support_checkbox_col, reflection_col) pairs by sheet+session+role
  const checkCols = state.bundle.columns.filter(c =>
    c.original_header.toLowerCase().includes('check a box for each type of person')
  );
  const reflectCols = state.bundle.columns.filter(c =>
    c.original_header.toLowerCase().includes('thoughts came up')
  );
  // Index reflection cols by (sheet, rtu_session, rtu_role)
  const reflectIdx = new Map();
  for (const c of reflectCols) {
    const key = `${c.sheet_id}|${c.rtu_session ?? ''}|${c.rtu_role ?? ''}`;
    reflectIdx.set(key, c);
  }

  const pairs = [];
  for (const r of state.bundle.responses) {
    for (const checkCol of checkCols) {
      if (checkCol.sheet_id !== r.sheet_id) continue;
      const cellVal = r.values[checkCol.id];
      if (cellVal == null) continue;
      const n = countSupportCategories(cellVal);
      if (n === 0) continue;
      // Find paired reflection column
      const key = `${checkCol.sheet_id}|${checkCol.rtu_session ?? ''}|${checkCol.rtu_role ?? ''}`;
      const reflectCol = reflectIdx.get(key);
      if (!reflectCol) continue;
      // Find that response's freetext item for the reflection col
      const reflectFT = state.bundle.freetext_items.find(
        ft => ft.response_id === r.id && ft.column_id === reflectCol.id
      );
      if (!reflectFT) continue;
      pairs.push({
        x: n,
        y: reflectFT.sentiment_score,
        response: r,
        column: checkCol,
        reflectionText: reflectFT.text,
        cellVal: String(cellVal),
      });
    }
  }

  // School filter
  let visible = pairs;
  if (STATE.schoolFilter.size > 0) {
    visible = pairs.filter(p => STATE.schoolFilter.has(p.response.school));
  }

  const wrap = document.createElement('div');
  wrap.innerHTML = `
    <div class="panel">
      <div class="panel-title">about this figure</div>
      <h2 style="margin-top:0">Number of support people identified vs. reflection sentiment</h2>
      <p class="lede">For each respondent who answered both the support-people checkbox and the reflection question that follows it, the x-axis is how many distinct support categories they selected (1–${SUPPORT_CATEGORIES.length}); the y-axis is the model-scored sentiment of their reflection text.</p>
      <p class="lede" style="font-size:13px">Reflection prompt: <em>"What thoughts came up for you as you looked through those categories and thought about people who play some of those roles?"</em></p>
      <p class="lede" style="font-size:13px"><strong>n = ${visible.length} pairs</strong> (of ${pairs.length} eligible)</p>
    </div>

    <div class="panel">
      <div class="panel-title">controls</div>
      color by:
      <span class="chip" data-color="rtu_role" tabindex="0">role</span>
      <span class="chip" data-color="rtu_session" tabindex="0">session</span>
      <span class="chip" data-color="school" tabindex="0">school</span>
      <span class="chip" data-color="grade" tabindex="0">grade</span>
      <div style="margin-top:10px">
        <span style="font-family:var(--font-mono);font-size:11px;color:var(--ink-soft);text-transform:uppercase">filter to schools:</span>
        <div id="ss-school-chips" style="display:inline-block; margin-left:6px"></div>
      </div>
    </div>

    <div class="panel">
      <div class="panel-title">scatter (jittered) + per-x box plot + regression</div>
      <div id="ss-host" style="min-height:480px"></div>
      <div id="ss-stats" style="font-family:var(--font-mono);font-size:12px;color:var(--ink-soft);text-align:right;margin-top:8px"></div>
    </div>
  `;
  root.appendChild(wrap);

  document.querySelectorAll('[data-color]').forEach(el => {
    el.classList.toggle('active', el.dataset.color === STATE.colorBy);
    el.classList.toggle('muted',  el.dataset.color !== STATE.colorBy);
    el.addEventListener('click', () => { STATE.colorBy = el.dataset.color; renderSupportVsSentiment(root, state); });
  });

  const schoolBox = document.getElementById('ss-school-chips');
  const allSchools = [...new Set(pairs.map(p => p.response.school))].sort();
  for (const sid of allSchools) {
    const sch = state.schoolById.get(sid);
    const chip = document.createElement('span');
    chip.className = 'chip ' + (STATE.schoolFilter.has(sid) ? 'active' : 'muted');
    chip.tabIndex = 0;
    chip.textContent = sch?.display_name ?? sid;
    chip.addEventListener('click', () => {
      if (STATE.schoolFilter.has(sid)) STATE.schoolFilter.delete(sid);
      else STATE.schoolFilter.add(sid);
      renderSupportVsSentiment(root, state);
    });
    schoolBox.appendChild(chip);
  }

  drawScatter(visible, state);
  const stats = computeOLS(visible.map(p => p.x), visible.map(p => p.y));
  if (stats) {
    document.getElementById('ss-stats').innerHTML =
      `Pearson r = <strong>${stats.r.toFixed(3)}</strong> · slope β = <strong>${stats.slope.toFixed(3)}</strong> ` +
      `[95% CI ${stats.slopeCI[0].toFixed(3)}, ${stats.slopeCI[1].toFixed(3)}] · n = ${stats.n}`;
  }
}

function drawScatter(pairs, state) {
  const host = document.getElementById('ss-host');
  host.innerHTML = '';
  if (pairs.length === 0) {
    host.innerHTML = '<div class="empty-state">No pairs match this filter.</div>';
    return;
  }

  const W = 880, H = 480;
  const margin = { top: 20, right: 20, bottom: 60, left: 60 };
  const innerW = W - margin.left - margin.right;
  const innerH = H - margin.top - margin.bottom;

  const xMax = Math.max(...pairs.map(p => p.x));
  const x = d3.scaleLinear().domain([0, xMax + 1]).range([0, innerW]);
  const y = d3.scaleLinear().domain([-1, 1]).range([innerH, 0]);

  const svg = d3.select(host).append('svg')
    .attr('viewBox', `0 0 ${W} ${H}`).style('width', '100%').style('height', H + 'px');
  const g = svg.append('g').attr('transform', `translate(${margin.left}, ${margin.top})`);

  // Zero baseline + integer gridlines
  g.append('line').attr('x1', 0).attr('x2', innerW).attr('y1', y(0)).attr('y2', y(0))
    .attr('stroke', 'var(--border)').attr('stroke-dasharray', '2 4');
  g.append('g').attr('class', 'axis').attr('transform', `translate(0, ${innerH})`)
    .call(d3.axisBottom(x).ticks(xMax + 1).tickFormat(d3.format('d')));
  g.append('g').attr('class', 'axis').call(d3.axisLeft(y).ticks(5).tickFormat(d3.format('+.1f')));

  // Axis labels
  svg.append('text').attr('class', 'label').attr('x', margin.left + innerW / 2).attr('y', H - 18)
    .attr('text-anchor', 'middle').text('# unique support categories selected');
  svg.append('text').attr('class', 'label').attr('transform', 'rotate(-90)')
    .attr('x', -(margin.top + innerH / 2)).attr('y', 16).attr('text-anchor', 'middle')
    .text('reflection sentiment: negative ←→ positive');

  // Box plots per integer x
  const byX = new Map();
  for (const p of pairs) {
    if (!byX.has(p.x)) byX.set(p.x, []);
    byX.get(p.x).push(p.y);
  }
  for (const [xi, ys] of byX.entries()) {
    if (ys.length < 3) continue;
    const sorted = ys.slice().sort((a, b) => a - b);
    const q1 = sorted[Math.floor(sorted.length * 0.25)];
    const q2 = sorted[Math.floor(sorted.length * 0.50)];
    const q3 = sorted[Math.floor(sorted.length * 0.75)];
    const xc = x(xi);
    const halfW = Math.min(20, (innerW / (xMax + 2)) * 0.4);
    g.append('rect')
      .attr('x', xc - halfW).attr('y', y(q3))
      .attr('width', halfW * 2).attr('height', y(q1) - y(q3))
      .attr('fill', 'var(--cat-3)').attr('fill-opacity', 0.15)
      .attr('stroke', 'var(--cat-3)').attr('stroke-opacity', 0.5);
    g.append('line').attr('x1', xc - halfW).attr('x2', xc + halfW)
      .attr('y1', y(q2)).attr('y2', y(q2))
      .attr('stroke', 'var(--cat-1)').attr('stroke-width', 2);
  }

  // Color
  const cat = state.bundle.palette.categorical;
  const groupKey = (p) => groupKeyFor(p, state);
  const groups = [...new Set(pairs.map(groupKey))].sort();
  const color = d3.scaleOrdinal().domain(groups).range(groups.map((_, i) => cat[i % cat.length]));

  // Jittered dots
  const rng = mulberry32(42);
  g.append('g').selectAll('circle').data(pairs).enter().append('circle')
    .attr('cx', d => x(d.x) + (rng() - 0.5) * 14)
    .attr('cy', d => y(d.y))
    .attr('r', 4).attr('fill-opacity', 0.7)
    .attr('fill', d => color(groupKey(d)))
    .style('cursor', 'pointer')
    .on('click', (e, d) => showPair(d, state))
    .append('title').text(d => `${groupKey(d)} · n_support=${d.x} · sentiment=${d.y.toFixed(2)}`);

  // OLS regression line
  const stats = computeOLS(pairs.map(p => p.x), pairs.map(p => p.y));
  if (stats) {
    const xs = d3.range(0, xMax + 1, 0.1);
    const lineData = xs.map(xv => ({
      x: xv,
      y: stats.intercept + stats.slope * xv,
    }));
    g.append('path').datum(lineData)
      .attr('fill', 'none').attr('stroke', 'var(--cat-1)').attr('stroke-width', 2)
      .attr('d', d3.line().x(p => x(p.x)).y(p => y(Math.max(-1, Math.min(1, p.y)))));
  }

  // Legend
  const legend = svg.append('g').attr('transform', `translate(${margin.left}, 0)`);
  let lx = 0;
  for (const grp of groups) {
    const item = legend.append('g').attr('transform', `translate(${lx}, 0)`);
    item.append('rect').attr('width', 10).attr('height', 10).attr('fill', color(grp));
    item.append('text').attr('x', 14).attr('y', 9).attr('class', 'label').text(grp);
    lx += String(grp).length * 7 + 28;
  }
}

function groupKeyFor(p, state) {
  if (STATE.colorBy === 'rtu_role') return p.column?.rtu_role ?? '?';
  if (STATE.colorBy === 'rtu_session') return p.column?.rtu_session ?? '?';
  if (STATE.colorBy === 'school') {
    const s = state.schoolById.get(p.response.school);
    return s?.display_name ?? p.response.school;
  }
  if (STATE.colorBy === 'grade') return p.response.grade_level || 'unknown';
  return 'all';
}

function showPair(p, state) {
  const cats = SUPPORT_CATEGORIES.filter(c => p.cellVal.toLowerCase().includes(c.prefix.toLowerCase()));
  const html = `
    <h3>Support pair</h3>
    <div class="stat-row"><span class="k">support categories</span><span class="v">${p.x}</span></div>
    <div class="stat-row"><span class="k">reflection sentiment</span><span class="v">${p.y.toFixed(2)}</span></div>
    <div class="stat-row"><span class="k">school</span><span class="v">${escapeHTML(p.response.school)}</span></div>
    <div class="stat-row"><span class="k">grade</span><span class="v">${escapeHTML(p.response.grade_level ?? '?')}</span></div>
    <h3 style="margin-top:14px;font-size:13px">Categories selected</h3>
    <div style="font-family:var(--font-mono);font-size:11px">
      ${cats.map(c => `<span class="chip muted" style="margin:2px">${escapeHTML(c.label)}</span>`).join('')}
    </div>
    <h3 style="margin-top:14px;font-size:13px">Reflection</h3>
    <div class="question">${escapeHTML(p.reflectionText)}</div>
  `;
  openSidePanel(html);
}

function computeOLS(xs, ys) {
  const n = xs.length;
  if (n < 3) return null;
  const xMean = xs.reduce((a, b) => a + b, 0) / n;
  const yMean = ys.reduce((a, b) => a + b, 0) / n;
  let sxx = 0, sxy = 0, syy = 0;
  for (let i = 0; i < n; i++) {
    sxx += (xs[i] - xMean) ** 2;
    sxy += (xs[i] - xMean) * (ys[i] - yMean);
    syy += (ys[i] - yMean) ** 2;
  }
  if (sxx < 1e-12) return null;
  const slope = sxy / sxx;
  const intercept = yMean - slope * xMean;
  const r = sxy / Math.sqrt(sxx * syy);
  let ss_res = 0;
  for (let i = 0; i < n; i++) {
    ss_res += (ys[i] - (intercept + slope * xs[i])) ** 2;
  }
  const mse = ss_res / (n - 2);
  const se_slope = Math.sqrt(mse / sxx);
  return { n, slope, intercept, r, slopeCI: [slope - 1.96 * se_slope, slope + 1.96 * se_slope] };
}

function mulberry32(seed) {
  return function() {
    let t = seed += 0x6D2B79F5;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
