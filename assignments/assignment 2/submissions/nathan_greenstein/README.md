# Bikeshare Data Wrangling

## Overview

This assignment loads data from the Citibike Bikeshare, cleans it up, and carries out several basic visualization / analysis operations. The analyses are designed to provide a very broad sense of what the data look like and identify any obvious relationships (or lacks thereof) in the data. With these analyses, I aim to familiarize myself with this dataset and get a clearer picture of further analyses that might yield interesting results.

## Dataset

This assignment uses data from New York City's Citibike Bikeshare. More information can be found [on their website](https://www.citibikenyc.com/system-data), and the CSV file used in this assignment can be downloaded from [https://s3.amazonaws.com/tripdata/JC-201902-citibike-tripdata.csv.zip](https://s3.amazonaws.com/tripdata/JC-201902-citibike-tripdata.csv.zip).

## Running the Code

Simply navigate to the `Cell` menu and select `Run All`. No preparation / setup is necessary; the data file is downloaded directly from the server, and no third-party packages are required except for those already installed in the Psych 81.09 kernel.

## Contributing

This assignment takes a very general look at the bikeshare trips data, but it considers the data as a whole rather than breaking them down into any kind of subgroup (aside from color-coding gender in the final scatter plot). Further analysis could yield interesting results by comparing trip information with demographic data (gender and age).

The portion of this assignment that computes the distance between to lat/long points comes from [user Michael0x2a on StackOverflow](https://stackoverflow.com/a/19412565).