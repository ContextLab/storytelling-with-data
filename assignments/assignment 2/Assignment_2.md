# Storytelling with Data: Assignment 2

## Overview
The purpose of this assignment is to introduce you to some "data wrangling" tools-- i.e. tools for organizing and manipulating data.  We will be exploring two tools in this assignment: [`Numpy`](http://www.numpy.org/) and [`Pandas`](https://pandas.pydata.org/).  You will download a sample dataset of your choosing (some example data sources may be found in the README file on the [main course GitHub repository](https://github.com/ContextLab/storytelling-with-data), or in the [data visualization notebook](https://github.com/ContextLab/storytelling-with-data/blob/master/slides/data_visualization.ipynb)).  Completing the assignment entails finishing *all* of the tasks below.  To receive credit for this assignment you must submit it by making a pull request to the [main course GitHub repository](https://github.com/ContextLab/storytelling-with-data) by the due date (prior to the start of class on Monday, April 8, 2019).  This assignment is worth 3% of your final course grade.

### Background
You may find it useful to go through [this `numpy` tutorial](https://docs.scipy.org/doc/numpy/user/quickstart.html) and/or [this `pandas` tutorial](https://pandas.pydata.org/pandas-docs/stable/getting_started/10min.html) prior to beginning this assignment.

## A note on what it means to "complete" this assignment
You may not be able to complete every part of this assignment.  That's OK!  If you are stuck on any step or task, you can still earn most of the credit (up to 90%) if you do the following for each thing you got stuck on, written in one or more `Markdown` cell(s) within your assignment's Jupyter notebook:
1. Describe (in plain English) what you were trying to do
2. Describe how you tried to solve the task
3. Describe what you thought would happen when you tried solving the task in that way
4. Describe what actually happened
5. Describe what you did to help get yourself unstuck (e.g. asked a classmate, met with the course instructor, posted questions to Slack, searched on Google or Stack Exchange, read a book, watched a tutorial, etc.)
6. Estimate how much time you spent working on that part of the assignment (rounded to the nearest hour)

## Setup task list
  - [ ] From the jupyter.dartmouth.edu page (after logging in), navigate to your folder in the `Psych81.09/course` directory.  Then navigate to the `storytelling-with-data/assignments/assignment 2/submissions` folder
  - [ ] Create a new *folder* inside the submissions directory called `<lastname>_<firstname>`.  This folder will contain all of the files for this assignment.  Within that folder, create a new Jupyter notebook (`<lastname>_<firstname>.ipynb`), selecting the `Psych 81.09` kernel from the dropdown menu in the upper right.
  - [ ] Create a `README.md` file within your assignment folder.  This will contain documentation for your assignment.

## Todo list
In your notebook, please do each of the following:
  - [ ] Create a cell at the top of your notebook that imports any libraries you'll be using in the rest of your notebook.  At minimum, import `pandas`.
  - [ ] Add a second cell that downloads or imports a dataset of your choosing into the notebook.  If you download your data to one or more files, save them to your assignment folder.  Load the data into a Pandas DataFrame and display the first 5 rows using `DataFrame.head`.
  - [ ] Add a third cell that does some data cleaning:
    - Remove non-numerical values (or turn non-numerical values into numerical values)
    - Use `fill_na` to remove "nan" values
    - Rename or drop rows and/or columns that are irrelevant
  - [ ] Add a fourth cell that creates a plot (can be of any type, using any graphics library including built-in `Pandas` functions)
  - [ ] Add a fifth cell that extracts the data from the dataframe as a `numpy` array (e.g., by using the `values` function)
  - [ ] Add a sixth cell that carries out some sort of basic analysis or data visualization of the numpy array.  For example, you could compute a summary of the data, plot a heatmap or barplot, etc.
  - [ ] Add one or more Markdown cells to describe what you did and what you "found"

Next, edit the `README.md` file you created in your assignment folder.  Add the following information about your assignment, following [this basic format](https://github.com/ContextLab/storytelling-with-data/blob/master/data-stories/demo/README.md):
  - [ ] Four headings (each denoting a different section): Overview, Dataset, Running the code, Contributing
  - [ ] In the *Overview* section, write a few sentences about what you did in your notebook (e.g. what was the "point" of the analyses you ran)
  - [ ] In the *Dataset* section, briefly describe the dataset you chose to analyze.  Include a link to (or description of) the source of your dataset.
  - [ ] In the *Running the code* section, briefly describe how someone should run your notebook.  (Assume your audience is someone else in the class.)
  - [ ] In the *Contributing* section, briefly describe how other people could build on your work.  For example, you might have ideas for sections of your notebook that could use some cleaning up or debugging, or you might have ideas for followup analyses.  Also acknowledge any collaborations (e.g. other students you consulted for this assignment).

Finally, add your assignment folder (add all assignment files) to your fork (using `git`'s `add`, `commit`, and `push` commands) and then submit a `pull` request to merge your changes into the [main course GitHub repository](https://github.com/ContextLab/storytelling-with-data).

## Advanced users
If you are already familiar with `pandas` and `numpy`, try using `apply` and/or [`groupby`](https://pandas.pydata.org/pandas-docs/version/0.22/groupby.html) somewhere in your assignment.  Other ideas:
  - Create some sort of interesting visualization, rather than just a basic visualization (e.g. something visually pleasing, an animated plot, an interactive plot, a 3-dimensional graphic of some sort, etc.)
  - Carry out some sort of interesting analysis, rather than just a basic analysis.
  - Use the `%%timeit` built-in "magic command" (or the datetime library, or another library or function) to estimate how scalable one of your functions or cells is.  For example, as you scale the size of the input data (add more rows/observations), what is the slowdown in your code's execution time?

## Submitting your assignment
Your assignment is considered to have been submitted when you make a pull request to the main course GitHub repository.

## Honor code
You may work with other students on this project, but you may *not* (simply) copy anyone else's code.  Note: you *may* "mix and match" code from other students, the course materials, code you find on the Internet, etc.-- but you need to be the one that actually enters the code and text into your notebook and understandings (and accepts responsibility for!) any code that makes it into your notebook.  Each student should independently submit their own work.  If you work with other students on this assignment you should make a note (in a Markdown comment) in your Jupyter notebook and/or in the README file for your assignment.
