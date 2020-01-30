"""
@author Anthony J. Trasatti , atrasatti3@gatech.edu
@author Joshua E. Morgan , jmorgan63@gatech.edu
Socially Aware Mobility (SAM) Lab, Georgia Tech
v_1.0
"""
import bisect


class BusSearch:
    """
    BusSearch is used by the breeze loader to find what bus the person got on
    """

    def __init__(self, vehicle_apc_df):  # , id=None):
        # {route_id : pandas_df (arrival_DTM, stop_id)
        self.df = vehicle_apc_df[["ROUTE_ABBR", "ARRIVAL_DTM", "DEPARTURE_DTM", "stop_id"]].sort_values("ARRIVAL_DTM").reset_index(drop=True)

        # self.vehicle_route_dict = {route_id: time_df.reset_index(drop=True) for route_id, time_df in temp.groupby("ROUTE_ABBR")}
        # self.times = {route_id: list(time_df.ARRIVAL_DTM) for route_id, time_df in self.vehicle_route_dict.items()}
        self.times = list(self.df.ARRIVAL_DTM)

    def find_time_index(self, time, route_id):
        """
        This bus search is for a specific vehicle number
        This method finds the index for the closet time for a route to determine what stop the passenger got on
        :param time: transaction time
        :param route_id: route number
        :return: index of pandas dataframe to use
        """
        return bisect.bisect_right(self.times, time)
        # if route_id in self.times:
        #
        # else:
        #     return None

    def find_stop_route(self, time, route_id):
        """
        This bus search is for a specific vehicle number
        This method finds the index for the closet time for a route to determine what stop the passenger got on
        :param time: transaction time
        :param route_id: route number
        :return: tuple of time, stop
        """

        index = self.find_time_index(time, route_id)
        if index is None:
            return None, None
        else:
            if index == 0:
                # ensures that the first time is used
                loc = index
            elif index == len(self.times):
                # ensures that the last time is used
                loc = index - 1
            else:
                if abs(time - self.times[index]) < abs(time - self.times[index - 1]):
                    loc = index
                else:
                    loc = index - 1
            # @todo - is times checking right? also probably want to do closer to right, self.times is sorted??
            ret = self.df.loc[loc]
            # @todo - should probably go from departure time -- need to make that a DTM
            if ret.ARRIVAL_DTM != self.times[loc]:
                print(ret.ARRIVAL_DTM, self.times[loc])
            return ret.ARRIVAL_DTM, ret.stop_id , ret.ROUTE_ABBR
