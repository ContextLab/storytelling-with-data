# Project information
### Group members
Amelia Ockert, Keara Dennehy (kearadennehy), Hannah Utter (hannahutter99), Nathan Hwang (nhwang1325)
### Contributions
Keara and Amelia did the data wrangling, visualizations, and some script work. Hannah and Nathan did the script and video. 

# Overview
### Main question
Our research question was loosely "does money buy happiness?", meaning that we wanted to analyze the relationship between happiness and GDP to discover whether GDP or another variable can predict happiness.
### Approach
We analyzed the relationship between GDP and happiness for every country with available data, then we zoomed in on a few happy European countries to see if changes in GDP were related to happiness. We then looked at another variable (social support) to discover another factor at play.
### Findings
Our main finding was a correlation between GDP and happiness but no change in happiness when GDP changed in a few wealthy, happy European countries. We then found a correlation between social support and happiness, as well as a correlation between social support and GDP. For Finland (the “happiest” country in the world in 2021), happiness appeared to fluctuate with social support. 
### Video link
https://www.youtube.com/watch?v=lsynvwGw7-k

# Downloading the data
### World Happiness Report 2021
https://www.kaggle.com/ajaypalsinghlo/world-happiness-report-2021?select=world-happiness-report-2021.csv
### World Happiness Report (years cumulative)
https://www.kaggle.com/ajaypalsinghlo/world-happiness-report-2021?select=world-happiness-report.csv

# Running the code
### Notebook
https://colab.research.google.com/drive/1M9kcbUHMoxKKZAl9z6STREA_2oYYq0US?authuser=3#scrollTo=yJ5JRDuLNNuI
### Description
At the start of our code, we install and smuggle all the libraries we wanted for this project. Then, we load in the data from Kaggle and create data frames. We then create scatterplot visualizations of the correlations that we explored. After that, we load in the over-time data and visualize some trends over time. We then create maps of happiness scores around the world and in the top 10 “happiest” countries and bottom 10 “least happy” countries.

# Contributing to the code
### Next steps
Next steps for this project might be to dig a little further into the GDP / Happiness index connection. We primarily explored changes in GDP versus changes in happiness for the wealthiest countries - but might we see a different relationship for low-to-mid GDP countries? In other words, might it be that for those countries already wealthy, changes in GDP do not equate to changes in happiness, but for countries with lower GDP, an increase above a certain threshold might have a larger impact on happiness.

We could also explore other indicators more in depth, beyond GDP and social support. Using the World Bank’s World Development Indicators, we could get an even fuller picture of the indicators related to happiness. https://www.kaggle.com/worldbank/world-development-indicators

### Questions
What does the GDP vs/ Happiness Index look like for the bottom-ranked GDP countries? Middle-ranked GDP countries?

Is there a certain change in GDP (or a certain threshold) that appears to be correlated with increasing happiness scores?

What are some of the other factors that seem more correlated with within-country changes in GDP?

### Challenges
This is a pretty robust and well-cited dataset from the World Happiness Report. As such, the data was pretty complete and fairly clean.
One difficulty was matching this dataset to Plotly’s chloropleth maps. This dataset did not include Iso-alpha codes, so we needed to make a column of those for every country in the dataset. Luckily, there is a package and function that can convert from country name to iso-alpha code, however several country names did not match the way this function codes for this, and so we had to manually sift through the data to find the problems and change the country names. 
Another difficulty is controlling for the many variables in this dataset. While the variables all indicate how strongly they influence the country’s Life Ladder (happiness index), it is tough to control for these when comparing happiness indices across countries.

### Known bugs
The only known challenge with our notebook is that you must load in the kaggle.json file in order to run kaggle commands and load in the data. 

# Acknowledgements
We received lots of help with debugging and story planning in class from our professor, Jeremy Manning. Thank you, Professor Manning!
