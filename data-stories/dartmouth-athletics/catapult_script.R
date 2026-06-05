library(dplyr)
library(tidyverse)

# football first since it has most complete GPS data 
football %>%
  select(accel.decel_efforts, 
         ima_band1_accel_count, ima_band1_decel_count,
         ima_band2_accel_count, ima_band2_decel_count,
         ima_band3_accel_count, ima_band3_decel_count,
         total_ima_accel_decel) %>%
  cor(use = "complete.obs") %>%
  round(3)

# scatterplot of GPS accel/decel efforts vs total IMA accel/decel
ggplot(football, aes(x = total_ima_accel_decel, y = accel.decel_efforts)) +
  geom_point(alpha = 0.3) +
  geom_smooth(method = "lm", color = "blue") +
  labs(
    title = "Football: GPS Accel/Decel Efforts vs. Total IMA Accel/Decel",
    x = "Total IMA Accel + Decel (All Bands)",
    y = "GPS Accel/Decel Efforts"
  ) +
  theme_minimal()

# scatterplots by individual bands

# reshape to long format 
football_long <- football %>%
  select(accel.decel_efforts, 
         ima_band1_accel_count, ima_band2_accel_count, ima_band3_accel_count,
         ima_band1_decel_count, ima_band2_decel_count, ima_band3_decel_count) %>%
  pivot_longer(
    cols = -accel.decel_efforts,
    names_to = "ima_band",
    values_to = "count"
  ) %>%
  mutate(
    band = case_when(
      grepl("band1", ima_band) ~ "Band 1 (Low)",
      grepl("band2", ima_band) ~ "Band 2 (Med)",
      grepl("band3", ima_band) ~ "Band 3 (High)"
    ),
    type = ifelse(grepl("accel_count", ima_band), "Accel", "Decel")
  )

ggplot(football_long, aes(x = count, y = accel.decel_efforts)) +
  geom_point(alpha = 0.2) +
  geom_smooth(method = "lm", color = "blue") +
  facet_grid(type ~ band) +
  labs(
    title = "Football: GPS Efforts vs. Each IMA Band",
    x = "IMA Band Count",
    y = "GPS Accel/Decel Efforts"
  ) +
  theme_minimal()


# 
# total IMA accel/deces vs other metrics, player load

# scatterplot of total IMA accel/decel v. player load

# combine for all three sports
all_catapult <- bind_rows(
  football %>% select(total_player_load, total_ima_accel_decel, sport),
  wlax %>% select(total_player_load, total_ima_accel_decel, sport),
  mlax %>% select(total_player_load, total_ima_accel_decel, sport)
)

ggplot(all_catapult, aes(x = total_ima_accel_decel, y = total_player_load, color = sport)) +
  geom_point(alpha = 0.3) +
  geom_smooth(method = "lm", se = FALSE) +
  labs(
    title = "Total IMA Accel/Decel vs. Player Load (All Sports)",
    x = "Total IMA Accel + Decel",
    y = "Total Player Load",
    color = "Sport"
  ) +
  theme_minimal()

# get the r squared vals for each sport
all_catapult %>%
  group_by(sport) %>%
  summarise(
    r = cor(total_ima_accel_decel, total_player_load, use = "complete.obs"),
    r_squared = r^2,
    n = n()
  )

# Correlation matrix of individual IMA bands vs different metrics 
# football
football %>%
  select(total_player_load, total_distance, total_duration, player_load_per_minute,
         ima_band1_accel_count, ima_band2_accel_count, ima_band3_accel_count,
         ima_band1_decel_count, ima_band2_decel_count, ima_band3_decel_count) %>%
  cor(use = "pairwise.complete.obs") %>%
  round(3)

# visualization: correlation heatmap
#install.packages("reshape2")
library(reshape2)

cor_matrix <- football %>%
  select(total_player_load, total_distance, player_load_per_minute,
         ima_band1_accel_count, ima_band2_accel_count, ima_band3_accel_count,
         ima_band1_decel_count, ima_band2_decel_count, ima_band3_decel_count) %>%
  cor(use = "pairwise.complete.obs") %>%
  round(3)

