# Project information

Author: Kate Marine 
Username: kate-marine

# Overview

Main question: what it would look like to build something that lets a language model actually do data analysis, instead of just write code for someone else to run?

For this project I designed and built an MCP server that lets clients such as LLMs upload data, define visualizations, and retrieve resutlts as part of a contextual workflow. It was originally part of a project for the DALI lab, but I expanded it to explore more practical applications. When working with an LLM on a dataset, such as like I have been doing with earlier data stories projects, it can produce great code snippets, but I still have to run everything in a notebook and continuously communicate back and forth into the chat (before I started doing Claude code).
Instead of asking Claude to generate code, an MCP client can call a tool that actually does the thing, such as loading a dataset or rendering a chart and gets the result back inline. My server exposes a bunch tools organized into four categories: dataset operations (upload, describe, list), transforms (filter, aggregate, sort, select columns), visualization specifications (create, suggest, update chart definitions), and rendering (generate PNG or interactive HTML plots). I built it in Python using FastMCP for the protocol layer, pandas for data manipulation, matplotlib for static charts, and Plotly for interactive ones.

The most important design decision was making every object the server creates (such as datasets, chart specs, rendered plots) addressable by a unique ID, so that any follow-up call can reference earlier work without having to re-upload anything. For example when a user wants to now filter to just Boston store locations and regenerate the plot, the client doesn't need to send the dataset again it just passes the ID. 
For the actually story part, I wanted to show how the server could actually be used in a somewhat real world scenario. The data is a simulated coffee sales dataset that I was using for testing. It includes twelve months of revenue, customers, ratings, and marketing spend across six cities. The main point of the story wasn't to actually emphasize the findings themselves (because it’s just simulated) but to show how the tool could be used in a real kind of iterative analysis workflow.

The biggest limitation I ran into was that suggest_vizspec (tool that is supposed to interpret plain English chart requests but didn’t end up finishing) can pick the right plot type but doesn't know to chain in a aggregate_dataset call when the request implies it. For example asking for "total revenue by city" is a single spoken phrase but implies two server-side operations, and means letting tools call other tools which I didn’t have time to implement.

See DESIGN.md for more in depth explanation of server itself and data-mcp-2 for full repo just for the mcp itself




Upload a movie of your data story to YouTube and include a link here.  You can narrate over a screencast of you scrolling through your notebook, or you can paste your figures into a Powerpoint or Keynote presentation (or similar).  You may also find [Marp](https://yhatt.github.io/marp/) useful; it's what I'm using to generate the slideshows for [Modules 1--4](https://github.com/ContextLab/storytelling-with-data/blob/master/slides/outline.md).  (Sample slides [here](https://github.com/ContextLab/storytelling-with-data/blob/master/slides/modules_and_numpy.md) and [here](https://github.com/ContextLab/storytelling-with-data/blob/master/slides/pandas.md).)

# Downloading the data

Provide a link to the dataset(s) you're using for the project, along with a brief description of the data.

# Running the code

Describe, in sufficient detail for a new person (moderately competent but unfamiliar with your work) to follow, how to run your code.  If the project is implemented in one or more Colaboratory notebooks, you should provide a link to the notebook(s) here.  Also copy the notebooks (as .ipynb files) into your project folder so that everything related to your project is backed up on GitHub.

# Contributing to the code

Tell other people how they can contribute to the project you've started.  Specifically:
- What are the most obvious next steps?
- What are some questions that your work raises?
- What challenges remain?
- Are there any known bugs or problems with your approach that someone continuing your project should be aware of?

# Acknowledgements

If your idea is based on or inspired by someone else's work (either their code or their ideas), cite them and provide links to their work.  Also, if you received help or support from someone who is not listed as an author on this project, you should acknowledge them here.


Project information: project name, authors, GitHub usernames
Overview: main question, approach, data used, tools used, key findings
YouTube link: a link to your 5-minute data story video
Data links: where to find the data you analyzed
Running the code: instructions for replicating your results
Contributing: next steps, open questions, known issues
Acknowledgements and citations
