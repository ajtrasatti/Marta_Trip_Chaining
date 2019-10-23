"""
@author Joshua E. Morgan , jmorgan63@gatech.edu
Pascal Van Henteryck Lab
v_0.0
"""

from sklearn.neighbors import BallTree
from collections import defaultdict
from stop import MegaStop
from union_find import UnionFind
import numpy as np
from StopBallTree import StopBallTree
from math import radians, degrees


class MegaStopFac:
    """
    This is the MegaStop factory class which builds megastops when given data
    Attributes
        - limit - the limited distance between two positions on the globe
        - count - the number of megastops made
    """

    def __init__(self, limit):
        """
        :param limit: float, that limits the values between stops
        """
        self.R = 3959.87433 * 5280 # radius of the earth in feet
        self.limit = limit
        self.count = 0

    def build_ball_tree(self, inbound, outbound):
        """
        This function builds ball trees from the space
        :param inbound: ndarray of lat and lon values
        :param outbound: ndarray of lat and lon values
        :return: tuple of sklearn balltree objects
        """
        inbound_tree = BallTree(inbound, metric='haversine')
        outbound_tree = BallTree(outbound, metric='haversine')
        return inbound_tree, outbound_tree

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


    def correct_inbound_matches(self, in_dist, in_matches):
        """
        This function ensures that the distance between stops is correct.
        :param in_dist:
        :param in_matches:
        :return: list, of stops that are being pointed at
        """
        length = len(in_matches)
        for i, dist in enumerate(in_dist):
            if dist <= self.limit:
                in_matches[i] = in_matches[i] + length
            else:
                in_matches[i] = i
        return in_matches


    def correct_outboud_matches(self, out_dist, out_matches, length):
        """
        This function removes stops that are out of range
        in terms of distance and readjusts indices to math the inbound funtion
        :param out_dist: list, containing distance between nearest neighbor
        :param out_matches: list, containing index of nearest neighbor
        :param length: list, length of the opposing route
        :return: list, of the partners
        """
        for i, dist in enumerate(out_dist):
            if dist > self.limit:
                out_matches[i] = i + length
        return out_matches

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

    def union_find(self, partners):
        """
        This function  uses the union find to find the representative element of every class
        :param partners: list of stops a given stop is partnered with
        :return:
        """
        # make set or bijection of partners to indices this has already occured
        uf = UnionFind(partners)
        for i,j in enumerate(partners):
            uf.union(i,j)
        return uf.ids

    def get_groups(self, partners):
        """
        This function take a bunch of numbers and creates a map of number to the indexes it occurs at
        :param partners: list of integers
        :return: dict{group_repr:[index1, index2]}
        """
        groups = defaultdict(list)
        for i, x in enumerate(partners):
            groups[x].append(i)
        return groups

    def build_mega_stops(self, groups,stops):
        """
        This function builds megastops from a set of grouped data points and stops
        :param groups: dict, {repr: [index, index]}
        :param stops: list, [stop1,stop2]
        :return: [megas_stop1, mega_stop2]
        """
        mega_stops= []
        for group in groups.values():
            s = [stops[x] for x in group]
            mega_stops.append(MegaStop("M"+str(self.count),s))
            self.count += 1
        return mega_stops


    def stop_2_tup(self,stops):
        """
        This function takes a list of stops and returns a set of tuples with postions in radians
        :param stops: list of stop.Stop objects
        :return: np.ndarray with [lat lon]
        """
        _ = np.asarray([(s.lat,s.lon) for s in stops])
        return np.radians(_)


    def get_mega_stops(self, inbound, outbound):
        """
        This function builds all of the different megastops
        #note testing is visual for this function
        :param inbound: a list of stop objects in the same direction
        :param outbound: a list of stop objects in the opposite direction
        :return: a list of mega stops
        """
        if len(inbound) == 0 and len(outbound) == 0:
            return []
        elif len(inbound) == 0:
            return [MegaStop(stop.id, [stop]) for stop in outbound]
        elif len(outbound) == 0:
            return [MegaStop(stop.id, [stop]) for stop in inbound]
        inbound_tups = self.stop_2_tup(inbound)
        outbound_tups = self.stop_2_tup(outbound)
        # build a kd tree out of all of the stops
        inbound_tree, outbound_tree = self.build_ball_tree(inbound_tups, outbound_tups)
        stops = inbound + outbound
        unions = self.get_neighbors(inbound_tups, outbound_tups, inbound_tree, outbound_tree)
        grouped = self.union_find(unions)
        groups = self.get_groups(grouped)
        return self.build_mega_stops(groups, stops)

    def get_train_mega_stops(self,inbound, outbound):
        """

        :param inbound:
        :param outbound:
        :return:
        """
        outbound = [s for s in outbound if s not in inbound]
        inbound_tups = self.stop_2_tup(inbound)
        outbound_tups = self.stop_2_tup(outbound)
        inbound_tree, outbound_tree = self.build_ball_tree(inbound_tups, outbound_tups)
        stops = inbound + outbound
        unions = self.get_neighbors(inbound_tups, outbound_tups, inbound_tree, outbound_tree)
        grouped = self.union_find(unions)
        groups = self.get_groups(grouped)
        return self.build_mega_stops(groups, stops)