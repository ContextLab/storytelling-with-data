---
marp: true
theme: cdl-theme
math: katex
---

# Vibe Coding: AI-Assisted Development
## Jeremy R. Manning
### PSYC 81.09: Storytelling with Data

---

## What is vibe coding?

<div class="definition-box" data-title="Vibe coding">

**Vibe coding** is the practice of using AI coding agents to rapidly prototype and implement software by **describing what you want in natural language**, then iterating on the output. You focus on the *what* and *why* — the AI handles the *how*.

</div>

---

## Why vibe coding matters for data storytelling

<div class="important-box" data-title="Automation-resilient skills">

AI can handle syntax, boilerplate, and implementation details. That frees you to focus on the skills that **can't be automated**:

- **Critical thinking** — Is this the right question to ask?
- **Problem framing** — What data do we need and why?
- **Storytelling** — How do we communicate findings to an audience?
- **Verification** — Does the output actually make sense?

These are the skills that matter most in a world of AI tools (Donoghue et al., 2020, §3.5).

</div>

---

## The vibe coding mindset

<div class="note-box" data-title="You + AI = a team">

| You | AI |
|-|-|
| **Direct** the project | **Execute** the details |
| **Verify** correctness | **Generate** code and text |
| **Understand** the logic | **Remember** syntax and APIs |
| **Ask** the right questions | **Produce** candidate answers |

You don't need to memorize Python syntax. You *do* need to understand what your code is doing and why.

</div>

---

## Free AI tools at Dartmouth

<div class="tip-box" data-title="Your Dartmouth AI toolkit">

