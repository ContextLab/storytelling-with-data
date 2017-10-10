# Overview

The [twitter-topics notebook](twitter-topics.ipynb) contains code for:
- Scraping twitter for keywords (or lists of keywords)
- Fitting topic models to lists of tweets
- Performing sentiment analyses on tweets
- Plotting the results with HyperTools

# Downloading the dataset

The data are downloaded automatically in the notebook (scraped from Twitter)

# Running the code

You need to install the following libraries in order to run the notebook: twitterscraper, nltk, and textblob.  You can do this (from within docker) by running:
```
pip install textblob
pip install nltk
pip install twitterscraper
```

# Contributing to the code

To contribute to this project, make a *new* Jupyter notebook (you can copy twitter-topics.ipynb to use as a template) and name it something informative, like (tweet-sentiments.ipynb).  Also create a new readme (you can use this one as a template) and name it something that matches your new notebook (e.g. tweet-sentiments.md).

Please document your code with markdown and python comments!
