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

See DESIGN.md for more in depth explanation of server itself and [data-mcp-2](https://github.com/kate-marine/data-visualization-mcp-server) for the full repo of for the mcp server 


**Video link:** https://youtu.be/ghtawmGFPXc


## Downloading the data

See csv. It's super small, used just to test the MCP tools which were the main focus of this project

# Running the code

See [data-mcp-2 ](https://github.com/kate-marine/data-visualization-mcp-server) for full code repo.

Describe, in sufficient detail for a new person (moderately competent but unfamiliar with your work) to follow, how to run your code. 

# Contributing to the code

Tell other people how they can contribute to the project you've started.  Specifically:
- What are the most obvious next steps?
- What are some questions that your work raises?
- What challenges remain?
- Are there any known bugs or problems with your approach that someone continuing your project should be aware of?

# Acknowledgements

Original MCP server was built based on an application prompt from the DALI lab. Here is link: https://dalilab.notion.site/Data-Challenge-2b3ecf13c9e14ce18932c95b095519a3 



