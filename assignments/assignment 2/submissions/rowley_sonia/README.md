## Overview
My analyses in this notebook are descriptive. I plotted `visitedresources` against `raisedhands` on a scatterplot, indicating the gender of individuals based on the color of the plot. I also created a histogram to show the frequency distribution of hand-raising in this sample. Although I did not run any formal analyses, these visualizations of the data indicate a few interesting patterns in the dataset. See my discusson of some of these patterns **What I Found** in the Jupyter notebook entitled `rowley_sonia`.

## Dataset
I chose an Students' Academic Performance dataset that I found in the data-stories folder, originally retrieved from https://www.kaggle.com/aljarah/xAPI-Edu-Data. The data from this dataset was collected from 480 students enrolled in an online learning platform from 14 different countries over 2 semesters. It includes sixteen attributes for each student, but I chose to focus on only two: raisedhands and visitedresources.

## Running the Code
To run my notebook, press the 'run' button at the top of the notebook for each cell.

## Contributing
First, future contributors could improve what I already have. They could more efficiently and elegantly clean the dataset. They could add a categorical key to the scatterplot, instead of a dimensional one, explaining that '1' and '0' are female and male, respectively. The key with graded colors is currently misleading, and I tried and did not succeed at changing it. 

Second, future contributors could conduct followup analyses on the reduced dataset that I created. Although I did not use gender in my analysis, I am interested in whether the frequency distribution of hand-raising and resource-visiting differs between male and female students. Does gender predict the strength of the relationship between hand-raising and resource-visiting? I do not know how to conduct an analysis like this, but I would be interested to learn.

I consulted Jeremy and my dad, Michael Rowley, about this assignment. The work is my own.

#### Questions that came up as I did this assignment
* Why is it important to remove non-numerical values from a dataset? The vast majority of the columns in this dataset were filled with non-numerical values.
* With the .values function, can you extract a subset of columns into a nparray?
* I dropped most of the columns of the dataset, and I had to list all of them. Is there any way to do this more efficiently?
* How do you change column names? I attempted this based on various online resources and each time I copy/pasted code, nothing changed. For example: `education_data.rename(columns = {"raisedhands":"raised_hands", "visitedresources":"visited_resources", "announcementsview":"announcements_viewed"})` 
* What is a heatmap? How can one interpret a seaborn heatmap?
* Many `numpy` tutorials talk about 'broadcasting'. I have looked this up but I still don't understand what it means conceptually. What is broadcasting? 
* What is the difference between Plotly Express and Plotly? When I was trying to figure out how to make the scatterplot color key categorical (instead of dimensional), I struggled to find online resources specific to Plotly Express.