# **Mapping the Structure of *The Unbearable Lightness of Being***

Authors: Natalia Schmitter-Emerson ([nataliaeschmitter-emerson26-ops](https://github.com/nataliaeschmitter-emerson26-ops)) · Marissa Benz (marissapbenz26-eng) 

We distributed data analysis, visualizations, scriptwriting, and video production equally. We alternated roles for each video, such that we both completed all of them.

# **Overview**

This project examines whether the narrative structure of a novel can be tracked by measuring meaning mathematically, without any prior knowledge of the text.

We took the full text of *The Unbearable Lightness of Being* by Milan Kundera and split it into 914 overlapping 400-word sliding windows. Each window was encoded by a pretrained sentence embedding model (all-mpnet-base-v2 via HuggingFace) into a 768-dimensional vector, where position in space is determined entirely by semantic meaning. We then used UMAP and PCA to project those vectors into 2D and 3D for visualization, k-means clustering to auto-detect thematic sections, cosine dissimilarity between consecutive windows to measure moment-to-moment narrative drift, and word frequency analysis on each cluster to generate section-level word clouds. This work was completed via Google Co-lab and Claude.

The narrative trajectory on the UMAP folds back on itself through the same regions rather than traveling A to B, which is a metaphor for Kundera’ main theme: eternal recurrence. The clustering algorithm placed Franz's sections of the book separate from the Prague-centered material, without any meaningful or genuine knowledge of character or plot, revealing how digressions and changes in the narrative are measurable using data science tools. Every one of the five largest semantic drift spikes in the book corresponds exactly to a moment where Kundera interrupts the narrative with a philosophical digression.

Youtube Link: [https://youtu.be/ooqbnb0VpOA](https://youtu.be/ooqbnb0VpOA)

# **Downloading the data**

The text we examined was downloaded from a PDF on google, linked here:   
[https://www.msjkeeler.com/uploads/1/4/0/6/1406968/milan\_kundera\_-\_the\_unbearable\_lightness\_of\_being.pdf](https://www.msjkeeler.com/uploads/1/4/0/6/1406968/milan_kundera_-_the_unbearable_lightness_of_being.pdf) 

To run on *The Unbearable Lightness of Being* specifically, you will need a legally obtained plain-text (.txt) copy of the book.

# **Running the code**

Dependencies — install once:

pip install sentence-transformers umap-learn scikit-learn wordcloud plotly numpy

The first run will download the embedding model (\~420MB) and cache it locally, rendering subsequent runs faster.

Run the analysis:

\# On any .txt file  
python analyze.py \--book "unbearable\_lightness.txt" \--title "Unbearable Lightness of Being"

\# Or test immediately with the built-in demo text  
python analyze.py \--demo

\# Or pull any public domain book directly from Project Gutenberg  
python analyze.py \--gutenberg 2554 \--title "Crime and Punishment"

Output: A self-contained output/report.html file. Open it in any browser — no server required. It contains all visualizations (UMAP 2D, UMAP 3D, PCA, semantic drift chart, section word clouds) as interactive Plotly figures.

Colab Notebook: [https://colab.research.google.com/drive/1lsmezbyQUrhbiudGpgsLClyAR0a1eikJ](https://colab.research.google.com/drive/1lsmezbyQUrhbiudGpgsLClyAR0a1eikJ) 

---

# **Contributing to the code**

Most obvious next steps:

* Compare multiple books in the same embedding space to see whether different authors or genres cluster differently  
* Compare multiple translations of the same book to measure how translator choices shift meaning across the narrative  
* Use longer sliding narratives  
* Subtract out the average word from each word cloud to look at differences across sections  
* Random seed parameter to get a different rotation

Open questions raised by this work:

* Does the looping trajectory pattern appear in other Kundera novels, or is it specific to this book? (This might indicate an intentionality related to the contents of the book)  
* The five drift spikes all correspond to philosophical digressions. Is this true for other essay-novel hybrids not written by Kundera?

Known limitations:

* The word clouds were producing strange words due to line breaks and running headers  
* UMAP needs improvement via hidden parameters

Acknowledgements: 

* Kundera, M. (1984). *The unbearable lightness of being* (M. H. Heim, Trans.). Harper & Row. Retrieved from [https://www.msjkeeler.com/uploads/1/4/0/6/1406968/milan\_kundera\_-\_the\_unbearable\_lightness\_of\_being.pdf](https://www.msjkeeler.com/uploads/1/4/0/6/1406968/milan_kundera_-_the_unbearable_lightness_of_being.pdf)

