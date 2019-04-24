# Storytelling with Data

This repository contains course materials for the Dartmouth Course [Storytelling with Data (PSYC 81.09)](https://pbs.dartmouth.edu/undergraduate/permission-courses/spring-2019).  The syllabus may be found [[here](https://github.com/ContextLab/storytelling-with-data/blob/master/admin/PSYC_81_syllabus.pdf)].  Feel free to follow along with the course materials (whether you are officially enrolled in the course or just visiting!), submit comments and suggestions, etc.  If you are a Dartmouth student currently enrolled in this course, please read the *Student instructions* below to get set up.  A list of tutorials and some ideas for tracking down some nice datasets may be found at the bottom of this document.

## A note about this Open Course
This course is taught as an *Open Course*, meaning that the course is designed from the ground up to be shareable and accessible to anyone.  To that end, all code for this course should be written in [Python](https://www.python.org/) and organized in a [Jupyter notebook](http://jupyter.org/).  Any data you analyze must be shareable with all other students in the course, and ideally it should be shareable with the public.  All code and other student-generated materials will be shared publicly.

# Student instructions

## Overview
We will use the following tools in this course:
- [Slack](https://stories-about-data.slack.com): used to coordinate all course communication
- [GitHub](https://www.github.com): used to download code and data, collaborate with other students, and submit course assignments
- [Dartmouth JupyterHub Cluster](https://jupyter.dartmouth.edu/): a Dartmouth server we will use to write code, download data, run analyses, and submit assignments

If you are a Dartmouth student currently enrolled in PSYC 81.09, please follow *Setup Track 1, Part 1: Dartmouth students* below, followed by *Setup Track 2, Part 1: Everyone*.  If you are **not** currently enrolled in PYSC 81.09, please follow *Setup Track 2, Part 1: Everyone else* below, followed by *Setup Part 2: Everyone*.  In selecting the right track for you, you may find it useful to draw inspiration and/or guidance from the quotes below.

>     "There are Dartmouth students, and then there's everyone else..."
>        ~ Dartmouth Alum

>     "Know thyself" [paraphrasing]
>        ~ Pythagoras

## Setup Track 1, Part 1: Dartmouth students
1. You should start by signing up for the course's [Slack account](https://stories-about-data.slack.com) (you need to join using your @dartmouth.edu email address).  You can ask questions and get help with all aspects of the course via Slack.
2. Next, create a free [GitHub account](https://www.github.com) if you don't already have one.  (If you already have an account, you may use it for this course.)
3. Sign up for a [DartFS](https://rcweb.dartmouth.edu/accounts/) account.  This will give you access to the course fileserver.  You can access the fileserver from on campus, or from off campus using [Dartmouth's VPN](https://services.dartmouth.edu/TDClient/KB/ArticleDet?ID=66806).  You can also mount the fileserver on your computer using these instructions: [Mac](https://rc.dartmouth.edu/index.php/hrf_faq/how-to-access-dartfs-from-a-mac/), [PC](https://rc.dartmouth.edu/index.php/hrf_faq/how-to-access-dartfs-from-a-pc/).
4. Use your DartID to sign up for an account on our [JupyterHub cluster](https://jupyter.dartmouth.edu/).  You should sign in using the username `KIEWIT\<Your DartID>` (replacing `<Your DartID>` with your actual Dartmouth ID, using all lowercase letters).  You can use any password (choose something secure)-- you will use your password to log into your account for the duration of the course.  When you log in, perform the following sequence of steps to connect your JupyterHub account with DartFS:
  - Open a Terminal window (using the *New* menu from the Jupyter window)
  - Within the Terminal window that comes up, run the following command: `ln -s /dartfs/rc/lab/P/Psych81.09/  Psych81.09`
5.  Note: when any course instructions tell you to execute a Terminal command (e.g. `fixed width text`), clone something from GitHub, download something, submit an assignment, etc., you will do so from within this JupyterHub environment.
6. Proceed to *Setup Part 2: Everyone!*

## Setup Track 2, Part 1: Everyone else
1. We have created a [Docker](https://www.docker.com/) container to provide a reproducible computing environment with all of the course packages preinstalled.  Docker is a tool for packaging up everything programs need to run into isolated "containers" that can run on anybody's computer.  (You can always attempt to install packages that we use in the course via other means, but Docker is the only *supported* method.)  To get Docker set up on your machine, following [these instructions](https://github.com/ContextLab/storytelling-with-data/blob/master/docker/README.md).  If you are *not* a Dartmouth student enrolled in PSYC 81.09, I recommend that you use our Docker container to participate in this course.
2. When any course instructions tell you to execute a Terminal command (e.g. `fixed width text`), clone something from GitHub, download something, submit an assignment, etc., you will do so from within this Docker environment.
3. Proceed to *Setup Part 2: Everyone!*

## Setup Part 2: Everyone!
1. If you haven't used GitHub before, start by reading [this overview](https://guides.github.com/introduction/git-handbook/).  Next, check out [this tutorial](https://github.com/Summer-MIND/mind_2018/tree/master/tutorials/git_github) for a quickstart guide to the most important commands.  [These tutorials](https://help.github.com/en/articles/git-and-github-learning-resources) provide a more in-depth background for the interested learner.
2. Create a fork of this repository (if you're viewing this page on GitHub, press the `Fork` button in the upper right after logging into your GitHub account).
3. Clone your fork to your computing environment-- from within Terminal, run `git clone https://github.com/<GitHub username>/storytelling-with-data.git`, replacing `<GitHub username>` with your actual GitHub username.
4. Use a text editor to add your fork to the `add_remotes.sh` script by appending the following line:
```
git remote add <your first name> https://github.com/<GitHub username>/storytelling-with-data.git
```
5. Commit your change to your local fork (`git commit -a -m "added my fork to the add_remotes.sh script"`)
6. Run the `add_remotes.sh` script: `./add_remotes.sh`
7. Pull the changes from the upstream fork into your local fork: `git pull upstream master`
8. Merge any changes from the upstream fork into your local fork: `git commit -a -m "merging upstream changes into my fork"`
9. Push your changes to your local fork: `git push`.  Note for advanced users: if you've set up two-factor authentication, [here](https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line) is how you can get your push requests working (they will fail to authenticate unless you follow those instructions).  In summary, this entails:
  - Generating a [new token](https://github.com/settings/tokens)
  - Using the token in place of your actual GitHub password when it asks
  - Note: to store your credentials so that you don't have to keep typing your username and password, run `git config credential.helper store`, followed by `git pull` (or another operation that requires you to enter your username/password).  Your credentials should now be stored (and used when you make further commits, pull requests, push requests, etc.).
10. Submit a pull request to integrate your changes into the main course repository.  Navigate (using a web browser) to your repository's fork on GitHub (e.g. something like https://github.com/ContextLab/storytelling-with-data, but replacing "ContextLab" with your GitHub username) and click on the "Pull requests" button near the top.  Then click the green "New pull request" button, followed by the Green "Create pull request" button.  Add a title and comment to your pull request and then confirm it by pressing the new "Create pull request" button.

In the future, any time you want to incorporate changes from the main course repository into your local fork, you'll repeat steps 7 and 8 (prior to making any additional changes to your local fork in order to avoid merge conflicts).  Having run the `add_remotes.sh` script will also allow you to pull in changes from any other course participant's fork, which is useful for collaborative projects.  For example, `git pull jeremy master` will pull the latest changes from `jeremymanning`'s fork into your fork.  (Note: re-running the `add_remotes.sh` script is safe, but will display a `fatal: remote <name> already exists` message for any repositories that you have already tagged.)  Make sure to run the final version of the `add_remotes.sh` script after all students have added themselves to it.

# Course projects
This course is organized around a series of hackathon-style projects.  The central repository for all of these projects is the `data-stories` folder within this GitHub repository.

## Starting a new project
Each time you begin a new project, you should (in collaboration with your project team):
- If you haven't already done so, fork this repository and clone it to your computing environment (note: you already did this if you followed the setup instructions above)
- Come up with a creative, fun, yet descriptive, name for your project
- Group leader: create a new project sub-folder under [data-stories](https://github.com/ContextLab/storytelling-with-data/tree/master/data-stories) (note: do this *within your fork*)
- Follow the instructions [here](https://github.com/ContextLab/storytelling-with-data/tree/master/data-stories/README.md) to finish setting up your project.
- All team members: pull the group leader's changes into your local forks using `git pull <group leader's name> master`.
- Use the group leader's fork a a staging point for coordinating any project changes.  Each team member should pull their changes into the group leader's fork when they have something to share with the group.
- When the group is ready to share with the class, open a pull request into the ContextLab (upstream) fork.

## Contributing to an existing project
You can also (when the mood strikes) continue, or fork, *someone else's project* -- in the real world, this is called (amongst other things) "doing science."  Or, as Bernard of Chartres, and more recently Isaac Newton, described it, "standing on the shoulders of giants."  To stand on the shoulders of someone else's project, simply modify it on your local fork.  If you are working with a group, select one group member to serve as the "group leader" and pull each team member's changes into their fork.  When you are ready to share your changes with the class, pull the group's changes into the ContextLab (upstream) fork.  If you're feeling extra nice, it's never a bad idea to acknowledge the original project on which your work is based (e.g. in your project's readme file), and/or to give the original project's authors a heads up that you're about to change the world using something they started!

In the course of modifying an existing project, you may determine that your project has diverged sufficiently from the original that it now merits a new project name.  If so, create a new project folder (e.g. following the *Starting a new project* instructions above) and use `git mv` to migrate the relevant files to the new project's folder.

# Getting help
Data science is a tricky, rewarding, and often frustrating business.  Luckily for us data scientists, there are many places to get help!  Examples include:
- [Google](https://www.google.com)-- searchable portal to of all human knowledge. Most Internet things are reachable through here, and it's a great place to start your search.  You can often find code that other people have written that solves a similar problem to the one you're working on, or a tutorial that teaches you how to solve a particular class of problems.
- [Wikipedia](https://www.wikipedia.org/)-- community-curated encyclopedia. Wikipedia is a good resource for learning about the background of a technique, looking up equations, etc.  It's not a good source for tutorials.
- [Slack](https://stories-about-data.slack.com)-- course chatroom for Dartmouth students.  A good place for to ask questions, post ideas, etc., to other members of the class.
- The last (but hopefully not least) option if you're feeling stuck, unhappy with how things are progressing, looking for fun new ideas to revitalize your project and get you interested in science again, etc. is to *come talk with me*.  If you're a Dartmouth person you can come to my regular office hours, [email me](mailto:jeremy@dartmouth.edu), message me on Slack, or come visit [my lab](http://www.context-lab.com/).
- **Important**-- chances are good that if you're feeling lost, you're not the only one!  If you learn something useful, please share it via Slack or by opening a [GitHub issue](https://github.com/ContextLab/storytelling-with-data/issues).

# Tutorials
If you're new to computer programming, Python, or Jupyter notebooks, you'll want to run through some tutorials to help you get started.  We'll go over the very high-level ideas in class, and you can always ask questions in class or via Slack, but you will likely need to go through these tutorials on your own time to fully experience the delicious learning benefits encapsulated within.

- Quickstart guide to [Python with Jupyter Notebooks](https://gitlab.erc.monash.edu.au/andrease/Python4Maths/tree/master/Intro-to-Python) (über beginner)

- Introduction to [Python](https://www.codecademy.com/learn/learn-python) (beginner)
- Introduction to [Git](https://www.codecademy.com/learn/learn-git) (beginner)
- Video introduction to [Jupyter Notebooks](https://youtu.be/CSkTJRNBTME) (with [code](https://github.com/dartmouth-brainhack-2017/IntroToJupyter/tree/9a2cca0a88b837745430b234a3002ba6165ed6ce)) (beginner)
- Learning to code with [Python *and* Jupyter Notebooks](http://introtopython.org/) (beginner)

Once you have the basics down, you can move on to learn about some very useful Python packages:

- Introduction to [Pandas](https://pandas.pydata.org/pandas-docs/stable/10min.html) (intermediate)
- Practice your Pandas [skills](https://github.com/guipsamora/pandas_exercises) (intermediate)
- Getting started with [Numpy](https://docs.scipy.org/doc/numpy-dev/user/quickstart.html) (intermediate)
- Getting started with [Scipy](https://docs.scipy.org/doc/scipy/reference/tutorial/index.html) (intermediate)
- Exploring high dimensional data with [HyperTools](http://blog.kaggle.com/2017/04/10/exploring-the-structure-of-high-dimensional-data-with-hypertools-in-kaggle-kernels/) (intermediate)

Another really useful technique for doing reproducible open science in the real world is to develop [unit tests](http://docs.python-guide.org/en/latest/writing/tests/).  I suggest using [Travis CI](https://docs.travis-ci.com/) to automatically run your unit tests when you check in new code:
- Testing applications with [Pytest](https://semaphoreci.com/community/tutorials/testing-python-applications-with-pytest) (advanced)
- Setting up [Travis CI](https://docs.travis-ci.com/user/for-beginners) (advanced)

My lab also maintains a public repository of tutorials on a variety of topics [here](https://github.com/ContextLab/CDL-tutorials).

# Where to find nice datasets

In todays "Big Data" world, there are an abundance of high-quality, free datasets to enjoy and explore.  Below is a short list of websites that are great resources for data:

- [Kaggle](https://www.kaggle.com/datasets)
- [FiveThirtyEight](https://github.com/fivethirtyeight/data)
- [Awesome Public Datasets](https://github.com/caesar0301/awesome-public-datasets)
- [Datalad](http://datasets.datalad.org/)
- [Princeton Neuroscience Institute](http://dataspace.princeton.edu/jspui/handle/88435/dsp0147429c369)
