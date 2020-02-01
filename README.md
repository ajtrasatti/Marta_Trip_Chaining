# Marta Trip Chaining

## Objective:
To build a software to build from transaction data and automated personel counter data to a origin destination matrix for marta system improvements and optimization

## File Descriptions
- **main_odx.py** - main file that calls each of the modules and puts all components together to create a cohesive data set to build from
- *gtfs* 
  - **gtfs_fac.py** - creates the route_dictionary that is used for the apc_matching for breeze data
  - **route.py** - builds route of megastops and contains methods to get information about the route
  - **stop.py** - contains different types to allow for different stops with different properties to be created
  - **stop_ball_tree.py** - provides stop friendly interface with sklearn R-Tree to find nearest neighbors
- *apc*
  - **apc.py** - Loads the automated personel counter data and process it to create a input data set
  - **bus_search.py** - implements a binary search to determine when a given passenger entered a bus
- **breeze_loader.py** - main file that calls each of the modules and puts all components together to create a cohesive data set to build from
- **rail_mapping_loader.py** - loads data from the rail map from station names to latitudes to the megastops

To be added:
- **trip_chaining.py** - used to trip chain for each breeze id over all the data
  - **network.py** - object that provides a central storage location for all of the routes and a easy interface to get information from  each of the routes


## Pipeline Diagram 

- **Coming Soon**
