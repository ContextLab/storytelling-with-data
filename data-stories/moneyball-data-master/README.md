# Project information

In this project, we examined the data used by the Athletics baseball team as portrayed in the movie "Moneyball" which resulted in their massively succesful 2003 season despite having an extremely low budget relative to other teams at the time. 

# Overview

This is where you describe what your project is about, in a few sentences.  Specifically:
- Our main question was how can the tecniques applied by Billy Beane in the Moneyball story apply to the MLB and impact it going forward as a whole?
- We did so using data compiled on Kaggle which contained the main metrics that they considered; OBP, SLG, and Rs.
  - We used seaborne's lmplot() function primarily which fits a regression plot to the data provided to it. 

The link to our video story can be found [here](https://www.youtube.com/watch?v=FV7cSq2wPkM&feature=youtu.be).

# Downloading the data

The following [link](https://www.kaggle.com/wduckett/moneyball-mlb-stats-19622012/data) is to the original data set however we put it within our github folder for easier download by running:

df = pd.read_csv('https://raw.githubusercontent.com/scottstuart11/moneyball-data/master/baseball.csv')

# Running the code

The code for our project can be found in the following notebook: https://github.com/scottstuart11/moneyball-data/blob/master/moneyball.ipynb

# Contributing to the code

Tell other people how they can contribute to the project you've started.  Specifically:
- Some of the next steps could include pulling data from more recent years than 2012 or also collecting data from other sports and seeing how certain metrics there can be similarly predictive of team / player success

# Acknowledgements

Although this article used R, we were able to similarly recreate the linear regression capabilities it used in python using seaborn:
https://kharshit.github.io/blog/2017/07/28/moneyball-how-linear-regression-changed-baseball
