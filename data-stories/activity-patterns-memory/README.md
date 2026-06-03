# Overview
Author: Kate Marine kate-marine

**Main question:** Can the temporal patterns in fitbit activity data predict memory-task performance beyond what is already captured by a participant's average activity level? 

# Approach

I tested built two models, one as a baseline using only mean activity, and another with added temporal/dynamic features. I then tried to see whether the second model predicted memory performance better than the baseline and which dynamic features drive any improvement for which memory tasks (using interprettable methods). 


# Data

I used 113 participants' Fitbit data along with memory-task outcomes from the study _Manning, J. R., Notaro, G. M., Chen, E., & Fitzpatrick, P. C. (2022)_. Fitness tracking reveals task-specific associations between memory, mental health, and physical activity. *Scientific Reports*, 12, 13822. https://doi.org/10.1038/s41598-022-17781-0

I reshaped the raw Fitbit CSVs into a participant-by-date panel for the temporal modelinge. 
