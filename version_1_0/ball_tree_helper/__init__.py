from sklearn.neighbors import BallTree
import numpy as np

class BallTreeHelper:

    def __init__(self):
        self.R = 3959.87433 * 5280

    def stop_2_tup(self,stops):
        """
        This function takes a list of stops and returns a set of tuples with postions in radians
        :param stops: list of stop.Stop objects
        :return: np.ndarray with [lat lon]
        """
        _ = np.asarray([(s.lat,s.lon) for s in stops])
        return np.radians(_)

    def build_ball_tree(self, route):
        """
        Constraucts a ball tree
        :param route:
        :return:
        """
        stops = self.stop_2_tup(route)
        return BallTree(stops, metric='euclidean')

    def get_neighbors(self, inbound, outbound, in_tree, out_tree):
        """
        this function finds the neighbors of a given object and returns them as a list with corrected indexes
        :param inbound: list of inbound facing stops
        :param outbound: list of outbound facing stops
        :param in_tree: sklearnBallTree for the inbound stops
        :param out_tree: sklearnBallTree for the outbound stops
        :return: list, of all pointers
        """
        result = out_tree.query(inbound)
        in_dist, in_matches = self.process_query_results(result)
        in_matches = self.correct_inbound_matches(in_dist, in_matches)
        result = in_tree.query(outbound)
        out_dist, out_matches = self.process_query_results(result)
        out_matches = self.correct_outboud_matches(out_dist, out_matches, len(inbound))
        return in_matches + out_matches

    def process_query_results(self, query_result):
        """
        This function takes takes the query results from sklearn and reformats them
        :param query_result: tuple, of lists with [[val],[val]]
        :return: tuple(distances, matches)
        """
        dist, matches = query_result
        dist = [self.R * x[0] for x in dist]
        matches = [x[0] for x in matches]
        return dist, matches

    def get_nearest(self, lat, lon, ball_tree):
        """
        this function takes in a lat and a l
        :return: megastop_id
        """
        _ = np.radians((lat, lon))
        return ball_tree.tree_stops[ball_tree.query(_)[0]]
