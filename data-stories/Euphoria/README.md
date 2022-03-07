# Project information

Sentiment analysis of Twitter reactions after instances of Domestic Violnece on HBO's Euphoria. The team consists of Akiah Watts (AkiahW) and Saruul (Saruulijile2).

# Overview

This project is an analysis of two characters in the HBO show Euphoria. Since there is a consistent air time of the show, we were able to collect Twitter reactions directly after the episode aired but before the next episode. We specifically looked at reactions after episodes where each character engaged in violence toward their girlfriend.

What we were specifically interested in was whether there would be potentially racially driven differences between public opinion of the characters since one is a caucasian male and the other is a Black male or if there would be a halo effect and more forgiveness for his actions since Nate's character is ridiculously attractive. To explore the public perception, we manually scraped Twitter data on each of the characters of interest (Nate and McKay) in the time frame of the date the episode aired to the day before the next episode (a week). We used bar graphs and word clouds to visualize the data. Since the event of abuse wasn't isolated in the episode (Nate also threatened another character (Jules) in the episode where he physically abused his girlfriend and McKay experienced a traumatic hazing event directly before he was rough with his girlfriend) these events also colored the perception of the action. Interestingly, in McKay's case, people were generally more concerned about his mental state after his traumatic event than angry at him for how he physically took his emotions out on his girlfriend. Whereas people's tweets generally tended to have negative valence while insulting Nate and wanting to see justice served either through pressing charges or by his victims teaming up against him. It would be interesting to see the gender and ethnicities/races of the people commenting the message to see if there are any trends in that regard. 


YouTube Link: https://youtu.be/aLZkylRIK4E

# Downloading the data

Tweets about McKay following the epsiode where he commits an abuse act towards his girlfriend. 
McKay's tweets: https://github.com/AkiahW/storytelling-with-data-1/blob/f80dc74a7dc3c5e3c49f3a6f897f6cb3cadc474e/data-stories/Euphoria/McKay%20Tweets%20-%20Sheet1.csv

Tweets about Nate following the epsiode where he commits an abuse act towards his girlfriend. 
Nate's tweets: https://github.com/AkiahW/storytelling-with-data-1/blob/f80dc74a7dc3c5e3c49f3a6f897f6cb3cadc474e/data-stories/Euphoria/Nate%20Tweets%20-%20Sheet1.csv


# Running the code

Start by running the setup (outside libraries required for visualizing the data) and data (the aforementioned tweets). The spreadsheets include the tweets, and human analysis of the valence and category the tweet would fall under. Under the Analysis section, the first visualization is of the categories and counts of Nate's tweets with insults toward him and wanting to see him brought to justice being the main categories. The second visualization is the bar graph of McKay's categories with the main ones being anti-shipping (expressing wanting him and his girlfriend to no longer be dating) and concern. In addition to the categories, we also determined the valence of the tweet as either positive, negative, or neutral. The third visualization, shows the frequency of valence in the Nate tweets with the overwhelming majority being negative. And the fourth is that for McKay with neutral being the prevailing valence. After all the bar graphs, we made word clouds to show the common words in the tweets about each character minus stopwords like "the" and "and" and also minus the characer name, show name etc so that we could have a clearer visual of the spread. A word cloud was made for both characters.

# Contributing to the code

Some next steps would be to perform the same sentiment analysis for the girlfriends to see how people react to the victims of the abuse. Deeper analysis could incorporate the demographic information of the tweet authors and preform statistical analysis to see if there are any significant differences in the opinions of the characters.

# Acknowledgements

My lovely boyfriend and CS major Robert for debugging and helping with the construction of the first bar graph. 
