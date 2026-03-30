---
marp: true
theme: cdl-theme
math: katex
---

# The Python Data Science Stack
## Demo
### PSYC 81.09: Storytelling with Data

---

## Today's agenda

<div class="note-box" data-title="What we're covering today">

- A quick tour of the **Python data science stack** — what each tool does and when to use it
- **Live demos** using vibe coding — we'll build real analyses with AI assistance
- Focus on *understanding*, not memorizing syntax

</div>

---

## The Python ecosystem

<div class="definition-box" data-title="Python + libraries = a data science toolkit">

Python on its own is a general-purpose language. Its power for data science comes from **libraries** — pre-built packages that handle specific tasks:

| Library | Purpose |
|-|-|
| **NumPy** | Numerical arrays and fast math |
| **Pandas** | Tabular data (rows and columns) |
| **Matplotlib** | Flexible plotting |
| **Seaborn** | Beautiful statistical plots |
| **Hypertools** | High-dimensional data visualization |

Think of these as specialized tools in a toolbox — each one is designed for a particular job.

</div>

---

## NumPy: crunching numbers

<div class="note-box" data-title="When you need to crunch numbers, reach for NumPy">

**NumPy** provides:
- **Arrays** — efficient containers for numerical data (faster than Python lists)
- **Vectorized operations** — apply math to entire arrays at once, no loops needed
- **Linear algebra, statistics, random numbers** — the mathematical foundation for everything else

Almost every other data science library in Python is built *on top of* NumPy.

</div>

---

## Pandas: working with tables

<div class="note-box" data-title="When you have data in rows and columns, reach for Pandas">

**Pandas** provides:
- **DataFrames** — like spreadsheets in Python
- **Loading data** — read CSVs, Excel files, JSON, databases, and more
- **Filtering and selecting** — grab exactly the rows and columns you need
- **Grouping and aggregating** — compute summaries by category
- **Merging** — combine multiple datasets together

If your data looks like a table, Pandas is your tool.

</div>

---

## Matplotlib & Seaborn: seeing your data

<div class="note-box" data-title="When you want to see your data, reach for these">

**Matplotlib** is the foundation — it can create virtually any plot, but requires more manual setup.

**Seaborn** builds on Matplotlib with:
- Beautiful default styles
- Statistical plot types (violin plots, pair plots, heatmaps)
- Tight integration with Pandas DataFrames

**Rule of thumb:** Start with Seaborn for common plots. Drop down to Matplotlib when you need full control.

</div>

---

## Hypertools: visualizing high-dimensional data

<div class="note-box" data-title="When your data has many dimensions, reach for Hypertools">

Real-world datasets often have dozens or hundreds of features. **Hypertools** makes it easy to:

- **Reduce dimensions** — project high-dimensional data into 2D or 3D for visualization
- **Align datasets** — compare data from different sources on a common coordinate system
- **Explore structure** — discover clusters, trajectories, and patterns

It wraps complex dimensionality reduction algorithms in a simple interface.

</div>

---

## Demo 1: vibe coding a data analysis

<div class="example-box" data-title="Let's build an analysis with AI">

**The workflow:**
1. **Describe the goal** — "Load this dataset, clean it, and give me a summary of the key variables"
2. **AI generates code** — Claude Code produces a working script
3. **We review and explain** — walk through each step together

Let's try it live. We'll use a real dataset and see what the AI produces.

</div>

---

## Demo 1 continued: the generated code

<div class="example-box" data-title="Walking through what the AI produced">

A typical AI-generated analysis might include:

- `import pandas as pd` — load the Pandas library
- `df = pd.read_csv('data.csv')` — read the data into a DataFrame
- `df.describe()` — summary statistics for every numeric column
- `df.dropna()` — handle missing values
- `df.groupby('category').mean()` — average values by group

Each line has a clear purpose. The AI wrote the syntax — our job is to understand the logic.

</div>

---

## Verify and explain

<div class="warning-box" data-title="Pause and check your understanding">

Before moving on, ask yourself:

- **What does each line do?** Can you explain it in plain English?
- **What would happen if the data had missing values?** Would the code handle that correctly?
- **Are the results reasonable?** Do the numbers make sense given what you know about the data?

AI-generated code is a *starting point*, not a finished product. Verification is your responsibility.

</div>

---

## Demo 2: vibe coding a visualization

<div class="example-box" data-title="Let's create a publication-quality figure">

**The prompt:** "Create a clear, informative visualization that shows the relationship between these two variables, with a trend line and labeled axes."

**The workflow:**
1. Describe what we want to see
2. AI generates the plot code
3. We run it and evaluate the result
4. We iterate until it tells the right story

</div>

---

## Demo 2 continued: iteration

<div class="tip-box" data-title="Iteration is the workflow">

The first attempt is rarely perfect. After seeing the initial plot, we asked for:

- A **colorblind-friendly palette** — accessibility matters
- **Larger axis labels** — readability at presentation scale
- A **descriptive title** — the figure should stand on its own

Each request is a short, natural-language instruction. The AI adjusts the code; we evaluate the result. This back-and-forth *is* vibe coding.

</div>

---

## Verify and explain

<div class="warning-box" data-title="Think critically about the visualization">

Before accepting a figure, ask:

- **What type of plot did the AI choose?** Is it appropriate for this data?
- **Why this plot type?** Would a different choice tell a different story?
- **What story does this visualization tell?** Could it be misleading?
- **What's missing?** Are there important caveats or context not shown?

The ability to evaluate a visualization is more important than the ability to code one.

</div>

---

## Want to go deeper?

<div class="note-box" data-title="Detailed reference decks for self-study">

Today's demo gave you the big picture. For deeper dives, see these decks (all available in the course repository):

- **Modules and NumPy** — arrays, vectorized operations, and numerical computing in detail
- **Pandas** — DataFrames, filtering, grouping, merging, and reshaping
- **Data Visualization** — plot types, design principles, and storytelling with figures
- **Vibe Coding Demos** — extended walkthroughs of AI-assisted coding workflows

Use these as references when you're working on your own analyses.

</div>

---

## Summary

<div class="definition-box" data-title="What to take away">

You don't need to memorize syntax — AI handles that. You need to know **what** these tools do and **when** to use them:

| Tool | Reach for it when... |
|-|-|
| **NumPy** | You need to crunch **numbers** |
| **Pandas** | You have data in **tables** |
| **Matplotlib / Seaborn** | You want to **see** your data |
| **Hypertools** | Your data has **many dimensions** |

Your job: **direct**, **verify**, and **explain**. The AI's job: write the code.

</div>

---

# Questions? Want to chat more?

<div class="emoji-figure">
  <div class="emoji-col">
    <span class="emoji emoji-xl emoji-bg emoji-bg-navy">&#x1F4E7;</span>
    <span class="label"><a href="mailto:jeremy@dartmouth.edu">Email</a> me</span>
  </div>
  <div class="emoji-col">
    <span class="emoji emoji-xl emoji-bg emoji-bg-purple">&#x1F4AC;</span>
    <span class="label">Join our <a href="https://stories-about-data.slack.com">Slack</a></span>
  </div>
  <div class="emoji-col">
    <span class="emoji emoji-xl emoji-bg emoji-bg-green">&#x1F481;</span>
    <span class="label">Come to <a href="https://context-lab.com/scheduler">office hours</a></span>
  </div>
</div>

<div class="note-box" data-title="Up next...">

- **Friday:** Hackathon + brainstorming + Assignment 4 release

</div>
