---
marp: true
theme: cdl-theme
math: katex
transition: fade 0.25s
author: Contextual Dynamics Lab
---

# Introduction to Pandas
## Jeremy R. Manning
### PSYC 81.09: Storytelling with Data

---

### Our philosophy

<div class="important-box" data-title="Tools, Not Syntax">

We focus on understanding **what** tools do and **when** to use them — not memorizing syntax. AI handles the syntax; you handle the thinking.

</div>

This lecture introduces **Pandas**, the core Python library for working with tabular data. You will learn what it is, when to reach for it, and how to use vibe coding to get things done.

---

### Python data science computing stack

![height:500px](figs/python_libraries.png)

---

### What is Pandas?

<div class="definition-box" data-title="Pandas in a Nutshell">

**Pandas** is Python's toolkit for working with structured, tabular data — the kind of data you encounter in spreadsheets, CSV files, and databases.

It provides two core data structures:
- **Series** — a labeled one-dimensional array (like a single column)
- **DataFrame** — a labeled two-dimensional table (rows and columns)

</div>

---

### Pandas = NumPy + :star2:

<div class="note-box" data-title="What Pandas Adds to NumPy">

- NumPy gives you fast numerical arrays
- Pandas wraps those arrays with **labeled rows and columns**, so you can refer to data by name instead of position
- Pandas also adds built-in support for **reading/writing common file formats** (CSV, Excel, JSON, SQL, and more)
- It includes functions for **grouping, merging, reshaping, and summarizing** data

</div>

Think of it this way: NumPy is the engine, Pandas is the dashboard.

---

### When to reach for Pandas

<div class="note-box" data-title="Use Pandas When...">

Reach for Pandas whenever your data has **rows and columns**:
- CSV or Excel files
- SQL query results
- Survey responses, experimental logs, behavioral data
- Anything you would open in a spreadsheet

If your data is a plain grid of numbers (e.g., a matrix of pixel values), NumPy alone may be enough. If it has **labels, mixed types, or missing values**, Pandas is the right tool.

</div>

---

### The vibe coding workflow

<div class="tip-box" data-title="How We Work With Pandas">

Instead of memorizing API details, we use a three-step workflow:

1. **Describe** your goal in plain language
2. **Generate** code with an AI assistant (e.g., Claude Code)
3. **Verify and explain** — read the code, make sure it does what you intended, and explain it in your own words

</div>

This is how professional data scientists increasingly work. The skill is in knowing what to ask for and whether the result is correct.

---

<!-- _class: scale-90 -->

### Vibe coding demo: loading and exploring data

Suppose you have a CSV of automobile data and you want to explore it. You might prompt:

> *"Load the CSV from this URL into a Pandas DataFrame. Show the first few rows and a statistical summary of the numeric columns."*

The generated code might look like:

```python
import pandas as pd

cars = pd.read_csv('https://tinyurl.com/ydevw29o')
print(cars.head())
print(cars.describe())
```

The key question is not "did I write this?" but "do I understand what it does?"

---

### Vibe coding demo: filtering and grouping

Next, you might ask:

> *"Group the cars by number of cylinders and compute the average miles per gallon for each group. Sort the result from highest to lowest mpg."*

Generated code:

```python
avg_mpg = cars.groupby('cylinders')['mpg'].mean().sort_values(ascending=False)
print(avg_mpg)
```

One line — but it chains several Pandas operations. Can you explain each step?

---

### Vibe coding demo: creating new columns

> *"Add a column called 'efficiency' that categorizes each car as 'high' if mpg > 30, 'medium' if between 20 and 30, and 'low' otherwise."*

Generated code:

```python
import numpy as np

cars['efficiency'] = np.select(
    [cars['mpg'] > 30, cars['mpg'] >= 20],
    ['high', 'medium'],
    default='low'
)
```

Notice how the AI reached for `np.select` — a NumPy function that works seamlessly with Pandas columns. Understanding the ecosystem matters.

---

<div class="warning-box" data-title="Verify and Explain">

**Before moving on**: read the generated code and explain in your own words what each section does and why.

- What does `groupby` actually do to the data?
- Why does `sort_values` take `ascending=False`?
- What happens if a column has missing values?

If you cannot explain the code, you do not yet understand it. Ask the AI to break it down step by step, or try modifying the code and observing what changes.

</div>

---

<!-- _class: scale-90 -->

### The Pandas toolkit at a glance

<div style="display: flex; gap: 2em;">
<div>

<div class="note-box" data-title="Loading &amp; Saving">

- `read_csv`, `read_excel`, `read_json` — load data from files or URLs
- `to_csv`, `to_excel` — export data back out

</div>

<div class="note-box" data-title="Exploration">

- `head`, `tail` — preview rows
- `describe` — summary statistics
- `info` — column types and missing values

</div>

</div>
<div>

<div class="note-box" data-title="Transformation">

- `groupby` — split-apply-combine
- `merge`, `join` — combine DataFrames
- `apply` — run a function on each row or column
- `fillna` — handle missing data

</div>

<div class="note-box" data-title="Visualization">

- `plot` — quick charts built on Matplotlib

</div>

</div>
</div>

You do not need to memorize these. Know they exist so you can ask for them by name.

---

### What could go wrong?

<div class="warning-box" data-title="Common Pitfalls">

AI-generated Pandas code can be subtly wrong. Watch for:
- **Wrong column names** — the AI may guess a column name that does not exist in your data
- **Silent type coercion** — numbers stored as strings can cause unexpected results
- **Missing data** — operations may silently drop rows with `NaN` values
- **Index confusion** — Pandas indexes can behave in surprising ways after filtering or merging

Always inspect your DataFrame (`head`, `shape`, `dtypes`) after each transformation.

</div>

---

### Developing your intuition

<div class="tip-box" data-title="Practice Strategy">

To build real understanding through vibe coding:
1. **Start with a question** about a dataset, not a function name
2. **Generate** the code, then **predict** what the output will be before running it
3. **Compare** your prediction to the actual result
4. **Modify** the code — change a parameter, swap a function — and observe what changes
5. **Explain** the result to a classmate (or to yourself out loud)

The goal is to develop intuition for what Pandas operations do, so you can direct the AI effectively and catch its mistakes.

</div>

---

### Summary

<div class="tip-box" data-title="Key Takeaways">

- **Pandas** is the go-to Python library for tabular data (rows and columns)
- It builds on NumPy by adding labels, file I/O, and powerful data manipulation tools
- In this course, we use **vibe coding**: describe what you want, generate code with AI, then verify and explain
- Your job is to **think clearly about data** — know what questions to ask, what tools exist, and whether the answers make sense
- The syntax will change; the thinking will not

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

- Check the course schedule for what's coming next

</div>
