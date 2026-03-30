# General Data Story Instructions

## Overview

In Part II of the course (weeks 5–10), you will apply the tools and
skills you learned in Part I to create your own data stories. You'll
cycle through three stages repeatedly:

1. **Pitching and brainstorming.** Present your ideas to classmates,
   form groups, and workshop story ideas.
2. **Refinement.** Workshop your ideas and code. Bring up new content,
   tools, or techniques you'd like to learn more about.
3. **Critiquing.** As a class, we'll discuss your story and provide
   constructive feedback. We'll also go through your code and discuss
   relevant coding issues (challenges, clever hacks, etc.).

You should plan to make it through this cycle **at least three times**
during Part II — that is, you should produce at least **3 data stories**.

## What is a Data Story?

A data story is a short (5-minute) presentation that uses data to tell
a compelling narrative. It combines:

- A **question** you want to answer or explore
- **Data** that helps you investigate that question
- **Analysis** and **visualizations** that reveal patterns and insights
- A **narrative** that ties it all together for your audience

You can work **individually or in groups** of any size. Projects and
groups should form organically and remain flexible.

## Deliverables

Each data story should be contained in a single sub-folder of
[data-stories](https://github.com/ContextLab/storytelling-with-data/tree/master/data-stories).
Your project should include the following files, based on the
[project template](https://github.com/ContextLab/storytelling-with-data/tree/master/data-stories/demo):

### 1. README.md

Based on the
[README template](https://github.com/ContextLab/storytelling-with-data/blob/master/data-stories/demo/README.md),
your README should contain:

- **Project information**: project name, authors, GitHub usernames
- **Overview**: main question, approach, data used, tools used, key findings
- **YouTube link**: a link to your 5-minute data story video
- **Data links**: where to find the data you analyzed
- **Running the code**: instructions for replicating your results
- **Contributing**: next steps, open questions, known issues
- **Acknowledgements and citations**

### 2. YouTube Video (5 minutes)

A video presentation of your data story. You can:

- Narrate over a screencast of your notebook
- Create slides (using Marp, PowerPoint, Keynote, etc.)
- Use any other creative format you like

The key is to **tell a compelling story** backed by data, not just
walk through code.

### 3. Code

Your project's code (Jupyter notebooks, Python scripts, etc.), based on
the [notebook template](https://github.com/ContextLab/storytelling-with-data/blob/master/data-stories/demo/demo.ipynb).
Your code should be well-documented and reproducible.

### 4. Data

- If your data files are **under 10 MB total**, include them directly
  in your project folder.
- If larger, host them on Google Drive, Dropbox, or another accessible
  cloud source.
- **Either way**, your notebook must include code for downloading and
  importing the data so anyone can reproduce your results.

## Weekly Rhythm

| Day | Activity |
|-|-|
| **Monday** | Review and discuss data stories from the previous week |
| **Wednesday** | New tools, demos, and techniques |
| **Thursday (X-hour)** | Office hours or hackathon/demos |
| **Friday** | Hackathon + brainstorming for next week's stories |

## Tips for Great Data Stories

- **Start with a question**, not a dataset. What do you want to know?
- **Keep it focused.** A 5-minute story should make one or two clear
  points, not try to cover everything.
- **Show, don't tell.** Let your visualizations carry the narrative.
- **Iterate.** Your first attempt won't be perfect — use feedback from
  classmates to improve.
- **Be creative.** The best stories surprise the audience or change how
  they think about something.
- **Collaborate.** Build off each others' code, questions, and ideas.
  Interdisciplinary teams often produce the most interesting work.

## Finding Data

Need inspiration? Here are some places to find interesting datasets:

- [Kaggle Datasets](https://www.kaggle.com/datasets)
- [FiveThirtyEight Data](https://github.com/fivethirtyeight/data)
- [Awesome Public Datasets](https://github.com/caesar0301/awesome-public-datasets)
- [World Bank Open Data](https://data.worldbank.org/)
- [World Health Organization](https://apps.who.int/gho/data/node.home)
- [Registry of Open Data on AWS](https://registry.opendata.aws/)
- [Reddit: r/datasets](https://www.reddit.com/r/datasets/)
- [Google Dataset Search](https://datasetsearch.research.google.com/)

## Evaluation

Each data story will be evaluated on:

| Criterion | What we're looking for |
|-|-|
| **Question** | Is the question interesting and well-defined? |
| **Data** | Is the data appropriate for the question? |
| **Analysis** | Is the analysis sound and well-executed? |
| **Visualization** | Do the figures effectively communicate insights? |
| **Narrative** | Does the story flow logically and engage the audience? |
| **Code quality** | Is the code clean, documented, and reproducible? |
| **Feedback** | Did you incorporate feedback from previous iterations? |

## Submitting Your Story

1. Create a folder in `data-stories/` named descriptively (e.g.,
   `data-stories/climate-trends/`)
2. Include your README.md, notebook(s), and data files
3. Upload your video to YouTube (unlisted is fine)
4. Submit a pull request to the course repository
