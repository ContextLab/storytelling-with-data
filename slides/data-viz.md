---
marp: true
theme: cdl-theme
math: katex
---

![bg opacity:0.1](figs/dviz_bg.png)
# Data visualization in the age of AI
## Jeremy R. Manning
### PSYC 81.09: Storytelling with Data

---

## Why visualize data?

<div class="important-box" data-title="The power of vision">

- Our visual systems **rapidly process massive amounts of information** and are adept at **pattern recognition**
- We can leverage the visual system to convey patterns in data
- Conveying the patterns we want people to perceive means figuring out how to **turn data into pictures**

</div>

---

## Which is clearest to you?
![height:500px](figs/data_representations.png)

---

## Anscombe's quartet

<div class="warning-box" data-title="Statistics can't tell the whole story">

These four datasets have identical summary statistics, but look very different when plotted!

</div>

![height:400px](figs/anscombes_quartet.png)

---

<div class="important-box" data-title="The most important question">

**What message do you want your audience to take away?**

Every visualization decision -- color, layout, chart type -- should serve that message. Start with the message, then choose the visualization.

</div>

---

<div class="note-box" data-title="Our approach">

We focus on understanding **what** these tools do and **when** to use them -- not memorizing syntax. AI handles the syntax; you handle the thinking.

</div>

---

## Vibe coding your visualizations

<div class="definition-box" data-title="The vibe coding workflow">

1. **Describe** the visualization you want in plain language
2. **Generate** it with Claude Code (or another AI coding tool)
3. **Iterate** on the design -- refine colors, labels, layout
4. **Verify and explain** -- make sure the output is correct and you understand every element

</div>

---

<div class="warning-box" data-title="Verify and explain">

AI-generated code can produce plots that *look* right but are **wrong** -- axes may be swapped, data may be filtered incorrectly, or statistics may be miscomputed. Always verify the output against your data, and make sure you can explain what every part of the figure shows.

</div>

---

## Grammar of graphics

<div class="note-box" data-title="Figures comprise separable layers">

- **Data**: the values being plotted
- **Aesthetics**: mapping from data to visual properties (position, color, size)
- **Geometries**: shapes representing the data (points, bars, lines)
- **Facets**: subplots or groupings
- **Statistics**: summaries or transformations
- **Coordinates**: the coordinate system (Cartesian, polar, geographic)
- **Theme**: non-data elements (fonts, backgrounds, legends)

</div>

---

<!-- _class: scale-90 -->

## Choosing the right visualization

<div class="tip-box" data-title="Match the visualization to your data and message">

- **Comparing categories?** Bar chart, box plot
- **Showing distributions?** Histogram, violin plot
- **Revealing relationships?** Scatter plot, heatmap
- **Tracking change over time?** Line plot
- **Displaying spatial data?** Choropleth map
- **Showing connections?** Network graph
- **Adding a dimension?** Animation

</div>

---

![bg opacity:0.1](figs/dviz_bg.png)
# Visualization gallery
### A reference collection of common plot types

---

## Scatter plot
![height:500px](figs/scatterplot.png)

---

## Bar chart
![height:500px](figs/barplot.png)

---

## Histogram
![height:500px](figs/histplot.png)

---

## Heatmap
![height:500px](figs/heatmap.png)

---

## Violin plot
![height:500px](figs/violinplot.png)

---

## Box plot
![height:500px](figs/boxplot.png)

---

## Line plot
![height:500px](figs/lineplot.png)

---

## Choropleth map
![height:500px](figs/cloropleth.png)

---

## Network graph
![height:500px](figs/network_graph.png)

---

## Animation: life expectancy vs. GDP over time
![height:500px](figs/gapminder.gif)

---

## General tips and tricks

<div class="tip-box" data-title="Design principles">

- Tufte's **data-to-ink ratio** principle
- Optimize for **intuition and readability**
- Use consistent color schemes to highlight connections
- Use visual weight across figure elements
- **Be willing to break all of the rules!**

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

- **Friday:** Workshop data story ideas + Assignment 2 release

</div>
