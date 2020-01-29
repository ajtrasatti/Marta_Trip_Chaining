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

    def apc_match(self, bus_df, bus_searches):
        """
        New updated version of the APC match function
        :param bus_df: the data frame with bus_df
        :param bus_searches:
        :return:
        """
        removed = []
        bus_df = bus_df.sort_values(by='Transaction_dtm')
        stops = []
        # times = []
        # routes = []
        for tup in bus_df.itertuples():
            if tup.bus_id in bus_searches.keys():
                bus_search = bus_searches[tup.bus_id]
                time, stop, route = bus_search.find_stop_route(tup.Transaction_dtm)
                if abs(tup.Transaction_dtm - time).seconds <= 600:
                    stops.append(stop)
                    # times.append(time)
                    # routes.append(route)
                else:
                    removed.append(tup.bus_id)
                    stops.append("time difference too large")
                    # times.append(np.nan)
                    # routes.append(np.nan)
            else:
                removed.append(tup.bus_id)
                stops.append("bus id not found")
                # times.append(np.nan)
                # routes.append(np.nan)

        # if test:
            # handle error ones

        bus_df["MEGA_STOP"] = stops
        # breeze_df.insert(len(breeze_df.columns),"APC_TIME", times)
        # breeze_df.insert(len(breeze_df.columns),"APC_ROUTES",routes)

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
        len_before = len(rail_df)
        rail_df.update(rail_df.stop_name.str.upper())
        rail_df = rail_df.merge(rail_mapping, left_on='stop_name', right_on='stop_name')
        # for testing
        # temp = rail_df.merge(rail_mapping, how='left', left_on='STOP', right_on='stop_name')
        if len_before != len(rail_df):
            raise ValueError('error with rail stop mapping')
            exit()

        # @todo : make it so it just returns (only) stop_id (and mega_stop_id)?
        header = ['Serial_Nbr', 'Transaction_dtm', 'Dev_Operator', 'ctl_grp_short_desc', 'use_type_desc', 'bus_id',
                  'route_no', 'route_name', 'MEGA_STOP']
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



