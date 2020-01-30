"""
@author Anthony J. Trasatti , atrasatti3@gatech.edu
@author Joshua E. Morgan , jmorgan63@gatech.edu
Socially Aware Mobility (SAM) Lab, Georgia Tech
v_1.0
"""

from .bus_search import BusSearch
import pandas as pd
# import haversine
from geo import haversine_feet

BUS_TO_STOP_DIST = 1000  # global param to add to file


class APC:
    """
    This file loads the apc data and finds the mega stops for each row
    Then you can get the bus_search dictionary to use to find the time passengers got on buses
    """

    def __init__(self, filename):
        """
        :param filename: apc_test.csv where a days worth of apc data is kept
        """
        self.df = pd.read_csv(filename)
        self.df.ARRIVAL_DTM = pd.to_datetime(self.df.ARRIVAL_DTM, format="%Y-%m-%d %H:%M:%S")
        self.df.DEPARTURE_DTM = pd.to_datetime(self.df.DEPARTURE_DTM, format="%Y-%m-%d %H:%M:%S")
        # self.join_megas()  # add megas to self.df

    def get_route_tree(self, routes_dict, route_id):
        """
        :param routes_dict: dictionary {route_id : Route(route_id)}
        :param route_id:
        :return:
        """
        if route_id in routes_dict.keys():
            return routes_dict[route_id].tree
        else:
            return -1

    def join_megas(self, routes_dict, test=False):
        """
        :param routes_dict: dictionary {route_id : Route(route_id)}
        :param test: to be removed

        :return: number of skipped rows if test
        """
        x = []
        bad = 0
        for tup in self.df.itertuples():
            tree = self.get_route_tree(routes_dict, str(tup.ROUTE_ABBR))
            if type(tree) != int:
                # tree_query - returns the mega stop, .id access the id of the mega stop
                ms = tree.query_point(tup.LATITUDE, tup.LONGITUDE)
                if haversine_feet(ms.lat, ms.lon, tup.LATITUDE, tup.LONGITUDE) < BUS_TO_STOP_DIST:
                    x.append(ms.stop_id)
                else:
                    x.append("No nearby stop on route")
            else:
                bad += 1
                x.append("NO_ROUTE_INFO")  # IF ROUTE NOT FOUND IN GTSF

        # if test:
        #     return bad
        print("NOT FOUND PERCENT IN APC LOADER", bad / len(self.df))  # to be out puted into a stats csv/excel
        self.df["stop_id"] = x
        # return self.df

    def get_apc_df(self):
        return self.df

    def export_apc_df(self, filename):
        self.df.to_csv(filename)

    def get_bus_search_dict(self):
        """
        This
        :param apc_df:
        :return:
        """
        return {vehicle_id: BusSearch(df) for vehicle_id, df in self.df.groupby("VECHILE_TAG")}

    # -------- Below is unused
    # def combine_stops(self, apc_df, time_limit):
    #     """
    #     This function combines stops with the same mega stop in a row to merge alighting
    #     and boarding for the given stop
    #
    #     :param time_limit: int, is the difference in time that determines if the values will not be updated
    #     :return: apc_df, with the associated additions
    #     """
    #     for name, group in apc_df.groupby.VECHILE_TAG:
    #         group = group.sort_values(by='ARRIVAL_DTM')
    #         # calculates lag for the group
    #
    #         # checks to see if lag and stop meet constraints
    #
    #         # adds together