cor_melted <- melt(cor_matrix)

ggplot(cor_melted, aes(x = Var1, y = Var2, fill = value)) +
  geom_tile() +
  geom_text(aes(label = value), size = 2.5) +
  scale_fill_gradient2(low = "blue", mid = "white", high = "red", midpoint = 0) +
  labs(title = "Football: Correlation Heatmap — IMA Bands vs. Key Metrics") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1, size = 7),
        axis.text.y = element_text(size = 7),
        axis.title = element_blank())

# mlax
cor_mlax <- mlax %>%
  select(total_player_load, total_distance, player_load_per_minute,
         ima_band1_accel_count, ima_band2_accel_count, ima_band3_accel_count,
         ima_band1_decel_count, ima_band2_decel_count, ima_band3_decel_count) %>%
  cor(use = "pairwise.complete.obs") %>%
  round(3)

ggplot(melt(cor_mlax), aes(x = Var1, y = Var2, fill = value)) +
  geom_tile() +
  geom_text(aes(label = value), size = 2.5) +
  scale_fill_gradient2(low = "blue", mid = "white", high = "red", midpoint = 0) +
  labs(title = "Men's Lacrosse: Correlation Heatmap — IMA Bands vs. Key Metrics") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1, size = 7),
        axis.text.y = element_text(size = 7),
        axis.title = element_blank())

# wlax
cor_wlax <- wlax %>%
  select(total_player_load, total_distance, player_load_per_minute,
         ima_band1_accel_count, ima_band2_accel_count, ima_band3_accel_count,
         ima_band1_decel_count, ima_band2_decel_count, ima_band3_decel_count) %>%
  cor(use = "pairwise.complete.obs") %>%
  round(3)

ggplot(melt(cor_wlax), aes(x = Var1, y = Var2, fill = value)) +
  geom_tile() +
  geom_text(aes(label = value), size = 2.5) +
  scale_fill_gradient2(low = "blue", mid = "white", high = "red", midpoint = 0) +
  labs(title = "Women's Lacrosse: Correlation Heatmap — IMA Bands vs. Key Metrics") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1, size = 7),
        axis.text.y = element_text(size = 7),
        axis.title = element_blank())

# summary table bands to player load correlations
band_pl_cors <- data.frame(
  band = c("Band 1 Accel", "Band 2 Accel", "Band 3 Accel",
           "Band 1 Decel", "Band 2 Decel", "Band 3 Decel"),
  Football = c(0.679, 0.470, 0.308, 0.458, 0.328, 0.166),
  Mens_Lax = c(0.540, 0.481, 0.395, 0.345, 0.276, 0.052),
  Womens_Lax = c(0.515, 0.379, 0.279, 0.343, 0.310, 0.183)
)

# Reshape for plotting
band_pl_long <- band_pl_cors %>%
  pivot_longer(cols = -band, names_to = "sport", values_to = "correlation") %>%
  mutate(
    sport = recode(sport, "Mens_Lax" = "Men's Lacrosse", "Womens_Lax" = "Women's Lacrosse"),
    band = factor(band, levels = c("Band 1 Accel", "Band 2 Accel", "Band 3 Accel",
                                   "Band 1 Decel", "Band 2 Decel", "Band 3 Decel"))
  )

ggplot(band_pl_long, aes(x = band, y = correlation, fill = sport)) +
  geom_col(position = "dodge") +
  labs(
    title = "Correlation of Each IMA Band with Player Load, by Sport",
    x = "", y = "Correlation with Player Load", fill = "Sport"
  ) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
  geom_hline(yintercept = 0, linetype = "dashed")

#football by position
table(football$position_name)

football <- football %>%
  mutate(pos_group = case_when(
    position_name %in% c("DL", "OL") ~ "Bigs",
    position_name %in% c("LB", "TE") ~ "Mids",
    position_name %in% c("QB", "RB", "SAF", "CB", "WR") ~ "Skills"
  ))

