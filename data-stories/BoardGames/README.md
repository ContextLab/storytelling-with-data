# Overview

Research shows that games can be used for good. In fact, the Tiltfactor lab here at Dartmouth designs games that confront biases, prevent diseases, and encourage prosociality. This notebook is meant to guide game designers by showing what categories of games tend to be highly rated and what game mechanics work best with those categories of games. We hope that, using our visualizations, game designers will create successful games that serve the greater good.

We begin this notebook by correlating game features such as # of players, playtime,age of target player, and release year against geek ratings (determined by boardgamegeek.com) and by visualizing the distribution of geek ratings among all of the games included in the dataset and the average geek rating of each category of game. In the second half of this notebook, we further analyze eight game categories (environmental, medical, card, fantasy, economic, puzzle, war, and murder/mystery). 

# Dataset

We downloaded a dataset from https://www.kaggle.com/mrpantherson/board-game-data. The dataset uses information from boardgamegeek.com, and therefore includes a "geek rating for each game." According to boardgamegeek.com, geek ratings differ from average ratings in that "To prevent games with relatively few votes climbing to the top of the BGG Ranks, artificial "dummy" votes are added to the User Ratings. These votes are currently thought to be 100 votes equal to the mid range of the voting scale: 5.5, but the actual algorithm is kept secret to avoid manipulation. The effect of adding these dummy votes is to pull BGG Ratings toward the mid range. Games with a large number of votes will see their BGG Rating alter very little from their Average Rating, but games with relatively few user ratings will see their BGG Rating move considerably toward 5.5."

# Running the Code

To run this code, you must first download the dataset. Then, navigate to "Cell" and click "Run All."

To interact with the "Find a Game" section, replace whatever categories and game mechanics you are seeking with x, y, and z. If you are searching for more than three qualities, add on to the provided code using the same format. In order for the code to run, you must spell each word exactly as it appears in the list provided in the notebook.

# Contributing

Those who contribute to this notebook might want to analyze game categories (e.g. party games and racing games) that were not analyzed in this notebook. They might also analyze games on an individual basis rather than on a categorical basis. 

Additionally, those who contribute to this notebook should consider analyzing the interactions between various categories and various mechanics.