## Authors
Group Name: JAMRS
Individuals: Jay Zhou, Aly Berger, Matt Rube, Richard Yang, Sonia Rowley

## Overview
All of our analyses were exploratory. We sought to described and better understand patterns in this dataset. Specifically, we were interested in town-level data and demographics. 

In `aly_analysis_final`, we created a hypertools plot to get a high-level summary of the individual-level data and visuzlize the potential presence of patterns. Then, donations from each town was grouped by deciles and shown in a bar graph. The primary insignts we gained were as follows:
* The majority of donations come from the top decile, and tapers off dramatically.
* Further analysis is needed to determine the cost / benefit of directing fundraising efforts in smaller towns.

In `richard_plots_final`, we created six basic, descriptive plotly express scatterplots to visualize the relationship between town-level demographics and both restricted and unrestricted donations. The primary insights we gained from these visualizations were as follows:
* There appears to be positive relationships between Avg UR Donation and Avg R Donation _amounts_ and MedianHHIncome.
* There also appears to be weak positive relationships between Avg UR Donation and Avd R donation _counts_ and MedianHHIncome.
* There appears to be no relationships between Avg UR Donation and Avg R Donation _amounts_ or _counts_ and age (i.e. the number of people in a town that are 55+ years old).

In `sonia_heatmaps_FINAL`, we created heatmaps to visualize UR donation amounts over time in each town. The primary insights we gained from these visualizations were as follows:
* Over the years, Hanover has given the most to this organization by far. Norwich, Lyme, and "Other Towns" in MA, VT, and elsewhere have also donated substantially.
* No clear patterns emerge across towns or over time. 

In `jay_map_final`, we used Mapbox and plotly express to create a map showing the size and number of restricted donations from each town. The primary insights from this analysis were as follows:
* UVLT could be doing more to engage higher income / educated regions.
* Towns with greater acreage generally donate on a more frequent basis.

In `matt_analysis_final`, we compared median household income with membership and unrestricted donations on a scatterplot. Then, we did a linear regression analysis on unrestricted donations and various demographics. The primary insights from this analysis were as follows:
* There is no clear relationship between median household income in membership, but there appears to be one between median household income and donations given.
* Using only linear regression analysis does not show much predictive power between various demographics variables and the size of unrestricted donations. However, of these variables, education demographics showed the greatest predictive power.

## Dataset
Data was sourced from the Upper Valley Land Trust (UVLT). Each of the analyses above uses data from the file `../data-stories/upper-valley-land-trust/data/UVLTdata_final.dta`, which shows donation and activity related to UVLT on an individual basis. Jay and Richard's analyses also use data from the files `../data-stories/upper-valley-land-trust/data/UVLTDataAnalysis.xls` and `../data-stories/upper-valley-land-trust/data/TownLevelData.xlsx`, the latter of which shows demographics information on each town relevant to UVLT activities.

## Running the Code
The JAMRS folder itself should be in the same folder as the UVLT data files. Each notebook (outlined above) can be run individually by running each cell in succession. Ignore other files in the JAMRS folder with titles that do not include `_final` or `_FINAL` at the end.

## Contributing
Each group member was the primary author on the notebook with their name on it, although we worked collaboratively on all analyses. Sonia and Jay received help from Jeremy with some of their code. Specifically, Jeremy helped Sonia group rows in a dataframe by town and he helped Jay write a function to extract zipcodes from a dataframe.

Future predictive analyses could to build on Matt's work. Of the factors he analyzed, Matt found that the factor with most ability to predict average UR donations was the % of a town's population with a BA. This factor could be explored in further predictive analyses using more powerful tools, like deep learning.

Future analyes could also use the plot formats we have created to compare different sets of variables. For example, Jay's maps could be altered to represent average Unrestricted Donations per town, instead of average restricted donations per town. 