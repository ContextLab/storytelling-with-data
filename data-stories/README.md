
# Setting up a new project

## Creating a project folder on GitHub
First, you should fork the main class repository and clone the (forked) repository to your computer.  Invite any project collaborators to have read and/or write and/or administrative access to the project.  If you're a student, please also invite [me](@jeremyrmanning) as an admin!

Each project should exist as a subfolder of the current [data-stories](https://github.com/ContextLab/storytelling-with-data/tree/master/data-stories) folder.  An example project may be found [here](https://github.com/ContextLab/storytelling-with-data/tree/master/data-stories/demo).  You should create the following files (if it helps, you can start with "dummy" versions of the files by copying the files from the demo project):
- **README.md** -- documentation for your project
- **notebook.ipynb** (you can rename this file to something descriptive) -- code for running the key analyses and/or generating the key figures

You can also add additional files that you think are useful.  Note: do *not* store big datasets in GitHub-- it can't deal with big files well!  But if your dataset fits in a small spreadsheet file or text file, it's probably fine to store here.

## Setting up a Slack channel (optional)
If you're starting a several-person project, you should start a new channel on the course Slack account.  Be sure to invite all team members, me (i.e. the course instructor, i.e. @jeremy), and others who express an interest and/or who you want to be aware of your project.

## Updating the class Docker image (optional)
Occasionally projects will require packages that aren't yet included in the Docker image.  To add request that new packages be added to the Docker image:
- Send a message to Andy (@andy) on Slack, telling him which specific packages you'd like to add
- Post a message to the #general channel on Slack, telling everyone to update their Docker image (so that they can run your code!)
