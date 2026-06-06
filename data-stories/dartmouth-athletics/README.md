# Project information

This comes from some of data analysis work I did for the Dartmouth Athletics department, which uses Catapult wearable sensors to track athletes during practices and games. Coaches get tons of (often overlapping) metrics each session, so part of my job was trying to understand the relationship between these measurements, specifically IMA band accelerations and decelerations. I did the code in R and worked with data from football and men's and women's lacrosse.

Author: Kate Marine (kate-marine)

Link to video: 


## Overview

**Main questions:**

- Which of the Catapult reporting metrics give coaches the most unique and valuable information? Specifically what is the relationship between IMA acceleration bands and Player Load?
- How well are practices preparing athletes for game-like intensity?

## Approach and Methods

I did this project in RStudeio and used libraries such as `tidyverse`/`dplyr` for data wrangling and `ggplot2` for visualization.
I started by taking the exports for each sport and loaded them into separate data frames (football, mlax, wlax). I also split them into positions (football into bigs, mids, and skills and lacrosse into attackers, midfielders, and defenders). I used Pearson coefficients with pairwise handling to account for missing values. Then I combined all three sports to plot total IMA vs Player Load and recorded the correlation and R² for each sport. I also built correlation matrices for each sport of the individual bands against Player Load, (along with a few other metrics like distance and duration) and visualized them as heatmaps (make_heatmap function). 

For the games vs practices analysis I filtered the datasets by activity_name and then compared games and practices first with mean IMA band counts and then with proportion of each band count (to capture intensity mix).

**Data** I had access to three large excel sheet exports from Catapult with one row per athlete per session. The main columns I was paying attention to were Player Load, total distance, duration, GPS accel/decel efforts, and IMA acceleration/deceleration counts (split into three bands). The datasets were for Dartmouth football, men's lacrosse, and women's lacrosse teams from the 2025–2026 season.


## Findings
- IMA totals and Player Load are related but not completely redundant (IMA explains only around 40%
  of Player Load variance). However Band 1 (low intensity) is more closely related to
  Player Load (suggesting it's mostly re-measuring volume), while Band 3 is more independent of
  it.
- How redundant a band is depends on the athlete's position. Football linemen (Bigs) show pretty much all three bands closely correlated with
  Player Load, however skill positions and all lacrosse positions have their higher intensity bands much more independent of player load. Also the Lacrosse athelets were much more consistent across positions than football.
- Games are mostly higher volume, and not necessarily intensity as I found that the proportion of low/medium/high
  band efforts stays roughly the same from practices to games for all three sports. Suggests coaches are doing a good job of replicating game-level intensity in their training.


## Downloading the data

Unfortunately I'm not allowed to share the actual datasets since Dartmouth can't technically share any private athlete data. However,
to reproduce the analysis you could try recreating a synthetic sample dataset and run catapult_script.R just knowing that the actual numbers won't be the same.

Columns used in the script: `total_player_load`, `total_distance`, `total_duration`,
`player_load_per_minute`, `accel.decel_efforts` (GPS), `total_ima_accel_decel`,
`ima_band{1,2,3}_{accel,decel}_count`, `position_name`, `activity_name`, `period_name`,
`athlete_jersey`, `sport`.

---

# Running the code

I have all the code in a single R script: `catapult_script.R`.


Requirement packages: `tidyverse`, `dplyr`, `reshape2`, `scales`
  ```r
  install.packages(c("tidyverse", "reshape2", "scales"))
  ```

**Note** The script assumes the data frames
`football`, `mlax`, `wlax`, and `all_vx` already exist in R environment so before running
the script load each sport's dataset (generate simulated ones) and bind/clean it into objects with those names. Also make
sure each one has a `sport` column. For the period analysis (not mentioned in video) then have the three `*_byPeriod.csv` files in your working directory.

## Contributing to the code

**Next steps:**
- **Practice clustering:** Currently working on clustering practices into
  light/moderate/high intensity categories (k-means on band counts) so coaches can see if their athletes' effort/exertion is actually matching their plan for a recovery day vs a more intense day, etc. Can then plot the practices over time so see the effects of preseason or the effects of a high intense practice on the upcoming game. 
- **VX data vs Catapult:** Basically Dartmouth only switched to start using Catapult at the beginning of this season and before that they used VX which has a completely different measurement system. So if I want to look at trends over time (especially useful for football preseason which was before Catapult introduced) then I need to look into how to convert the different metrics. Specifically with accelerations and decelerations they have totally different ways of counting (VX much higher) so first steps would be some sort of conversion/normalization that would let coaches track trends across the system switch themselves and not necessarily interpretting the number drops as a reflection of performance.

**Other open questions**
- Why do men's lacrosse practices show more total IMA efforts than football or women's lacrosse?
- Is decel load more associated with injury risk than acceleration load? (Accels exceed
  decels in every band/cluster)
- How should take into account frequently subbed players when analyzing player load in games? (right now I'm just filtering to athletes who are playing in at least every quarter but this is obviously leaving out a lot of athletes) 



# Acknowledgements
 
 Dartmouth Athletics, specfically Sarah Deussing and the football and lacrosse teams for allowing me to work with them and all their data. 
