# Marta Trip Chaining

## Objective:
To build a software to build from transaction data and automated personel counter data to a origin destination matrix for marta system improvements and optimization

## File Descriptions
- **odx** - main file that calls each of the modules and puts all components together to create a cohesive data set to build from
- **apc_loader** - Loads the automated personel counter data and process it to create a input data set
- **bus_search** - implements a binary search to determine when a given passenger entered a bus
- **extract_test** - creates the test data from the raw data files
- **mega_stop_fac** - factory pattern that builds megastops 
- **network** - object that provides a central storage location for all of the routes and a easy interface to get information from  each of the routes
- **odx_2_html** - interface between odx system and folium for plotting
- **rail_mapping_loader** - loads data from the rail map from station names to latitudes to the megastops
- **rail_stop_fac** - builds rail mega_stops from data
- **route** - builds route of megastops and contains methods to get information about the route
- **stop** - contains different types to allow for different stops with different properties to be created
- **stop_ball_tree** - provides stop friendly interface with sklearn R-Tree to find nearest neighbors
- **test** - directory containing all unit tests and integration tests
- **union_find** - implementation of union_find algorithm for mega_stop pairing

## Pipleine Diagram 

- **Coming Soon**
