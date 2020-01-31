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
        This method matches the non-rail (bus) breeze data to the apc data
        - It uses the vehilce id and time to
        :param bus_df: the data frame with bus_df
        :param bus_searches: {bus_id : BusSearch(bus_id, apc_df)}
        :param verbose: print more details
        :return:
        """
        removed = []
        bus_df = bus_df.sort_values(by='Transaction_dtm')
        # bus_df = bus_df[bus_df.Dev_Operator == "MARTA Bus"]

        stops = []
        arr_times = []
        dep_times = []
        routes = []
        directions = []
        errors = []
        lists = [stops, arr_times, dep_times, routes, directions]

        for tup in bus_df.itertuples():
            if tup.bus_id in bus_searches.keys():
                bus_search = bus_searches[tup.bus_id]  # get BusSearch object corresponding to that bus_id
                trans_time = tup.Transaction_dtm
                # apc_row is pandas row with: stop_id, ROUTE_ABBR, ARRIVAL_DTM, DEPARTURE_DTM
                apc_row = bus_search.find_apc_row(trans_time)  # find the row in apc near that time

                # Error checking
                error = np.nan
                arr_time = apc_row.ARRIVAL_DTM
                dep_time = apc_row.DEPARTURE_DTM
                if trans_time < dep_time or abs(trans_time - dep_time).seconds <= BREEZE_TAP_TIME_WINDOW:
                    if tup.route_no != apc_row.ROUTE_ABBR:
                        error = "route id different"
                else:
                    error = "time difference too large"

                stops.append(apc_row.stop_id)
                arr_times.append(arr_time)
                dep_times.append(dep_time)
                routes.append(apc_row.ROUTE_ABBR)
                directions.append(apc_row.ROUTE_DIRECTION_NAME)
                errors.append(error)
            else:
                errors.append("bus id not found")
                for arr in lists:
                    arr.append(np.nan)

        bus_df["stop_id"] = stops
        bus_df["MATCH_ARRIVAL_TIME"] = arr_times
        bus_df["MATCH_DEPARTURE_TIME"] = dep_times
        bus_df["MATCH_ROUTE"] = routes
        bus_df["MATCH_DIRECTION"] = directions
        bus_df["MATCH_ERROR"] = errors

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
                error_stats(bus_df.MATCH_ERROR, x)

        return bus_df

    def match_rail_stops(self, rail_df, rail_mapping):
        """
        :param rail_df:
        :param rail_mapping:
        :return:
        """
        # Pull out the names of (ex. names Gate - North Springs)
        rail_df["stop_name"] = rail_df.ctl_grp_short_desc.str.split('-').apply(lambda x: x[1].split(',')[0].strip())
        rail_df.update(rail_df.stop_name.str.upper())
        rail_df = rail_df[rail_df["stop_name"] != "TEST"]  # Had some nn-TEST that we wanted to ignore

        len_before = len(rail_df)  # For error checking
        first_set = set(rail_df.stop_name)  # For error checking

        rail_df = rail_df.merge(rail_mapping, on='stop_name')

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

        rail_df["MATCH_ARRIVAL_TIME"] = rail_df["Transaction_dtm"]
        rail_df["MATCH_DEPARTURE_TIME"] = [np.nan] * len(rail_df)
        rail_df["MATCH_ROUTE"] = [0] * len(rail_df)
        rail_df["MATCH_DIRECTION"] = ["RAIL"] * len(rail_df)
        rail_df["MATCH_ERROR"] = [np.nan] * len(rail_df)
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



