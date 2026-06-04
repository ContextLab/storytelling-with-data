**Data Story: The Architecture of Persuasion** 

**Authors:**   
**Marissa Benz \-** Github: marissapbenz26-eng  
**Natalia Schmitter-Emerson** \- Github: username 

**Overview:**   
**Main question:** Does the structure of a persuasive argument predict whether it succeeds — and does it matter more than what you say?

We used a dataset of 1,017 conversations in which one stranger tried to convince another to donate part of their paycheck to Save the Children. Every conversation measured how much, if anything, the persuadee donated. We mapped each persuader's argument into a knowledge graph using a LangChain graph transformer, where nodes represent concepts and edges represent relationships between them. We measured various structural features of these graphs, including concept count, edge density, and betweenness centrality, and compared them across successful and failed conversations. We also analyzed text features, conversation timing, and whether the persuader had donated themselves to see whether it predicted whether the conversation would end in a successful donation.

**Key findings:**

* Surface level features of the conversation such as word count, question count, and emotional language, did not predict success  
* In successful conversations, Save the Children had twice the betweenness centrality compared to failed ones (0.155 vs 0.078), suggesting successful persuaders built their argument around the charity as a hub   
* The only statistically significant predictor in a logistic regression was whether the persuader had donated themselves

**YouTube link:** [https://youtu.be/MPry4XHoRo4](https://youtu.be/MPry4XHoRo4) 

**Downloading the data:** 

The dataset used is the PersuasionForGood corpus, available through ConvoKit — a toolkit developed at Cornell for analyzing conversations at scale.

**ConvoKit documentation: [https://convokit.cornell.edu/documentation/persuasionforgood.html](https://convokit.cornell.edu/documentation/persuasionforgood.html)**

**Running the code:** 

The full analysis is contained in persuasionforgood.ipynb. To run it:

1. Clone this repository  
2. Install dependencies: pip install convokit langchain langchain-anthropic networkx pyvis scikit-learn scipy matplotlib pandas  
3. Set your Anthropic API key as an environment variable: export ANTHROPIC\_API\_KEY=your\_key\_here  
4. Open persuasionforgood.ipynb in VS Code and run all cells in order

**Contributing to this code:** 

Next Steps: 

* Extending the analysis to predict donation amount continuously rather than as a binary succeeded/failed outcome  
* X  
* X

Open Questions: 

* The dataset includes rich demographic and psychological data for every participant — age, income, ideology, Big Five personality traits, moral foundations, and decision making style — none of which were used in this analysis. Future work could explore whether any of these variables mediate or moderate the persuader donation effect, or whether personality matching between persuader and persuadee predicts success better than argument structure alone.  
* X

Limitations: 

* The betweenness centrality finding is significant at the aggregate level but does not survive as an individual-level predictor in the regression  
* All conversations are about the same charity, which limits how generalizable the structural findings are to persuasion in other contexts  
* The binary succeeded/failed framing loses a lot of information — a conversation that got $0.01 and one that got $100 are treated the same

**Acknowledgements:** 

* Dataset: Wang et al., "Persuasion for Good: Towards a Personalized Persuasive Dialogue System for Social Good." ACL 2019\. [link](https://convokit.cornell.edu/documentation/persuasionforgood.html)  
* ConvoKit: [https://convokit.cornell.edu](https://convokit.cornell.edu)  
* LangChain LLMGraphTransformer: [https://python.langchain.com](https://python.langchain.com)