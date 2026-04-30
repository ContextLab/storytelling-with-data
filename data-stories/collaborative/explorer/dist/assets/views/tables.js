// T029-T032: Tables view — virtualized table with full-question tooltips,
// expandable freetext cells, per-column summary side panel, and schema-diff panel.

import { openSidePanel, escapeHTML } from '../app.js';

const TRUNC = 220;  // chars before truncation
let _tabulator = null;

export function renderTables(root, state) {
  const wb = state.workbookById.get(state.currentWorkbookId);
  const sheet = state.sheetById.get(state.currentSheetId);
  if (!sheet) {
    root.innerHTML = '<div class="empty-state">Pick a workbook and sheet from the top bar.</div>';
    return;
  }

  const rows = state.responsesBySheet.get(sheet.id) || [];
  const cols = sheet.column_ids
    .map(cid => state.columnById.get(cid))
    .filter(Boolean);

  // Build the header
  const wrap = document.createElement('div');
  wrap.innerHTML = `
    <h1>${escapeHTML(wb?.title ?? '')}</h1>
    <p class="lede">${escapeHTML(sheet.period_label)} · ${rows.length} responses · ${cols.length} columns</p>
    <div class="table-toolbar">
      <span class="stat">rows: <strong>${rows.length}</strong></span>
      <span class="stat">columns: <strong>${cols.length}</strong></span>
      <span class="stat">source: <strong>${sheet.source_row_count}</strong> · usable: <strong>${sheet.usable_row_count}</strong></span>
      <span style="flex:1"></span>
      ${wb?.kind === 'core_measures'
        ? '<button id="btn-schema-diff" type="button">schema diff…</button>' : ''}
      <button id="btn-export-csv" type="button">export CSV</button>
    </div>
    <div id="tabulator-host"></div>
  `;
  root.appendChild(wrap);

  // Filter rows by global filters (school, grade, freetext search)
  const filtered = applyFilters(rows, state, cols);

  // Build Tabulator columns
  const tabCols = cols.map(c => columnDef(c, state));

  // Map response rows → flat objects keyed by sanitized field id
  const tabData = filtered.map(r => {
    const row = { __response_id: r.id };
    for (const cid of sheet.column_ids) {
      row[fieldKey(cid)] = r.values[cid] ?? null;
    }
    return row;
  });

  if (_tabulator) { try { _tabulator.destroy(); } catch (_) {} _tabulator = null; }
  _tabulator = new Tabulator('#tabulator-host', {
    data: tabData,
    columns: tabCols,
    layout: 'fitDataStretch',
    height: '100%',
    movableColumns: true,
    resizableColumns: true,
    placeholder: '<div class="empty-state">No rows match the active filters.</div>',
    rowHeight: 30,
    virtualDomBuffer: 320,
  });

  // Bind toolbar buttons
  document.getElementById('btn-schema-diff')?.addEventListener('click', () => {
    showSchemaDiff(state, wb);
  });
  document.getElementById('btn-export-csv')?.addEventListener('click', () => {
    _tabulator?.download('csv', `${sheet.id}.csv`);
  });
}

function fieldKey(colId) {
  // Tabulator treats `.` as nested object access; replace with `__`
  return colId.replace(/\./g, '__');
}

function columnDef(col, state) {
  const isFreeText = col.inferred_type === 'freetext';
  const display = `<span class="mono" title="${escapeAttr(col.original_header)}">${escapeHTML(col.display_header)}</span>`;
  const headerHtml = `${display} <span class="col-id" style="opacity:.5">ⓘ</span>`;
  return {
    title: headerHtml,
    field: fieldKey(col.id),
    headerSort: false,
    headerTooltip: col.original_header,
    headerClick: (e, column) => {
      showColumnSummary(state, col);
    },
    formatter: isFreeText ? freetextFormatter : defaultFormatter,
    cellClick: isFreeText ? (e, cell) => {
      const ft = cell.getElement().querySelector('.freetext-cell');
      if (!ft) return;
      const isExpanded = ft.dataset.expanded === '1';
      const tail = ft.querySelector('.ft-tail');
      const aff = ft.querySelector('.expand-affordance');
      if (!tail) return;
      if (isExpanded) {
        tail.style.display = 'none';
        if (aff) aff.textContent = '…show more';
        ft.dataset.expanded = '0';
      } else {
        tail.style.display = '';
        if (aff) aff.textContent = '   show less';
        ft.dataset.expanded = '1';
      }
    } : undefined,
    minWidth: isFreeText ? 280 : 110,
    maxInitialWidth: isFreeText ? 420 : 220,
  };
}

function defaultFormatter(cell) {
  const v = cell.getValue();
  if (v === null || v === undefined) return '<span style="color:var(--ink-soft)">—</span>';
  return escapeHTML(String(v));
}

function freetextFormatter(cell) {
  const v = cell.getValue();
  if (v === null || v === undefined || v === '') return '<span style="color:var(--ink-soft)">—</span>';
  const s = String(v);
  if (s.length <= TRUNC) return `<div class="freetext-cell">${escapeHTML(s)}</div>`;
  const head = s.slice(0, TRUNC);
  const tail = s.slice(TRUNC);
  return `<div class="freetext-cell" data-expanded="0">
    <span class="ft-head">${escapeHTML(head)}</span><span class="ft-tail" style="display:none">${escapeHTML(tail)}</span>
    <span class="expand-affordance">…show more</span>
  </div>`;
}

