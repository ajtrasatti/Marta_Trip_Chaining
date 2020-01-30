"""
@author Anthony J. Trasatti , atrasatti3@gatech.edu
@author Joshua E. Morgan , jmorgan63@gatech.edu
Socially Aware Mobility (SAM) Lab, Georgia Tech
v_1.0
"""

import pandas as pd
import numpy as np
import csv

from parameters import BREEZE_TAP_TIME_WINDOW

class BreezeLoader:
    def load_breeze(self, path):
        """
        this function loads a path for the breeze data
        :param path: os.path object
        :return: pd.DataFrame
        """
        return pd.read_pickle(path)

    def get_marta_only(self, breeze_df):
        """
        This function removes the data from other tranist agencies
        :return: pd.DataFrame containing the cleaned breeze data
        """
        return breeze_df[(breeze_df['Dev_Operator'].str.contains('MARTA'))]

    def split_tranist(self, breeze_df):
        """

        :param breeze_df:
        :return:
        """
        marta_df = breeze_df[(breeze_df['Dev_Operator'].str.contains('MARTA'))]
        other_df = breeze_df[~(breeze_df['Dev_Operator'].str.contains('MARTA'))]
        return marta_df, other_df

    def split_frame(self, breeze_df, parking=False):
        """
        This function splits data into the a rail data frame and a bus data frame
        :param breeze_df: pd.DataFrame containing raw breeze data
        :param parking: bool, that determines whether or not to return the parking data set
        :return:
        """
        bus_df = breeze_df[pd.notnull(breeze_df['bus_id'])]
        rail_df = breeze_df[~(pd.notnull(breeze_df['bus_id']))]
        parking_df = rail_df[rail_df.Dev_Operator.str.contains('Parking')]
        rail_df = rail_df[~(rail_df.Dev_Operator.str.contains("Parking"))]
        if parking:
            return (bus_df, rail_df,parking_df)
        else:
            return (bus_df,rail_df)

    def apc_match(self, bus_df, bus_searches, verbose=True):
        """
        New updated version of the APC match function
        :param bus_df: the data frame with bus_df
        :param bus_searches:
        :param verbose: print more details
        :return:
        """
        removed = []
        bus_df = bus_df.sort_values(by='Transaction_dtm')
        # bus_df = bus_df[bus_df.Dev_Operator == "MARTA Bus"]
        stops = []
        bad_time = 0
        bad_bus_id = 0
        # times = []
        # routes = []
        for tup in bus_df.itertuples():
            if tup.bus_id in bus_searches.keys():
                bus_search = bus_searches[tup.bus_id]
                time, stop, route_id = bus_search.find_stop_route(tup.Transaction_dtm, tup.route_no)
                if tup.route_no != route_id:
                    stops.append("route id different")
                else:
                    if abs(tup.Transaction_dtm - time).seconds <= BREEZE_TAP_TIME_WINDOW:
                        stops.append(stop)
                        # times.append(time)
                        # routes.append(route)
                    else:
                        removed.append(tup.bus_id)
                        # print(tup)
                        stops.append("time difference too large")
                        bad_time += 1

                        # times.append(np.nan)
                        # routes.append(np.nan)
            else:
                removed.append(tup.bus_id)
                stops.append("bus id not found")
                bad_bus_id += 1
                # times.append(np.nan)
                # routes.append(np.nan)

        bus_df["stop_id"] = stops
        # breeze_df.insert(len(breeze_df.columns),"APC_TIME", times)
        # breeze_df.insert(len(breeze_df.columns),"APC_ROUTES",routes)

        if verbose:
            def error_stats(df_col, e):
                if len(df_col) != 0:
                    l1 = sum(df_col == e)
                    l2 = len(df_col)
                    error_per = l1 / l2 * 100
                    print(e, l1, l2, error_per, "%")
            for x in ["time difference too large", "bus id not found",
                      "No nearby stop on route", "route id not found for vehicle",
                      "route id different"]:
                error_stats(bus_df.stop_id, x)
            # print("bad_time ", f"{bad_time}, {len(bus_df)}, {bad_time/len(bus_df) * 100:.3f}%")
            # print("bad_bus_id ", f"{bad_bus_id}, {len(bus_df)}, {bad_bus_id / len(bus_df) * 100:.3f}%")

        return bus_df

    def match_rail_stops(self, rail_df, rail_mapping):
        """
        :param rail_df:
        :param rail_mapping:
        :param network:
        :return:
        """
        # Pull out the names of (ex. names Gate - North Springs)
        rail_df["stop_name"] = rail_df.ctl_grp_short_desc.str.split('-').apply(lambda x: x[1].split(',')[0].strip())
        rail_df.update(rail_df.stop_name.str.upper())
        rail_df = rail_df[rail_df["stop_name"] != "TEST"]

        len_before = len(rail_df)  # For error checking
        first_set = set(rail_df.stop_name)  # For error checking

        rail_df = rail_df.merge(rail_mapping, left_on='stop_name', right_on='stop_name')

        # for testing
        # temp = rail_df.merge(rail_mapping, how='left', left_on='STOP', right_on='stop_name')
        if len_before != len(rail_df):
            print(len_before, len(rail_df))
            second_set = set(rail_df.stop_name)
            print(sorted(first_set))
            print(sorted(second_set))
            raise ValueError('error with rail stop mapping')
            exit()

        header = ['Serial_Nbr', 'Transaction_dtm', 'Dev_Operator', 'ctl_grp_short_desc', 'use_type_desc', 'bus_id',
                  'route_no', 'route_name', 'stop_id']
        rail_df = rail_df[header]
        return rail_df

    #
    # def apc_test_stats(self, df):
    #     """
    #
    #     :param df:
    #     :return:
    #     """
    #     # calculating time
    #     temp = df[pd.notnull(df.APC_TIME)]
    #     print(pd.notnull(df.APC_TIME).sum()/df.shape[0])
    #     temp1 = abs(temp.Transaction_dtm - temp.APC_TIME)
    #     temp.insert(len(temp.columns), 'diff', temp1.apply(lambda x: x.seconds // 60))
    #     temp.to_csv('apc_df_val.csv')
    #     print(temp.describe())