table(football$pos_group)

# make heatmap for position group
make_heatmap <- function(data, title) {
  cor_mat <- data %>%
    select(total_player_load, total_distance, player_load_per_minute,
           ima_band1_accel_count, ima_band2_accel_count, ima_band3_accel_count,
           ima_band1_decel_count, ima_band2_decel_count, ima_band3_decel_count) %>%
    cor(use = "pairwise.complete.obs") %>%
    round(3)
  
  ggplot(melt(cor_mat), aes(x = Var1, y = Var2, fill = value)) +
    geom_tile() +
    geom_text(aes(label = value), size = 2.5) +
    scale_fill_gradient2(low = "blue", mid = "white", high = "red", midpoint = 0) +
    labs(title = title) +
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1, size = 7),
          axis.text.y = element_text(size = 7),
          axis.title = element_blank())
}

make_heatmap(football %>% filter(pos_group == "Bigs"), "Football Bigs (DL/OL)")
make_heatmap(football %>% filter(pos_group == "Mids"), "Football Mids (LB/TE)")
make_heatmap(football %>% filter(pos_group == "Skills"), "Football Skills (QB/RB/WR/CB/SAF)")

pos_cors <- data.frame(
  band = c("Band 1 Accel", "Band 2 Accel", "Band 3 Accel",
           "Band 1 Decel", "Band 2 Decel", "Band 3 Decel"),
  Bigs = c(0.754, 0.705, 0.643, 0.609, 0.618, 0.549),
  Mids = c(0.756, 0.609, 0.443, 0.615, 0.495, 0.362),
  Skills = c(0.660, 0.421, 0.270, 0.399, 0.252, 0.103)
)

pos_cors_long <- pos_cors %>%
  pivot_longer(cols = -band, names_to = "pos_group", values_to = "correlation") %>%
  mutate(
    band = factor(band, levels = c("Band 1 Accel", "Band 2 Accel", "Band 3 Accel",
                                   "Band 1 Decel", "Band 2 Decel", "Band 3 Decel")),
    pos_group = factor(pos_group, levels = c("Bigs", "Mids", "Skills"))
  )

ggplot(pos_cors_long, aes(x = band, y = correlation, fill = pos_group)) +
  geom_col(position = "dodge") +
  labs(
    title = "Correlation of IMA Bands with Player Load by Position Group",
    x = "", y = "Correlation with Player Load", fill = "Position Group"
  ) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
  geom_hline(yintercept = 0, linetype = "dashed")


# lax position groups and make heat maps
cat("Men's Lacrosse positions:\n")
table(mlax$position_name)

cat("\nWomen's Lacrosse positions:\n")
table(wlax$position_name)

# mlax position groups
mlax <- mlax %>%
  mutate(pos_group = case_when(
    position_name %in% c("Offensive Midfielder", "Defensive Midfielder", "Face Off") ~ "Midfielders",
    position_name %in% c("Attacker") ~ "Attackers",
    position_name %in% c("Defender", "Long Stick Midfielder", "Goalie") ~ "Defenders"
  ))

table(mlax$pos_group)

# wlax
wlax <- wlax %>%
  mutate(pos_group = case_when(
    position_name == "Midfielder" ~ "Midfielders",
    position_name == "Attacker" ~ "Attackers",
    position_name == "Defender" ~ "Defenders"
  ))

table(wlax$pos_group)


make_heatmap(mlax %>% filter(pos_group == "Attackers"), "Men's Lax Attackers")
make_heatmap(mlax %>% filter(pos_group == "Midfielders"), "Men's Lax Midfielders")
make_heatmap(mlax %>% filter(pos_group == "Defenders"), "Men's Lax Defenders")
make_heatmap(wlax %>% filter(pos_group == "Attackers"), "Women's Lax Attackers")
make_heatmap(wlax %>% filter(pos_group == "Midfielders"), "Women's Lax Midfielders")
make_heatmap(wlax %>% filter(pos_group == "Defenders"), "Women's Lax Defenders")




