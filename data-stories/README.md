
# Setting up a new project

## Creating a project folder on GitHub
Each project should exist as a subfolder of the current [data-stories](https://github.com/ContextLab/storytelling-with-data/tree/master/data-stories) folder.  An example project may be found [here](https://github.com/ContextLab/storytelling-with-data/tree/master/data-stories/demo).  You should create the following files (if it helps, you can start with "dummy" versions of the files by copying the files from the demo project):
- **README.md** -- documentation for your project
- **notebook.ipynb** (you can rename this file to something descriptive) -- code for running the key analyses and/or generating the key figures

You can also add additional files that you think are useful.  Note: do *not* store big datasets in GitHub-- it can't deal with big files well!  But if your dataset fits in a small spreadsheet file or text file, it's probably fine to store here.

## Updating the course computing environments
Occasionally projects will require packages that aren't yet included in the JupyterHub environment or Docker image.  To add request that new packages be added (e.g. so that everyone can run your code):
- Send a message to me (@jeremy) on Slack, telling me which specific packages you'd like to add
- Post a message to the #computing-tools channel on Slack, telling everyone to restart their Kernel and/or update their Docker image (so that they can run your code!)

## Setting up a Slack channel (optional)
If you're starting a several-person project, you should start a new channel on the course Slack account.  Be sure to invite all team members, me (i.e. the course instructor, i.e. @jeremy), and others who express an interest and/or who you want to be aware of your project.
