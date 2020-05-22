# Language Shift

### GitHub usernames:
- Jae Hong (jaeshong)
- Maddy Lee (maddyrlee)
- Mira Ram (miramints)
- Bill Tang (giga-bit)

### Contributions:
- Jae Hong - Assisted data collection, imported datasets, created a graph, and helped find trends in the data.
- Maddy Lee - Assisted data collection, created a graph, helped find trends, and completed documentation.
- Mira Ram - Assisted data collection, helped find trends in the data, and created the youtube video.
- Bill Tang - Created multiple graphs. Helped find trends.

# Overview

Linguists have noticed a strange phenomenon dubbed third generation shift. Most immigrant groups switch to using English as their primary language by the 3rd generation. We found an interesting dataset that covers three generations of multiple Asian and Hispanic ethnicities and their language proficiency in various U.S. cities. We explored this dataset in order to compare and contrast language shift in Asian and Hispanic populations.

Although Asian immigrants had higher English Only scores than Hispanic immigrants in every generation, if one investigates how all the ethnicities within these broad categories, they will find that the trends within the groups vary greatly.

In conclusion, Asian and Hispanic are broad categories that fit very different and diverse cultures within them. To understand the third generation shift, one must look at individual ethnicities rather than these broad labels.

Link to youtube video is in [language_shift.ipynb]() file.

# Downloading the data

We created multiple datasets. The information includes data from multiple Asian and Hispanic ethnicities recorded in multiple cities across the U.S. English proficiency across generations is recorded as well as the population of that ethnicity in each city. 
Data source: https://ccis.ucsd.edu/_files/wp111.pdf

## Overall language
English proficiency across three generations of multiple Asian and Hispanic ethnicities. https://raw.githubusercontent.com/jaeshong/bob-the-weasel/master/out%201.csv

## Asian population
Asian population in tested cities in 2004. [area_vs_asian_population.csv](https://raw.githubusercontent.com/jaeshong/bob-the-weasel/master/area_vs_asian_population.csv)

## Hispanic population
Hispanic population in tested cities in 2004. [area_vs_hispanic_population.csv](https://raw.githubusercontent.com/jaeshong/bob-the-weasel/master/area_vs_hispanic_population.csv)

## Asian language speakers
English proficiency across three generations of Asians. [asian_generational_language_statistics.csv](https://raw.githubusercontent.com/jaeshong/bob-the-weasel/master/asian_generational_language_statistics.csv)

## Hispanic language speakers
English proficiency across three generations of Hispanics. [hispanic_generational_language_statistics.csv]( https://raw.githubusercontent.com/jaeshong/bob-the-weasel/master/hispanic_generational_language_statistics.csv)

## County FIPS
County FIPS. [ZIP-COUNTY-FIPS_2012-06.csv](https://raw.githubusercontent.com/jaeshong/bob-the-weasel/master/ZIP-COUNTY-FIPS_2012-06.csv)

# Running the code

Open the [language_shift.ipynb]() file. Then run each line of code. 

# Contributing to the code
We found many interesting trends within individual ethnicities in terms of where there are spikes or a lack of spikes in each group. Some paths to explore could include:
- Does foreign conflict affect immigrant groups shift toward English exclusive language? 
  - The spike in English proficiency occurs in second generation Japanese immigrants which correlates with World War Two. 
  - The spike in English proficiency occurs in third generation Vietnamese immigrants which correlates with the Vietnam War.
- Why Domincan immigrant groups do not have as strong of a third generation shift compared to other immigrant groups?
- Does population density of individual ethnic groups affect mother tongue language retention?
