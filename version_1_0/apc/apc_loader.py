
import pandas as pd
from .bus_search import BusSearch

class APC_Loader:
    """
    This file loads the apc data and preprocesses it
    """

    def __init__(self,network = None):
        """

        :param network:
        """
        self.network = network

    def load_apc(self,filename):
        """

        :param path:
        :return:
        """
        # import pickle
        # x = pickle.Unpickler("apc_test.pick")
        # print(x.load().head())
        #
        # return pd.read_pickle(path)

        return pd.read_csv(filename, parse_dates=["ARRIVAL_DTM"])


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
                # tree_query - returns the mega stop, .id access the id of the megastop
                ms = tree.query_point(tup.LATITUDE, tup.LONGITUDE)
                x.append(ms.id)
            else:
                bad += 1
                x.append("NO_ROUTE_INFO") # IF ROUTE NOT FOUND IN GTSF
        if test:
            return bad
        print("NOT FOUND PERCENT IN APC LOADER", bad/len(apc_df))
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

    def build_bus_search(self,bus_df):
        """
        This
        :param bus_df:
        :return:
        """
        # print(bus_df.columns)
        times = list(bus_df.ARRIVAL_DTM)
        stops = list(bus_df.MEGA_STOP)
        routes = list(bus_df.ROUTE_ABBR)
        return BusSearch(stops, routes, times)

    def build_search_dict(self, apc_df):
        """
        This
        :param apc_df:
        :return:
        """
        return {name: self.build_bus_search(group) for name, group in apc_df.groupby("VECHILE_TAG")}






