// Figure 1: Recipe savory↔sweet (or complexity) vs. sentiment of the same
// respondent's "What did you learn from this event?" answer (Event 4).

import { escapeHTML, openSidePanel } from '../app.js';

const STATE = {
  recipeAxis: 'savory_sweet',  // 'savory_sweet' | 'complexity'
  colorBy: 'rtu_role',          // 'rtu_role' | 'rtu_session' | 'school' | 'grade'
  schoolFilter: new Set(),
};

export function renderRecipeVsLearn(root, state) {
  root.innerHTML = '';
  // Pull (recipe, learn-sentiment) pairs from same response_id
  const recipeFTs = state.bundle.freetext_items.filter(
    ft => ft.is_recipe_candidate && ft.recipe_axes && ft.recipe_axes.recipe_confidence >= 0.25
  );
  // For each recipe-bearing response, find the same response's "what did you learn" freetext item(s)
  const learnColumnIds = new Set(
    state.bundle.columns
      .filter(c => c.original_header.toLowerCase().includes('what did you learn'))
      .map(c => c.id)
  );
  const ftByResponse = new Map();
  for (const ft of state.bundle.freetext_items) {
    if (!learnColumnIds.has(ft.column_id)) continue;
    if (!ftByResponse.has(ft.response_id)) ftByResponse.set(ft.response_id, []);
    ftByResponse.get(ft.response_id).push(ft);
  }
  const pairs = [];
  for (const r of recipeFTs) {
    const learnFTs = ftByResponse.get(r.response_id);
    if (!learnFTs || !learnFTs.length) continue;
    // average the response's learn sentiments (usually 1)
    const learnSent = learnFTs.reduce((a, b) => a + b.sentiment_score, 0) / learnFTs.length;
    const resp = state.responseById.get(r.response_id);
    if (!resp) continue;
    pairs.push({
      x: r.recipe_axes[STATE.recipeAxis],
      y: learnSent,
      recipeText: r.text,
      learnText: learnFTs[0].text,
      response: resp,
      column: state.columnById.get(r.column_id),
    });
  }

  // School filter
  let visible = pairs;
  if (STATE.schoolFilter.size > 0) {
    visible = pairs.filter(p => STATE.schoolFilter.has(p.response.school));
  }

  // Header + controls
  const wrap = document.createElement('div');
  wrap.innerHTML = `
    <div class="panel">
      <div class="panel-title">about this figure</div>
      <h2 style="margin-top:0">Recipe culinary axis vs. "What did you learn"</h2>
      <p class="lede">Each dot is one Event-4 respondent who submitted both a cookbook recipe and a "what did you learn" answer.
      The x-axis is their recipe's position on the savory↔sweet (or complexity) axis from the recipe-aware embedding model.
      The y-axis is the sentiment score of their <em>same response's</em> "what did you learn" reflection.</p>
      <p class="lede" style="font-size:13px"><strong>n = ${visible.length} pairs</strong> (of ${pairs.length} eligible after recipe-confidence filter ≥ 0.25)</p>
    </div>

    <div class="panel">
      <div class="panel-title">controls</div>
      x-axis:
      <span class="chip" data-axis="savory_sweet" tabindex="0">savory ↔ sweet</span>
      <span class="chip" data-axis="complexity" tabindex="0">simple ↔ complex</span>
      &nbsp;&nbsp;color by:
      <span class="chip" data-color="rtu_role" tabindex="0">role</span>
      <span class="chip" data-color="rtu_session" tabindex="0">session</span>
      <span class="chip" data-color="school" tabindex="0">school</span>
      <span class="chip" data-color="grade" tabindex="0">grade</span>
      <div style="margin-top:10px">
        <span style="font-family:var(--font-mono);font-size:11px;color:var(--ink-soft);text-transform:uppercase">filter to schools:</span>
        <div id="rl-school-chips" style="display:inline-block; margin-left:6px"></div>
      </div>
    </div>

    <div class="panel">
      <div class="panel-title">scatter + regression</div>
      <div id="rl-host" style="min-height:480px"></div>
      <div id="rl-stats" style="font-family:var(--font-mono);font-size:12px;color:var(--ink-soft);text-align:right;margin-top:8px"></div>
    </div>
  `;
  root.appendChild(wrap);

  // Bind controls
  document.querySelectorAll('[data-axis]').forEach(el => {
    el.classList.toggle('active', el.dataset.axis === STATE.recipeAxis);
    el.classList.toggle('muted',  el.dataset.axis !== STATE.recipeAxis);
    el.addEventListener('click', () => { STATE.recipeAxis = el.dataset.axis; renderRecipeVsLearn(root, state); });
  });
  document.querySelectorAll('[data-color]').forEach(el => {
    el.classList.toggle('active', el.dataset.color === STATE.colorBy);
    el.classList.toggle('muted',  el.dataset.color !== STATE.colorBy);
    el.addEventListener('click', () => { STATE.colorBy = el.dataset.color; renderRecipeVsLearn(root, state); });
  });

  // School chips
  const schoolBox = document.getElementById('rl-school-chips');
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
      renderRecipeVsLearn(root, state);
    });
    schoolBox.appendChild(chip);
  }

  drawScatter(visible, state);
  // Pearson r + OLS β + 95% CI on slope
  const stats = computeOLS(visible.map(p => p.x), visible.map(p => p.y));
  if (stats) {
    document.getElementById('rl-stats').innerHTML =
      `Pearson r = <strong>${stats.r.toFixed(3)}</strong> · slope β = <strong>${stats.slope.toFixed(3)}</strong> ` +
      `[95% CI ${stats.slopeCI[0].toFixed(3)}, ${stats.slopeCI[1].toFixed(3)}] · n = ${stats.n}`;
  }
}

