## Uber NYC Rides Analysis 
Contributors: Jane Lee & Lillian Zhao

PURPOSE:
To visualize the fluctuation in time-related uber pickup traffic. 
- locations throughout the day and correlate it with daily commuter transit. 


DATA:
Data source link: 
##FIND THIS

We have edited the original data source in this github repo, removing unneeded data files. Data files that we kept are described below. 

This directory contains data on over 4.5 million Uber pickups in New York City from April to September 2014, and 14.3 million more Uber pickups from January to June 2015. Trip-level data on 10 other for-hire vehicle (FHV) companies, as well as aggregated data for 329 FHV companies, is also included. All the files are as they were received on August 3, Sept. 15 and Sept. 22, 2015. 

FiveThirtyEight obtained the data from the [NYC Taxi & Limousine Commission (TLC)](http://www.nyc.gov/html/tlc/html/home/home.shtml) by submitting a Freedom of Information Law request on July 20, 2015. The TLC has sent us the data in batches as it continues to review trip data Uber and other HFV companies have submitted to it. The TLC's correspondence with FiveThirtyEight is included in the files `TLC_letter.pdf`, `TLC_letter2.pdf` and `TLC_letter3.pdf`. TLC records requests can be made [here](http://www.nyc.gov/html/tlc/html/passenger/records.shtml).

In the folder `uber-trip-data`, there are six files of raw data on Uber pickups in New York City from April to September 2014. The files are separated by month and each has the following columns:

Header | Definition
---|---------
`Date/Time` | The date and time of the Uber pickup
`Lat` | The latitude of the Uber pickup
`Lon` | The longitude of the Uber pickup
`Base` | The [TLC base company](http://www.nyc.gov/html/tlc/html/industry/base_and_business.shtml) code affiliated with the Uber pickup

The file `Aggregate_FHV_Data.xlsx`, which contains aggregate analysis on taxi and FHV trips, came directly from the TLC.

The file `Uber-Jan-Feb-FOIL.csv` contains aggregated daily Uber trip statistics in January and February 2015.



LIBRARIES:
We're plotting some data from Uber.  The sample code loads in data, organizes it, and plots it (using Plotly).
To run this analysis you need to install plotly (run from within the docker container):
`pip install plotly`


