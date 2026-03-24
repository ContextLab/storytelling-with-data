---
marp: true
theme: cdl-theme
math: katex
---

![bg opacity:0.1](https://mediashift.org/wp-content/uploads/2015/07/dviz.png)
# Data visualization: approaches to creating effective figures
## Jeremy R. Manning
### PSYC 81.09: Storytelling with Data

---

## On the nature of data and data comprehension

<div class="note-box" data-title="Key idea">

A dataset is just a **collection of values** (numbers, text, etc.). In principle we could display those raw values to our audience, but that's usually ineffective at conveying the **specific message** we want to get across.

</div>

---

## Which is clearest to you?
![height:500px](https://miro.medium.com/max/693/1*bV7S0zACdidh11ikjYpLpQ.png)

---

## Why visualize data?

<div class="important-box" data-title="The power of vision">

- Our visual systems **rapidly process massive amounts of information** and are adept at **pattern recognition**
- We can leverage the visual system to convey patterns in data
- Conveying the patterns we want people to perceive means figuring out how to **turn data into pictures**

</div>

---

## Anscombe's quartet

<div class="warning-box" data-title="Statistics can't tell the whole story">

These four datasets have identical summary statistics, but look very different when plotted!

</div>

![height:400px](https://seaborn.pydata.org/_images/anscombes_quartet.png)

---

## The Datasaurus Dozen

<div class="warning-box" data-title="Same statistics, wildly different shapes">

Another striking example of why visualization matters.

</div>

![height:350px](https://blog.revolutionanalytics.com/downloads/DataSaurus%20Dozen.gif)

---

## Grammar of graphics: intuition

<div class="definition-box" data-title="Grammar of graphics">

A language for describing *all* possible figures. The main idea is to **separate data from how we visualize it**. This can be a useful framework for thinking about data visualization.

</div>

---

<!-- _class: scale-90 -->

## Grammar of graphics: layers

<div class="note-box" data-title="Figures comprise seven layers">

- **Data**: what information (values) we'll be plotting
- **Aesthetics**: mapping from data into a "data representation space"
- **Geometries**: what shapes can be used to represent the data
- **Facets**: define subplots (groupings) of the data
- **Statistics**: define statistical models and summaries
- **Coordinates**: maps coordinates in data space onto the figure
- **Theme**: any non-data elements of the figure

</div>

---

## Grammar of graphics: takeaways

<div class="tip-box" data-title="Practical takeaway">

Even if you never use GoG tools explicitly, it's useful to consider what the **separable elements** of figures are and how they affect the figure's appearance.

</div>

---

## Considerations for deciding how to display data

<div class="note-box" data-title="Key questions">

- Do you want to display the raw values or a summary (or both)?
- Are the observations discrete or continuous?
- What patterns in the data do you want to explore or emphasize?
- **What message do you want your audience to take away?**

</div>

---

<!-- _class: scale-90 -->

## Approaches to displaying data

<div style="display: flex; gap: 2em;">
<div>

<div class="note-box" data-title="Basic approaches">

- **Raw data**: show individual datapoints
- **Summaries**: highlight trends or patterns
- **Combinations**: show both raw data *and* trends
- **Polar plots**: circular data

</div>

</div>
<div>

<div class="note-box" data-title="Advanced approaches">

- **Clustering**: display groupings in data
- **Timeseries**: show changes over time
- **Networks**: links between datapoints
- **Geospatial**: geographic maps
- **Animations**: movement conveys information

</div>

</div>
</div>

---

![bg opacity:0.1](https://mediashift.org/wp-content/uploads/2015/07/dviz.png)
# Displaying "raw" data
### Directly map each observation onto a single point or shape

---

## Table
![height:450px](figs/table.png)

---

## Bar graph
![height:500px](https://seaborn.pydata.org/_images/barplot_1_0.png)

---

## Bar graph (grouped)
![height:500px](https://seaborn.pydata.org/_images/grouped_barplot.png)

---

## Bar graph (stacked)
![height:500px](figs/bar_stacked.png)

---

## Scatterplot (2D)
![height:500px](https://seaborn.pydata.org/_images/scatterplot_3_0.png)

---

## Scatterplot (3D)
![height:500px](figs/scatter3D.png)

---

## Heatmap
![height:500px](https://seaborn.pydata.org/_images/seaborn-heatmap-1.png)

---

## Volume plot
![height:450px](https://www.mathworks.com/matlabcentral/mlc-downloads/downloads/submissions/36139/versions/8/screenshot.jpg)

---

![bg opacity:0.1](https://mediashift.org/wp-content/uploads/2015/07/dviz.png)
# Summaries
### Characterize overarching trends or patterns without showing individual datapoints

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
![height:500px](figs/quiver_plot.png)

---

## Streamline plot
![height:500px](figs/streamplot.png)

---

![bg opacity:0.1](https://mediashift.org/wp-content/uploads/2015/07/dviz.png)
# Combination plots
### Show both the individual datapoints *and* the summary in a single plot

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
# Polar plots
### Display circular (angular) data, or visualize summaries using polar coordinates

---

## Polar area chart (AKA Coxcomb chart, Rose chart)
![height:500px](https://i.stack.imgur.com/gxPwy.png)

---

## Pie chart
![height:500px](figs/pie_chart.png)

---

## Target (bullseye) plot
![height:500px](https://ggplot2.tidyverse.org/reference/coord_polar-4.png)

---

![bg opacity:0.1](https://mediashift.org/wp-content/uploads/2015/07/dviz.png)
# Clustering
### Emphasize or display groupings in the data

---

## Dendrogram
![height:500px](https://www.data-to-viz.com/graph/dendrogram_files/figure-html/unnamed-chunk-3-1.png)

---

## Clustermap
![height:500px](https://seaborn.pydata.org/_images/seaborn-clustermap-1.png)

---

![bg opacity:0.1](https://mediashift.org/wp-content/uploads/2015/07/dviz.png)
# Timeseries data
### Show changes over time

---

## Line plot
![height:500px](https://seaborn.pydata.org/_images/wide_data_lineplot.png)

---

## Ribbon plot
![height:500px](https://seaborn.pydata.org/_images/errorband_lineplots.png)

---

![bg opacity:0.1](https://mediashift.org/wp-content/uploads/2015/07/dviz.png)
# Networks
### Highlight physical or conceptual links between datapoints

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
# Geospatial data
### Geographic maps (locations, addresses, GPS coordinates, etc.)

---

## Map projections
![height:400px](https://imgs.xkcd.com/comics/map_projections.png)

Also see [Wikipedia: List of map projections](https://en.wikipedia.org/wiki/List_of_map_projections)

---

## Choropleth map
![height:500px](figs/cloropleth.png)

---

## Bubble map
![height:500px](figs/bubble_map.png)

---

## Geographical line plot
![height:500px](figs/lineplot_map.png)

---

![bg opacity:0.1](https://mediashift.org/wp-content/uploads/2015/07/dviz.png)
# Animations
### Use movement to convey additional information

---

## Uber trips in New York City
![height:500px](figs/uber_trips_timelapse.gif)

---

## Yearly life expectancy vs. GDP throughout the world
![height:500px](figs/gapminder.gif)

---

## Brain-decoded thoughts from different people listening to a story
![height:450px](https://hypertools.readthedocs.io/en/latest/_images/hypertools.gif)

---

![bg opacity:0.1](https://mediashift.org/wp-content/uploads/2015/07/dviz.png)
# Classics

---

## Periodic table
![height:500px](figs/periodic_table.png)

---

## Minard's map of Napoleon's Russian campaign
![height:500px](https://upload.wikimedia.org/wikipedia/commons/2/29/Minard.png)

---

## FiveThirtyEight's electoral votes depictions
![height:500px](https://images.squarespace-cdn.com/content/v1/5bfc8dbab40b9d7dd9054f41/1599947028927-DT85T3QZVWTYV9DDCSAJ/ke17ZwdGBToddI8pDm48kHLiAMEEMQDM76tQyRpIIg17gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z5QHyNOqBUUEtDDsRWrJLTmnhbJtrfwp8bfXu9iW6Tjn7C_3AHyGAAQIRTc8e8HE5EqiurBLwmJjKjNnB4mrT8N/Snake+Chart+-+2020+-+Election+-+Forecast+-+FiveThirtyEight.jpg)

---

## General tips and tricks

<div class="tip-box" data-title="Design principles">

- Tufte's **data-to-ink ratio** principle
- Optimize for **intuition and readability**
- Use consistent color schemes to highlight connections
- Use visual weight across figure elements
- **Be willing to break all of the rules!**

</div>
