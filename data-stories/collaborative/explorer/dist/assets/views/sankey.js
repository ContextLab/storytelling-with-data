// T045-T047: Sankey view — 5-event response funnel with stratification by school/grade.
// Aggregate-funnel mode (FR-018) since respondent linking is unavailable.

import { escapeHTML } from '../app.js';
import { exportSvgPng } from '../util/export.js';

const STATE = {
  stratifyBy: 'school',  // 'school' | 'grade' | 'none'
};

export function renderSankey(root, appState) {
  const wrap = document.createElement('div');
  wrap.innerHTML = `
    <h1>Retention across the 5 RTU events</h1>
    <p class="lede">Aggregate response funnel from Kickoff → Event 5, optionally stratified by school or grade.</p>

    <div class="banner">
      <span class="label">Limitation</span>
      Individual respondents cannot be linked across events (no participant ID in the source data).
      This is an <strong>aggregate response funnel</strong>, not an individual-level Sankey:
      ribbons reflect the share of total responses moving from one event's pool to the next, not the same students returning.
    </div>

    <div class="panel">
      <div class="panel-title">stratify by</div>
      <span class="chip" data-strat="school" tabindex="0">school</span>
      <span class="chip" data-strat="grade" tabindex="0">grade</span>
      <span class="chip" data-strat="none" tabindex="0">none</span>
    </div>

    <div class="panel">
      <div class="panel-title">funnel</div>
      <div id="sk-host" style="min-height:520px"></div>
      <div style="text-align:right;margin-top:10px">
        <button id="sk-export" type="button">export PNG + caption</button>
      </div>
    </div>
  `;
  root.appendChild(wrap);

  bindStratChips(appState);
  document.getElementById('sk-export').addEventListener('click', () => doExport());
  drawSankey(appState);
}

function bindStratChips(appState) {
  document.querySelectorAll('[data-strat]').forEach(el => {
    el.classList.toggle('active', el.dataset.strat === STATE.stratifyBy);
    el.classList.toggle('muted', el.dataset.strat !== STATE.stratifyBy);
    el.addEventListener('click', () => {
      STATE.stratifyBy = el.dataset.strat;
      bindStratChips(appState);
      drawSankey(appState);
    });
  });
}

