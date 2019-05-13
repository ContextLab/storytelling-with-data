# Hackathon 1

## Overview

I have worn a fitbit device nearly every day for the past four years, collecting detailed data on my sleep and daily physical activity. The fitbit app has built-in visualizations that show some longitudinal data trends but I was interested in looking at other metrics and seeing how multiple variables are related in my life. 

The fitbit website allows downloading up to 31 days of either sleep or activity data at a time, so I downloaded data for the past few months as well as September, October, and November 2018. I was interested in looking at trends for this fall as it was a particularly difficult term for me and I kept a detailed calendar of my classes, assignments, interviews, and extracurriculars. I expected to find a decrease in my sleep quantity and quality as big assignments and interviews came up as well as decreases in physical activity as the term went on. Moreover, since the term ended in mid-November, I expected to see a sharp change in my activity and sleep since I went straight from finals to break.

Because my data comes in 31-day chunks, I had to combine datasets from each month to create a master dataset. From there, I plotted variables such as amount of sleep over time, steps over time, steps versus calories burned, and time im bed versus minutes asleep. I also added columns on each dataset (sleep and activity data) tracking the day of the week to see trends for weekdays versus weekends. 

## Downloading the dataset

Fitbit users can download their own raw fitbit data by logging in to https://www.fitbit.com/, navigating to settings, and selecting the "data export tab." As previously mentioned, only 31 days can be downloaded at a time (in a friendly format, at least), so any more data will need to be downloaded in chunks. 

## Running the code

This code can be run with any other fitbit dataset by changing the import statements and perhaps changing dataframe names to make more sense to their content. The dataset(s) must be in the same folder as the notebook.

## Contributing to the code

Others can contribute to this project by creating more plots along other dimensions, potentially realizing new trends. 

