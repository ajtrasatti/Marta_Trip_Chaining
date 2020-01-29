from .gtfs import GTFS,load_gtfs
from .schedule import ScheduleMaker
from .stop import BusStop
from .mega_stop_fac import MegaStopFac
from collections import defaultdict
from os.path import join
import os
import datetime as dt
import bisect


MAX_DIST = 700

class GtfsFac:
    """
    GTFS Factory - This class is used to organize many gtfs folders that span across many dates
    For any given date it will figure out which folder has the correct dates to look at
    and which service_id to look at (i.e. Weekday vs. Saturday vs. Sunday service)

    It will also manage all the stops and mega_stops to make sure that they span across all the dates consistently
        @ todo: add a stops.csv and mega_stops.csv file that can help keep track across iterations
    ex. {stop_id : {"stop_id" : stop_id, "route" : 87, "lat_lon" : [39.345,-87.3423] },
             stop_id : {...}, stop_id : {...}, ...
        }

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

        self.folders = [name for name in os.listdir(folder_path) if os.path.isdir(join(folder_path,name))]  # list of folders in directory

        to_dt = lambda folder_name: dt.datetime(int(folder_name[-4:]), int(folder_name[-10:-8]), int(folder_name[-7:-5]))
        self.dates = sorted([to_dt(name) for name in self.folders])  # ex. gtfs_mm_dd_YYYY
        print(self.dates)
        self.gtfs_dict = {}
        self.stops = {}
        self.mega_stops = {}
        self.route_stops = None

        # MAKING MEGA STOPS
        for folder, date in zip(self.folders, self.dates):
            # build a scheduler and get the self.route_stops from each append after dropping duplicates
            gtfs = load_gtfs(join(folder_path, folder))
            scheduler = ScheduleMaker(gtfs['trips'], gtfs['stop_times'], gtfs['stops'], gtfs['routes'])
            route_stops = scheduler.get_stops(split=False)
            if self.route_stops is None: # first time
                self.route_stops = route_stops
            else:
                self.route_stops.append(route_stops)
                cols = ['route_short_name', 'direction_id', 'stop_id', 'stop_lat', 'stop_lon']
                self.route_stops.drop_duplicates(subset=cols)

        self.route_stops.to_csv(join(folder_path, "all_stops.csv"))

        routes_dict = self.build_route_dict(self.route_stops)
        # build paired stops
        self.mega_stops = self.build_mega_stop_dict(routes_dict)

        # @ todo : combine mega stops across routes
        # combine mega stops across routes
        # self.megas =

        # @ todo : pass in the mega stops to gtfs objects
        for folder, date in zip(self.folders, self.dates):
            self.gtfs_dict[date] = GTFS(join(folder_path, folder), date, self.mega_stops)

            # self.stops = ??
            # self.megas = append??
    def build_route_dict(self, route_stops):
        """
        :param route_stops: df
        :return:
        """
        route_names = route_stops.route_short_name.drop_duplicates()
        route_dict = {route: defaultdict(list) for route in route_names}
        for group_name, stop_df in route_stops.groupby(['route_short_name', 'direction_id']):
            route_dict[group_name[0]][group_name[1]] = [BusStop(s.stop_id, s.stop_lat, s.stop_lon)  # @todo change name from bus stop
                                                        for s in stop_df.itertuples()]
        return route_dict

    def build_mega_stop_dict(self, routes_dict):
        """
        @document
        :param routes_dict: # dict {route_id : {direction : [mega_ids]}}
        :return: dict {route_id : [MegaStops]}
        """
        route_mega_stop_dict = {}
        MSF = MegaStopFac(MAX_DIST)
        for route in routes_dict.keys():
            route_mega_stop_dict[route] = MSF.get_mega_stops(routes_dict[route][0], routes_dict[route][1]) # this makes a route??

        return route_mega_stop_dict  # dict {route_id : [PairedStop]}


    def get_gtfs_network(self, date):
        ind = bisect.bisect_right(self.dates, date) - 1  # find index of last date that the gtfs data was updated
        print(self.dates, date)
        print("ind", ind)
        ind_date = self.dates[ind]  # get the date to use as index for gtfs dictionary
        print("date, ind_date", ind_date, date)
        return self.gtfs_dict[ind_date].get_network(date)

    def get_gtfs_routes_dict(self,date):
        return self.get_gtfs_network(date).routes_dict

    def get_megas(self):
        return self.megas

    def export_megas(self, filename, date):
        self.gtfs_dict[date].export_megas(filename, date)