# Differences in VX vs Catapult units 

# prep Catapult totals in comparable format
catapult_compare <- all_catapult %>%
  select(total_accel_decel = total_ima_accel_decel, sport) %>%
  mutate(system = "Catapult")

vx_compare <- all_vx %>%
  select(total_accel_decel = vx_total_accel_decel, sport) %>%
  mutate(system = "VX")
compare_df <- bind_rows(catapult_compare, vx_compare)

# Side by side boxplots
ggplot(compare_df, aes(x = system, y = total_accel_decel, fill = system)) +
  geom_boxplot(outlier.alpha = 0.2) +
  facet_wrap(~ sport, scales = "free_y") +
  labs(
    title = "Total Accel/Decel: VX vs. Catapult by Sport",
    x = "",
    y = "Total Accel + Decel Count"
  ) +
  theme_minimal() +
  theme(legend.position = "none")

compare_df %>%
  group_by(sport, system) %>%
  summarise(
    mean = round(mean(total_accel_decel, na.rm = TRUE), 1),
    median = round(median(total_accel_decel, na.rm = TRUE), 1),
    sd = round(sd(total_accel_decel, na.rm = TRUE), 1),
    n = n(),
    .groups = "drop"
  ) %>%
  arrange(sport, system)



# Practices vs games intensity


# Check activity types
cat("Football activities:\n")
sort(unique(football$activity_name))

cat("\nMen's Lax activities:\n")
sort(unique(mlax$activity_name))

cat("\nWomen's Lax activities:\n")
sort(unique(wlax$activity_name))

#  game vs practice label
football <- football %>%
  mutate(session_type = case_when(
    grepl("Game", activity_name) ~ "Game",
    grepl("Walk_Thru", activity_name) ~ "Walk Thru",
    TRUE ~ "Practice/Training"
  ))

table(football$session_type)

# MLax
mlax <- mlax %>%
  mutate(session_type = case_when(
    grepl("vs|at[A-Z]", activity_name, ignore.case = FALSE) ~ "Game",
    grepl("Indi|indi", activity_name) ~ "Individual",
    TRUE ~ "Practice/Training"
  ))

table(mlax$session_type)

# WLax
wlax <- wlax %>%
  mutate(session_type = case_when(
    grepl("vs|at[A-Z]|exhibition", activity_name, ignore.case = FALSE) ~ "Game",
    grepl("SAQ|saq|captains|Captains|conditioning|optional|Puccio|rtp|RTP", activity_name) ~ "Other",
    TRUE ~ "Practice/Training"
  ))

table(wlax$session_type)

# Game vs practice comparison w IMA bands

# combine all sports keep only games and practice/training
all_game_practice <- bind_rows(
  football %>% filter(session_type %in% c("Game", "Practice/Training")) %>%
    select(sport, session_type, pos_group,
           ima_band1_accel_count, ima_band2_accel_count, ima_band3_accel_count,
           ima_band1_decel_count, ima_band2_decel_count, ima_band3_decel_count,
           total_ima_accel_decel, total_player_load),
  mlax %>% filter(session_type %in% c("Game", "Practice/Training")) %>%
    select(sport, session_type, pos_group,
           ima_band1_accel_count, ima_band2_accel_count, ima_band3_accel_count,
           ima_band1_decel_count, ima_band2_decel_count, ima_band3_decel_count,
           total_ima_accel_decel, total_player_load),
  wlax %>% filter(session_type %in% c("Game", "Practice/Training")) %>%
    select(sport, session_type, pos_group,
           ima_band1_accel_count, ima_band2_accel_count, ima_band3_accel_count,
           ima_band1_decel_count, ima_band2_decel_count, ima_band3_decel_count,
           total_ima_accel_decel, total_player_load)
)

