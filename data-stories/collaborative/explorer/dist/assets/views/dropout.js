// Dropout / retention analysis view.
//
// Renders four panels driven by `bundle.dropout_analysis` (precomputed in
// pipeline/dropout_analysis.py). All metrics are aggregate / ecological:
// the source data carry no participant identifier, so this view does NOT
// follow individual students across events.
//
// Panels:
//   1. Limitation banner (ecological-only caveat).
//   2. Retention curves — one D3 line per school, % of Kickoff vs. event.
//   3. Coefficient (forest) plot — pooled OLS β1, β2, β3 + collapsed
//      school heterogeneity range.
//   4. Top-20 biggest drop-off cohorts — hand-rolled table.
//
// The chip group at the very top toggles which schools appear in
// panels 2 and 4. All HTML interpolation is escaped via escapeHTML().

import { escapeHTML, showTooltip, hideTooltip } from '../app.js';

const STATE = {
  selectedSchools: null,  // null = all (initialized lazily on first render)
};

const COEF_LABEL = {
  event_ordinal: 'β1 · event ordinal',
  prior_mean_sentiment: 'β2 · prior mean sentiment',
  prior_pct_agree_safety: 'β3 · prior % agree safety',
};

export function renderDropout(root, appState) {
  const da = appState.bundle && appState.bundle.dropout_analysis;
  if (!da || !da.events || !da.schools) {
    root.innerHTML =
      '<h1>Dropout & retention</h1>' +
      '<div class="empty-state">' +
      '<strong>No <code>dropout_analysis</code> in this bundle.</strong><br/>' +
      'Rebuild with <code>python -m pipeline.build --out dist/data.json</code> ' +
      'to populate this view.' +
      '</div>';
    return;
  }

  // Initialize school selection on first render.
  if (STATE.selectedSchools === null) {
    STATE.selectedSchools = new Set(da.schools);
  }

  const wrap = document.createElement('div');
  wrap.innerHTML =
    '<h1>Dropout & retention across the 5 RTU events</h1>' +
    '<p class="lede">' +
    'Aggregate-funnel analysis with regression of retention on prior-event ' +
    'sentiment and safety. Cells with fewer than ' + da.min_cell_n +
    ' responses are dropped from the regression.' +
    '</p>' +
    '<div class="banner">' +
    '<span class="label">Ecological caveat</span> ' +
    escapeHTML(da.caveat || 'Aggregate analysis only.') +
    '</div>' +
    '<div class="panel">' +
    '<div class="panel-title">filter schools (panels below)</div>' +
    '<div id="dr-school-chips"></div>' +
    '</div>' +
    '<div class="panel">' +
    '<div class="panel-title">retention curves — % of each school\'s Kickoff response count</div>' +
    '<div id="dr-curves" style="min-height:340px"></div>' +
    '</div>' +
    '<div class="panel">' +
    '<div class="panel-title">pooled regression — coefficients with 95% bootstrap CIs</div>' +
    '<p class="lede" style="margin-top:0">' +
    'Pooled OLS with school as a one-hot fixed effect. ' +
    'Outcome = retention (% of school\'s Kickoff count). ' +
    (da.pooled_regression
      ? 'n_cells = ' + da.pooled_regression.n_cells + '.'
      : '(no fit — too few valid (school, event) cells).') +
    '</p>' +
    '<div id="dr-forest" style="min-height:200px"></div>' +
    '</div>' +
    '<div class="panel">' +
    '<div class="panel-title">biggest drop-off cohorts (top 20)</div>' +
    '<p class="lede" style="margin-top:0">' +
    'Sorted by absolute % change between adjacent events. Negative drop_pct ' +
    'means responses <em>grew</em> from one event to the next.' +
    '</p>' +
    '<div id="dr-table"></div>' +
    '</div>';
  root.appendChild(wrap);

  buildSchoolChips(appState, da);
  drawCurves(appState, da);
  drawForest(appState, da);
  drawTable(appState, da);
}

// ---------------------------------------------------------------------------
// School chip selector
// ---------------------------------------------------------------------------

