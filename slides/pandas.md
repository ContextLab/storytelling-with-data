---
title: Intro to Pandas
description: Introduction to Pandas
url: https://github.com/ContextLab/storytelling-with-data
theme: gaia
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.jpg')
class:
  - lead  
---

![bg opacity:0.1](https://miro.medium.com/max/1080/1*_oSOImPmBFeKj8vqE4FCkQ.jpeg)
# Introduction to Pandas: **P**ytho**n** **d**ata **a**nalysi**s** toolkit
## Jeremy R. Manning
### PSYC 81.09: Storytelling with Data

---
### Python data science computing stack

![height:500px](https://raw.githubusercontent.com/jeremymanning/storytelling-with-data/master/slides/figs/python_libraries.png)

---
### Pandas = NumPy + :star2:

- NumPy `array` objects organize information into tables
- Pandas introduces `Series` and `DataFrame` objects, which are like enhanced versions of `array`
- Pandas includes a bunch of functions for creating `DataFrame` objects from common filetypes like .csv, .xlsx, .json, .html, and many others
- The toolbox also includes some (basic) statistical analysis and plotting functions

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
Index(['California', 'Texas', 'New York', 'Florida',
       'Illinois'], dtype='object')

>>> states.columns
Index(['population', 'area'], dtype='object')

>>> states.values
array([[38332521,   423967],
       [26448193,   695662],
       [19651127,   141297],
       [19552860,   170312],
       [12882135,   149995]])
```

---
### Indexing `DataFrame` objects
```python
>>> states['area']
California    423967
Florida       170312
Illinois      149995
New York      141297
Texas         695662
Name: area, dtype: int64
```

---
### Indexing `DataFrame` objects
```python
>>> states['California']
----------------------------------------------------------

KeyError                 Traceback (most recent call last)
...
...
KeyError: 'California'
```

---
### Indexing `DataFrame` objects
```python
>>> states.loc['California']
population    38332521
area            423967
Name: California, dtype: int64

>>> type(states.loc['California'])
pandas.core.series.Series
```

---
### Indexing `DataFrame` objects
```python
>>> states.iloc[1:3]
population    area
Texas       26448193  695662
New York    19651127  141297
```

---
### Adding columns to `DataFrame` objects
```python
>>> states['density'] = states['population'] / states['area']
>>> states
            population    area     density
California    38332521  423967   90.413926
Texas         26448193  695662   38.018740
New York      19651127  141297  139.076746
Florida       19552860  170312  114.806121
Illinois      12882135  149995   85.883763
```

---
### Modifying values of `DataFrame` objects
```python
>>> states.loc['California', 'population'] += 1
>>> states
            population    area     density
California    38332522  423967   90.413926
Texas         26448193  695662   38.018740
New York      19651127  141297  139.076746
Florida       19552860  170312  114.806121
Illinois      12882135  149995   85.883763
```

---
### Let's get some data!
```python
>>> cars = pd.read_csv('https://tinyurl.com/ydevw29o')
>>> cars.head()
    mpg  cylinders  displacement  ...                      name
0  18.0          8         307.0  ... chevrolet chevelle malibu
1  15.0          8         350.0  ...         buick skylark 320
2  18.0          8         318.0  ...        plymouth satellite
3  16.0          8         304.0  ...             amc rebel sst
4  17.0          8         302.0  ...               ford torino

[5 rows x 9 columns]
```

---
### Data summaries with `pandas.describe`

```python
>>> cars.describe()
              mpg   cylinders  ...  acceleration  model_year
count  398.000000  398.000000  ...    398.000000  398.000000
mean    23.514573    5.454774  ...     15.568090   76.010050
std      7.815984    1.701004  ...      2.757689    3.697627
min      9.000000    3.000000  ...      8.000000   70.000000
25%     17.500000    4.000000  ...     13.825000   73.000000
50%     23.000000    4.000000  ...     15.500000   76.000000
75%     29.000000    8.000000  ...     17.175000   79.000000
max     46.600000    8.000000  ...     24.800000   82.000000

[8 rows x 7 columns]
```

---
### Some other useful functions to explore (part 1)
- `groupby`: organize data according to particular values (e.g., group cars by model year)
- `fillna`, `ffill`, `bfill`: deal with missing data
- `rolling`: compute averages over a sliding window
- `merge`, `join`: combine multiple `DataFrame` objects
- `melt`: restructure `DataFrame` to have just two columns-- `variable` and `value`

---
### Some other useful functions to explore (part 2)
- `head`, `tail`: print out just the first (or last) rows
- `apply`: apply a function to each value along a given axis
- `plot`: create figures (lots of options!)

---
## Summary
- Pandas is a powerful tool for organizing and manipulating data
- The more Pandas "tricks" you learn, the more efficiently you'll be able to work with data
  - NumPy tricks also come in handy; most work in Pandas too!
- The best way to learn is to load some real data into a `DataFrame` and start playing around with it
