"""
@author Joshua E. Morgan, jmorgan63@gatech.edu
Pascal Van Henteryck Lab
v_0.0
"""

from collections import defaultdict
from .stop import BusStop, TrainStop


class ScheduleMaker:
    """
    This class builds a daily service table or schedule based off of the gtfs day for a given day.
    attributes:
    """

    def __init__(self, trips, stop_times, stops, routes, service_id = None):
        """
        :param trips: pd.DataFrame that coresponds to the trips table in the gtfs data set
        :param calendar: pd.DataFrame that corresponds to the calendar table in the gtfs data set
        :param stop_times: pd.DataFrame that coresponds to the stop_times table in the gtfs data set
        :param stops: pd.DataFrame that corresponds to the stops table in the gtfs data set
        :param routes: pd.DataFrame that corresponds to the routes table in the gtfs data set
        :param service_id: (3,4,5) from gtfs calendar representing (saturday,sunday, or weekday) resp.
        """

        self.gtfs_trips = trips
        self.gtfs_stop_times = stop_times
        self.gtfs_stops = stops
        self.gtfs_routes = routes
        self.service_id = service_id
        if service_id:
            trips = self.gtfs_trips[self.gtfs_trips.service_id == service_id]
        else:
            trips = self.gtfs_trips
        trips = trips.merge(self.gtfs_routes[['route_id', 'route_short_name']], on=['route_id'])
        route_stops = self.gtfs_stop_times.merge(
            trips[['trip_id', 'direction_id', 'block_id', 'route_short_name', 'service_id']],  # removed route_id **
            on=['trip_id'])
        self.route_stops = route_stops.merge(self.gtfs_stops[['stop_id', 'stop_lat', 'stop_lon']])

        # self.train_table = self.route_stops[
        #     self.route_stops.route_short_name.isin(['RED', 'BLUE', 'GREEN', 'GOLD'])]
        # self.bus_table = self.route_stops[
        #     ~(self.route_stops.route_short_name.isin(['RED', 'BLUE', 'GREEN', 'GOLD']))]

    def get_stops(self, split=False):
        """
        :param split: if you want to split bus and train table
        :return: stops with
        """
        cols = ['route_short_name', 'direction_id', 'stop_id', 'stop_lat', 'stop_lon']
        if split:
            bus = self.bus_table.drop_duplicates(subset=cols)
            bus = bus[cols]
            train = self.train_table.drop_duplicates(subset=cols)
            train = train[cols]
            return bus, train
        else:
            return self.route_stops.drop_duplicates(subset=cols)

    # def get_stops_multiple(self, split=False):
    #     """
    #     :param split: if you want to split bus and train table
    #     :return: stops with
    #     """
    #     cols = ['route_short_name', 'direction_id', 'stop_id', 'stop_lat', 'stop_lon']
    #     if split:
    #         bus = self.bus_table.drop_duplicates(subset=cols)
    #         bus = bus[cols]
    #         train = self.train_table.drop_duplicates(subset=cols)
    #         train = train[cols]
    #         return bus, train
    #     else:
    #         return self.route_stops.drop_duplicates(subset=cols)

    # def build_bus_stops(self, bus_df):
    #     """
    #     :param bus_df:
    #     :return:
    #     """
    #     bus_df
    #     route_names = bus_df.route_short_name.drop_duplicates()
    #     route_dict = {route: defaultdict(list) for route in route_names}
    #     for group_name, stop_df in bus_df.groupby(['route_short_name', 'direction_id']):
    #         route_dict[group_name[0]][group_name[1]] = [BusStop(s.stop_id, s.stop_lat, s.stop_lon)
    #                                                     for s in stop_df.itertuples()]
    #     return route_dict

    def build_train_stop_dict(self, train_df):
        """
        :param train_df:
        :return:
        """
        train_dict = {}
        for group_name, stops in train_df.groupby('route_short_name'):
            train_dict[group_name] = [TrainStop(group_name, s.stop_lat, s.stop_lon, group_name)
                                      for s in stops.itertuples()]
        return train_dict

    def get_routes(self):
        """
        Extracts all of the routes from the table
        :return: dict {route_id:{0:[inbound stops], 1:[outboundstops]}
        """
        # take the schedule and get all of the unique (route,stop, directions)
        bus_df, train_df = self.get_stops(split=True)
        # train_df.to_csv("train_df.csv")

        return self.build_bus_stops(bus_df), self.build_train_stop_dict(train_df)

    def get_trains_dict(self):
        """"""
        pass
