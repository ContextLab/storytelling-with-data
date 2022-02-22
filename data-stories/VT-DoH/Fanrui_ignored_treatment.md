# Youtube Link
[ignored_treatment](https://www.youtube.com/watch?v=XJc5zbxlO0k)

# Overview

1. _What was your main question?_  
Are other diseases or medical appointment canceled or retarded due to the pendamic? How?

2. _How did you approach exploring and/or answering your question?
What data did you use?_   
I tell my life story and use data from two sources: German questionaire answered by doctors in 2020, regarding the number of patients/appointments they have; a larger data set about the expected and actual Medicare physician fee schedule spending in US 2020.

3. _What sorts of data science tools did you use?_  
Pandas and Plotly

4. _What did you find or accomplish (be brief)? For example, did you find any interesting results or insights? Or did you solve an interesting problem that might be useful in another project?_  
Yes, the part on what kinds of medicare service is more likely to be ignored under pendamic makes sense. But the between-states difference needs more detailled data and analysis.

# Outline

1.	Story of my surgery before covid, and after removal all the suture, I came to France, where I found that they missed one suture. What to do?
2.	The hospitals are closed, and I don’t have a local health care
3.	Indeed, the incidence like such is common during pandemic, for example…
4.	The lack of data seems to tell us the impact of pandemic that takes the resources from other medical treatments(1.5min)
5.	Graphs (3min)
6.	Back to the first story, how I remove the suture by myself

# Written narrative

In december 2019, I had a small surgery on the left side of my nose in my hometown in China. The suture was removed in a week and I flied to France for a language exam. After the exam, I went to visit friends in Germany, and finally had time to look at myself in the mirror. I suddenly noticed a blue thread on my surgical wound. I looked **5% like a modern Frankenstein**.  I didn’t know what to do.
Covid had its first outburst in China that the hospitals, schools and airports were closed. it was unlikely that my parents could go to the hospital to the nurse or the doctor that was responsible for me.
I was not able to go back home and did not have a French or German health insurance, neither did I want to go to a hospital to expose myself to potential virus. 

During the pandemic, there are other patients like me who is not able to or unwilling to go to an emergency room or a scheduled appointment. 
In Germany, where I noticed my unremoved suture thread, doctors reported the general trend of cancelation in selective surgeries. 
in the same survey, more than half of the doctors observed a decrease in oncological patients coming for consultation.  
And there were also less emergent surgeries, which may tell us that home is a safe place? when people stay at home, they seem less likely to be injured.

In the US, we see a similar pattern from the Medicare physician fee schedule **(MPFS)** services. Every year every state has a MPFS spending budget for each specialties in medicare, and at the end of the year, we calculate the actual spending. In 2020, the estimated shortfall in MPFS spending associated with the pandemic was **$13.9 billion (14 percent)**. And we witnessed reductions for all states and every major specialty. Yet, as you can imagine, the percentage decrease depends on the specialties. The selective treatments are more likely to be ignored compared to more life-threatening problems.
The following three specialties are the ones with the highest percentage reduction in spending: **physical therapy** – it’s reasonable that people stopped to do physical exercise at the beginning of pandemic; **optometry** – I have to admit I still wear my old glasses that I got 3 years ago. And **otolaryngology**, namely related to nose, throat and ear, the domain that my surgery belongs.  The three specialties’ actual spending is **less than 80 % of the expected**. 
In comparison, The least influenced specialties are **infectious disease, interventional radiology, and nephrology**. does not belong to the specialty of infectious disease, as it was not expected in the spending before 2020.
Like I mentioned before, the MPFS spending dropped in in every state, while the percentage drop is more striking in some states than the other. In this graph, the states on the left side has the highest percentage drop, while the ones on the right have the lowest percentage drop. 
How can we explain the difference bt states?
I mean, for example, a small state’s non-covid medicare spending can be more influenced by covid, for an easier application of quarantine policy, and a lower budget. However, on this graph, we see that the states with a higher MPFS spending, in red or yellow, like Minnesota Okahoma, and South Carolina have quite different percentage drops. Minnesota dropped by **22%**, while South Caroline only **8%**. Same for Vermont, NH and Idaho. Therefore, to think about difference bt states, we need other insights or to look at specific difference and relate them to local quarantine policies etc. 

At this point, If you still remember the blue thread on my nose, I can tell you my solution at that time. From my senior neuroscience lab class, I learned basic suture. My knowledge was telling me that it’s an undissovable thread hidden by blood scab and forgotten by the nurse. So I spent 2 hours to removed it by myself. Happy ending. But I was actually lucky that I safely removed the thread and it was not connected to a knot or other delicate suture. to be honest, I hope people can get prompt treatment and diagnostic in the post-pandemic time.


# Downloading the data

data from:

[German non-university questionaire 2020](https://bmcsurg.biomedcentral.com/articles/10.1186/s12893-020-00970-x/tables/4) 

[US MPFS spending 2020](https://www.ama-assn.org/system/files/2020-prp-covid-impact-medicare-physician-spending.pdf)


# Running the code

[code in colab](https://colab.research.google.com/drive/1kCgP697FHf2-I-0C3Sd_95oz5TMAS4pq)

# Contributing to the code

Tell other people how they can contribute to the project you've started. Specifically:

1. _What are the most obvious next steps?_   
To look at detailed spending in a specific region, instead of national data. To find a rawer but more detailed dataset.

2. _What are some questions that your work raises?_ 
How do states differ in their MPFS spending? Why and where does the difference exist? Why are some medicare specialties more impacted by covid than the others?

3. _What challenges remain?_  
There are complexer and other factors contribute to the difference in spending in medicare that may or maynot be related to covid. It's hard to draw a conclusion.

4. _Are there any known bugs or problems with your approach that someone continuing your project should be aware of?_  
I am intimidated to draw any conclusion in this project, as my data are more exploratory than complete. I think in the future I will look at smaller dataset, or my personal data that I know better, and feel more confident to make observations and suggestions.


# Acknowledgements

Thanks for Jeremy's office hour and the two debug sessions that helped my coding process. 


