---
marp: true
theme: cdl-theme
math: katex
transition: fade 0.25s
author: Contextual Dynamics Lab
---

# The pursuit of truth
## PSYC 81.09: Storytelling with Data

Jeremy R. Manning
Dartmouth College
Spring 2026

---

# Who am I?
<!-- _class: manual-layout -->

<div class="instructor-container">

<div class="instructor-header">
<div class="instructor-header-left">
<h3 style="color: #001c12 !important; margin: 0;">Jeremy R. Manning, Ph.D.</h3>
<p>
Associate Professor | Psychological &amp; Brain Sciences | <img src="figs/instructor/dartmouth_logo.png" style="height: 1.2em; vertical-align: middle; margin: 0 0.1em;"> | <a href="https://context-lab.com/scheduler">Moore 349</a>
</p>
</div>
<div class="instructor-header-right">
<div class="header-link-row">
<img src="figs/instructor/cdl_logo.png" class="header-icon">
<a href="https://www.context-lab.com" class="header-link"><u>context-lab.com</u></a>
</div>
<div class="header-link-row">
<img src="figs/instructor/github_logo.png" class="header-icon">
<a href="https://github.com/ContextLab" class="header-link"><u>ContextLab</u></a>
</div>
</div>
</div>

<div class="content-grid">

<div class="col-flex">

<div class="info-box-styled" style="text-align: left !important;">
<h4>Research focus</h4>
<p style="text-align: left !important; display: block; margin: 0;">How do our brains support our ongoing conscious thoughts, and how (and what) do we remember?</p>
</div>

<div class="info-box-styled" style="text-align: left !important;">
<h4>Key areas</h4>
<p style="text-align: left !important; display: block; margin: 0;">Learning and memory, education technology, brain network dynamics, data science, NLP</p>
</div>

<div class="info-box-styled" style="text-align: left !important;">
<h4>Approach</h4>
<p style="text-align: left !important; display: block; margin: 0;">Theory, models, experiments, neuroimaging</p>
</div>

</div>

<div class="col-flex">

<div class="info-box-styled" style="text-align: left !important;">
<h4>Training</h4>
<div class="training-grid">
<div class="training-logo-cell"><img src="figs/instructor/brandeis_logo.svg" alt="Brandeis" class="training-logo"></div>
<div class="training-text" style="text-align: left !important;">B.S., Neuroscience &amp; Computer Science</div>

<div class="training-logo-cell"><img src="figs/instructor/upenn_logo.png" alt="Penn" class="training-logo"></div>
<div class="training-text">Ph.D., Neuroscience</div>

<div class="training-logo-cell"><img src="figs/instructor/princeton_logo.svg" alt="Princeton" class="training-logo"></div>
<div class="training-text">Postdoc, Computer Science &amp; Neuroscience</div>
</div>
</div>

<div class="info-box-styled">
<h4>Funding &amp; collaborators</h4>
<div class="funding-logo-grid">
<img src="figs/instructor/nih_logo.png" alt="NIH" style="max-height: 45px;">
<img src="figs/instructor/nsf_logo.png" alt="NSF" style="max-height: 65px;">
<img src="figs/instructor/darpa_logo.png" alt="DARPA" style="max-height: 30px;">
<img src="figs/instructor/brainfit_logo.png" alt="BrainFit" style="max-height: 48px;">
</div>
<div class="combined-card-spacer"></div>
<div class="logo-grid">
<img src="figs/instructor/intel_labs_logo.png" alt="Intel Labs" title="Intel Labs" style="max-height: 28px;">
<img src="figs/instructor/meta_logo.png" alt="Meta" title="Meta" style="max-height: 22px;">
<img src="figs/instructor/google_logo.webp" alt="Google" title="Google" style="max-height: 32px;">
<img src="figs/instructor/amazon_logo.png" alt="Amazon" title="Amazon" style="max-height: 30px;">
</div>
</div>

</div>

</div>

</div>

---
<!-- _class: scale-90 -->