// Cell-click toggle for freetext expansion — capture phase so Tabulator's
// stopPropagation doesn't swallow the event.
document.addEventListener('click', (e) => {
  const ft = e.target.closest('.freetext-cell');
  if (!ft) return;
  const isExpanded = ft.dataset.expanded === '1';
  const tail = ft.querySelector('.ft-tail');
  const aff = ft.querySelector('.expand-affordance');
  if (!tail) return;
  if (isExpanded) {
    tail.style.display = 'none';
    if (aff) aff.textContent = '…show more';
    ft.dataset.expanded = '0';
  } else {
    tail.style.display = '';
    if (aff) aff.textContent = '   show less';
    ft.dataset.expanded = '1';
  }
}, true);  // capture phase

function showColumnSummary(state, col) {
  const measure = col.measure_id ? state.measureById.get(col.measure_id) : null;
  const tv = (col.top_values || []).map(t =>
    `<div class="row"><span>${escapeHTML(String(t.value))}</span><span class="num">${t.count}</span></div>`
  ).join('');
  const html = `
    <h3>${escapeHTML(col.display_header)}</h3>
    <div class="question">${escapeHTML(col.original_header)}</div>
    <div class="stat-row"><span class="k">type</span><span class="v">${escapeHTML(col.inferred_type)}</span></div>
    <div class="stat-row"><span class="k">% missing</span><span class="v">${col.missing_pct.toFixed(1)}%</span></div>
    <div class="stat-row"><span class="k">column id</span><span class="v">${escapeHTML(col.id)}</span></div>
    ${col.rtu_session ? `
      <div class="stat-row"><span class="k">RTU session</span><span class="v">${escapeHTML(col.rtu_session)}</span></div>
      <div class="stat-row"><span class="k">RTU role</span><span class="v">${escapeHTML(col.rtu_role)}</span></div>
      <div class="stat-row"><span class="k">RTU instance</span><span class="v">${col.rtu_instance}</span></div>
    ` : ''}
    ${measure ? `
      <div style="margin-top:14px;padding:10px;background:var(--seq-1);border-left:3px solid var(--cat-3);">
        <div class="panel-title">canonical measure</div>
        <strong>${escapeHTML(measure.display_name)}</strong>
        <div class="question" style="margin-top:6px">${escapeHTML(measure.description)}</div>
        <div style="font-family:var(--font-mono);font-size:11px;margin-top:6px;color:var(--ink-soft)">
          scale: ${escapeHTML(measure.value_scale_canonical)}${measure.scale_mixed ? ' · <strong style="color:var(--bonfire-orange)">scale changed across years</strong>' : ''}
        </div>
      </div>` : ''}
    <h3 style="margin-top:18px;font-size:14px">Top values</h3>
    <div class="topvals">${tv || '<em style="color:var(--ink-soft)">no values</em>'}</div>
  `;
  openSidePanel(html);
}

function showSchemaDiff(state, wb) {
  const drift = (state.bundle.schema_drift || []).find(d => d.workbook_id === wb.id);
  if (!drift) {
    openSidePanel(`<h3>Schema diff</h3><div class="empty-state">No drift records for ${escapeHTML(wb.title)}.</div>`);
    return;
  }
  const fmtList = (arr) => arr.length === 0
    ? '<em style="color:var(--ink-soft)">none</em>'
    : '<ul style="padding-left:18px">' + arr.map(r =>
        `<li><span class="mono" style="font-size:11px;color:var(--ink-soft)">${escapeHTML(r.sheet_id)}</span><br/>${escapeHTML(r.original_header)}</li>`
      ).join('') + '</ul>';

  openSidePanel(`
    <h3>Schema drift — ${escapeHTML(wb.title)}</h3>
    <div class="question">Columns added or removed across years (consecutive sheets).</div>
    <h3 style="margin-top:18px;font-size:14px">Added (${drift.added.length})</h3>
    ${fmtList(drift.added)}
    <h3 style="margin-top:18px;font-size:14px">Removed (${drift.removed.length})</h3>
    ${fmtList(drift.removed)}
  `);
}

function applyFilters(rows, state, cols) {
  const fs = state.filters.schools;
  const fg = state.filters.grades;
  const q = (state.filters.freetextQuery || '').trim();
  const ftCols = cols.filter(c => c.inferred_type === 'freetext').map(c => c.id);

  return rows.filter(r => {
    if (fs.size > 0 && !fs.has(r.school)) return false;
    if (fg.size > 0 && !fg.has(r.grade_level)) return false;
    if (q) {
      const hay = ftCols.map(cid => String(r.values[cid] ?? '')).join(' ').toLowerCase();
      if (!hay.includes(q)) return false;
    }
    return true;
  });
}

function escapeAttr(s) {
  return String(s ?? '').replace(/"/g, '&quot;').replace(/</g, '&lt;');
}
