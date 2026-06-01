# Calibrated Claims: Conformal Prediction Meets Sports Betting Market Efficiency

# Overview
A study of soccer betting market efficiency across 9 European leagues (2015–2022), using conformal prediction and simulation-based uncertainty quantification.

Betting markets are often thought of highly efficient markets, meaning that the prices should reflect true outcome probabilities. A widely documented violation of this efficiency though is the favorite-longshot bias (FLB) where favorites are underpriced relative to their true win probability, and longshots (the underdogs) are overpriced. Two recent papers give interesting ideas on this idea though and are what inspired this project. 

Hegarty & Whelan (2024) show that the standard test for FLB is methodologically biased, and Winkelmann et al. (2024) show that the per-league, per-season analyses common in literature actually have some severe multiple-testing and statistical-power problems. So my main question is this project was to which sports betting markets can be still be called efficient (and whether they really have FLB) once they are tested more robustly with proper uncertainty quantification, multiple-testing correction, and power analysis?

## Approach and Methods

I started by replicating the Hegarty & Whelan FLB regression across 9 European soccer leagues, then applied Winkelmann's critique on my own results via Bonferroni/BH-FDR correction, analytical power analysis, and a direct null simulation. 

First step was devigging the bookmaker odds (ie removing  built-in profit margin to turn the raw prices into actual probabilities) using four methods (normalized, additive, power, and Shin) with the normalized estimator as the primary measure. To test for favorite-longshot bias, I ran a weighted least squares regression with match-level cluster-robust standard errors, since the three outcomes of a match are mechanically correlated. Then I had to correct for testing nine leagues at once using Bonferroni and BH-FDR. I assessed each null result with simulation-based power analysis, and verified the test's calibration with a direct null simulation. 

Separately, I benchmarked the market against a LightGBM multiclass classifier to quantify how much real information the market's prices contain. I trained it with walk-forward cross-validation to avoid lookahead and recalibrated the outputs with post-hoc isotonic regression. Then wrapped it in split and Mondrian conformal prediction to compare model and market on equal footing. Also attached bootstrap confidence intervals to every reported metric.

## Data
I used closing-odds and match-result data for 9 European soccer leagues (2013-2024) from https://www.football-data.co.uk/data.php (8,538 total matches).

## Key Findings

1. FLB is present in the pooled data (γ = +0.046, p < 0.001) but after correcting for testing 9 leagues simultaneously, only Serie A was still statistically significant. Supports Winkelman's prediction suggesting that most individual league findings are fragile under robust testing.

2. A null result is not an efficiency result: the Premier League is underpowered to detect a pooled-size bias, so "no FLB in the Premier League" is a statement about sample size, not market efficiency.

3. The market out-predicts a carefully calibrated ML model, and the gap is statistically real — evidence that prices encode information (injuries, lineups, betting flow) beyond team-level featur

## Key findings

### 1. Favorite-longshot bias exists in the data — but survives multiple-testing correction only for Serie A

Pooled across 18,538 matches: **γ = +0.046** (95% CI [+0.021, +0.070]), p < 0.001. γ > 0 means favorites are systematically underpriced — returns on favorites exceed returns on longshots.

After Bonferroni correction for 9 simultaneous league-level tests, only **Serie A (I1, γ = +0.114)** remains clearly significant. League 1 England (E2, γ = +0.221) is borderline under BH-FDR (q = 0.06). The English Championship's apparent significance at p = 0.051 vanishes under any reasonable correction — demonstrating Winkelmann et al.'s multiple-testing concern directly on this dataset.

The inverse-odds estimator used in much of the earlier literature gives a pooled γ of −0.003 (p = 0.81), absorbing the bias signal into the overround. Normalized probabilities, as H&W recommend, recover the correct sign and magnitude.

### 2. "No FLB in the Premier League" is a power statement, not an efficiency statement

Premier League (E0): MDE = **0.086** at 80% power. The pooled effect (0.046) is smaller than this threshold — if the Premier League had FLB at exactly the pooled level, we'd detect it only **32% of the time**. Bundesliga (D1) and La Liga (SP1) face similar constraints.

The honest conclusion is not "these leagues are efficient" but "we cannot rule out FLB smaller than 0.086 in the Premier League given the available data."

### 3. The betting market genuinely outperforms a calibrated ML model

A LightGBM classifier trained on Elo ratings, 5-match rolling form, and rest days achieves a Brier score of **0.213 raw** and **0.205 after isotonic calibration** (walk-forward CV, 2016–2022). The market achieves **0.195**, with non-overlapping bootstrap CIs. The market also has half the ECE (0.006 vs 0.012 calibrated).

Raw LightGBM probabilities are predictably uncalibrated — isotonic post-hoc calibration closes 89% of the ECE gap. The remaining **~10% of the gap and the full Brier gap** represent the market's genuine information advantage: prices aggregate injury news, lineup signals, and betting flow that team-level features cannot.

At the same 90% conformal coverage level, the market's prediction sets are 0.14–0.21 outcomes smaller than the calibrated model's, with the gap smallest in League 1 (E2) — the least efficient market in the FLB analysis.

### 4. The parametric test is well-calibrated under the efficient-markets null

A simulation-based null check (2,000 draws per league from the market-implied distribution) confirms that the cluster-robust normal approximation is accurate: simulation-to-parametric p-value ratios are 1.00–1.25 for 8 of 9 leagues. The inflation Winkelmann et al. diagnose for season-by-season analyses is largely absent here because we pool across seasons within each league and use cluster-robust standard errors.

