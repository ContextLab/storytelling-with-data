# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is the course repository for **Storytelling with Data (PSYC 81.09)** at Dartmouth College, taught by Jeremy Manning. It is an Open Course — all materials are public and Python-based. The canonical upstream is `ContextLab/storytelling-with-data`.

The course site is built as a **GitHub Pages static site** with automated CI/CD.

## Structure

- **index.html** — Landing page (hub) with course outline, nav to spoke pages
- **css/** — `base-styles.css` (Dartmouth theme variables) + `site-styles.css` (layout)
- **pages/** — Spoke pages: `slides.html`, `assignments.html`, `stories.html`, `syllabus.html`
- **slides/** — Lecture slides as cdl-slides markdown (`.md` with `marp: true` frontmatter), compiled to HTML
- **slides/figs/** — All slide images (shared across decks, no remote references)
- **assignments/** — Assignment markdown files in `assignment-N/` dirs, auto-compiled to HTML + PDF
- **data/** — `stories.yaml` — metadata for data story gallery (single source of truth)
- **data-stories/** — Student data story projects (each subfolder follows `data-stories/demo/` template)
- **scripts/** — Build scripts (`build-pages.py`, `build-slides.sh`, `build-gallery.py`, `build-pdfs.py`, `extract-images.py`)
- **admin/** — Syllabus PDF and administrative documents
- **docker/** — Docker container setup (legacy, not required for site build)
- **.github/workflows/deploy-site.yml** — GitHub Actions: build + deploy to GitHub Pages

## Build Commands

```bash
# Install dependencies
pip install cdl-slides pyyaml playwright
npm install -g @marp-team/marp-cli
playwright install chromium

# Compile all slides to HTML
./scripts/build-slides.sh

# Build spoke pages + assignment HTML
python scripts/build-pages.py

# Generate data story gallery
python scripts/build-gallery.py

# Generate assignment PDFs
python scripts/build-pdfs.py

# Full local build (assemble _site/)
rm -rf _site && mkdir -p _site/css _site/pages _site/slides/figs _site/assignments _site/admin
cp index.html _site/ && cp css/*.css _site/css/ && cp pages/*.html _site/pages/
cp -r slides/figs/ _site/slides/figs/ && cp slides/*.html _site/slides/
for dir in assignments/assignment-*/; do d=$(basename "$dir"); mkdir -p "_site/assignments/$d"; cp "$dir"index.html "$dir"*.pdf "_site/assignments/$d/" 2>/dev/null; done
cp admin/*.pdf _site/admin/ 2>/dev/null && touch _site/.nojekyll

# Preview locally
cd _site && python -m http.server 8000
```

## Slide Conventions

- All slides use cdl-slides (Marp) format with frontmatter: `marp: true`, `theme: cdl-theme`, `math: katex`
- Use semantic callout boxes instead of raw bullets: `note-box`, `definition-box`, `tip-box`, `important-box`, `warning-box`, `example-box`
- Use `<!-- _class: scale-90 -->` (or scale-80, scale-70) for dense content
- Images stored in `slides/figs/` with relative paths — no remote image references
- Diagrams recreated as SVG using CDL theme color palette

## Key Conventions

- All student code must be **Python** in **Jupyter notebooks** (.ipynb), runnable in Google Colab
- Data stories follow the `data-stories/demo/` template
- Story metadata lives in `data/stories.yaml` — adding new stories only requires editing this file
- The Python stack: numpy, pandas, matplotlib, seaborn, scikit-learn, hypertools
- CSS uses Dartmouth brand colors (`--dartmouth-green: #00693e`, `--river-blue: #267aba`, `--bonfire-orange: #ffa00f`)

## Git Workflow

- `master` is the main branch
- Upstream remote: `https://github.com/ContextLab/storytelling-with-data.git`
- Push to master triggers GitHub Actions deploy to GitHub Pages
- Students work on forks; instructor merges via per-student remotes in `add_remotes.sh`

## Active Technologies
- Markdown (cdl-slides format), HTML/CSS, YAML, cdl-slides (Marp)
- index.html is auto-generated from slides/README.md via `scripts/build-index.py`
- slides/README.md is the single source of truth for the week-by-week course schedule
- Flat files — slide markdown, assignment markdown, stories.yaml

## Recent Changes
- 003-course-schedule-refactor: Restructured from 4-module layout to week-by-week Spring 2026 schedule. Added build-index.py to auto-generate index.html from slides/README.md. Created 8 new slide decks, audited all existing decks. Deleted deprecated git1-git6 slides. Renamed lecture-1.md → truth-and-storytelling.md.
- 002-vibe-coding-curriculum: Added vibe coding slides, reworked Module 4 content, refactored Assignment 3

## Recent Changes
- 002-vibe-coding-curriculum: Added Markdown (cdl-slides format), HTML/CSS, YAML + cdl-slides (Marp), existing build pipeline from feature 001