function drawScatter(pairs, state) {
  const host = document.getElementById('rl-host');
  host.innerHTML = '';
  if (pairs.length === 0) {
    host.innerHTML = '<div class="empty-state">No pairs match the current filter.</div>';
    return;
  }

  const W = 880, H = 480;
  const margin = { top: 20, right: 20, bottom: 60, left: 60 };
  const innerW = W - margin.left - margin.right;
  const innerH = H - margin.top - margin.bottom;

  const x = d3.scaleLinear().domain([-1, 1]).range([0, innerW]);
  const y = d3.scaleLinear().domain([-1, 1]).range([innerH, 0]);

  const svg = d3.select(host).append('svg')
    .attr('viewBox', `0 0 ${W} ${H}`).style('width', '100%').style('height', H + 'px');
  const g = svg.append('g').attr('transform', `translate(${margin.left}, ${margin.top})`);

  // Quadrant lines
  g.append('line').attr('x1', x(0)).attr('x2', x(0)).attr('y1', 0).attr('y2', innerH)
    .attr('stroke', 'var(--border)').attr('stroke-dasharray', '2 4');
  g.append('line').attr('x1', 0).attr('x2', innerW).attr('y1', y(0)).attr('y2', y(0))
    .attr('stroke', 'var(--border)').attr('stroke-dasharray', '2 4');

  g.append('g').attr('class', 'axis').attr('transform', `translate(0, ${innerH})`)
    .call(d3.axisBottom(x).ticks(5).tickFormat(d3.format('+.1f')));
  g.append('g').attr('class', 'axis').call(d3.axisLeft(y).ticks(5).tickFormat(d3.format('+.1f')));

  // Axis labels
  const xLabel = STATE.recipeAxis === 'savory_sweet' ? 'recipe: savory ←→ sweet' : 'recipe: simple ←→ complex';
  svg.append('text').attr('class', 'label').attr('x', margin.left + innerW / 2).attr('y', H - 18)
    .attr('text-anchor', 'middle').text(xLabel);
  svg.append('text').attr('class', 'label').attr('transform', 'rotate(-90)')
    .attr('x', -(margin.top + innerH / 2)).attr('y', 16).attr('text-anchor', 'middle')
    .text('learn-sentiment: negative ←→ positive');

  // Color scale
  const cat = state.bundle.palette.categorical;
  const groupKey = (p) => groupKeyFor(p, state);
  const groups = [...new Set(pairs.map(groupKey))].sort();
  const color = d3.scaleOrdinal().domain(groups).range(groups.map((_, i) => cat[i % cat.length]));

  // Dots
  g.append('g').selectAll('circle').data(pairs).enter().append('circle')
    .attr('cx', d => x(d.x)).attr('cy', d => y(d.y))
    .attr('r', 5).attr('fill-opacity', 0.7)
    .attr('fill', d => color(groupKey(d)))
    .style('cursor', 'pointer')
    .on('click', (e, d) => showPair(d))
    .append('title').text(d =>
      `${groupKey(d)}\n${STATE.recipeAxis}: ${d.x.toFixed(2)} · learn-sentiment: ${d.y.toFixed(2)}\n` +
      `recipe: ${d.recipeText.slice(0, 60)}…\nlearn: ${d.learnText.slice(0, 60)}…`
    );

  // OLS regression line + 95% CI band
  const stats = computeOLS(pairs.map(p => p.x), pairs.map(p => p.y));
  if (stats) {
    const xs = d3.range(-1, 1.01, 0.05);
    const lineData = xs.map(xv => {
      const yv = stats.intercept + stats.slope * xv;
      const se = Math.sqrt(stats.mse * (1 / stats.n + Math.pow(xv - stats.xMean, 2) / stats.sxx));
      return { x: xv, y: yv, lo: yv - 1.96 * se, hi: yv + 1.96 * se };
    });
    // CI band
    g.append('path').datum(lineData)
      .attr('fill', 'var(--cat-3)').attr('fill-opacity', 0.12)
      .attr('d', d3.area()
        .x(p => x(p.x))
        .y0(p => y(Math.max(-1, p.lo)))
        .y1(p => y(Math.min(1, p.hi))));
    // Line
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

function groupKeyFor(pair, state) {
  if (STATE.colorBy === 'rtu_role') return pair.column?.rtu_role ?? '?';
  if (STATE.colorBy === 'rtu_session') return pair.column?.rtu_session ?? '?';
  if (STATE.colorBy === 'school') {
    const s = state.schoolById.get(pair.response.school);
    return s?.display_name ?? pair.response.school;
  }
  if (STATE.colorBy === 'grade') return pair.response.grade_level || 'unknown';
  return 'all';
}

function showPair(p) {
  const html = `
    <h3>Recipe + learn pair</h3>
    <div class="stat-row"><span class="k">${STATE.recipeAxis}</span><span class="v">${p.x.toFixed(2)}</span></div>
    <div class="stat-row"><span class="k">learn-sentiment</span><span class="v">${p.y.toFixed(2)}</span></div>
    <div class="stat-row"><span class="k">school</span><span class="v">${escapeHTML(p.response.school)}</span></div>
    <div class="stat-row"><span class="k">grade</span><span class="v">${escapeHTML(p.response.grade_level ?? '?')}</span></div>
    <h3 style="margin-top:14px;font-size:13px">Recipe</h3>
    <div class="question">${escapeHTML(p.recipeText)}</div>
    <h3 style="margin-top:14px;font-size:13px">"What did you learn"</h3>
    <div class="question">${escapeHTML(p.learnText)}</div>
  `;
  openSidePanel(html);
}

// OLS with bootstrap-free analytic SE
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
  // Pearson r
  const r = sxy / Math.sqrt(sxx * syy);
  // residuals + MSE
  let ss_res = 0;
  for (let i = 0; i < n; i++) {
    const pred = intercept + slope * xs[i];
    ss_res += (ys[i] - pred) ** 2;
  }
  const mse = ss_res / (n - 2);
  const se_slope = Math.sqrt(mse / sxx);
  return {
    n, slope, intercept, r,
    slopeCI: [slope - 1.96 * se_slope, slope + 1.96 * se_slope],
    mse, sxx, xMean,
  };
}
