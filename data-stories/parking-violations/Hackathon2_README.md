## Authors
Paxton Fitzpatrick, Sonia Rowley, and Athina Schmidt

## Overview

In our first hackathon, we mapped the parking violations in one precinct (94) of Brooklyn, NY on January 1, 2019. This project extends our previous work. We visualize a greater quantity of NYC parking violations data using more sophisticated visualizations.

1. We expanded the scope of our dataset to include six precincts in Brooklyn: 79, 81, 83, 88, and 90, in addition to 94. We also included four days' worth of data, from Friday, 1/11/2019 to Monday, 1/14/2019. 
2. We created basic bar graphs to visualize this new dataset. We graphed # of violations by hour, by day, and by ticket cost.
3. As before, we used a google maps API key to add latitude, longitude, and zip codes to each row of the dataframe.
4. We expanded upon our first mapping analysis. First, we added a pop-up to each individual parking violation icon. Icons are colored by ticket cost, and pop-ups display violation code and time issued. To  reduce the clutter of four days of data, we created a FastMarkerCluster map. The parking violation icons  collapse and expand depending on the zoom of the map. 
6. We experimented with a new type of geographic visualization: choropleth maps. In one map, the shading of each precinct is determined by the total number of tickets issued in that region. In the other, the shading of each precinct is determined by the total dollar amount spent on tickets in that region. 

## Dataset

Source: https://data.cityofnewyork.us/City-Government/Parking-Violations-Issued-Fiscal-Year-2019/pvqr-7yc4 

`violations-final.csv` is a small subset of this data that we created as follows:

We filtered the data in the NYC OpenData website by precinct (79, 81, 83, 88, 90, 94) and date (1/11/19-1/14/19) before downloading. In Excel, we removed columns irrelevant to our analysis. We added a "City & State" column and manually added "Brooklyn, NY" to each row.

In Jupyter Notebooks, we cleaned and expanded the data. First, we added ticket cost and ticket type to the dataframe. Second, we used a GoogleMaps API key to add the zip code, latitude, and longitude of each address to the dataset. We kept addresses that were entered as intersections. 

We eliminated 42 incomplete rows from the dataset. These rows either lacked adequate addresses or were missing violation number/ticket cost.

The final dataset includes 5582 rows.

`totalcounts.csv` is a tiny dataframe, created in Excel for the choropleth map. It includes total # of tickets issued and total cost of tickets issued in each of the six precincts. 

## Running the Code

This code requires the following packages to run: `numpy`, `pandas`, `folium`, `pyplot`, and `datetime`. 

Please make sure the following file paths are set properly to your directory for the code to run properly: 

brooklyn_violations.csv
violation_codes.xlsx
violations_final.csv
totalcounts.csv
pp.geojson (geojson file for all NYC police precints)

Once the rough dataset is downloaded from NYCOPENDATA one must run the get-geodata.ipynb notebook to obtain the geodata from addresses using a google maps API key. This will create a geodata.p file which is then is added to the cleaned up dataframe from NYCOPENDATA to create "violations_final.csv". 
(This step should only be completed once. Another user would only have to complete these steps if they wanted to look at different dates or bouroughs than the ones described above).

The basic visulations are rendered using the pyplot package.     

For the Clustered Map the folium pacakge is used in hand with the "marker cluster" feature. Since we have 5,000+ datapoint mapping each indiviudal point is messy and counterintuitive. Therefore each indivudal point is represented in clusters that can be clicked on by the user to provide a more detailed view. When the user clicks down to the final cluster and on a single violation the violation date and code will be shown. The color of the indivual point itself cooresponds to ticket cost. 

For the Choropleth map the folium package is also used. It works by binding a pandas dataframe onto a geojson file. Our map shows the total number of violations issued in each of the Brooklyn precincts we selected. Light green corresponds to less tickets and dark green corresponds to more tickets issued over the selected four day period. Make sure to check the "key_on" feature in your geojson file to avoid errors. Whichever item you choose to sort on must be formatted exactly the same in the dataframe as it is in the geojson file.


## Contributing

As before, we got the inspiration for this project from https://www.reddit.com/r/dataisbeautiful/comments/anvc7v/oc_visualizing_all_parking_violations_in_los/. 

In addition to this source, we relied heavily on the following online tutorials to create our maps:
* https://python-visualization.github.io/folium/plugins.html
* https://python-visualization.github.io/folium/quickstart.html#Markers
* https://nbviewer.jupyter.org/github/python-visualization/folium_contrib/blob/master/notebooks/ClusteredMarker_and_FeatureGroup.ipynb
* https://blog.dominodatalab.com/creating-interactive-crime-maps-with-folium/
* https://gis.stackexchange.com/questions/272197/error-message-module-object-has-no-attribute-markercluster

Currently, a pandas dataframe serves as a legend for our first map, showing the costs corresponding to icon color and the violation types corresponding to violation codes. Future contributors could include this information on the map itself, using a folium legend.

Future contributors could build on this work by creating similar visualizations with more data. These maps would be even more interesting if they included data from all NYC precincts. The FastMarkerCluster feature allows for the display of large quantities of data without adding clutter to the map.

Future contributors could also create an animated map using folium to plot violation locations and times over the course of a 24-hour period. Violation icons would pop up by time issued and accumulate on the map.