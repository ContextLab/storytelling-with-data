# Final assignment: Semantic Mapping

## Overview

For my final project, I attempted to improve upon an approach devised by Huth et al. (2016; paper available [here](https://www.nature.com/articles/nature17637); code available [here](https://github.com/HuthLab/speechmodeltutorial/)) by which researchers systematically mapped the semantic selectivity of various regions across the human neocortex.  Huth et al. (2016) created a vector-space semantic model describing the similarity between features of 10,470 words.  With these features, they built linear models of fMRI data, and fit a regression model to their temporal presence in ten stories to predict real neural activity while participants viewed an eleventh (held-out) story.  

The current approach models words' semantic features as 985-dimensional vectors.  These vector representations were computed based on the rate at which 10,470 unique words occur within 15 words of 985 "basis words," selected from [Wikipedia's List of 1000 basic words](https://simple.wikipedia.org/wiki/Wikipedia:List_of_1000_basic_words). These co-occurence rates were drawn from a massive corpus of Wikipedia articles, popular books, reddit comments, and the story stimuli used in the experiment.  While this semantic modeling approach shares certain basic properties with algorithms like [Latent Semantic Analysis](https://en.wikipedia.org/wiki/Latent_semantic_analysis) and [word2vec](https://en.wikipedia.org/wiki/Word2vec), it is somewhat unusual and self-admittedly ad hoc.

Huth et al. (2016) broadly found that most areas within the semantic system represent information about specific semantic domains.  I therefore decided to try applying [Latent Dirichlet Allocation](https://en.wikipedia.org/wiki/Latent_Dirichlet_allocation) (LDA) to their semantic mapping approach in place of the original semantic model.  LDA (like other topic modeling algorithms) assumes that any given text document is comprised of a set of latent themes (or "topics").  Topic models learn these topics from a collection of text documents (similarly based on the co-occurence rate of words) and infers their proportional presence in new documents.  So, for example, if the word "cat" and "dog" commonly occur in the same document, while "money" and "stock" commonly co-occur in different documents, each pair may be predicted to be part of two different topics.  These topics are identified in an unsupervised manner, but it is sometimes possible to assign names to them in a post-hoc way (e.g., "pets" or "finance").  The key feature to LDA (as opposed to other topic models) is the use of a sparse dirichlet prior, embodying the intuition that documents tend to cover only a small set of topics and that topics tend to use a small number of words frequently.

## Running the code

The following modules must be installed to run the notebooks in this directory:
via pip:
- `numpy`
- `hypertools`
- `matplotlib`
- `seaborn`
- `tables`
- `scipy`
- `scikit-learn`
- `nibabel`
- `nltk`
- `joblib`
- `h5py`
- `lxml`
- `shapely`
- `html5lib`
via GitHub:
- `pycortex` (`git clone https://github.com/gallantlab/pycortex.git && cd pycortex && python setup.py install`)

You will also need to download the
