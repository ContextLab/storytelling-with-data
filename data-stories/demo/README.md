# Overview

I scraped tweets in the days after well-known mass shootings in the US from 2012 to 2017, and analyzed the frequency of keywords that indicated discussion of these shootings.

# Downloading the dataset

The dataset was a random sample of tweets on the day of and two days after each shooting, as well as a sample from Feb 1-3 each February from 2012 to 2017 to assess a baseline level of conversation (i.e., keyword use). The shootings were the Aurora movie theater shooting (7/20-7/22/2012, 12 deaths); the Sandy Hook Elementary School shooting (12/14-12/16/2012, 27 deaths excluding shooter); the Charleston church shooting (6/17-6/19/2015, 9 deaths); the Pulse nightclub shooting (6/12-6/14/2016, 49 deaths excluding shooter); the Las Vegas shooting (10/2-10/4/2017, 58 deaths excluding shooter); and the Sutherland Springs church shooting (11/5-11/7/2017, 26 deaths excluding shooter). The Las Vegas shooting occurred on October 1, 2017, but since it happened late at night, I sampled tweets from the following three days. I found a strong correlation between keyword use and number of deaths, but no evidence of change in baseline conversation about firearm policy as indicated by keyword frequency.

# Running the code

The code is straightforward and annotated. The twitterscraper package is used to scrape the tweets; the tweets are converted from a list to a string for easier analysis; and the frequency of each word in the sample is printed. It can be replicated for each shooting by changing the dates which are sampled. The string needed to run each search can be found by entering the search into "Twitter Advanced Search" and copying the resulting link into the code. The following libraries should be installed before running the code: twitterscraper, nltk, textblob.

# Contributing to the code

A comprehensive sampling of tweets after all mass shootings since 2012, or 2010 at the earliest, would produce more useful results. All definitions of mass shootings are arbitrary, but the Congressional Research Service's definition involves four or more casualties, and a number of databases exist.
