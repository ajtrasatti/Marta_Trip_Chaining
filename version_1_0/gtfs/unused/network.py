"""
@author Anthony J. Trasatti , atrasatti3@gatech.edu
@author Joshua E. Morgan , jmorgan63@gatech.edu
Socially Aware Mobility (SAM) Lab, Georgia Tech
v_1.0
"""
import itertools as it
import os
from version_1_0.gtsf.route import Route


class Network:
    """
    This is the network class which will store all of the data associated with the different routes.
    - look up a given route and find the set of stops
    - look up a route_id, stop_id and get the stop
    - look up a route_id, stop_id and get the valid transitions
    - be easily stored in a json format
    - be stored in a pickle format
    - The constructor should be able to be run in batch over all gtfs days
        to build a search tree to find the directory for a given day
    """

    def __init__(self, route_mega_dict, trans_limit, service_id, dates=None):
        """

        :param route_mega_dict: dictionary {route_id : [stops]}
        :param trans_limit: max distance allowed for transition
        :param dates: tup, (dt.datetime, dt.datetime, weekend) used to determine which days are valid

        create routes_dict : dictionary {route_id : Route([stops])
        """

        self.trans_limit = trans_limit
        self.routes_dict = {route_id: Route(route_id, stops) for route_id, stops in route_mega_dict.items()}
        # self.build_transitions()
        # self.service_id = service_id
        # self.dates = dates

    # def find_stop(self, route_id, stop_id):
    #     """
    #     This function finds a given stop given its identifiers
    #     :param route_id:
    #     :param stop_id:
    #     :return: MegaStop
    #     """
    #     return self.routes_dict[route_id].stops[stop_id]

    # def build_transitions(self, route_mega_dict):
    #     """
    #     :param route_mega_dict: dictionary {route_id : [MegaStop]}
    #     :return: routes_dict: {route_id : Route(route_id,[MegaStop])}
    #     """
    #     routes_dict =
    #
    #     # for route1, route2 in it.combinations(routes_dict.keys(), 2):
    #     #     # routes[route1] is a Route object
    #     #     l1 = list(routes_dict[route2].stops.values())
    #     #     l2 = list(routes_dict[route1].stops.values())
    #     #
    #     #     stop_ball_tree = routes_dict[route1].tree
    #     #     routes_dict[route1].trans[route2] = stop_ball_tree.query_radius(l1, self.trans_limit, True)
    #     #     stop_ball_tree = routes_dict[route2].tree
    #     #     routes_dict[route2].trans[route1] = stop_ball_tree.query_radius(l2, self.trans_limit, True)
    #
    #     return routes_dict

    # def get_transition(self, route_id1, route_id2, stop_id):
    #     """
    #     look up a route_id, stop_id and get the valid transitions
    #     :param route_id:
    #     :param stop_id:
    #
    #     transitions is the return of the StopBallTree query_radius function
    #
    #     :return: list of possible transitions from that route_id1 to stop_id
    #     """
    #     transitions = self.routes_dict[route_id1].trans[route_id2]  #
    #     if stop_id in transitions:
    #         return transitions[stop_id]
    #     else:
    #         return []
    #
    # def export_transition(self, path):
    #     """
    #     This is a test functi
    #     :param path:
    #     :return:
    #     """
    #     cur = os.path.abspath(os.getcwd())
    #     test = os.path.abspath(os.path.join(cur,'Test'))
    #     with open(os.path.join(test,path),'w') as fout:
    #         import csv
    #         writer = csv.writer(fout)
    #         writer.writerow(['ROUTE','STOP_ID','TRANS_STOPS'])
    #         for ind, r in self.routes_dict.items():
    #             for s, o in r.trans.items():
    #                 writer.writerow([ind, str(s), [str(x) for x in o]])

    # def to_json(self,path_out):
    #     """
    #     be easily stored in a json format
    #     :param path_out:
    #     :return:
    #     """
    #     pass
    #
    # def to_pickle(self,path_out):
    #     pass
