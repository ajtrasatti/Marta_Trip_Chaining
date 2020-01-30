"""
@author Anthony J. Trasatti , atrasatti3@gatech.edu
@author Joshua E. Morgan , jmorgan63@gatech.edu
Socially Aware Mobility (SAM) Lab, Georgia Tech
v_1.0
"""
from sklearn.neighbors import BallTree
import numpy as np


def stop_2_rads_tup(stops):
    """
    This function takes a list of stops and returns a set of tuples with lat longs in radians instead of degrees
    :param stops: list of stop objects
    :return: np.ndarray with [lat lon]
    """
    temp = np.asarray([(s.lat, s.lon) for s in stops])
    return np.radians(temp)


class StopBallTree:
    """
    This class is a stop friendly implementation of a sklearn ball-tree
    distances (in feet) are converted to radians, to be used with stops which have lat_longs
    """

    def __init__(self, stops):
        """
        :param stops: list of Stop objects
        """
        self.tree = BallTree(stop_2_rads_tup(stops), metric='haversine')
        self.tree_stops = list(stops)
        self.R = 3959.87433 * 5280

    def query(self, stops):
        """
        This function takes takes the query results from sklearn and reformats them
        :param stops: tuple, of lists with [[val],[val]]
        :return: tuple(distances, matches)
        """
        print(stop_2_rads_tup(stops))
        dist, matches = self.tree.query(stop_2_rads_tup(stops))
        dist = [self.R * x[0] for x in dist]
        matches = [x[0] for x in matches]
        return dist, matches

    def query_radius(self, stops, radius, earth=True):
        """
        Interface for stops with the sklearn query_radius function
        :param stops: list of mega_stops
        :param radius: maximum walking radius around a stop (in feet)
        :param earth: if lat_longs then this is TRUE and the r has to be in unit radians
        :return:
        """

        r = radius/self.R  # need to convert radius into radians distance
        ind = self.tree.query_radius(stop_2_rads_tup(stops), r=r)
        return {stops[i]: [self.tree_stops[j] for j in ind[i]] for i in range(len(stops))}

    def query_point(self, lat, lon):
        """
        this function queries a given point in lat and lon and returns the nearest stop object
        :param lat:
        :param lon:
        :return:
        """

        rads = np.radians((lat, lon))
        matches = self.tree.query(rads.reshape(1, -1), return_distance=False)
        return self.tree_stops[matches[0][0]]




