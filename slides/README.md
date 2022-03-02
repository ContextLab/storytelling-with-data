# Course outline

PSYC 81.09 (Storytelling with Data) is organized into 2 main parts.  [Part I](https://github.com/ContextLab/storytelling-with-data/blob/master/slides/README.md#part-i) comprises four modules, and is collectively aimed at introducing students to the process of creating "data stories" using Python data science tools:
- [Module 1: What makes a good story?](https://github.com/ContextLab/storytelling-with-data/blob/master/slides/README.md#module-1-what-makes-a-good-story)
- [Module 2: Visualizing data](https://github.com/ContextLab/storytelling-with-data/blob/master/slides/README.md#module-2-visualizing-data)
- [Module 3: Python and Jupyter notebooks as a medium for data storytelling](https://github.com/ContextLab/storytelling-with-data/blob/master/slides/README.md#module-3-python-and-jupyter-notebooks-as-a-medium-for-data-storytelling)
- [Module 4: Data science tools](https://github.com/ContextLab/storytelling-with-data/blob/master/slides/README.md#module-4-data-science-tools)

[Part II](https://github.com/ContextLab/storytelling-with-data/blob/master/slides/README.md#part-ii) is project-based, and revolves around mini data science projects.  For each project, one or more students choose a question and dataset to explore and turn into a data story.  Each week students and groups will report on their progress with the latest iterations of their stories.  Students should aim to participate in three or more projects during Part II of the course.  At students' discretion, those three (or more) projects may comprise the same questions and/or datasets (e.g., whereby each story builds on the previous story), or multiple questions and/or datasets that may or may not be related.  In addition, students are encouraged to build off of each others' code, projects, and questions.  Projects and project groups should form organically and should remain flexible to facilitate changing goals and interests.

Lecture recordings are denoted in **bolded** links below.  (Inactive links denote
  lectures that have not happened yet.)

## Introduction
- [Welcome message](https://www.youtube.com/watch?v=LvFQLLTu5KY)
  - [Supplemental welcome message](https://youtu.be/JwA6zyWdNIs)
- Learning remotely: [tools](https://youtu.be/uxqZ-Xdra0I), [tips](https://youtu.be/RzCXL8p5VAU), and [tricks](https://youtu.be/5OmFGIYy1kM) for engaging with online aspects of the course.
- [Course syllabus](https://github.com/ContextLab/storytelling-with-data/blob/master/admin/PSYC_81_syllabus.pdf)
- [**Discussion: the pursuit of truth**](https://youtu.be/X0P9GHjmmBE)

---

# Part I

## Module 1: What makes a good story?
- [Introduction to storytelling](https://www.khanacademy.org/partner-content/pixar/storytelling/we-are-all-storytellers/v/storytelling-introb) (Source: [Khan Academy's The art of storytelling](https://www.khanacademy.org/partner-content/pixar/storytelling))
- [What makes a great story?](https://www.khanacademy.org/partner-content/pixar/storytelling/we-are-all-storytellers/v/video2-stories) (Source: [Khan Academy's The art of storytelling](https://www.khanacademy.org/partner-content/pixar/storytelling))
- Exercise: [Telling a story about a vivid memory](https://www.khanacademy.org/partner-content/pixar/storytelling/we-are-all-storytellers/a/activity-1) (Source: [Khan Academy's The art of storytelling](https://www.khanacademy.org/partner-content/pixar/storytelling))
- [Structuring stories to make them effective communication tools](https://www.khanacademy.org/partner-content/pixar/storytelling/story-structure/v/piab-storystructure) (Source: [Khan Academy's The art of storytelling](https://www.khanacademy.org/partner-content/pixar/storytelling))
- [Using pictures to tell a story](https://www.khanacademy.org/partner-content/pixar/storytelling/visual-language/v/visual-language) (Source: [Khan Academy's The art of storytelling](https://www.khanacademy.org/partner-content/pixar/storytelling))
- [Pitching your story (or idea!)](https://www.khanacademy.org/partner-content/pixar/storytelling/storyboard-your-film/v/pitching1) (Source: [Khan Academy's The art of storytelling](https://www.khanacademy.org/partner-content/pixar/storytelling))
- [Giving constructive feedback](https://www.khanacademy.org/partner-content/pixar/storytelling/storyboard-your-film/v/pitching2) (Source: [Khan Academy's The art of storytelling](https://www.khanacademy.org/partner-content/pixar/storytelling))
- [Using feedback to improve your story](https://www.khanacademy.org/partner-content/pixar/storytelling/storyboard-your-film/v/pitching3) (Source: [Khan Academy's The art of storytelling](https://www.khanacademy.org/partner-content/pixar/storytelling))
- [Assignment 1: tell the class a 5-minute story](https://github.com/ContextLab/storytelling-with-data/blob/master/assignments/assignment%201/Assignment_1.md)  You may find some inspiration by taking a look at some [Moth Radio Hour stories](https://themoth.org/radio-hour).
  - [**Workshopping story ideas**](https://youtu.be/neSuDd6s3Kc)
  - [**Discussions about stories (part 1)**](https://youtu.be/hopzOYrLTTc)
  - [**Discussions about stories (part 2)**](https://youtu.be/58rs4Yy-c9Y)
    - Submissions for Spring, 2020: [[link](https://www.youtube.com/playlist?list=PLjQYT8Fwp985vuGsFBKkJlOv5L8H4igar)]
    - Submissions for Spring, 2021: [[link](https://www.youtube.com/playlist?list=PLjQYT8Fwp985vbr6g0_ATi5tkh7XtUPVQ)]
    - Submissions for Winter, 2022: [[link](https://youtube.com/playlist?list=PLjQYT8Fwp987zYZpfHblo0UwyBp407Nq6)]

## Module 2: Visualizing data
- [Introduction to representing data](https://www.khanacademy.org/math/pre-algebra/pre-algebra-math-reasoning/pre-algebra-representing-data/v/ways-to-represent-data) (Source: [Khan Academy's Representing Data course](https://www.khanacademy.org/math/pre-algebra/pre-algebra-math-reasoning#pre-algebra-representing-data))
- [Designing effective scientific figures](https://www.dropbox.com/s/qdiqqt3a8i632hn/DesigningEffectiveScientificFigures_Zabala_afternoon_v00.pdf) (Source: [Aiora Zabala](https://bioinformatics-core-shared-training.github.io/effective-figure-design/DesigningEffectiveScientificFigures_Zabala_afternoon_v00.pdf))
- [Maximizing the data-to-ink ratio](https://medium.com/plotly/maximizing-the-data-ink-ratio-in-dashboards-and-slide-deck-7887f7c1fab) (Source: [medium.com](https://medium.com/))
- Take a look at [A Layered Grammar of Graphics](https://www.dropbox.com/s/xhpjth2f4aamn5u/layered-grammar.pdf) by Hadley Wickham (skim or skip the code examples) and [The Grammar of Graphics](https://www.dropbox.com/s/4qwd16psogqdgi6/Wilk10.pdf) by Leland Wilkinson.
- [**Discussion: telling effective stories about data**](https://youtu.be/TbrNyfw9voU)
- [Assignment 2: data story remix](https://github.com/ContextLab/storytelling-with-data/blob/master/assignments/assignment%202/Assignment_2.md)  You find some inspiration by taking a look at one or more of the following sources of data stories:
  - [FiveThirtyEight.com](https://fivethirtyeight.com/)
  - [Reddit: DataIsBeautiful](https://www.reddit.com/r/dataisbeautiful/)
  - [Towards Data Science](https://towardsdatascience.com/)
  - [Minute Physics](https://www.youtube.com/user/minutephysics)
  - [Kaggle Blog](https://medium.com/kaggle-blog)
  - [IQuantNY](https://iquantny.tumblr.com/)
  - [New York Times: Science](https://www.nytimes.com/section/science)
  - [Washington Post: Visual Stories](https://www.washingtonpost.com/)
  - [Distill.pub](https://distill.pub/archive/)
- [**Workshopping data story ideas**](https://youtu.be/o-FO7pulALM)
- [**Discussions about data stories (part 1)**](https://youtu.be/RowGoMEwBoQ)
- [**Discussions about data stories (part 2)**](https://youtu.be/ygRP2rFwJjY)
  - Submissions for Spring, 2020: [[link](https://www.youtube.com/playlist?list=PLjQYT8Fwp98490cWdyQaIOaMcGF8tXM-Y)]
  - Submissions for Spring, 2021: [[link](https://youtube.com/playlist?list=PLjQYT8Fwp984OgKhTwslvZ6RHIt1mXMeB)]
  - Submissions for Winter, 2022: [[link](https://www.youtube.com/playlist?list=PLjQYT8Fwp984bcI29bbv9-mLSbKbx5RFW)]

## Module 3: Python and Jupyter notebooks as a medium for data storytelling
- Discussion: Introduction to programming
  - [**Discussion: intro to programming**](https://youtu.be/g92mLcBc_gI)
- [Getting set up on Google Colaboratory](https://colab.research.google.com/github/ContextLab/cs-for-psych/blob/master/slides/module_1/introduction_and_overview.ipynb) (Source: [Introduction to Programming for Psychological Scientists](https://github.com/ContextLab/cs-for-psych/tree/master/slides))
- [Project management and version control with git and GitHub](https://www.youtube.com/playlist?list=PLjQYT8Fwp984zMjN5rJChfdI5Z8jtaWww):
  - [Overview of Git and GitHub](https://www.youtube.com/watch?v=4Fsg4UPHsrM)
  - [Git basics part 1: fork, clone, and status](https://www.youtube.com/watch?v=4aMftm6V_lY)
  - [Git basics part 2: add, rm, mv, commit, push, and pull](https://www.youtube.com/watch?v=j1EuezxSqsY)
  - [Intermediate git: ignore, revert, checkout, branch, merge, and remote](https://www.youtube.com/watch?v=PlqGgzpw1c0)
  - [Handling git merge conflicts](https://youtu.be/N9_OP6gwgjU)
  - [GitHub project management tools](https://youtu.be/9SIqCrj_vyQ)
  - Optional (ungraded) assignment: [GitHub Fundamentals](https://github.com/ContextLab/github-starter-course) [[Accept assignment](https://classroom.github.com/a/--OlsCRh)]
- [Introduction to using the command line](https://www.codecademy.com/learn/learn-the-command-line) (Source: [codecademy](https://www.codecademy.com/))
- [High-level introduction to Python](https://github.com/ContextLab/storytelling-with-data/blob/master/slides/intro_to_python.ipynb)
- Resources for learning Python:
  - [Introduction to Programming for Psychological Scientists](https://github.com/ContextLab/cs-for-psych/tree/master/slides)
  - [Codecademy's Introduction to Python](https://www.codecademy.com/learn/learn-python) (Source: [codecademy](https://www.codecademy.com/))
  - [Learning to code with Python and Jupyter Notebooks](http://introtopython.org/) (Source: [introtopython.org](http://introtopython.org/))
  - [DataCamp](https://www.datacamp.com) has generously donated free access to all course materials for Dartmouth students enrolled in Storytelling with Data.  I have pinned an invite link to the `#general` channel in Slack.
- [Assignment 3: Binary converter](https://github.com/ContextLab/storytelling-with-data-binary-converter) [[Accept assignment](https://classroom.github.com/a/6eTaFkVe)]
- [**Python continued: list comprehensions and decorators**](https://youtu.be/QcwJtVtmxz0)
- [**Assignment 3 Q&A, introduction to Python modules, preview of Python data science stack**](https://youtu.be/WY_mOznaQyA) [[slides](https://github.com/ContextLab/storytelling-with-data/blob/master/slides/modules_and_numpy.md)]

## Module 4: Data science tools
- [Modules and Packages](https://jakevdp.github.io/WhirlwindTourOfPython/13-modules-and-packages.html) (from [Whirlwind Tour of Python](https://jakevdp.github.io/WhirlwindTourOfPython/index.html) by Jake VanderPlas)
- [Numpy](https://jakevdp.github.io/PythonDataScienceHandbook/02.00-introduction-to-numpy.html) and [Pandas](https://jakevdp.github.io/PythonDataScienceHandbook/03.00-introduction-to-pandas.html) (from [Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/index.html) by Jake VanderPlas)
  - [**Introduction to NumPy**](https://youtu.be/d82FIOduvik) [[slides](https://github.com/ContextLab/storytelling-with-data/blob/master/slides/modules_and_numpy.md)]
  - [**Introduction to Pandas**](https://youtu.be/Ly6ZweQ5bJs) [[slides](https://github.com/ContextLab/storytelling-with-data/blob/master/slides/pandas.md)]
  - (Optional) practice problems for [NumPy](https://github.com/rougier/numpy-100) and [Pandas](https://github.com/ajcr/100-pandas-puzzles)
- [Data visualization overview](https://github.com/ContextLab/cs-for-psych/blob/master/slides/module_4/data_visualization.ipynb)
- More details on plotting libraries: [Matplotlib](https://jakevdp.github.io/PythonDataScienceHandbook/04.00-introduction-to-matplotlib.html) and [Seaborn](https://jakevdp.github.io/PythonDataScienceHandbook/04.14-visualization-with-seaborn.html) (from [Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/index.html) by Jake VanderPlas)
- [Grammar of graphics in Python](https://towardsdatascience.com/how-to-use-ggplot2-in-python-74ab8adec129) (Source: [towardsdatascience.com](https://towardsdatascience.com/))
- [Visualizing high-dimensional data with Hypertools](https://hypertools.readthedocs.io/en/latest/tutorials.html) (Source: [hypertools.readthedocs.io](https://hypertools.readthedocs.io/))
- Interactive lecture: exploring and visualizing a sample dataset [[notebook](https://github.com/ContextLab/storytelling-with-data/blob/master/slides/data_visualization_playground.ipynb)]
  - [**Part I: data wrangling**](https://youtu.be/UPNTM_eakg8)
  - [**Part II: data wrangling continued, basic plotting**](https://youtu.be/aN5PrEeiWbY)
- [Assignment 4: tell your first (notebook-based) data story!](https://github.com/ContextLab/storytelling-with-data/blob/master/assignments/assignment%204/Assignment_4.md)
  - [**Discussion with Vermont Department of Health**](https://youtu.be/3kUGSReTXA0) [[slides](https://github.com/ContextLab/storytelling-with-data/raw/master/assignments/assignment%204/VT_DOH_slides.pptx)]
  - [**Story ideas workshop and brainstorm**](https://youtu.be/WzCBWl4VRew)
  - [**Debugging session (Part I)**](https://youtu.be/Rdxtqvo1bQs)
  - [**Debugging session (Part II)**](https://youtu.be/EPSlVDlXDK8)
  - [**Debugging session (Part III)**](https://youtu.be/IuRmj1d-n7g)
  - [**Story critiques**](https://youtu.be/ig0dUWWxAYY)
    - Submissions for Spring, 2020: [[link](https://youtube.com/playlist?list=PLjQYT8Fwp987s_ajlAjwijpE4NvWGBUDo)]
    - Submissions for Spring, 2021: [[link](https://youtube.com/playlist?list=PLjQYT8Fwp987pUS5Ol-A5QIIfjZ7yFBLD)]
    - Submissions for Winter, 2022: [[link](https://youtube.com/playlist?list=PLjQYT8Fwp9872PMrg45QvnpNnB9Zb4QVZ)]
---

# Part II

We will spend Part II of the course repeating three general steps in the storytelling process (a video introduction to Part II may be found [here](https://youtu.be/WxW-6dsPxB0)):
1. **Pitching and brainstorming.**  You'll present your ideas to your classmates, form groups, workshop story ideas.
    - Brainstorm session
2. **Refinement.** We'll workshop your (and your group's) ideas and code.  You can also use this time to bring up new content ideas that you'd like to learn more about.
3. **Critiquing.** As a class we will discuss your story and provide constructive feedback.  We'll also go through your code and discuss any relevant coding issues (e.g., challenges, clever hacks, etc.) that might be relevant to the class.

You should plan to make it through this cycle at least three times during Part II of the course (i.e., you should produce at least 3 data stories).

Each data story should be contained in a single sub-folder of [data-stories](https://github.com/ContextLab/storytelling-with-data/tree/master/data-stories).  Your project should comprise the following files, based on [this project template](https://github.com/ContextLab/storytelling-with-data/blob/master/data-stories/demo/):
- A README.md markdown file based on [this template](https://github.com/ContextLab/storytelling-with-data/blob/master/data-stories/demo/README.md).  The README file should contain:
  - A project description and overview.
  - A link to a YouTube video of your (5 minute) data story.  (A playlist containing the current set of data stories may be found [here](https://www.youtube.com/playlist?list=PLjQYT8Fwp987s_ajlAjwijpE4NvWGBUDo).)
  - Links to the data you analyzed.
  - Instructions for replicating your results.
  - A description of how someone could contribute to your project.
  - Acknowledgements and citations.
- Your data story (hosted on YouTube and cited in your README file).  Note: you don't need to upload the source video, but if you use any images or slides you should include them in a sub-folder.
- Your project's code (e.g., notebooks, Python scripts, etc.), based on [this template](https://github.com/ContextLab/storytelling-with-data/blob/master/data-stories/demo/demo.ipynb).
- If under 10 MB (total), you can include your data files directly in your project folder.  Otherwise you should host it on Google Drive, Dropbox, or some other cloud-based source accessible to all (current and future) students.  Regardless of how your project's data files are hosted, your notebook should include code for downloading and importing the data (so from a user's perspective it shouldn't matter where the data files are hosted).

## Part II Lecture recordings:
  - Brainstorming, pitch sessions, debugging, and story critiques:
    - [**Part a**](https://youtu.be/9xg1WAb8g5g)
    - [**Part b**](https://youtu.be/u3B65-6Nfr0)
    - **Part c**
    - **Part d**
    - **Part e**
