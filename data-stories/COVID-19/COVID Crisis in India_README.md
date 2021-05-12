# Project information
### Group members
Isha Liu (ishaliu), Laya Indukuri, Keara Dennehy (kearadennehy)
### Contributions
Isha and Keara found the data for the project and loaded it into the Google Colab notebook. Isha wrangled the data, created scatterplots, worked on the video script and slideshow, and created the screenrecorded video. Keara edited the scatterplots, loaded in GeoJSONs and made maps, created the video script and slideshow, and wrote the read me file. Laya participated in meetings and found the media headlines for our slideshow.

# Overview
### Main question
Our main question was about where India's current COVID-19 crisis is hitting the hardest and how COVID cases and vaccinations might be related to income.
### Approach
We used state-level data to observe correlations between per capita income and COVID cases and vaccinations. This was the most granular data we were able to find for the whole country. We mainly used Pandas to work with the data, and we made our plots using ggplot and plotly express.
### Findings
Our main findings were a correlation between COVID cases and per capita income at the state level (and district level in Madhya Pradesh) and between vaccinations and per capita income at the state level (and district level in Madhya Pradesh). We were surprised by the correlation between COVID cases and income but hypothesize that there is a confounding variable or more complex set of variables going on with urbanity. We then looked at correlations with population density for Madhya Pradesh, which exhibited positive relationships between density and COVID cases and vaccinations.
### Video link
https://youtu.be/b-yGWfT569k

# Downloading the data

## Income
https://docs.google.com/spreadsheets/d/1dsSgGNYBqy7PpAb_MTmCLrydM-K0PEpG3hkkMsO8_Sw/edit?usp=sharing
### Original source
https://www.statista.com/statistics/1027998/india-per-capita-income-by-state/
### Description
This data shows per capita income by state in India.

## Vaccine
https://docs.google.com/spreadsheets/d/1mF0T0tDfMNCMuzU_K9YgwJGAO_RadyZRoN20oWyJ-cI/edit?usp=sharing
### Original source
https://geographicinsights.iq.harvard.edu/IndiaVaccine
### Description
This data shows vaccination rates by state in India.

## Testing
https://docs.google.com/spreadsheets/d/1mx0dWnPBzgVI2BBYHIwHsfEUqDtsHo4t_tpaZ3Ci2xY/edit?usp=sharing
### Original source
https://www.grainmart.in/news/covid-19-coronavirus-india-state-and-district-wise-tally/
### Description
This data shows testing and COVID case numbers by state in India.

## State level GeoJSON
https://drive.google.com/file/d/1hhkiIKG5DJbjnJ-iSZaB9gcdIX90czPN/view?usp=sharing
### Original source
https://un-mapped.carto.com/tables/states_india/public
### Description
This is a GeoJSON of the state boundaries of India. I simplified the original file to load faster and have slightly less detailed boundaries.

## Kerala
https://docs.google.com/spreadsheets/d/1zWdEE6i3ea4x_ENk-4dwtMNNrGzkV-InstJNQCe6-Ts/edit?usp=sharing
### Original sources
https://en.wikipedia.org/wiki/List_of_districts_and_cities_in_Kerala_by_GDP_per_capita
https://github.com/covid19india/api
### Description
This data includes COVID case numbers and per capita income by district in Kerala.

## Kerala vaccines
https://docs.google.com/spreadsheets/d/1QILG0ncZmdMFy97bckdsSxHJlkMH1eRl3DAT8RY--lg/edit?usp=sharing
### Original source
https://api.covid19india.org/
### Description
This data includes vaccination rates by district in Kerala.

## Kerala GeoJSON
https://drive.google.com/file/d/1eY_IRueR9-a0PWUh8RFIQ0sbwJL9dSj-/view?usp=sharing
### Original source
https://github.com/geohacker/kerala/blob/master/geojsons/district.geojson
### Description
This is a GeoJSON of the district boundaries of Kerala, India.

## Madhya Pradesh
https://docs.google.com/spreadsheets/d/12n7IFMMn_wUPFiOHVLtKAw9nCPbeqcv8JaZRxCNOpyo/edit?usp=sharing
### Original sources
https://data.gov.in/resources/district-wise-capita-income-current-prices-2004-2005-2012-2013
https://api.covid19india.org/
https://github.com/covid19india/api
### Description
This data includes COVID numbers, vaccination rates, population density, and per capita income by district in Madhya Pradesh.

We loaded all the data into Google spreadsheets because some of it came from tables (rather than file downloads) on Indian government websites or data companies.

# Running the code
### Notebook
https://colab.research.google.com/drive/1gAe45NZZe8dU1ujVvh2GC6N7pCDDgYpW#scrollTo=Yapd6a_7owPF
### Description
At the start of our code, we install and smuggle all the libraries we wanted for this project. Then, we load in the data from Google spreadsheets using Google credentials and wrangle it into data frames. We then create scatterplot visualizations of our main correlations at the country-level, state-level in Madhya Pradesh, and state-level in Kerala. After that, we use Google credentials again to load in a GeoJSON file of India's state boundaries. We create three graphs of the whole country, displaying per capita income, vaccination rates, and COVID cases by state. We then load in a GeoJSON map of Kerala's districts from a Google Drive file and create maps of Kerala's per capita income, population density, COVID cases, and vaccination rates by district. 

# Contributing to the code
### Next steps
Next, this project could explore population density correlations for the whole country if the data can be found. It could also include graphs or maps that change by date over time to show changes in trends throughout the crisis.
### Questions
Our work raises questions of resource allocation equity with the vaccine, whether disparities occur based on wealth or urbanity. It also raises questions of how much of a "protective" factor wealth is against the spread of a deadly virus, especially when wealthy populations have chosen to live in highly transmissible areas like cities. Our hypothesis that wealth would have a reverse correlation with COVID cases was not supported by this data, which ultimately raises questions of why that is.
### Challenges
Much of our data came from government websites or Indian data/media sources. It was typically not in convenient formats, so we had to use the Google Drive spreadsheet solution. There are also related challenges of data availability, which prevented analysis of population density for the whole country. 
### Known bugs
The main problem with our approach would probably be the Google Drive loading method. The files must be in one's own Google Drive and loaded in via Google authentication. If the files at the given Google Drive links are edited, the loading and wrangling may not work properly.

# Acknowledgements
We were inspired in part by the work of Monalisa Panda on Kaggle (https://www.kaggle.com/monalisapanda94/covid-20-second-wave-details-and-vaccination). We did not discover her work until we were about halfway done with our project, but we appreciated her graphs and thought about them throughout the second half of our project. Thank you, Monalisa!
We also received lots of support from our professor, Jeremy Manning, who taught us to use these tools and helped us workshop in class. Thank you, Professor Manning!