function buildSchoolChips(appState, da) {
  const box = document.getElementById('dr-school-chips');
  box.innerHTML = '';

  const allBtn = document.createElement('span');
  allBtn.className = 'chip muted';
  allBtn.tabIndex = 0;
  allBtn.textContent = 'all';
  allBtn.style.margin = '2px';
  allBtn.addEventListener('click', () => {
    STATE.selectedSchools = new Set(da.schools);
    buildSchoolChips(appState, da);
    drawCurves(appState, da);
    drawTable(appState, da);
  });
  box.appendChild(allBtn);

  const noneBtn = document.createElement('span');
  noneBtn.className = 'chip muted';
  noneBtn.tabIndex = 0;
  noneBtn.textContent = 'none';
  noneBtn.style.margin = '2px';
  noneBtn.addEventListener('click', () => {
    STATE.selectedSchools = new Set();
    buildSchoolChips(appState, da);
    drawCurves(appState, da);
    drawTable(appState, da);
  });
  box.appendChild(noneBtn);

  for (const sid of da.schools) {
    const sRec = appState.schoolById.get(sid);
    const display = sRec && sRec.display_name ? sRec.display_name : sid;
    const chip = document.createElement('span');
    chip.className = 'chip ' + (STATE.selectedSchools.has(sid) ? 'active' : 'muted');
    chip.tabIndex = 0;
    chip.textContent = display;
    chip.style.margin = '2px';
    const apply = () => {
      if (STATE.selectedSchools.has(sid)) STATE.selectedSchools.delete(sid);
      else STATE.selectedSchools.add(sid);
      buildSchoolChips(appState, da);
      drawCurves(appState, da);
      drawTable(appState, da);
    };
    chip.addEventListener('click', apply);
    chip.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); apply(); }
    });
    box.appendChild(chip);
  }
}

// ---------------------------------------------------------------------------
// Panel 2 — Retention curves
// ---------------------------------------------------------------------------

