#Project information#

_Color Theory_, FanruiShao

# Overview

This is where you describe what your project is about, in a few sentences.  Specifically:
- What was your main question?
What's the proportion of cool , warm, and earth colors in the sets of oil paints sold on current market? How is the proprotaion related to the price of the set?

- How did you approach exploring and/or answering your question?
  - What data did you use?
The information of products on Blick.com, my art practice, my knowledge of color theory, 
  - What sorts of data science tools did you use?
Pandas and Plotly.
- What did you find or accomplish (be brief)?  For example, did you find any interesting results or insights?  Or did you solve an interesting problem that might be useful in another project?
I found: 1. The more expensive set should have 1:1:1 in three colors, since they can afford more expensive indigents.
2. non-US brand have an even proportion in colors, while US brand don’t.
3. when you buy a cheaper set, you will have a higher the proportion of earth color.

Upload a movie of your data story to YouTube and include a link here.  You can narrate over a screencast of you scrolling through your notebook, or you can paste your figures into a Powerpoint or Keynote presentation (or similar).  You may also find [Marp](https://yhatt.github.io/marp/) useful; it's what I'm using to generate the slideshows for [Modules 1--4](https://github.com/ContextLab/storytelling-with-data/blob/master/slides/outline.md).  (Sample slides [here](https://github.com/ContextLab/storytelling-with-data/blob/master/slides/modules_and_numpy.md) and [here](https://github.com/ContextLab/storytelling-with-data/blob/master/slides/pandas.md).)
[Color Theory](https://www.youtube.com/watch?v=J7AcDy7VkdE)

# Downloading the data

Provide a link to the dataset(s) you're using for the project, along with a brief description of the data.
[the distribution of ryb 3 colors](https://github.com/ContextLab/storytelling-with-data/raw/master/data-stories/color-theory/3_color.csv)
[the earth color and unit price](https://github.com/ContextLab/storytelling-with-data/raw/master/data-stories/color-theory/earthcolor.csv)

# Running the code

Describe, in sufficient detail for a new person (moderately competent but unfamiliar with your work) to follow, how to run your code.  If the project is implemented in one or more Colaboratory notebooks, you should provide a link to the notebook(s) here.  Also copy the notebooks (as .ipynb files) into your project folder so that everything related to your project is backed up on GitHub.

[see this notebook](https://colab.research.google.com/drive/1jCCDXrUe6ULzSFPbb3WutCCZAkXO8sDM)

# Contributing to the code

Tell other people how they can contribute to the project you've started.  Specifically:
- What are the most obvious next steps?
To look at more oil paint sets; to eliminate customs' impact on the price of imported art supply

- What are some questions that your work raises?
How to choose the colors in a set to better train one's artistic skills(ie.color sensibility)? Why is there price difference in different colors in oil paints?

- What challenges remain?
Yes, artistic taste/instinct is often regarded more important than skills/basic knowledge and there is no fixed way to learn about colors, thus my approach is only one way to approach color theory.

- Are there any known bugs or problems with your approach that someone continuing your project should be aware of?
Yes, actually the tone in color is comparative. That is to say, in the category of cool blue, some blue is cooler than the other, but there is no universal scale to measure. I think it might be fruitful to build a system to classify the warmth of color in a more subtle way, than the binary we have at this point.

# Acknowledgements

If your idea is based on or inspired by someone else's work (either their code or their ideas), cite them and provide links to their work.  Also, if you received help or support from someone who is not listed as an author on this project, you should acknowledge them here.

The abstract painting on the left in the three-painting page is made by Ekene Duruaku 22' at Dartmouth College; other paintings and drawings are made by Fanrui Shao 22 'MA COLT at Dartmouth College.
