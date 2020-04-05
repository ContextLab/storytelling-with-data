---
title: Data visualization
description: Approaches to creating effective figures
url: https://github.com/ContextLab/storytelling-with-data
theme: default
class:
  - lead
---

# Data visualization: approaches to creating effective figures
## Jeremy R. Manning
### PSYC 81.09: Storytelling with Data

---
## On the nature of data and data comprehension
- A dataset is just a **collection of values** (numbers, text, etc.)
- In principle we could display those raw values to our audience
- But that's (usually) ineffective at conveying the **specific message** we want to get across

---
## Which is clearer to you?
![Image](https://miro.medium.com/max/693/1*bV7S0zACdidh11ikjYpLpQ.png)

---
## Why visualize data?
- Our visual systems **rapidly process massive amounts of information** and are adept at **pattern recognition**
- We can leverage the visual system to convey patterns in data
- Conveying the patterns we want people to perceive means figuring out how to **turn data into pictures**

---
## Anscombe's quartet
![Image](https://seaborn.pydata.org/_images/anscombes_quartet.png)

---
## Grammar of graphics: intuition
- A language for describing *all* possible figures
- Can be a useful way of framing data visualization
- Main idea: separate data from how we visualize it

---
### Figures comprise the following **layers**:
  - **Data**: what information (values) we'll be plotting
  - **Aesthetics**: mapping from data into a "data representation space"
  - **Geometries**: what shapes can be used to represent the data
  - **Facets**: define subplots (groupings) of the data
  - **Statistics**: define statistical models and summaries (e.g., mean, median, distributions, counts, etc.)
  - **Coordinates**: maps coordinates in data representation space onto coordinates in the figure (e.g. cartesian, polar, geographic, etc.)
  - **Theme**: any non-data elements of the figure (labels, color schemes, etc.)

---
## Grammar of graphics: takeaways
- You might choose to explicitly use data visualization tools that use the grammar of graphics to create figures
- But even of you never use GoG explicitly, it can be useful to consider what the separable elements of figures are and how they affect the figure's appearance

---
## Considerations for deciding how to display data
- Do you want to display the raw values or a summary (or both!)?
- Are the observations discrete or continuous?
- What patterns in the data do you want to explore or emphasize?
- **What message do you want your audience to take away?**

---
## Examples of approaches to displaying data
- **Raw data**: show individual datapoints
- **Summaries**: highlight trends or patterns
- **Combinations**: show both raw data *and* the underlying trends or patterns
- **Polar plots**: good for displaying circular data (angles, periodic data)

---
## Examples of approaches to displaying data (continued...)
- **Clustering**: emphasize or display groupings in the data
- **Timeseries plots**: show changes over time
- **Network plots**: highlight physical or conceptual links between datapoints
- **Geospatial plots**: geographic maps (e.g., locations, addresses, GPS coordinates, etc.)
- **Animations**: use movement to convey additional information

---
# Displaying "raw" data

---
## Table
![Image](https://raw.githubusercontent.com/jeremymanning/storytelling-with-data/master/slides/figs/table.png)

---
## Bar graph
![Image](https://seaborn.pydata.org/_images/color_palettes.png)

---
## Bar graph (grouped)
![Image](https://seaborn.pydata.org/_images/grouped_barplot.png)

---
## Bar graph (stacked)
![Image](https://raw.githubusercontent.com/jeremymanning/storytelling-with-data/master/slides/figs/bar_stacked.png)

---
## Scatterplot (2D)
![Image](https://seaborn.pydata.org/_images/seaborn-scatterplot-4.png)

---
## Scatterplot (3D)
![Image](https://raw.githubusercontent.com/jeremymanning/storytelling-with-data/master/slides/figs/scatter3D.png)

---
## Heatmap
![Image](https://seaborn.pydata.org/_images/seaborn-heatmap-1.png)

---
## Volume plot
![Image](https://www.mathworks.com/matlabcentral/mlc-downloads/downloads/submissions/36139/versions/8/screenshot.jpg)

---
# Summaries

---
- histogram (discrete) -- can be 1d or 2d
- distribution or area plot (continuous)
- regression lines
- statistical reports
- vector fields, streamline plots

---
# Combinations
- violin plot, swarm plot, boxenplot, boxplot
- ridge plot
- joint grid, joint plot (hex, scatter)
- pair grid
- scatterplot matrix
- lmplot
- raincloud plot

---
# Polar coordinates (angles)
- Rose plot
- Pie chart, polar area chart
- target plot

---
# Clustering
- clustermap
- dendrogram

---
# Timeseries data
- line plot, ribbon plot

---
# Networks:
- circos plots
- circular tree
- edge colormap
- graph, directed graph
- node colormap
- edge colormap
- ego graph

---
# Geospatial data:
- map projections
- cloropleth maps
- geo scatterplots and line plots

---
# Animations:
- uber use
- world happiness animation
- hypertools story listening

---
# Classics:
- periodic table: https://docs.bokeh.org/en/latest/docs/gallery/periodic.html
- napoleonic campaign infographic: https://en.wikipedia.org/wiki/Charles_Joseph_Minard
- fivethirtyeight snake plot https://medium.com/@kevindewalt/fivethirtyeights-snake-is-data-visualization-genius-f9901be5a74a

---
# Grammar of graphics:
- useful way of framing data visualization
- main idea: separate data from how we visualize it
- a language for describing *all* possible plots we could make
- plot = data + geometric objects (how data are summarized and/or converted to shapes) + scale and coordinate system (how geometric shapes are transformed and/or organized visually) + facets (groupings of different subsets of data) + annotations (axis labels, title, tick labels, etc.)

---
# General tips and tricks:
- tufte's data-to-ink ratio principle
- "at a glance" readability
- use consistent color schemes to highlight connections
- visual weight
