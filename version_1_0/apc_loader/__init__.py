
import pandas as pd
import bisect

class APC_Loader:

    def __init__(self,network = None):
        """

        :param network:
        """
        self.network = network

    def load_apc(self,path):
        """

        :param path:
        :return:
        """
        return pd.read_pickle(path)


    def get_route_tree(self,route_id):
        """

        :param route_id:
        :return:
        """
        if route_id in self.network.routes.keys():
            return self.network.routes[route_id].tree
        else:
            return -1

    def join_megas(self, apc_df, test=False):
        """

        :param apc_df:
        :return: number of skipped rows
        """
        x = []
        bad = 0
        for tup in apc_df.itertuples():
            tree = self.get_route_tree(str(tup.ROUTE_ABBR))
            if type(tree) != int:
                x.append(tree.query_point(tup.LATITUDE, tup.LONGITUDE).id)
            else:
                bad += 1
        if test:
            return bad
        apc_df.insert(len(apc_df.columns),"MEGA_STOP",x)
        return apc_df

    def combine_stops(self, apc_df, time_limit):
        """
        This function combines stops with the same mega stop in a row to merge alighting and boarding for the given stop
        :param time_limit: int, is the difference in time that determines if the values will not be updated
        :return: apc_df, with the associated additions
        """
        for name, group in apc_df.groupby.VECHILE_TAG:
            group = group.sort_values(by='ARRIVAL_DTM')
            #calculates lag for the group

            # checks to see if lag and stop meet constraints

            # adds together

    def build_bus_tree(self,bus_df):
        pass

    def build_bus_trees(self, apc_df):
        return {self.build_bus_tree(group) for name, group in apc_df.groupby("VECHILE_TAG")}


class BusTree:

    def __init__(self, stops, routes, times):
        time_tups = sorted([(i,t) for i, t in enumerate(times)])
        self.times = [t for id,t in time_tups]
        self.ids = [id for id,t in time_tups]
        self.stops = stops
        self.routes = routes

    def find_time_index(self, time):
        """

        :param time:
        :return:
        """
        return bisect.bisect_right(self.times, time)

    def find_stop_route(self, time):
        """

        :param time:
        :return: tuple of times, stops, routes
        """
        index = self.find_time_index(time)
        if index == 0:
            # ensures that the first time is used
            loc = index
        elif index == len(self.times):
            # ensures that the last time is used
            loc = index - 1
        else:
            #checks to see which one is closest
            pass

        return (self.times[index], self.stops[self.ids[index]], self.routes[self.ids[index]])



