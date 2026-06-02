# Soccer Betting Market Efficiency Modeling

# Overview
A study of soccer betting market efficiency across 9 European leagues (2015–2022), using conformal prediction and simulation-based uncertainty quantification.

Most people think of betting markets as highly efficient markets, meaning that the prices generally reflect true outcome probabilities. A well known violation of this efficiency though is the favorite-longshot bias (FLB) where favorites are underpriced relative to their true win probability, and longshots (the underdogs) are overpriced. I read two papers recently that both have interesting ideas on this topic and are what inspired this project. 

Hegarty & Whelan (2024) show that the standard test for FLB is methodologically biased, and Winkelmann et al. (2024) show that the per-league, per-season analyses common in literature actually has some severe multiple-testing and statistical-power problems. So my main question in this project was to see which sports betting markets can still be called efficient (and whether they really have FLB) once they are tested more robustly with proper uncertainty quantification, multiple-testing correction, null simulations, and power analysis.

Link to video: https://youtu.be/75sMtEiYkBM 

## Approach and Methods

I started by replicating the Hegarty & Whelan FLB regression across 9 European soccer leagues, then applied Winkelmann's critique on my own results via Bonferroni/BH-FDR correction, analytical power analysis, and a direct null simulation. 

First step was devigging the bookmaker odds (ie removing  built-in profit margin to turn the raw prices into actual probabilities) using four methods (normalized, additive, power, and Shin) with the normalized estimator as the primary measure. To test for favorite-longshot bias, I ran a weighted least squares regression with match-level cluster-robust standard errors, since the three outcomes of a match are correlated. Then I had to correct for testing nine leagues at once using Bonferroni and BH-FDR. I assessed each null result with simulation-based power analysis, and verified the test's calibration with a direct null simulation. 

Separately, I benchmarked the market against a LightGBM multiclass classifier to quantify how much real information the market's prices contain. I trained it with walk-forward cross-validation to avoid lookahead and recalibrated the outputs with post-hoc isotonic regression. Then wrapped it in split and Mondrian conformal prediction to compare model and market on equal scale. Also attached bootstrap confidence intervals to every reported metric.

## Data
I used closing-odds and match-result data for 9 European soccer leagues (2013-2024) from https://www.football-data.co.uk/data.php 8,538 total matches, one CSV per league per season. 

## Key Findings

1. FLB is present in the pooled data (γ = +0.046, p < 0.001) but after correcting for testing 9 leagues simultaneously, only Serie A was still statistically significant. Supports Winkelman's prediction suggesting that most individual league findings are fragile under robust testing.

2. Even though I got a null result for the other 8 leagues, it doesn't necessarily mean those markets are definitely efficient. My sample size was ultimately not big enough for the null result conclusively say there is no FLB. 

3. The market was a better predictor then my calibrated ML model, and the gap in performance was statistically significant. Suggests that prices take into account a lot of information such as injuries, lineups, etc beyond the team-level features I was able to encode in my model.


## Running the code
 
### Setup
 
```bash
python3 -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```
 
### Verify the install
 
```bash
pytest                          # 127 tests
python scripts/smoke_test.py    # generates synthetic data, runs the full pipeline end-to-end
```

Smoke test generates synthetic data and runs the entire pipeline so you can confirm the code works before actually using any real data.
 

### Running the full analysis
 
Each script reads the Parquet files written by earlier steps, so run them in order. Approximate runtimes are for a 2020 MacBook Pro:
 
```bash
python scripts/run_replication.py          # ~1 min  — H&W regression + multiple-testing correction
python scripts/run_model.py                # ~1 min  — LightGBM walk-forward CV
python scripts/run_conformal.py            # ~5 sec  — conformal prediction set sizes
python scripts/run_calibration.py          # ~2 min  — Brier, ECE, reliability diagrams (n_boot=1000)
python scripts/run_calibration_ablation.py # ~3 min  — post-hoc calibration comparison
python scripts/run_power_analysis.py       # ~5 min  — MDE table + simulation validation
python scripts/run_null_simulation.py      # ~5 sec  — efficient-markets null simulation
```

## Next Steps

- I want to expand the dataset and look at different sports betting markets and see if results are consistent or if different patterns emerge.
- Also can extend the model's feature set. Currently there's a lot of information not being captured likeinjuries, confirmed lineups, general game trends, etc. Not sure how would add a lot of these though.
- Potentially try pooling leagues in a hierarchical model. For example a partial-pooling (random-effects) model across leagues that could potentially estimate league-level FLB instead of doing the independent tests like I am now.


## Acknowledgements

- **Hegarty & Whelan (2024)**, *Sports Economics Review* 8.100042. Shows the standard inverse-odds test for market efficiency is biased toward accepting the null. Recommends normalized probabilities and finds substantial FLB in soccer and tennis markets.
- **Winkelmann et al. (2024)**, *Journal of Sports Economics* 25(1). Shows via Monte Carlo that season-by-season betting market analyses routinely produce false-positive significance findings (77.6% false-positive rate over 14 seasons). For this project I applied their critique to my own league-level analysis via Bonferroni correction, power analysis, and null simulation.
