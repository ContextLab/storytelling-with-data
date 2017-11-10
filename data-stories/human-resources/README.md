# Overview

My project was about human resources analytics. I used a dataset from Kaggle that wanted someone to solve the problem of employee retention. I created different plots to assess which factors contributed most to employee turnover.

# Downloading the dataset

The following dataset provides the data associated with each variable recorded. Each data point corresponds to each employee.

https://www.kaggle.com/ludobenistant/hr-analytics

# Running the code

First you want to import the different tools for the notebook. using the following code:
import pandas as pd
import hypertools as hyp
import numpy as np
import seaborn as sns

Then you want to read in the data
To read in the data use the code:
data = pd.read_csv(raw_data)

Organize the data so you can see each variable. Use the follwing code:
data.head()

From there you will need to use different tools, such as hypertools and seaborn, in order to start creating plots. Here are a few different types of plots I used:
hyp.plot(data, '.', model='SpectralEmbedding', group=data['salary'])
sns.factorplot(kind='bar', data=data, x='satisfaction_level', y='salary')

You can replace the code for the kind of graph that you want to use and the variables that you want to compare.

Here's a link to all the different types of graphs you can plot through seaborn:
https://seaborn.pydata.org/tutorial.html

Most of the variables were numeric so plotting them was easy. There were a couple that I had to change in order to plot. In order to do that you simply change the categorical variable, salary, to a numeric form. This will help when you are comparing different variables to see their effect on employee retention.

Here is an example:
data['performance'] = data['salary'].replace({'low': 0, 'medium': 1, 'high': 2})
data.head()

# Contributing to the code

I would suggest doing a regression and possibly a t-test to see if there is a significant correlation between the different variables. This would help support or possibly refute the claims I made from the code I already created.
