# Project information

The Collaborative is one of Vermont's largest substance misuse prevention organizations, dedicated to empowering youth and families while fostering 
healthy, supportive communities. One of their main initiatives is the Resilience Through Understanding (RTU) program which is a series of events 
designed for middle and high school students and their families. The goal of this project was to track where the program maintains participation in these 
events throughout the school year and where it starts to fall off.

Authors: Marissa Benz, Kate Marine, Andy Kim, Henry Ren, Natalia Schmitter-Emerson, SamMacuga

**Link to video:** https://youtu.be/Hd0XKR3HTLg 

# Overview

## Research questions

Where does RTU's reach hold across the program year, and where does it break down?

Specifically:
- How many youth-adult pairs participate at each of the five events?
- Where in the program do the largest drops happen?
- Are those drops uniform across schools, or are they possibly driven by specific schools or specific event formats?
- What do the patterns suggest about program design and scalability?

## Data

We used data from a series of follow-up surveys that RTU asked partipants after each event. These surveys contain responses from both youth participants and their caring adults, 
who attend events together as pairs (so for this project all participation counts refer to youth-adult pairs). The dataset for these surveys is an Excel workbook with one sheet 
per event (Kickoff, Event 2, Event 3, Event 4, Event 5). Each row is one survey response from a youth-adult pair.

## Approach

We started by cleaning the data by removing blank rows (artifact from the Excel format) and standardizing school names so we didn't do any double-counting. 
Then we counted youth-adult pairs (one row = one pair) at each of the five events. To analyze where the drops were happening, we built a matrix where rows were 
schools and columns were events and observed the results.

## Findings

The first main point where we found participate to clearly start dropping off was Event 4. Response counts fell by 149 compared to Event 3, and it was consistent across all participating schools (BBA fell by 56, Long Trail by 22, Leland & Gray by 17, Flood Brook by 16, and Maple Street by 10). 
Some of this could definitely be due to the fact that Event 4 was in January, where weather can disrupts scheduling and the ski pass incentive starts to lose its power as students have possibly already purchased ones for the season.

The second major participation dropoff was at Event 5, especially when viewed at the school-level. There were 137 fewer responses in total. 
Interestingly, participation came almost entirely from the schools Leland & Gray (23), BBA (20), and Long Trail (13). The other seven schools only had a handful of responses or none at all.


## Downloading the data

Survey dataset is stored an Excel workbook with one sheet per event (Kickoff, Event 2, Event 3, Event 4, Event 5). 
Each row is one survey response from a youth-adult pair. See data-stories/collaborative/2025-2026 All RTU Data.xlsx 

## Running the code

Link to colab notebook: https://colab.research.google.com/github/ContextLab/storytelling-with-data/blob/master/data-stories/collaborative/Assignment4.ipynb 

## Contributing to the code

We want to acknowledge that the data is using survey responses and not actual attendance count. So if a pair attended an event but didn't fill out the follow-up survey then they get missed out
and this could definitely have contributed to misleading stats in our analysis. Also, we treat each row as one youth-adult pair and we don't have a consistent pair ID across events, so we can't track individual 
pairs over time. Future surveys could implement this and allow for some interesting case studies of how participants perhaps change over time as they go through the events. 
The Event 2 count exceeds Kickoff for several schools (e.g., Leland & Gray: 69 → 93). This likely reflects late joiners or makeup activity rather than a true increase in unique pairs. Our retention curves show this honestly rather than capping at 100%.
Finally, we can only really make guesses at the reasons behind some of the participation drops. Future work could possibly involve more interviews from Collaborative staff and participants.


## Acknowledgements

Thank you to https://thecollaborative.us/ for giving access to their survey data and allowing us to help support their work.
