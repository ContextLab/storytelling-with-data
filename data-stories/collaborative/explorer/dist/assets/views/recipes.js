// T065-T067: Recipe view — savory↔sweet × complexity scatter, color/filter,
// click-to-read, footer count of filtered-out non-recipe content.

import { escapeHTML, openSidePanel } from '../app.js';

const STATE = {
  xAxis: 'savory_sweet',
  yAxis: 'complexity',
  colorBy: 'school',  // 'school' | 'grade' | 'sentiment'
  schoolFilter: 'all',
  threshold: 0.25,
};

export function renderRecipes(root, appState) {
  const wrap = document.createElement('div');
  wrap.innerHTML = `
    <h1>Recipe analysis</h1>
    <p class="lede">Event-4 cookbook responses positioned on culinary axes derived from a recipe-aware embedding model.</p>

    <div id="rc-banner-host"></div>

    <div class="panel">
      <div class="panel-title">axes</div>
      x:
      <select id="rc-x"><option value="savory_sweet">savory ↔ sweet</option><option value="complexity">simple ↔ complex</option></select>
      &nbsp; y:
      <select id="rc-y"><option value="complexity">simple ↔ complex</option><option value="savory_sweet">savory ↔ sweet</option></select>
    </div>

    <div class="panel">
      <div class="panel-title">color by</div>
      <span class="chip" data-color="school" tabindex="0">school</span>
      <span class="chip" data-color="grade" tabindex="0">grade</span>
      <span class="chip" data-color="sentiment" tabindex="0">co-response sentiment</span>
    </div>

    <div class="panel">
      <div class="panel-title">school filter</div>
      <select id="rc-school"></select>
    </div>

    <div class="panel">
      <div class="panel-title">map</div>
      <div id="rc-host" style="min-height:520px"></div>
      <div id="rc-footer" style="font-family:var(--font-mono);font-size:11px;color:var(--ink-soft);margin-top:8px;text-align:right"></div>
    </div>
  `;
  root.appendChild(wrap);

  // Recipe candidates
  const candidates = appState.bundle.freetext_items.filter(ft => ft.is_recipe_candidate && ft.recipe_axes);
  if (candidates.length === 0) {
    document.getElementById('rc-banner-host').innerHTML =
      '<div class="banner"><span class="label">recipe model</span>Recipe model not available — install/enable to use this view.</div>';
    return;
  }

  // Populate school filter
  const schoolSel = document.getElementById('rc-school');
  const schoolIds = [...new Set(candidates.map(ft => appState.responseById.get(ft.response_id)?.school).filter(Boolean))].sort();
  schoolSel.innerHTML = '<option value="all">All schools</option>' +
    schoolIds.map(sid => `<option value="${sid}">${escapeHTML(appState.schoolById.get(sid)?.display_name ?? sid)}</option>`).join('');
  schoolSel.addEventListener('change', e => { STATE.schoolFilter = e.target.value; drawScatter(appState); });

  document.getElementById('rc-x').addEventListener('change', e => { STATE.xAxis = e.target.value; drawScatter(appState); });
  document.getElementById('rc-y').addEventListener('change', e => { STATE.yAxis = e.target.value; drawScatter(appState); });
  bindColorChips(appState);

  drawScatter(appState);
}

function bindColorChips(appState) {
  document.querySelectorAll('[data-color]').forEach(el => {
    el.classList.toggle('active', el.dataset.color === STATE.colorBy);
    el.classList.toggle('muted', el.dataset.color !== STATE.colorBy);
    el.addEventListener('click', () => {
      STATE.colorBy = el.dataset.color;
      bindColorChips(appState);
      drawScatter(appState);
    });
  });
}

