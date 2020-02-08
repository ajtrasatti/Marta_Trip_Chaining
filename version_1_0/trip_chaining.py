import numpy as np
import pandas as pd
import datetime as dt
import folium
from collections import defaultdict

#######################
global trip_id
trip_id = 1000000
########################

class TripChain:
    """ 
    This implements the finite state machine design pattern for
    state space:
        - 0 - start - occurs when a trip is being built
        - 1 - error
        - 2 - in train - occurs when a customers has entered into a train
        - 3 - out train - occurs when a customer exits a train
        - 4 - bus - occurs when a customer has entered into a bus
        - 5 - end

    :attributes:
        - trans_dist - distance that limits the transitions this is the maximum transfer distance
        - trans_time - transfer time - max transfer time

        - network - network object
        - trip_state - this is the current state of the FSM

    """
    def __init__(self):
        self.state = None
        self.trip = None
        self.tracking = ["trip_id", "breeze_id", "start_time", "start_stop", "end_stop", "stops", "routes",
                         "num_legs", "used_bus", "used_train"]
        self.trips = defaultdict(lambda: [])
        self.trip_df = None

    def is_rail(self, dev_op):
        print(dev_op, "RAIL" in dev_op.upper())
        if "RAIL" in dev_op:
            return 1
        else:
            print("WAS BUS")
            return 0

    def is_bus(self, dev_op):
        return 1 - self.is_rail(dev_op)

    def start_trip(self, cur_leg):
        """
        This trip
        :param cur_leg:
        :return:
        """
        self.state = "start"
        self.trip = defaultdict(lambda: np.nan)
        self.trip["breeze_id"] = cur_leg.Serial_Nbr
        self.trip["start_time"] = cur_leg.Transaction_dtm
        self.trip["start_stop"] = cur_leg.stop_id
        self.trip["used_bus"] = self.is_rail(cur_leg.Dev_Operator)
        self.trip["used_train"] = self.is_bus(cur_leg.Dev_Operator)
        self.trip["routes"] = [cur_leg.MATCH_ROUTE]
        self.trip["stops"] = [cur_leg.stop_id]
        self.trip["directions"] = [cur_leg.MATCH_DIRECTION]
        self.trip["num_legs"] = 1
        global trip_id
        self.trip["trip_id"] = trip_id

        trip_id += 1


    def same_trip(self, next_leg):
        """
        This check to see if next leg meets criteria to chain it to previous leg
        :param next_leg: row of pandas df
        :return: boolean for if the trip leg is part of same trip as previous leg
        """
        time_dif = (next_leg.Transaction_dtm - self.trip["start_time"])
        time_bol = time_dif < dt.timedelta(hours=2)

        rail = next_leg.MATCH_ROUTE == 0
        if rail:
            not_return = next_leg.stop_id not in self.trip["stops"] # make sure it is not the return trip
        else:
            not_return = next_leg.MATCH_ROUTE not in self.trip["routes"] # make sure it is not the return trip

        end = next_leg.use_type_desc == "Exit (Tag Off)"

        if (time_bol and not_return) or end:  # less than 2 hours
            return True
        else:
            return False

    def trip_chain(self, next_leg):
        # self.trip["end_time"] = next_leg.Transaction_dtm
        self.trip["end_stop"] = next_leg.stop_id
        self.trip["stops"].append(next_leg.stop_id)
        if next_leg.use_type_desc != "Exit (Tag Off)":
            self.state = "exit"
            self.trip["routes"].append(next_leg.MATCH_ROUTE)
            self.trip["used_train"] += self.is_rail(next_leg.Dev_Operator)
            self.trip["used_bus"] += self.is_bus(next_leg.Dev_Operator)
            self.trip["num_legs"] += 1
        else:
            self.state = "transfer"

    def finish_trip(self, next_leg=None):
        if next_leg is not None:
            pass  # @todo : add in look for destination
        for k in self.tracking:
            self.trips[k].append(self.trip[k])
        # return self.trips

    def trip_chain_df(self, breeze_df=None):
        if breeze_df is None:
            breeze_df = self.df

        iter_df = breeze_df.iloc[1:].iterrows()  # df iterator

        self.start_trip(breeze_df.iloc[0])
        for ind, trip_leg in iter_df:
            if self.same_trip(trip_leg):
                self.trip_chain(trip_leg)
            else:
                # attempt to add destination and add trip to trip df
                self.finish_trip(next_leg=trip_leg)
                self.start_trip(trip_leg)
        self.finish_trip()  # add unfinished trip to trip df

        trip_df = pd.DataFrame(self.trips)
        print(trip_df.head())
        trip_df.to_csv("trips.csv")
        print("TEST TEST", len(trip_df), len(breeze_df))
        return trip_df

def test():
    # For a given df that corresponds to an individual, go through each row and update the state
    filename = "/Users/anthonytrasatti/Desktop/Research/Marta/Trip-Chaining-master/Data/People/4089507211.csv"

    df = pd.read_csv(filename, index_col=0)
    df.Transaction_dtm = pd.to_datetime(df.Transaction_dtm)

    x = df.head()
    print(df.columns)
    print(x)

    # MAIN METHOD done for each person's df
    trip_chain = TripChain()
    trip_chain.trip_chain_df(df)


if __name__ == '__main__':
    test()



