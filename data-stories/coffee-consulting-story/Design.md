# Design Document 

## Overview

An MCP server that gives clients (currently testing with Claude Desktop) the ability to work with data. A client can upload a dataset, describe how they want it visualized, and get a chart back with tool calls in a normal conversation.

---

## Work process


1. Client uploads dataset (CSV)
    
2. Server stores dataset with id

3. Client requests a chart 

4. Server creates a VizSpec with an id 

5. Client calls generate_plot

6. Server creates PNG (HTML if asked for)


Note: Every object the server creates has a unique ID, and subsequent calls reference that ID. Allows a multi-turn conversation to build on earlier steps without re-uploading data.

---

## Files and tools


**main.py** - Initialize the server and register all tools and resources


**datasets.py**    — tools to upload, describe, list datasets
**transforms.py**  — tools filter, aggregate, sort, and select columns
**specs.py**       — tools to create, update, suggest visualization specs
**plots.py**       — tools to generate, retrieve, and list plots

**renderer.py**      — renders static PNG visualizations using Matplotlib (takes a pandas DataFrame and VizSpec and generates a static PNG image based on plot type)

**interactive.py**   — renders interactive HTML visualizations using Plotly Express

**store.py**             — manages in-memory caching with SQLite backend for datasets and visualization specs, and in-memory storage for rendered plots
**models.py**           — defines the data models for the server using Pydantic
**server.py**           - sets up logging, creates the FastMCP server instance, initializes the in-memory store


Note: All tools share a single `ResourceStore` instance. State is never passed between tools directly it's only through IDs.

---

## Data model

Classes that define the data the server works with

| Object | What it represents | Key fields |
|--------|--------------------|------------|
| **Dataset** | Uploaded tabular data | id, name, columns, row_count |
| **VizSpec** | chart instructions | dataset_id, plot_type, x_column, y_column, color_by |
| **Plot** | rendered output | spec_id, has_html |

The actual DataFrame is stored separately alongside the Dataset (pydantic can't serialize it)

---

## Tools 

### Dataset tools
| Tool | Description |
|------|-------------|
| `upload_dataset` | Upload a CSV as a raw string; returns a dataset ID |
| `upload_dataset_from_path` | Load a CSV directly from a file path on disk |
| `describe_dataset` | Per-column stats: mean/min/max/std for numeric, unique count and top values for categorical |
| `list_datasets` | List all datasets currently in the store |
| `get_dataset` | Retrieve metadata for a specific dataset by ID |

### Transform tools
| Tool | Description |
|------|-------------|
| `filter_dataset` | Keep rows matching a condition; returns a new dataset ID |
| `aggregate_dataset` | Group by a column and apply a function; returns a new dataset ID |
| `sort_dataset` | Reorder rows by a column ascending/descending; returns a new dataset ID |
| `select_columns` | Drop unwanted columns; returns a new dataset ID |

### Visualization spec tools
| Tool | Description |
|------|-------------|
| `create_vizspec` | Create a chart instructions: specify dataset, plot type, x/y columns, optional color/grouping |
| `suggest_vizspec` | Create a VizSpec from a plain English description; returns the spec plus `reasoning` and `confidence` fields |
| `update_vizspec` | Modify fields on an existing VizSpec (plot type, columns, labels, color, etc.) |
| `get_vizspec` | Retrieve a VizSpec by ID |
| `list_vizspecs` | List all VizSpecs in the store |

### Plot tools
| Tool | Description |
|------|-------------|
| `generate_plot` | Render a VizSpec into a PNG (optionally store HTML) |
| `get_plot` | Retrieve a previously rendered plot;  returns the image |
| `list_plots` | List all rendered plots in the store |
| `list_plot_types` | List all supported plot type names |


## Limitations

- **No authentication.** Any client with access to the server can read all data.
- **In-memory during runtime.** Very large datasets will consume RAM proportionally.
- **No multi-series y-columns.** A VizSpec has one y_column. Plotting two metrics on the same chart requires two separate specs.
- **Aggregate intent in suggest_vizspec.** "Total revenue by city" implies aggregation, but `suggest_vizspec` only creates a VizSpec — the caller must run `aggregate_dataset` first.
- **Fuzzy column matching has a cutoff.** Conceptual synonyms ("revenue" for a column named "sales") won't match.