# summary stats sport and session type
all_game_practice %>%
  group_by(sport, session_type) %>%
  summarise(
    mean_player_load = round(mean(total_player_load, na.rm = TRUE), 1),
    mean_total_ima = round(mean(total_ima_accel_decel, na.rm = TRUE), 1),
    mean_band3_accel = round(mean(ima_band3_accel_count, na.rm = TRUE), 1),
    mean_band3_decel = round(mean(ima_band3_decel_count, na.rm = TRUE), 1),
    n = n(),
    .groups = "drop"
  ) %>%
  arrange(sport, session_type)


# Compare IMA band distribution games vs practices

# Reshape to long format 
game_practice_long <- all_game_practice %>%
  select(sport, session_type,
         ima_band1_accel_count, ima_band2_accel_count, ima_band3_accel_count,
         ima_band1_decel_count, ima_band2_decel_count, ima_band3_decel_count) %>%
  pivot_longer(
    cols = starts_with("ima"),
    names_to = "band",
    values_to = "count"
  ) %>%
  mutate(
    intensity = case_when(
      grepl("band1", band) ~ "Band 1 (Low)",
      grepl("band2", band) ~ "Band 2 (Med)",
      grepl("band3", band) ~ "Band 3 (High)"
    ),
    type = ifelse(grepl("accel", band), "Accel", "Decel"),
    intensity = factor(intensity, levels = c("Band 1 (Low)", "Band 2 (Med)", "Band 3 (High)"))
  )

# Mean counts
game_practice_summary <- game_practice_long %>%
  group_by(sport, session_type, intensity, type) %>%
  summarise(mean_count = mean(count, na.rm = TRUE), .groups = "drop")

ggplot(game_practice_summary, aes(x = intensity, y = mean_count, fill = session_type)) +
  geom_col(position = "dodge") +
  facet_grid(type ~ sport) +
  labs(
    title = "Mean IMA Band Counts: Game vs. Practice by Sport",
    x = "", y = "Mean Count", fill = "Session Type"
  ) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))


#Compare proportion of each band 
game_practice_props <- game_practice_summary %>%
  group_by(sport, session_type, type) %>%
  mutate(proportion = mean_count / sum(mean_count)) %>%
  ungroup()

ggplot(game_practice_props, aes(x = session_type, y = proportion, fill = intensity)) +
  geom_col(position = "stack") +
  facet_grid(type ~ sport) +
  scale_fill_manual(values = c("Band 1 (Low)" = "#4DAF4A", 
                               "Band 2 (Med)" = "#FF7F00", 
                               "Band 3 (High)" = "#E41A1C")) +
  scale_y_continuous(labels = scales::percent) +
  labs(
    title = "IMA Band Proportions: Game vs. Practice by Sport",
    x = "", y = "Proportion of Total IMA Efforts", fill = "Intensity"
  ) +
  theme_minimal()




# Load new period data csvs
fb_period <- read.csv("fb_2025_2026_byPeriod.csv")
mlax_period <- read.csv("mlax_2025_2026_byPeriod.csv")
wlax_period <- read.csv("wlax_2025_2026_byPeriod.csv")

cat("Football periods:", nrow(fb_period), "rows,", ncol(fb_period), "columns\n")
cat("Men's Lax periods:", nrow(mlax_period), "rows,", ncol(mlax_period), "columns\n")
cat("Women's Lax periods:", nrow(wlax_period), "rows,", ncol(wlax_period), "columns\n")

#cat("\nFootball period names:\n")
#table(fb_period$period_name)

# check lax period and column names
#cat("Men's Lax period names:\n")
#table(mlax_period$period_name)

#cat("\nWomen's Lax period names:\n")
#table(wlax_period$period_name)

#cat("\nFootball period columns:\n")
#names(fb_period)




#  filter to game quarters
fb_game_quarters <- fb_period %>%
  filter(grepl("^Quarter [0-9]|^1st Half|^2nd Half", period_name)) %>%
  mutate(
    period_order = case_when(
      period_name == "1st Half" ~ 1,
      period_name == "2nd Half" ~ 2,
      period_name == "Quarter 1" ~ 1,
      period_name == "Quarter 2" ~ 2,
      period_name == "Quarter 5" ~ 3,
      period_name == "Quarter 9" ~ 4,
      period_name == "Quarter 10" ~ 5,
      period_name == "Quarter 14" ~ 6,
      TRUE ~ NA_real_
    )
  )

