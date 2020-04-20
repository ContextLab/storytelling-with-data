---
title: Python external modules and intro to numpy
description: Intro to data science with Python
url: https://github.com/ContextLab/storytelling-with-data
theme: gaia
class:
  - invert
  - lead
---

![bg opacity:0.1](https://miro.medium.com/max/1000/0*H-KlSZBvm_6tzGGH.png)
# Python external modules and introduction to NumPy
## Jeremy R. Manning
### PSYC 81.09: Storytelling with Data

---
# What's a Python module?

- A Python *module* is a package that provides access to **functions**, **variables**, and **data** within your workspace.
- Modules extend the *Python standard library*.
- Modules are kind of like Python's *apps*.

---
# Which Python modules can you use?
- There are two types of modules you can use in your Python programs: built-in modules and modules that you install using `pip`, which is like Python's app store.
- A list of built-in modules may be found [here](https://docs.python.org/3/library/).
- There are hundreds of thousands of installable modules.  Googling what you're looking for is a good place to start.  Or you can do a search [here](https://pypi.org/).

---
# How do you install new modules?

- The easiest way to install Python modules on your local machine is using the [`pip` command](https://pypi.org/project/pip/) from within Terminal:
```bash
pip install --user hypertools
```
- Within a Colaboratory notebook you can call Terminal commands (including `pip`) by putting a `!` in front of the command in a code cell:
```bash
!pip install timecorr
```

---
# Which modules are installed in your environment?

- To get a list of the (many!) already-installed modules from within Colaboratory, type:
```bash
!pip freeze
```
- In a "regular" Terminal session (e.g., on your local machine), just omit the `!`

---
# Use `import` statements to gain access to new modules in your workspace

```python
import itertools
import os, sys
import numpy as np
from math import log
from glob import glob as lsdir
```

---
# Creating your own packages (modules)

- You probably won't write or publish your own packages in this course.
- But, in case you want to see how packages are made, [here](https://github.com/ContextLab/CDL-tutorials/tree/master/packages) is my lab's tutorial for writing one (and making it installable via `pip`).

---
# Modules give Python its **data science superpowers**

- Python is a nice language, but many others are nice too
- Python's enormous library of installable packages is why Python stands out

---
# Python has excellent libraries for...
- **Wrangling data**: getting the data from the format it's in to the format you need it in
- **Analyzing data**: carrying out statistical tests, machine learning
- **Modeling data**: fitting existing models to your data and/or implementing your own models
- **Visualizing data**: creating figures
- ...and nearly anything else you can imagine!

---
### (Part of the) Python data science computing stack

![height:550px](https://raw.githubusercontent.com/jeremymanning/storytelling-with-data/master/slides/figs/python_libraries.png)

---
# Data wrangling
- Real-world datasets are often messy:
  - Missing or inconsistent data
  - Organized in ways that are difficult or inefficient to work with
- The point of data wrangling tools is to make data easier and more efficient to work with


---
![bg height:500 opacity:0.1](https://cdn-images-1.medium.com/fit/t/1600/480/1*cyXCE-JcBelTyrK-58w6_Q.png)
# NumPy: efficiently storing and manipulating data
- NumPy stands for NUMerical PYthon.  **It's the foundation of nearly every data science tool and analysis in Python.**
- Introduces a new type of object called an `array` (plus some others).  These objects store *n*-dimensional tables of numbers (i.e., vectors, matrices, and tensors).
- Also introduces a bunch of functions for efficiently working with `array` objects, and with lots of other useful linear algebra and calculus functions, random number generators, etc.
- Official tutorials and documentation may be found [here](https://numpy.org/doc/stable/user/quickstart.html).

---
![bg height:500 opacity:0.1](https://cdn-images-1.medium.com/fit/t/1600/480/1*cyXCE-JcBelTyrK-58w6_Q.png)
# NumPy: basic usage
- Open up a scratch notebook in Colaboratory and follow along!
```python
import numpy as np

>>> a = np.array([1, 2, 3])
>>> a
array([1, 2, 3])
>>> a + 2
array([3, 4, 5])
```

---
![bg height:500 opacity:0.1](https://cdn-images-1.medium.com/fit/t/1600/480/1*cyXCE-JcBelTyrK-58w6_Q.png)
# Some useful functions for querying `array` objects (try them!)
- `a.ndim`: the number of axes (dimensions) of the array
- `a.shape`: returns a `tuple` indicating the size of the array in each dimension
- `a.size`: the total number of elements in the array
- `a.dtype`: the data type of the array's elements

---
![bg height:500 opacity:0.1](https://cdn-images-1.medium.com/fit/t/1600/480/1*cyXCE-JcBelTyrK-58w6_Q.png)
# Some useful functions for manipulating `array` objects (part 1)
- `a.reshape`: reshapes the array into a new array of the given size
- Slicing: `array` objects support slice notation similar to `list` objects.  NumPy `array` objects may be sliced along each dimension simultaneously.
- `np.ravel`: flattens the `array` into a 1-D vector

---
![bg height:500 opacity:0.1](https://cdn-images-1.medium.com/fit/t/1600/480/1*cyXCE-JcBelTyrK-58w6_Q.png)
# Some useful functions for manipulating `array` objects (part 2)
- `np.repeat`, `np.tile`: repeat elements of an array, or copy the entire array and merge with itself
- `np.vstack`, `np.hstack`, `np.stack`, `np.concatenate`, `np.block`: combine multiple arrays
- `np.hsplit`, `np.vsplit`, `np.dsplit`, `np.split`: split an array into parts
- `a.sort`: returns a sorted copy of `a`

---
![bg height:500 opacity:0.1](https://cdn-images-1.medium.com/fit/t/1600/480/1*cyXCE-JcBelTyrK-58w6_Q.png)
# Some other commonly used `numpy` functions (part 1)
- `np.arange`: works like the `range` function, but returns an `array` object
- `np.linspace`, `np.logspace`, `np.mgrid`, `np.ogrid`: create `array`s of linearly (or logarithmically) spaced values
- `np.zeros` and `np.ones`: produce an `array` of the given size, filled with all 0s or 1s
- `np.zeros_like`, `np.ones_like`: produce an `array` of the same size as the input, but filled with 0s or 1s

---
![bg height:500 opacity:0.1](https://cdn-images-1.medium.com/fit/t/1600/480/1*cyXCE-JcBelTyrK-58w6_Q.png)
# Some other commonly used `numpy` functions (part 2)
- Many standard math and stats functions you might expect
  - `np.sin`, `np.cos`, `np.exp`, `np.sqrt`, `np.dot`, `np.outer`, `np.mean`, `np.std`, etc.
  - These all operate on `array` objects, but can also be used for other built-in datatypes like `int` and `float`.
- `np.random.rand`, `np.random.randn`, `np.random.randint`: generate random numbers.
- `np.random.choice`: choose random element(s) from a 1D `array`.

---
![bg height:500 opacity:0.1](https://cdn-images-1.medium.com/fit/t/1600/480/1*cyXCE-JcBelTyrK-58w6_Q.png)
# Some other commonly used `numpy` functions (part 3)
- `a.all()`: `True` iff *every* element of the array is `True`
- `a.any()`: `True` iff *any* element of the array is `True`
- `a.argmax`, `a.argmin`: return the max or min values (potentially along each dimension)
- `a.cumsum`, `a.cumprod`: return an array of the same size as `a`, but storing the cumulative sum or product of each successive element of `a` along the given dimension

---
![bg height:500 opacity:0.1](https://cdn-images-1.medium.com/fit/t/1600/480/1*cyXCE-JcBelTyrK-58w6_Q.png)
## Some strange NumPy stuff
- When you slice an array, it returns a *pointer* to the original data, called a `view`.
- If you change the data in the original array, the values in the slice will change too.
- If you don't want this to happen, use `copy`:
  - `a.copy()`: creates a new `array` with the same data
- If you're finding that your data is being changed in strange ways, a good thing to check first is that you're dealing with `array` objects correctly.
- Only copy data when you need too-- otherwise you'll be wasting memory by storing redundant copies of the same thing.

---
![bg height:500 opacity:0.1](https://cdn-images-1.medium.com/fit/t/1600/480/1*cyXCE-JcBelTyrK-58w6_Q.png)
# Practicing NumPy: basics
- Create an `array` of ones with 10 rows and 5 columns
- Create a 4 by 7 `array` of random integers between 6 and 30
  - Find the rows and columns of all values greater than 10
  - Write a function that checks if any of the values are equal to 30.
    - If so, the function should print "The array contains at least 1 30!"
    - If not, the function should print "No 30s were found"
    - Then return the number of times 30 appeared in the array

---
## Practicing NumPy: broadcasting and loops
- Create an `array` containing the first 10 cubes (i.e., 1, 8, 27, etc.)
- Create a function that returns an `array` containing the square roots of `n` evenly spaced values between to integers, `x` and `y`.  (Your function should accept 3 inputs: `x`, `y`, and `n`.)
- Create a 3 by 4 by 5 `array` of random numbers chosen uniformly between 0 and 1.
  - Sort the values in ascending order and reshape the `array` into a new 20 by 30 `array`
  - Print out the 10th row
  - Print out rows 5 through 9 (inclusive) of columns 20 through 25

---
## Practicing NumPy: manipulating matrices
- Create two `array` objects, each filled with random draws from the unit Gaussian distribution:
  - `a` should be 5 by 7
  - `b` should be 10 by 7
- Create a new `array`, `c`, comprising `a` stacked on top of `b`
- Reshape `c` into a column vector
- Create a new `array`, `d`, comprising `c` stacked horizontally 5 times
- Create a new `array`, `e`, that repeats each element of `d` 2 times in a row (it should have twice as many rows and columns as `d`)

---
# Closing thoughts and things to consider
- Most (all?) data may be represented as matrices, so `array` objects are highly generalizable.
- Suppose you had a dataset, like a huge spreadsheet of measurements.  How could you use NumPy to start understanding your data?
- Think about what is or isn't *intuitive* about NumPy.  Why might things have been set up the way they are?  Can you articulate any points of confusion?
