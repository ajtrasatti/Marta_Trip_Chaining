import time
import numpy as np
import pandas as pd
from collections import defaultdict
from .StopBallTree import StopBallTree
from .stop import Stop

global MAX_DISTANCE
MAX_DISTANCE = 500


class Network:
    def __init__(self, filename="../Data/MARTA_gtfs/all_stops.csv"):
        """
        Initialize the network object so that all the stops which other routes have stops that are close
        :param df_stops: a pandas df with cols ['stop_id', 'route_short_name', 'stop_lat', 'stop_lon']

        :attributes:
            # - stops_routes: dictionary {stop_id: routes}
            # - stops: [Stops]
            - stops_dict: {stop_id: Stop}
            - stops_routes_neighbors {stop_id: {route_id: {neighbor_stop_ids}}
        """
        cols = ['stop_id', 'route_short_name', 'stop_lat', 'stop_lon']    
        df_stops = pd.read_csv(filename)[cols].sort_values(["route_short_name", "stop_id"]).reset_index(drop=True)
        self.df_stops = df_stops
        groups = df_stops.groupby('stop_id')
        self.stops_routes = {stop_id: df_routes.route_short_name.values for stop_id, df_routes in groups}
        # print(stops_routes)
        self.error_check(df_stops)
        self.stops = self.make_stops(df_stops)
        self.id_stops = {s.stop_id: s for s in self.stops}

        self.stops_routes_neighbors = self.make_transitions(self.stops)
        print("MADE NETWORK")


    def error_check(self, df_stops):
        test1 = df_stops.drop_duplicates(subset=["stop_id","stop_lat","stop_lat"])
        test2 = df_stops.drop_duplicates(subset=["stop_id"])
        # test3 = df_stops.drop_duplicates(subset=["stop_lat","stop_lat"])
        if len(test1) != len(test2):
            # print("Error, multiple stops with same stop_id, but different lat-longs")
            print("test1", len(test1))
            print("test2", len(test2))
            # print("test3", len(test3))
            raise ValueError("Error, multiple stops with same stop_id, but different lat-longs")
            # exit()

    # @staticmethod
    # def make_stop(stop_id, lat, lon, routes):
    #     return Stop(stop_id, lat, lon, routes)

    def make_stops(self, df_stops):
        cols = ["stop_id", "stop_lat", "stop_lon"]
        temp = df_stops.drop_duplicates(subset=["stop_id", "stop_lat", "stop_lat"])
        return temp[cols].apply(lambda x: Stop(x[0], x[1], x[2], self.stops_routes[x[0]]), axis=1).values

    def make_transitions(self, stops):
        """
        :param stops: set or list of Stop objects 

        :attributes: 
            - ind_stops {ind: Stop}
            - ball_tree: StopBallTree(Stops) - finds neighbors within max distance
            - neighbors: [[stop_ids], [stop_ids], ...] index corresponds with ind_stop

        :return: dictionary of transitions for each stop {stop_id : {route_id : {neighbor_stop_ids}}}
        """
        # print(stops)
        stops = list(stops)
        ind_stops = {ind: s.stop_id for ind, s in enumerate(stops)}
        ball_tree = StopBallTree(stops)
        neighbors_arr = ball_tree.query_radius(stops, MAX_DISTANCE)
        stops_routes_neighbors = defaultdict(lambda: defaultdict(lambda: set()))

        # print(neighbors_arr)
        for stop_ind, neighbors in enumerate(neighbors_arr):
            neighbors_dict = defaultdict(lambda: set()) 
            for n_ind in neighbors:  # neighbor id
                n_stop_id = ind_stops[n_ind]  # neighbor stop id
                for route_id in self.stops_routes[n_stop_id]:
                    # changing rail names to 0 for now to represent "RAIL"
                    if route_id in ["BLUE", "RED", "GOLD", "GREEN"]:
                        route_id = 0
                    neighbors_dict[int(route_id)].add(int(n_stop_id))

            stop_id = int(ind_stops[stop_ind])
            stops_routes_neighbors[stop_id] = neighbors_dict

        return stops_routes_neighbors

    def get_transition(self, stop_id, route_id=None, ret_bool=False):
        stop_id = int(stop_id)
        if route_id is None:
            return self.stops_routes_neighbors[stop_id]
        else:
            route_id = int(route_id)  # changing rail names to numbers for now
            stops = self.stops_routes_neighbors[stop_id][route_id]
            if ret_bool:
                return len(stops) > 0  # returns if the set is non-empty i.e. if there exists a valid transfer
            else:
                return stops



def main():
    # filename = "mega_stops.csv"
    # filename = "/Users/anthonytrasatti/Desktop/Research/Marta/MARTA_gtfs_01_13_2018/stops.txt"
    # filename = "all_stops.csv"
    # df_stops = pd.read_csv(filename)[cols].sort_values(["route_short_name","stop_id"]).reset_index(drop=True)
    network = Network("../../Data/MARTA_gtfs/all_stops.csv")

    # print(test1[]

    print(network.df_stops.head())
    print(network.df_stops.columns)
    for x in network.get_transition(100004, 68): # print stops on route 68 close to stop 100004
        print(x)
    # print(network.neighbors)
    # print(network.stops_routes_neighbors)
    # stops_neighbors_dict = {int(s.stop_id):route_stop_dict(n) for s,n in list(zip(X,neighbors))[0:5]}
    # print(stops_neighbors_dict)

if __name__ == '__main__':
    main()
# print(count_values([len(x) for x in neighbors]))
# test = builder_class(neighbors).build()
# print(test)
# test = [test.pop() for i in range(10)]
