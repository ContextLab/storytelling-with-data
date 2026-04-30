// T050-T052: Effectiveness panel — survey_direct, sentiment_derived,
// behavioral_intent, retention_derived indicators with tooltipped definitions.

import { escapeHTML } from '../app.js';
import { exportSvgPng } from '../util/export.js';

const STATE = {
  selectedIds: new Set(),
};

const FAMILY_ORDER = ['survey_direct', 'sentiment_derived', 'behavioral_intent', 'retention_derived'];
const FAMILY_LABEL = {
  survey_direct: 'Survey-direct',
  sentiment_derived: 'Sentiment-derived',
  behavioral_intent: 'Behavioral intent',
  retention_derived: 'Retention-derived',
};

export function renderEffectiveness(root, appState) {
  const wrap = document.createElement('div');
  wrap.innerHTML = `
    <h1>Event effectiveness</h1>
    <p class="lede">Survey-direct, sentiment-derived, behavioral-intent, and retention-derived indicators.</p>

    <div class="panel">
      <div class="panel-title">indicators (hover names to see how each is computed)</div>
      <div id="ef-picker"></div>
    </div>

    <div id="ef-charts"></div>
  `;
  root.appendChild(wrap);
  populatePicker(appState);
  drawCharts(appState);
}

function populatePicker(appState) {
  const box = document.getElementById('ef-picker');
  box.innerHTML = '';
  const groups = {};
  for (const fam of FAMILY_ORDER) groups[fam] = [];
  for (const ind of appState.bundle.effectiveness_indicators) {
    if (groups[ind.family]) groups[ind.family].push(ind);
  }
  for (const fam of FAMILY_ORDER) {
    if (!groups[fam].length) continue;
    const sect = document.createElement('div');
    sect.style.marginBottom = '10px';
    sect.innerHTML = `<div class="panel-title" style="margin-bottom:4px">${FAMILY_LABEL[fam]}</div>`;
    box.appendChild(sect);
    for (const ind of groups[fam]) {
      const chip = document.createElement('span');
      chip.className = 'chip ' + (STATE.selectedIds.has(ind.id) ? 'active' : 'muted');
      chip.tabIndex = 0;
      chip.textContent = ind.display_name;
      chip.title = ind.description + '\n\nValue scale: ' + ind.value_scale;
      chip.style.margin = '2px';
      chip.addEventListener('click', () => {
        if (STATE.selectedIds.has(ind.id)) STATE.selectedIds.delete(ind.id);
        else STATE.selectedIds.add(ind.id);
        populatePicker(appState);
        drawCharts(appState);
      });
      sect.appendChild(chip);
    }
  }
}

function drawCharts(appState) {
  const box = document.getElementById('ef-charts');
  box.innerHTML = '';
  if (STATE.selectedIds.size === 0) {
    box.innerHTML = '<div class="empty-state">Pick one or more indicators above.</div>';
    return;
  }
  const fs = appState.filters.schools;
  for (const id of STATE.selectedIds) {
    const ind = appState.bundle.effectiveness_indicators.find(i => i.id === id);
    if (!ind) continue;
    drawIndicator(box, ind, appState, fs);
  }
}

function drawIndicator(box, ind, appState, schoolFilter) {
  const card = document.createElement('div');
  card.className = 'panel';
  card.innerHTML = `
    <div class="panel-title">${escapeHTML(FAMILY_LABEL[ind.family] || ind.family)}</div>
    <h2 style="margin-top:0">${escapeHTML(ind.display_name)}</h2>
    <p class="lede" style="margin-top:0">${escapeHTML(ind.description)}</p>
  `;
  box.appendChild(card);

  // Slice computed_values by event/year/school combinations
  const filtered = ind.computed_values.filter(v => {
    if (schoolFilter.size > 0 && v.filters.school_id && !schoolFilter.has(v.filters.school_id)) return false;
    return true;
  });

  if (filtered.length === 0) {
    card.insertAdjacentHTML('beforeend', '<div class="empty-state">n/a — no data for the active filter.</div>');
    return;
  }

  // Group by event_id (preferred) or year
  const groupKey = filtered[0].filters.event_id ? 'event_id' : 'year';
  const byGroup = new Map();
  for (const v of filtered) {
    const key = v.filters[groupKey] ?? 'all';
    if (!byGroup.has(key)) byGroup.set(key, []);
    byGroup.get(key).push(v);
  }
  // Aggregate within each group: weighted mean by n
  const groupRows = [];
  for (const [k, vs] of byGroup.entries()) {
    const totalN = vs.reduce((a, b) => a + b.n, 0);
    if (totalN === 0) continue;
    const wm = vs.reduce((a, b) => a + b.value * b.n, 0) / totalN;
    groupRows.push({ key: k, value: wm, n: totalN });
  }
  if (groupRows.length === 0) return;

  // Sort: events by ordinal, years numerically
  if (groupKey === 'event_id') {
    const order = appState.bundle.events.map(e => e.id);
    groupRows.sort((a, b) => order.indexOf(a.key) - order.indexOf(b.key));
  } else {
    groupRows.sort((a, b) => Number(a.key) - Number(b.key));
  }

  // Render bar chart
  const margin = { top: 8, right: 12, bottom: 50, left: 50 };
  const W = 760, H = 220;
  const innerW = W - margin.left - margin.right;
  const innerH = H - margin.top - margin.bottom;
  const svg = d3.select(card).append('svg')
    .attr('viewBox', `0 0 ${W} ${H}`).style('width', '100%').style('height', H + 'px');
  const g = svg.append('g').attr('transform', `translate(${margin.left}, ${margin.top})`);

  const x = d3.scaleBand().domain(groupRows.map(r => labelFor(r.key, groupKey, appState))).range([0, innerW]).padding(0.25);
  const yMax = ind.value_scale === 'pct_in_0_100' ? 100
    : ind.value_scale === 'mean_in_neg1_pos1' ? 1 : 1;
  const yMin = ind.value_scale === 'mean_in_neg1_pos1' ? -1 : 0;
  const y = d3.scaleLinear().domain([yMin, yMax]).range([innerH, 0]);

  g.append('g').attr('class', 'axis').call(d3.axisLeft(y).ticks(5).tickFormat(
    ind.value_scale === 'pct_in_0_100' ? d => d + '%' : d3.format('.2f')
  ));
  g.append('g').attr('class', 'axis').attr('transform', `translate(0, ${innerH})`)
    .call(d3.axisBottom(x))
    .selectAll('text').attr('transform', 'rotate(-25)').style('text-anchor', 'end');

  const cat = appState.bundle.palette.sequential;
  for (const row of groupRows) {
    const xKey = labelFor(row.key, groupKey, appState);
    const yPos = y(row.value);
    g.append('rect')
      .attr('x', x(xKey)).attr('y', Math.min(yPos, y(0)))
      .attr('width', x.bandwidth()).attr('height', Math.abs(y(0) - yPos))
      .attr('fill', cat[3]);
    g.append('text')
      .attr('x', x(xKey) + x.bandwidth() / 2)
      .attr('y', yPos - 4)
      .attr('text-anchor', 'middle')
      .attr('class', 'label')
      .text(`n=${row.n}`);
  }
}

function labelFor(key, groupKey, appState) {
  if (groupKey === 'event_id') {
    const e = appState.bundle.events.find(x => x.id === key);
    return e?.display_name ?? key;
  }
  return String(key);
}