function drawCurves(appState, da) {
  const host = document.getElementById('dr-curves');
  host.innerHTML = '';

  const events = da.events.slice().sort((a, b) => a.ordinal - b.ordinal);
  const selected = [...STATE.selectedSchools];

  if (selected.length === 0) {
    host.innerHTML = '<div class="empty-state">No schools selected — use the chips above.</div>';
    return;
  }

  const margin = { top: 16, right: 200, bottom: 50, left: 56 };
  const W = 980, H = 360;
  const innerW = W - margin.left - margin.right;
  const innerH = H - margin.top - margin.bottom;

  const svg = d3.select(host).append('svg')
    .attr('viewBox', '0 0 ' + W + ' ' + H)
    .style('width', '100%').style('height', H + 'px');
  const g = svg.append('g').attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')');

  const x = d3.scalePoint()
    .domain(events.map(e => e.id))
    .range([0, innerW])
    .padding(0.5);
  const y = d3.scaleLinear().domain([0, 110]).range([innerH, 0]);

  // Axes
  g.append('g').attr('class', 'axis').call(
    d3.axisLeft(y).ticks(6).tickFormat(d => d + '%')
  );
  g.append('g').attr('class', 'axis')
    .attr('transform', 'translate(0, ' + innerH + ')')
    .call(d3.axisBottom(x).tickFormat(id => {
      const ev = events.find(e => e.id === id);
      return ev ? ev.display_name : id;
    }));

  // Reference 100% line
  g.append('line')
    .attr('x1', 0).attr('x2', innerW)
    .attr('y1', y(100)).attr('y2', y(100))
    .attr('stroke', 'var(--cat-6)')
    .attr('stroke-dasharray', '3,3')
    .attr('stroke-width', 1);
  g.append('text')
    .attr('x', innerW - 4).attr('y', y(100) - 4)
    .attr('text-anchor', 'end').attr('class', 'footnote')
    .text('Kickoff baseline (100%)');

  // Build a Dartmouth-green palette for the visible schools.
  const cat = appState.bundle.palette.categorical;
  const seq = appState.bundle.palette.sequential;
  const colorPool = [...cat, ...seq.slice(2)];
  const color = d3.scaleOrdinal().domain(selected).range(
    selected.map((_, i) => colorPool[i % colorPool.length])
  );

  // Line generator with defined() to render gaps for null cells.
  const line = d3.line()
    .defined(d => d.value != null && Number.isFinite(d.value))
    .x(d => x(d.eventId))
    .y(d => y(d.value));

  const legend = svg.append('g').attr('transform',
    'translate(' + (W - margin.right + 12) + ', ' + margin.top + ')');
  let ly = 0;

  for (const sid of selected) {
    const curve = (da.school_retention || {})[sid];
    if (!curve) continue;
    const counts = (da.school_event_counts || {})[sid] || {};
    const pts = events.map(ev => ({
      eventId: ev.id,
      value: curve[ev.id],
      ordinal: ev.ordinal,
      n: counts[ev.id] || 0,
    }));
    const c = color(sid);

    g.append('path')
      .datum(pts)
      .attr('fill', 'none')
      .attr('stroke', c)
      .attr('stroke-width', 1.8)
      .attr('d', line);

    // Defined points
    g.selectAll(null).data(pts.filter(p => p.value != null)).enter().append('circle')
      .attr('cx', d => x(d.eventId)).attr('cy', d => y(d.value))
      .attr('r', 3.5).attr('fill', c).attr('stroke', 'white').attr('stroke-width', 1)
      .style('cursor', 'pointer')
      .on('mouseover', (e, d) => {
        const sName = (appState.schoolById.get(sid) || {}).display_name || sid;
        showTooltip(
          '<strong>' + escapeHTML(sName) + '</strong><br/>' +
          escapeHTML(d.eventId) + ' · n=' + d.n + ' · ' +
          '<span style="font-family:var(--font-mono)">' + d.value.toFixed(1) + '%</span> of Kickoff',
          e.clientX, e.clientY
        );
      })
      .on('mouseout', hideTooltip);

    // Render explicit "no data" markers for null cells (gaps).
    g.selectAll(null).data(pts.filter(p => p.value == null)).enter().append('text')
      .attr('x', d => x(d.eventId)).attr('y', y(0) + 14)
      .attr('text-anchor', 'middle').attr('class', 'footnote')
      .attr('fill', 'var(--ink-soft)').text('—');

    // Legend entry
    const sName = (appState.schoolById.get(sid) || {}).display_name || sid;
    const row = legend.append('g').attr('transform', 'translate(0, ' + ly + ')');
    row.append('line')
      .attr('x1', 0).attr('x2', 16).attr('y1', 6).attr('y2', 6)
      .attr('stroke', c).attr('stroke-width', 2);
    row.append('text').attr('x', 22).attr('y', 10)
      .attr('class', 'label').text(truncate(sName, 22));
    ly += 16;
  }
}

function truncate(s, n) {
  s = String(s);
  return s.length > n ? s.slice(0, n - 1) + '…' : s;
}

// ---------------------------------------------------------------------------
// Panel 3 — Forest plot of pooled coefficients
// ---------------------------------------------------------------------------

