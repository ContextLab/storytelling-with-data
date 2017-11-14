# Overview

My project is analyzing the types of words used when people comment on the dances of different genres. I am going to see if there are patterns in the types of words used depending on the genre, For example, are there certain words used when commenting on a ballet video and are there certain words used when commenting on a hip hop video? What is the sentiment of the comments? Can I determine what genre of dance is in the video just based on the comments? 

I will be focusing on [So You Think You Can Dance](https://www.fox.com/so-you-think-you-can-dance).

I will be using [Youtube](http://youtube.com) to collect comments.

I will begin by creating a word cloud with [Wordle](http://www.wordle.net) to find patterns in word usage. There will be a map detailing my findings. 

# Downloading the dataset
I have scraped the data from the Youtube channels, so the dataset did not necessarily exist beforehand. I am gathering the top 200 comments from each video that I choose to scrape.

# Running the code
If you run the jupyter notebook you will see that the code is meant to scrape a YouTube video for data. The base code came from egertbouman [here](https://github.com/egbertbouman/youtube-comment-downloader/blob/master/downloader.py). I have focused in on scraping the comments of the video. The code will get the comments for each video id that is passed in. Then, I run a sentiment analysis on the comments. The scores correlating to each set of comments are then put into a list, and counted. I count negative sentiments (scores with a "-") and positive sentiments (scores without a "-").

# Contributing to the code
My project will go on github for other people to continue working on it!

#Videos
These are the videos that I pulled comments from:
###Contemporary
[Medicine](https://www.youtube.com/watch?v=RQ11mwgbReE) 
[Wicked Game](https://www.youtube.com/watch?v=khvcCpoFszM)
[Hallelujah](https://www.youtube.com/watch?v=G8u8xPLar-E)

###Hip Hop
[My Chick Bad](https://www.youtube.com/watch?v=hATakt0zOzg)
[Outta Your Mind](https://www.youtube.com/watch?v=TLtSfYX8tJk)
[Hello Good Morning](https://www.youtube.com/watch?v=tCb_UOakEQI)