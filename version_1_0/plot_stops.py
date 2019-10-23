"""
@author Joshua E. Morgan, jmorgan63@gatech.edu
Pascal Van Henteryck Lab
v_0.0
"""
import folium

class PlotStops:
    """
    Plots stops creates plots of stops using folium plotting software

    Attributes:
        - start_coords - location where the map will begin at
        - m - folium map object
    """
    def __init__(self, lat=33.749, lon=-84.3880):
        """

        :param lat: float, for latitude of starting point
        :param lon: float, for longitude of startinpoin
        """
        self.start_coords = (lat, lon)
        self.m  = folium.Map(location= self.start_coords, zoom_start=14)

    def add_stop(self, stop):
        """
        Adds a stop to the folium map
        :param stop: stop.Stop Object, contains information about a single bus or train stop
        :return: None
        """
        #folium.Marker(location=(stop.lat, stop.lon), icon=folium.Icon(icon='bus', color='blue'),
        #              popup="<i>Stop: {}</i>".format(stop.id)).add_to(self.m)
        folium.Circle(location=(stop.lat, stop.lon),radius=213).add_to(self.m)

    def add_mega(self, stop,circle=True):
        """
        Adds a megastop to the folium map
        :param stop: stop.MegaStop Object, contains information about a set of stops grouped into a megastop
        :return: None
        """
        folium.Marker(location=(stop.lat, stop.lon), icon=folium.Icon(icon='bus', color='green'),
                      popup="<i>Mega Stop: {}</i>".format(stop.id)).add_to(self.m)
        if circle:
            folium.Circle(location=(stop.lat, stop.lon), radius=122).add_to(self.m)

    def export(self, path_out):
        """
        Exports the given map to a specfic file must be html
        :param path_out: path object detailing where the file will be loaded too
        :return:
        """
        self.m.save(path_out)
