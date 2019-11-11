"""
@todo build new interface for ball tree with megastops
"""
from sklearn.neighbors import BallTree
import numpy as np

class StopBallTree:
    """
    This class is a stop friendly implementation of a sklearn ball-tree
    """

    def __init__(self, stops):
        """

        :param stops: list of Stop objects
        """
        self.tree = BallTree(self.stop_2_tup(stops),metric='haversine')
        self.tree_stops = list(stops)
        self.R = 3959.87433 * 5280

    def stop_2_tup(self,stops):
        """
        This function takes a list of stops and returns a set of tuples with postions in radians
        :param stops: list of stop.Stop objects
        :return: np.ndarray with [lat lon]
        """
        _ = np.asarray([(s.lat,s.lon) for s in stops])
        return np.radians(_)

    def query(self, stops):
        """
        This function takes takes the query results from sklearn and reformats them
        :param query_result: tuple, of lists with [[val],[val]]
        :return: tuple(distances, matches)
        """
        print(self.stop_2_tup(stops))
        dist, matches = self.tree.query(self.stop_2_tup(stops))
        dist = [self.R * x[0] for x in dist]
        matches = [x[0] for x in matches]
        return dist, matches

    def query_radius(self, stops, radius,earth=False):
        """
        Interface for stops with the sklearn query_radius function
        :param stops:
        :return:
        """
        if earth:
            ind = self.tree.query_radius(self.stop_2_tup(stops), r = radius/self.R )
        else:
            ind = self.tree.query_radius(self.stop_2_tup(stops), r=radius)
        # need to convert radius into radians distance
        return {stops[i]:[self.tree_stops[j] for j in ind[i]] for i in range(len(stops))}

    def query_point(self, lat, lon):
        """
        this function querys a given point in lat and lon and returns the nearest stop object
        :param lat:
        :param lon:
        :return:
        """
        _ = (lat, lon)
        _ = np.radians(_)
        matches = self.tree.query(_.reshape(1,-1),return_distance=False)
        return self.tree_stops[matches[0][0]]