function drawSankey(appState) {
  const host = document.getElementById('sk-host');
  host.innerHTML = '';
  const events = appState.bundle.events.slice().sort((a, b) => a.ordinal - b.ordinal);

  // Build counts: per (event_id, stratum) -> count
  const counts = new Map(); // key -> count
  const strataSet = new Set();
  for (const r of appState.bundle.responses) {
    const sheet = appState.sheetById.get(r.sheet_id);
    if (!sheet) continue;
    const ev = events.find(e => e.sheet_id === sheet.id);
    if (!ev) continue;
    const stratum = stratumOf(r, appState);
    if (stratum == null) continue;
    strataSet.add(stratum);
    const key = ev.id + '__' + stratum;
    counts.set(key, (counts.get(key) || 0) + 1);
  }
  const strata = [...strataSet].sort();

  // Build Sankey nodes: one per (event, stratum)
  const nodes = [];
  const nodeIndex = new Map();
  for (const ev of events) {
    for (const st of strata) {
      const idx = nodes.length;
      nodes.push({ name: `${ev.display_name} · ${st}`, evId: ev.id, stratum: st, evOrdinal: ev.ordinal });
      nodeIndex.set(ev.id + '__' + st, idx);
    }
  }

  // Links: for each consecutive event pair, route the *minimum* of the
  // two counts as a "stayed" flow per stratum, plus the rest as drop-off
  // into a phantom 'gone' node (we render only the kept flows for clarity).
  // Aggregate funnel approximation: ribbon thickness = source count.
  const links = [];
  for (let i = 0; i < events.length - 1; i++) {
    const a = events[i], b = events[i + 1];
    for (const st of strata) {
      const cA = counts.get(a.id + '__' + st) || 0;
      const cB = counts.get(b.id + '__' + st) || 0;
      const flow = Math.min(cA, cB);
      if (flow > 0) {
        links.push({
          source: nodeIndex.get(a.id + '__' + st),
          target: nodeIndex.get(b.id + '__' + st),
          value: flow,
          srcCount: cA,
          dstCount: cB,
          stratum: st,
        });
      }
    }
  }

  if (links.length === 0) {
    host.innerHTML = '<div class="empty-state">No flow data for this stratification.</div>';
    return;
  }

  const W = 980, H = 520;
  const svg = d3.select(host).append('svg')
    .attr('viewBox', `0 0 ${W} ${H}`).style('width', '100%').style('height', H + 'px');

  const sankey = d3.sankey()
    .nodeId((d, i) => i)
    .nodeWidth(14)
    .nodePadding(4)
    .extent([[20, 30], [W - 130, H - 20]]);

  const layout = sankey({
    nodes: nodes.map(d => Object.assign({}, d)),
    links: links.map(d => Object.assign({}, d)),
  });

  const cat = appState.bundle.palette.categorical;
  const color = d3.scaleOrdinal().domain(strata).range(strata.map((_, i) => cat[i % cat.length]));

  // Links
  svg.append('g').attr('fill', 'none').attr('stroke-opacity', 0.5)
    .selectAll('path').data(layout.links).enter().append('path')
    .attr('d', d3.sankeyLinkHorizontal())
    .attr('stroke', d => color(d.stratum))
    .attr('stroke-width', d => Math.max(1, d.width))
    .append('title').text(d => {
      const ret = d.srcCount > 0 ? (d.value / d.srcCount * 100).toFixed(0) : '?';
      const srcName = (typeof d.source === 'object') ? d.source.name : nodes[d.source].name;
      const dstName = (typeof d.target === 'object') ? d.target.name : nodes[d.target].name;
      return `${srcName} → ${dstName}\n` +
        `flow: ${d.value} · src: ${d.srcCount} · dst: ${d.dstCount} · retention: ${ret}%`;
    });

  // Nodes
  svg.append('g').selectAll('rect').data(layout.nodes).enter().append('rect')
    .attr('x', d => d.x0).attr('y', d => d.y0)
    .attr('height', d => Math.max(2, d.y1 - d.y0)).attr('width', d => d.x1 - d.x0)
    .attr('fill', d => color(d.stratum))
    .append('title').text(d => `${d.name}\nresponses: ${d.value}`);

  // Event-column headers (top)
  const events2 = events;
  for (const ev of events2) {
    const xs = layout.nodes.filter(n => n.evId === ev.id).map(n => (n.x0 + n.x1) / 2);
    if (xs.length === 0) continue;
    const x = xs.reduce((a, b) => a + b, 0) / xs.length;
    const total = [...counts.entries()].filter(([k]) => k.startsWith(ev.id + '__'))
      .reduce((a, [, v]) => a + v, 0);
    svg.append('text').attr('x', x).attr('y', 18).attr('text-anchor', 'middle')
      .attr('class', 'label').text(`${ev.display_name} (n=${total})`);
  }

  // Legend
  const legend = svg.append('g').attr('transform', `translate(${W - 120}, 30)`);
  let ly = 0;
  for (const st of strata) {
    const g = legend.append('g').attr('transform', `translate(0, ${ly})`);
    g.append('rect').attr('width', 12).attr('height', 12).attr('fill', color(st));
    g.append('text').attr('x', 18).attr('y', 10).attr('class', 'label').text(st);
    ly += 16;
  }
}

function stratumOf(r, appState) {
  if (STATE.stratifyBy === 'school') {
    const s = appState.schoolById.get(r.school);
    return s?.display_name ?? r.school;
  }
  if (STATE.stratifyBy === 'grade') {
    return r.grade_level || 'unknown';
  }
  return 'all';  // 'none' = single stratum
}

function doExport() {
  const svg = document.querySelector('#sk-host svg');
  if (!svg) return;
  exportSvgPng(svg, `sankey_by_${STATE.stratifyBy}`, {
    view: 'sankey',
    stratify_by: STATE.stratifyBy,
    note: 'Aggregate response funnel; individual-level retention not available.',
    generated_at: new Date().toISOString(),
  });
}
