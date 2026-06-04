**Data Story: Emotional Support Conversations**

**Authors:**   
**Marissa Benz \-** Github: marissapbenz26-eng  
**Natalia Schmitter-Emerson** \- Github: [nataliaeschmitter-emerson26-ops](https://github.com/nataliaeschmitter-emerson26-ops)

**Overview:**   
**Main question:** Does talking to a peer supporter with your problems, and does it depend on what you are going through? 

We used a dataset of 1,150 emotional support conversations from Cornell University's Emotional Support Conversation Corpus, in which people in distress spoke with trained peer supporters. Each seeker rated their own emotional distress on a 1–5 scale before and after the conversation.

We used VADER sentiment analysis to score the emotional content of every message in every conversation from \-1 to \+1. We then mapped sentiment trajectories across conversation time, clustered outcomes into "much improved" and "somewhat improved" groups, and divided results by emotion type and problem type to understand who benefits most from emotional support conversations and when in a conversation improvement happens.

**Key findings:** 

* Talking to peer support helped in all conversations, with sentiment increasing  
* Anxiety was the least responsive emotion to a single conversation; anger and sadness improved most  
* Improvement tends to happen surprisingly early (by around the second quarter) in an emotional support conversation.   
* Situational crises (breakups, job loss, friendship conflict) showed 64–69% much improved outcomes, while ongoing depression showed only 55% 

**YouTube link: [https://youtu.be/\_hzcUkERzR0](https://youtu.be/_hzcUkERzR0)** 

**Downloading the data**

The dataset used is the Emotional Support Conversation Corpus, available through the original authors' GitHub repository. 

Dataset repository: [https://github.com/thu-coai/Emotional-Support-Conversation](https://github.com/thu-coai/Emotional-Support-Conversation)

**Running the code:** 

The full analysis is contained in emotionalsupport.ipynb. To run it:

1. Clone this repository  
2. Install dependencies: pip install pandas numpy matplotlib scipy vaderSentiment  
3. Download the dataset from the link above and place it in the project folder  
4. Open emotionalsupport.ipynb in VS Code and run all cells in order

**Contributing to the code:**

Next Steps/Open Questions: 

* Are the differences between much improved and somewhat improved actually statistically reliable? The raw sentiment values are very close: 0.40 vs 0.38 in the final quarter. A t-test at each quarter would tell you whether meaningful gaps exist.  
* Do certain supporter strategies work better for certain presenting problems, and can that be detected in the language?  
* The dataset includes open-ended post-conversation responses from both seekers and supporters (seeker\_question1, seeker\_question2, supporter\_question1, supporter\_question2)---none of which were used in this analysis. Future work could run sentiment analysis or graph transformers on these to understand how people describe their own experience of the conversation

Limitations: 

* Self-report distress ratings are subjective and could reflect social desirability bias. People may rate themselves as improved partially because they feel they should have after talking to someone.  
* The much improved / somewhat improved groupings lose a lot of information. The two groups are fairly similar, so a continuous outcome measure might be better used.

**Acknowledgements:** 

* Dataset: Rashkin et al. / Liu et al. — *Emotional Support Conversation Corpus*, Cornell University. https://github.com/thu-coai/Emotional-Support-Conversation  
* VADER Sentiment Analysis: Hutto, C.J. & Gilbert, E.E. "VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text." ICWSM 2014\. https://ojs.aaai.org/index.php/ICWSM/article/view/14550  
* ConvoKit: [https://convokit.cornell.edu](https://convokit.cornell.edu)

