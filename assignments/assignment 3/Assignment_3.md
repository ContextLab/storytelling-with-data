# Storytelling with Data: Assignment 3

## Overview
The purpose of this assignment is to introduce you to the process of collaborative storytelling with data.  You will work with up to 4 other students (max group size: 5 students; min group size: 2 students) on this assignment.  Every group will be analyzing the [same dataset](https://github.com/ContextLab/storytelling-with-data/tree/master/data-stories/upper-valley-land-trust), provided by the [Upper Valley Land Trust](https://uvlt.org/).  Completing the assignment entails finishing *all* of the tasks below.  To receive credit for this assignment you must submit it by making a pull request to the [main course GitHub repository](https://github.com/ContextLab/storytelling-with-data) by the due date (prior to the start of class on Friday, April 19, 2019).  This assignment is worth 4% of your final course grade.

### Background
I have provided a [sample notebook](https://github.com/ContextLab/storytelling-with-data/blob/master/data-stories/upper-valley-land-trust/uvlt_explorations.ipynb) in the `data-stories/upper-valley-land-trust` folder to help get you started.  The notebook outlines some general functions that you might find useful for this assignment:
- Loading in and viewing the various parts of the dataset
- Data wrangling and cleaning
- Doing some prediction analyses-- trying to predict individuals' donations and/or volunteer hours using their past history

To facilitate working on this assignment, you may find it useful to go through one or more of [these `scikit-learn` tutorials](https://scikit-learn.org/stable/tutorial/index.html) and/or the examples or tutorials suggested in the [data visualization notebook](https://github.com/ContextLab/storytelling-with-data/blob/master/slides/data_visualization.ipynb).

## A note on what it means to "complete" this assignment
You may not be able to complete every part of this assignment.  That's OK!  If you are stuck on any step or task, you can still earn most of the credit (up to 90%) if you do the following for each thing you got stuck on, written in one or more `Markdown` cell(s) within your assignment's Jupyter notebook(s):
1. Describe (in plain English) what you were trying to do
2. Describe how you tried to solve the task
3. Describe what you thought would happen when you tried solving the task in that way
4. Describe what actually happened
5. Describe what you did to help get yourself unstuck (e.g. asked a classmate, met with the course instructor, posted questions to Slack, searched on Google or Stack Exchange, read a book, watched a tutorial, etc.)
6. Estimate how much time you spent working on that part of the assignment (rounded to the nearest hour)

## Setup task list
  - [ ] Update your GitHub fork of the class repository by pulling in the latest changes (the second add_remotes command ensures you will have run the latest version of that command):
```
./add_remotes.sh
git pull upstream master
./add_remotes.sh
```
  - [ ] Come up with a name for your group
  - [ ] Inside the `data-stories/upper-valley-land-trust` folder, create a new sub-folder for your group (named after your group name).  We'll call this folder `data-stories/upper-valley-land-trust/<GROUP NAME>`.
  - [ ] Designate one group member to create a `README.md` file inside the `data-stories/upper-valley-land-trust/<GROUP NAME>` folder.  This will contain documentation for your assignment.  Somewhere in the README file, add a heading called `Authors`.  Under that heading, add a numbered or bullet pointed list of your group's members.  (You will add other text to this file later.)

## Assignment instructions
Your Assignment 3 submission will comprise the following, all contained in your group's folder (i.e., `data-stories/upper-valley-land-trust/<GROUP NAME>`):
- a `README.md` file with documentation and a list of project group members
- one or more Jupyter notebooks
- optionally, some other data that you download (along with associated documentation)

Your job for this assignment is to discover or report something "interesting" about the Upper Valley Land Trust data (here *interesting* is defined broadly to mean whatever you think it means in the colloquial sense).  Your assignment could take the form of an analysis or series of analyses, a data visualization of some sort (the [course textbooks](https://github.com/ContextLab/storytelling-with-data/blob/master/admin/PSYC_81_syllabus.pdf) contain some inspiring example figures; you may also find interesting example data visualizations on [fivethirtyeight.com](https://fivethirtyeight.com/)), or similar.  You will present your findings as a (5ish minute) "data story" to the class, and we will discuss and constructively evaluate each other's approaches and findings.  Ideally you should try to find some "truth" about your dataset and make a convincing case about what you think is going on.

### Where to begin
I recommend starting with a brainstorming and discussion session.  For example:
- What sorts of questions might you want to ask about this dataset?
- What sorts of questions might you be *able* to ask about this dataset?
- Are there other datasets you might want to pull in to help make your case?  (If you download additional data, add the relevant files to the `data-stories/upper-valley-land-trust` folder along with one or more README files describing the new data, where they came from, etc.)
- Are there particular tools (e.g. Python libraries) or approaches that you are excited to learn about, that you may want to use for this assignment?
- Can you draw inspiration from other analyses or datasets that might be related in some way?
- What sorts of approaches might be more or less appropriate for crafting into a cohesive story?
- What sorts of stories will your classmates likely find interesting?
- What are the challenges you are likely to encounter, and how might you approach overcoming them?
- What are the strengths of each group member, and how can you play to each other's strengths?

### Starting the assignment
Inside your group folder, create one or more Jupyter notebooks.  Add some markdown cells to create a basic outline of what each notebook will ultimately contain.  Also update your group's `README.md` file following [this basic format](https://github.com/ContextLab/storytelling-with-data/blob/master/data-stories/demo/README.md):
  - [ ] Five headings (each denoting a different section): Authors, Overview, Dataset, Running the code, Contributing
  - [ ] In the *Authors* section (described above), simply list your group's members.
  - [ ] In the *Overview* section, write a few sentences about what you did for your project (e.g. what was the "point" of the analyses you ran)
  - [ ] In the *Dataset* section, briefly describe the subset of the data (or additional datasets) you chose to analyze.  Include links to any relevant documentation and/or descriptions of data formats where relevant.
  - [ ] In the *Running the code* section, briefly describe how someone should run your notebook.  (Assume your audience is someone else in the class.)  If you have more than one notebook, explain what each notebook does.
  - [ ] In the *Contributing* section, briefly describe how other people could build on your work.  For example, you might have ideas for sections of your notebook(s) that could use some cleaning up or debugging, or you might have ideas for followup analyses.  Also acknowledge any sources (e.g. other non-group students you consulted for this assignment, code you copied or references, etc.).

In addition to the code needed to run any analyses or generate figures, your notebook(s) should include (in markdown cells) human-readable descriptions of the analyses and any findings.  You'll use these markdown cells to tell your "story."

### Workflow
An important part of this project will likely be to find a system for tracking project tasks.  You may find it useful to divide your project into one or more [GitHub issues](https://github.com/ContextLab/storytelling-with-data/issues), create a [Slack channel](http://stories-about-data.slack.com) to coordinate discussions, use a [Trello board](trello.com) or another organizational tool, or use some other software tool to help keep track of who is doing what.

You should always write code on your own fork.  However, you can share code by pulling in code from your group member's forks.  To pull code from a classmate's fork, you can use the following syntax:
```
git pull jeremy master
```
(replacing `jeremy` with the lowercase first name of whichever group member's code you want to pull into your fork.)  You can then run
```
git push
```
to incorporate the changes into your own fork.

### Submitting the assignment
To submit the assignment, add your group's folder (add all assignment files) to your fork (using `git`'s `add`, `commit`, and `push` commands) and then submit a `pull` request to merge your changes into the [main course GitHub repository](https://github.com/ContextLab/storytelling-with-data).

Your assignment is considered to have been submitted when one of your group members makes a pull request to the main course GitHub repository.  (You should discuss amongst your group members to decide who is going to submit the pull request.)

## Honor code
This is a group project.  You will be working directly with other students, and you are allowed (and encouraged!) to copy each other's code, incorporate code you find on the internet, borrow other code from the course repository or from other groups, etc.  The only "honor" requirement is that each group member must make at least one pull request (either to the main course GitHub repository, or to another group member's fork).
