# Overview

This assignment pulled data from FiveThirtyEight's repository on GitHub. FiveThirtyEight is a data analytics blog that focuses on politics, economics, and sports. Its soccer blog has compiled a list that ranks ~650 clubs from around the world on a Soccer Power Index. The Soccer Power Index (SPI) is based on a team's offensive and defensive abilities, in addition to how much it spends in the summer transfer market. The SPI is adjusted on a match-by-match basis, with the score falling when a team loses a game that the model predicts it to win. In my analysis, I look to track how closely offensive ratings track with SPI, which by extension provides us with an estimation of how heavily dependent SPIs are on a team's offensive performance. Furthermore, the data set includes information on a team's defensive score and their ranking movement, which I use to plot in a multi-dimensional visualization.


# Dataset

The dataset can be found here: https://github.com/fivethirtyeight/data/tree/master/soccer-spi
The data shows each of the clubs' names, the professional league that they belong to, along with their current rankings, ranking movement compared to the previous year, and performance statistics like SPI, offensive score, and defensive score. 


# Running

To run this notebook, one must go in order from top to bottom. It is especially key to run the first cell first, which imports the various plotting and data visualization libraries. Additionally, the third cell, which cleans the data and re-orders the columns, should not be run more than one time because it is hard-coded to move the first two columns. If run more than once, this would make the dataset fairly difficult to interpret. Cells 4-6 simply plot the data and create a numpy array -- they only need to be run after cells 1-3.


# Contributing

There are several interesting ways in which this project could be expanded upon. There are certainly different ways to present the data that I initially plotted. For one, a researcher could plot the ranking variables on the Professional Leagues, perhaps narrowing it down to the top 25 or so leagues to keep the x-axis clean and interpretable. Also, one could look into the relationship between offensive score and ranking movement, or defensive score and ranking movement. It would be interesting to see what facet actually impacts results. If we had more data across a longer timespan, I would have liked to research whether certain leagues shot up in the rankings across the years.   