function drawForest(appState, da) {
  const host = document.getElementById('dr-forest');
  host.innerHTML = '';

  const pooled = da.pooled_regression;
  if (!pooled) {
    host.innerHTML = '<div class="empty-state">Pooled regression not available — too few cells.</div>';
    return;
  }

  // Build the rows: β1, β2, β3 + collapsed school FE range.
  const coefs = pooled.coefficients || {};
  const rows = [];
  for (const key of ['event_ordinal', 'prior_mean_sentiment', 'prior_pct_agree_safety']) {
    const c = coefs[key];
    if (!c) continue;
    rows.push({
      label: COEF_LABEL[key] || key,
      beta: c.beta,
      lo: (c.ci95 && c.ci95[0] != null) ? c.ci95[0] : null,
      hi: (c.ci95 && c.ci95[1] != null) ? c.ci95[1] : null,
      kind: 'main',
    });
  }
  // School heterogeneity collapsed range
  const fer = pooled.school_heterogeneity_range;
  if (fer && Number.isFinite(fer[0]) && Number.isFinite(fer[1])) {
    const center = (fer[0] + fer[1]) / 2;
    rows.push({
      label: 'school heterogeneity (FE range)',
      beta: center,
      lo: fer[0],
      hi: fer[1],
      kind: 'fe',
    });
  }

  if (rows.length === 0) {
    host.innerHTML = '<div class="empty-state">No coefficients to display.</div>';
    return;
  }

  const margin = { top: 12, right: 24, bottom: 36, left: 240 };
  const rowH = 28;
  const W = 880;
  const H = margin.top + margin.bottom + rows.length * rowH;
  const innerW = W - margin.left - margin.right;
  const innerH = rows.length * rowH;

  const svg = d3.select(host).append('svg')
    .attr('viewBox', '0 0 ' + W + ' ' + H)
    .style('width', '100%').style('height', H + 'px');
  const g = svg.append('g').attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')');

  // x scale: union of all CI bounds + betas
  let xMin = 0, xMax = 0;
  for (const r of rows) {
    if (r.lo != null) xMin = Math.min(xMin, r.lo);
    if (r.hi != null) xMax = Math.max(xMax, r.hi);
    xMin = Math.min(xMin, r.beta);
    xMax = Math.max(xMax, r.beta);
  }
  const pad = (xMax - xMin) * 0.1 || 1;
  const x = d3.scaleLinear().domain([xMin - pad, xMax + pad]).range([0, innerW]);

  // x axis (bottom)
  g.append('g').attr('class', 'axis')
    .attr('transform', 'translate(0, ' + innerH + ')')
    .call(d3.axisBottom(x).ticks(6).tickFormat(d3.format('.2f')));

  // x axis label
  svg.append('text')
    .attr('x', margin.left + innerW / 2).attr('y', H - 8)
    .attr('text-anchor', 'middle').attr('class', 'footnote')
    .text('β (change in retention % per unit predictor)');

  // Vertical reference line at 0
  g.append('line')
    .attr('x1', x(0)).attr('x2', x(0))
    .attr('y1', 0).attr('y2', innerH)
    .attr('stroke', 'var(--cat-1)').attr('stroke-dasharray', '4,3')
    .attr('stroke-width', 1).attr('opacity', 0.5);

  // Row backgrounds (alternate)
  rows.forEach((r, i) => {
    g.append('rect')
      .attr('x', -margin.left).attr('y', i * rowH)
      .attr('width', W).attr('height', rowH)
      .attr('fill', i % 2 === 0 ? 'transparent' : 'var(--seq-1)');
  });

  // Row labels
  rows.forEach((r, i) => {
    g.append('text')
      .attr('x', -10).attr('y', i * rowH + rowH / 2 + 4)
      .attr('text-anchor', 'end').attr('class', 'label')
      .text(r.label);
  });

  // CI bars + points
  rows.forEach((r, i) => {
    const cy = i * rowH + rowH / 2;
    const c = r.kind === 'fe' ? 'var(--cat-5)' : 'var(--cat-3)';
    if (r.lo != null && r.hi != null) {
      g.append('line')
        .attr('x1', x(r.lo)).attr('x2', x(r.hi))
        .attr('y1', cy).attr('y2', cy)
        .attr('stroke', c).attr('stroke-width', 2);
      // CI ticks
      g.append('line')
        .attr('x1', x(r.lo)).attr('x2', x(r.lo))
        .attr('y1', cy - 4).attr('y2', cy + 4)
        .attr('stroke', c).attr('stroke-width', 2);
      g.append('line')
        .attr('x1', x(r.hi)).attr('x2', x(r.hi))
        .attr('y1', cy - 4).attr('y2', cy + 4)
        .attr('stroke', c).attr('stroke-width', 2);
    }
    g.append('circle')
      .attr('cx', x(r.beta)).attr('cy', cy)
      .attr('r', 5).attr('fill', c).attr('stroke', 'white').attr('stroke-width', 1.5)
      .style('cursor', 'help')
      .on('mouseover', (e) => {
        const ciTxt = (r.lo != null && r.hi != null)
          ? '[' + r.lo.toFixed(2) + ', ' + r.hi.toFixed(2) + ']'
          : '(CI unavailable)';
        showTooltip(
          '<strong>' + escapeHTML(r.label) + '</strong><br/>' +
          '<span style="font-family:var(--font-mono)">β = ' + r.beta.toFixed(3) + '</span><br/>' +
          '<span style="font-family:var(--font-mono)">95% CI ' + escapeHTML(ciTxt) + '</span>',
          e.clientX, e.clientY
        );
      })
      .on('mouseout', hideTooltip);

    // β value label, right of the point
    g.append('text')
      .attr('x', x(r.beta) + 9).attr('y', cy - 6)
      .attr('class', 'label').attr('font-size', 10)
      .text(r.beta.toFixed(2));
  });
}

