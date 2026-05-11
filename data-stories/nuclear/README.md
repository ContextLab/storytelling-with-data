# The Only Winning Move: Eighty Years of Nuclear Arsenals

A data story tracing US and USSR/Russian nuclear arsenals from 1945 through 2024, separating two metrics that are usually conflated: how many warheads each country held, and how much destructive capacity those warheads represented.

## Project information

**Author:** Sam Macuga (GitHub: smacuga19)

**Course:** PSYC 81.09, Storytelling with Data, Dartmouth College, 2026

## Overview

### Main question

What does the data on nuclear arsenals from 1945 to today show, and how does the story differ depending on whether we measure warhead counts or total destructive capacity?

### Approach

I compiled annual data on warhead counts and total megatonnage for the United States and USSR/Russia from 1945 through 2024, drawing on Johnston's Archive (which reconciles multiple authoritative sources for the historical period) and the Federation of American Scientists Nuclear Notebook for recent years. The primary visualization is a Plotly animated bubble chart in the Hans Rosling style: each country is a bubble that moves through 2D space over time. Position on the x-axis shows warhead count; position on the y-axis (log scale) shows average yield per warhead; bubble size shows total destructive megatonnage. Two static figures (a two-panel time series and a trajectory plot) show the same data from complementary angles.

### Findings

Total destructive capacity peaked years before warhead count peaked. US megatonnage peaked in 1960 at over 20,000 megatons — seven years before the US warhead count peaked at 32,500 in 1967. Soviet megatonnage peaked in 1975 at 19,400 megatons — ten years before the Soviet warhead count peaked at 45,000 in 1985.

The decline in megatonnage and the decline in warhead counts followed different timelines, driven by different mechanisms. Megatonnage fell as missile accuracy improved and very large yields became unnecessary. Warhead counts fell later, after the end of the Cold War and the signing of bilateral arms control treaties (SALT, START, SORT, New START). The treaties capped warhead counts but did not directly cap destructive yield.

The era of formal arms control between the US and Russia ended in February 2026. New START, the most recent treaty, expired without a successor. The two countries have informally agreed to keep observing the treaty's limits while they negotiate a replacement, but the arrangement is voluntary and not legally binding. For the first time since 1972, there is no formal cap on either country's strategic nuclear arsenal.

## Video

YouTube: [https://youtu.be/hJDVfCPZOYc](https://youtu.be/u_0ErPb7Ntw)

The video opens with a short clip from the 1983 film *WarGames* and uses the bubble chart's 1983 frame — the year the film was released — as the visual entry point before the animation rewinds to 1945 and plays forward through 2024, with narration extending to the February 2026 expiration of New START. See the *Note on the video* section of the notebook for a full description of the video's structure and a media-attribution / fair-use statement.

## Data

The dataset combines two sources to span 1945 through 2024.

The primary historical source is Johnston's Archive, specifically:

- United States, warheads and megatonnage, covering 1945–2012
- USSR/Russia, warheads and megatonnage, covering 1949–2007

Wm. Robert Johnston compiled these estimates by reconciling multiple authoritative sources, including the Natural Resources Defense Council Nuclear Weapons Databook (1984, 1989, 1994, 1995, 2000, 2002, 2006), Department of Energy declassified figures (1994), and reports from senior US defense officials.

For the years after Johnston's compilation ends — 2013–2024 for the US and 2008–2024 for Russia — I supplement with warhead count estimates from the Federation of American Scientists Nuclear Notebook and the SIPRI Yearbook 2025. Megatonnage for these years is not directly published; I estimate it by extrapolating the average-yield-per-warhead trend from the late Johnston period, accounting for the documented retirement of high-yield weapons (such as the B83-1).

The compiled dataset is stored in this folder as `nuclear_yields.csv`. Each row contains one country's estimated warhead count, total megatonnage, and a source flag (Johnston or FAS+estimate) for one year.

## Files in this folder

- `nuclear_arsenals.ipynb` — the project notebook (analysis, visualizations, narrative)
- `nuclear_yields.csv` — the compiled dataset, 156 rows × 5 columns (`country`, `year`, `warheads`, `megatons`, `source`)
- `README.md` — this file

## Running the code

The notebook is designed to run in Google Colab without any local setup. Open it in Colab and run all cells in order; the data-loading cell tries the local CSV first and falls back to a GitHub raw URL if no local file is present.

If you prefer a local environment, the notebook requires pandas, numpy, matplotlib, and plotly. All four are standard scientific-Python packages and ship with most Anaconda distributions.

## Acknowledgements

**Primary historical data source.** Johnston's Archive: Nuclear Stockpile Estimates, compiled by Wm. Robert Johnston (last modified 2007).

**Recent-year data sources.** Federation of American Scientists Nuclear Notebook (Kristensen, Korda, Norris, Johns, and Knight, 2024) for warhead counts after 2007. SIPRI Yearbook 2025 for current arsenal figures and modernization trends. *The Future of US Nuclear Weapons Policy* (National Academy of Sciences, 1997) for context on the technological shift toward smaller, more accurate warheads.

**Post-treaty reporting.** Information about the February 2026 expiration of New START and the subsequent informal arrangement between the US and Russia comes from reporting by the Arms Control Association, the Council on Foreign Relations, NPR, PBS NewsHour, and Axios.

**Cultural reference and video media.** The accompanying video opens with a short clip from the 1983 film *WarGames* (directed by John Badham, MGM) and closes with a montage from the end of the same film — the WOPR simulation sequence ending in the line "The only winning move is not to play," which the project title draws on. Both clips are used briefly under fair use (17 U.S.C. § 107) for purposes of criticism, commentary, and educational analysis. See the *Note on the video* section of the notebook for full details.

**Visualization style.** The bubble chart animation is inspired by the work of Hans Rosling.

**AI assistance.** This project was developed with help from two AI tools. Anthropic's Claude was used for iterative discussion of narrative framing, data visualization design, animation logic, and writing assistance. Google's Gemini (built into Colab) was used for code generation and notebook editing. All analytical decisions, final narrative choices, and interpretations of the data are my own.

**Thanks.** To Professor Jeremy Manning and PSYC 81.09 (Storytelling with Data) at Dartmouth College.
