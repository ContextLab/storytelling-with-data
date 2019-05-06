# Hackathon 1
### Athina Schmidt, Paxton Fitzpatrick, Sonia Rowley

## Overview

In this notebook, we mapped the parking violations in Greenpoint Brooklyn (94th Precinct) that occurred on January 1, 2019. The icon at the site of each violation is colored by the type of violation that occurred. 

## Dataset

Source: https://data.cityofnewyork.us/City-Government/Parking-Violations-Issued-Fiscal-Year-2019/pvqr-7yc4

`parking-violations-geodata.csv` is a very small subset of this data that we created as follows:

Because the full 2019 dataset (as of April 28) has 8,718,669 rows, we filtered the data in the NYC OpenData website by precinct (94) and date (1-1-2019) before downloading.

In Microsoft Excel, we further pared down the data. First we deleted all the columns that were irrelevant to our analysis, keeping only Summons Number, Street Number, Street Name, Violation Time, Violation Code, and Intersection. We then began to format addresses. In order for our program to work, we needed addresses in the format “**Street, City, State, etc...*** ”. We deleted the 34 rows that did not have properly-formatted addresses for our analysis. These entries’ addresses were recorded as corners, i.e. “Street 1 c/o Street 2”. Then, we manually added a city_state column. Every entry in this pared-down data was from Brooklyn, NY.

In Jupyter Notebooks, we used GoogleMaps to add the zip code, latitude, and longitude of each address to the dataset.

## Running the Code
This code requires the following packages to run: `numpy`, `pandas`, `pickle`, `googlemaps`, and `folium`. Obtaining geodata from addresses requires a google maps API key. 
Other users should set file loading paths to the location of the dataset on their computers. 
In "violations-map," running cells whose last line contains a single 'm' will generate a veiw of the map.

## Contributing

Briefly describe how other people could build on your work. For example, you might have ideas for sections of your notebook that could use some cleaning up or debugging, or you might have ideas for follow-up analyses. Also acknowledge any collaborations (e.g. other students you consulted for this assignment). 

We got the inspiration for this visualization from: https://www.reddit.com/r/dataisbeautiful/comments/anvc7v/oc_visualizing_all_parking_violations_in_los/.  
Just as Steve Bottos’ above visualization inspired our current visualization, it also provides inspiration for future directions we could take this analysis. 

First, and perhaps most obviously, we could visualize more data. We started with a single day in a single precinct, but we could also scale up to visualize the whole city for a day, a precinct for a year, or even the whole city for a year. The primary roadblock to scaling up is the cap on our free use of the Google API key. We also need to find a way to convert the poorly formatted addresses (“street 1 corner of street 2”) into the correct format instead of simply deleting them.

In order to visualize more data, we would have to declutter our visualization. Bottos’ visualization provides inspiration for one way to do so. In his visualization, he uses a folium “bubble map.” As the user zooms out, violations collapse into single points labeled with a sum of all violations in the surrounding area. An interesting alternative would be to visualize NYC violations _by precinct_ using a folium “choropleth map.”

We could also add more information to the visualization by adding popup information to each point. It would be ideal if, when the user moused over each icon, they could see the violation type, price, date, and time. 

Finally, we could create simple bar graphs with the data, comparing # of violations by month, time of day, violation reasons, type of car, etc. (see Bottos visualization)