// ---------------------------------------------------------------------------
// Panel 4 — Top-20 drop-off cohorts
// ---------------------------------------------------------------------------

function drawTable(appState, da) {
  const host = document.getElementById('dr-table');
  host.innerHTML = '';

  const allRows = (da.top_drop_offs || []).filter(
    r => STATE.selectedSchools.has(r.school)
  );
  const rows = allRows.slice(0, 20);

  if (rows.length === 0) {
    host.innerHTML = '<div class="empty-state">No drop-off cohorts for the selected schools.</div>';
    return;
  }

  const tbl = document.createElement('table');
  tbl.style.width = '100%';
  tbl.style.borderCollapse = 'collapse';
  tbl.style.fontFamily = 'var(--font-mono)';
  tbl.style.fontSize = '12px';

  const thead = document.createElement('thead');
  const trh = document.createElement('tr');
  trh.style.background = 'var(--seq-1)';
  trh.style.borderBottom = '2px solid var(--cat-3)';
  const headerCells = [
    ['school', 'left'],
    ['transition', 'left'],
    ['n_before', 'right'],
    ['n_after', 'right'],
    ['drop_pct', 'right'],
  ];
  for (const [label, align] of headerCells) {
    const th = document.createElement('th');
    th.textContent = label;
    th.style.textAlign = align;
    th.style.padding = '6px 8px';
    th.style.color = 'var(--cat-1)';
    trh.appendChild(th);
  }
  thead.appendChild(trh);
  tbl.appendChild(thead);

  const tbody = document.createElement('tbody');
  rows.forEach((r, i) => {
    const tr = document.createElement('tr');
    tr.style.borderBottom = '1px solid var(--border, #e5e5e5)';
    tr.style.background = i % 2 === 0 ? 'transparent' : 'var(--seq-1)';

    const sName = (appState.schoolById.get(r.school) || {}).display_name || r.school;
    const dropColor = r.drop_pct > 0 ? 'var(--div-1)' : 'var(--cat-3)';
    const dropTxt = (r.drop_pct >= 0 ? '+' : '') + r.drop_pct.toFixed(1) + '%';

    const tdSchool = document.createElement('td');
    tdSchool.style.padding = '5px 8px';
    tdSchool.style.fontFamily = 'var(--font-serif)';
    tdSchool.textContent = sName;
    tr.appendChild(tdSchool);

    const tdTrans = document.createElement('td');
    tdTrans.style.padding = '5px 8px';
    tdTrans.textContent = r.transition_label;
    tr.appendChild(tdTrans);

    const tdBefore = document.createElement('td');
    tdBefore.style.padding = '5px 8px';
    tdBefore.style.textAlign = 'right';
    tdBefore.textContent = String(r.n_before);
    tr.appendChild(tdBefore);

    const tdAfter = document.createElement('td');
    tdAfter.style.padding = '5px 8px';
    tdAfter.style.textAlign = 'right';
    tdAfter.textContent = String(r.n_after);
    tr.appendChild(tdAfter);

    const tdDrop = document.createElement('td');
    tdDrop.style.padding = '5px 8px';
    tdDrop.style.textAlign = 'right';
    tdDrop.style.color = dropColor;
    tdDrop.style.fontWeight = '600';
    tdDrop.textContent = dropTxt;
    tr.appendChild(tdDrop);

    tbody.appendChild(tr);
  });
  tbl.appendChild(tbody);

  host.appendChild(tbl);

  if (allRows.length > 20) {
    const note = document.createElement('div');
    note.className = 'footnote';
    note.style.marginTop = '8px';
    note.style.fontFamily = 'var(--font-serif)';
    note.style.fontStyle = 'italic';
    note.style.color = 'var(--ink-soft)';
    note.textContent = 'Showing 20 of ' + allRows.length + ' drop-off cohorts (sorted by |drop_pct|).';
    host.appendChild(note);
  }
}
