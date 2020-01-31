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
        """
        :param vehicle_apc_df: pandas dataframe for a given vehicle_id
        columns include "ROUTE_ABBR", "ARRIVAL_DTM", "DEPARTURE_DTM", "stop_id" and others
        """
        cols = ["ROUTE_ABBR", "ARRIVAL_DTM", "DEPARTURE_DTM", "stop_id", "ROUTE_DIRECTION_NAME"]
        self.df = vehicle_apc_df[cols].sort_values("ARRIVAL_DTM").reset_index(drop=True)
        self.times = list(self.df.ARRIVAL_DTM)

    def find_time_index(self, time):  # , route_id):
        """
        This bus search is for a specific vehicle number
        This method finds the index for the closet time for a route to determine what stop the passenger got on
        :param time: transaction time
        :param route_id: route number
        :return: index of pandas dataframe to use
        """
        return bisect.bisect_right(self.times, time)

    def find_apc_row(self, time, always_after=True):  # , route_id):
        """
        This bus search is for a specific vehicle number
        This method finds the index for the closet time for a route to determine what stop the passenger got on
        :param time: transaction time
        :param always_after: boolean for whether you want to match it to a previous row or closest
        :return: return the row from the APC data
            - includes stop_id, ROUTE_ABBR, ARRIVAL_DTM, DEPARTURE_DTM
        """
        index = self.find_time_index(time)  # , route_id)
        if always_after:  # Assume that they get on at the last place bus logged a time (check time elapse later)
            if index == 0:
                # ensures that the first time is used
                loc = index
            else:
                loc = index - 1  # This version if you always want the bus to have stopped first
            return self.df.loc[loc]
        else:  # In this case you pick the time that is closer whether it is before or after
            if index == 0:
                # ensures that the first time is used
                loc = index
            elif index == len(self.times):
                # ensures that the last time is used
                loc = index - 1
            else:
                t1 = abs(time - self.times[index])
                t2 = abs(time - self.times[index - 1])
                if t1 < t2:
                    loc = index
                else:
                    loc = index - 1
                # if min(t1, t2).seconds > 600:
                #     print(min(t1, t2), t1 < t2, t2 < t1, ret.ARRIVAL_DTM, ret.DEPARTURE_DTM)
                return self.df.loc[loc]

