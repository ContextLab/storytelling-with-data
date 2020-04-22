---
title: Intro to Pandas
description: Introduction to Pandas
url: https://github.com/ContextLab/storytelling-with-data
theme: uncover
class:
  - lead
---

![bg opacity:0.1](https://miro.medium.com/max/1080/1*_oSOImPmBFeKj8vqE4FCkQ.jpeg)
# Introduction to Pandas: PythoN Data AnalysiS toolkit
## Jeremy R. Manning
### PSYC 81.09: Storytelling with Data

---
# Pandas = NumPy + :star2:

- NumPy `array` objects organize information into tables
- Pandas introduces `Series` and `DataFrame` objects, which are like enhanced versions of `array`
- Pandas also includes a bunch of functions for reading in common filetypes like .csv, .xlsx, .json, .html, and many others

---
# Installing Pandas
- Pandas is installed by default in Colaboratory
- You can install it in other environments using
```bash
pip install pandas
```

---
### Importing Pandas into your workspace (follow along in a notebook!)

```python
import pandas as pd
```

---
## `Series` objects: 1-D array of indexed data

```python
>>> data = pd.Series([0.25, 0.5, 0.75, 1.0])
>>> data
0    0.25
1    0.50
2    0.75
3    1.00
dtype: float64
```

---
## `Series` objects: 1-D array of indexed data

```python
>>> data.values
array([ 0.25,  0.5 ,  0.75,  1.  ])

>>> data.index
RangeIndex(start=0, stop=4, step=1)

>>> data[2]
0.75

>>> data[1:3]
1    0.50
2    0.75
dtype: float64
```

---
### Defining indices
- By default, `Series` objects are indexed by integers
- You can specify arbitrary indices as follows:
```python
>>> data = pd.Series([0.25, 0.5, 0.75, 1.0],
                 index=['a', 'b', 'c', 'd'])
>>> data
a    0.25
b    0.50
c    0.75
d    1.00
dtype: float64
```
---
### Defining indices
- This allows `Series` objects to act like a more powerful version of `dict`

```python
>>> data['a']
0.25

>>> data['a':'c']
a    0.25
b    0.50
c    0.75
dtype: float64
```

---
### `DataFrame`: a more powerful `array`
- A `DataFrame` is like a 2D `array`, but with the rows and columns labeled
- Rows labels are called the `index`
- Column labels are called the `columns`

---
### `DataFrame`: a more powerful `array`
```python
>>> areas = {'California': 423967,
             'Texas': 695662,
             'New York': 141297,
             'Florida': 170312,
             'Illinois': 149995}
>>> populations = {'California': 38332521,
                   'Texas': 26448193,
                   'New York': 19651127,
                   'Florida': 19552860,
                   'Illinois': 12882135}
```

---
### `DataFrame`: a more powerful `array`
```python
>>> states = pd.DataFrame({'population': populations, 'area': areas})
>>> states
            population    area
California    38332521  423967
Texas         26448193  695662
New York      19651127  141297
Florida       19552860  170312
Illinois      12882135  149995
```

---
### `DataFrame`: a more powerful `array`
```python
>>> states.index
Index(['California', 'Texas', 'New York', 'Florida', 'Illinois'], dtype='object')

>>> states.columns
Index(['population', 'area'], dtype='object')

>>> states.values
array([[38332521,   423967],
       [26448193,   695662],
       [19651127,   141297],
       [19552860,   170312],
       [12882135,   149995]])
```
