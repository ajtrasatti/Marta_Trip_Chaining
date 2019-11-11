
import pandas as pd

class Breeze_Loader:

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

    def match_rail_stops(self, rail_df, rail_mapping, network):
        """

        :param rail_df:
        :param rail_mapping:
        :param network:
        :return:
        """
        pass


    def match_2_apc(self, bus_df, apc_df):
        """
        this function matches the breeze and apc data frames
        :param bus_df:
        :param apc_df:
        :return: pd.DataFrame containing the breeze data with the stops
        """
        apc_df = apc_df.sort_values(by='ARRIVAL_DTM')
        apc_g = apc_df.groupby("VECHILE_TAG")
        bus_g = bus_df.groupby('bus_id')
        buses = list(pd.unique(apc_df['VECHILE_TAG']))

        def get_lat_lon(df, row):
            """
            note this function could be replaced by building a set of cutpoints and constraints
            Then implementing a search tree to determine the location of a given route in this space
            """
            return df.loc[(df['ARRIVAL_DTM'] - row.Transaction_dtm).abs().idxmin(), "MEGA_STOP"]

        for bus in buses:
            if bus in bus_g.groups:
                temp1 = apc_g.get_group(bus)
                temp2 = bus_g.get_group(bus)
                bus_df.loc[temp2.index, 'STOP_ID'] = temp2.apply(lambda row: get_lat_lon(temp1, row), axis=1)
        return bus_df

class Bus_Stop_Tree:

    def __init__(self, bus_df, lower, upper):
        pass
        """
        need a constraint that determines between two stops 
        """

