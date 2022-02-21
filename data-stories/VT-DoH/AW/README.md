# Project information
The correlation between fast food restuarants, access to healthcare,  and coronary heart disease/stroke levels per county in Vermont. Authors include Alex Wells (AlexWells-22) and Akiah Watts (AkiahW). Alex Wells found the heart disease and income data sets, worked on adding the files into the code, and the fast food choropleth maps. Akiah Watts made the fast food per county file, helped with the coding/debugging, and construction/analysis of the health related choropleth maps. 

# Overview
Our main question is to see whether there is an intereaction between the amount of fast food restuarants in a county, heart attack/stroke deaths, and insurance. Mainly, we wanted to see if locations with more fast food restuarnts had higher prevalences of heart attack/stroke deaths than places with fewer fast food restuarants. 

We approached this question by aggregating the number of popular fast food chains per county in Vermont and then choropleth mapping the amount of fast food chains per capita. We then created choropleth maps for the health data specifically looking at how the counties statistically relate to the average in Vermont as either better, same, or worse. The created choropleth maps for levels of hypertension/high blood pressure, deaths from heart attacks, deaths from strokes, and access to healthcare. We found that people who weren't insured didn't have a statistically significant difference in access to healthcare than average in Vermont which is a positive thing. We also found that Rutland County, which had the highest amount of fast food restuarants per capita in Vermont, also had a higher than average in Vermont at a statistically significant level death rate from strokes. And Caledonia County is on the higher end of fast food resturants per capita in Vermont and has a statistically significant higher heart disease death rate per 100,000 than average in Vermont. On the opposite end, the counties on the lower end of fast food restuarnts per capita like Esssex and Orange County didn't show statistically signifcant differences in our areas of interest.


Youtube link: https://youtu.be/JDdsRdtlodY

# Downloading the data

Food file shows the number of various fast food resturants per county in Vermont. This data set was created by our team using the listed sources 
Food file: https://raw.githubusercontent.com/ContextLab/storytelling-with-data/master/data-stories/VT-DoH/Fast%20Food%20Restaurants%20-%20Sheet1.csv
Sources: https://docs.google.com/document/d/1djIMtBM74CTyHmichuHmLFcyj79AcU0ERvr2m4WuCQI/edit?usp=sharing

Access file indicates the percentage of people between the ages of 18-64 by county from 2008-2015 with or without insurance and compares it to the percentage of people in the state with access to health services. 
Access: https://github.com/ContextLab/storytelling-with-data/raw/master/assignments/assignment%204/data/Access%20to%20Health%20Services.xlsx

Heart file shows the coronary heart disease death rate per 100,000 people and stroke death by counties in Vermont from 2000-2015 and then compares it to the entire state of Vermont.
Heart: https://github.com/ContextLab/storytelling-with-data/raw/master/assignments/assignment%204/data/Heart%20Disease%20%26%20Stroke.xlsx

# Running the code

Start by running the lines of code to initialize the data. The food variable is a data set of the number of various fast food resturants per county in Vermont. The access variable is a data set of the percentage of people between the ages of 18-64 by county from 2008-2015 with or without insurance and compares it to the percentage of people in the state with access to health services. The heart variable is a data set of oronary heart disease death rate per 100,000 people and stroke death by counties in Vermont from 2000-2015 and then compares it to the entire state of Vermont. We also have a geography section which is for constructing the maps and the fips section which assigns numerical values to the location of the counties allowing them to be mapped. 

In analysis, the first thing we did was add a column that aggregates the total number of fast food places per county. With this, we created the choropleth maps of total fast food places by county and fast food places per capita. Both are color coded such that counties with more fast food restuarants are more yellow in color and counties with fewer fast food places are darker in color with zero being a deep purple. The next set of choropleth maps show the coronary heart disease death rate data per 100,000 people per county, hypertension rate data per 100,000, access to healthcare among adults who cannot obtain or delay care, and stroke death rate per 100,000. In these maps, the counties are statistically compared to the average in Vermont and are considered either better (yellow), same (teal), or worse (deep purple). 

Link to code: https://colab.research.google.com/drive/1n3Wxdm5rbHojGnGu2lx0YCKvX_SiXRDU?usp=sharing

# Contributing to the code
Next steps are finding more up to date datasets of the current year for the health related information and do an additional correlation to distribution of socioeconomic status per county.

# Acknowledgements

Citations for the food dataset sources: https://docs.google.com/document/d/1djIMtBM74CTyHmichuHmLFcyj79AcU0ERvr2m4WuCQI/edit?usp=sharing

Akiah's computer science major boyfriend Robert for helping with debugging.