- **[chat.dartmouth.edu](https://chat.dartmouth.edu)** — Access to Claude, ChatGPT, Mistral, and more. Chat interface for general-purpose AI assistance.
- **[claude.dartmouth.edu](https://claude.dartmouth.edu)** — Dedicated Claude access with extended features.

Both are **free with your Dartmouth credentials** — no subscriptions or API keys needed.

</div>

---

## Fallback options

<div class="note-box" data-title="Browser-only and off-campus alternatives">

If you can't access the Dartmouth tools or need browser-only options:

- **[claude.ai](https://claude.ai)** — Free tier available (rate-limited)
- **GitHub Copilot** — Free with a [GitHub Student Developer Pack](https://education.github.com/pack)
- **Google Colab AI features** — Built-in code suggestions in Colab notebooks

These are backup options — the Dartmouth tools should be your first choice.

</div>

---

## Claude Code: your AI coding agent

<div class="definition-box" data-title="What is Claude Code?">

**Claude Code** is a terminal-based AI agent that can:

- **Read** your entire project and understand its structure
- **Write** code, tests, and documentation
- **Run** commands and see the output
- **Manage** Git commits, branches, and pull requests
- **Iterate** based on errors and your feedback

It lives in your terminal and works directly with your files — no copy-pasting between browser tabs.

</div>

---

<!-- _class: scale-90 -->

## Installing Claude Code

<div class="example-box" data-title="Setup (macOS / Linux / Windows WSL)">

**1. Install Node.js** (if you don't already have it):
```bash
# macOS with Homebrew
brew install node

# Or download from https://nodejs.org
```

**2. Install Claude Code:**
```bash
npm install -g @anthropic-ai/claude-code
```

**3. Launch it:**
```bash
cd your-project-folder
claude
```

</div>

<div class="note-box" data-title="Browser alternative">

If you can't install software locally, use **[claude.dartmouth.edu](https://claude.dartmouth.edu)** or **[claude.ai](https://claude.ai)** in your browser instead.

</div>

---

## Basic Claude Code usage

<div class="example-box" data-title="A typical interaction">

```
$ claude
> Load my_data.csv and show me the first 5 rows

Claude reads the file, writes Python code, runs it, and shows output.

> Now create a bar chart of the 'category' column counts

Claude generates matplotlib code, creates the chart, and saves it.

> The colors are hard to read — use the Dartmouth color palette

Claude updates the code and regenerates the chart.
```

</div>

The key pattern: **describe → review → refine → repeat**.

---

## The classic four-step workflow

<div class="note-box" data-title="From idea to implementation">

| Step | What you do | What AI does |
|-|-|-|
| **1. Describe** | Explain what you want in plain English | Listens and asks clarifying questions |
| **2. Design** | Agree on the approach and structure | Proposes architecture and components |
| **3. Plan** | Review and approve the plan | Breaks work into concrete steps |
| **4. Implement** | Verify each piece works correctly | Writes and runs the code |

</div>

This works well for small projects. For larger or more complex work, use **speckit**.

---

## The speckit workflow

<div class="definition-box" data-title="Spec-driven development">

**speckit** is a structured approach to vibe coding: you write a **specification** first — describing *what* you want and *why* — then let AI plan and implement the solution.

Think of it like writing a detailed recipe request before the chef starts cooking. The clearer your request, the better the meal.

</div>

---

<!-- _class: scale-90 -->

## The 6 speckit steps (part 1)

<div class="example-box" data-title="Steps 1–3: Define the problem">

**1. Constitution** — Define the ground rules for your project
- "All code must be Python, runnable in Google Colab"
- "Use matplotlib and seaborn for visualizations"

**2. Specify** — Describe WHAT you want and WHY (never HOW)
- "I need a tool that helps me explore correlations in survey data so I can find interesting patterns to investigate further"

**3. Clarify** — The AI asks you targeted questions
- "Should it handle missing data? How many variables? What kind of output?"

</div>

---

<!-- _class: scale-90 -->

## The 6 speckit steps (part 2)

<div class="example-box" data-title="Steps 4–6: Build the solution">

**4. Plan** — AI proposes a technical architecture
- Data loading module, correlation computation, visualization layer
- You review and approve before any code is written

**5. Tasks** — Break the plan into small, testable chunks
- "Task 1: Load CSV and validate columns"
- "Task 2: Compute pairwise correlations"
- "Task 3: Generate heatmap visualization"

**6. Implement** — Execute each task with verification
- AI writes code, runs tests, and you confirm each piece works

</div>

---

## Writing a good spec

<div class="warning-box" data-title="The golden rule">

**Focus on WHAT and WHY, never HOW.**

No programming languages, databases, frameworks, or APIs in the spec! Those are implementation details that the AI should decide (or that you'll discuss during the planning phase).

</div>

**Good:** "I need to visualize how survey responses cluster into groups so I can identify distinct participant profiles."

**Bad:** "Use scikit-learn KMeans with k=5 and plot with plotly in a Dash app using PostgreSQL."

---

## Example spec

<div class="example-box" data-title="A user story with acceptance scenarios">

**As a** researcher analyzing survey data,
**I want** an interactive visualization of response patterns,
**So that** I can identify clusters of similar respondents.

**Given** a CSV file with numeric survey responses,
**When** I run the tool,
**Then** it should display a 2D plot where similar respondents appear close together.

**Given** the visualization is displayed,
**When** I hover over a point,
**Then** I should see that respondent's ID and key response values.

</div>

---

## Guided example: describe the project

<div class="example-box" data-title="Step 1: Start with a clear description">

Imagine you want to explore a dataset of movie ratings. You might say:

> "I want a tool that loads a CSV of movie ratings, lets me filter by genre, and creates an interactive scatter plot showing rating vs. number of reviews. I want to be able to hover over points to see the movie title."

</div>

<div class="tip-box" data-title="Tip">

Notice: no mention of specific libraries or implementation details. Just **what** you want and **why** it would be useful.

</div>

---

<!-- _class: scale-90 -->

## Guided example: spec and plan

<div class="example-box" data-title="Step 2: Use speckit to structure your thinking">

In Claude Code:
```
> /speckit.specify
```

The AI will help you turn your description into a formal spec, ask clarifying questions, then generate a plan:

- **Data layer:** Load and validate the CSV, handle missing values
- **Filter layer:** Genre selection with a dropdown
- **Visualization layer:** Interactive scatter plot with hover tooltips
- **Output:** Self-contained HTML file or Colab notebook

</div>

You review the plan and say "looks good" or "actually, I also want..."

---

## Guided example: implement and iterate

<div class="example-box" data-title="Step 3: Build it piece by piece">

```
> /speckit.implement
```

Claude Code works through each task:
1. Loads and validates `movies.csv` ✓
2. Adds genre filter ✓
3. Creates scatter plot... *but the axis labels are wrong*

You catch the issue:
```
> The x-axis should be "Number of Reviews", not "Review Count".
   Also, can you add a trend line?
```

Claude fixes it and continues.

</div>

<div class="warning-box" data-title="Verify and explain!">

Before moving on: **read the generated code** and explain in your own words what each section does and why. This is the most important step!

</div>

---

## Verify and explain!

<div class="warning-box" data-title="The most important habit in vibe coding">

After every piece of generated code, ask yourself:

1. **Can I explain** what this code does in plain English?
2. **Does the output** match what I expected?
3. **Have I tested** it with different inputs?
4. **Could I describe** to someone else *why* each step is necessary?

If the answer to any of these is "no," **stop and ask the AI to explain** before moving on. Never accept code you don't understand.

</div>

---

## Simplicity principles

<div class="tip-box" data-title="Keep it simple">

- **Spend time clarifying upfront** — 10 minutes of clear thinking saves hours of debugging
- **Ambiguity is OK initially** — start vague, then refine as you learn more
- **Continually simplify** — if a solution feels complicated, ask "is there a simpler way?"
- **Single source of truth** — one file for data, one file for config, one file for output
- **Keep your project clean** — delete experiments you're done with, organize what you keep

</div>

---

## Common pitfalls

<div class="warning-box" data-title="Mistakes to avoid">

- **Accepting code you don't understand** — The #1 mistake. Always verify and explain.
- **Not testing** — Run the code with real data. Check edge cases. Look at the output.
- **Vague prompts** — "Make it better" gives vague results. Be specific about what to change.
- **Not iterating** — The first output is rarely perfect. Refine, refine, refine.
- **Ignoring errors** — Read error messages carefully. They usually tell you exactly what's wrong.
- **Over-specifying implementation** — Tell the AI *what* you want, not *how* to build it.

</div>

---

## When AI gets stuck

<div class="tip-box" data-title="Strategies for getting unstuck">

- **Break the problem smaller** — Instead of "build the whole thing," try "just load the data first"
- **Provide more context** — Share example data, expected output, or error messages
- **Try a different approach** — "That approach isn't working. Can you try a completely different method?"
- **Ask AI to explain its reasoning** — "Walk me through your thought process step by step"
- **Start fresh** — Sometimes a clean conversation works better than a long, tangled one
- **Ask a human** — Office hours, classmates, and the course discussion board are all great resources

</div>

---

## Practice exercise: plan your project (1/2)

Think of a simple data project you'd like to build. It could be:

- A visualization of your favorite dataset
- A tool that analyzes text from a book or article
- An interactive chart comparing statistics across categories

<div class="example-box" data-title="Write your spec">

1. **What** do you want to build? (2-3 sentences)
2. **Why** is it interesting or useful? (1-2 sentences)
3. **What should happen** when it works? (Given/When/Then format)

</div>

---

## Practice exercise: build it! (2/2)

Now use the vibe coding workflow:

<div class="example-box" data-title="Follow these steps">

1. Open Claude Code (or claude.dartmouth.edu)
2. Share your spec from the previous slide
3. Let the AI ask clarifying questions — answer them!
4. Review the proposed plan
5. Implement step by step
6. Test with real data

</div>

<div class="warning-box" data-title="Verify and explain!">

Before you call it done: **read every section of the generated code** and explain in your own words what it does and why. If you can't explain it, you're not done yet.

</div>

---

## Summary + resources

**Key takeaways:**
- Vibe coding lets you focus on **thinking** while AI handles **syntax**
- Always **verify and explain** — never accept code you don't understand
- Start with **what** and **why**, not **how**
- **Iterate** — the first output is a draft, not a final product

<div class="tip-box" data-title="Resources">

- **[chat.dartmouth.edu](https://chat.dartmouth.edu)** — Multi-model AI chat (free with Dartmouth credentials)
- **[claude.dartmouth.edu](https://claude.dartmouth.edu)** — Dedicated Claude access
- **[Claude Code docs](https://docs.anthropic.com/en/docs/claude-code)** — Installation and usage guide
- **[speckit](https://github.com/ContextLab/speckit)** — Spec-driven development toolkit

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

- **Friday:** Assignment 3 brainstorm + release

</div>


<!-- Donoghue et al. integration tracking (FR-009):
  1. Creative problem solving (§3) → implemented in Assignment 3 (separate file)
  2. Automation-resilient skills (§3.5) → slide 3 "Why vibe coding matters"
  3. Data literacy over syntax (§3.1) → implemented in Module 4 reworks (separate files)
  4. Teaching how to get unstuck (§4.4) → slide 22 "When AI gets stuck" + demos deck
  5. Practical relevant tooling (§4.2) → slides 5-9 Dartmouth AI tools + Claude Code
-->
