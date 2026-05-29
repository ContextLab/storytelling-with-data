# Why Is Measles Back?

A data story on US measles resurgence and the geography of vaccination coverage.

*PSYC 81.09: Storytelling with Data — Spring 2026*
*Dartmouth College | Professor Jeremy Manning*

**Author:** Sam Macuga
**Video:** https://youtu.be/myMGMW1ZCe4

---

## What's here

This repository contains the project artifacts:

| File | What it is |
| --- | --- |
| `measles.ipynb` | The analysis notebook. Loads CDC data, runs a Monte Carlo outbreak simulation, builds the composite figure, and walks through the interpretation. |
| `seir_simulation.py` | Neighbor-based SEIR outbreak model imported by the notebook. Same parameters as the canned HTML visualization, but lets us run the model thousands of times to characterize the *distribution* of outbreak outcomes rather than a single canned run. |
| `data/measles_cases_by_year.csv` | Annual US measles case counts, 2010–2026 (CDC). |
| `data/state_mmr_coverage_tiers.csv` | Number of states + DC in each MMR coverage tier, by school year (CDC SchoolVaxView + MMWR). |
| `measles_sim.html` | Interactive single-run SEIR visualization comparing Connecticut (98% MMR coverage) vs Idaho (78.5%). Used as the visual centerpiece of the video. |
| `r0_comparison.png` | Static figure ranking measles transmissibility against other infectious diseases. Used in Part 1 of the video. |

The notebook reads from the two CSVs in `data/` rather than hardcoding values, so updating the analysis as new CDC data is released only requires editing the CSVs.

---

## The argument, in one paragraph

US kindergarten MMR coverage dropped from 95.2% (2019–20) to 92.5% (2024–25). That national three-point drop sounds small, but it conceals a structural change in *where* the coverage gaps live. From 2011 through 2019, only 3–4 states had kindergarten MMR coverage below 90%. By the 2024–25 school year, 16 do. The pre-pandemic distribution was a stable handful of low-coverage outliers; the current distribution is widespread sub-threshold coverage. Outbreaks need a spark — an imported case landing in an undervaccinated community — and through 2024, the spark and the cluster hadn't connected at scale. In early 2025, they did: a chain that began in a low-coverage West Texas community sustained for months, spread to other states, and produced the most US measles cases since 1992. The country is now under WHO review for whether it still qualifies as having eliminated measles. The vaccine hasn't changed; what's changed is how many places are below the threshold.

---

## How to reproduce the figure

Requirements: Python 3.9+, with `pandas`, `numpy`, and `matplotlib`.

**Locally:**

```bash
pip install pandas numpy matplotlib jupyter
jupyter notebook measles_data_story.ipynb
```

Run all cells top to bottom. The composite figure is saved as `composite.png`, and the simulation histogram as `outbreak_distributions.png`, in the working directory.

**In Google Colab:**

The notebook expects `seir_simulation.py` and a `data/` folder (containing the two CSVs) next to it. In a fresh Colab session, upload everything in one of two ways:

1. Use the file panel to upload `seir_simulation.py` to `/content/`, then upload both CSVs to `/content/data/`. The notebook auto-discovers files in `/content` and `/content/measles_story`, so no code changes needed.
2. Or, if you've cloned the project to a folder, do `from google.colab import drive; drive.mount('/content/drive')` and point `DATA` at the cloned folder.

If the notebook can't find the files it raises `FileNotFoundError` with the list of locations it checked.

If a CDC release updates a value, edit the corresponding CSV in `data/` — no notebook changes required. The sanity-check cell will catch any tier mismatches before the figure is plotted.

---

## Data lineage and known limitations

**Cases (`data/measles_cases_by_year.csv`).** Pulled from the CDC's [Measles Cases and Outbreaks](https://www.cdc.gov/measles/data-research/index.html) tracker. The 2026 row is year-to-date through May 21, 2026 — it will continue updating through year-end. The `note` column flags years with notable outbreaks for narrative context.

**Coverage tiers (`data/state_mmr_coverage_tiers.csv`).** Each row gives the number of states + DC (51 jurisdictions, or 50 in years where DC wasn't separately reported) in three MMR coverage tiers, for the school year ending in the listed calendar year. Sources:

- **2011, 2012, 2018, 2019, 2020–2025**: Verified directly from the corresponding CDC MMWR annual report on kindergarten vaccination coverage. These rows are marked `verified` in the `data_quality` column.
- **2013–2017**: For these years the CDC published national-median coverage and totals, but did not publish the exact count of states in each tier. Values for these rows are interpolated between verified endpoints and are flagged `interpolated`. The overall narrative shape — flat distribution through 2019, sharp post-pandemic shift — is supported by the verified endpoints and isn't sensitive to the exact interpolated values.

**What this analysis cannot show.** State-level averages still hide local clustering. A single state with high average coverage can contain communities with very low coverage, and that's where outbreaks actually originate (NYC in 2019, West Texas in 2025). A county- or zip-code-level extension is listed under "Future directions" in the notebook; assembling a national county-level series would require pulling from individual state health departments, since the CDC publishes county-level data for some states but not others.

---

## Acknowledgments

Thanks to Professor Jeremy Manning and PSYC 81.09 (Storytelling with Data) at Dartmouth College.

This analysis was assisted by Anthropic's Claude (Claude Opus 4.7) for data verification, figure design, and notebook structure. Anthropic's Claude was also used to support the writing of the accompanying video narration script. All analytical decisions, final narrative choices, source verification, and interpretations are my own.

## Primary data sources

- CDC, *Measles Cases and Outbreaks*: https://www.cdc.gov/measles/data-research/index.html
- CDC, *SchoolVaxView*: https://www.cdc.gov/schoolvaxview/data/index.html
- CDC MMWR, *Vaccination Coverage Among Kindergartners*, annual reports 2011–12 through 2024–25.
- KFF, *Kindergarten Routine Vaccination Rates Continue to Decline* (September 2025): https://www.kff.org/medicaid/kindergarten-routine-vaccination-rates-continue-to-decline/
- PAHO, *PAHO calls for regional action as Americas lose measles elimination status* (November 2025).
- Guerra, F.M. et al. (2017). The basic reproduction number (R₀) of measles: a systematic review. *Human Vaccines & Immunotherapeutics*.
