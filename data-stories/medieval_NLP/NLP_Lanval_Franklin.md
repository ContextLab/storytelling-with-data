# Project information

Name the project and list the authors and their GitHub usernames.  If the GitHub commit history of your project does not reflect each contributor's work (e.g., if a single person was nominated to pull everyone's changes into the repository), you should include a brief description of each contributor's role in the project.

_Natural Language Processing on "Lanval" and "The Franklin's Tale"_ 

Username: FanruiShao

# Overview

This is where you describe what your project is about, in a few sentences.  Specifically:
- What was your main question?

Does the word frequency that match my observation and analysis? 
What's the rhyming pattern in the two texts?

- How did you approach exploring and/or answering your question?

I looked at the word count and the first and the last word of each verse.

- What data did you use? 

2 txt files of medieaval texts that I used for my MA thesis.

- What sorts of data science tools did you use? 
 
Pandas and plotly.

- What did you find or accomplish (be brief)?  For example, did you find any interesting results or insights?  Or did you solve an interesting problem that might be useful in another project?


From my analysis on pandas and plotly, we see how colors and word frequencies reflect the identities of characters and the social norms. And we observe the rhyming pattern at the end of each verse in couplet AABB. 


Upload a movie of your data story to YouTube and include a link here.  You can narrate over a screencast of you scrolling through your notebook, or you can paste your figures into a Powerpoint or Keynote presentation (or similar).  You may also find [Marp](https://yhatt.github.io/marp/) useful; it's what I'm using to generate the slideshows for [Modules 1--4](https://github.com/ContextLab/storytelling-with-data/blob/master/slides/outline.md).  (Sample slides [here](https://github.com/ContextLab/storytelling-with-data/blob/master/slides/modules_and_numpy.md) and [here](https://github.com/ContextLab/storytelling-with-data/blob/master/slides/pandas.md).)
[NLP_Lanval_Franklin](https://youtu.be/tjZN0bExhrM)



# Downloading the data

Provide a link to the dataset(s) you're using for the project, along with a brief description of the data.

[Lais_de_Marie_de_France_Lanval.txt](https://github.com/ContextLab/storytelling-with-data/files/8259198/Lais_de_Marie_de_France_Lanval.txt)

[Franklin1.txt](https://github.com/ContextLab/storytelling-with-data/files/8259200/Franklin1.txt)


# Running the code

Describe, in sufficient detail for a new person (moderately competent but unfamiliar with your work) to follow, how to run your code.  If the project is implemented in one or more Colaboratory notebooks, you should provide a link to the notebook(s) here.  Also copy the notebooks (as .ipynb files) into your project folder so that everything related to your project is backed up on GitHub.


[NLP_for_lanval](https://colab.research.google.com/drive/1athAjKgRPKpouUZYU-wgf-5uwRimmFcM#scrollTo=I24IbiR21YU0)

[NLP_for_franklin](https://colab.research.google.com/drive/14cuBVomLogSzYVKNgsMZrpDcbLeytf_3#scrollTo=vpgfKqoGzILc)

[character_title](https://colab.research.google.com/drive/1P4LwN6pa9reUrcIDyFrOkvtnnpA31Iac)

this is the coding for the pie charts in particular.

# Contributing to the code

Tell other people how they can contribute to the project you've started.  Specifically:
- What are the most obvious next steps?

To visualize the rhyming pattern and to code the mediaeval linguistic syntax


- What are some questions that your work raises?

How can we analyse ancient/old languages through modern scopes or by natural language processing? 

Is there a way to specify the puns or metaphors in word count?


- What challenges remain?

The old languages have many meaningless words that exist only for the the sound, like the "li" in Old French, I found it distracting. There are also many articles that I don't really need in NLP and do not know if there is a way to eliminate them.(We aslo need to keep in mind that the ancient languages have more cases, that is to say, for example, a "that" may have more than 4 forms, which makes the idetification more difficult) 


- Are there any known bugs or problems with your approach that someone continuing your project should be aware of?

the single quotation mark that functions in the vocal phenomina "liason" in French language is not recognized by the system, i.e. "fils d'or." We need to teach the system that "d'or" = "de or"

# Acknowledgements

Many thanks to Prof.Jeremy Manning for his office hours where he taught me to code NLP and debuged my coding! Thanks to my advisors, Prof.Georges Edmonson and Prof.Andrea Tarnowski who inspired me and has supported me on my way to write the thesis!
