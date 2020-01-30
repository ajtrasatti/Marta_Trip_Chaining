from .gtfs import GTFS, load_gtfs
from .schedule import ScheduleMaker
from .stop import Stop  # , BusStop
from .route import Route
# from .mega_stop_fac import MegaStopFac

from collections import defaultdict
from os.path import join
import os
import datetime as dt
import bisect

MAX_DIST = 700
# COMBINE = {"RAIL": ['RED', 'BLUE', 'GREEN', 'GOLD']}


class GtfsFac:
    """
    GTFS Factory - This class is used to organize many gtfs folders that span across many dates
    For any given date it will figure out which folder has the correct dates to look at
    and which service_id to look at (i.e. Weekday vs. Saturday vs. Sunday service)

    It will also manage all the stops and mega_stops to make sure that they span across all the dates consistently
        @ todo: add a stops.csv and mega_stops.csv file that can help keep track across iterations
        @ todo: it will check to make sure that two stops do not have different lat_longs
    """

    def __init__(self, folder_path, stops_file=None, mega_stops_file=None):
        """
        :param folder_path: folder that contains (only) many folders of gtfs folders for different dates
                - folder_path (containing the following)
                    > gtfs_01_13_2018
                        >> agency.txt
                        >> calendar_dates.txt
                        >> ...
                    > gtfs_01_30_2018
                        >> ...
                    > gtfs_mm_dd_YYYY
                        >> ...
                    > ...
        :param stops_file: will be added so that mega stop names stay consistent over time (file can be appended)
        :param mega_stops_file:  will be added so that mega stop names stay consistent over time (file can be appended)
        """

        self.folders = [name for name in os.listdir(folder_path) if
                        os.path.isdir(join(folder_path, name))]  # list of folders in directory

        def to_dt(folder_name):  # ex. gtfs_mm_dd_YYYY
            year = int(folder_name[-4:])
            month = int(folder_name[-10:-8])
            day = int(folder_name[-7:-5])
            return dt.datetime(year, month, day)

        self.dates = sorted([to_dt(name) for name in self.folders])
        print(self.dates)

        # Finding all stops across GTFS
        self.all_route_stops = None
        for folder, date in zip(self.folders, self.dates):
            # build a scheduler and get the self.route_stops from each append after dropping duplicates
            gtfs = load_gtfs(join(folder_path, folder))
            scheduler = ScheduleMaker(gtfs['trips'], gtfs['stop_times'], gtfs['stops'], gtfs['routes'])
            route_stops = scheduler.get_route_stops(direction=False, split=False)
            if self.all_route_stops is None:  # first time
                self.all_route_stops = route_stops
            else:
                self.all_route_stops.append(route_stops)
                cols = ['route_short_name', 'stop_id', 'stop_lat', 'stop_lon']
                self.all_route_stops.drop_duplicates(subset=cols)
        self.all_route_stops.to_csv(join(folder_path, "all_stops.csv"))

        self.route_dict = self.build_route_dict(self.all_route_stops, directions=False)
        # build paired stops
        # self.mega_stops = self.build_mega_stop_dict(routes_dict)

        # @ todo : use mega stops?
        # combine mega stops across routes

        # self.stops = {}
        # self.mega_stops = {}

        # self.megas =

        # self.gtfs_dict = {}
        # # @ todo : move route_dict down a level and use below
        # for folder, date in zip(self.folders, self.dates):
        #     self.gtfs_dict[date] = GTFS(join(folder_path, folder), date, self.mega_stops)

            # self.stops = ??
            # self.megas = append??

    def build_route_dict(self, route_stops, combine=None, directions=False):
        """
        :param directions:
        :param combine: dictionary (ex. {'Rail': ['BLUE', 'GOLD']}) of routes to combine
            - because of gate system vs. tap onto vehicle
        :param route_stops: df with columns (route_id, direction, stop_id, lat, lon)
            - Note the combination of route_id, direction, and stop_id should be a unique identifier

        :return: {route_id : Route(route_id,[Stop(stop_id,lat,lon)]
            - might also want to keep track of which routes/directions each stop belongs too
            - Also want to keep track of all the stops
            - probably have a stop_fac that knows all stops, and gets_stop
        """
        route_names = route_stops.route_short_name.drop_duplicates()
        route_dict = {route: defaultdict(list) for route in route_names}

        for route_id, stop_df in route_stops.groupby(['route_short_name']):
            stop_set = {Stop(s.stop_id, s.stop_lat, s.stop_lon) for s in stop_df.itertuples()}
            route_dict[route_id] = Route(route_id, stop_set)

        return route_dict

    def get_gtfs_routes_dict(self, date):
        return self.route_dict
        # return self.get_gtfs_network(date).routes_dict

    # def get_gtfs_network(self, date):
    #     ind = bisect.bisect_right(self.dates, date) - 1  # find index of last date that the gtfs data was updated
    #     print(self.dates, date)
    #     print("ind", ind)
    #     ind_date = self.dates[ind]  # get the date to use as index for gtfs dictionary
    #     print("date, ind_date", ind_date, date)
    #     return self.gtfs_dict[ind_date].get_network(date)

    # def get_megas(self):
    #     return self.megas

    # def export_megas(self, filename, date):
    #     self.gtfs_dict[date].export_megas(filename, date)




    # def build_route_dict(self, route_stops, combine=None, directions=False):
    #     """
    #     :param directions:
    #     :param combine: dictionary (ex. {'Rail': ['BLUE', 'GOLD']}) of routes to combine
    #         - because of gate system vs. tap onto vehicle
    #     :param route_stops: df with columns (route_id, direction, stop_id, lat, lon)
    #         - Note the combination of route_id, direction, and stop_id should be a unique identifier
    #
    #     :return: {route_id : Route(route_id,[Stop(stop_id,lat,lon)]
    #         - might also want to keep track of which routes/directions each stop belongs too
    #         - Also want to keep track of all the stops
    #         - probably have a stop_fac that knows all stops, and gets_stop
    #     """
    #     route_names = route_stops.route_short_name.drop_duplicates()
    #     route_dict = {route: defaultdict(list) for route in route_names}
    #     # for group_name, stop_df in route_stops.groupby(['route_short_name', 'direction_id']):
    #     #     route_dict[group_name[0]][group_name[1]] = [Stop(s.stop_id, s.stop_lat, s.stop_lon)
    #     #                                                 for s in stop_df.itertuples()]
    #     if combine:
    #         combines = {}
    #         to_combine =
    #
    #     for route_id, stop_df in route_stops.groupby(['route_short_name']):
    #         stop_set = {Stop(s.stop_id, s.stop_lat, s.stop_lon) for s in stop_df.itertuples()}
    #         if not combine or route_id not in to_combine:
    #             route_dict[route_id] = Route(route_id, stop_set)
    #     for k in combine.keys():
    #         route_dict[k] = Route(k, combines[k])
    #
    #     return route_dict

    # def build_mega_stop_dict(self, routes_dict):
    #     """
    #     @document
    #     :param routes_dict: # dict {route_id : {direction : [mega_ids]}}
    #     :return: dict {route_id : [MegaStops]}
    #     """
    #     route_mega_stop_dict = {}
    #     MSF = MegaStopFac(MAX_DIST)
    #     for route in routes_dict.keys():
    #         route_mega_stop_dict[route] = MSF.get_mega_stops(routes_dict[route][0], routes_dict[route][1]) # this makes a route??
    #
    #     return route_mega_stop_dict  # dict {route_id : [PairedStop]}