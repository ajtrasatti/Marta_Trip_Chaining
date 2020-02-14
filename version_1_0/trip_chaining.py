import numpy as np
import pandas as pd
import datetime as dt
import folium
from collections import defaultdict
from gtfs import Network

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
        - state - this is the current state of the FSM

        - tracking: array of string keys for self.trips that are going to be the columns of trips_df
        - trips: dictionary {col_key: [values]} for all trips of a user
        - trip: dictionary {col_key: value} for a given trips
        - Ex. the use for self.tracking, self.trips, and self.trip in finish_trip()
        # for k in self.tracking:
        #     self.trips[k].append(self.trip[k])
    """
    def __init__(self):
        self.state = None
        self.network = Network()

        self.tracking = ["trip_id", "breeze_id", "start_stop", "start_time", "end_stop", "end_time",
                         "stops", "routes", "num_legs", "used_bus", "used_train"]
        self.trips = defaultdict(lambda: [])  # For everything
        self.trip = defaultdict(lambda: np.nan)

        self.trip_df = None

    @staticmethod
    def is_rail(dev_op):
        """
        :param dev_op: ex. "MARTA Bus" or "MARTA Rail"
        :return: 1 if rail, 0 if bus
        """
        # print(dev_op, "RAIL" in dev_op.upper())
        if "RAIL" in dev_op:
            return 1
        else:
            return 0

    def is_bus(self, dev_op):
        """
        :param dev_op: ex. "MARTA Bus" or "MARTA Rail"
        :return: 0 if rail, 1 if bus
        """
        return 1 - self.is_rail(dev_op)

    def valid_transfer(self, stop_id, route_id):
        """
        Check to see if the next stop is accessible from previous route (within a maximum distance)
        :param stop_id: the stop_id for the next leg
        :param route_id: the route of the last leg

        :return: boolean representing if it is a valid transfer
        """
        valid_transition = self.network.get_transition(stop_id, route_id, ret_bool=True)
        return valid_transition

    def start_trip(self, first_leg):
        """
        Create the the trip using information from first leg
        :param first_leg: a pandas row from "breeze_output.csv"
        """
        self.state = "start"
        stop_id = int(first_leg.stop_id)
        route_id = int(first_leg.MATCH_ROUTE)
        self.trip = defaultdict(lambda: np.nan)
        self.trip["breeze_id"] = first_leg.Serial_Nbr
        self.trip["start_time"] = first_leg.Transaction_dtm
        self.trip["start_stop"] = stop_id
        self.trip["routes"] = [route_id]
        self.trip["stops"] = [stop_id]
        self.trip["used_bus"] = self.is_rail(first_leg.Dev_Operator)
        self.trip["used_train"] = self.is_bus(first_leg.Dev_Operator)
        self.trip["directions"] = [first_leg.MATCH_DIRECTION]
        self.trip["num_legs"] = 1
        global trip_id
        self.trip["trip_id"] = trip_id

        trip_id += 1

    def same_trip(self, next_leg):
        """
        This check to see if next leg meets criteria to chain it to previous leg
        Criteria
            1. Time of leg is less than two hours of start of trip
            2. Not if it is a return trip
                - return trip if they get back on a line they have already used

        :param next_leg: row of pandas df
        :return: boolean for if the trip leg is part of same trip as previous leg
        """
        time_dif = (next_leg.Transaction_dtm - self.trip["start_time"])
        within_time_limit = time_dif < dt.timedelta(hours=2)  # @todo: MAX TIME Global parameter

        # rail = next_leg.MATCH_ROUTE == 0
        not_return_trip = next_leg.MATCH_ROUTE not in self.trip["routes"]  # make sure it is not the return trip

        cur_route = self.trip["routes"][-1]

        valid_transition = self.network.get_transition(next_leg.stop_id, cur_route, ret_bool=True)
        # print(valid_transition)

        end_of_last_trip = next_leg.use_type_desc == "Exit (Tag Off)"

        return (within_time_limit and not_return_trip and valid_transition) or end_of_last_trip

    def trip_chain(self, next_leg):
        """

        :param next_leg:
        :return:
        """
        # self.trip["end_time"] = next_leg.Transaction_dtm
        stop_id = int(next_leg.stop_id)
        route_id = int(next_leg.MATCH_ROUTE)
        if self.state != "exit":  # if last stop wasn't exit (i.e. it was recorded) - record where they got on next time
            self.trip["stops"].append(stop_id)
        if next_leg.use_type_desc != "Exit (Tag Off)":  # was not an exit
            self.state = "transfer"
            self.trip["end_stop"] = np.nan  # remove previous entry - have not found end yet
            self.trip["end_time"] = np.nan  # remove previous entry - have not found end yet
            self.trip["routes"].append(route_id)
            self.trip["used_train"] += self.is_rail(next_leg.Dev_Operator)
            self.trip["used_bus"] += self.is_bus(next_leg.Dev_Operator)
            self.trip["num_legs"] += 1
        else:  # was an exit
            self.state = "exit"
            self.trip["end_stop"] = int(stop_id)
            self.trip["end_time"] = next_leg.Transaction_dtm

    def valid_destination(self, next_stop_id, route_id, next_route_id):
        """
        Check to see if the next leg is a possible destination of the last leg
            - Check if stop is far enough away from other stops on trip
                - don't want to check except at end (ex. exit at rail station then get on nearby bus)
                - this would be to make sure that the next leg is actually the destination of their last leg
        :param next_stop_id: the stop_id for the next leg
        :param route_id: the route of the last leg
        :param next_route_id: route_id for next leg
        :return: boolean representing if it is a valid transfer
        """
        if not self.valid_transfer(next_stop_id, route_id):
            return False

        # check that stop isn't too close to any previous stops on trips
        for prev_stop in self.trip["stops"]:
            # check to see next_stop is walking distance from any previous stop
            if next_stop_id in self.network.get_transition(prev_stop, next_route_id):
                print("NOT VALID")
                return False
        # else
        return True

    def finish_trip(self, next_leg=None):
        """
        First,
            - we don't yet have an end stop for trip (ex. have where they exited rail)
            - and we have a next trip for breeze_id
            Then we check to see if the origin of next trip is possible destination of current trip
        Then add trip to the log
        :param next_leg: row from pandas dataframe for first leg of next trip
        """
        self.state = "Finish"
        if next_leg is not None:
            next_stop_id = int(next_leg.stop_id)
            next_route_id = int(next_leg.MATCH_ROUTE)
            # print(self.trip["end_stop"], np.isnan(self.trip["end_stop"]))
            if np.isnan(self.trip["end_stop"]):
                print("looking at next leg")
                route_id = self.trip["routes"][-1]
                if self.valid_destination(next_stop_id, route_id, next_route_id):
                    self.trip["end_stop"] = next_stop_id
                    self.trip["stops"].append(next_stop_id)
                    # self.trip["end_time"] =  # @todo: need to look at apc data to find end time for buses

        for k in self.tracking:
            self.trips[k].append(self.trip[k])
        # return self.trips

    def trip_chain_df(self, breeze_df=None, breeze_number=None):
        print("Starting for person ", breeze_number, len(breeze_df))
        if breeze_df is None:
            breeze_df = self.df
        breeze_df.Transaction_dtm = pd.to_datetime(breeze_df.Transaction_dtm)

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
        # trip_df.to_csv("trips.csv")
        print("TEST TEST", len(trip_df), len(breeze_df), breeze_number)
        return trip_df


def test():
    # For a given df that corresponds to an individual, go through each row and update the state
    filename = "/Users/anthonytrasatti/Desktop/Research/Marta/Trip-Chaining-master/Data/People/4089507211.csv"

    df = pd.read_csv(filename, index_col=0)

    x = df.head()
    print(df.columns)
    print(x)

    # MAIN METHOD done for each person's df

    trip_chain = TripChain()
    trip_chain.trip_chain_df(df, breeze_number=filename.split("/")[-1].split(".csv")[0])


if __name__ == '__main__':
    test()