#cat("game quarter rows:", nrow(fb_game_quarters), "\n")
#table(fb_game_quarters$period_name)

# mlax
mlax_game_quarters <- mlax_period %>%
  filter(grepl("Quarter|1st Half|2nd Half", period_name)) %>%
  mutate(
    period_order = case_when(
      period_name %in% c("1st Half") ~ 1,
      period_name %in% c("2nd Half") ~ 2,
      period_name %in% c("1st quarter", "1st Quarter") ~ 1,
      period_name %in% c("2nd quarter", "2nd Quarter") ~ 2,
      period_name %in% c("3rd quarter", "3rd Quarter") ~ 3,
      period_name %in% c("4th quarter", "4th Quarter") ~ 4
    )
  )

cat("\nmensgame quarter rows:", nrow(mlax_game_quarters), "\n")
table(mlax_game_quarters$period_name)

# wlax
wlax_game_quarters <- wlax_period %>%
  filter(grepl("Quarter", period_name)) %>%
  mutate(
    period_order = case_when(
      period_name == "1st Quarter" ~ 1,
      period_name == "2nd Quarter" ~ 2,
      period_name == "3rd Quarter" ~ 3,
      period_name == "4th Quarter" ~ 4
    )
  )

#cat("\nwomens lax game quarter rows:", nrow(wlax_game_quarters), "\n")
#table(wlax_game_quarters$period_name)

# plot band 3 efforts across game periods
fb_fatigue <- fb_game_quarters %>%
  filter(period_name %in% c("1st Half", "2nd Half")) %>%
  mutate(period_label = factor(period_name, levels = c("1st Half", "2nd Half")))

# lax use 4 quarters only
mlax_fatigue <- mlax_game_quarters %>%
  filter(period_name %in% c("1st Quarter", "2nd Quarter", "3rd Quarter", "4th Quarter")) %>%
  mutate(period_label = factor(period_name, levels = c("1st Quarter", "2nd Quarter", "3rd Quarter", "4th Quarter")))

wlax_fatigue <- wlax_game_quarters %>%
  filter(period_name %in% c("1st Quarter", "2nd Quarter", "3rd Quarter", "4th Quarter")) %>%
  mutate(period_label = factor(period_name, levels = c("1st Quarter", "2nd Quarter", "3rd Quarter", "4th Quarter")))

# Combine with sport labels
all_fatigue <- bind_rows(
  fb_fatigue %>% mutate(sport = "Football") %>%
    select(sport, period_label, ima_band1_accel_count, ima_band2_accel_count, ima_band3_accel_count,
           ima_band1_decel_count, ima_band2_decel_count, ima_band3_decel_count, total_player_load),
  mlax_fatigue %>% mutate(sport = "Men's Lacrosse") %>%
    select(sport, period_label, ima_band1_accel_count, ima_band2_accel_count, ima_band3_accel_count,
           ima_band1_decel_count, ima_band2_decel_count, ima_band3_decel_count, total_player_load),
  wlax_fatigue %>% mutate(sport = "Women's Lacrosse") %>%
    select(sport, period_label, ima_band1_accel_count, ima_band2_accel_count, ima_band3_accel_count,
           ima_band1_decel_count, ima_band2_decel_count, ima_band3_decel_count, total_player_load)
)

# Summarize mean Band 3 accel/decel
fatigue_summary <- all_fatigue %>%
  mutate(band3_total = ima_band3_accel_count + ima_band3_decel_count,
         band1_total = ima_band1_accel_count + ima_band1_decel_count) %>%
  group_by(sport, period_label) %>%
  summarise(
    mean_band3 = mean(band3_total, na.rm = TRUE),
    mean_band1 = mean(band1_total, na.rm = TRUE),
    mean_player_load = mean(total_player_load, na.rm = TRUE),
    .groups = "drop"
  )

