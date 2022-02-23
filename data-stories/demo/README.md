# Project information
Our team consists of Karim Khalil and Saruul Ijilmurun. We both analyzed the data and put the story together.

# Overview
- What was your main question?
For our project, we chose to examine how mental health Illnesses, regardless of their severity, correlate with substance abuse such as alcohol and drugs and drug overdoses. We focused our study on the state of New Hampshire, since we both attend Dartmouth College and were intrigued to understand the prevalence of mental illness, over-dosing, and substance abuse in our current location. 

Mental health illness has been increasingly prevalent in our world, especially after the covid pandemic. Research has found that oftentimes drugs and alcohol are used as coping mechanisms for mental illnesses. 

By analyzing the above datasets we were hoping to develop a better understanding of how substance abuse and mental health correlate. Our intention was to dig deeper into these datasets in hopes of generating attention to public mental health discourse, practice, research, and evidence that illustrates the rapid change in mental health illnesses.

- How did you approach exploring and/or answering your question?
Firstly, we evaluated the trends of any mental illness prevalence, which we will refer to as AMI, and severe mental illness, which we will refer to as SMI. We  use both of these indicators to understand whether Mental Illness has been increasing or decreasing in New Hampshire. 

We then used datasets on current illicit drug usage, which involves the misuse of prescription psychotherapeutics, the use of marijuana, cocaine (including crack), heroin, hallucinogens, inhalants, or methamphetamine. After having analyzed those trends for the New Hampshire Area, we moved on to heavy alcohol consumption. We evaluated the trend line for the dataset and created choropleth.

Furthermore, we examined a data set on overdoses in the state of New Hampshire and created a bar graph of the overdoses over the course of several years, and choropleth to see if it looks similar to the alcohol consumption map. 

Finally, we ran a correlation test between SMI, AMI and illicit drug consumption, heavy alcohol use and overdoses. We believed that by checking for correlation we would be able to truly see if there was a relationship between these variables, while keeping in mind that correlation does not mean causation.

- What sorts of data science tools did you use?
Since the analysis was focused on google notebooks, we used python libraries, such as Numpy and Pandas, to manipulate and analyze the data. We also used Plotly Express to visualize our data through graphs and figures.

- What did you find or accomplish (be brief)?  For example, did you find any interesting results or insights?  Or did you solve an interesting problem that might be useful in another project?
First we found that both illicit drug use prevalence rate and drug overdose death rate are strongly correlated with SMI. Illicit drug use prevalence and SMI have a strong positive correlation of 0.77, similarly drug overdose death rate and SMI have a correlation of 0.83.

On the other hand, we didn’t see the same sort of correlation between illicit drug use prevalence and AMI, and drug overdose death rate and AMI.  

Furthermore, we found a weak negative correlation between SMI and heavy alcohol use. Which we found quite shocking since we were expecting at least a positive correlation after having seen how SMI correlated with drug use and overdoses.
Similarly, and a moderate negative correlation between AMI and heavy alcohol use. 

Finally, what we noticed, which was shown in both maps above, was that the areas with the highest rates for whichever indicator was being tested, whether it was overdose rate or alcohol consumption rate, were located around the capital and most metropolitan areas of the state of New Hampshire.

https://youtu.be/AbQqIMK0hMw

# Downloading the data
All of our data sets were extracted from the New Hampshire Department of Health and Human services. Which we found to be trustworthy as it is a New Hampshire government run website – that is, of course, if you trust the government. All jokes aside, these were  most definitely the most reliable datasets that we could get access to. We used a data set on Severe Mental Health Prevalence, Any Mental Health Prevalence, Current Illicit drug usage, heavy alcohol consumption prevalence, and overdoses. 

https://github.com/ContextLab/storytelling-with-data/raw/master/data-stories/VT-DoH/SubstanceMisuseData.csv
https://github.com/karimkhalil-byte/storytelling-with-data/raw/master/data-stories/VT-DoH/SubstanceMisuseDataAMI.csv
https://github.com/karimkhalil-byte/storytelling-with-data/raw/master/data-stories/VT-DoH/AlcMapData.csv
https://github.com/karimkhalil-byte/storytelling-with-data/raw/master/data-stories/VT-DoH/AlcTimetrendData.csv
https://github.com/karimkhalil-byte/storytelling-with-data/raw/master/data-stories/VT-DoH/ODMap.csv
https://github.com/karimkhalil-byte/storytelling-with-data/raw/master/data-stories/VT-DoH/ODtime.csv
https://github.com/ContextLab/storytelling-with-data/raw/master/data-stories/VT-DoH/CurDrugUse.csv

# Contributing to the code
- What are the most obvious next steps? What are some questions that your work raises?
We believe that by using specific data sets on stimulants vs depressants, we could gain a better understanding of whether specific drugs/ substances have a correlation with mental illness. Furthermore, we could take socioeconomic factors into account to see whether those are actually the root, or one of the causes of the mental health prevalence increase. 

- What challenges remain?
One of the biggest challenges we have right now is the limited amount of datasets regarding substance misuse in New Hampshire. Also, the available datasets are too broad, which make it hard to further analyze the current data and ensure the accurateness of the analysis.

- Are there any known bugs or problems with your approach that someone continuing your project should be aware of?
There are no bugs that need to be made known, however, there are several elements that would be useful to know. Firstly, in the map for alcohol consumption, there weren’t estimates for the consumption rate of every county. However, they provided upper and lower bound estimates, so we used the average of both as the estimate for those said counties. Secondly, we should remember that NH is currently in an opioid pandemic and that the spike in overdoses could be correlated to that rather than the spike in mental health prevalence. 
