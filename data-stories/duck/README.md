# The Duck That's Complicating California's Grid

A data story about how the rapid buildout of solar generation has reshaped California's electricity grid over the past nine years, and what grid-scale batteries are doing about it.

**Author:** Sam Macuga
**Course:** PSYC 81.09 — Storytelling with Data
**Instructor:** Professor Jeremy Manning
**Institution:** Dartmouth College
**Term:** Spring 2026

---

## What's in this submission

- **`duck_curve_analysis.ipynb`** — Jupyter notebook with the full analysis: data loading, processing, and five figures showing the duck curve story across 2018–2026. The YouTube video link is included in the notebook's opening cell.
- **`CAISO_data.zip`** — 90 CSVs from CAISO's Today's Outlook dashboard (45 weekdays × 2 file types: net demand and supply). Covers April 14–18 of each year from 2018 to 2026.
- **`README.md`** — This file.

The YouTube video is the main deliverable and tells the story for a general audience. The notebook is the supporting analysis showing how every claim in the video is derived from the data.

---

## How to run the notebook

The notebook is written for Google Colab. Local Jupyter should also work but is untested.

1. Open `duck_curve_analysis.ipynb` in Google Colab.
2. Upload `CAISO_data.zip` to the Colab session — drag it into the file panel on the left side of the screen, or use the upload button. It should land at `/content/CAISO_data.zip`.
3. Run the cells in order, top to bottom. The first code cell unzips the data; subsequent cells load it, run the analysis, and render Figures 0 through 4.

No other setup needed. All required libraries (`pandas`, `numpy`, `matplotlib`, `scipy`) are preinstalled in Colab.

---

## What the analysis does

The notebook compares an average spring weekday across nine consecutive years (2018–2026) using 5-minute resolution operating data from CAISO. For each year, the five April 14–18 weekdays are averaged into one representative daily profile, then aggregated to hourly resolution.

Five figures, each its own narrative beat:

- **Figure 0** — California electricity demand on a normal spring day, showing the underlying demand shape before any renewable subtraction comes into play.
- **Figure 1** — The same day with net load added underneath. The gap between demand and net load is what renewables are covering.
- **Figure 2** — The 2026 net load by itself, with the evening ramp ("the cliff") measured and labeled.
- **Figure 3** — Net load curves for all nine years overlaid, showing the belly dropping from +9 GW in 2018 to −6 GW in 2026.
- **Figure 4** — The 2026 net load with and without batteries, showing the shaded regions where batteries charge (midday) and discharge (evening).

---

## Data source

All data comes from [CAISO's Today's Outlook dashboard](https://www.caiso.com/todays-outlook). The dashboard provides 5-minute resolution operating data for California's electricity grid, including demand, supply by fuel type, and battery dispatch. See the Data section of the notebook for full methodological notes, including how CAISO defines "demand" (it is net of behind-the-meter rooftop solar).

---

## Acknowledgements

- **Data:** CAISO Today's Outlook dashboard.
- **Image credit (video opening):** PondCo, ["Designing Electrical Substations for a Modernized Energy Grid."](https://www.pondco.com/blog/designing-electrical-substations-for-a-modernized-energy-grid)
- **AI assistance:** Anthropic's Claude was used for iterative discussion of the narrative framing, figure design, and writing. Google's Gemini (built into Colab) was used for code generation and notebook editing. All analytical decisions, narrative choices, and interpretations are my own.
- **Thanks** to Professor Jeremy Manning and the PSYC 81.09 cohort for feedback throughout the term.