function drawScatter(appState) {
  const host = document.getElementById('rc-host');
  host.innerHTML = '';

  const allCandidates = appState.bundle.freetext_items.filter(ft => ft.is_recipe_candidate && ft.recipe_axes);
  const filteredOut = allCandidates.filter(ft => ft.recipe_axes.recipe_confidence < STATE.threshold);
  let items = allCandidates.filter(ft => ft.recipe_axes.recipe_confidence >= STATE.threshold);

  if (STATE.schoolFilter !== 'all') {
    items = items.filter(ft => appState.responseById.get(ft.response_id)?.school === STATE.schoolFilter);
  }

  document.getElementById('rc-footer').textContent =
    `Showing ${items.length} recipes · ${filteredOut.length} responses excluded as non-recipe content (confidence < ${STATE.threshold})`;

  if (items.length === 0) {
    host.innerHTML = '<div class="empty-state">No recipes for this filter.</div>';
    return;
  }

  const W = 880, H = 500;
  const margin = { top: 24, right: 16, bottom: 50, left: 60 };
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
  svg.append('text').attr('class', 'label')
    .attr('x', margin.left + innerW / 2).attr('y', H - 14).attr('text-anchor', 'middle')
    .text(axisLabel(STATE.xAxis));
  svg.append('text').attr('class', 'label')
    .attr('transform', `rotate(-90)`)
    .attr('x', -(margin.top + innerH / 2)).attr('y', 16).attr('text-anchor', 'middle')
    .text(axisLabel(STATE.yAxis));

  // Quadrant corner hints
  const corners = [
    [innerW - 4, 12, axisHi(STATE.xAxis) + ' · ' + axisHi(STATE.yAxis), 'end'],
    [4, 12, axisLo(STATE.xAxis) + ' · ' + axisHi(STATE.yAxis), 'start'],
    [innerW - 4, innerH - 6, axisHi(STATE.xAxis) + ' · ' + axisLo(STATE.yAxis), 'end'],
    [4, innerH - 6, axisLo(STATE.xAxis) + ' · ' + axisLo(STATE.yAxis), 'start'],
  ];
  for (const [cx, cy, txt, anchor] of corners) {
    g.append('text').attr('x', cx).attr('y', cy).attr('text-anchor', anchor)
      .attr('class', 'footnote').text(txt);
  }

  g.append('g').selectAll('circle').data(items).enter().append('circle')
    .attr('cx', d => x(d.recipe_axes[STATE.xAxis]))
    .attr('cy', d => y(d.recipe_axes[STATE.yAxis]))
    .attr('r', 5)
    .attr('fill', d => colorFor(d, appState))
    .attr('fill-opacity', 0.75)
    .style('cursor', 'pointer')
    .on('click', (e, d) => showRecipe(d, appState))
    .append('title').text(d => `${d.text.slice(0, 80)}…`);
}

function axisLabel(a) {
  return a === 'savory_sweet' ? 'savory ←→ sweet' : 'simple ←→ complex';
}
function axisHi(a) { return a === 'savory_sweet' ? 'sweet' : 'complex'; }
function axisLo(a) { return a === 'savory_sweet' ? 'savory' : 'simple'; }

function colorFor(ft, appState) {
  const cat = appState.bundle.palette.categorical;
  if (STATE.colorBy === 'sentiment') {
    return d3.interpolateRgb('#a86b6b', '#00351e')(0.5 + ft.sentiment_score / 2);
  }
  const resp = appState.responseById.get(ft.response_id);
  if (!resp) return '#999';
  let key = STATE.colorBy === 'school' ? resp.school : (resp.grade_level || 'unknown');
  let h = 0;
  for (let i = 0; i < key.length; i++) h = (h * 31 + key.charCodeAt(i)) >>> 0;
  return cat[h % cat.length];
}

function showRecipe(ft, appState) {
  const resp = appState.responseById.get(ft.response_id);
  openSidePanel(`
    <h3>Recipe</h3>
    <div class="question">${escapeHTML(ft.text)}</div>
    <div class="stat-row"><span class="k">school</span><span class="v">${escapeHTML(appState.schoolById.get(resp?.school)?.display_name ?? resp?.school ?? '?')}</span></div>
    <div class="stat-row"><span class="k">grade</span><span class="v">${escapeHTML(resp?.grade_level ?? '?')}</span></div>
    <div class="stat-row"><span class="k">savory ↔ sweet</span><span class="v">${ft.recipe_axes.savory_sweet.toFixed(2)}</span></div>
    <div class="stat-row"><span class="k">simple ↔ complex</span><span class="v">${ft.recipe_axes.complexity.toFixed(2)}</span></div>
    <div class="stat-row"><span class="k">recipe confidence</span><span class="v">${ft.recipe_axes.recipe_confidence.toFixed(2)}</span></div>
    <div class="stat-row"><span class="k">co-response sentiment</span><span class="v">${ft.sentiment_score.toFixed(2)} (${ft.sentiment_label})</span></div>
  `);
}
