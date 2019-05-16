# Authors

    Sarah Kovan, Morgan Sizemore, Grace Thompson, Abby Zweifach

# Overview

    The goal of our project was to identify the zip codes with the fastest growing donations. Considering that UVLT's goal is to increase donations, we believe that this approach will allow UVLT to identify areas that yield high donations and areas that require more attention in terms of marketing. 

    We began by sorting the living (i.e. Deceased = 0) donor  by their zip codes. Then, we calculated the slope of each zip code's mean yearly donations in order to determine the fastest growing zip codes (in terms of donations to UVLT). We believe that these zip codes show the most potential and, therefore, that future analyses should focus on them.

# Dataset

    We chose to analyze the mean yearly donation (2000-2018) in each zip code. To do this, we first dropped irrelevant data columns, summed yearly unrestricted and restricted donations, and grouped donors by zip code.

# Running the Code

    To run this code, make sure that you have have the "UVLTDataAnalysis" dataset in your folder. Then run the cells in order.

# Contributing
    Data scientists hoping to contribute to this project should analyze factors such as income level and amount of land owned for each of the fastest growing zip codes in order to determine which features are similar across them and therefore may contribute to donations. Moreover, they can look at individual donors within each zip code to determine if it is the number of donations or the value of each donation that is growing. Finally, they can look at qualities of each zip code (e.g. magazines they subscribe to) to determine the best way to reach potential donors within each zip code.
