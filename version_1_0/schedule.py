"""
@author Joshua E. Morgan, jmorgan63@gatech.edu
Pascal Van Henteryck Lab
v_0.0
"""

from collections import defaultdict
from stop import Stop, BusStop, TrainStop

class ScheduleMaker:
    """
    This class builds a daily service table or schedule based off of the gtfs day for a given day.
    attributes:
        - trips - pd.DataFrame that coresponds to the trips table in the gtfs data set
        - cal - pd.DataFrame that corresponds to the calendar table in the gtfs data set
        - stop_times - pd.DataFrame that coresponds to the stop_times table in the gtfs data set
        - stops - pd.DataFrame that corresponds to the stops table in the gtfs data set
        - routes - pd.DataFrame that corresponds to the routes table in the gtfs data set
    """

    def __init__(self, trips, calendar, stop_times, stops,routes):
        """

        :param trips: pd.DataFrame that coresponds to the trips table in the gtfs data set
        :param calendar: pd.DataFrame that corresponds to the calendar table in the gtfs data set
        :param stop_times: pd.DataFrame that coresponds to the stop_times table in the gtfs data set
        :param stops: pd.DataFrame that corresponds to the stops table in the gtfs data set
        :param routes: pd.DataFrame that corresponds to the routes table in the gtfs data set
        """
        self.trips = trips
        self.cal = calendar
        self.stop_times = stop_times
        self.stops = stops
        self.routes = routes



    def build_daily_table(self, day, split=True):
        """
        Builds a schedule table for a day of gtfs data
        :param day: dt.DateTime object that contains the day of interest
        :param split: Boolean, default true, returns the dataframe split into a bus or train set
        :return: if split - return tuple of pd.Data frame (train_table,bus_table) other was weekly schedule
        """
        service_id = self.get_service_type(day)
        trip_w_routes = self.trips[self.trips.service_id == service_id].merge(self.routes[['route_id', 'route_short_name']],
                                                                    on=['route_id'])
        route_stops = self.stop_times.merge(
            trip_w_routes[['route_id', 'trip_id', 'direction_id', 'block_id', 'route_short_name', 'service_id']],
            on=['trip_id'])
        self.route_stops = route_stops.merge(self.stops[['stop_id', 'stop_lat', 'stop_lon']])

        if split:
            self.train_table = self.route_stops[self.route_stops.route_short_name.isin(['RED', 'BLUE', 'GREEN', 'YELLOW'])]
            self.bus_table = self.route_stops[~(self.route_stops.route_short_name.isin(['RED', 'BLUE', 'GREEN', 'YELLOW']))]
            return self.train_table, self.bus_table
        else:
            return route_stops


    def get_service_type(self, day):
        """
        Finds the specific service type for a given day
        :param day: dt.DateTime object containing the date of the rest
        :return: int, the service type of the
        """
        day_o_week = day.weekday()
        for tup in self.cal.itertuples():
            if tup[day_o_week + 2] == 1:
                return tup.service_id

    def build_stops(self, df):
        """

        :param df:
        :return:
        """
        for group_name, stop_df in df.groupby(['route_short_name', 'direction_id']):
            self.route_dict[group_name[0]][group_name[1]] = [BusStop(s.stop_id, s.stop_lat, s.stop_lon) for s in
                                                         stop_df.itertuples()]
        return self.route_dict

    def build_train_stops(self, train_df):
        """

        :param df:
        :return:
        """
        _ = []
        # group these together at
        for group_name, s in train_df.groupby('stop_id'):
            _.append(TrainStop(group_name, s.stop_lat.mean(),
                               s.stop_lon.mean(), s['route_short_name'].tolist()))
        return _

    def build_train_stop_dict(self, train_df):
        _ = {}
        for group_name, stops in train_df.groupby('route_short_name'):
            _[group_name] = [TrainStop(group_name, s.stop_lat, s.stop_lon,group_name)
                                for s in stops.itertuples()]
        return _

    def get_stops(self):
        """
        
        :param df: 
        :return: 
        """
        cols = ['route_short_name', 'direction_id', 'stop_id', 'stop_lat', 'stop_lon']
        bus = self.bus_table.drop_duplicates(subset=cols)
        bus = bus[cols]
        train = self.train_table.drop_duplicates(subset=cols)
        train = train[cols]
        return bus, train

    def get_routes(self):
        """
        Extracts all of the routes from the table
        :return: dict {route_id:{0:[inbound stops], 1:[outboundstops]}
        """
        # take the schedule and get all of the unique (route,stop, directions)
        bus_df,train_df = self.get_stops()
        train_df.to_csv("train_df.csv")
        route_names = bus_df.route_short_name.drop_duplicates()
        self.route_dict = {route: defaultdict(list) for route in route_names}
        return self.build_stops(bus_df), self.build_train_stop_dict(train_df)

    def get_trains_dict(self):
        """"""
        pass