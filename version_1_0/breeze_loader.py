import pandas as pd
import numpy as np

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

    def match_rail_stops(self, rail_df, rail_mapping):
        """

        :param rail_df:
        :param rail_mapping:
        :param network:
        :return:
        """
        _ = rail_df.ctl_grp_short_desc.str.split('-').apply(lambda x: x[1].strip())
        rail_df.insert(len(rail_df.columns), 'STOP',
                       rail_df.ctl_grp_short_desc.str.split('-').apply(lambda x: x[1].strip()))
        rail_df.update(rail_df.STOP.str.upper())
        # print(rail_df.head())
        # print(rail_mapping.head())
        _ = rail_df.merge(rail_mapping,left_on='STOP',right_on='stop_name')
        # print(_.columns)
        header = ['Serial_Nbr', 'Transaction_dtm', 'Dev_Operator', 'ctl_grp_short_desc', 'use_type_desc', 'bus_id',
                  'route_no', 'route_name', 'MEGA_STOP']
        # print("MEGA_STOP" in _.columns)
        return _[header]
        #return _

    # def match_2_apc(self, bus_df, apc_df):
    #     """
    #     this function matches the breeze and apc data frames
    #     :param bus_df:
    #     :param apc_df:
    #     :return: pd.DataFrame containing the breeze data with the stops
    #     """
    #     apc_df = apc_df.sort_values(by='ARRIVAL_DTM')
    #     apc_g = apc_df.groupby("VECHILE_TAG")
    #     bus_g = bus_df.groupby('bus_id')
    #     buses = list(pd.unique(apc_df['VECHILE_TAG']))
    #
    #     def get_lat_lon(df, row):
    #         """
    #         note this function could be replaced by building a set of cutpoints and constraints
    #         Then implementing a search tree to determine the location of a given route in this space
    #         """
    #         return df.loc[(df['ARRIVAL_DTM'] - row.Transaction_dtm).abs().idxmin(), "MEGA_STOP"]
    #
    #     for bus in buses:
    #         if bus in bus_g.groups:
    #             temp1 = apc_g.get_group(bus)
    #             temp2 = bus_g.get_group(bus)
    #             bus_df.loc[temp2.index, 'STOP_ID'] = temp2.apply(lambda row: get_lat_lon(temp1, row), axis=1)
    #     return bus_df


    def apc_match(self, breeze_df, bus_searches):
        """
        New updated version of the APC match function
        :param bus_trees:
        :return:
        """
        removed = []
        breeze_df = breeze_df.sort_values(by='Transaction_dtm')
        stops= []
        times = []
        routes = []
        for tup in breeze_df.itertuples():
            if tup.bus_id in bus_searches.keys():
                search = bus_searches[tup.bus_id]
                _ = search.find_stop_route(tup.Transaction_dtm)
                if abs(tup.Transaction_dtm - _[0]).seconds <= 600:
                    times.append(_[0])
                    stops.append(_[1])
                    routes.append(_[2])
                else:
                    removed.append(tup.bus_id)
                    stops.append(np.nan)
                    times.append(np.nan)
                    routes.append(np.nan)
            else:
                removed.append(tup.bus_id)
                stops.append(np.nan)
                times.append(np.nan)
                routes.append(np.nan)

        breeze_df.insert(len(breeze_df.columns),'MEGA_STOP', stops)
        # breeze_df.insert(len(breeze_df.columns),"APC_TIME", times)
        # breeze_df.insert(len(breeze_df.columns),"APC_ROUTES",routes)

        return breeze_df

    def apc_test_stats(self, df):
        """

        :param df:
        :return:
        """
        # calculating time
        temp = df[pd.notnull(df.APC_TIME)]
        print(pd.notnull(df.APC_TIME).sum()/df.shape[0])
        temp1 = abs(temp.Transaction_dtm - temp.APC_TIME)
        temp.insert(len(temp.columns), 'diff', temp1.apply(lambda x: x.seconds// 60))
        temp.to_csv('apc_df_val.csv')
        print(temp.describe())



