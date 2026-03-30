---
marp: true
theme: cdl-theme
math: katex
transition: fade 0.25s
author: Contextual Dynamics Lab
---

# Introduction to Python
## Jeremy R. Manning
### PSYC 81.09: Storytelling with Data

---

## What is a Jupyter notebook?

<div class="definition-box" data-title="Jupyter notebooks">

An interactive tool that lets you combine **notes**, **executable code**, and **figures** in a single, shareable document. Notebooks comprise a series of **cells**:

- **Markdown cells**: formatted text (like a word processor)
- **Code cells**: Python instructions that the computer executes

</div>

<div class="tip-box" data-title="Running cells">

Hold `Shift` and press `Enter` to run a cell.

</div>

---

## Python as a calculator

<div class="note-box" data-title="Arithmetic expressions">

You can type mathematical expressions and Python will evaluate them, just like a calculator.

</div>

```python
1 + 1        # 2
3 * (4 + 1)  # 15
```

<div class="warning-box" data-title="Floating point quirks">

Python represents numbers in binary internally, which can produce surprising results:

```python
0.3 - 0.2 - 0.1  # -2.78e-17, not 0!
```

</div>

---

## Variables

<div class="definition-box" data-title="What is a variable?">

A **variable** is a named object with a particular value. Use the **assignment operator** (`=`) to create one: the name goes on the left, the value on the right.

</div>

```python
x = 3
y = 4
x + y  # 7
```

<div class="tip-box" data-title="Why use variables?">

Abstracting values into named variables lets you reuse the same code with different inputs.

</div>

---

## Operators

<div class="note-box" data-title="Arithmetic operators">

| Operator | Meaning | Example |
|-|-|-|
| `+` | Addition | `3 + 2` &rarr; `5` |
| `-` | Subtraction | `3 - 2` &rarr; `1` |
| `*` | Multiplication | `3 * 2` &rarr; `6` |
| `/` | Division | `7 / 2` &rarr; `3.5` |
| `**` | Exponentiation | `3 ** 2` &rarr; `9` |

</div>

---

## Logical and equality operators

<div class="definition-box" data-title="Logical operators">

Logical operators work on **Boolean** values (`True` / `False`):

| Operator | Meaning |
|-|-|
| `or` | `True` if *either* operand is `True` |
| `and` | `True` if *both* operands are `True` |
| `not` | Flips `True` to `False` and vice versa |

</div>

<div class="important-box" data-title="Equality operator">

Use `==` (not `=`) to **test** whether two values are equal. The result is a `bool`.

</div>

---

## Comments and `print`

<div class="note-box" data-title="Documenting your code">

- **Inline comments**: start with `#`
- **Block comments**: enclosed in triple quotes (`'''` or `"""`)

</div>

```python
pi = 3.14159265359  # ratio of circumference to diameter
r = 6               # radius

area = pi * r ** 2
print(area)          # 113.097...
```

---

## Data types

<!-- _class: scale-90 -->

<div class="definition-box" data-title="Common Python data types">

| Type | Description | Example |
|-|-|-|
| `int` | Integer | `42` |
| `float` | Decimal number | `3.14` |
| `bool` | Boolean | `True`, `False` |
| `str` | String (text) | `'hello'` |
| `list` | Ordered collection | `[1, 'a', 3.0]` |
| `dict` | Key-value pairs | `{'name': 'Ada'}` |
| `None` | Null / no value | `None` |

</div>

<div class="tip-box" data-title="Typecasting">

Convert between types: `float(3)` &rarr; `3.0`, `str(42)` &rarr; `'42'`, `int('7')` &rarr; `7`. Use `type(x)` to check a value's type.

</div>

---

## `if` / `elif` / `else`

<div class="definition-box" data-title="Conditional execution">

Run different code depending on whether a condition is `True` or `False`.

</div>

```python
my_name = 'Jeremy Manning'

if my_name == 'Jeremy Manning':
    print('You are the course instructor.')
elif my_name == 'Marie Curie':
    print('You won two Nobel Prizes.')
else:
    print("Nice to meet you!")
```

<div class="important-box" data-title="Syntax rules">

End each condition line with a **colon** (`:`). **Indent** the body of each block.

</div>

---

## Functions

<div class="definition-box" data-title="What is a function?">

A reusable block of code that takes **arguments** (inputs) and optionally **returns** a value.

</div>

```python
def square(x):
    return x ** 2

print(square(3))  # 9
print(square(7))  # 49
```

<div class="note-box" data-title="Key points">

- Define with `def`, end the signature with `:`
- Use `return` to send a value back (otherwise the function returns `None`)
- Functions can call other functions, including themselves

</div>

---

## `for` loops

<div class="definition-box" data-title="Iterating over a collection">

A `for` loop runs the same block of code once **for each item** in a list (or other iterable).

</div>

```python
for x in ['a', 'b', 'c', 'd']:
    print(x)
# prints: a  b  c  d
```

---

## `while` loops

<div class="definition-box" data-title="Loop until a condition is false">

A `while` loop repeats **while** its condition remains `True`.

</div>

```python
i = 10
while i > 0:
    i = i - 1
    print(i)
# prints: 9 8 7 6 5 4 3 2 1 0
```

<div class="warning-box" data-title="Infinite loops">

If the loop condition never becomes `False`, the loop runs forever. Press `Ctrl + C` to stop it.

</div>

---

## Importing libraries

<div class="note-box" data-title="Extending Python's capabilities">

Use `import` to load libraries of functions written by others.

</div>

```python
import math as m
from math import degrees as deg

m.sin(m.pi) - m.cos(m.pi)  # ≈ 1.0
```

<div class="tip-box" data-title="Useful keywords">

- `import X` &mdash; import library `X`
- `import X as Y` &mdash; import and rename to `Y`
- `from X import f` &mdash; import only function `f` from `X`

</div>

---

## Getting help and handling errors

<div class="tip-box" data-title="Built-in help">

Call `help(function_name)` to see documentation for any function.

</div>

<div class="warning-box" data-title="Error messages">

When something goes wrong, Python prints a **traceback** that tells you *what* failed and *where*:

```python
1 + 'test'
# TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

</div>

<div class="note-box" data-title="Other resources">

Google, Stack Overflow, class Slack, and office hours are all great places to get unstuck.

</div>

---

## Happy coding!

<div class="important-box" data-title="Key takeaway">

Programming is one of the most rewarding skills you can pick up. Don't be afraid to make mistakes, experiment freely, and ask for help when you need it.

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

- **Thursday X-hour:** Introduction to vibe coding

</div>
