# Overview

This project is based on the [twitter-topics notebook](https://github.com/ContextLab/storytelling-with-data/blob/master/data-stories/twitter-election/twitter-topics.ipynb), which contains code for:
- Scraping twitter for keywords (or lists of keywords)
- Fitting topic models to lists of tweets
- Performing sentiment analyses on tweets
- Plotting the results with HyperTools

Whereas that project is primarily based around exploring election-related tweets, this project is aimed at exploring finance-related trends.

## Important note
The code here is provided *as is*: any financial decisions you make based on the analyses in this project (or other course-related projects in this repository) *are at your own risk*.  **We do not guarantee any aspect of their functionality-- there are likely to be bugs, inaccuracies, misleading statements, etc.**

# Downloading the dataset

The data are downloaded automatically in the notebook (scraped from Twitter)

# Running the code

You need to install the following libraries in order to run the notebook: twitterscraper, nltk, textblob, and pandas-datareader.  You can do this (from within docker) by running:
```
pip install textblob
pip install nltk
pip install twitterscraper
pip install pandas-datareader
```

# Contributing to the code

To contribute to this project, make a *new* Jupyter notebook (you can copy twitter-trends.ipynb to use as a template) and name it something informative, like (tweet-sentiments.ipynb).  Also create a new readme (you can use this one as a template) and name it something that matches your new notebook (e.g. tweet-sentiments.md).

Please document your code with markdown and python comments!
