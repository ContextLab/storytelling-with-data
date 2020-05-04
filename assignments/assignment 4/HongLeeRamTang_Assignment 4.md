# Project Name: HongLeeRamTang_Assignment 4

### GitHub usernames:
- Jae Hong (jaeshong)
- Maddy Lee (maddyrlee)
- Mira Ram (miramints)
- Bill Tang (giga-bit)

### Contributions:
- Jae Hong - Created the youtube video and helped find trends in the data.
- Maddy Lee - Assisted data collection, finding trends, and completed documentation.
- Mira Ram - Created cumulative csv including data from governor party and state opening dates. Found links to various datasets.
- Bill Tang - Imported datasets and created graphs for state opening, governor party, and age distributions. Helped find trends.

# Overview

During the current COVID-19 crisis, some states have been hit harder economically than others. Our goal is to investigate what possible reasons could cause some states to suffer more economic downturn than others. We noticed that a couple states in particular, most notably New York, Vermont, Hawaii, Nevada, Michigan, and West Virginia. Vermont and Hawaii were incredibly hard hit with some data points showing a decrease in economic activity as big as 90%. Since Dartmouth is so closely tied to Vermont and with some of our group members even having held jobs there, we wanted to explore what made Vermont so different. 

We looked at data including COVID-19 cases, political party of the current governor, date of state reopening to potentially explain why some states had a larger decrease in closed local businesses than others. We used plotly and Google Colab to analyze the data and create graphs.

We found New York and Michigan were most likely impacted by the large number of COVID-19 cases, while Hawaii and Nevada were impacted by decreased tourism. Our analyses, however, were not able to figure out potential reasons why Vermont suffered so much more than the other 5 New England states.

Here is our youtube link: https://www.youtube.com/watch?v=QiQ2_Es3g3A&feature=youtu.be

# Downloading the data

## Party of Governor
Party of the Governor per state as of 2020. 'R' indicates Republican and 'D' indicates Democrate. Located in the [gov_v_state.csv](https://github.com/maddyrlee/storytelling-with-data/blob/master/assignments/assignment%204/csvs/gov_v_state.csv) file. Source: https://en.wikipedia.org/wiki/List_of_United_States_governors

## Date of State Reopening
Reported date of each state reopening located in the [states-reopening.csv](https://github.com/maddyrlee/storytelling-with-data/blob/master/assignments/assignment%204/csvs/state-reopenings.csv) file. Source: https://www.cnn.com/interactive/2020/us/states-reopen-coronavirus-trnd/

## Local Businesses Closed
COVID-19 impact on percent local businesses open per state located in the [businessdata.csv](https://github.com/maddyrlee/storytelling-with-data/blob/master/assignments/assignment%204/csvs/businessdata.csv) file. Sources: https://joinhomebase.com/data/covid-19/ 

## COVID-19 Cases
COVID-19 cases and deaths in each state from 1/21/2020 to present. Source: https://github.com/nytimes/covid-19-data/raw/master/us-states.csv

## Age Distribution of COVID-19 Cases
Age distribution of COVID-19 cases per state and total population per state. Source: https://raw.githubusercontent.com/veltman/state-population-by-age/master/2010.csv

# Running the code

Open the [HongLeeRamTang_Assignment 4.ipynb]() file. Then run each line of code. 

# Contributing to the code
You can contribute too!

### We couldn't investigate every factor that could explain why certain states were impacted more financially than others.
- Find more datasets of possible factors to potentially explain why some states were impacted more.
- Examine the differences in how small vs. large businesses were affected.
- What type of businesses were impacted more than others?
- What are more factors that could affect Vermont that we did not consider?
