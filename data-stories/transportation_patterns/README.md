# Hackathon: Commuting Trends Analysis
By Jay and Richard

## Overview

We initially set out with the goal of finding trends across IPUMS data, a data set that we had brief exposure to in a Labor Economics class. Looking through the variables, we thought that trends in individuals' commuting patterns would be interesting to analyze, especially given various demographic variables that we also had access to, such as income, education level, gender, age, and geographic location. 

After downloading the dataset, we proceeded to clean it. We created 4 separate DataFrames to work in, each more specific and exclusive of non-zero, missing values than the last. Ultimately, the most specific DataFrame excluded individuals/rows missing Mode of Transportation, Carpooling, and County Code data, as well as those that had zero commuting time. When looking at the data by education level, we found IPUMS education classification to be too specific for any meaningful sort of analysis, so we created a function to bucket the individuals into broader education categories of Advanced Degree (MD, PhD, Masters, others), Undergraduate Degree (BA or Associates), HS Graduate (or GED), or less than HS Diploma.

Through our analysis, we found that a greater percentage of less educated individuals carpooled than those with higher degrees. The financial incentive definitely seems stronger than any sense of environmental duty. Overall, carpooling definitely tracks with income -- even comparing mean incomes of those who carpooled vs. those who drove alone within education buckets, the mean was always higher among solo drivers.

We also found that the data was strangely skewed towards those who only graduated from high school. Looking at he income distribution by transportation, we also saw a strange blip around households earning $500,000. The highest mean income of individuals by method of transportation was for those taking trains to work, followed by those working at home, those with motorcycles (albeit with a tiny sample size), and those taking the subway. 


## Dataset

The data set was pulled from the IPUMS USA website, found here: https://usa.ipums.org/

IPUMS USA includes data from the American Survey, from 2000-2017. Due to limitations in the size of file that we could upload to Jupyter notebook, we limited our analysis to individuals from Pennsylvania in 2017 -- this trimmed our initial file (which included all 50 states and all 17 years) from 3 GB to 0.1 GB. 

## Running

To run this notebook, one should go from top to bottom. After the "Recategorize Education Buckets" section, one could choose to omit running certain sections and it would not change the plot outputs. 

## Contributing

There are several ways this project could be expanded upon. For one, we would like to look at PA across a longer time frame, and perhaps expand our analysis to several different states. This might help us diversify our data set as well, since the current set of survey participants is comprised predominantly of those who only obtained a high school degree. Additionally, we would like to use the Datashader Python package to visualize county-to-county differences on a map. This might be a project for next week, especially if we can track these changes across time.  