#Band 3 vs Band 1
fatigue_long <- fatigue_summary %>%
  pivot_longer(cols = c(mean_band3, mean_band1), names_to = "metric", values_to = "value") %>%
  mutate(metric = recode(metric, "mean_band3" = "Band 3 (High Intensity)", "mean_band1" = "Band 1 (Low Intensity)"))

ggplot(fatigue_long, aes(x = period_label, y = value, color = metric, group = metric)) +
  geom_line(linewidth = 1.2) +
  geom_point(size = 3) +
  facet_wrap(~ sport, scales = "free_x") +
  labs(
    title = "IMA Efforts Across Game Periods: Band 1 vs. Band 3",
    x = "", y = "Mean Count per Athlete", color = ""
  ) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))


head(wlax_fatigue$date)
names(wlax_fatigue)

# Normalize by playing time and filter to athletes who played all periods
wlax_fatigue <- wlax_fatigue %>%
  mutate(game_date = as.Date(date, format = "%m/%d/%Y"))

# find athletes who played all 4 quarters per game
wlax_quarters_played <- wlax_fatigue %>%
  group_by(athlete_jersey, activity_name) %>%
  summarise(n_quarters = n_distinct(period_label), .groups = "drop") %>%
  filter(n_quarters == 4)


cat("Athletes x Games with all 4 quarters:", nrow(wlax_quarters_played), "\n")

# Filter to full game athletes and normalize
wlax_full_game <- wlax_fatigue %>%
  semi_join(wlax_quarters_played, by = c("athlete_jersey", "activity_name")) %>%
  mutate(
    band3_total = ima_band3_accel_count + ima_band3_decel_count,
    band1_total = ima_band1_accel_count + ima_band1_decel_count,
    duration_min = total_duration / 60,
    band3_per_min = band3_total / duration_min,
    band1_per_min = band1_total / duration_min
  )
# Summarize by quarter
wlax_full_game %>%
  group_by(period_label) %>%
  summarise(
    mean_band3_per_min = round(mean(band3_per_min, na.rm = TRUE), 3),
    mean_band1_per_min = round(mean(band1_per_min, na.rm = TRUE), 3),
    n = n(),
    .groups = "drop"
  )


# Plot per-minute rates a

# wlax
wlax_fatigue_summary <- wlax_full_game %>%
  group_by(period_label) %>%
  summarise(
    mean_band3_per_min = mean(band3_per_min, na.rm = TRUE),
    mean_band1_per_min = mean(band1_per_min, na.rm = TRUE),
    .groups = "drop"
  ) %>%
  pivot_longer(cols = starts_with("mean"), names_to = "metric", values_to = "value") %>%
  mutate(metric = recode(metric, 
                         "mean_band3_per_min" = "Band 3 (High)", 
                         "mean_band1_per_min" = "Band 1 (Low)"))

ggplot(wlax_fatigue_summary, aes(x = period_label, y = value, color = metric, group = metric)) +
  geom_line(linewidth = 1.2) +
  geom_point(size = 3) +
  labs(
    title = "Women's Lax: IMA Efforts Per Minute Across Quarters (Full-Game Athletes)",
    x = "", y = "Mean Efforts per Minute", color = ""
  ) +
  theme_minimal()

head(mlax_fatigue$date)

mlax_fatigue <- mlax_fatigue %>%
  mutate(game_date = as.Date(date, format = "%m/%d/%Y"))


names(mlax_fatigue)[grep("name|jersey|athlete", names(mlax_fatigue), ignore.case = TRUE)]

# do same for mens lax
mlax_quarters_played <- mlax_fatigue %>%
  group_by(athlete_jersey, activity_name) %>%
  summarise(n_quarters = n_distinct(period_label), .groups = "drop") %>%
  filter(n_quarters == 4)

cat("Athletes x Games with all 4 quarters:", nrow(mlax_quarters_played), "\n")