## Welcome!

<div class="note-box" data-title="What this course is about">

This course is a **data science bootcamp** wrapped in the art of storytelling. You will learn to:

- Find, analyze, interpret, and visualize data
- Craft compelling narratives grounded in evidence
- Use modern tools — Python, Jupyter, and AI-assisted coding — to tell stories that matter

*Whether you pursue data science, medicine, policy, research, business, or myriad other fields, these skills will serve you well **nearly everywhere**!*

</div>

<div class="tip-box" data-title="Teaching philosophy">

I strongly believe in **teaching by doing**. We will learn concepts through hands-on practice. You will build a portfolio of data stories that you can share with future employers, collaborators, and friends. We'll critically evaluate each others' stories in a supportive environment, and you'll learn to give and receive feedback that helps you grow.

</div>

---

<!-- _class: scale-90 -->

## Course structure

<div class="note-box" data-title="Part 1: Building the toolkit (Weeks 1&mdash;4)">

Four modules, each with an assignment:
1. What makes a good story?
2. Data visualization
3. Python and Jupyter notebooks
4. Vibe coding and data science tools

</div>

<div class="note-box" data-title="Part 2: Data stories (Weeks 5&mdash;10)">

- Pick a question and a dataset (solo or in groups)
- Analyze the data, build visualizations, and create a video telling your story
- Produce a minimum of **3 data stories** during Part 2

</div>

---
<!-- _class: scale-80 -->

## Overarching goal: the pursuit of *truth*

<div class="definition-box" data-title="A fundamental question">

What does it mean to **know** something?

</div>

<div class="note-box" data-title="Think of something you know with near-100% certainty...">

- How did that knowledge get into your brain?
- What evidence supports it?
- What would it take to convince you otherwise?

</div>

<div class="example-box" data-title="Example: &quot;levels of scientific inquiry&quot;">

- In my lab, I study learning and memory. I *assume* that these functions happen in the brain, and that we can learn about them by measuring brain activity.
- At a hypothetical lab one level *lower* in the hierarchy: maybe memories are stored in RNA instead of synapses. Some memories can even be passed on to offspring! (This is actually a real hypothesis in the field of epigenetics.)
- At a hypothetical lab one level *higher* in the hierarchy: maybe learning and memory are epiphenomena of more general principles of information processing that apply to all complex systems, from brains to ecosystems to economies.

</div>

---

## How do we evaluate claims?

<div class="note-box" data-title="Sources of knowledge">

- **Direct observation** — you saw or measured it yourself
- **Trusted testimony** — someone credible told you
- **Logical deduction** — you reasoned your way to it
- **Data and evidence** — systematic measurement and analysis

</div>

<div class="warning-box" data-title="The catch">

Every source of knowledge is fallible. Our measurements are always incomplete, our reasoning can be flawed, and our trusted sources can be wrong.

</div>

---

<!-- _class: scale-90 -->

## Truth in the age of information

<div class="warning-box" data-title="Challenges to truth">

- **Misinformation and disinformation** — false claims spread faster than corrections
- **Confirmation bias** — we seek out evidence that supports what we already believe
- **Cherry-picking data** — selecting only the numbers that tell the story you want
- **Viral narratives** — compelling stories can drown out careful analysis

</div>

<div class="tip-box" data-title="The antidote">

Data literacy is a superpower. *When you can evaluate evidence for yourself, you are harder to mislead.*

</div>

<div class="important-box" data-title="AI is not going to (fully) solve this for us">

Consider: when you ask ChatGPT to analyze some data, how can you really **know** that it did what you asked (or meant)? You need to be able to think through the process yourself to (a) ask the right questions, and (b) evaluate the answers you get.

</div>

---

<!-- _class: scale-90 -->

## Truth in the age of AI

<div class="important-box" data-title="New challenges for 2026 and beyond">

