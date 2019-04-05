# Overview

This analysis looked for trends in the 9 categories of McDonald's menu items.  The first plot simply compares the average calorie counts between the categories, highlighting a high variation in options within each. The second reduces the items' various nutritional attributes (e.g. grams of fat, protein, carbohydrates, sugar, etc.) to two dimensions and plots them, enabling a high-level examination of the 9 categories' clustering tendencies, as well as that of the entire menu. 


# Dataset

source: https://www.kaggle.com/mcdonalds/nutrition-facts/version/1

`menu.csv` contains each of the 260 items on the McDonald's menu (as of 2017), along with the category on the menu it falls under, its standard serving size, and its basic nutrition facts. The items and nutrition info was scraped from the McDonald's website.


# Running the code

To replicate these anlyses, first make sure the dataset (`menu.csv`) is present in the same directory as `fitzpatrick_paxton.ipynb` (alternatively, update the path to the CSV file in `pd.read_csv()` in cell 2 in the notebook. Open `fitzpatrick_paxton.ipynb` and run each cell, sequentially. Cell 6, **visualize clustering of nutrition info** will take a few moments to run. **NOTE:** if running the notebook with a newer version of Pandas than 0.22.0, check to make sure the output order of menu categories from `menu.index.levels[0]` matches the order of `legend` after running cell 6.  `Pandas.MultiIndex` label behavior was changed slightly in a recent update.


# Contributing

The best way to contribute to this analysis in its current state would be to determine what nutrition attributes contribute most heavily to a a menu item's location on the 2D `UMAP` embedding. One could begin by simply correlating each column of the `menu` DataFrame (sans the columns dropped in cell 5!) with the each item's location in the 2D plane.  It may also be useful to try different reduction algorithms (potentially Sparse PCA) to see if the clustering is similar or different.
Another analysis that would be potentially interesting would be to scrape the McDonald's website for descriptions of their menu items, transform the descriptions with a trained topic model, and featurally examine at how the company chooses to describe items from different menu categories, or items of varying levels of "healthiness."  One could also attempt a sentiment analysis on the same gathered data.