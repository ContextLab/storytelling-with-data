---
title: Data visualization
description: Approaches to creating effective figures
url: https://github.com/ContextLab/storytelling-with-data
theme: gaia
class:
  - invert
  - lead
---

![bg opacity:0.1](https://mediashift.org/wp-content/uploads/2015/07/dviz.png)
# Data visualization: approaches to creating effective figures
## Jeremy R. Manning
### PSYC 81.09: Storytelling with Data

---
## On the nature of data and data comprehension
- A dataset is just a **collection of values** (numbers, text, etc.)
- In principle we could display those raw values to our audience
- But that's (usually) ineffective at conveying the **specific message** we want to get across

---
## Which is clearest to you?
![height:500px](https://miro.medium.com/max/693/1*bV7S0zACdidh11ikjYpLpQ.png)

---
## Why visualize data?
- Our visual systems **rapidly process massive amounts of information** and are adept at **pattern recognition**
- We can leverage the visual system to convey patterns in data
- Conveying the patterns we want people to perceive means figuring out how to **turn data into pictures**

---
## Statistics and summaries can't tell us the whole story: **Anscombe's quartet**
![height:500px](https://seaborn.pydata.org/_images/anscombes_quartet.png)

---
## Statistics and summaries can't tell us the whole story: **The Datasaurus Dozen**
![height:450px](https://blog.revolutionanalytics.com/downloads/DataSaurus%20Dozen.gif)

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
![bg opacity:0.1](https://mediashift.org/wp-content/uploads/2015/07/dviz.png)
# Displaying "raw" data: directly map each observation onto a single point or shape

---
## Table
![height:450px](https://raw.githubusercontent.com/ContextLab/storytelling-with-data/master/slides/figs/table.png)

---
## Bar graph
![height:500px](https://seaborn.pydata.org/_images/barplot_1_0.png)

---
## Bar graph (grouped)
![height:500px](https://seaborn.pydata.org/_images/grouped_barplot.png)

---
## Bar graph (stacked)
![height:500px](https://raw.githubusercontent.com/ContextLab/storytelling-with-data/master/slides/figs/bar_stacked.png)

---
## Scatterplot (2D)
![height:500px](https://seaborn.pydata.org/_images/scatterplot_3_0.png)

---
## Scatterplot (3D)
![height:500px](https://raw.githubusercontent.com/ContextLab/storytelling-with-data/master/slides/figs/scatter3D.png)

---
## Heatmap
![height:500px](https://seaborn.pydata.org/_images/seaborn-heatmap-1.png)

---
## Volume plot
![height:450px](https://www.mathworks.com/matlabcentral/mlc-downloads/downloads/submissions/36139/versions/8/screenshot.jpg)

---
![bg opacity:0.1](https://mediashift.org/wp-content/uploads/2015/07/dviz.png)
# Summaries: characterize overarching trends or patterns in the data, but don't show individual datapoints

---
## Report
![height:500px](https://www.pybloggers.com/wp-content/uploads/2016/02/www.marsja.sewp-contentuploads201602output_pandas_describe-36b54bfafa7419582f516b1a41d1feb3d22e5bdf.png)

---
## Histograms and density plot
![height:500px](https://seaborn.pydata.org/_images/histplot_9_0.png)

---
## Two-dimensional histogram or density plot
![height:500px](https://seaborn.pydata.org/_images/jointplot_9_0.png)

---
## Ridge plot
![height:500px](https://seaborn.pydata.org/_images/kde_ridgeplot.png)

---
## Regression line
![height:500px](https://seaborn.pydata.org/_images/seaborn-regplot-1.png)

---
## Vector field
![height:500px](https://raw.githubusercontent.com/ContextLab/storytelling-with-data/master/slides/figs/quiver_plot.png)

---
## Streamline plot
![height:500px](https://raw.githubusercontent.com/ContextLab/storytelling-with-data/master/slides/figs/streamplot.png)

---
![bg opacity:0.1](https://mediashift.org/wp-content/uploads/2015/07/dviz.png)
# Combination plots: show both the individual datapoints *and* the summary in a single plot

---
## Violin plot
![height:500px](https://seaborn.pydata.org/_images/simple_violinplots.png)

---
## Swarm plot
![height:500px](https://seaborn.pydata.org/_images/swarmplot_5_0.png)

---
## Boxenplot
![height:500px](https://seaborn.pydata.org/_images/boxenplot_7_0.png)

---
## Box (and whiskers) plot
![height:500px](https://seaborn.pydata.org/_images/boxplot_15_0.png)

---
## Joint plot (scatter)
![height:500px](https://seaborn.pydata.org/_images/jointplot_7_0.png)

---
## Joint plot (hex)
![height:500px](https://seaborn.pydata.org/_images/jointplot_11_0.png)

---
## Pair grid
![height:500px](https://seaborn.pydata.org/_images/PairGrid_5_0.png)

---
## Scatterplot matrix
![height:500px](https://seaborn.pydata.org/_images/scatterplot_matrix.png)

---
## Raincloud plot
![height:500px](https://raw.githubusercontent.com/RainCloudPlots/RainCloudPlots/master/images/10repanvplot_cropped.jpg)

---
![bg opacity:0.1](https://mediashift.org/wp-content/uploads/2015/07/dviz.png)
# Polar plots: display circular (angular) data, or visualize data summaries using polar coordinates

---
## Polar area chart (AKA Coxcomb chart, Rose chart)
![height:500px](https://i.stack.imgur.com/gxPwy.png)

---
## Pie chart
![height:500px](https://raw.githubusercontent.com/ContextLab/storytelling-with-data/master/slides/figs/pie_chart.png)

---
## Target (bullseye) plot
![height:500px](https://ggplot2.tidyverse.org/reference/coord_polar-4.png)

---
![bg opacity:0.1](https://mediashift.org/wp-content/uploads/2015/07/dviz.png)
# Clustering: emphasize or display groupings in the data

---
## Dendrogram
![height:500px](https://www.data-to-viz.com/graph/dendrogram_files/figure-html/unnamed-chunk-3-1.png)

---
## Clustermap
![height:500px](https://seaborn.pydata.org/_images/seaborn-clustermap-1.png)

---
![bg opacity:0.1](https://mediashift.org/wp-content/uploads/2015/07/dviz.png)
# Timeseries data: show changes over time

---
## Line plot
![height:500px](https://seaborn.pydata.org/_images/wide_data_lineplot.png)

---
## Ribbon plot
![height:500px](https://seaborn.pydata.org/_images/errorband_lineplots.png)

---
![bg opacity:0.1](https://mediashift.org/wp-content/uploads/2015/07/dviz.png)
# Networks: highlight physical or conceptual links between datapoints

---
## Undirected graph
![height:500px](https://networkx.github.io/documentation/stable/_images/sphx_glr_plot_random_geometric_graph_001.png)

---
## Directed graph
![height:500px](https://networkx.github.io/documentation/stable/_images/sphx_glr_plot_directed_001.png)

---
## Circos plots (AKA Chord diagram)
![height:500px](https://www.data-to-viz.com/graph/chord_files/figure-html/unnamed-chunk-1-1.png)

---
## Circular tree
![height:500px](https://networkx.github.io/documentation/stable/_images/sphx_glr_plot_circular_tree_001.png)

---
## Node colormap
![height:500px](https://networkx.github.io/documentation/stable/_images/sphx_glr_plot_node_colormap_001.png)

---
## Edge colormap
![height:500px](https://networkx.github.io/documentation/stable/_images/sphx_glr_plot_edge_colormap_001.png)

---
## Ego graph
![height:500px](https://networkx.github.io/documentation/stable/_images/sphx_glr_plot_ego_graph_001.png)

---
![bg opacity:0.1](https://mediashift.org/wp-content/uploads/2015/07/dviz.png)
# Geospatial data: geographic maps (e.g., locations, addresses, GPS coordinates, etc.)

---
## Map projections (also see [Wikipedia](https://en.wikipedia.org/wiki/List_of_map_projections))
![height:400px](https://imgs.xkcd.com/comics/map_projections.png)

---
## Cloropleth map
![height:500px](https://raw.githubusercontent.com/ContextLab/storytelling-with-data/master/slides/figs/cloropleth.png)

---
## Bubble map
![height:500px](https://raw.githubusercontent.com/ContextLab/storytelling-with-data/master/slides/figs/bubble_map.png)

---
## Geographical line plot
![height:500px](https://raw.githubusercontent.com/ContextLab/storytelling-with-data/master/slides/figs/lineplot_map.png)

---
![bg opacity:0.1](https://mediashift.org/wp-content/uploads/2015/07/dviz.png)
# Animations: use movement to convey additional information

---
## Example: Uber trips in New York City
![height:500px](https://raw.githubusercontent.com/ContextLab/storytelling-with-data/master/slides/figs/uber_trips_timelapse.gif)

---
## Example: Yearly life expectancy vs. GDP throughout the world
![height:500px](https://raw.githubusercontent.com/ContextLab/storytelling-with-data/master/slides/figs/gapminder.gif)

---
## Example: brain-decoded thoughts from different people as they're listening to a story
![height:450px](https://hypertools.readthedocs.io/en/latest/_images/hypertools.gif)

---
![bg opacity:0.1](https://mediashift.org/wp-content/uploads/2015/07/dviz.png)
# Classics

---
## Periodic table
![height:500px](https://raw.githubusercontent.com/ContextLab/storytelling-with-data/master/slides/figs/periodic_table.png)

---
## Minard's map of Napoleon's Russian campaign
![height:500px](https://upload.wikimedia.org/wikipedia/commons/2/29/Minard.png)

---
## FiveThirtyEight's electoral votes depictions
![height:500px](https://images.squarespace-cdn.com/content/v1/5bfc8dbab40b9d7dd9054f41/1599947028927-DT85T3QZVWTYV9DDCSAJ/ke17ZwdGBToddI8pDm48kHLiAMEEMQDM76tQyRpIIg17gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z5QHyNOqBUUEtDDsRWrJLTmnhbJtrfwp8bfXu9iW6Tjn7C_3AHyGAAQIRTc8e8HE5EqiurBLwmJjKjNnB4mrT8N/Snake+Chart+-+2020+-+Election+-+Forecast+-+FiveThirtyEight.jpg)

---
![bg opacity:0.1](https://mediashift.org/wp-content/uploads/2015/07/dviz.png)
# General tips and tricks
- Tufte's data-to-ink ratio principle
- Optimize for intuition and readability
- Use consistent color schemes to highlight connections
- Use of visual weight across figure elements
- **Be willing to break all of the rules!**