mlax_full_game <- mlax_fatigue %>%
  semi_join(mlax_quarters_played, by = c("athlete_jersey", "activity_name")) %>%
  mutate(
    band3_total = ima_band3_accel_count + ima_band3_decel_count,
    band1_total = ima_band1_accel_count + ima_band1_decel_count,
    duration_min = total_duration / 60,
    band3_per_min = band3_total / duration_min,
    band1_per_min = band1_total / duration_min
  )


mlax_full_game %>%
  group_by(period_label) %>%
  summarise(
    mean_band3_per_min = round(mean(band3_per_min, na.rm = TRUE), 3),
    mean_band1_per_min = round(mean(band1_per_min, na.rm = TRUE), 3),
    n = n(),
    .groups = "drop"
  )

# Combined plot for both lax sports
mlax_fatigue_summary <- mlax_full_game %>%
  group_by(period_label) %>%
  summarise(
    mean_band3_per_min = mean(band3_per_min, na.rm = TRUE),
    mean_band1_per_min = mean(band1_per_min, na.rm = TRUE),
    .groups = "drop"
  ) %>%
  pivot_longer(cols = starts_with("mean"), names_to = "metric", values_to = "value") %>%
  mutate(metric = recode(metric, "mean_band3_per_min" = "Band 3 (High)", "mean_band1_per_min" = "Band 1 (Low)"),
         sport = "Men's Lacrosse")

wlax_fatigue_summary <- wlax_fatigue_summary %>%
  mutate(sport = "Women's Lacrosse")

both_lax_fatigue <- bind_rows(mlax_fatigue_summary, wlax_fatigue_summary)

ggplot(both_lax_fatigue, aes(x = period_label, y = value, color = metric, group = metric)) +
  geom_line(linewidth = 1.2) +
  geom_point(size = 3) +
  facet_wrap(~ sport) +
  labs(
    title = "IMA Efforts Per Minute Across Quarters (Full-Game Athletes Only)",
    x = "", y = "Mean Efforts per Minute", color = ""
  ) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))


# Wlax fatigue by position
wlax_full_game %>%
  group_by(position_name, period_label) %>%
  summarise(
    mean_band1_per_min = round(mean(band1_per_min, na.rm = TRUE), 3),
    mean_band3_per_min = round(mean(band3_per_min, na.rm = TRUE), 3),
    n = n(),
    .groups = "drop"
  ) %>%
  arrange(position_name, period_label)
#fatigue by position for women lax
wlax_pos_fatigue <- wlax_full_game %>%
  group_by(position_name, period_label) %>%
  summarise(
    mean_band3_per_min = mean(band3_per_min, na.rm = TRUE),
    mean_band1_per_min = mean(band1_per_min, na.rm = TRUE),
    .groups = "drop"
  ) %>%
  pivot_longer(cols = starts_with("mean"), names_to = "metric", values_to = "value") %>%
  mutate(metric = recode(metric, 
                         "mean_band3_per_min" = "Band 3 (High)", 
                         "mean_band1_per_min" = "Band 1 (Low)"))

ggplot(wlax_pos_fatigue, aes(x = period_label, y = value, color = metric, group = metric)) +
  geom_line(linewidth = 1.2) +
  geom_point(size = 3) +
  facet_wrap(~ position_name) +
  labs(
    title = "Women's Lax: Fatigue by Position (Full-Game Athletes, Per Minute)",
    x = "", y = "Mean Efforts per Minute", color = ""
  ) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))


# football fatigue by position group 
#  fb_game_quarters
names(fb_game_quarters)[grep("name|jersey|position", names(fb_game_quarters), ignore.case = TRUE)]

#position groups
fb_game_quarters <- fb_game_quarters %>%
  mutate(pos_group = case_when(
    position_name %in% c("DL", "OL") ~ "Bigs",
    position_name %in% c("LB", "TE") ~ "Mids",
    position_name %in% c("QB", "RB", "SAF", "CB", "WR") ~ "Skills"
  ))
