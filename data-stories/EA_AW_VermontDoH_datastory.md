# Project information

We both contributed to the coding, research, and video portions of the project. Emily Appenzeller ’22 (EmilyApp2) identified/processed the data sets, coded the tables and graphs, researched heart disease and cholesterol, and co-wrote the script. Allison Wachen ’22 (allisonwachen) performed research on heart disease and cholesterol, co-wrote the script, edited the video, and helped with coding and debugging. Emily uploaded the assignment to GitHub and Allison posted the video to YouTube.

# Overview

We investigated the role of and access to cholesterol screenings in Vermont. Specifically, we explored how social factors — including insurance coverage rates and the number of healthcare providers per capita — impacted people's access to cholesterol screenings. We noted trends over time in accessing healthcare screenings and insurance. And, we analyzed if there was a connection between cholesterol screenings and the incidence of heart disease-related deaths or hypertension. 

We were interested in these trends statewide and in the Upper Valley region — which contains Windsor and Orange Counties in Vermont. Previous research conducted by the Vermont Department of Health indicated that the prevelance of high cholesterol in Windsor County was a significantly higher than the state average. 

To explore these questions, we analyzed heart health and healthcare access data from the Vermont Department of Health in Google Colaboratory.

Findings: 

Statewide, we discovered that there was a moderate, positive correlation between the prevalance of physicians and the percentage of cholesterol checks: the more physicians in the area, the more people receiving cholesteral checks.

We also discovered a moderate, positive correlation between the number of insured people and the percentage of cholesterol checks: people with insurance are more likely to get cholesterol checks.

Both Windsor and Orange counties and statewide, we found that the percentage of people getting cholesterol checks increased. However, from 2004 to 2016, the number of cholesterol checks in Windsor County lagged behind those in the rest of the state. Orange County had higher rates. Given that parts of Orange County lie outside the Upper Valley and that there is a higher percentage of people getting cholesterol checks there, we decided to focus on Windsor County for our video. 

Video: https://youtu.be/aBG3cjYn7cQ

# Downloading the data

Health Access Data: https://github.com/ContextLab/storytelling-with-data/raw/master/assignments/assignment%204/data/Access%20to%20Health%20Services.xlsx 

Heart Disease Data: https://github.com/ContextLab/storytelling-with-data/raw/master/assignments/assignment%204/data/Heart%20Disease%20%26%20Stroke.xlsx

The datasets contain 2000 - 2017 health data from the state of Vermont broken down into state, county, district office, and hospital service levels. 

The health access data included variables for percenters of Vermonters with health insurance (age 18-64, 17 or younger, statewide), percent of adults who cannot obtain care or delay care, percent of adults with a usual primary care provider or a specific source of ongoing care, percentage of persons with insurance coverage for clinical preventative services, and the number of FTE Primary Care Providers per 100,000 (nurses, physicians, physician assistants, dentists).

The heart disease data set included the percent of adults with a cholesterol check in the past 5 years, percent of adults with hypertension, percent of children and teens with hypertension, deaths by coronary heart diesease per 100,000, and stroke death rate per 100,000.

# Running the code

Code: https://colab.research.google.com/drive/1tp2jWZ8W6YZILvy0F155_UUzVzKTFOMC?usp=sharing

Packages: 
- We used numpy and pandas packages for processing the data
- We used plotly, plotly.express, seaborn, matplotlib, pyplot, and mpl_toolkits.mplot3d for visualizing the data.

Key steps:
- Load in data
- Process data, selecting for certain years, counties, or indicators
- Run correlations between two indicators
- Plot how indicators change over time on a county-specific level.

# Contributing to the code
Tell other people how they can contribute to the project you've started. Specifically:

Limitations:
- We realized that the presence of cholesterol checks did not tell us the rates for people actually having high cholesterol. It would be helpful to explore cholesterol level data from the same period
- Our data was somewhat spotty and outdated. The last years included were 2017 or earlier, and some variables were missing data.

Next Steps:
- Conducting our analysis with updated data
  -  Have the percentage of people getting insurance and the percentage getting cholesterol checks both continued to increase? 
  -  How has the correlation between different factors changed with the updated data?
  -  Impact of COVID-19
- Exploring how rates of high cholesterol connect to the other data points
  - Are people more likely to get cholesterol checks if they have high cholesterol? 
  - How do rates of high cholesterol correlate with prevelance of heart disease deaths and hypertension in Vermont — and does this match trends nationwide?

# Acknowledgements

Thank you to Professor Jeremy Manning. (jeremymanning) for helping us process the datasets and debug the code.