The joint test across all 9 leagues simultaneously is significant: **p = 0.010** (max |t| statistic), confirming the dataset is collectively inconsistent with full market efficiency without any multiple-testing adjustment.

---

## Data

**Soccer:** [football-data.co.uk](https://www.football-data.co.uk/data.php) — one CSV per league per season. 9 European leagues (D1, E0, E1, E2, F1, I1, N1, SC0, SP1), seasons 2013/14–2025/26 depending on league. H&W replication uses 2015/16–2021/22.

**Tennis:** [tennis-data.co.uk](http://www.tennis-data.co.uk/alldata.php) — one XLSX per tour per year. Loader implemented and tested on synthetic data; real data not yet loaded.

All raw data is gitignored. See "Adding real data" below.

---

## Methods summary

| Component | What it does |
|-----------|-------------|
| **Devigging** | Four methods: normalized (H&W's preferred), additive, power, Shin (1992). Normalized probabilities are the theoretically correct estimator under strong-form efficiency. |
| **H&W replication** | WLS regression of `Y_ij − P^N_ij` on `P^N_ij`, cluster-robust SEs at the match level (H/D/A outcomes within a match are mechanically correlated). Bonferroni and BH-FDR correction for 9 simultaneous league tests. |
| **Predictive model** | LightGBM multiclass with Elo ratings, 5-match rolling form, and rest days. Walk-forward expanding-window CV — never shuffled. Post-hoc isotonic calibration on the prior season's predictions. |
| **Conformal wrapper** | Split conformal (marginal guarantee) and Mondrian by league (conditional guarantee). Walk-forward calibration: test season T calibrated on T−1. Compares model vs. market prediction set sizes. |
| **Calibration metrics** | Brier score, log-loss, ECE with 1,000-bootstrap CIs (match-level resampling). Reliability diagrams saved as both PNG and CSV. |
| **Power analysis** | Analytical MDE = (z_{α/2} + z_{1−β}) × SE_cluster. Simulation validation for E0 confirms formula accurate to within 2.5 percentage points at the MDE. |
| **Null simulation** | 2,000 draws per league from Categorical(P^N_iH, P^N_iD, P^N_iA). Pre-computed projection matrix M = (X'WX)^{−1}X'W makes each simulation a single matrix–vector multiply (2,000 sims × 9 leagues in ~0.5s). |

---

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Running tests

```bash
pytest                          # 127 tests, ~10 seconds
```

## Smoke test (no real data needed)

Generates synthetic data in the real file formats, runs the full pipeline, checks all invariants:

```bash
python scripts/smoke_test.py
```

## Adding real data

Drop soccer CSVs and tennis XLSXs anywhere under `data/raw/`. The loaders tolerate arbitrary subfolder layouts and recover season from the `Date` column when not in the filename:

```bash
python -c "
from src.loaders import load_soccer, load_tennis
load_soccer('data/raw', 'data/processed', recursive=False)  # recursive=False skips synthetic subdir
load_tennis('data/raw', 'data/processed')
"
```

## Running the full analysis

Scripts run in order; each reads parquet files written by earlier steps:

```bash
python scripts/run_replication.py         # H&W FLB regression + multiple-testing correction
python scripts/run_model.py               # LightGBM walk-forward CV
python scripts/run_conformal.py           # Conformal prediction set sizes
python scripts/run_calibration.py         # Brier, ECE, reliability diagrams
python scripts/run_calibration_ablation.py # Post-hoc calibration comparison
python scripts/run_power_analysis.py      # MDE table + power curves
python scripts/run_null_simulation.py     # Efficient-markets null simulation
```

---

## Project layout

```
src/
  devig.py        — four devigging methods (normalized, additive, power, Shin)
  synth.py        — synthetic data generator (efficient and FLB variants)
  loaders.py      — soccer and tennis loaders → harmonized Parquet
  replication.py  — H&W WLS regression, multiple-testing correction
  features.py     — Elo, rolling form, rest days (walk-forward, no lookahead)
  model.py        — LightGBM walk-forward CV
  conformal.py    — split conformal and Mondrian conformal
  calibration.py  — Brier score, ECE, reliability diagram data
  postcal.py      — isotonic and Platt post-hoc calibration
  power.py        — analytical MDE and simulation-based power curves
  null_sim.py     — efficient-markets null simulation

tests/            — 127 tests; every nontrivial function validated on synthetic
                    data with known ground truth before trusting on real data

scripts/          — one script per analysis step; reads/writes Parquet and CSV
notes/            — per-phase process log: what was built, decisions, what failed

results/
  tables/         — CSV and Markdown tables for every reported result
  figures/        — reliability diagrams, power curves, null distributions
```

---

## Anchor papers

- **Hegarty & Whelan (2024)**, *Sports Economics Review* 8.100042. Shows the standard inverse-odds test for market efficiency is biased toward accepting the null. Recommends normalized probabilities. Finds substantial FLB in soccer and tennis.
- **Winkelmann et al. (2024)**, *Journal of Sports Economics* 25(1). Shows via Monte Carlo that season-by-season betting market analyses routinely produce false-positive significance findings (77.6% false-positive rate over 14 seasons). This project applies their critique to its own league-level analysis via Bonferroni correction, power analysis, and direct null simulation.