- **Deepfakes** — synthetic audio and video that are increasingly indistinguishable from reality
- **AI-generated text** — large language models can produce fluent, convincing, and completely fabricated content
- **Synthetic data** — AI can generate realistic-looking datasets that never came from real observations
- **Automation of persuasion** — AI tools can produce targeted misinformation at scale

</div>

<div class="note-box" data-title="Why this matters for you">

The ability to critically evaluate claims — and to produce honest, evidence-based analyses — has never been more important. The ability to *communicate* your arguments clearly and compellingly is also crucial. This course will help you develop both skill sets.

</div>

---

## Data as evidence

<div class="definition-box" data-title="The data science perspective">

From a data science perspective, knowledge must come from (real) **data**. Data gives us tools to move beyond opinion, intuition, and anecdote toward rigorous evaluation of claims.

</div>

<div class="example-box" data-title="What data can do">

- Reveal patterns invisible to casual observation
- Quantify uncertainty so we know how confident to be
- Compare competing explanations systematically
- Scale analysis far beyond any individual's capacity

</div>

---

## "All models are wrong, but some are useful"

<div class="definition-box" data-title="George Box, 1976">

Every model, theory, or dataset is an **approximation**. No measurement captures everything. No analysis is assumption-free.

</div>

<div class="note-box" data-title="What this means in practice">

- We never have exactly the right data, or enough of it
- There are always multiple ways to analyze and interpret the same dataset
- These are **fundamental** limitations, not problems we can simply engineer away
- The goal is not perfection — it is to be **less wrong** over time

</div>

---

<!-- _class: scale-90 -->

## Critical thinking with data

<div class="warning-box" data-title="Common pitfalls">

- **Correlation vs. causation** — two things moving together does not mean one causes the other
- **Sampling bias** — who is (and isn't) in your dataset changes what conclusions you can draw
- **Base rate neglect** — ignoring how common something is leads to wildly wrong probability estimates
- **Overfitting** — a model that explains everything in your data may explain nothing in new data

</div>

<div class="tip-box" data-title="Rule of thumb">

Always ask: *What would have to be true for this conclusion to be wrong?*

</div>

---

## Stories shape how we see truth

<div class="note-box" data-title="The double-edged sword of narrative">

Stories are the most powerful communication tool humans have. They can:

- **Illuminate** — making complex data accessible, memorable, and actionable
- **Mislead** — framing evidence selectively to support a predetermined conclusion

The same dataset can tell very different stories depending on what you choose to show, emphasize, or leave out.

</div>

<div class="important-box" data-title="Our responsibility">

As data storytellers, we have an obligation to be **honest** — even when the truth is complicated or inconvenient.

</div>

---

## Your mission

<div class="tip-box" data-title="What you'll learn to do">

Learn to tell **true stories** with data — stories that are:

- **Honest** — grounded in evidence, transparent about limitations
- **Compelling** — structured, visual, and memorable
- **Evidence-based** — reproducible analyses that others can verify

</div>

---

<!-- _class: scale-90 -->

## What we'll cover this term

<div class="note-box" data-title="Topics and tools">

- **Storytelling principles** — narrative structure, audience, framing
- **Data visualization** — turning numbers into insight
- **Programming** — Python, Jupyter notebooks, Google Colab
- **Vibe coding** — using AI assistants to accelerate your workflow
- **Data science tools** — pandas, matplotlib, seaborn, scikit-learn, and more

</div>

<div class="tip-box" data-title="No prerequisites">

You do not need prior programming experience. We will build up the required skill set from scratch.

</div>

---

## Discussion

<div class="example-box" data-title="Let's talk">

- What is a claim you have seen recently that you were not sure was true?
- How would you go about evaluating it?
- What evidence would you need to feel confident one way or the other?

</div>

<div class="note-box" data-title="Think about">

As we discuss, notice the difference between *wanting* something to be true and *having evidence* that it is true.

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

- **Wednesday and Thursday (X-hour):** No class (I'll be traveling)
- **Friday:** What makes a good story? We'll workshop some ideas and I'll release Assignment 1

</div>
