// Custom view — sub-tab dispatcher for four figures:
//  1. Recipe sweetness vs. learn-sentiment
//  2. Support count vs. reflection sentiment
//  3. Themes from "how will you apply"
//  4. Dropout / retention analysis (built by sub-agent)

import { escapeHTML } from '../app.js';
import { renderRecipeVsLearn } from './custom-recipe-learn.js';
import { renderSupportVsSentiment } from './custom-support-sentiment.js';
import { renderApplicationThemes } from './custom-app-themes.js';
import { renderDropout } from './dropout.js';

const SUB_VIEWS = [
  { id: 'recipe-learn',     label: 'Recipe ↔ learn',          render: renderRecipeVsLearn },
  { id: 'support-sentiment', label: 'Support count ↔ feeling', render: renderSupportVsSentiment },
  { id: 'app-themes',       label: 'Application themes',      render: renderApplicationThemes },
  { id: 'dropout',          label: 'Dropout analysis',        render: renderDropout },
];

const STATE = { active: 'recipe-learn' };

export function renderCustom(root, state) {
  root.innerHTML = '';
  const wrap = document.createElement('div');
  wrap.innerHTML = `
    <h1>Custom figures</h1>
    <p class="lede">Four exploratory figures answering specific cross-cutting questions about the dataset.</p>
    <div class="panel" style="padding: 8px 14px;">
      <div id="custom-tabs" style="display: flex; gap: 6px; flex-wrap: wrap;"></div>
    </div>
    <div id="custom-host"></div>
  `;
  root.appendChild(wrap);

  const tabs = document.getElementById('custom-tabs');
  for (const sv of SUB_VIEWS) {
    const chip = document.createElement('span');
    chip.className = 'chip ' + (sv.id === STATE.active ? 'active' : 'muted');
    chip.tabIndex = 0;
    chip.textContent = sv.label;
    chip.addEventListener('click', () => {
      STATE.active = sv.id;
      renderCustom(root, state);
    });
    chip.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); chip.click(); }
    });
    tabs.appendChild(chip);
  }

  const host = document.getElementById('custom-host');
  const sv = SUB_VIEWS.find(s => s.id === STATE.active);
  try {
    sv.render(host, state);
  } catch (err) {
    console.error('[custom]', sv.id, err);
    host.innerHTML = `<div class="empty-state">Sub-view <code>${escapeHTML(sv.id)}</code> failed: ${escapeHTML(err.message)}</div>`;
  }
}
