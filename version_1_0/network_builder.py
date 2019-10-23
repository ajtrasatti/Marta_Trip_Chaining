"""
@author Joshua E. Morgan , jmorgan63@gatech.edu
Pascal Van Henteryck Lab
v_0.0
"""
from route import Route
from network import Network
import itertools as it
from StopBallTree import StopBallTree

class NetworkBuilder:
    """
    This implements the Builder function
    """

    def __init__(self, trans_limit):
        self.trans_limit = trans_limit

    def build_transitions(self, routes):
        """
        @redesign for 
        @optimize
        @test
        :param routes:
        :return:
        """

        for route1, route2 in it.combinations(routes.keys(),2):
            #This line is error
            _ = routes[route1].tree.query_radius(list(routes[route2].stops.values()),0,True)
            routes[route1].trans[route2] = routes[route1].tree.query_radius(list(routes[route2].stops.values()),0,True)
            routes[route2].trans[route1] = routes[route2].tree.query_radius(list(routes[route1].stops.values()),0,True)


    def build(self,megas_dict, id):
        """

        :param megas_dict: dic, containing "route_id": list like of stops
        :param id: int,
        :param dates:
        :return:
        """
        routes_dict = {k: Route(k,v) for k, v in megas_dict.items()}
        self.build_transitions(routes_dict)
        return Network(routes_dict, id)

